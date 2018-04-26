import sys
import csv
import logging

# Function to check the parity bit and log if there is any issue
def checkParityBit( bitString, paperID):

    # In this function we break our string and we check
    # if the first string char is 1 then an even number of 1s should be there
    # if not log it as a mistake
    arrayOfBits = list(bitString)

    # For Odd numbers of 1s
    if arrayOfBits[0] == '0':

        if bitString.count('1') % 2 != 0:
            logging.error('Paper s ID error!')
            logging.error('Seems there is an issue with the paper ', str(paperID), 'binary ID.')
    # For Even number of 1s
    else:
        if (bitString.count('1') - 1) % 2 == 0:
            logging.error('Paper s ID error!')
            logging.error('Seems there is an issue with the paper ', str(paperID), 'binary ID.')


if len(sys.argv) == 1:
    logging.error('Expected command line argument was not given.')
    logging.error('CSV file path is required.')
    sys.exit(1)

records = []

with open(sys.argv[1], newline='') as csvfile:
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

for x in range(numberOfRows):
    mergeIDElements = ''
    for y in range(12,19):

        if Matrix[x][y] != '':
                mergeIDElements += str(ord(Matrix[x][y]) - 65)

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

    # Get the paper ID given from the FormScanner to use it for logging purposes
    paperFormScannerID = Matrix[x][0]

    # Call function to check if there is mistake from the scanned documents
    checkParityBit(toBinary, paperFormScannerID)

    # Adding the newly binary seq in the place of Lettered paper ID
    newSortedArray[x][1] = int(toBinary[2:], 2)

with open("parsed_from_FormScanner.csv", "w+") as my_csv:
    csvWriter = csv.writer(my_csv, delimiter=',')
    csvWriter.writerows([titleLabel] + newSortedArray)

