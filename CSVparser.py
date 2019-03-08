import csv
import logging
import argparse


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


# Method to compose the results file
def produceResultsFile(args, titleLable, arrayBeforeCSV):
    # Set the output csv file path. The default will be used if not provided in the arguments
    output_csvfile_path = "final_grades.csv"
    if args.output_file:
        output_csvfile_path = args.output_file

    with open(output_csvfile_path, "w+", encoding='utf8') as output_csvfile:
        csvWriter = csv.writer(output_csvfile, delimiter=',')
        csvWriter.writerows([titleLabel] + arrayBeforeCSV)


# Method to manage the command line arguments
def read_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i","--input_csv",
                    help="The CSV file that contains the results produced by FormScanner")
    parser.add_argument("-o","--output_file",
                    help="The path for the output file. The default will be used if not set by the user.")
    parser.add_argument("-s","--students_info",
                    help="The path where the student IDs and Name are located")
    args = parser.parse_args()

    return args


# Method that retrieves student info from a given csv file
def get_student_info(args):
    records = []
    with open(args.input_csv, newline='') as csvfile:
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


def analyze_results(records, titleLabel, args):    
    # Before creating our two dimension array we get the number of fields for each record
    # and then the number of records to offer a dynamic flavor for our script.
    first_record = ';'.join(records[0])
    number_of_columns = first_record.count(';') + 1
    number_of_students = records.__len__()
    logging.info("Found {} entries".format(number_of_students))

    Matrix = [[0 for x in range(number_of_columns)] for y in range(number_of_students)]
    for x in range(number_of_students):
        arrayRecordElements = ';'.join(records[x]).split(';')
        for y in range(number_of_columns):
            Matrix[x][y] = arrayRecordElements[y].upper()

    # We create a new array where we add the new elements sorted and we also merge the student ID and the paper's ID
    # Elements 0 => String of 7 numbers(Student ID), 1 => String of papers ID, and 2-12 => Student's answers for
    # all the founded number of records, 14 student name, and 15 for logging comment, error, etc.
    total_number_of_fields = 14
    newSortedArray = [[0 for x in range(total_number_of_fields)] for y in range(number_of_students)]
    paperFormScannerID = ''

    for x in range(number_of_students):

        # Get the paper ID given from the FormScanner that is stored  in the first place of the second dimention
        paperFormScannerID = Matrix[x][0]

        # Here we retrieve the students ID from characters and we interpret it in decimals
        mergeIDElements = ''
        for y in range(12, 19):
            if Matrix[x][y] != '':
                    mergeIDElements += str(ord(Matrix[x][y]) - 65)

        # Now we are going to pipe the retrieved student ID to get its name
        newSortedArray[x][total_number_of_fields - 1] = paperFormScannerID
        studentName = getStudentByID(mergeIDElements)
        comment_message = ''

        # If the student is not found through an error and log it
        if str(studentName).__eq__(""):
            comment_message = "[NOT FOUND] {} in the student info {}".format(mergeIDElements, paperFormScannerID)
            logging.error(comment_message)
            f = open("logs/error_logs", "a+")
            f.write("{}\n".format(comment_message))
            f.close()
            newSortedArray[x][total_number_of_fields - 1] = comment_message
            studentName = "UNKNOWN"
            
        # Now are going to build a binary number from the Pape's ID
        newSortedArray[x][1] = str(Matrix[x][1]).replace('|','')
        toBinary = ''
        paperIDlist = list(newSortedArray[x][1])

        # Initially, the paper's ID is translated (from the FormScanner) in letters (ADEJ)
        for code in range(ord('A'), ord('J') + 1):
            if chr(code) in paperIDlist:
                toBinary += "1"
            else:
                toBinary += "0"

        # Call function to check if there is mistake from the scanned documents
        if checkParityBit(toBinary, paperFormScannerID):
            # If there is no mistake convert the binary to Integer
            newSortedArray[x][1] = int(toBinary[1:], 2)
        else:
            comment_message += "[PARITY BIT] check error for {}".format(paperFormScannerID)
            logging.error(comment_message)
            newSortedArray[x][total_number_of_fields - 1] = comment_message

        get_duplicate = find_duplicate_ID(newSortedArray, mergeIDElements)
        if get_duplicate.__ne__(''):
            comment_message += "[DUPLICATED] {} A.M. with {}".format(paperFormScannerID, get_duplicate)
            logging.error(comment_message)
            newSortedArray[x][total_number_of_fields - 1] = comment_message
            

        # We add the student ID last to have a valid check with find_duplicate method
        newSortedArray[x][0] = mergeIDElements
        newSortedArray[x][total_number_of_fields-2] = studentName

        # Upon exiting store results in newSortedArray as the first element of all Records
        for j in range(2,12):
            newSortedArray[x][j] = Matrix[x][j]

    return newSortedArray


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    logging.info("Executing script as standalone")

    args = read_arguments()

    logging.info("Input csv file: {}".format(args.input_csv))
    titleLabel = ["A.M.", "Paper ID", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Student Names", "Comments"]
    records = get_student_info(args)

    # The first record is the title of each filed, therefore, we have to remove it.
    records.pop(0)

    processed_data = analyze_results(records, titleLabel, args)
    produceResultsFile(args, titleLabel, processed_data)
    logging.info("Execution completed. Process terminated.")
