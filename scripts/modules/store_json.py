from json import dump


def store_json (questions, output_file, tab_size=None):
	print("\n\n========================================================")
	print("===================== Storing JSON =====================")
	print("========================================================")

	print(f"\nStoring questions dictionary in \"{output_file}\".\n")

	with open(output_file, 'w') as outfile:
		dump(questions, outfile, indent=tab_size)
