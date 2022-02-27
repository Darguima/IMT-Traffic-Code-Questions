#!/usr/bin/python

from sys import argv, exit
from getopt import getopt, GetoptError
import json

def scriptParameters ():
	inputFileName = "questions.json"
	questions = None
	outputFileName = "questionsIndented.json"
	outputFile = None
	tabSize = 2

	try:
		opts, _ = getopt(argv[1:], "hi:o:t:", ["help", "inputFile=", "outputFile=", "tabSize="])
	except GetoptError:
		print("\nInvalid parameters. Read documentation or help.")
		print("\n> indenterJsonFile.py -h\n")
		exit()
	
	for opt, arg in opts:
		if opt in ("-h", "--help"):
			print("""

-h     --help                Show this menu

-i     --inputFile           Receive the JSON input file to indent.\tDefault - ./questions.json
-o     --outputFile          Receive the output file to store the indented JSON.\tDefault - ./questionsIndented.json

-t     --tabSize             Receive the number of spaces on the tab.\tDefault - 2

Examples of commands:

> indenterJsonFile.py
> indenterJsonFile.py -i questions.json -o questionsIndented.json -t 2
> indenterJsonFile.py --inputFile questions.json --outputFile questionsIndented.json --tabSize 2

			""")
			exit()
		
		elif opt in ("-i", "--inputFile"):
			inputFileName = arg

			try:
				with open(inputFileName, 'r') as inputFile:
					questions = json.load(inputFile)

			except FileNotFoundError:
				print(f"\nFile `{inputFileName}` not founded\n")
				exit()
			except json.decoder.JSONDecodeError:
				print(f"\nFile `{inputFileName}` not contain a JSON\n")
				exit()
			except:
				print(f"\nSomething wrong happened (maybe JSON syntax) on `{inputFileName}`\n")
				exit()

		elif opt in ("-o", "--outputFile"):
			outputFileName = arg

		elif opt in ("-t", "--tabSize") and arg.isnumeric():
			tabSize = int(arg)
		
		else:
			print("\nInvalid values. Read documentation or help.")
			print("\n> indenterJsonFile.py -h\n")
			exit()
		
	if questions == None:
		try:
			with open(inputFileName, 'r') as inputFile:
				questions = json.load(inputFile)

		except FileNotFoundError:
			print(f"\nFile `{inputFileName}` not founded\n")
			exit()
		except json.decoder.JSONDecodeError:
			print(f"\nFile `{inputFileName}` not contain a JSON\n")
			exit()
		except:
			print(f"\nSomething wrong happened (maybe JSON syntax) on `{inputFileName}`\n")
			exit()
		
	try:
		outputFile = open(outputFileName, "w")
	except FileNotFoundError:
		print(f"\nFile `{outputFileName}` cannot be created\n")
		exit()

	return inputFileName, questions, outputFileName, outputFile, tabSize

inputFileName, questions, outputFileName, outputFile, tabSize = scriptParameters()

print("\n==============================================================")
print("=====================  Starting indenter =====================")
print("==============================================================")

print(f"\nInput File: {inputFileName}")
print(f"\nOutput File: {outputFileName}")
print(f"\nIndent Tab Size: {tabSize}")

json.dump(questions, outputFile, indent=tabSize)

outputFile.close()
