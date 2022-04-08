from json import dump


def store_json (questions, output_file, tab_size=None):
	debug_file = output_file[:output_file.rfind(".")] + "_debug" + output_file[output_file.rfind("."):]

	print("\n\n========================================================")
	print("===================== Storing JSON =====================")
	print("========================================================")

	print(f"\nStoring questions dictionary in \"{output_file}\".")
	print(f"Storing questions (debug) dictionary in \"{debug_file}\".\n")

	with open(debug_file, 'w') as outfile:
		dump(questions, outfile, indent=tab_size)

	print("Cleaning questions to output!")

	for category in questions:
		for question in questions[category]:
			question.pop("imageId")
			question.pop("error")

	with open(output_file, 'w') as outfile:
		dump(questions, outfile, indent=tab_size)

	
