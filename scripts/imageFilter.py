#!/usr/bin/python

from sys import argv, exit
from getopt import getopt, GetoptError

from os import listdir, mkdir
from os.path import isfile, join, exists
from shutil import copyfile

from PIL import Image
import imagehash

import json

def scriptParameters():
	in_directory = None
	out_directory = None
	outputFile = "./images.json"

	try:
		opts, _ = getopt(argv[1:], "hi:o:f:", ["help", "inputDirectory=", "outputDirectory=", "outputFile="])
	except GetoptError:
		print("\nInvalid parameters. Read documentation or help.")
		print("\n> imageFilter.py -h\n")
		exit()

	for opt, arg in opts:
		if opt in ["-h", "--help"]:
			print("""

-h     --help                Show this menu

-i     --inputDirectory           (Required) Receive the input directory with images files.
-o     --outputDirectory          (Required) Receive the directory to store images files with hashes names.

NOTE: All files in inputDirectory need be named like "{questionNumber}.jpg" or "{questionNumber}.png".

-f     --outputFile          Receive the output file to store the JSON.\tDefault - ./images.json


Examples of commands:

> imageFilter.py
> imageFilter.py -i images -o questionsImages -f imageHashes.json

			""")
			exit()

		elif opt in ("-i", "--inputDirectory"):
			in_directory = arg

		elif opt in ("-o", "--outputDirectory"):
			out_directory = arg
		
		elif opt in ("-f", "--outputFile"):
			outputFile = arg
	
	if in_directory == None or out_directory == None:
		print("\nInvalid parameters. Read documentation or help.")
		print("Need to set inputDirectory and outputDirectory.")
		print("\n> imageFilter.py -h\n")
		exit()

	
	try:
		imagesFiles = list(filter(lambda fileName:  
			isfile(join(in_directory, fileName)) and
			fileName.find(".") > 0 and
			fileName[:fileName.find(".")].isnumeric() and				# name start with question number
			fileName[fileName.find(".") + 1:] in ("jpg", "jpeg", "png")	# end with .jpg or .png
		, listdir(in_directory)))

		imagesFiles = list(map(lambda fileName:
			{
				"fileName": fileName,
				"questionNumber": fileName[:fileName.find(".")]
			}
		, imagesFiles))	

	except FileNotFoundError:
		print("\nInput Directory Not Founded")
		print("\n> imageFilter.py -h\n")
		exit()

	return in_directory, out_directory, outputFile, imagesFiles

# Variables Initialization =====

in_directory, out_directory, outputFile, imagesFiles = scriptParameters()
img_format = ""

if not exists(out_directory): mkdir(out_directory)

print("\n========================================================")
print("===================  Starting filter ===================")
print("========================================================")

print(f"\nFiltering images from \"{in_directory}\" to \"{out_directory}\" and saving output info in \"{outputFile}\".")

img_format = imagesFiles[0]["fileName"][imagesFiles[0]["fileName"].find(".") + 1:]

print(f"\nWere founded {len(imagesFiles)} images on \"{in_directory}\".")

imagesHash = {}

for image in imagesFiles:
	hash = imagehash.dhash(Image.open(f'{in_directory}/{image["fileName"]}'))

	if hash.__str__() not in imagesHash:
		imagesHash[hash.__str__()] = []
	
	imagesHash[hash.__str__()].append(image)

images = {}

for img_hash in imagesHash:
	for img in imagesHash[img_hash]:
		copyfile(f'{in_directory}/{img["fileName"]}', f'{out_directory}/{img_hash}.{img_format}')
		images[img["fileName"]] = img_hash

with open(outputFile, 'w') as outfile:
  json.dump(images, outfile, indent=2)
