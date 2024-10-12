import argparse
import csv
import logging
import os
import sys

# Function to check the parity bit and log if there is any issue
def checkParityBit(bitString):

    # In this function we break our string and we check
    # if the first string's character is 1 then an even number of 1s should be there
    # if not log it as a mistake
    arrayOfBits = list(bitString)

    # For Odd numbers of 1s
    if arrayOfBits[0] == '0':

        if bitString.count('1') % 2 != 0:
            return False
    # For Even number of 1s
    else:
        if (bitString.count('1') - 1) % 2 == 0:
            return False

    return True


# Function to get the student's names and ID from a CSV file (it was excel before)
def get_studentName_by_ID(studentID, students_info):

    # Open file where student IDs and Names are located
    with open(students_info, 'r', encoding='utf8') as csvfile:
        read_from_csv = csv.reader(csvfile, delimiter=',')
        for row in read_from_csv:
            if studentID in row:
                return (str(row)
                        .split(',')[1]
                        .replace("'","")
                        .replace("]",""))
    # If not found there return an empty string
    return ""


# Method to compose the results file
def produceResultsFile(output_csvfile_path, titleLabel, arrayBeforeCSV):
    with open(output_csvfile_path, "w+", encoding='utf-8-sig') as output_csvfile:
        csvWriter = csv.writer(output_csvfile, delimiter=',')
        csvWriter.writerows([titleLabel] + arrayBeforeCSV)


# Method to manage the command line arguments
def read_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_csv",
        help="The CSV file that contains the results produced by FormScanner")
    parser.add_argument("students_info",
        help="The path where the student IDs and Name are located")
    parser.add_argument("output_file",
        help="The path for the output file. The default will be used if not set by the user.")
    args = parser.parse_args()

    return args


def parse_arguments(input_csv, students_info, output_file):
    if not os.path.isfile(input_csv):
        logging.error("FormScanner input csv file does not exist in path :: {}".format(input_csv))
        raise FileNotFoundError("Invalid FormScanner input csv file")
        sys.exit(1)

    if not os.path.isfile(students_info):
        logging.error("Students info input file does not exist in path :: {}".format(students_info))
        raise FileNotFoundError("Invalid students info input file")
        sys.exit(1)

    logging.info('''Parsing FormScanner CSV ...
        - FormScanner input CSV: {}
        - Students info CSV: {}
        - Final results output CSV: {}'''
        .format(os.path.abspath(input_csv), os.path.abspath(students_info), os.path.abspath(output_file)))


# Method that opens and stores in memory the results of the given FormScanner output csv
def read_formScanner_output_csv(input_csv):
    records = []
    with open(input_csv, newline='') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in readCSV:
            records.append(row)

    return records


# Method that checks for duplicate occurances of the same A.M.
def find_duplicate_ID(arrayWithStudents, currentID):

    numrows = len(arrayWithStudents)
    for x in range(numrows):
        if str(currentID).__eq__(str(arrayWithStudents[x][0])):
            return arrayWithStudents[x][1]
    return ''


