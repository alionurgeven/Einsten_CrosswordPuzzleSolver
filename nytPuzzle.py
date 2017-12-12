#!python2
import requests
import csv, re, time, copy
from bs4 import BeautifulSoup
from decimal import Decimal
import pygame
from pip._vendor.requests.packages.urllib3.util import retry
from pygame.locals import *
import sys
import math
import datetime
import string
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import json
import os, sys

now = datetime.datetime.now()
record = now.strftime("%d-%m-%Y")

class Grid:
    Tiles = []
    Chars = []
    Answers = []
    Words = []
    def __init__(self):
        self.Tiles = []
        for i in range(0,25,1):
            self.Chars.append("")
            self.Answers.append("")



def puzzle_spider():
    browser = webdriver.Chrome()
    browser.get('https://www.nytimes.com/crosswords/game/mini')
    items = browser.find_elements_by_tag_name("span")
    items[24].click()
    items = browser.find_elements_by_tag_name("button")
    items[5].click()
    items = browser.find_elements_by_tag_name("a")
    items[18].click()
    items = browser.find_elements_by_tag_name("span")
    #i = 0
    #for el in items:
    #    print(el.text, i)
    #    i += 1
    items[26].click()

    items = browser.find_elements_by_tag_name("a")
    items[30].click()

    html = browser.page_source
    soup = BeautifulSoup(html, "html.parser")
    i=0
    for title in soup.findAll("h3", {"class":"ClueList-title--1-3oW"}):
        Titles.append(title.text)
    for clue in soup.findAll("span", {"class": "Clue-text--3lZl7"}):
        Clues.append(clue.text)
    for label in soup.findAll("span", {"class": "Clue-label--2IdMY"}):
        Labels.append(int(label.text))
    for cells in soup.findAll("g", {"data-group":"cells"}):
        for cell in cells.findAll("g"):
            grid.Tiles.append(cell)
    for answer in grid.Tiles:
        for a in answer.findAll("text", {"text-anchor": "middle"}):
            grid.Answers[i] = a.text
        i+=1
    Words = []

    Words.append([])
    Words.append([])
    Words.append([])
    Words.append([])
    Words.append([])
    Words.append([])
    Words.append([])
    Words.append([])
    Words.append([])
    Words.append([])

    k = 0
    l = 0
    for row in grid.Answers:
        Words[k].append(row)
        l += 1
        if l % 5 == 0:
            k += 1
    a = 0
    b=0
    for col in Words:
        for chr in col:
            if col != "":
                Words[k + a].append(chr)
            a += 1
        if a == 5:
            a = 0
        b+=1
        if b == 5:
            break

    new_words = []

    for word in Words:
        wrd = filter(None, word)
        new_words.append(wrd)
    for word in new_words:
        print(word)
    browser.quit()
    grid.Words = new_words

def reveal():
    for i in range(0, grid.Chars.__len__(), 1):
        grid.Chars[i] = grid.Answers[i]


def clear():
    for i in range(0, grid.Chars.__len__(), 1):
        grid.Chars[i] = ""



