import subprocess
import os 
import shutil
import argparse
from colorama import Fore, Back, Style 

parser = argparse.ArgumentParser()

parser.add_argument("-p", "--scanned_pdf_directory", 
    help="The directory path that contains the scanned pdf files. The default will be used if not set by the user.")
parser.add_argument("-sc", "--skip_pdf_conversion", action='store_true',
    help="A flag for skipping the pdf-to-images conversion")
parser.add_argument("-i", "--scanned_images_directory",
    help="The path for the directory that hosts the converted images. The default will be used if not set by the user.")
parser.add_argument("-f", "--form_scanner_path", 
    help="The file path of the formscanner-main-XXX.jar executable. The default will be used if not set by the user.")
parser.add_argument("-t", "--form_scanner_template_xml",
    help="The path for the FormScanner template xml file. The default will be used if not set by the user.")
parser.add_argument("-o", "--output_form_scanner_csv",
    help="The path for the csv file produced by FormScanner. The default will be used if not set by the user.")
parser.add_argument("-c", "--output_csv_file",
    help="The parsed csv file. The default will be used if not set by the user.")
parser.add_argument("-e", "--exams_sheet",
    help="The path for the exam's excel document. The default will be used if not set by the user.")
parser.add_argument("-ad", "--auto_deploy", action='store_true',
    help="A flag for auto-deploying a new sheet inside the above-mentioned excel document with exam's information")
args = parser.parse_args()


def execute_FormScanner(formScanner_path, template_path, imagesDirectory_path, outputCSV_path):
    print('''## Scanning images with FormScanner ##
        - Using template :: {}'''
        .format(template_path), flush=True)
    subprocess.call(['java', '-jar', formScanner_path, template_path, imagesDirectory_path, outputCSV_path])
    print("- Finished.\n", flush=True)


def execute_PdfToPngConverter(pdfDirecoty_path, outputImagesDir_path):
    print('''## Converting scanned pdf to images ##
        - PDF directory :: {}
        - Output images directory :: {}'''
        .format(pdfDirecoty_path, outputImagesDir_path), flush=True)    

    pdf_file_list = os.listdir(pdfDirecoty_path)
    for pdf in pdf_file_list:
        if pdf.endswith(".pdf"):
            pdf_file_path = os.path.join(pdfDirecoty_path, pdf)
            scanned_image_path = os.path.join(outputImagesDir_path, pdf)
            print("\t- Converting pdf :: {}".format(pdf_file_path), flush=True)
            subprocess.call(['convert', pdf_file_path, "-threshold", "90%", (scanned_image_path+"_converted.png")])
        else:
            # print("--- skipping :: {}".format(pdf))
            pass
    print("- Finished.\n", flush=True)


def execute_CsvParser(inputCSV_path, course_info, outputCSV_path, autoDeploy_flag):
    print('''## Parsing FormScanner csv ##
        - CSV location :: {}
        - Course info xsls :: {}
        - Output CSV location :: {}'''
        .format(inputCSV_path, course_info, outputCSV_path), flush=True)
    subprocess.call(["python", 
                    "CSVparser.py", 
                    (inputCSV_path + ".csv"), 
                    "--output_file",
                    outputCSV_path,
                    autoDeploy_flag, 
                    "--exams_sheet",
                    course_info]
                    )
    print("- Finished.\n", flush=True)


# initialize path variables
if args.scanned_pdf_directory:
    scanned_pdf_directory_path = args.scanned_pdf_directory
else: 
    scanned_pdf_directory_path = "scanned_files"

# set the scanned_images_directory path
if args.scanned_images_directory:
    scanned_images_directory_path = args.scanned_images_directory
else:
    scanned_images_directory_path = "questionnaire_images"

# set the output formScannerCSV path
if args.output_form_scanner_csv:
    output_form_scanner_csv_path = args.output_form_scanner_csv
else:
    output_form_scanner_csv_path = os.path.join("formscanner_csv","formScannerCSV")

# set the FormScanner executable file path
if args.form_scanner_path:
    formScannerJar_path = args.form_scanner_path
else:
    formScannerJar_path = os.path.join("lib","formscanner-main-1.1.3.jar")

# set the FromScanner xml template file path
if args.form_scanner_template_xml:
    form_scanner_template_xml_path = args.form_scanner_template_xml
else:
    form_scanner_template_xml_path = os.path.join("templates", "default_template.xtmpl")

# set the parsed output csv file path
if args.output_csv_file:
    output_csv_file_path = args.output_csv_file
else:
    output_csv_file_path = os.path.join("scan_to_csv", "parsed_results.csv")

# set the exam sheets file path
if args.exams_sheet:
    exams_sheet_path = args.exams_sheet
else:
    exams_sheet_path = os.path.join("course_info", "course_info.xlsx")

if args.auto_deploy:
    autoDeploy_flag = "-ad"
else:
    autoDeploy_flag = ""

if args.skip_pdf_conversion:
    print("Skipping pdf conversion.", flush=True)
else:
    execute_PdfToPngConverter(scanned_pdf_directory_path, scanned_images_directory_path)

execute_FormScanner(formScannerJar_path, form_scanner_template_xml_path, scanned_images_directory_path, output_form_scanner_csv_path)
execute_CsvParser(output_form_scanner_csv_path,exams_sheet_path,output_csv_file_path,autoDeploy_flag)