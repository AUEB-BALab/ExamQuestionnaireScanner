import subprocess
import os 
import shutil
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-p", "--scanned_pdf_directory", 
    help="The directory path that contains the scanned pdf files. The default will be used if not set by the user.")
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
parser.add_argument("-d", "--delete_temp_files", action='store_true',
    help="Delete the image files and the intermidiate csv files after the execution.")


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


def execute_CsvParser(inputCSV_path, outputCSV_path):
    print('''## Parsing FormScanner csv ##
        - CSV location :: {}
        - Output CSV location :: {}'''
        .format(inputCSV_path, outputCSV_path), flush=True)
    subprocess.call(["python", "CSVparser.py", (inputCSV_path + ".csv"), "--output_file",outputCSV_path])
    print("- Finished.\n", flush=True)


def delete_temp_files(imagesDirectory_path, formscanner_csv):
    print("## Deleting temp files ##", flush=True)
    print("\tDeleting images in :: {}".format(imagesDirectory_path), flush=True)
    # delete images
    for image_file in os.listdir(imagesDirectory_path):
        if image_file.endswith(".png"):
            image_file_path = os.path.join(imagesDirectory_path, image_file)
            try:
                if os.path.isfile(image_file_path):
                    os.unlink(image_file_path)
            except Exception as e:
                print(e)

    # delete csv
    print("\tDeleting form scanner csv :: {}".format(formscanner_csv), flush=True)
    os.remove((formscanner_csv + ".csv"))
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


execute_PdfToPngConverter(scanned_pdf_directory_path, scanned_images_directory_path)
execute_FormScanner(formScannerJar_path, form_scanner_template_xml_path, scanned_images_directory_path, output_form_scanner_csv_path)
execute_CsvParser(output_form_scanner_csv_path,output_csv_file_path)
if args.delete_temp_files:
    delete_temp_files(scanned_images_directory_path, output_form_scanner_csv_path)




