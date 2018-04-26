# Exam Questionnaire Scanner

## Dependencies
The following packages are required for converting the scanned pdf files to images and for parsing the FormScanner output csv file: 
- [FormScanner](http://www.formscanner.org/) is a free and open source OMR (optical mark recognition) software for scanning and grading user-filled, multiple choice forms.
- [ImageMagick](https://www.imagemagick.org/script/index.php) is a free open source application that can create, edit, compose, or convert bitmap images.
- [Python 3](https://www.python.org/) (or later)


## Process
The while process consists from 5 basic steps:

	* Scan the exams using a physical scanner (manual step)
	* Covert the exported PDF files (from the above step) to PNG using the ImageMagick 
	* Pipe the PNG images to the Java-based FormScanner to retrieve a CSV file with all exams student IDs, paper IDs, and Answers
	* Parse the CSV files (translates binary and charatcter to the appropriate decimals) using the Python CSVparser.py script
	* Megre newly exported CSV file with the Excel sheet
