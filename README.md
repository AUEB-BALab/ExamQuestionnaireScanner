# Exam Questionnaire Scanner

## Dependencies
The following packages are required for converting the scanned pdf files to images and for parsing the FormScanner output csv file: 
- [FormScanner](http://www.formscanner.org/) is a free and open source OMR (optical mark recognition) software for scanning and grading user-filled, multiple choice forms.
- [ImageMagick](https://www.imagemagick.org/script/index.php) is a free open source application that can create, edit, compose, or convert bitmap images.
- [Python 3](https://www.python.org/) (or later)

## How to
### Scan the exam papers
- //TODO
### Convert the scanned PDF to seperate image files
- //TODO
```
convert input.pdf -threshold 90% questionnaire.png
```
### Parse with FormScanner
- Load the FormScanner template //TODO add more details
- Load the image files in FormScanner
- Parse the image files
- Save the output csv file

### Parse the csv file
 - //TODO
