# Exam Questionnaire Scanner

## Dependencies
The following packages are required for converting the scanned pdf files to images and for parsing the FormScanner output csv file: 
- [FormScanner](http://www.formscanner.org/) is a free and open source OMR (optical mark recognition) software for scanning and grading user-filled, multiple choice forms.
- [ImageMagick](https://www.imagemagick.org/script/index.php) is a free open source application that can create, edit, compose, or convert bitmap images.
- [Python 3](https://www.python.org/) (or later)
- Python modules via ```pip install -r requirements.txt```

## How to
### Scan the exam papers
- The first and only manual step of the grading process is the scanning of the exam papers. The goal is to feed the FormScanner with an image file of each exam sheet. 
Unfortunately, our equipment does not offer the functionality of saving scanned documents to image format and thus, we are forced to create a **pdf** file for each scanned set of exam sheets. 
To automatically scan a bundle of exam, place the exam sheets on the top tray of the scanner, as it is illustrated in the following picture. 
![Scanning_setup](media/scanning_setup.jpg)
- Retrieve the PDF files (one for each scanned bundle of exam sheets).

### Execute the automated grading set of tools
- Place the **pdf** files in the ```scanned_files``` directory.
- Place the **student_info.xlsx** file that contains the information for each student that participates in this year's course, in the ```grades_csv``` directory. This **student_info.xlsx** file is provided by the course organizer. 
- Fire up the python script that performs the rest of the steps with the following command:
```
python examQuestionnaireScanner.py
``` 
The aforementioned command will read/write all the necessary files from/to the default directories defined in the application. All paths are customizable. 

See the help for defining custom paths: ```python examQuestionnaireScanner.py -h```

## Reading the results
The succesfull completion of the grading process will fill-in the appropriate **student_info.xlsx** tab with the follwoing information:
- Student id
- Exam sheet id
- a sequence of 10 multiple question responces (in form of A,B,C and D)

## Resolving the errors
Cases that failed to parse (due to *parity check error* or *invalid student id*) will be logged in a file and also presented at the console at the end of the execution. 

The log will mention the *image's file name* in order to manually inspect and resolve the error. Corrections can be applied directly on the **student_info.xlsx** document.  
