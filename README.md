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
		"questionNumber": integer,
		"category": string[], // "A", "AM", "B", "C" or/and "D"
		"theme": string,
		"text": string,
		"imageHash": string, // difference hash of `www.bomcondutor.pt` questions images
		"options": [
			{
				"text": string,
				"correct": boolean
			}
		],
		"correctOptionIndex": integer // 0, 1, 2 or 3
	}
```

## Images 🖼️

If you want use the images questions along questions, you can use the `imageHash` on `questions.json`. This hash is also the name of the correct image file in the `questionsImages.zip` available at [Releases Page](https://github.com/Darguima/IMTT-Traffic-Code-Questions/releases/tag/v1.0.0).

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
$ scripts/webScraper.py -i 1 -f 5444 -u http://www.bomcondutor.pt/questao/ -t 2
$ scripts/webScraper.py --initialQuestion 1 --finalQuestion 5444 --baseUrl http://www.bomcondutor.pt/questao/ --tabSize 2
```

| Short Argument | Long Argument     | Default                           | Description                                                                                          |
|----------------|-------------------|-----------------------------------|------------------------------------------------------------------------------------------------------|
|-h              | --help            |                                   | Show help menu                                                                                       |
|-i              | --initialQuestion | 1                                 | Receive the first question to scrap                                                                  |
|-f              | --finalQuestion   | 5444                              | Receive the last (included) question to scrap                                                        |
|-u              | --baseUrl         |https://www.bomcondutor.pt/questao/| Receive the base url to use on scrap. Need starts with a valid protocol (http://, https://, file://) |
|-c              | --inputFile       |                                   | Receive the input file to continue the JSON                                                          |
|-o              | --outputFile      | ./questions.json                  | Receive the output file to store the JSON                                                            |
|-t              | --tabSize         | None                              | Receive the number of spaces on the tab of indentation                                               |
|-p              | --preQuestion     | ""                                | Receive the string to use before question number on the URL. Ex.: ".html"                            |
|-a              | --afterQuestion   | ""                                | Receive the string to use after question number on the URL                                           |

---

### verifyJson ✔️

Python Script used to verify if the JSON file is with correct syntax.

#### Requirements

1. Pillow - `pip install Pillow`
2. ImageHash - `pip install ImageHash`

#### Running 🚀

```console
$ scripts/imageFilter.py
$ scripts/imageFilter.py -h
$ scripts/imageFilter.py -i images -o questionsImages -f imageHashes.json
```

| Short Argument | Long Argument     | Default                          | Description                                                      |
|----------------|-------------------|----------------------------------|------------------------------------------------------------------|
|-h              | --help            |                                  | Show help menu                                                   |
|-i              | --inputDirectory  | (Required)                       | Receive the input directory with images files                    |
|-o              | --outputDirectory | (Required)                       | Receive the directory to store images files with hashes names    |
|-f              | --outputFile      | ./images.json                    | Receive the output file to store the JSON                        |

NOTE: All files in inputDirectory need be named like "{questionNumber}.jpg" or "{questionNumber}.png".

---

### imageFilter 🖼️

Python Script used to rename questions images to their dhash (difference hash) by deleting repeated images.
To access them you can use the `imageHash` in `questions.json`.

#### Requirements

#### Running 🚀

```console
$ scripts/verifyJson.py
$ scripts/verifyJson.py -h
$ scripts/verifyJson.py -j questions.json -i 1 -f 5444 -d imagesQuestions
$ scripts/verifyJson.py --jsonFile questions.json --initialQuestion 1 --finalQuestion 5444 --imagesDir imagesQuestions
```

| Short Argument | Long Argument     | Default                          | Description                                                      |
|----------------|-------------------|----------------------------------|------------------------------------------------------------------|
|-h              | --help            |                                  | Show help menu                                                   |
|-j              | --jsonFile        | questions.json                   | Receive the input file to verify the JSON                        |
|-i              | --initialQuestion | 1                                | Receive the first question that need be on file                  |
|-f              | --finalQuestion   | 5444                             | Receive the last (included) question that need be on file        |
|-d              | --imagesDir       | None                             | Receive the questions images directory to verify the images hash |

###### NOTE: All files in inputDirectory need be named like `{questionNumber}.jpg` or `{questionNumber}.png`.

---

## License 📝

<img alt="License" src="https://img.shields.io/badge/license-MIT-%2304D361">

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Thanks 🙏

All this questions were scraped from [`www.bomcondutor.pt`](https://www.bomcondutor.pt). They do a awesome job on this area and everyone who wants to learn should visit them.

All IMTT question are [public](https://www.imt-ip.pt/sites/IMTT/Portugues/Condutores/PerguntasExames/Paginas/PerguntasExamesAtualizacao.aspx) and published by the institute itself.

---
