import matplotlib.pyplot as plt
import numpy as np
import spotlight
import re
import ast
import codecs

def reformat_file(path_file, path_file_out):

	with codecs.open(path_file, "r",encoding='utf-8', errors='ignore') as file_in:
	#file_in = open(path_file, 'r')
	# reformat file welL!! close site property
		file_out = open(path_file_out, 'w',encoding='utf-8')
		end_flag = True
		for line in file_in:
			line = line.strip()
			if line.startswith("<site url="):
				if not end_flag:
					file_out.write("</site>\n")
				end_flag = False
				file_out.write(line+"\n")
			elif line.startswith("<phrase>"):
				file_out.write("\t" + line+"\n")
				for line in file_in:
					line = line.strip()
					if line.startswith("</site>"):
						file_out.write(line+"\n")
						end_flag = True
						break
					elif line.startswith("<site url="):
						end_flag = False
						file_out.write("</site>\n")
						file_out.write(line+"\n")
						break

					file_out.write(line+"\n")

		file_in.close()
		file_out.close()
		print("The xml file is now well formatted")


def read_xml_file(path_file_out):
	domain_coverage = dict()
	num_sources = dict()
	text_dict = dict()

	###analyis_source_coverage
	##note : domain url = www.ibmd.com -- url = www.ibmd.com/shdoif034kj/dfs..
	# to create DICT : text_dict[dataitem][url] = str_text
	file_in = open(path_file_out, 'r',encoding='utf-8')
	for line in file_in:
		line = line.strip()
		if line.startswith("<site url="):
			end_flag = False
			# new claim
			index_url = line.index("url=")
			index_dataitem = line.index("person=")
			index_end = line.index(">")
			url = line[index_url + 5: index_dataitem - 2]
			index_pref = url.index("://") + 3
			domain_url = url[:url[index_pref:].index("/") + index_pref]
			dataitem = line[index_dataitem + 8:index_end - 1].replace('"', '')

			if domain_url not in domain_coverage:
				domain_coverage[domain_url] = set()
			domain_coverage[domain_url].add(dataitem)

			if dataitem not in num_sources:
				num_sources[dataitem] = set()
			num_sources[dataitem].add(domain_url)
		# print()
		elif line.startswith("<phrase>"):
			str_text = line.replace("<phrase>", "").replace("</phrase>", "")
			for line in file_in:
				line = line.strip()
				if line.startswith("</site>"):
					end_flag = True
					break
				str_text += " " + line.replace("<phrase>", "").replace("</phrase>", "")

			if end_flag:
				if dataitem not in text_dict:
					text_dict[dataitem] = dict()
				if url not in text_dict[dataitem]:
					text_dict[dataitem][url] = str_text

	file_in.close()
	print("number data items processed " + str(len(text_dict)))

	return domain_coverage, num_sources, text_dict


