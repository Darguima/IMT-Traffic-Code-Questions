from os import remove
from os.path import exists

from requests import get
from io import BytesIO
from PIL import Image

from imagehash import dhash, hex_to_hash


def images_filter (questions, scraped_images, base_url, images_output_dir):
	print("\n========================================================")
	print("====================  Images Filter ====================")
	print("========================================================")

	print(f"\nFiltering images scraped from PDFs with \"{base_url}\".")

	scraped_images = list(map(lambda hash: hex_to_hash(hash), scraped_images))

	images_hashes = {"A": {}, "B": {}, "C": {}, "D": {}}
	necessary_images = []

	for category in questions:
		for question in questions[category]:
			images_hashes[category][question["imageId"]] = {"hash": "", "error": 100}
	

	print("\n\nImages to Filter:")
	print(f"\tCategory A - {len(images_hashes['A']):0>4}")
	print(f"\tCategory B - {len(images_hashes['B']):0>4}")
	print(f"\tCategory C - {len(images_hashes['C']):0>4}")
	print(f"\tCategory D - {len(images_hashes['D']):0>4}")

	print("\n\nComparing Hashes:")
	for category in images_hashes:
		print(f"\tStarting category \"{category}\".")

		for image_id in images_hashes[category]:
			if (exists(base_url)):
				img = Image.open(f'{base_url}/imgs{category}/{image_id}.jpg')
			
			else:
				response = get(f'{base_url.replace("questao", "bd")}/imgs{category}/{image_id}.jpg')
				img = Image.open(BytesIO(response.content))
			
			online_image_hash = dhash(img)

			lower = 100
			for scraped_img_hash in scraped_images:
				if online_image_hash - scraped_img_hash < lower:
					lower = online_image_hash - scraped_img_hash
					images_hashes[category][image_id] = {"hash": str(scraped_img_hash), "error": lower}
			
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
		