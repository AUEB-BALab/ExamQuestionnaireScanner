import argparse
import logging
import os
from pathlib import Path
import subprocess
import sys

import CSVparser


def execute_FormScanner(formScanner_executable, formScanner_template, images_dir, output_csv):
    """
    Executes the FormScanner for scanning the images and producing the output CSV.

    Args:
        formScanner_executable (string): The FormScanner's .jar executable path
        formScanner_template (string): The FormScanner's .xtmpl template path
        images_dir (string): The converted images' directory path
        output_csv (string): The FormScanner's csv output path

    Raises:
        subprocessfileedProcessError: Upon FormScanner execution failure
    """

    logging.info('''Scanning images with FormScanner ...
        - FormScanner template: {}'''
        .format(formScanner_template))

    formScanner_cmd = ['java',
                            '-jar',
                            formScanner_executable,
                            formScanner_template,
                            images_dir,
                            output_csv]
    logging.debug("Prepared FormScanner command :: {}".format(' '.join(formScanner_cmd)))
    try:
        subprocess.run(formScanner_cmd, check=True)
    except Exception:
        logging.error("FormScanner execution failed.")
        raise


def execute_PdfToPngConverter(pdf_dir, output_images_dir, threshold=90):
    """
    Convert a set of PDF to images. The task is performed by ImageMagick tool.
    Check http://www.imagemagick.org/ for more details.

    Args:
        pdf_dir (string): The directory that contains the PDF files
        output_images_dir (string): The directory that will store the converted images

    Raises:
        subprocessfileedProcessError: Upon conversion failure
    """
    # TODO: Add threshold level cli argument
    logging.info('''Converting scanned PDF to images ...
        - PDF directory: {}
        - Output images directory: {}
        - Black and white threshold: {}'''
        .format(pdf_dir, os.path.abspath(output_images_dir), threshold))

    pdf_file_list = os.listdir(pdf_dir)
    for pdf in pdf_file_list:
        # Skip non-pdf files
        if Path(pdf).suffix != ".pdf":
            logging.debug("File {} is not a PDF and will not be converted.".format(pdf))
            continue

        pdf_file = os.path.join(pdf_dir, pdf)
        scanned_image = os.path.join(output_images_dir, pdf)
        logging.info("Converting pdf: {} ...".format(pdf_file))
        convert_cmd = ['convert',
                            pdf_file,
                            "-threshold", "{}%".format(threshold),
                            (scanned_image + "_converted.png")]
        # add black and white support
        # convert_cmd = ['convert',
        #                     "-density","100",
        #                     pdf_file,
        #                     "-resize", "594x841",
        #                     (scanned_image + "_converted.png")]
        logging.debug("Prepared convert command :: {}".format(' '.join(convert_cmd)))
        try:
            subprocess.run(convert_cmd, check=True)
        except Exception:
            logging.error("PDF conversion process failed.")
            raise


# calls the CSVparser functions to perform the parsing and
# write the final output csv file
def execute_CsvParser(inputCSV_path, students_csv, outputCSV_path):
    CSVparser.parse_arguments(inputCSV_path, students_csv, outputCSV_path)
    CSVparser.parse_FormScanner_csv(inputCSV_path, students_csv, outputCSV_path)


def read_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument("scanned_pdf_dir",
        help="The directory path that contains the pdf files generated by scanning the exam sheets.")
    parser.add_argument("formScanner_template",
        help="The FormScanner's template XTMPL file path.")
    parser.add_argument("students_info",
        help="The file path of the csv file that contains the student ids.")
    parser.add_argument("-f", "--output_form_scanner_csv",
        help="The path for the csv file produced by FormScanner. The default will be used if not set by the user.")
    parser.add_argument("-s", "--skip_pdf_conversion", action='store_true',
        help="A flag for skipping the pdf-to-images conversion")
    parser.add_argument("-j", "--form_scanner_path",
        help="The file path of the formscanner-main-XXX.jar executable. The default will be used if not set by the user.")
    parser.add_argument("-o", "--final_grades_output_csv",
        help="The parsed csv file. The default will be used if not set by the user.")
    args = parser.parse_args()

    return args


