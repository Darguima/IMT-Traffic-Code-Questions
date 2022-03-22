#!/usr/bin/python

from sys import argv, exit
from getopt import getopt, GetoptError

import json


def scriptParameters():
	inputFile = "questions.json"
	questions = []
	initialQuestion = 1
	finalQuestion = 5444

	try:
		opts, _ = getopt(argv[1:], "hj:i:f:", ["help", "jsonFile=", "initialQuestion=", "finalQuestion="])
	except GetoptError:
		print("\nInvalid parameters. Read documentation or help.")
		print("\n> verifyJson.py -h\n")
		exit()

	for opt, arg in opts:
		if opt in ["-h", "--help"]:
			print("""

-h     --help                Show this menu

-j     --jsonFile            Receive the input file to verify the JSON.\tDefault - "questions.json"

-i     --initialQuestion     Receive the first question that need be on file.\tDefault - 1
-f     --finalQuestion       Receive the last (included) question that need be on file.\tDefault - 5444

Examples of commands:

> verifyJson.py
> verifyJson.py -j questions.json -i 1 -f 5444
> verifyJson.py --jsonFile questions.json --initialQuestion 1 --finalQuestion 5444

			""")
			exit()

		elif opt in ("-j", "--jsonFile"):
			inputFile = arg

		elif opt in ("-i", "--initialQuestion") and arg.isnumeric():
			initialQuestion = int(arg)

		elif opt in ("-f", "--finalQuestion") and arg.isnumeric():
			finalQuestion = int(arg)
		
		else:
			print("\nInvalid values. Read documentation or help.")
			print("\n> verifyJson -h\n")
			exit()
	
	try:
		with open(inputFile, 'r') as inFile:
			file_questions = json.load(inFile)

		for question in file_questions:
			questions.append(question)

	except FileNotFoundError:
		print(f"\nFile `{inputFile}` not founded\n")
		exit()
	except json.decoder.JSONDecodeError:
		print(f"\nFile `{inputFile}` not contain a JSON\n")
		exit()
	except:
		print(f"\nSomething wrong happened (maybe JSON syntax) on `{inputFile}`\n")
		exit()
	
	questionsNumbers = list(range(initialQuestion, finalQuestion + 1))
		
	return inputFile, questions, initialQuestion, finalQuestion, questionsNumbers

# Variables Initialization =====

inputFile, questions, initialQuestion, finalQuestion, questionsNumbers = scriptParameters()

print("\n==============================================================")
print("===================  Starting verification ===================")
print("==============================================================")

print(f"\nVerifying question from {initialQuestion} to {finalQuestion} from \"{inputFile}\".\n")

possibleCategories = ["A", "AM", "B", "C", "D"]

possibleThemes = {
	"AM": ["Cedência de passagem, condução defensiva e peões", "Circulação, segurança, veículos missão urgente", "Classificação, caractericas dos veículos, ambiente, iluminação, equipamentos, acidente, passageiros", "Estado físico do condutor, álcool, drogas e medicamentos", "Paragem, estacionamento e cruzamento de veículos, ultrapassagem", "Sinais de Cedência de Passagem", "Sinais de Indicação", "Sinais de Perigo", "Sinais de Proibição", "Sinais de obrigação", "Sinalização luminosa, marcas rodoviárias, outra sinalização", "Títulos, obtenção, revalidação, responsabilidade civil e criminal, contra ordenações, cassação", "Velocidade,outras manobras, condicionantes da velocidade", "Vias de trânsito e condições ambientais adversas"],
	"A": ["Classificação das vias", "Constituintes do veículo", "Equipamento de Protecção", "Visibilidade relativamente aos outros utentes da via"],
	"B": [ "Cedência de passagem", "Circulação, segurança e veículos em missão urgente de socorro", "Classificação, constituintes, inspecções, pesos e dimensões, protecção de ambiente, equipamentos de segurança, acidente", "Estado físico do condutor, alcool, drogas e medicamentos, sinais de obrigação", "Iluminação, passageiros e carga, condução defensiva e peões", "Outras manobras", "Paragem, estacionamento e cruzamento de veículos", "Sinais de indicação", "Sinais de perigo", "Sinais de prescrição específica, sinais de cedência de passagem", "Sinais de proibição", "Sinalização luminosa, marcas no pavimento e outra sinalização", "Títulos de condução, obtenção, revalidação, responsabilidade civil e criminal, contra-ordenações, cassação", "Ultrapassagem", "Velocidade", "Vias de trânsito, condições ambientais adversas"],
	"C": ["Classificação de Veículos e Inspecções Periódicas", "Documentos de que o condutor deverá ser portador", "Logística (tipos, utilização, leitura e manutenção)", "Manutenção", "Noções Básicas do Veículo", "Períodos de Condução e Repouso", "Protecção do Ambiente e Equipamentos de Segurança", "Transporte de Mercadorias"],
	"D": ["Classificação de Veículos e Inspecções Periódicas", "Documentos de que o condutor deverá ser portador", "Logística (tipos, utilização, leitura e manutenção)", "Manutenção", "Noções Básicas do Veículo", "Períodos de Condução e Repouso", "Protecção do Ambiente e Equipamentos de Segurança", "Transporte de Passageiros"]
}

validQuestions = []
invalidQuestions = []
verifiedQuestions = []

