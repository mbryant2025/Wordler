from datetime import date

print()
print("The guess is: ")

with open("/Users/michaelbryant/Desktop/wordlewords.txt", "r") as f:
    d0 = date(2021, 6, 19)
    today = date.today()
    delta = today - d0
    idx = delta.days
    i = 0
    for w in f:
        if i == idx:
            print(w)
        i += 1