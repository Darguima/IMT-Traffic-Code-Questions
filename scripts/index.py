#!/usr/bin/python

from modules.questions_downloader import questions_downloader
from modules.questions_scrape import questions_scrape
from modules.store_json import store_json
from modules.images_downloader import images_downloader


download_mode = True
download_directory = "./questionsOffline"
download_again = False
output_file = "./questions.json"

if download_mode:
	base_url = download_directory
else: 
	base_url = "https://testes-codigo.pt/questao/"

print("\n========================================================")
print("===================  Starting Scrape ===================")
print("========================================================")

print()
print(f"Download Mode      - {download_mode}")
print(f"Download Directory - {download_directory}")
print(f"Download Again     - {download_again}")
print(f"Base Url           - {base_url}")
print(f"Output File        - {output_file}")

if download_mode: questions_downloader(download_directory, download_again)

questions = questions_scrape(base_url)

if download_mode: images_downloader(questions, download_directory, download_again)

store_json(questions, output_file)

print(f"\n\nDone!!\n")
