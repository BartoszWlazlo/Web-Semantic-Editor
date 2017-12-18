from flask import Flask, render_template, jsonify, request
from nltk_main import find_word_in_text
from owlready2 import *
from collections import defaultdict
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/LOAD_ONTOLOGY_1_IN_BACKEND")
def LOAD_ONTOLOGY_1_FROM_BACKEND():
    global onto
    onto = get_ontology("file://people.owl").load()

@app.route("/LOAD_ONTOLOGY_2_IN_BACKEND")
def LOAD_ONTOLOGY_2_FROM_BACKEND():
    global onto
    onto = get_ontology("file://guns.owl").load()


@app.route('/DISP_ALL_CLASSES')
def OWL_DATA_CLASSES():
    list_of_classes = list(onto.classes())
    list_of_classes_for_jsonify=[]
    for each_class in list_of_classes:
        list_of_classes_for_jsonify.append(str(each_class).split('.')[1])
    return jsonify(all_classes_response = list_of_classes_for_jsonify)

@app.route('/DISP_ALL_INDIVIDUALS')
def OWL_DATA_INDIVIDUALS():
    list_of_individuals = list(onto.individuals())
    list_of_individuals_for_jsonify = []
    for each_individual in list_of_individuals:
        list_of_individuals_for_jsonify.append(str(each_individual).split('.')[1])
    return jsonify(all_individuals_response = list_of_individuals_for_jsonify )

@app.route('/DISP_ALL_RELACTIONS')
def OWL_DATA_OBJECT_PROPERTIES():
    list_of_relations = list(onto.object_properties())
    list_of_relations_for_jsonify = []
    for each_relaction in list_of_relations:
        list_of_relations_for_jsonify.append(str(each_relaction).split('.')[1])
    return jsonify(all_relations_response = list_of_relations_for_jsonify)