def printPuzzle():
    while True:
        mouse_x = None
        mouse_y = None
        for event in pygame.event.get():
            if event.type is QUIT:
                pygame.quit();
                sys.exit();
            elif event.type is pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                print(mouse_y,mouse_y)
                if mouse_x < 700 and mouse_x > 600 and mouse_y <= 500 and mouse_y >= 450:
                    reveal()
                elif 900 >= mouse_x and mouse_x >= 800 and 500 >= mouse_y and mouse_y >= 450:
                    clear()
                elif 1000 > pygame.mouse.get_pos()[0] and pygame.mouse.get_pos()[0] > 900 and 600 > pygame.mouse.get_pos()[1] and pygame.mouse.get_pos()[1] > 550:
                    SolvePuzzle(screen)

        screen = pygame.display.set_mode((1800, 1000))
        screen.fill(white);

        if 700 > pygame.mouse.get_pos()[0] and pygame.mouse.get_pos()[0] > 600 and 500 > pygame.mouse.get_pos()[1] and pygame.mouse.get_pos()[1] > 450:
            pygame.draw.rect(screen, bright_green, (600, 450, 100, 50))
        else:
            pygame.draw.rect(screen, green, (600, 450, 100, 50))
        smallText = pygame.font.Font("freesansbold.ttf", 20)
        text = font.render("Reveal!", 1, (0, 0, 0))
        screen.blit(text, (615, 465))

        if 900 > pygame.mouse.get_pos()[0] and pygame.mouse.get_pos()[0] > 800 and 500 > pygame.mouse.get_pos()[1] and pygame.mouse.get_pos()[1] > 450:
            pygame.draw.rect(screen, bright_red, (800, 450, 100, 50))
        else:
            pygame.draw.rect(screen, red, (800, 450, 100, 50))
        smallText = pygame.font.Font("freesansbold.ttf", 20)
        text = font.render("Clear!", 1, (0, 0, 0))
        screen.blit(text, (815, 465))

        if 1000 > pygame.mouse.get_pos()[0] and pygame.mouse.get_pos()[0] > 900 and 600 > pygame.mouse.get_pos()[1] and pygame.mouse.get_pos()[1] > 550:
            pygame.draw.rect(screen, bright_red, (900, 550, 100, 50))
        else:
            pygame.draw.rect(screen, white, (900, 550, 100, 50))
        smallText = pygame.font.Font("freesansbold.ttf", 20)
        text = font.render("Solve!", 1, (0, 0, 0))
        screen.blit(text, (915, 565))

        startx = 520
        starty = 5
        lastLabel = 0
        text = font.render(Titles[0], 1, (0, 0, 0))
        screen.blit(text, (startx, starty))
        text = font.render(Titles[1], 1, (0, 0, 0))
        screen.blit(text, (startx + 700, starty))

        starty = 55
        i = 0
        a = 0
        for element in Labels:
            if lastLabel < element:
                text = font.render(str(Labels[i]), 1, (0, 0, 0))
                screen.blit(text, (startx, starty + a * 50))
                text = font.render(Clues[i], 1, (0, 0, 0))
                screen.blit(text, (startx + 20, starty + a * 50))
                i += 1
                a += 1
                lastLabel = element
            else:
                startx += 700
                starty = 55
                lastLabel = 0
                a = 0
                text = font.render(str(Labels[i]), 1, (0, 0, 0))
                screen.blit(text, (startx, starty + a * 50))
                text = font.render(Clues[i], 1, (0, 0, 0))
                screen.blit(text, (startx + 20, starty + a * 50))
                i += 1
                a += 1
                lastLabel = element
        a = 0

        for nn in range(0,grid.Tiles.__len__(),1):
            tile = grid.Tiles[nn].find("rect")
            if tile.get("fill") == "black":
                pygame.draw.rect(screen, black, (float(tile.get("x")), float(tile.get("y")), 100, 100), 0)
                grid.Chars[nn] = ""
            else:
                pygame.draw.rect(screen, black, (float(tile.get("x")), float(tile.get("y")), 100, 100), 1)
            for number in grid.Tiles[nn].findAll("text", {"text-anchor": "start"}):
                text = font.render(number.text, 1, (0, 0, 0))
                screen.blit(text, (float(number.get("x")), float(number.get("y"))-30))
            if grid.Chars[nn] != "":
                text = font.render(grid.Chars[nn].upper(), 1, (0, 0, 0))
                screen.blit(text, (float(tile.get("x"))+20, float(tile.get("y"))+20))

        if mouse_x is not None and mouse_y is not None:
            arr = CheckMousePos(mouse_x, mouse_y)
            if arr is not None:
                mposx = arr[0]
                mposy = arr[1]
                stri = ask(screen, "Key")
                for i in range(0, stri.__len__(), 1):
                    a = (mposx-int(float(grid.Tiles[0].find("rect").get("x"))))/100
                    b = (mposy-int(float(grid.Tiles[0].find("rect").get("y"))))/100
                    if i < 5:
                        if (b * 5 + a + i) % 5 == 0 and (b * 5 + a) % 5 != 0:
                            break
                        findTile(stri[i], a, b, i)

        pygame.display.update()


def findTile(char, a, b,i):
    grid.Chars[b*5+a+i] = char


def display_box(screen, message):
    fontobject = pygame.font.Font(None,18)
    pygame.draw.rect(screen, (0,0,0), ((screen.get_width() / 2) - 100, (screen.get_height() / 2) +20, 200,20), 0)
    #pygame.draw.rect(screen, (255,255,255), ((screen.get_width() / 2) - 102, (screen.get_height() / 2) - 12, 204,24), 1)
    if len(message) != 0:
        screen.blit(fontobject.render(message, 1, (255,255,255)), ((screen.get_width() / 2) - 100, (screen.get_height() / 2) +20))
    pygame.display.flip()


