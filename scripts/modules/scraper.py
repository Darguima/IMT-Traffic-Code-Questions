from requests import get
from os.path import exists

def scrape_question (category, questionNumber, baseUrl):
	if (exists(baseUrl)):
		try:
			response = open(f'{baseUrl}/{category}/{questionNumber}', 'rb').read().decode("utf-8")
		except FileNotFoundError:
			return "responseCode"

	else:
		response = get(f"{baseUrl}/{category}/{questionNumber}", allow_redirects=False)

		if (response.status_code != 200):
			return "responseCode"
		
		response = response.text

	htmlLines = response.replace("\t", "").replace("\r", "").replace("\ufeff", "").split("\n")
	
	jsVars = list(filter(lambda line: line.startswith("var js_"), htmlLines))
	jsVars = [var.removeprefix("var ").removesuffix(";") for var in jsVars]

	if len(jsVars) < 6 or \
		not jsVars[0].startswith("js_linesimgs") or \
		not jsVars[1].startswith("js_linesPerguntas") or \
		not jsVars[2].startswith("js_linesResposta1") or \
		not jsVars[3].startswith("js_linesResposta2") or \
		not jsVars[4].startswith("js_linesResposta3") or \
		not jsVars[5].startswith("js_linesCerta"):
		
		return f"ERROR {category}/{questionNumber} - JavaScript Variables are wrong. Maybe an update of the site. Open an Issue and wait for updates."

	question = {
		"questionNumber": questionNumber,

		"category": category,

		"imageId": jsVars[0][jsVars[0].find('= ') + 2 : ],

		"questionText": jsVars[1][ jsVars[1].find("\"") + 1 : jsVars[1].rfind("\"") ],
		
		"options": [
			jsVars[2][ jsVars[2].find("\"") + 1 : jsVars[2].rfind("\"") ],
			jsVars[3][ jsVars[3].find("\"") + 1 : jsVars[3].rfind("\"") ],
		],

		"correctOptionIndex": int( jsVars[5][ jsVars[5].find("\"") + 1 : jsVars[5].rfind("\"") ] ) - 1
	}

	if (jsVars[4][ jsVars[4].find("\"") + 1 : jsVars[4].rfind("\"") ] != ""):
		question["options"].append(jsVars[4][ jsVars[4].find("\"") + 1 : jsVars[4].rfind("\"") ])

	return question
