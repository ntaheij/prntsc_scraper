# prnt.sc Scraper

## The program
The program will scrape images from the [LightShot or prnt.sc](https://prnt.sc/) site. You can use these images as a dataset.

## Pre-requisites

To automatically install any dependencies, use the following command:

```
$ pip install -r requirements.txt
```

This script was tested on the following python modules, however earlier/later versions may work fine:

```
- python 3.9
- requests 2.26.0
- beautifulsoup4 4.9.3
- lxml 4.6.3
```

## Using the Script

The script takes 3 arguments as follows:

* ```--startcode```: 6 character string made up of lowercase letters and numbers which is where the scraper will start.
  * e.g. ```ae4dde```
  * default: ```lj9me9```
* ```--timeout```: The time-out between requests.
  * e.g. ```3```
  * default: ```5```
* ```--count```: The number of images to scrape.
  * e.g. ```50```
  * default: ```30```
* ```--output_path```: The path where images will be stored.
  * e.g. ```output/```
  * default: ```output/```

En example command you can try:
```
$ python3 scraper.py --start_code 33eeae --timeout 3 --count 30
```

# Licensing
 
This project is released under the MIT license, see LICENSE.md for more details.