def ask(screen, question):
    pygame.font.init()
    current_string = []
    display_box(screen, question + ": " + string.join(current_string,""))
    while 1:
        inkey = get_key()
        if inkey == K_BACKSPACE:
            current_string = current_string[0:-1]
        elif inkey == K_RETURN:
            break
        elif inkey == K_MINUS:
            current_string.append("_")
        elif inkey <= 127:
            current_string.append(chr(inkey))
        display_box(screen, question + ": " + string.join(current_string,""))
    return string.join(current_string,"")


def get_key():
    while 1:
        event = pygame.event.poll()
        if event.type == KEYDOWN:
            return event.key
        else:
            pass

def saver():
    # Saving The clues in the .txt file
    thefile = open("oldPuzzles/"+record + 'Clues.txt', 'w')
    for item in Clues:
        thefile.write("%s\n" % item)
    # Saving the Title in the .txt file
    thefile = open("oldPuzzles/"+record + 'Titles.txt', 'w')
    for item in Titles:
        thefile.write("%s\n" % item)
    # Saving the labels of clues in the .txt file
    thefile = open("oldPuzzles/"+record + 'Labels.txt', 'w')
    for item in Labels:
        thefile.write("%s\n" % item)

    thefile = open("oldPuzzles/"+record + 'GridTiles.txt', 'w')
    for item in grid.Tiles:
        thefile.write("%s\n" % item)

    thefile = open("oldPuzzles/" + record + 'GridAnswers.txt', 'w')
    for item in grid.Answers:
        thefile.write("%s\n" % item)

    thefile = open("oldPuzzles/" + record + 'GridWords.txt', 'w')
    for item in grid.Words:
        thefile.write("%s\n" % item)


def Loader(puzzleDate):
    text_file = open("oldPuzzles/"+puzzleDate + "Clues.txt", "r")
    for line in text_file:
        current_string = []
        for count in range(0, line.__len__(), 1):
            if ord(line[count]) == 10:
                current_string.append(" ")
            else:
                current_string.append(str(line[count]))
        Clues.append(string.join(current_string, ""))
    text_file.close()

    text_file = open("oldPuzzles/"+puzzleDate + "Titles.txt", "r")
    for line in text_file:
        current_string = []
        for count in range(0,line.__len__(),1):
            if ord(line[count]) == 10:
                current_string.append(" ")
            else:
                current_string.append(str(line[count]))
        Titles.append(string.join(current_string,""))
    text_file.close()

    text_file = open("oldPuzzles/"+puzzleDate + "Labels.txt", "r")
    for line in text_file:
        current_string = []
        for count in range(0, line.__len__(), 1):
            if ord(line[count]) == 10:
                current_string.append(" ")
            else:
                current_string.append(str(line[count]))
        Labels.append(string.join(current_string, ""))
    text_file.close()

    text_file = open("oldPuzzles/" + puzzleDate + "GridWords.txt", "r")
    for line in text_file:
        current_string = []
        for ch in line:
            if ch.isupper():
                current_string.append(ch)
        grid.Words.append(current_string)
    text_file.close()

    with open("oldPuzzles/"+puzzleDate+"GridTiles.txt") as fp:
        soupTile = BeautifulSoup(fp, "html.parser")
        for tt in soupTile.findAll("g"):
            grid.Tiles.append(tt)
    fp.close()

    i=0
    text_file = open("oldPuzzles/"+puzzleDate+"GridAnswers.txt", "r")
    for line in text_file:
        current_string = []
        for count in range(0, line.__len__(), 1):
            if ord(line[count]) == 10:
                current_string.append(" ")
            else:
                current_string.append(str(line[count]))
        grid.Answers[i] =string.join(current_string, "")
        i+=1
    text_file.close()


def CheckMousePos(mousePositionx, mousePositiony):
        mposx = mousePositionx
        mposy = mousePositiony
        if mposx < int(float(grid.Tiles[0].find("rect").get("x"))) or mposx > int(float(grid.Tiles[24].find("rect").get("x")))+100 or mposy < int(float(grid.Tiles[0].find("rect").get("y"))) or mposy > int(float(grid.Tiles[24].find("rect").get("y")))+100:
            return None
        arr =[]
        arr.append(mposx)
        arr.append(mposy)
        return arr