def get_occurrence_predicate_and_location_in_text(text_dict_, url_dbpedia_spotlight_, already_processed_, file_out_):
	# only_place_filter = {'types': "DBpedia:Person,DBpedia:Place"}
	only_place_filter = {'types': "DBpedia:Place"}
	annot_values_dict = dict()

	ann_occu_dict = dict()
	predicate_occu_dict = dict()

	f_out = open(file_out_, 'a+',encoding='utf-8')

	for d in text_dict_:
		# url == source
		for url in text_dict_[d]:

			if d in already_processed_:
				if url in already_processed_[d]:
					continue

			text_ = text_dict_[d][url]

			if "born" not in text_:
				continue
			# find all occurences of "born"
			phrases = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text_)
			n_ph_ = -1
			for ph_ in phrases:

				n_ph_ += 1
				if "born" not in ph_:
					continue

				index_sentence = text_.index(ph_)
				occ_predicate_index = list()
				for match in re.finditer("born", ph_):
					occ_predicate_index.append(match.start()+ index_sentence)
				try:
					index_entity_ann = dict()
					annotations = spotlight.annotate(url_dbpedia_spotlight_, ph_, confidence=0.5, support=20, filters=only_place_filter)

					if d not in annot_values_dict:
						annot_values_dict[d] = set()
					for ann in annotations:
						off_set = ann["offset"] + index_sentence
						if ann['URI'] not in index_entity_ann:
							index_entity_ann[ann['URI']] = set()
						index_entity_ann[ann['URI']].add(off_set)

					if d not in ann_occu_dict:
						ann_occu_dict[d] = dict()
					ann_occu_dict[d][url] = index_entity_ann
					# for each d - source this dict contains all mentions index of Place in its webpage
					if d not in predicate_occu_dict:
						predicate_occu_dict[d] = dict()
					predicate_occu_dict[d][url] = occ_predicate_index
					# for each d - source this dict contains all occurrence of PREDICATE BORN in its webpage
					for pred_ind in occ_predicate_index:
						min_dist = 100000000
						min_location_uri = set()
						min_location_index = set()
						for uri_ in index_entity_ann:
							for uri_index in index_entity_ann[uri_]:
								if pred_ind < uri_index:
									dist_ = uri_index-pred_ind
									if dist_ < min_dist:
										min_dist = dist_
										min_location_uri.clear()
										min_location_uri.add(uri_)
										min_location_index.clear()
										min_location_index.add(uri_index)
									elif dist_ == min_dist:
										min_location_uri.add(uri_)
										min_location_index.add(uri_index)

						for loc_ in min_location_uri:
							app_index = ""
							for ind_ in min_location_index:
								if ind_ in index_entity_ann[loc_]:
									app_index = ind_
									break
							str_out = str(d) + '\t' + str(url) + '\t' + str(n_ph_) + '\t' + str(pred_ind) + '\t' + str(
								app_index) + '\t' + str(loc_) + '\n'
							f_out.write(str_out)

					#devo scrivere su file
				except spotlight.SpotlightException:
					aaa= 0
					#print("no annotations of' DBpedia:Place' found for '" + str(d) + "' in the text provided '" + str(url) + "'")
				except:
					print("other error for " + str(d) + "\t" + str(url))

			#save occurrence of predicate and occcurence of annotated place

				f_out.flush()


	# end dbpedia splotlight
	f_out.close()
	return predicate_occu_dict, ann_occu_dict

if __name__ == '__main__':

	# https://github.com/dbpedia-spotlight/dbpedia-spotlight
	url_dbpedia_spotlight = 'http://model.dbpedia-spotlight.org/en/annotate' # API
	#rl_dbpedia_spotlight = 'http://localhost:2222/rest/annotate' #local annotations >java -jar dbpedia-spotlight-latest.jar en http://localhost:2222/rest

	path_file = 'person_birthLocation_webpage.xml'  # XML file -- input file where scraping information were collected
	file_out_occurence = path_file.replace('.xml', '_occurences_birthLocation.xml')  # save information related to predicate and Place occurences
	claims_path = 'claims_.txt'  # Output FILE where the extrated claims are saved

	path_file_out = path_file.replace('.xml', '_well_formatted.xml')
	try:
		fh = open(file_out_occurence, 'r')
		fh.close()
	except:
		# if file does not exist, create it
		fh = open(file_out_occurence, 'w')
		fh.close()
	try:
		fh = open(claims_path, 'r')
		fh.close()
	except:
		# if file does not exist, create it
		fh = open(claims_path, 'w')
		fh.close()

	###analyis_source_coverage
	reformat_file(path_file, path_file_out)
	# concatenate all the sentence for each url-dataitem pair
	domain_coverage_xml, num_sources_xml, text_dict_xml = read_xml_file(path_file_out)
	print(" - XML file read ")

	already_processed = None#get_dataitem_and_url_already_annotated(file_out_occurence)

	#retrieve each occurrence of predicate "was born" in the text, and the occurrence of each LOCATION identify by spotlight
	predicate_occu_dict, ann_occu_dict = get_occurrence_predicate_and_location_in_text(text_dict_xml, url_dbpedia_spotlight, already_processed, file_out_occurence)
	print(" - All occurences of predicates and locations identified! ")
