def word_split(text):
    return text.split()

def word_count(text):
    return len(text.split())

def word_frequency(text):
    words = text.upper().split()
    dct = {}
    for word in words:
        if word in dct:
            dct[word] += 1
        else:
            dct[word] = 1
    return dct

def most_frequent_word(dct, text):
    lst = dct(text)
    lst = sorted(lst.items(), key = lambda x: x[1], reverse = True )
    word, count = lst[0]
    return word.upper(), count

def lexical_density(dct, text):
    lst = dct(text)
    lst = set(lst)
    total = len(text.split())
    result = len(lst) / total * 100
    return round(result, 2)   



# print(word_split(user_input))
# print(word_count(user_input))
# print(word_frequency(user_input))
# print(most_frequent_word(word_frequency, user_input))
# print(lexical_density(word_frequency, user_input))
