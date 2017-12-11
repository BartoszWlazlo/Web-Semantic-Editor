from flask import Flask, render_template, jsonify, request
from nltk_main import click_event_processing2
from owlready2 import *
from collections import defaultdict
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/OWL_DATA_LIB_button1")
def OWL_DATA_LIB_button1():
    global onto
    onto = get_ontology("file://D:/INZ/people.owl").load()

@app.route("/OWL_DATA_LIB_button2")
def OWL_DATA_LIB_button2():
    global onto
    onto = get_ontology("file://D:/INZ/guns.owl").load()


@app.route('/OWL_DATA_CLASSES')
def OWL_DATA_CLASSES():
    data1 = list(onto.classes())
    data2=[]
    for every in data1:
        data2.append(str(every).split('.')[1])
    return jsonify(dataCLASSESback = data2)

@app.route('/OWL_DATA_INDIVIDUALS')
def OWL_DATA_INDIVIDUALS():
    data1 = list(onto.individuals())
    data2 = []
    for every in data1:
        data2.append(str(every).split('.')[1])
    return jsonify(dataINDIback = data2)

@app.route('/OWL_DATA_OBJECT_PROPERTIES')
def OWL_DATA_OBJECT_PROPERTIES():
    data1 = list(onto.object_properties())
    data2 = []
    for every in data1:
        data2.append(str(every).split('.')[1])
    return jsonify(dataPROPERTIESback = data2)


