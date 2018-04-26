# Exam Questionnaire Scanner

## Dependencies
The following packages are required for converting the scanned pdf files to images and for parsing the FormScanner output csv file: 
- [FormScanner](http://www.formscanner.org/) is a free and open source OMR (optical mark recognition) software for scanning and grading user-filled, multiple choice forms.
- [ImageMagick](https://www.imagemagick.org/script/index.php) is a free open source application that can create, edit, compose, or convert bitmap images.
- [Python 3](https://www.python.org/) (or later)
- Python modules via ```pip install -r requirements.txt```

## How to
### Scan the exam papers
The first and only manual step of the grading process is the scanning of the exam papers. The goal is to feed the FormScanner with an image file of each exam sheet. 
Unfortunately, our equipment does not offer the functionality of saving scanned documents to image format and thus, we are forced to create a **pdf** file for each scanned set of exam sheets. 
To automatically scan a bundle of exam, place the exam sheets on the top tray of the scanner, as it is illustrated in the following picture. 
![Scanning_setup](media/scanning_setup.jpg)

### Convert the scanned PDF to seperate image files
- //TODO

### Parse with FormScanner
- Load the FormScanner template //TODO add more details
- Load the image files in FormScanner
- Parse the image files
- Save the output csv file

### Parse the csv file
- CSV file path is required as a command line argument

## Process
The while process consists from 5 basic steps:

* Scan the exams using a physical scanner (manual step)
* Covert the exported PDF files (from the above step) to PNG using the ImageMagick 
* Pipe the PNG images to the Java-based FormScanner to retrieve a CSV file with all exams student IDs, paper IDs, and Answers
* Parse the CSV files (translates binary and charatcter to the appropriate decimals) using the Python CSVparser.py script
* Megre newly exported CSV file with the Excel sheet
