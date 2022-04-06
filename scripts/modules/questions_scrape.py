from modules.scraper import scrape_question


def questions_scrape (baseUrl):
	print("\n\n========================================================")
	print("======================== Scrape ========================")
	print("========================================================")

	print(f"\nScraping questions from \"{baseUrl}\".\n")
	print("Current Question:")

	questions = {"A": [], "B": [], "C": [], "D": []}

	for category in questions:
		quest_number = 0

		while True:
			question = scrape_question(category, quest_number, baseUrl)
			
			if question == "responseCode":
				break

			elif isinstance(question, str): # Error
				print(f"\n\n{question}")
				if input("\nContinue (y/n): ").lower() != "y":
					exit()
			
			else:
				questions[category].append(question)

			quest_number += 1

			print(f"\tCat {category} - Question {quest_number:0>4}", end="\r")
		
	print("\n\nQuestions Scraped:")
	print(f"\tCategory A - {len(questions['A']):0>4} (of 0593) questions")
	print(f"\tCategory B - {len(questions['B']):0>4} (of 3910) questions")
	print(f"\tCategory C - {len(questions['C']):0>4} (of 0307) questions")
	print(f"\tCategory D - {len(questions['D']):0>4} (of 0350) questions")

	return questions