for question in questions:

	#questionNumber
	if not "questionNumber" in question:
		print(f"Question num \"unknown\" - Missing 'Question Number'")
		invalidQuestions.append("unknown")
		continue

	elif not isinstance(question["questionNumber"], int):
		print(f"Question num \"{question['questionNumber']}\" - 'Question number' invalid")
		invalidQuestions.append(question['questionNumber'])
		continue
	
	elif not initialQuestion <= question["questionNumber"] <= finalQuestion:
		# questionNumber out of range
		continue
	
	elif question["questionNumber"] in verifiedQuestions:
		print(f"Question num \"{question['questionNumber']}\" - Question repeated")
		invalidQuestions.append(question['questionNumber'])
		continue

	#category
	if not "category" in question:
		print(f"Question num \"{question['questionNumber']}\" - Missing 'Category'")
		invalidQuestions.append(question['questionNumber'])
		continue

	elif len(question["category"]) == 0: 
		print(f"Question num \"{question['questionNumber']}\" - Missing 'Category' Values")
		invalidQuestions.append(question['questionNumber'])
		continue

	elif any(cat not in possibleCategories for cat in question["category"]):
		print(f"Question num \"{question['questionNumber']}\" - Invalid Category")
		invalidQuestions.append(question['questionNumber'])
		continue

	#theme
	if not "theme" in question:
		print(f"Question num \"{question['questionNumber']}\" - Missing 'Theme'")
		invalidQuestions.append(question['questionNumber'])
		continue

	else:
		questionPossibleCategories = []
		for cat in question["category"]:
			questionPossibleCategories += possibleThemes[cat]
		
		if not question["theme"] in questionPossibleCategories:
			print(f"Question num \"{question['questionNumber']}\" - 'Theme' invalid for this categories")
			invalidQuestions.append(question['questionNumber'])
			continue
		
	#text
	if not "text" in question:
		print(f"Question num \"{question['questionNumber']}\" - Missing Question 'Text'")
		invalidQuestions.append(question['questionNumber'])
		continue

	elif not isinstance(question["text"], str):
		print(f"Question num \"{question['questionNumber']}\" - Question 'Text' invalid")
		invalidQuestions.append(question['questionNumber'])
		continue

	#imageHash
	if not "imageHash" in question:
		print(f"Question num \"{question['questionNumber']}\" - Missing Question 'Image Hash'")
		invalidQuestions.append(question['questionNumber'])
		continue

	elif not isinstance(question["imageHash"], str) and len(question["imageHash"]) != 16:
		print(f"Question num \"{question['questionNumber']}\" - Question 'Image Hash' invalid")
		invalidQuestions.append(question['questionNumber'])
		continue

	#options
	if not "options" in question:
		print(f"Question num \"{question['questionNumber']}\" - Missing 'Options'")
		invalidQuestions.append(question['questionNumber'])
		continue
	
	elif not isinstance(question["options"], list):
		print(f"Question num \"{question['questionNumber']}\" - Question 'Options' invalid")
		invalidQuestions.append(question['questionNumber'])
		continue

	elif len(question["options"]) == 0: 
		print(f"Question num \"{question['questionNumber']}\" - Missing 'Options' Values")
		invalidQuestions.append(question['questionNumber'])
		continue

	else:
		trueAmounts = 0
		correctOptionIndex = None
		for index, option in enumerate(question["options"]):
		# options -> text
			if not "text" in option:
				print(f"Question num \"{question['questionNumber']}\" - Missing 'Text' on 'Options'")
				invalidQuestions.append(question['questionNumber'])
				continue

			elif not isinstance(option["text"], str):
				print(f"Question num \"{question['questionNumber']}\" - 'Text' on 'Options' invalid")
				invalidQuestions.append(question['questionNumber'])
				continue
		
			# options -> correct
			if not "correct" in option:
				print(f"Question num \"{question['questionNumber']}\" - Missing 'Correct' on 'Options'")
				invalidQuestions.append(question['questionNumber'])
				continue

			elif not isinstance(option["correct"], bool):
				print(f"Question num \"{question['questionNumber']}\" - 'correct' on 'Options' invalid")
				invalidQuestions.append(question['questionNumber'])
				continue

			elif option["correct"]:
				trueAmounts += 1
				correctOptionIndex = index
			
		if trueAmounts != 1:
			print(f"Question num \"{question['questionNumber']}\" - more than one/none correct option on 'Options'")
			invalidQuestions.append(question['questionNumber'])
			continue

	if not "correctOptionIndex" in question:
		print(f"Question num \"{question['questionNumber']}\" - Missing 'Correct Option Index'")
		invalidQuestions.append(question['questionNumber'])
		continue

	elif not isinstance(question["correctOptionIndex"], int):
		print(f"Question num \"{question['questionNumber']}\" - 'Correct Option Index' invalid")
		invalidQuestions.append(question['questionNumber'])
		continue

	elif not 0 <= question["correctOptionIndex"] <= 3:
		print(f"Question num \"{question['questionNumber']}\" - 'Correct Option Index' out of range")
		invalidQuestions.append(question['questionNumber'])
		continue

	elif question["correctOptionIndex"] != correctOptionIndex:
		print(f"Question num \"{question['questionNumber']}\" - incorrect 'Correct Option Index'")
		invalidQuestions.append(question['questionNumber'])
		continue
	
	verifiedQuestions.append(question["questionNumber"])

print("\n\nInvalid Questions:")
print(invalidQuestions)

questionsNumbers = list(
	filter(lambda questionNumber: 
		questionNumber not in invalidQuestions and questionNumber not in verifiedQuestions
		, questionsNumbers
	)
)

print("\n\nNot founded questions:")
print(questionsNumbers)

print("\nBye!\n")
