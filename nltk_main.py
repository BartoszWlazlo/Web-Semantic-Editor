from nltk import sent_tokenize

def find_word_in_text(position_of_cursor_in_text, text):
    position_of_cursor_in_text = int(position_of_cursor_in_text)
    text = str(text)
    splited_text = text.split()
    if position_of_cursor_in_text >= len(text):
        return['','']
    elif len(text)==0:
        return['empty','empty']
    else:
        variable_for_counting_words = 0
        the_number_of_words_till_clicked_word = 0
        while the_number_of_words_till_clicked_word <= position_of_cursor_in_text:
            the_number_of_words_till_clicked_word += len(splited_text[variable_for_counting_words])+1
            variable_for_counting_words += 1
        tokenized_text = sent_tokenize(text)
        list_of_words_in_sentences = []
        for each_word in tokenized_text:
            word = each_word.split()
            list_of_words_in_sentences.append(word)
        counter = 0
        v = 0
        while counter <= variable_for_counting_words-1:
            counter += len(list_of_words_in_sentences[v])
            v+=1
        return [splited_text[variable_for_counting_words-1], tokenized_text[v-1]]