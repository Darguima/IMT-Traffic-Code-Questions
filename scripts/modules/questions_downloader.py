from os import mkdir
from os.path import exists

from requests import get

def questions_downloader (outputDir = "./questionsOffline", downloadAgain = False):
	print("\n========================================================")
	print("============  Starting questions downloader ============")
	print("========================================================")

	print(f"\nDownloading html files to \"{outputDir}\".")

	if not downloadAgain: print("Ignoring already downloaded files!")
	else: print("Downloading again already downloaded files!")

	if not exists(outputDir): mkdir(outputDir)

	for category in ["A", "B", "C", "D"]:
		print(f"\n\nStarting category \"{category}\".")
		print("Current Question:")

		if not exists(f"{outputDir}/{category}"): mkdir(f"{outputDir}/{category}")
		
		question_num = 0

		while True:
			if not downloadAgain and exists(f'{outputDir}/{category}/{question_num}'):
				question_num += 1
				print(f"\t{question_num:0>4} with skipped files", end="\r")
				continue

			file = get(f"https://testes-codigo.pt/questao/{category}/{question_num}", allow_redirects=False)

			if (file.status_code == 200):
				open(f'{outputDir}/{category}/{question_num}', 'wb').write(file.content)
				print(f"\t{question_num:0>4}", end="\r")
				question_num += 1

			else:
				break