def SolvePuzzle(screen):
    #for clue in Clues:
    #    print(clue)
    #    with open('clues.csv') as csvfile:
    #        readCSV = csv.reader(csvfile, delimiter=',')
    #        for row in readCSV:
    #            if str(clue).replace(' ', '') == str(row[13]).replace(' ', ''):
    #                print(row[14])
    #        print("Finished")

    #english_words = load_words()

    """""
    with open('clues.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')

        for row in readCSV:
            if len(row[14]) <= 5:
                english_words[row[14]] = 1
    print english_words
    """

    english_words = {}
    with open('other.txt') as words:
        for row in words:
            row = row.strip()
            if len(row) <= 5:
                english_words[row] = 1
    print len(english_words)

    possibleAnswersToClues = [{},{},{},{},{},{},{},{},{},{}]
    gs = GridState()
    """"
    for i in range(0, 10, 1):
        with open('clues.csv') as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            for row in readCSV:
                if str(Clues[i]).replace(' ', '') == str(row[13]).replace(' ', '') and len(row[14]) <= 5:
                    possibleAnswersToClues[i][row[14]] = 1

    for i in range(0, 10, 1):
        if len(possibleAnswersToClues[i]) >= 1:

            for el in possibleAnswersToClues[i].keys():
                print el

                if len(el) != len(grid.Words[i]):
                    possibleAnswersToClues[i].pop(el, 1)


    possibleAnswersToCluesIter = [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}]
    possibleAnswersToCluesIter = copy.deepcopy(possibleAnswersToClues)

    for i in range(0, 10, 1):
        if len(possibleAnswersToClues[i]) >= 1:
            gs.addWord(possibleAnswersToClues[i].keys()[0], i, screen)

    print 'WORDS: ', gs.Words

    
    a = -1
    isEnteredCorrect = False
    solvedPartial = False
    while not solvedPartial:
        for i in range(0, 5, 1):
            for x in range(0, 10, 1):
                for el in possibleAnswersToClues[x]:
                    if el == gs.Words[i]:
                        a = x
            print a, len(possibleAnswersToClues[a].keys())
            for k in range(0, len(possibleAnswersToClues[a].keys()), 1):

                print isEnteredCorrect
                if isEnteredCorrect:
                    break
                if len(gs.Words[i]) != 0:
                    while not isEnteredCorrect and len(possibleAnswersToClues[a].keys()) != 0:
                        isEnteredCorrect = True
                        print 'Keys: ', possibleAnswersToClues[a].keys()
                        for j in range(0, len(gs.Words[i]), 1):
                            print 'i: ', i, ' j: ', j
                            print 'Words: ', gs.Words[i], gs.Words[5 + j]
                            if len(gs.Words[5 + j]) != 0 and len(gs.Words[5 + j]) > i  and gs.Words[i][j] != gs.Words[5 + j][i]:
                                isEnteredCorrect = False
                                print 'Wrong word found!'
                                break
                        if not isEnteredCorrect:
                            gs.addWord(possibleAnswersToClues[a].keys()[0], i, screen)
                            possibleAnswersToClues[a].pop(possibleAnswersToClues[a].keys()[0], 1)
            if isEnteredCorrect:
                break
            possibleAnswersToClues = copy.deepcopy(possibleAnswersToCluesIter)
            possibleAnswersToClues.po
            print isEnteredCorrect
        solvedPartial = isEnteredCorrect
    print 'Finished'

    solvePuzzleRecursion()
    """
    #for el in string.ascii_lowercase:
    #    findWord(0, el,  english_words, len(grid.Words[7]), 7)

    solution = solveRecursion(english_words, gs)

    if solution is not None:
        print solution.Words
    else:
        print 'Could not find a valid solution!'
def updateGameScreenGridChars(screen):
    screen.fill(white);
    for nn in range(0, grid.Tiles.__len__(), 1):
        tile = grid.Tiles[nn].find("rect")
        if tile.get("fill") == "black":
            pygame.draw.rect(screen, black, (float(tile.get("x")), float(tile.get("y")), 100, 100), 0)
            grid.Chars[nn] = ""
        else:
            pygame.draw.rect(screen, black, (float(tile.get("x")), float(tile.get("y")), 100, 100), 1)
        for number in grid.Tiles[nn].findAll("text", {"text-anchor": "start"}):
            text = font.render(number.text, 1, (0, 0, 0))
            screen.blit(text, (float(number.get("x")), float(number.get("y")) - 30))
        if grid.Chars[nn] != "":
            text = font.render(grid.Chars[nn].upper(), 1, (0, 0, 0))
            screen.blit(text, (float(tile.get("x")) + 20, float(tile.get("y")) + 20))
    pygame.display.update()
    time.sleep(.5)


def solvePuzzleRecursion():
    print 'done'


