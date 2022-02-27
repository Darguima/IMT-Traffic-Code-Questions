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
$ scripts/webScraper.py
$ scripts/webScraper.py -h
$ scripts/webScraper.py -i 1 -f 5444 -u http://www.bomcondutor.pt/questao/
$ scripts/webScraper.py --initialQuestion 1 --finalQuestion 5444 --baseUrl http://www.bomcondutor.pt/questao/
```

| Short Argument | Long Argument     | Default                          | Description                                                                                                      |
|----------------|-------------------|----------------------------------|------------------------------------------------------------------------------------------------------------------|
|-h              | --help            |                                  | Show help menu                                                                                                   |
|-i              | --initialQuestion | 1                                | Receive the first question to scrap                                                                              |
|-f              | --finalQuestion   | 5444                             | Receive the last (included) question to scrap                                                                    |
|-u              | --baseUrl         |http://www.bomcondutor.pt/questao/| Receive the base url to use on scrap. Need be a copy of `bomcondutor.pt`. Can be used offline copies of the site |

---

## License 📝

<img alt="License" src="https://img.shields.io/badge/license-MIT-%2304D361">

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Thanks 🙏

All this questions were scraped from [`www.bomcondutor.pt`](https://www.bomcondutor.pt). They do a awesome job on this area and everyone who wants to learn should visit them.

All IMTT question are [public](https://www.imt-ip.pt/sites/IMTT/Portugues/Condutores/PerguntasExames/Paginas/PerguntasExamesAtualizacao.aspx) and published by the institute itself.

---