def parse_arguments(scanned_pdf_dir, output_form_scanner_csv,
    form_scanner_path, formScanner_template_xml, final_grades_output_csv_filepath,
    students_info, skip_pdf_conversion):

    # initialize path variables
    if scanned_pdf_dir:
        if not os.path.isdir(scanned_pdf_dir):
            logging.error("Scanned PDF directory does not exist in path: {}".format(scanned_pdf_dir))
            raise FileNotFoundError("Invalid scanned PDF directory")
        else:
            scanned_pdf_dir_path = scanned_pdf_dir
        logging.debug("Scanned PDF directory: {}".format(scanned_pdf_dir_path))
    else:
        logging.warning("Scanned PDF directory is not set.")

    scanned_images_dir = "tmp" # set the default path
    logging.debug("Scanned images directory :: {}".format(scanned_images_dir))

    # set the output formScannerCSV path
    if output_form_scanner_csv:
        formScanner_output_csv = output_form_scanner_csv
    else:
        formScanner_output_csv = os.path.join("tmp","formScannerCSV.csv")
    logging.debug("Output FormScanner csv :: {}".format(formScanner_output_csv))

    # set the FormScanner executable file path
    if form_scanner_path:
        if not os.path.isfile(form_scanner_path):
            logging.error("FormScanner executable does not exist in path :: {}".format(form_scanner_path))
            raise FileNotFoundError("Invalid FormScanner executable path")
        else:
            formScanner_executable = form_scanner_path
    else:
        formScanner_executable = os.path.join("lib","formscanner-main-1.1.2.jar")
    logging.debug("FormScanner executable :: {}".format(formScanner_executable))

    # set the FromScanner xml template file path
    if not os.path.isfile(formScanner_template_xml):
        logging.error("File {} does not exist".format(formScanner_template_xml))
        raise FileNotFoundError("Invalid file FormScanner template file path")
    elif Path(formScanner_template_xml).suffix != ".xtmpl":
        logging.error("File {} is not an XTMPL. Please provide a proper template file.".format(formScanner_template_xml))
        raise FileNotFoundError("Invalid file extension for FormScanner template")
    else:
        logging.debug("FormScanner XTMPL template :: {}".format(formScanner_template_xml))

    # set the parsed output csv file path
    if final_grades_output_csv_filepath:
        final_grades_csv = final_grades_output_csv_filepath
    else:
        final_grades_csv = os.path.join("./", "final_grades.csv")
    logging.debug("Final grades CSV: {}".format(final_grades_csv))

    # set the exam sheets file path
    if not os.path.isfile(students_info):
        logging.error("File {} does not exist".format(students_info))
        raise FileNotFoundError("Invalid students' information file path")
    else:
        logging.debug("Student details CSV :: {}".format(students_info))

    logging.debug("PDF conversion is set to :: {}".format(skip_pdf_conversion))

    return scanned_pdf_dir_path, scanned_images_dir, \
    formScanner_output_csv, formScanner_executable, formScanner_template_xml, \
    final_grades_csv, students_info


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    logging.info("Executing script as standalone")

    args = read_arguments()
    skip_pdf_conversion = True if args.skip_pdf_conversion else False

    # Read the command-line arguments
    scanned_pdf_dir, scanned_images_dir, \
    formScanner_output_csv, formScanner_executable, formScanner_template, \
    final_grades_csv, students_info = parse_arguments(
    args.scanned_pdf_dir, args.output_form_scanner_csv,
    args.form_scanner_path, args.formScanner_template,
    args.final_grades_output_csv, args.students_info, skip_pdf_conversion)

    if skip_pdf_conversion:
        logging.info("Skipping PDF to image conversion.")
    else:
        execute_PdfToPngConverter(scanned_pdf_dir, scanned_images_dir)

    execute_FormScanner(formScanner_executable, formScanner_template, scanned_images_dir, formScanner_output_csv)
    execute_CsvParser(formScanner_output_csv, students_info, final_grades_csv)

    logging.info("Execution completed. Open the {} file to check the results.".format(os.path.abspath(final_grades_csv)))
