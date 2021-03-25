"""The note for GET method"""

def spin_words(sentence):
    return ' '.join(word[::-1] if len(word) >= 5 else word for word in sentence.split(' '))


if __name__ == '__main__':
    print(spin_words('Strings passed in will consist of only letters and spaces'))
