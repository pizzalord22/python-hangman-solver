import string
from difflib import SequenceMatcher
import random
import time

target = ""
knownword = ""
knownLetters = []
badLetters = []
badWords = []


# function to select a random word
def getRandomWord():
    global target
    random.seed = time.time().as_integer_ratio()
    val = 0
    while val <= 0:
        val = random.randint(1, 24)
    mydict = getDict(val)
    target = mydict[random.randint(0, len(mydict) - 1)]


# function that creates an empty string as long as our target word
def knownWordInit():
    global knownword, target
    knownword = "_" * len(target)


# uodate known word
def updateKnownWord():
    global knownword, knownLetters, target
    tmp = list(knownword)
    knownword = ""
    for index in range(0, len(target)):
        if knownLetters[-1] == target[index]:
            tmp[index] = knownLetters[len(knownLetters) - 1]

    for letter in tmp:
        if letter == "":
            knownword += "_"
        else:
            knownword += letter
    # print(knownword)


# function to load in a dict
def getDict(wordLength):
    if wordLength < 1:
        wordLength = 5
    return open("dicts/dict" + str(wordLength) + ".txt", "r").read().split("\n")


# give an empty dict
def LetterDict():
    a = {
        "a": 0, "b": 0, "c": 0,
        "d": 0, "e": 0, "f": 0,
        "g": 0, "h": 0, "i": 0,
        "j": 0, "k": 0, "l": 0,
        "m": 0, "n": 0, "o": 0,
        "p": 0, "q": 0, "r": 0,
        "s": 0, "t": 0, "u": 0,
        "v": 0, "w": 0, "x": 0,
        "y": 0, "z": 0
    }
    return a


# we want everything to be lower case
def dictToLower():
    global words
    for index in range(0, len(words)):
        words[index] = words[index].lower()
        words.sort()


# resets the choice also used to initialize it
def resetChoice():
    return {
        "score": 0,
        "letter": "a"
    }


# get all the bad words
def getbBadWords():
    global words, knownLetters, badWords, badLetters
    for word in words:
        for letter in knownLetters:
            if letter not in word:
                if word not in badWords:
                    badWords.append(word)


def getbadLetters():
    global words, badLetters, badWords
    for word in words:
        for letter in badLetters:
            if letter in word:
                if word not in badWords:
                    badWords.append(word)


def getBadLetterPos():
    global words, knownword, badWords
    for word in words:
        for index in range(0, len(knownword) - 1):
            if knownword[index] != "_":
                try:
                    if word[index] != knownword[index]:
                        if word not in badWords:
                            badWords.append(word)
                except:
                    pass


# remove all the words that can not match the target
def removeBadWords():
    global words, badWords
    for word in badWords:
        words.remove(word)


# get the scores of all letters
def getScores():
    global words, letterChance, knownLetters, alphabet
    for word in words:
        for letter in alphabet:
            if letter in word:
                if letter not in knownLetters:
                    letterChance[letter] += 1


# this returns the best score and the letter that got it
def getHighestScore():
    global letterChance, bestChoice
    for letter in letterChance:
        if letterChance[letter] > bestChoice["score"]:
            bestChoice["score"] = letterChance[letter]
            bestChoice["letter"] = letter


def tryWord():
    global knownword, words
    bestMatch = {
        "word": "",
        "percentage": 0
    }
    for word in words:
        match = SequenceMatcher(None, word, knownword).ratio()
        if match > bestMatch["percentage"]:
            bestMatch["word"] = word
            bestMatch["percentage"] = match
    return bestMatch


# only die when we lose to the hangman game
matches = 0
wins = 0
loses = 0

alphabet = list(string.ascii_lowercase)

# this plays a 100 matches to test how good it is
while matches < 100:
    getRandomWord()
    knownWordInit()
    words = getDict(len(target))
    dictToLower()
    knownLetters = []
    badLetters = []
    badWords = []
    # only die when we lose to the hangman game
    x = 1
    while x < 6:
        bestChoice = resetChoice()
        letterChance = LetterDict()
        getbBadWords()
        getbadLetters()
        getBadLetterPos()
        removeBadWords()
        badWords.clear()
        getScores()
        getHighestScore()
        if bestChoice["letter"] in target:
            if bestChoice["letter"] not in knownLetters:
                knownLetters.append(bestChoice["letter"])
                x -= 1
        else:
            if bestChoice["letter"] not in badLetters:
                badLetters.append(bestChoice["letter"])

        if len(knownLetters) > 0:
            updateKnownWord()
        result = tryWord()
        if knownword == target:
            print("won the game in " + str(x) + " wrong guesses")
            wins += 1
            x = 10
        else:
            if x >= 5:
                loses += 1
                print("game lost")

        x += 1
    matches += 1


# print total wins and loses and then win percentage
print("wins ", wins, "\r\nloses", loses)
print("win percentage", matches / 100 * float(wins))
