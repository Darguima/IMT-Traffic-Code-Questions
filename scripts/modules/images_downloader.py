from os import mkdir
from os.path import exists
from requests import get
from PIL import Image, ImageDraw


def images_downloader (questions, outputDir = "./questionsOffline", downloadAgain = False):
	print("\n========================================================")
	print("==============  Starting image downloader ==============")
	print("========================================================")

	print(f"\nDownloading image files to \"{outputDir}\".")

	if not downloadAgain: print("Ignoring already downloaded files!")
	else: print("Downloading again already downloaded files!")

	if not exists(outputDir): mkdir(outputDir)

	print("\nEstimated Amount of Images:")
	print("\tCat A - 592")
	print("\tCat B - 3909")
	print("\tCat C - 306")
	print("\tCat D - 346")

	for category in questions:
		print(f"\n\nStarting category \"{category}\".")
		print("Current Question:")

		if not exists(f"{outputDir}/imgs{category}"): mkdir(f"{outputDir}/imgs{category}")

		for question in questions[category]:
			if not downloadAgain and exists(f"{outputDir}/imgs{category}/{question['imageId']}.jpg"):
				print(f"\t{question['questionNumber']:0>4} with skipped files", end="\r")
				continue

			file = get(f"https://testes-codigo.pt/bd/imgs{category}/{question['imageId']}.jpg", stream=True, allow_redirects=False)

			if (file.status_code == 200):

				img = Image.open(file.raw)
				draw = ImageDraw.Draw(img)
				
				if img.size == (300, 199) or img.size == (300, 200):
					draw.rectangle(((14, 164), (56, 187)), fill="black")
				
				elif img.size == (409, 272):
					draw.rectangle(((14, 224), (89, 258)), fill="black")
				
				elif img.size == (450, 299) or img.size == (451, 300):
					draw.rectangle(((14, 247), (98, 288)), fill="black")

				elif img.size == (556, 368) or img.size == (556, 369) or img.size == (556, 372):
					draw.rectangle(((14, 310), (117, 358)), fill="black")

				else:
						print(f"Resolution not founded in {question['imageId']} - {img.size}")

				img.save(f"{outputDir}/imgs{category}/{question['imageId']}.jpg", "JPEG")
				print(f"\t{question['questionNumber']:0>4}", end="\r")

			else:
				print(f"\n\nERROR - question {question['questionNumber']} has invalid image ID!\n")
				continue