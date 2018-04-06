import matplotlib.pyplot as plt
import numpy as np
import spotlight
import re
import ast
import copy
import codecs


def reformat_file_and_keep_born_only_sentence_v3(path_file, path_file_out):
	with codecs.open(path_file, "r",encoding='utf-8', errors='ignore') as file_in:

	# reformat file welL!! close site property
		file_out = open(path_file_out, 'w', encoding='utf-8')
		end_flag = True

		list_of_lines = list()

		for line in file_in:
			line = line.strip()
			if len(list_of_lines) == 0:
				if not line.startswith("<site url="):
					continue
				else:
					list_of_lines.append(line)
					# new claim
					index_url = line.index("url=")
					index_dataitem = line.index("person=")
					index_end = line.index(">")
					url = line[index_url + 5: index_dataitem - 2]
					index_pref = url.index("://") + 3
					dataitem = line[index_dataitem + 8:index_end - 1].replace('"', '')
					dataitem = dataitem.replace(' AND was born', '')#[1:-1]
			elif line.startswith("<phrase>"):
				if "born" in line.lower() or dataitem.lower() in line.lower():
					list_of_lines.append(line)

			elif line.startswith("</site>"):

				list_of_lines.append(line)
				if len(list_of_lines) > 2:
					if list_of_lines.count("</site>")>1:
						print(list_of_lines)
					file_out.write(list_of_lines[0] + "\n")
					for l_app in list_of_lines[1:-1]:
						file_out.write("\t" + l_app+"\n")
					file_out.write(list_of_lines[len(list_of_lines)-1] + "\n")
				list_of_lines.clear()

		file_in.close()
		file_out.close()
		print("The xml file is now well formatted")

	return 1


def read_xml_file(path_file_out):
	domain_coverage = dict()
	num_sources = dict()
	text_dict = dict()

	###analyis_source_coverage
	##note : domain url = www.ibmd.com -- url = www.ibmd.com/shdoif034kj/dfs..
	# to create DICT : text_dict[dataitem][url] = str_text
	file_in = open(path_file_out, 'r',encoding='utf-8')
	cont_line = 0
	for line in file_in:
		cont_line += 1
		if cont_line % 10000 == 0: print("Read lines : " + str(cont_line))

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
			str_text = ""
			#if "born" in line:
			str_text = line.replace("<phrase>", "").replace("</phrase>", "")
			for line in file_in:
				cont_line += 1
				line = line.strip()
				if line.startswith("</site>"):
					end_flag = True
					break
				#if "born" in line:
				str_text += " " + line.replace("<phrase>", "").replace("</phrase>", "")

			if end_flag:
				if str_text != "":
					if dataitem not in text_dict:
						text_dict[dataitem] = dict()
					if url not in text_dict[dataitem]:
						text_dict[dataitem][url] = str_text

	file_in.close()
	print("Tot line number : " + str((cont_line)))
	print("number data items processed " + str(len(text_dict)))

	return domain_coverage, num_sources, text_dict


