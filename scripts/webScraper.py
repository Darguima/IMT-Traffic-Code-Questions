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

	try:
		opts, args = getopt(argv[1:], "hi:f:u:", ["help", "initialQuestion=","finalQuestion=","baseUrl="])
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


Examples of commands:

> webScraper.py -i 1 -f 5444 -u http://www.bomcondutor.pt/questao/
> webScraper.py --initialQuestion 1 --finalQuestion 5444 --baseUrl http://www.bomcondutor.pt/questao/

			""")
			exit()

		elif opt in ("-i", "--initialQuestion") and arg.isnumeric():
			initialQuestionNum = int(arg)

		elif opt in ("-f", "--finalQuestion") and arg.isnumeric():
			finalQuestionNum = int(arg)

		elif opt in ("-u", "--baseUrl"):
			baseUrl = arg
		
		else:
			print("\nInvalid values. Read documentation or help.")
			print("\n> webScraper -h\n")
			exit()

	return initialQuestionNum, finalQuestionNum, baseUrl

# Variables Initialization =====

initialQuestionNum, finalQuestionNum, baseUrl = scriptParameters()
optionLetters = ["A", "B", "C", "D"]
possibleCategories = ["A", "AM", "B", "C", "D"]

questions = []
ignoredQuestions = []

print("\n=============================================================")
print("=====================  Starting scraper =====================")
print("=============================================================")

print(f"\nscraping question from {initialQuestionNum} to {finalQuestionNum} from \"{baseUrl}\".")
print("\nQuestions:\n\n")

driver = webdriver.Firefox()

for questionNumber in range(initialQuestionNum, finalQuestionNum + 1):
	try:
		driver.get(baseUrl + str(questionNumber))

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

		print(f"\n{questionNumber} - {question}")
		questions.append(question)

	except NoSuchElementException:
		ignoredQuestions.append(questionNumber)

driver.close()

print("\n\n\nscrap ended!!\n")

print("Ignored Questions:")
print(ignoredQuestions)

with open('questions.json', 'w') as outfile:
    json.dump(questions, outfile)

print("\nscraped data recorder in \"questions.json\" file.")

print("\n\nThanks for using me! Visit https://www.github.com/Darguima !!\n")
