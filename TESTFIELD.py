from owlready2 import *
onto = get_ontology("file://D:/INZ/People.owl").load()
text0="janna is a great"
text2 = text0.replace(",", "")
text3 = text2.replace('.', '')
text4 = text3.split()
text_ready_to_use = []
for every_word in text4:
    word = every_word
    big_word = word.capitalize()
    text_ready_to_use.append(big_word)
onto_list_classes_raw = list(onto.classes())
onto_list_classes = list(onto_list_classes_raw)
onto_list_individuals_raw = list(onto.individuals())
onto_list_individuals = list(onto_list_individuals_raw)
onto_list_raw = []
onto_list_raw.extend(onto_list_classes)
onto_list_raw.extend(onto_list_individuals)
onto_list = []
onto_list.extend(onto_list_raw)
onto_list = [str(i) for i in onto_list]
search_all_resp=[]
for every in onto_list:
       search_all_resp.append(str(every).split('.')[1])
search_all_resp2 = list(set(text_ready_to_use).intersection(search_all_resp))
list_to_swap=[]
index_list = ([i for i, item in enumerate(text_ready_to_use) if item in search_all_resp2])
print(index_list)
for every_index in index_list:
     word=text4[every_index]
     print(word)
     list_to_swap.append(word)
response_search_all_list2 = []
response_search_all_list2.extend(list_to_swap)
print(response_search_all_list2)