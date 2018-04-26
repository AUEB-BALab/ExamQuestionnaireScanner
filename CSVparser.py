import sys
import csv
import logging
import argparse
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument("input_csv",
    help="The CSV file that contains the results produced by FormScanner")
parser.add_argument("-o", "--output_file",
    help="The path for the output file. The default will be used if not set by the user.")
parser.add_argument("-e", "--exams_sheet",
    help="The path for the exam's excel document. The default will be used if not set by the user.")
args = parser.parse_args()


# Function to check the parity bit and log if there is any issue
def checkParityBit(bitString, paperID):

    # In this function we break our string and we check
    # if the first string char is 1 then an even number of 1s should be there
    # if not log it as a mistake
    arrayOfBits = list(bitString)

    # File for logging purposes
    f = open("error_logs", "a+")

    # For Odd numbers of 1s
    if arrayOfBits[0] == '0':

        if bitString.count('1') % 2 != 0:
            logging.error('Parity bit check error for ', str(paperID))
            f.write('Parity bit check error for %s \n' % str(paperID))
            f.close()
            return False
    # For Even number of 1s
    else:
        if (bitString.count('1') - 1) % 2 == 0:
            logging.error('Parity bit check error for ', str(paperID))
            f.write('Parity bit check error for %s \n' % str(paperID))
            f.close()
            return False

    return True


def  getStudentByID(stduentID):

    # From Professors grade sheet get all the students
    xls_file = pd.ExcelFile(args.exams_sheet, column="", index="")
    df = xls_file.parse('students')
    dfSelect = pd.DataFrame(df, columns=['Α/Α', 'Αρ. Μητρώου', 'Φοιτητής', 'Πατρώνυμο Πρόγρ. Τμήματος'])

    # This command will match the specific student
    getStudent = dfSelect[dfSelect['Φοιτητής'].str.contains(stduentID)]

    # Upon matching return that studnet
    if (dfSelect[dfSelect['Φοιτητής'].str.contains(stduentID)].empty):
        return ""
    else:
        return (getStudent['Φοιτητής'])

# read the input csvfile_path
csvfile_path = args.input_csv
records = []

with open(csvfile_path, newline='') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in readCSV:
        records.append(row)

# The first record is the title of each filed, therefore, we have to remove it
titleLabel = records[0]
records.pop(0)

# Before creating out two dimension array we get the number of fields for each record and then the number of records
# to offer a dynamic flavor for our executable.
firstRecord = ';'.join(records[0])
numberOfColumns = firstRecord.count(';') + 1
numberOfRows = records.__len__()

Matrix = [[0 for x in range(numberOfColumns)] for y in range(numberOfRows)]

# Filling array with elements
for x in range(numberOfRows):
    arrayRecordElements = ';'.join(records[x]).split(';')
    for y in range(numberOfColumns):
        Matrix[x][y] = arrayRecordElements[y].upper()

# We create a new array where we add the new elements sorted and we also merge the student ID and the paper's ID
# Elements 0 => String of 7 numbers(Student ID), 1 => String of papers ID, and 2-12 => Student's answers for
# all the founded number of records
newSortedArray = [[0 for x in range(12)] for y in range(numberOfRows)]
paperFormScannerID = ''
notToInclude = []

# File for logging purposes


for x in range(numberOfRows):

    # Get the paper ID given from the FormScanner to use it for logging purposes
    paperFormScannerID = Matrix[x][0]

    # Here we retrieve the students ID from characters and we interpret it in decimals
    mergeIDElements = ''
    for y in range(12,19):
        if Matrix[x][y] != '':
                mergeIDElements += str(ord(Matrix[x][y]) - 65)

    # Now we are going to pipe the retrieved student ID to get its name
    studentName = getStudentByID(mergeIDElements)

    # If the student is not found through an error and log it
    if studentName == "":
        logging.error("Student with ID ", mergeIDElements, " not found")
        f = open("error_logs", "a+")
        #f.write("In exam %s student with ID %s not found \n" % str(paperFormScannerID), str(mergeIDElements))
        f.write("In exam %s student with ID was not found \n" % str(paperFormScannerID),)
        f.close()


    # Upon exiting store results in newSortedArray as the first element of all Records
    for j in range(2,12):
        newSortedArray[x][j] = Matrix[x][j]
    newSortedArray[x][0] = mergeIDElements

    # Now are going to build a binary number from the Pape's ID
    newSortedArray[x][1] = str(Matrix[x][1]).replace('|','')
    toBinary = ''
    paperIDlist = list(newSortedArray[x][1])

    # For each element of paperIDlist
    for code in range(ord('A'), ord('J') + 1):
        if chr(code) in paperIDlist:
            toBinary += "1"
        else:
            toBinary += "0"

    # Call function to check if there is mistake from the scanned documents
    if checkParityBit(toBinary, paperFormScannerID):
        # Adding the newly binary seq in the place of Lettered paper ID
        newSortedArray[x][1] = int(toBinary[2:], 2)
    #If not then remove the whole record
    else:
        newSortedArray[x][0] = '0'
        notToInclude.append(x)

# Here we create a new list with our elements excluding the one that failed the parity bit check
totalNumberPasses = numberOfRows - len(notToInclude)
arrayBeforeCSV = []

for x in range(numberOfRows):
    for y in range(12):
        if newSortedArray[x][0] != '0':
            arrayBeforeCSV.append(newSortedArray[x])
            break

# Set the output csv file path. The default will be used if not provided in the arguments
output_csvfile_path = "parsed_from_FormScanner.csv"
if args.output_file:
    output_csvfile_path = args.output_file

with open(output_csvfile_path, "w+") as output_csvfile:
    csvWriter = csv.writer(output_csvfile, delimiter=',')
    csvWriter.writerows([titleLabel] + arrayBeforeCSV)

