# IMTT Traffic Code Questions 🚗

🇬🇧 This repository contains the JSON of all __IMTT__ Traffic Code Questions.

🇵🇹 Este repositório contém um JSON de todas as questões de código do __IMTT__.

###### `Instituto da Mobilidade e dos Transportes` (`Institute of Mobility and Transport`) is the Portuguese institute that regulates public roads and their laws. These are the traffic code questions created and published by them.

---

## Questions

All the __IMTT__ Traffic Code Questions are stored inside the `questions.json` with the following structure:

```javascript
[
	{
		"questionNumber": integer, // IMTT Question Number
		"category": string[], // "A", "AM", "B", "C" or/and "D"
		"text": string, //the question text
		"options": [
			{
				"index": integer, // 0, 1, 2 or 3
				"letter": string, // A, B, C or D
				"text": string,
				"correct": boolean
			}
		],
		"correctOptionIndex": // 0, 1, 2 or 3
	}
]
```

---

## Scripts ⚙️

### webScraper

Python Script used to scrap all questions from the site `www.bomcondutor.pt`.

#### Requirements

1. selenium - `pip install selenium`
2. geckodriver - on Arch `yay -S geckodriver`

#### Running 🚀

```console
$ ./scripts/webScraper.py
$ ./scripts/webScraper.py {?finalQuestionNum}
$ ./scripts/webScraper.py {?initialQuestionNum} {?finalQuestionNum}
$ ./scripts/webScraper.py {?initialQuestionNum} {?finalQuestionNum} {?baseUrl}

$ ./scripts/webScraper.py 5 50 "http://www.bomcondutor.pt/questao/"
```

1. __initialQuestionNum__ - optional - number of the first IMTT Question to scrape -> default "1"

2. __finalQuestionNum__ - optional - number of the last (inclusive) IMTT Question to scrape -> default "5444"

3. __baseUrl__ - optional -  base url for the scrape - need be a `bomcondutor.pt` page - used for offline version of the site -> default "http://www.bomcondutor.pt/questao/"

---

## License 📝

<img alt="License" src="https://img.shields.io/badge/license-MIT-%2304D361">

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Thanks 🙏

All this questions were scraped from [`www.bomcondutor.pt`](https://www.bomcondutor.pt). They do a awesome job on this area and everyone who wants to learn should visit them.

All IMTT question are [public](https://www.imt-ip.pt/sites/IMTT/Portugues/Condutores/PerguntasExames/Paginas/PerguntasExamesAtualizacao.aspx) and published by the institute itself.

---