from owlready2 import *
onto = get_ontology("file://D:/INZ/Guns4.owl").load()

###########################
value_from_onclick = 'Sex' 
###########################

# potrzebne do wyboru ktorej funkcji uzyc dla slowa (zaleznie czy jest klasa czy indywiduum + zmienne globalne:
classes = list(onto.classes())
def cut_the_class():
    cut_classes = list()
    for every_class in classes:
        cut_classes.append(str(every_class).split('.')[1])
    return cut_classes
cut_classes_list = cut_the_class()   # wycieta lista wszystkich klas ze slownika


individuals = list(onto.individuals())
def cut_the_individual():
    cut_individuals = list()
    for every_individual in individuals:
        cut_individuals.append(str(every_individual).split('.')[1])
    return cut_individuals
cut_individual_list = cut_the_individual  # wycieta lista wszystkich indywiduów ze slownika


def classes_with_power():  # funkcja do przypisywania klasom "sily". Potrzebne tylko do funkcji sortujacej.
    power_of_classes = dict()
    list_of_classes_with_powers = list()
    for one_class in classes:
        cutted_class = str(one_class).split('.')[-1]
        temporary_code = ("onto.search(subclass_of= onto." + cutted_class + ")")
        power_of_classes.update({cutted_class: list(eval(temporary_code))})
    for key, value in sorted(power_of_classes.items()):
        list_of_classes_with_powers.append(str(len([item for item in value if item])) + '.' + key)
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


def classes_below_class():   ### juz nie mialem sil sie z tym meczyc. zrob to albo ja jutro zrobie wieczorem moze.
    classes_below_classes_result = dict()
    temp = list()
    for one in classes:
        cutted_classes = str(one).split('.')[1]
        temp.append(eval("onto.search(subclass_of= onto." + cutted_classes + ")"))
    for every_list in temp:
        for every_object_in_a_list in every_list:
            temp = str(every_object_in_a_list).split('.')[-1]
            print(every_list, temp)
#classes_below_class()




def sorted_above():   # sortuje klasy powyzej slowa (to jest funkcja dla indywiduum i dla klasy)
    def comparision():
        dict_for_going_up = dict()
        dict_for_going_up.update(classes_above_individuals())
        dict_for_going_up.update(classes_above_class())
        one_object_classes = (dict_for_going_up[value_from_onclick])
        list_to_compare = classes_with_power()
        index = -1
        for one in one_object_classes:
            index = index+1
            for two in list_to_compare:
                if one == str(two).split('.')[-1]:
                    one_object_classes[index] = two
        else:
            pass
        return sorted(one_object_classes, reverse=True)

    def updated_hierarchy_of_classes():
        temp = comparision()
        i = 0
        for every in temp:
            temp[i] = (str(every).split('.')[-1])
            i = i + 1
        return temp
    result_sorted_above = updated_hierarchy_of_classes()
    return result_sorted_above


def sorted_below():  # sortuje klasy ponizej zaznaczonego slowa (funkcja tylko dla klasy)
    def comparision():
        dict_for_going_down = {}
        dict_for_going_down.update(classes_below_class())
        one_object_classes = (dict_for_going_down[value_from_onclick])
        list_to_compare = classes_with_power()
        index = -1
        for one in one_object_classes:
            index = index+1
            for two in list_to_compare:
                if one == str(two).split('.')[-1]:
                    one_object_classes[index] = two
        else:
            pass
        return sorted(one_object_classes, reverse=True)

    def updated_hierarchy_of_classes():
        temp = comparision()
        i = 0
        for every in temp:
            temp[i] = (str(every).split('.')[-1])
            i = i + 1
        return temp
    result_sorted_below = updated_hierarchy_of_classes()
    return result_sorted_below


def class_directly_above():  # oddaje bezposrednią nadklase dla slowa
    class_above = sorted_above()
    return class_above[-1]


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

cut_the_object_property_list = list(onto.object_properties())


def cut_the_object_property():
    cut_object_property = list()
    for every_class in cut_the_object_property_list:
        cut_object_property.append(str(every_class).split('.')[1])
    return cut_object_property

all_properties = cut_the_object_property()
all_individuals = cut_the_individual()


def relations():
    relations_result = dict()
    for every_individual in all_individuals:
        for every_property in all_properties:
            code = "list(onto." + every_individual + "." + every_property + ")"
            evaluated_relations = eval(code)
            i = -1
            if evaluated_relations == []:
                pass
            else:
                for every in evaluated_relations:
                    hehe = str(every).split('.')[-1]
                    hehe2 = str(every_individual)+' '+str(every_property)+' '+str(hehe)
                    print(hehe2)
    print(relations_result)
    return relations_result

relations()