@app.route('/one_word')
def one_word():
    #kursor id oraz text jest wysyłany przez front tak by wydobyc z tekstu klikniete slowo
    kursor_id = request.args.get('ID', 1, type=str)
    text = request.args.get('content', 1, type=str)
    res =  click_event_processing2(kursor_id, text)
    text_from_front=res[0]
    text_nocom = text_from_front.replace(",", "")
    text_nocom_and_dots = text_nocom.replace('.', '')
    value_from_onclick=text_nocom_and_dots.capitalize()




    ####################################################
    ####################################################
    ####################################################
    ####################################################

    def one_word_analysis():

        # potrzebne do wyboru ktorej funkcji uzyc dla slowa (zaleznie czy jest klasa czy indywiduum + zmienne globalne:
        classes = list(onto.classes())  # GLOBAL LIST

        def cut_the_class():
            cut_classes = list()
            for every_class in classes:
                cut_classes.append(str(every_class).split('.')[1])
            return cut_classes

        cut_classes_list = cut_the_class()  # wycieta lista wszystkich klas ze slownika

        individuals = list(onto.individuals())  # GLOBAL LIST

        def cut_the_individual():
            cut_individuals = list()
            for every_individual in individuals:
                cut_individuals.append(str(every_individual).split('.')[1])
            return cut_individuals

        cut_individual_list = cut_the_individual()  # wycieta lista wszystkich indywiduów ze slownika\

        cut_the_object_property_list = list(onto.object_properties())

        def cut_the_object_property():
            cut_object_property = list()
            for every_class in cut_the_object_property_list:
                cut_object_property.append(str(every_class).split('.')[1])
            return cut_object_property

        def classes_with_power():  # funkcja do przypisywania klasom "sily". Potrzebne tylko do funkcji sortujacej.
            classes = classes_above_class()
            list_of_classes_with_powers = []
            for one_class in classes:
                list_of_classes_with_powers.append(str(len(classes[one_class])) + '.' + one_class)
            return list_of_classes_with_powers

        def classes_above_individuals():  # zwraca klasy w ktorych znajduje sie inwdywiduum (funkcja tylko dla indywiduum)
            individuals_result = dict()
            classes_above_individuals_result = dict()
            for one in individuals:
                cutted_individuals = str(one).split('.')[1]
                individuals_result[cutted_individuals] = []
                for two in classes:
                    cutted_classes = str(two).split('.')[1]
                    individuals_of = "onto.search(type= onto." + cutted_classes + ")"
                    if one in eval(individuals_of):
                        individuals_result[cutted_individuals].append(cutted_classes)
            for one in individuals_result:
                classes_above_individuals_result.update({one: individuals_result[one]})
            return classes_above_individuals_result

        def classes_above_class():
            classes_above_class_result = dict()
            for one in classes:
                cutted_classes = str(one).split('.')[1]
                classes_above_class_result[cutted_classes] = []
                for two in classes:
                    cutted_classes_2 = str(two).split('.')[1]
                    classes_of = "onto.search(subclass_of= onto." + cutted_classes_2 + ")"
                    if one in eval(classes_of):
                        classes_above_class_result[cutted_classes].append(cutted_classes_2)
            for one in classes_above_class_result:
                classes_above_class_result.update({one: classes_above_class_result[one]})
            return classes_above_class_result

        def sorted_above():
            def comparision():
                dict_for_going_up = {}
                dict_for_going_up.update(classes_above_individuals())
                dict_for_going_up.update(classes_above_class())
                one_object_classes = (dict_for_going_up[value_from_onclick])
                list_to_compare = classes_with_power()
                index = -1
                for one in one_object_classes:
                    index = index + 1
                    for two in list_to_compare:
                        if one == str(two).split('.')[-1]:
                            one_object_classes[index] = two
                else:
                    pass
                return sorted(one_object_classes)

            def updated_hierarchy_of_classes():
                temp = comparision()
                i = 0
                for every in temp:
                    temp[i] = (str(every).split('.')[-1])
                    i = i + 1
                return temp

            result_sorted_above = updated_hierarchy_of_classes()
            return result_sorted_above

        def class_directly_above():  # oddaje bezposrednią nadklase dla slowa
            class_above = sorted_above()
            if class_above == []:
                return []
            else:
                return class_above[-1]

        print(class_directly_above())

        def instances_from_the_same_class():  # jesli slowo = instancja -> wyswietl wszystkie instancje z tej samej klasy
            class_above = class_directly_above()
            temp = "onto.search(type= onto." + class_above + ")"
            temp_evaluated = eval(temp)
            result = []
            for every_class in temp_evaluated:
                if (str(every_class).split('.')[1]) == value_from_onclick:
                    pass
                else:
                    result.append(str(every_class).split('.')[1])
            return result

        def instances_from_the_clicked_class():  # jesli slowo = klasa -> wyswietl wszystkie instancje tej klasy
            the_class = value_from_onclick
            temp = "onto.search(type= onto." + the_class + ")"
            temp_evaluated = eval(temp)
            result = []
            for every_class in temp_evaluated:
                if (str(every_class).split('.')[1]) == value_from_onclick:
                    pass
                else:
                    result.append(str(every_class).split('.')[1])
            return result

        all_properties = cut_the_object_property()
        all_individuals = cut_the_individual()

        all_properties = cut_the_object_property()
        all_individuals = cut_the_individual()

        def relations():
            list_with_duplicates = list()
            for every_individual in all_individuals:
                for every_property in all_properties:
                    code = "list(onto." + every_individual + "." + every_property + ")"
                    evaluated_relations = eval(code)
                    if evaluated_relations == []:
                        pass
                    else:
                        for every in evaluated_relations:
                            evaluated_relations_split = str(every).split('.')[-1]
                            concatenation = str(every_individual) + ' ' + str(every_property) + ' ' + str(
                                evaluated_relations_split)
                            list_with_duplicates.append(concatenation)
            relations_result = list(set(list_with_duplicates))
            return (relations_result)

        def classes_below():
            eval_code = "onto.search(subclass_of= onto." + value_from_onclick + ")"
            result = eval(eval_code)
            result2 = list()
            for every_class in result:
                result2.append(str(every_class).split('.')[1])
            return result2

        LIST = []

        print(cut_individual_list)
        # DATA FOR WORD IF WORD IS A INDIVIDUAL
        for every in cut_individual_list:
            if every == value_from_onclick:
                INDI_val1 = sorted_above()
                LIST.append(INDI_val1)
                INDI_val2 = instances_from_the_same_class()
                LIST.append(INDI_val2)
                INDI_val4 = relations()
                INDI_val3 = [s for s in INDI_val4 if str(value_from_onclick) in s]
                LIST.append(INDI_val3)
            else:
                pass

        for every in cut_classes_list:
            if every == value_from_onclick:
                CLASS_val1 = sorted_above()
                LIST.append(CLASS_val1)
                CLASS_val2 = classes_below()
                LIST.append(CLASS_val2)
                CLASS_val3 = instances_from_the_clicked_class()
                LIST.append(CLASS_val3)
            else:
                pass
        # DATA FOR WORD IF WORD IS A CLASS

        return LIST

    ####################################################
    ####################################################
    classes = list(onto.classes())
    def cut_the_class():
        cut_classes = list()
        for every_class in classes:
            cut_classes.append(str(every_class).split('.')[1])
        return cut_classes
    cut_classes_list = cut_the_class()
    individuals = list(onto.individuals())
    def cut_the_individual():
        cut_individuals = list()
        for every_individual in individuals:
            cut_individuals.append(str(every_individual).split('.')[1])
        return cut_individuals
    cut_individual_list = cut_the_individual()
    ####################################################
    ####################################################

    one_word_analysis_LIST=[]
    one_word_analysis_LIST=one_word_analysis()

    ####################################################
    ####################################################
    sorted_above_INDI_list=[]
    instances_from_the_same_class_list=[]
    relations_result_list=[]
    #IF INDIVIDUAL
    for every in cut_individual_list:
        if every == value_from_onclick:
            sorted_above_INDI_list = one_word_analysis_LIST[0]
            instances_from_the_same_class_list = one_word_analysis_LIST[1]
            relations_result_list=one_word_analysis_LIST[2]
        else:
            pass
    #IF CLASS
    classes_above_list = []
    subclass_of_class_list=[]
    instances_from_the_clicked_class_list=[]
    for every in cut_classes_list:
        if every == value_from_onclick:
            print('CLASS')
            classes_above_list = one_word_analysis_LIST[0]
            subclass_of_class_list = one_word_analysis_LIST[1]
            instances_from_the_clicked_class_list=one_word_analysis_LIST[2]
        else:
            pass

    return jsonify(subclass_of_list_response=subclass_of_class_list,classes_above_list_response=classes_above_list,instances_from_the_clicked_class_list_response=instances_from_the_clicked_class_list,sorted_above_INDI_list_response=sorted_above_INDI_list,instances_from_the_same_class_list_response=instances_from_the_same_class_list,relations_result_list_response=relations_result_list)


@app.route('/search_all')
def search_all():
    text_from_front = request.args.get('content', 0, type=str)
    text_to_bold=text_from_front.split()
    text_nocom = text_from_front.replace(",", "")
    text_nocom_and_dots = text_nocom.replace('.', '')
    text = text_nocom_and_dots.split()
    text_ready_to_use = []
    for every_word in text:
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
    search_all_resp = []
    for every in onto_list:
        search_all_resp.append(str(every).split('.')[1])
    search_all_resp2 = list(set(text_ready_to_use).intersection(search_all_resp))
    list_to_swap = []
    index_list = ([i for i, item in enumerate(text_ready_to_use) if item in search_all_resp2])
    for every_index in index_list:
        word = text_to_bold[every_index]
        list_to_swap.append(word)
    response_search_all_list2 = []
    response_search_all_list2.extend(list_to_swap)
    response_search_all_list2 = [str(i) for i in response_search_all_list2]
    return jsonify(response_search_all_list=response_search_all_list2)


if __name__ == "__main__":
    app.run()