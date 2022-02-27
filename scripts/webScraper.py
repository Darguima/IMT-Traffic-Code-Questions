#!/usr/bin/python

from sys import argv, exit
from getopt import getopt, GetoptError

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

import json

def scriptParameters ():
	initialQuestionNum = 1
	finalQuestionNum = 5444
	baseUrl = "http://www.bomcondutor.pt/questao/"
	inputFile = ""
	questions = []
	gottenQuestions = []
	outputFile = "questions.json"
	beforeQuestion = ""
	afterQuestion = ""

	try:
		opts, _ = getopt(argv[1:], "hi:f:u:i:o:b:a:", ["help", "initialQuestion=", "finalQuestion=", "baseUrl=", "inputFile=", "outputFile=", "beforeQuestion=", "afterQuestion="])
	except GetoptError:
		print("\nInvalid parameters. Read documentation or help.")
		print("\n> webScraper -h\n")
		exit()

	for opt, arg in opts:
		if opt in ["-h", "--help"]:
			print("""

-h     --help                Show this menu

-i     --initialQuestion     Receive the first question to scrap.\tDefault - 1
-f     --finalQuestion       Receive the last (included) question to scrap.\tDefault - 5444

-u     --baseUrl             Receive the base url to use on scrap. Need be a copy of `bomcondutor.pt`. Can be used offline copies of the site.\tDefault - http://www.bomcondutor.pt/questao/

-i     --inputFile           Receive the input file to continue the JSON.\tDefault - ""
-o     --outputFile          Receive the output file to store the JSON.\tDefault - ./questions.json

-b     --beforeQuestion      Receive the string to use before question number on the URL. Ex.: ".html".\tDefault - ""
-a     --afterQuestion       Receive the string to use after question number on the URL.\tDefault - ""

Examples of commands:

> webScraper.py
> webScraper.py -i 1 -f 5444 -u http://www.bomcondutor.pt/questao/ -a .html
> webScraper.py --initialQuestion 1 --finalQuestion 5444 --baseUrl http://www.bomcondutor.pt/questao/ --after .html

			""")
			exit()

		elif opt in ("-i", "--initialQuestion") and arg.isnumeric():
			initialQuestionNum = int(arg)

		elif opt in ("-f", "--finalQuestion") and arg.isnumeric():
			finalQuestionNum = int(arg)

		elif opt in ("-u", "--baseUrl"):
			baseUrl = arg
		
		elif opt in ("-i", "--inputFile"):
			inputFile = arg

			try:
				with open(inputFile, 'r') as inFile:
					questions = json.load(inFile)

				for question in questions:
					gottenQuestions.append(question["questionNumber"])
				gottenQuestions.sort()
				

			except FileNotFoundError:
				print(f"\nFile `{inputFile}` not founded\n")
				exit()
			except json.decoder.JSONDecodeError:
				print(f"\nFile `{inputFile}` not contain a JSON\n")
				exit()
			except:
				print(f"\nSomething wrong happened (maybe JSON syntax) on `{inputFile}`\n")
				exit()

		elif opt in ("-o", "--outputFile"):
			outputFile = arg

		elif opt in ("-b", "--beforeQuestion"):
			beforeQuestion = arg

		elif opt in ("-a", "--afterQuestion"):
			afterQuestion = arg
		
		else:
			print("\nInvalid values. Read documentation or help.")
			print("\n> webScraper -h\n")
			exit()

	return initialQuestionNum, finalQuestionNum, baseUrl, inputFile, questions, gottenQuestions, outputFile, beforeQuestion, afterQuestion

# Variables Initialization =====

initialQuestionNum, finalQuestionNum, baseUrl, inputFile, questions, gottenQuestions, outputFile, beforeQuestion, afterQuestion = scriptParameters()
optionLetters = ["A", "B", "C", "D"]
possibleCategories = ["A", "AM", "B", "C", "D"]

errorQuestions = []
skippedQuestions = []

print("\n=============================================================")
print("=====================  Starting scraper =====================")
print("=============================================================")

print(f"\nScraping question from {initialQuestionNum} to {finalQuestionNum} from \"{baseUrl}\".")
print(f"Storing JSON in `{outputFile}`")

if (inputFile != ""):
	print(f"\nContinuing the JSON in `{inputFile}` with questions number:")
	print(gottenQuestions)

if (beforeQuestion != ""): print(f"Before: {beforeQuestion}")
if (afterQuestion != ""): print(f"After: {afterQuestion}")
print("\nQuestions:\n\n")

driver = webdriver.Firefox()

try:
	for questionNumber in range(initialQuestionNum, finalQuestionNum + 1):
		if questionNumber in gottenQuestions:
			print(f"\n{beforeQuestion}{questionNumber}{afterQuestion} - skipped")
			skippedQuestions.append(questionNumber)
			continue

		try:
			driver.get(baseUrl + beforeQuestion + str(questionNumber) + afterQuestion)

			question = {
				"questionNumber": questionNumber,
				"category": "",
				"text": "",
				"options": [],
				"correctOptionIndex": 0
			}

			questionCategory = driver.find_element(by=By.CLASS_NAME, value="question-info").text.split(" ")[4:] # First char of text is always "A"
			categories = filter(lambda char: char in possibleCategories, questionCategory)
			question["category"] = list(categories)

			question["text"] = driver.find_element(by=By.CLASS_NAME, value="question-text").text

			options = driver.find_elements(by=By.CLASS_NAME, value="answer-text") 
			for index, answer in enumerate(options):
				isOptionCorrect = answer.value_of_css_property("background-color") != "rgba(0, 0, 0, 0)" # When background is white the option is wrong

				question["options"].append({
					"index": index, # 0, 1, 2 or 3
					"letter": optionLetters[index], # A, B, C or D
					"text": answer.text,
					"correct": isOptionCorrect
				})

				if (isOptionCorrect):
					question["correctOptionIndex"] = index

			print(f"\n{beforeQuestion}{questionNumber}{afterQuestion} - {question}")
			questions.append(question)
			gottenQuestions.append(questionNumber)

		except NoSuchElementException:
			errorQuestions.append(questionNumber)

except Exception as e:
	print("\n\nERROR: Something happened")
	print("=============================================")
	print(e)
	print("=============================================\n\n")

	print("\n\n\n\n\n===========================================================")
	print("We will try to store the questions on `webScrapper.bkp.json`")
	print("===========================================================\n\n\n\n\n")

	with open("webScrapper.bkp.json", 'w') as outfile:
		json.dump(questions, outfile)
	
	print("===========================================================")
	print("Questions saved on `webScrapper.bkp.json`")
	print("===========================================================\n\n\n\n\n")
	
	exit()

driver.close()

print("\n\n\nscrap ended!!")

errorQuestions.sort()
skippedQuestions.sort()
gottenQuestions.sort()

print("\nError Questions:")
print(errorQuestions)

print("\nSkipped Questions:")
print(skippedQuestions)

print("\nGotten Questions:")
print(gottenQuestions)

with open(outputFile, 'w') as outfile:
  json.dump(questions, outfile)

print(f"\nscraped data recorder in `{outputFile}` file.")

print("\n\nThanks for using me! Visit https://github.com/Darguima/IMTT-Traffic-Code-Questions !!\n")
