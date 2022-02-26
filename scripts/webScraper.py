#!/usr/bin/python

from sys import argv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

import json

# Script Parameters =====

"""
1. initialQuestionNum:
		optional
		number of the first IMTT Question to scrape
		default "1"

2. finalQuestionNum
		optional
		number of the last (inclusive) IMTT Question to scrape
		default "5444"

3. baseUrl
		optional
		base url for the scrape - need be a `bomcondutor.pt` page - used for offline version of the site
		default "http://www.bomcondutor.pt/questao/"
"""

initialQuestionNum = 1
finalQuestionNum = 5444
baseUrl = "http://www.bomcondutor.pt/questao/"

if len(argv) == 1: pass

elif len(argv) == 2 and argv[1].isnumeric():
	finalQuestionNum = int(argv[1])

elif len(argv) == 3 and argv[1].isnumeric() and argv[2].isnumeric():
	initialQuestionNum = int(argv[1])
	finalQuestionNum = int(argv[2])

elif len(argv) >= 4 and argv[1].isnumeric() and argv[2].isnumeric():
	initialQuestionNum = int(argv[1])
	finalQuestionNum = int(argv[2])
	baseUrl = argv[3]

else: print("\nInvalid parameters. Using default values.")

# Variables Initialization =====

letters = ["A", "B", "C", "D"]
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
				"letter": letters[index], # A, B, C or D
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