def analyze_results(records, titleLabel, students_info):
    # Before creating our two dimension array we get the number of fields for each record
    # and then the number of records to offer a dynamic flavor for our script.
    first_record = ';'.join(records[0])
    number_of_columns = first_record.count(';') + 1
    number_of_students = records.__len__()
    logging.info("Found {} exam entries to parse. Parsing results:".format(number_of_students))

    Matrix = [[0 for x in range(number_of_columns)] for y in range(number_of_students)]
    for x in range(number_of_students):
        arrayRecordElements = ';'.join(records[x]).split(';')
        for y in range(number_of_columns):
            Matrix[x][y] = arrayRecordElements[y].upper()

    # We create a new array where we add the new elements sorted and we also merge the student ID and the paper's ID
    # Elements 0 => String of 7 numbers(Student ID), 1 => String of papers ID, and 2-12 => Student's answers for
    # all found number of records, 14 student name, and 15 for logging comment, error, etc.
    total_number_of_fields = 14
    newSortedArray = [[0 for x in range(total_number_of_fields)] for y in range(number_of_students)]
    paperFormScannerID = ''

    successful_scans = 0
    for x in range(number_of_students):

        # Get the paper ID given from the FormScanner that is stored  in the first place of the second dimension
        paperFormScannerID = Matrix[x][0]

        # Retrieve the students ID from characters and interpret it in decimals
        mergeIDElements = ''
        for y in range(12, 19):
            if Matrix[x][y] != '':
                    mergeIDElements += str(ord(Matrix[x][y]) - 65)

        # Obtain student name from student ID
        newSortedArray[x][total_number_of_fields - 1] = paperFormScannerID
        comment_message = ''
        if len(mergeIDElements) != 7:
            comment_message = f"[INVALID STUDENT ID LENGHT] {mergeIDElements} "
        else:
            studentName = get_studentName_by_ID(mergeIDElements, students_info)
            # If the student is not found through an error and log it
            if not studentName:
                comment_message = f"[STUDENT ID NOT FOUND] {mergeIDElements} "

        if comment_message:
            newSortedArray[x][total_number_of_fields - 1] = comment_message
            studentName = "UNKNOWN"

        # Build a binary number from the Pape's ID
        newSortedArray[x][1] = str(Matrix[x][1]).replace('|','')
        toBinary = ''
        paperIDlist = list(newSortedArray[x][1])

        # Initially, the paper's ID is translated (from the FormScanner) in letters (ADEJ)
        for code in range(ord('A'), ord('J') + 1):
            if chr(code) in paperIDlist:
                toBinary += "1"
            else:
                toBinary += "0"

        # Check if there is mistake from the scanned documents
        comment2 = ''
        documentId = int(toBinary[1:], 2)
        if documentId < 100:
            comment2 = f"[INVALID DOCUMENT ID VALUE] {documentId} "
        elif not checkParityBit(toBinary):
            comment2 = f"[INVALID DOCUMENT ID PARITY] {documentId} "
        else:
            newSortedArray[x][1] = documentId

        if comment2:
            comment_message += comment2
            newSortedArray[x][total_number_of_fields - 1] = comment_message

        get_duplicate = find_duplicate_ID(newSortedArray, mergeIDElements)
        if get_duplicate.__ne__(''):
            comment_message += "[DUPLICATED] {} A.M. with {}".format(paperFormScannerID, get_duplicate)
            newSortedArray[x][total_number_of_fields - 1] = comment_message

        if comment_message:
            logging.warning(comment_message)
            f = open("logs/error_logs", "a+")
            f.write("{}\n".format(comment_message))
            f.close()
        else:
            successful_scans += 1

        # We add the student ID last to have a valid check with find_duplicate method
        newSortedArray[x][0] = mergeIDElements
        newSortedArray[x][total_number_of_fields-2] = studentName

        # Upon exiting store results in newSortedArray as the first element of all Records
        for j in range(2,12):
            newSortedArray[x][j] = Matrix[x][j]

    logging.info(f"Converted {successful_scans} out of {number_of_students} documents")
    return newSortedArray


def parse_FormScanner_csv(input_csv, students_info, output_file):
    titleLabel = ["A.M.", "Exam ID", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Student Name", "Comments"]
    records = read_formScanner_output_csv(input_csv)

    # The first record is the title of each field, therefore, we have to remove it.
    records.pop(0)

    processed_data = analyze_results(records, titleLabel, students_info)
    produceResultsFile(output_file, titleLabel, processed_data)


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    logging.info("Executing script as standalone")

    args = read_arguments()
    input_csv = args.input_csv
    students_csv = args.students_info
    output_csv = args.output_file

    parse_arguments(input_csv, students_csv, output_csv)
    parse_FormScanner_csv(input_csv, students_csv, output_csv)
