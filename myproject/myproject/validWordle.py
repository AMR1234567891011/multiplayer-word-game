import random
from .models import validWord, validGuess

def initSet():
    if len(validWord.objects.all()) <= 0:
        with open("C:/Users/Asher/Desktop/Django-gemini-Test/djano-gemini-test/myproject/myproject/ValidWords.txt", "r") as file:
            for line in file:
                validWord.objects.create(argument = str(line).strip())
    if len(validGuess.objects.all()) <= 0:
        with open("C:/Users/Asher/Desktop/Django-gemini-Test/djano-gemini-test/myproject/myproject/ValidGuesses.txt", "r") as file:
            for line in file:
                validGuess.objects.create(argument = str(line).strip())
    return True

def getRandWord():#returns a random word that is eligible to be a word of the day
    return str(validWord.objects.all()[random.randint(0, 2314)].argument)

def isValid(word):# checks if a guess is within the allowed guesses list
    if len(validGuess.objects.all()) > 0:
        if len(validGuess.objects.filter(argument= str(word))) > 0:
            return True
        else:
            return False
    else:
        initSet()
        return isValid(word)
