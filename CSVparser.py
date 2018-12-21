import csv
import logging
import argparse
import pandas as pd
from openpyxl import load_workbook


# Function to check the parity bit and log if there is any issue
def checkParityBit(bitString, paperID):

    # In this function we break our string and we check
    # if the first string's character is 1 then an even number of 1s should be there
    # if not log it as a mistake
    arrayOfBits = list(bitString)

    # File for logging purposes
    f = open("logs/error_logs", "a+")

    # For Odd numbers of 1s
    if arrayOfBits[0] == '0':

        if bitString.count('1') % 2 != 0:
            #error_message = "Parity bit check error for {}".format(mergeIDElements)
            logging.error('[LOGGING] Parity bit check error for {} seq {}' . format(str(paperID), bitString))
            f.write('Parity bit check error for {} \n'.format(paperID))
            f.close()
            return False
    # For Even number of 1s
    else:
        if (bitString.count('1') - 1) % 2 == 0:
            #error_message = "Parity bit check error for {}".format(mergeIDElements)
            logging.error('[LOGGING] Parity bit check error for {} seq {}' . format(str(paperID), bitString))
            f.write('Parity bit check error for {} \n' . format(paperID))
            f.close()
            return False

    return True


# Function to get the student's names and ID from a CSV file (it was excel before)
def getStudentByID(studentID):

    # Open file where student IDs and Names are located
    with open(args.students_info, 'r', encoding='utf8') as csvfile:
        read_from_csv = csv.reader(csvfile, delimiter=',')
        for row in read_from_csv:
            if studentID in row:
                return str(row).split(',').__getitem__(2).replace("'","")
    # If not found there return an empty string
    return ""


# Section for managing command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("input_csv",
                    help="The CSV file that contains the results produced by FormScanner")
parser.add_argument("output_file",
                    help="The path for the output file. The default will be used if not set by the user.")
parser.add_argument("students_info",
                    help="The path where the student IDs and Name are located")
args = parser.parse_args()

# read the input csvfile_path
csvfile_path = args.input_csv
records = []

with open(csvfile_path, newline='') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in readCSV:
        records.append(row)

# The first record is the title of each filed, therefore, we have to remove it
titleLabel = ["A.M.", "Paper ID", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Student Names"]
records.pop(0)

# Before creating out two dimension array we get the number of fields for each record and then the number of records
# to offer a dynamic flavor for our executable.
firstRecord = ';'.join(records[0])
number_of_columns = firstRecord.count(';') + 1
number_of_students = records.__len__()

Matrix = [[0 for x in range(number_of_columns)] for y in range(number_of_students)]

# Filling array with elements
for x in range(number_of_students):
    arrayRecordElements = ';'.join(records[x]).split(';')
    for y in range(number_of_columns):
        Matrix[x][y] = arrayRecordElements[y].upper()

# We create a new array where we add the new elements sorted and we also merge the student ID and the paper's ID
# Elements 0 => String of 7 numbers(Student ID), 1 => String of papers ID, and 2-12 => Student's answers for
# all the founded number of records
total_number_of_fields = 13
newSortedArray = [[0 for x in range(total_number_of_fields)] for y in range(number_of_students)]
paperFormScannerID = ''
notToInclude = []

for x in range(number_of_students):

    # Get the paper ID given from the FormScanner that is stored  in the first place of the second dimention
    paperFormScannerID = Matrix[x][0]

    # Here we retrieve the students ID from characters and we interpret it in decimals
    mergeIDElements = ''
    for y in range(12, 19):
        if Matrix[x][y] != '':
                mergeIDElements += str(ord(Matrix[x][y]) - 65)

    # Now we are going to pipe the retrieved student ID to get its name
    studentNameID = getStudentByID(mergeIDElements)

    # If the student is not found through an error and log it
    if str(studentNameID).__eq__(""):
        error_message = "Student {} not found".format(mergeIDElements)
        logging.error(error_message)
        f = open("logs/error_logs", "a+")
        f.write("Exam ID: {} Student {} not found \n".format(paperFormScannerID, mergeIDElements))
        f.close()
    # Otherwise add in the table
    else:
        newSortedArray[x][total_number_of_fields-1] = studentNameID

    # Upon exiting store results in newSortedArray as the first element of all Records
    for j in range(2,12):
        newSortedArray[x][j] = Matrix[x][j]
    newSortedArray[x][0] = mergeIDElements

    # Now are going to build a binary number from the Pape's ID
    newSortedArray[x][1] = str(Matrix[x][1]).replace('|','')
    toBinary = ''
    paperIDlist = list(newSortedArray[x][1])

    # For each element of paperIDlist
    # Initially, the paper's ID is trnaslated (from the FormScanner) in letters (ADEJ)
    for code in range(ord('A'), ord('J') + 1):
        if chr(code) in paperIDlist:
            toBinary += "1"
        else:
            toBinary += "0"

    # Call function to check if there is mistake from the scanned documents
    if checkParityBit(toBinary, paperFormScannerID):
        # If there is no mistake convert the binary to Integer
        newSortedArray[x][1] = int(toBinary[2:], 2)
    #If not then remove the whole record
    else:
        newSortedArray[x][0] = '0'
        notToInclude.append(x)

# Here we create a new list with our elements excluding the one that failed the parity bit check
totalNumberPasses = number_of_students - len(notToInclude)
arrayBeforeCSV = []

for x in range(number_of_students):
    for y in range(14):
        if newSortedArray[x][0] != '0':
            arrayBeforeCSV.append(newSortedArray[x])
            break

# Set the output csv file path. The default will be used if not provided in the arguments
output_csvfile_path = "final_grades.csv"
if args.output_file:
    output_csvfile_path = args.output_file

with open(output_csvfile_path, "w+", encoding='utf8') as output_csvfile:
    csvWriter = csv.writer(output_csvfile, delimiter=',')
    csvWriter.writerows([titleLabel] + arrayBeforeCSV)
