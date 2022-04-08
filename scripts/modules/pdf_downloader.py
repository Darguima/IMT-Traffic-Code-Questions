from os import mkdir
from os.path import exists

from urllib import request
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


def pdf_downloader (download_directory, download_again):
	print("\n========================================================")
	print("=============== Starting PDFs downloader ===============")
	print("========================================================")

	print(f"\nDownloading PDFs files to \"{download_directory}\".")

	if not download_again: print("Not downloading already downloaded PDFs!")
	else: print("Downloading again already downloaded PDFs!")

	if not exists(download_directory): mkdir(download_directory)

	print("\n\n")
	for pdf_index in range(1, 15):
		if not download_again and exists(f'{download_directory}/rel_{pdf_index}_condutores.pdf'):
			print(f"Downloading PDF number {pdf_index} with skipped files", end="\r")
			continue

		print(f"Downloading PDF number {pdf_index}", end="\r")

		request.urlretrieve(
			f'https://www.imt-ip.pt/sites/IMTT/Portugues/Condutores/PerguntasExames/Documents/rel_{pdf_index}_condutores.pdf',
			f'{download_directory}/rel_{pdf_index}_condutores.pdf'
		)
	
	print("")
