# IMT Traffic Code Questions 🚗

🇬🇧 This repository contains the JSON of all __IMT__ Traffic Code Questions.

🇵🇹 Este repositório contém um JSON de todas as questões de código do __IMT__.

###### `Instituto da Mobilidade e dos Transportes` (`Institute of Mobility and Transport`) is the Portuguese institute that regulates public roads and their laws. These are the traffic code questions created and published by them.

---

## Questions

All the __IMT__ Traffic Code Questions are stored inside the `questions.json`, organized by categories:

```javascript
{
	"A": question[],
	"B": question[],
	"C": question[],
	"D": question[]
}
```

Question Structure:
```
{
	"questionNumber": integer,
	"category": string, // "A", "B", "C" or "D"
	"questionText": string,
	"options": string[],
	"correctOptionIndex": integer, // 0, 1 or 2
	"imageHash": string, // name of the image file; ex.: `22808ee4a531585a.jpg`
}
```

## Images 🖼️

If you want use the images questions along questions, you can use the `imageHash` on `questions.json`. This hash is also the name of the correct image file in the `questionsImages.zip` available at [Releases Page](https://github.com/Darguima/IMT-Traffic-Code-Questions/releases/tag/v2.0.0).

Most of the images were scraped from the official IMT PDFs, using as reference the images from [`www.testes-codigo.pt`](https://testes-codigo.pt/). But sometimes the image was too low resolution and it was impossible for the Python Script to recognize the correct image, so in these cases we scraped the image again from [`www.testes-codigo.pt`](https://testes-codigo.pt/) and used a black watermark.

---

## Scripts ⚙️

All the questions were scraped using a Python Script.

#### Steps:

1. Download the questions html files. (Optional, for development purposes)

2. Scrape questions from the html files (offline or online).

3. Download the questions images files. (Optional, for development purposes)

4. Download the questions PDFs files. (Optional, for development purposes)

5. Scrape images from the PDF files (offline or online).

6. Compare the images difference hashes from PDF and reference website.

7. Store the questions object in a JSON file.

#### Requirements

1. Pillow - `pip install Pillow`
2. PyMuPDF - `pip install pymupdf`
3. ImageHash - `pip install ImageHash`

#### Some Configurations

The script can have some configuration, for that open `scripts/index.py` and change the variables:

```python
download_mode = True  # Set to True if you want the script downloads and use downloaded questions/images/PDFs files (development purposes)

download_directory = "./questionsOffline" # Were all the downloaded files are stored

download_again = False # Set to True if you want that the script ignore already downloaded files and download them again

output_file = "./questions.json" # The JSON file were questions are stored

images_output_dir = "./questionsImages" # Where the questions images files are stored

```

#### Running 🚀

```console
$ scripts/index.py
```


---

## License 📝

<img alt="License" src="https://img.shields.io/badge/license-MIT-%2304D361">

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Thanks 🙏

All this questions were scraped from [`www.testes-codigo.pt`](https://testes-codigo.pt/). They do a awesome job on this area and everyone who wants to learn should visit them.

All IMT question are [public](https://www.imt-ip.pt/sites/IMTT/Portugues/Condutores/PerguntasExames/Paginas/PerguntasExamesAtualizacao.aspx) and published by the institute itself.

---
