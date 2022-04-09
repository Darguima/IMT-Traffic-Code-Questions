from os import mkdir
from os.path import exists

from PIL import Image, ImageDraw
from imagehash import dhash, hex_to_hash
from requests import get, packages

import fitz
from io import BytesIO
from urllib3.exceptions import InsecureRequestWarning
packages.urllib3.disable_warnings(category=InsecureRequestWarning)


def pdf_images_scraper (download_directory, images_output_dir):
  print("\n========================================================")
  print("================  Starting PDFs scraper ================")
  print("========================================================")

  print(f"\nScraping PDFs files to \"{images_output_dir}\".\n")

  if not exists(images_output_dir): mkdir(images_output_dir)

  scraped_images = []

  for pdf_index in range(1, 15):
    if (exists(f"{download_directory}/rel_{pdf_index}_condutores.pdf")):
      pdf_file = fitz.open(f"{download_directory}/rel_{pdf_index}_condutores.pdf")

    else:
      print(f"Downloading PDF number {pdf_index}", end="\r")
      r = get(f"https://www.imt-ip.pt/sites/IMTT/Portugues/Condutores/PerguntasExames/Documents/rel_{pdf_index}_condutores.pdf", stream=True, verify=False)
      pdf_file = fitz.open("pdf", stream=r.content)

    print(f"Scraping PDF number {pdf_index} ...")

    for page_index, page in enumerate(pdf_file):
      for image_index, img in enumerate(page.get_images(), start=1):
        # get the XREF of the image
        xref = img[0]
          
        # extract the image bytes
        base_image = pdf_file.extract_image(xref)
        image_bytes = base_image["image"]

        img = Image.open(BytesIO(image_bytes))
        draw = ImageDraw.Draw(img)
        
        if img.size == (300, 199) or img.size == (300, 200):
          draw.rectangle(((14, 164), (56, 187)), fill="black")
        
        elif img.size == (408, 271) or img.size == (409, 272):
          draw.rectangle(((13, 223), (90, 259)), fill="black")
        
        elif img.size == (450, 299) or img.size == (451, 300):
          draw.rectangle(((14, 247), (98, 288)), fill="black")

        elif img.size == (556, 368) or img.size == (555, 369) or img.size == (556, 369) or img.size == (556, 372):
          draw.rectangle(((14, 310), (117, 358)), fill="black")

        else:
          if (img.size == (345, 62) and str(dhash(img)) == "84a4a0252d252c2c"):
            continue
          else:
            print(f"Resolution not founded in {page_index},{image_index} - {img.size}")
        
        img_hash = str(dhash(img))

        Image.open(BytesIO(image_bytes)).save(f"{images_output_dir}/{img_hash}.jpg", "JPEG")
        
        if img_hash not in scraped_images:
          scraped_images.append(img_hash)

  return scraped_images