def get_occurrence_predicate_and_location_in_text_v3(text_dict_, url_dbpedia_spotlight_, already_processed_, file_out_):
	# only_place_filter = {'types': "DBpedia:Person,DBpedia:Place"}
	only_place_filter = {'types': "DBpedia:Place"}
	annot_values_dict = dict()

	ann_occu_dict = dict()
	predicate_occu_dict = dict()

	f_out = open(file_out_, 'a+',encoding='utf-8')
	d_processed = -1
	for d in text_dict_:
		#d = "Frank Soo AND was born"
		d_str = d.replace(" AND was born", "")
		d_processed +=1
		if d_processed % 10 == 0: print("Processed data item " + str(d_processed) + "/" + str(len(text_dict_)))
		# url == source

		for url in text_dict_[d]:
			#url = "https://en.wikipedia.org/wiki/Frank_Soo"
			if d in already_processed_:
				if url in already_processed_[d]:
					continue

			text_ = text_dict_[d][url]
			if d_str not in text_:
				continue
			if "born" not in text_:
				continue
			occurence_of_person_d = list()
			for match in re.finditer(d_str.lower(), text_.lower()):
				app_number = match.start()
				occurence_of_person_d.append(app_number)
			# find all occurences of "born"
			occ_predicate_index = list()
			#text_ = "Hello EveryBody! I am in Paris, I am Valentina and I was born in the beautiful city of Milano, but it is also true that I was born in Austria and Berlin. My mother born in Turin. My sister was born in the beautfiul land of Paris."
			phrases = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text_)
			n_ph_ = -1
			local_claim = dict()
			for ph_ in phrases:

				n_ph_ += 1
				if "born" not in ph_.lower():
					continue

				index_sentence = text_.index(ph_)
				distance_from_occ_pred = dict()
				for match in re.finditer("born", ph_.lower()):
					app_number = match.start()+ index_sentence
					occ_predicate_index.append(app_number)
					distance_from_occ_pred[app_number] = dict()
				# http://localhost/rest/annotate'
				cond_verified_ = False
				for subj_ind in occurence_of_person_d:
					for pred_ind in occ_predicate_index:
						if subj_ind < pred_ind :
							cond_verified_ = True
							break
				if not cond_verified_:
					continue

				try:
					index_entity_ann = dict()
					# ind_predicate = text_.lower().index("born")
					annotations = spotlight.annotate(url_dbpedia_spotlight_, ph_, confidence=0.5, support=5, filters=only_place_filter)
					for ann in annotations:
						off_set = ann["offset"] + index_sentence

						if ann['URI'] not in index_entity_ann:
							index_entity_ann[off_set] = set()
						index_entity_ann[off_set].add(ann['URI'])


					for pred_index in distance_from_occ_pred:
						app = copy.deepcopy(index_entity_ann)
						for ind_app in index_entity_ann:
							if ind_app < pred_index:
								del app[ind_app]
						if len(app) == 0:
							continue
						min_distance_index = min(app.keys(), key=lambda x: abs(x - pred_index))
						if min_distance_index - pred_index not in local_claim:
							#if there is another claim with the same min distance I prefere the one that it is wrtitten before before
							local_claim[min_distance_index-pred_index] = index_entity_ann[min_distance_index]

					#devo scrivere su file
				except spotlight.SpotlightException as e:
					a= 0#print(e)
					#print("no annotations of' DBpedia:Place' found for '" + str(d) + "' in the text provided '" + str(url) + "'")
				except:
					print("other error for " + str(d) + "\t" + str(url))

			#save occurrence of predicate and occcurence of annotated place
			if len(local_claim)>0:
				min_distance_index_absolute = min(local_claim.keys())
				index_entity_ann_uri = local_claim[min_distance_index_absolute]
				for loc_ in index_entity_ann_uri:
					str_out_claim = str(d) + '\t' + str(url) + '\t' + str(loc_) + '\n'
					f_out.write(str_out_claim)
					f_out.flush()


	# end dbpedia splotlight
	f_out.close()
	return predicate_occu_dict, ann_occu_dict


def get_claims_already_process(in_path):
	#line of the file example: str(d) + '\t' + str(url) + '\t' + str(loc_) + '\n'
	f_in = open(in_path, 'r', encoding='utf-8')
	already_processed = dict()
	for line in f_in:
		line = line.strip().split('\t')
		d = line[0]
		url = line[1]
		if d not in already_processed:
			already_processed[d] = set()
		already_processed[d].add(url)
	f_in.close()
	return already_processed


if __name__ == '__main__':
	#to change based on experimental settings
	# https://github.com/dbpedia-spotlight/dbpedia-spotlight
	url_dbpedia_spotlight = 'http://model.dbpedia-spotlight.org/en/annotate' # API
	#url_dbpedia_spotlight = 'http://localhost:2222/rest/annotate' #local annotations >java -jar dbpedia-spotlight-latest.jar en http://localhost:2222/rest
	path_file = 'person_birthLocation_webpage.xml'  # XML file -- input file where scraping information were collected
	claims_path = 'claims_.txt'  # Output FILE where the extrated claims are saved

	path_file_out = path_file.replace('.xml', '_well_formatted_v3.xml')
	try:
		fh = open(claims_path, 'r')
		fh.close()
	except:
		# if file does not exist, create it
		fh = open(claims_path, 'w')
		fh.close()

	reformat_file_and_keep_born_only_sentence_v3(path_file, path_file_out)
	#read well formatted xml file -- for each data item - source pair, it concatens the text contianed in the sentences extracted from the webpage
	domain_coverage_xml, num_sources_xml, text_dict_xml = read_xml_file(path_file_out)
	print(" - XML file read ")
	#retrive all pairs data item-source already processed (for which a claim has been already extracted)
	already_processed = dict()#get_claims_already_process(claims_path)
	#retrieve the pair (ccurrence of predicate "was born", LOCATION identify by spotlight) having the minimum distance
	#write the claim on a file
	predicate_occu_dict, ann_occu_dict = get_occurrence_predicate_and_location_in_text_v3(text_dict_xml, url_dbpedia_spotlight, already_processed, claims_path)
	print(" - All occurences of predicates and locations identified! ")
	print("End of the process")
	exit()

