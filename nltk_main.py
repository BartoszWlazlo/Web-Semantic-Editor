from nltk import sent_tokenize
import re
# funkcja odpowiadajaca za znalezienie kliknietego slowa i zdania w akapicie
# przyjmujaca jako cursor_position pozycje kursora w edytorze oraz tekst (akapit)
#i zwracajaca klikniete slowo i klikniete zdanie
def click_event_processing2(cursor_position, text):
    cursor_position = int(cursor_position)
    text = str(text)
    l = text.split()
    if cursor_position >= len(text):
        return['','']
    #jesli akapit jest pusty zwraca klikniete slowo i zdanie jako empty
    elif len(text)==0:
        return['empty','empty']
    else:
        word_counter = 0
        # length_of_line_to_clicked_word to zmienna zwiekszana do czasu
        # az nie bedzie rowna lub wieksza od id
        length_of_line_to_clicked_word = 0
        while length_of_line_to_clicked_word <= cursor_position:
            length_of_line_to_clicked_word += len(l[word_counter])+1
            word_counter += 1
        # uzycie wbudowanej w nltk funkcji dzielenia lancucha znakow na zdania
        sentences = sent_tokenize(text)
        list_of_words_in_sentences = []
        for word in sentences:
            li = word.split()
            list_of_words_in_sentences.append(li)
        counter = 0
        j = 0
        #petla dodajaca kolejne wyrazy do dopoki
        # counter nie bedzie rownal sie  kliknietemu slowu
        while counter <= word_counter-1:
            counter += len(list_of_words_in_sentences[j])
            j+=1
        # zwrocenie kliknietego slowa i zdania
        return [l[word_counter-1], sentences[j-1]]