colWords = ['','','','','']
def solveRecursion(words, gridS, level=0):
    global colWords
    print 'Row Words: ', gridS.Words, 'Col Words: ', colWords
    spaceAvailable = False
    for i in range(0, 5):
        if len(gridS.Words[i]) == 0:
            spaceAvailable = True
            break
    if len(words) == 0 or not spaceAvailable:
        if gridS.isValidSol():
            return gridS
        else:
            return None

    for word in sorted(words.keys()):
        if gridS.fillFirst(word):


            blackCount = 0
            for i in range(0, 5):
                tile = grid.Tiles[level * 5 + i].find("rect")
                if tile.get("fill") == "black":
                    blackCount += 1
                else:
                    break
            for i, chr in enumerate(word):

                colWords[blackCount + i] += chr
            contToRec = True
            for col in colWords:
                hasWord = False
                for wrd in words.keys():
                    if wrd.startswith(col):
                        hasWord = True
                        break
                if not hasWord:
                    #print 'COL : ', col, 'Col Words*: ', colWords, 'ROWS: ', gridS.Words
                    contToRec = False
                    break
            words.pop(word, 1)
            if contToRec:
                ret = solveRecursion(words, gridS, level+1)
                if ret:
                    return ret
                else:
                    words[word] = 1
                    gridS.reverseState(word)
            else:
                #print 'NONE RETURNED'
                #print 'BEFORE: ', gridS.Words
                words[word] = 1
                gridS.reverseState(word)
                #print 'AFTER: ', gridS.Words
            for i in range(0, 5):
                if len(colWords[i]) != 0:
                    colWords[i] = colWords[i][:-1]

    return None


def findWord(chrIndex ,chr, words, length, wordNumber):
    for word in words:
        if word[chrIndex] == chr and word.__len__() == length:
            for i in range(0, length):
                if wordNumber < 5:
                    grid.Chars[i + 5 * wordNumber] = word[i]
                else:
                    grid.Chars[(wordNumber % 5) + i * 5] = word[i]

def load_words():
    try:
        filename = os.path.dirname(sys.argv[0]) + "\\" + "words_dictionary.json"
        with open(filename, "r") as english_dictionary:
            valid_words = json.load(english_dictionary)
            return valid_words
    except Exception as e:
        return str(e)


class GridState:
    Chars = []
    Words = []
    lastModifiedIndex = 0

    def __init__(self):
        for i in range(0, 25, 1):
            self.Chars.append("")
        for i in range(0, 10, 1):
            self.Words.append([])
        self.lastModifiedIndex = 4

    def isValid(self, wordList):

        for a in range(0, 10, 1):
            for i in range(0, 5, 1):
                if a < 5:
                    self.Words[i][a] = self.Chars[a + 5 * i]
                else:
                    self.Words[i][a] = self.Chars[(i % 5) + a * 5]

        for word in self.Words:
            if word not in wordList.keys():
                return False
        return True

    def isValidSol(self):

        # for j in range(0, len(gridState)):
        #    for i in range(0,len(gridState[j])):
        #        if gridState[j] != grid.Words[j][i]:
        #            return False
        print 'asfasf', self.Words, grid.Words
        for i in range(0, 5):
            for a,b in zip(self.Words[i], grid.Words[i]):
                if a != b:
                    return False
        return True

    def fillFirst(self, word):

        a = 0
        for i in range(0, 5):
            if len(self.Words[i]) == 0:
                a = i
                break
            else:
                a = -1

        if len(word) == len(grid.Words[a]) and a != -1:
            self.Words[a] = word
            for i in range(0, len(word)):
                    self.Chars[i + 5 * a] = word[i]
            return True
        return False

    def reverseState(self, word):
        self.Words[self.Words.index(word)] = ""

    def addWord(self, word, index, screen):

        print 'afasfasfasf', word, index
        if len(word) == len(grid.Words[index]):
            self.Words[index] = word
            for i in range(0, len(word)):
                if index < 5:
                    self.Chars[i + 5 * index] = word[i]
                else:
                    self.Chars[(index % 5) + i * 5] = word[i]
            print 'Added: ', self.Words
            a = 0
            for i in range(0, 25, 1):
                if grid.Answers[i] != ' ':
                    if self.Chars[a] != '':
                        grid.Chars[i] = self.Chars[a]
                        updateGameScreenGridChars(screen)
                    a += 1
                else:
                    if self.Chars[a] == '':
                        a += 1
            return True
        return False






Titles = []
Clues = []
Labels = []
grid = Grid()

black = (0, 0, 0);
white = (255, 255, 255);
green = (0,200,0)
bright_green = (0,255,0)
red = (200,0,0)
bright_red = (255,0,0)


pygame.init()
font = pygame.font.SysFont('C:\Windows\Fonts\Arial.ttf',30, False, False)


#puzzle_spider()
#saver()
Loader("10-12-2017")

printPuzzle()