@app.route('/one_word')
def one_word():

    cursor_id = request.args.get('ID', 1, type=str)
    text = request.args.get('content', 1, type=str)
    res =  find_word_in_text(cursor_id, text)
    text_from_front=res[0]
    text_nocom = text_from_front.replace(",", "")
    text_nocom_and_dots = text_nocom.replace('.', '')
    value_from_onclick=text_nocom_and_dots.capitalize()


    ####################################################
    ####################################################
    ####################################################
    ####################################################

    def one_word_analysis():


        classes = list(onto.classes())
        def cut_the_class():
            cut_classes = list()
            for each_element in classes:
                cut_classes.append(str(each_element).split('.')[1])
            return cut_classes
        cut_classes_list = cut_the_class()


        individuals = list(onto.individuals())
        def cut_the_individual():
            cut_individuals = list()
            for each_individual in individuals:
                cut_individuals.append(str(each_individual).split('.')[1])
            return cut_individuals
        cut_individual_list = cut_the_individual()


        cut_the_object_property_list = list(onto.object_properties())
        def cut_the_object_property():
            cut_object_property = list()
            for each_relation in cut_the_object_property_list:
                cut_object_property.append(str(each_relation).split('.')[1])
            return cut_object_property


        def classes_with_power():
            classes = classes_above_class()
            list_of_classes_with_powers = []
            for each_class in classes:
                list_of_classes_with_powers.append(str(len(classes[each_class])) + '.' + each_class)
            return list_of_classes_with_powers


        def classes_above_individuals():
            individuals_result = dict()
            classes_above_individuals_result = dict()
            for each_individual in individuals:
                cut_individuals = str(each_individual).split('.')[1]
                individuals_result[cut_individuals] = []
                for each_class in classes:
                    cut_classes = str(each_class).split('.')[1]
                    individuals_of = "onto.search(type= onto." + cut_classes + ")"
                    if each_individual in eval(individuals_of):
                        individuals_result[cut_individuals].append(cut_classes)
            for each_individual in individuals_result:
                classes_above_individuals_result.update({each_individual: individuals_result[each_individual]})
            return classes_above_individuals_result


        def classes_above_class():
            classes_above_class_result = dict()
            for each_class in classes:
                cut_classes = str(each_class).split('.')[1]
                classes_above_class_result[cut_classes] = []
                for each_class2 in classes:
                    cut_classes2 = str(each_class2).split('.')[1]
                    classes_of = "onto.search(subclass_of= onto." + cut_classes2 + ")"
                    if each_class in eval(classes_of):
                        classes_above_class_result[cut_classes].append(cut_classes2)
            for each_class in classes_above_class_result:
                classes_above_class_result.update({each_class: classes_above_class_result[each_class]})
            return classes_above_class_result


        def sorted_above():
            def comparision():
                dict_for_going_up = {}
                dict_for_going_up.update(classes_above_individuals())
                dict_for_going_up.update(classes_above_class())
                one_object_classes = (dict_for_going_up[value_from_onclick])
                list_to_compare = classes_with_power()
                index = -1
                for each_class in one_object_classes:
                    index = index + 1
                    for each_element in list_to_compare:
                        if each_class == str(each_element).split('.')[-1]:
                            one_object_classes[index] = each_element
                else:
                    pass
                return sorted(one_object_classes)


            def updated_hierarchy_of_classes():
                sorted_hierarchy = comparision()
                i = 0
                for each_element in sorted_hierarchy:
                    sorted_hierarchy[i] = (str(each_element).split('.')[-1])
                    i = i + 1
                return sorted_hierarchy
            sorted_above_result = updated_hierarchy_of_classes()
            return sorted_above_result


        def class_directly_above():
            class_above = sorted_above()
            if class_above == []:
                return []
            else:
                return class_above[-1]


        def instances_from_the_same_class():
            class_above = class_directly_above()
            individuals_of = "onto.search(type= onto." + class_above + ")"
            eval_individuals_of = eval(individuals_of)
            result = []
            for each_class in eval_individuals_of:
                if (str(each_class).split('.')[1]) == value_from_onclick:
                    pass
                else:
                    result.append(str(each_class).split('.')[1])
            return result


        def instances_from_the_clicked_class():
            the_class = value_from_onclick
            individuals_of = "onto.search(type= onto." + the_class + ")"
            eval_individuals_of = eval(individuals_of)
            result = []
            for each_class in eval_individuals_of:
                if (str(each_class).split('.')[1]) == value_from_onclick:
                    pass
                else:
                    result.append(str(each_class).split('.')[1])
            return result


        all_properties = cut_the_object_property()
        all_individuals = cut_the_individual()
        def relations():
            list_with_duplicates = list()
            for each_individual in all_individuals:
                for each_property in all_properties:
                    relations = "list(onto." + each_individual + "." + each_property + ")"
                    eval_relations = eval(relations)
                    if eval_relations == []:
                        pass
                    else:
                        for each_relation in eval_relations:
                            eval_relations_split = str(each_relation).split('.')[-1]
                            concatenation = str(each_individual) + ' ' + str(each_property) + ' ' + str(
                                eval_relations_split)
                            list_with_duplicates.append(concatenation)
            relations_result = list(set(list_with_duplicates))
            return (relations_result)


        def classes_below():
            subclasses_of = "onto.search(subclass_of= onto." + value_from_onclick + ")"
            eval_subclasses_of = eval(subclasses_of)
            list_of_classes_below = list()
            for each_class in eval_subclasses_of:
                list_of_classes_below.append(str(each_class).split('.')[1])
            return list_of_classes_below
        LIST = []
        for each_element in cut_individual_list:
            if each_element == value_from_onclick:
                if_individual_classes_above = sorted_above()
                LIST.append(if_individual_classes_above)
                if_individual_twin_individuals = instances_from_the_same_class()
                LIST.append(if_individual_twin_individuals)
                relations_list = relations()
                if_individual_relations = [s for s in relations_list if str(value_from_onclick) in s]
                LIST.append(if_individual_relations)
            else:
                pass
        for each_element in cut_classes_list:
            if each_element == value_from_onclick:
                if_class_classes_above = sorted_above()
                LIST.append(if_class_classes_above)
                if_class_classes_below = classes_below()
                LIST.append(if_class_classes_below)
                if_class_individuals_of_this_class = instances_from_the_clicked_class()
                LIST.append(if_class_individuals_of_this_class)
            else:
                pass
        return LIST

    ####################################################
    ####################################################

    classes = list(onto.classes())
    def cut_the_class():
        cut_classes = list()
        for each_class in classes:
            cut_classes.append(str(each_class).split('.')[1])
        return cut_classes
    cut_classes_list = cut_the_class()

    individuals = list(onto.individuals())
    def cut_the_individual():
        cut_individuals = list()
        for each_individual in individuals:
            cut_individuals.append(str(each_individual).split('.')[1])
        return cut_individuals
    cut_individual_list = cut_the_individual()

    ####################################################
    ####################################################

    one_word_analysis_LIST=[]
    one_word_analysis_LIST=one_word_analysis()

    ####################################################
    ####################################################

    sorted_classes_above_of_individual=[]
    twin_individuals_of_individual=[]
    relations_of_individual=[]
    for each_individual in cut_individual_list:
        if each_individual == value_from_onclick:
            sorted_classes_above_of_individual = one_word_analysis_LIST[0]
            twin_individuals_of_individual = one_word_analysis_LIST[1]
            relations_of_individual=one_word_analysis_LIST[2]
        else:
            pass

    subclasses_of_class = []
    classes_above_of_class=[]
    instances_of_class=[]
    for each_class in cut_classes_list:
        if each_class == value_from_onclick:
            print('CLASS')
            classes_above_of_class = one_word_analysis_LIST[0]
            subclasses_of_class = one_word_analysis_LIST[1]
            instances_of_class=one_word_analysis_LIST[2]
        else:
            pass
    return jsonify(subclasses_of_class_response=subclasses_of_class,classes_above_class_response=classes_above_of_class,individuals_of_class_response=instances_of_class,classes_of_individual_response=sorted_classes_above_of_individual,twin_individual_response=twin_individuals_of_individual,relations_response=relations_of_individual)


@app.route('/search_all')
def search_all():
    text_from_frontend = request.args.get('content', 0, type=str)
    text_to_bold=text_from_frontend.split()
    text_nocom = text_from_frontend.replace(",", "")
    text_nocom_and_dots = text_nocom.replace('.', '')
    text = text_nocom_and_dots.split()
    text_ready_to_use = []
    for each_word in text:
        word = each_word
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
    onto_list_str = []
    for each_element in onto_list:
        onto_list_str.append(str(each_element).split('.')[1])
    found_words = list(set(text_ready_to_use).intersection(onto_list_str))
    list_to_swap = []
    index_list = ([i for i, item in enumerate(text_ready_to_use) if item in found_words])
    for each_index in index_list:
        word = text_to_bold[each_index]
        list_to_swap.append(word)
    search_all_result = []
    search_all_result.extend(list_to_swap)
    search_all_result = [str(i) for i in search_all_result]
    return jsonify(search_all_response=search_all_result)


if __name__ == "__main__":
    app.run()
