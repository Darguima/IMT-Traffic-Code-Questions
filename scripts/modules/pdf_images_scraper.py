from os import mkdir, system, listdir, remove, rename
from os.path import exists
from PIL import Image, ImageDraw
from imagehash import dhash, hex_to_hash


def pdf_images_scraper (download_directory, images_output_dir):
  print("\n========================================================")
  print("================  Starting PDFs scraper ================")
  print("========================================================")

  print(f"\nScraping PDFs files to \"{images_output_dir}\".\n")

  if not exists(images_output_dir): mkdir(images_output_dir)

  scraped_images = []

  for pdf_index in range(1, 15):
    print(f"Scraping PDF number {pdf_index}", end="\r")
    system(f"pdfimages {download_directory}/rel_{pdf_index}_condutores.pdf {images_output_dir}/pdf_{pdf_index} -all")
  
  print("\n\nScraped!! Starting Filtering!")
  
  for file_name in listdir(images_output_dir):
    img = Image.open(f"{images_output_dir}/{file_name}")

    img_hash = dhash(img)

    if img.size == (345, 62) or str(img_hash) == "0000000000000000" or str(img_hash) == "0000404040400000" or str(img_hash) in scraped_images:
      remove(f"{images_output_dir}/{file_name}")
      continue

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
        print(f"Resolution not founded in {images_output_dir}/{str(img_hash)}{file_name[file_name.rfind('.'):]} - {img.size}")
    
    img_hash = dhash(img)
    
    rename(f"{images_output_dir}/{file_name}", f"{images_output_dir}/{str(img_hash)}{file_name[file_name.rfind('.'):]}")
    scraped_images.append(str(img_hash))

  return scraped_images
