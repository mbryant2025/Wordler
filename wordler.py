import enchant
from wordfreq import zipf_frequency

d = enchant.Dict("en_US")

yellow_set = []
green_letters = ["", "", "", "", ""]
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
words_remaining = 5153
word_objects = []
guessed = []
letter_scores = {'a':43, 'b':11, 'c':23, 'd':17, 'e':57, 'f':9, 'g':13, 'h':15, 'i':38, 'j':1, 'k':6, 'l':28, 'm':15, 'n':34, 'o':37, 'p':16, 'q':1, 'r':37, 's':29, 't':35, 'u':19, 'v':5, 'w':7, 'x':1, 'y':9, 'z':1}
first_guess = "irate"

class Word:
    def __init__(self, w):
        self.w = w
        s = set(self.w)
        self.unique_letters = len(s)
        self.word_score = 0

        for i in range(5):
            self.word_score += letter_scores[w[i]]

        self.frequency = zipf_frequency(w, 'en')

# green = "___id"
# yellow = "_v____"
# yellow = "m_____"
def words_left(green, yellow, gray):
    global words_remaining

    yellow_set.append(yellow)

    word_objects.clear()

    #update global list of green letters
    for i in range(5):
        if green[i] != "_" and green_letters[i] == "":
            green_letters[i] = green[i]

    #update global list of letters to remove gray ones
    for i in range(5):
        if gray[i] in gray[:i]:
            continue
        yellowFlag = False
        if gray[i] != "_":
            for y in yellow_set:
                if gray[i] in y:
                    yellowFlag = True
            if not yellowFlag:
                letters.remove(gray[i])

    #Markers to indicate if letter at position is green
    oneFlag = False
    twoFlag = False
    threeFlag = False
    fourFlag = False
    fiveFlag = False


    for l1 in letters:
        if green_letters[0] != "":
            l1 = green_letters[0]
            oneFlag = True
        for l2 in letters:
            if green_letters[1] != "":
                l2 = green_letters[1]
                twoFlag = True
            for l3 in letters:
                if green_letters[2] != "":
                    l3 = green_letters[2]
                    threeFlag = True
                for l4 in letters:
                    if green_letters[3] != "":
                        l4 = green_letters[3]
                        fourFlag = True
                    for l5 in letters:
                        if green_letters[4] != "":
                            l5 = green_letters[4]
                            fiveFlag = True
                        word = l1 + l2 + l3 + l4 + l5

                        #Skip if doesn't match green letters
                        continueMarker = False
                        for i in range(5):
                            if continueMarker:
                                break
                            if green_letters[i] == "":
                                continue
                            if green_letters[i] != word[i]:
                                continueMarker = True
                        if continueMarker:
                            continue


                        #Skip if it doesn't contain all of the yellow letters
                        continueMarker = False
                        for ys in yellow_set:
                            #List comprehension for extracting letters
                            ys = [x for x in ys if x != "_"]
                            if continueMarker:
                                break
                            for yl in ys:
                                if yl not in word:
                                    continueMarker = True
                                    break
                        if continueMarker:
                            continue

                        #Skip if contains a yellow letter in a yellow position
                        continueMarker = False
                        for ys in yellow_set:
                            if continueMarker:
                                break
                            for i in range(5):
                                if ys[i] == "":
                                    continue
                                if ys[i] == word[i]:
                                    continueMarker = True
                        if continueMarker:
                            continue


                        #Skip if not an English word
                        if(not d.check(word)):
                            continue

                        word_objects.append(Word(word))  
                        if fiveFlag:
                            break 
                    if fourFlag:
                        break  
                if threeFlag:
                    break  
            if twoFlag:
                break  
        if oneFlag:
            break 

    words_remaining = len(word_objects)

previous_guess = first_guess

print()
print("Wordle Bot")
print("Enter results of guess in this format: gbygy")
print()

for i in range(6):
    if i == 0:
        print(str(words_remaining) + " words remain")
        print("The next guess is " + first_guess)
        print()

        results = ""
        while len(results) != 5:
            results = input("Enter results: ")

        green = ""
        yellow = ""
        gray = ""

        for ch in enumerate(results):
            if ch[1] == "g":
                green += previous_guess[ch[0]]
                yellow += "_"
                gray += "_"

            if ch[1] == "y":
                green += "_"
                yellow += previous_guess[ch[0]]
                gray += "_"
            
            if ch[1] == "b":
                green += "_"
                yellow += "_"
                gray += previous_guess[ch[0]]
        print()
        words_left(green, yellow, gray)

        continue

    if(words_remaining == 1):
        print("1 word remains")
        print("The word is " + word_objects[0].w)
        break

    print(str(words_remaining) + " words remain")
    
    #Sort list
    word_objects.sort(key=lambda x: x.word_score, reverse=True)
    word_objects.sort(key=lambda x: x.unique_letters, reverse=True)

    if(words_remaining < 50):
        word_objects.sort(key=lambda x: x.frequency, reverse=True)

    guess =  word_objects[0].w
    inc = 1
    while guess in guessed:
        guess =  word_objects[inc].w
        inc += 1
    
    print("The next guess is " + guess)
    print()
    guessed.append(guess)
    previous_guess = guess

    results = ""
    while len(results) != 5:
        results = input("Enter results: ")

    green = ""
    yellow = ""
    gray = ""

    for ch in enumerate(results):
        if ch[1] == "g":
            green += previous_guess[ch[0]]
            yellow += "_"
            gray += "_"

        if ch[1] == "y":
            green += "_"
            yellow += previous_guess[ch[0]]
            gray += "_"
        
        if ch[1] == "b":
            green += "_"
            yellow += "_"
            gray += previous_guess[ch[0]]

    print()
    words_left(green, yellow, gray)
