from os import remove
from os.path import exists

from requests import get
from io import BytesIO
from PIL import Image, ImageDraw

from imagehash import dhash, hex_to_hash


def images_filter (questions, scraped_images, base_url, images_output_dir):
	print("\n========================================================")
	print("====================  Images Filter ====================")
	print("========================================================")

	print(f"\nFiltering images scraped from PDFs with \"{base_url}\".")

	scraped_images = list(map(lambda hash: hex_to_hash(hash), scraped_images))

	images_hashes = {"A": {}, "B": {}, "C": {}, "D": {}}
	necessary_images = []
	big_difference_hash_images = []

	for category in questions:
		for question in questions[category]:
			images_hashes[category][question["imageId"]] = {"hash": "", "error": 100}
	

	print("\n\nImages to Filter:")
	print(f"\tCategory A - {len(images_hashes['A']):0>4}")
	print(f"\tCategory B - {len(images_hashes['B']):0>4}")
	print(f"\tCategory C - {len(images_hashes['C']):0>4}")
	print(f"\tCategory D - {len(images_hashes['D']):0>4}")

	print("\n\nComparing Hashes:", end="\r")
	for category in images_hashes:
		print(f"\n\n\tStarting category \"{category}\":")

		for image_number, image_id in enumerate(images_hashes[category]):
			print(f"\t\tImage num: {image_number:0>4}", end="\r")
			if (exists(base_url)):
				img = Image.open(f'{base_url}/imgs{category}/{image_id}.jpg')
			
			else:
				response = get(f'{base_url.replace("questao", "bd")}/imgs{category}/{image_id}.jpg')
				img = Image.open(BytesIO(response.content))

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
						print(f"Resolution not founded in {question['imageId']} - {img.size}")
			
			online_image_hash = dhash(img)

			lower_dif_hash = 100
			for scraped_img_hash in scraped_images:
				if online_image_hash - scraped_img_hash < lower_dif_hash:
					lower_dif_hash = online_image_hash - scraped_img_hash
					images_hashes[category][image_id] = {"hash": str(scraped_img_hash), "error": lower_dif_hash}

			if lower_dif_hash > 7:
				img.save(f"{images_output_dir}/{str(online_image_hash)}.jpg", "JPEG")
				images_hashes[category][image_id] = {"hash": str(online_image_hash), "error": -1}
				big_difference_hash_images.append(str(online_image_hash))
	
	print(f"\n\nThis images diverges more than 7 bytes, so we are storing the online image with a black watermark: ({len(big_difference_hash_images)} images)")
	print(", ".join(big_difference_hash_images))
			
	for category in questions:
		for question in questions[category]:
			question["imageHash"] = images_hashes[category][question["imageId"]]["hash"]
			question["error"] = images_hashes[category][question["imageId"]]["error"]

			if question["imageHash"] not in necessary_images:
				necessary_images.append(question["imageHash"])
	
	print("\nCleaning unnecessary images!")

	for image_hash in scraped_images:
		if str(image_hash) not in necessary_images:
			remove(f"{images_output_dir}/{str(image_hash)}.jpg")
	
	return questions
	