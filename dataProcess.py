import collections
import json
import simplejson
import validation
import random
from prettytable import PrettyTable

data = collections.defaultdict(dict)

def prettyJsonData():
    parsedAsJson = json.dumps(data)
    print(simplejson.dumps(simplejson.loads(parsedAsJson), indent=4, sort_keys=False))


def tableTitle():
    return PrettyTable(['Record ID', 'First Name', 'Last Name', 'Age', 'Gender', 'Major'])


# Write the contents of the student array to a file
def write(data):
    parsedAsJson = json.dumps(data)
    dataFile = open("students.json", "w")
    dataFile.write(simplejson.dumps(simplejson.loads(parsedAsJson), indent=4, sort_keys=False))
    dataFile.close()

# Read student data from a file and populate the student array.
def dataFromFile():
    with open('students.json') as json_file:
        data = json.load(json_file)
        json_file.close()
        return data

# Check capacity of any array.
def checkCapacity(dataArr):
    return True if len(dataArr) < 100 else False

# Return number of records in the file.
def numberOfRecords(dataArr):
    return len(dataArr)

def fetchData(rowNumber = 10, fetchAll = False):
    with open('database.json') as json_file:
        #fetch data from external file
        fetchedData = json.load(json_file)
        json_file.close()

        # fetch the already registered students from students.json.
        # hence, new students in the database.json will be added end of the file.
        # So already existed students will not be deleted or overwritten.
        data = dataFromFile()
        beforeNewData = len(data)
        # Check whether students.json file empty or not
        if len(data) != 0:
            # If its not empty, get the last key
            currentIndex = int(list(data)[-1])
        else:
            # If It is empty, set the first key as 0.
            currentIndex = 0

        countData = 0

        # Looping the data in the database.json file.
        for info in fetchedData:
            # Check whether student.json file has 100 students or not before every data appending.
            if checkCapacity(data):
                countData += 1
                currentIndex += 1
                # Append data from database.json to data[] array.
                data[currentIndex] = info

                # This is a limit condition. Doe user want to fetch all data or just specified number of data from database.json?
                # If fetchAll parameter is not true, only specified number of rows by user or default parameter value (10) will be fetched.
                if not fetchAll:
                    if countData == rowNumber:
                        break
            else:
                print('Capacity is full now. Cant proceed.')
                break

        # Call write() function to writing the datas in data[] to students.json
        write(data)

        afterNewData = len(data)

        return print(
            "\nTotal Student Number Before Process: {}\n"
            "Now, {} Student(s) has been added\n"
            "Total number of students are currently: {}"
                .format(beforeNewData, countData, afterNewData))

# Add a new student to file
def addStudent(JSONData):
    # Decode Json Formatted Data
    userData = json.loads(JSONData)

    data = dataFromFile()

    # Find last key in the data and increment it 1.
    if len(data) != 0:
        newIndex = int(list(data)[-1]) + 1
    else:
        newIndex = 1

    # Populate the new index with User Data
    data[newIndex] = userData

    write(data)
    print('\nSuccessfully Added')
    return print("Now you have {} students in the file" .format(numberOfRecords(data)))


# Find a student by first name and last name, and show all the information
def findStudentByName(inputFirstName, inputLastName):

    recordID = findID(inputFirstName, inputLastName)

    if recordID:
        data = dataFromFile()
        t = tableTitle()
        t.align = "l"

        for uid, info in data.items():
           if recordID == uid:
                t.add_row([uid, info['firstName'], info['lastName'], info['age'], info['gender'], info['major']])
                break
        return print(t.get_string(sortby="First Name"))
    else:
        print("No Record Found")

def findStudentByID(recordID):

    data = dataFromFile()
    t = tableTitle()
    t.align = "l"

    result = False

    for uid, info in data.items():
       if recordID == uid:
            result = True
            t.add_row([uid, info['firstName'], info['lastName'], info['age'], info['gender'], info['major']])
            break

    return print(t.get_string(sortby="First Name")) if result else print("No Record Found")

def findID(inputFirstName, inputLastName):
    searchFirstName = inputFirstName
    searchLastName = inputLastName
    data = dataFromFile()
    recordID = None
    for uid, info in data.items():
       if searchFirstName == info['firstName'] and searchLastName == info['lastName']:
            recordID = uid
            break

    return recordID or False

# Show all students in a given age range (e.g. between ages 34 and 50)
def ageFilter(inputMinAge, inputMaxAge):

    validation.ageValidation(inputMinAge, inputMaxAge)

    if len(validation.errors) == 0:
        data = dataFromFile()
        t = tableTitle()
        result = 0
        t.align = "l"

        for uid, info in data.items():
            if info['age'] == "Not Filled":
                continue
            if inputMinAge <= int(info['age']) <= inputMaxAge:
                result += 1
                t.add_row([uid, info['firstName'], info['lastName'], info['age'], info['gender'], info['major']])
        return print("{} result(s) found\n".format(result), t.get_string(sortby="Age")) if result else print("No Record Found")

    else:
        for i in range(len(validation.errors)):
            print(validation.errors[i])


# Show all students
def showAll():
    data = dataFromFile()
    t = tableTitle()
    t.align = "l"
    result = 0

    if len(data) > 0:
        for uid, info in data.items():
            result += 1
            t.add_row([uid, info['firstName'], info['lastName'], info['age'], info['gender'], info['major']])
        return print("{} result(s) found\n".format(result), t.get_string(sortby="First Name"))

    else:
        return print("No Record Found")


# Modify a student record: input the first and last names, ask the field to modify,
# and get the new value from the user. Modify the record accordingly.
def updateData(inputFirstName, inputLastName, field, newValue):
    fieldSelector = {
        1: 'firstame',
        2: 'lastName',
        3: 'age',
        4: 'gender',
        5: 'major'
    }

    recordID = findID(inputFirstName, inputLastName)
    data = dataFromFile()

    for uid, info in data.items():
        if recordID == uid:
            if field != 3:
                info[fieldSelector.get(field)] = newValue
                break
            else:
                info[fieldSelector.get(field)] = int(newValue)
                break
    write(data)

    return findStudentByID(recordID)

# Delete a student with a specific first name-last name.
def deleteData(inputFirstName, inputLastName):
    recordID = findID(inputFirstName, inputLastName)
    data = dataFromFile()
    for uid, info in data.items():
        if recordID == uid:
            data.pop(uid)
            break
    write(data)

    print("Successfully Deleted.\n")
    return showAll()


# This class for search.py file.
class studentFinder(object):

    result = 0

    def __init__(self):
        self.value = None
        self.data = dataFromFile()
        self.t = tableTitle()


    def findByAge(self):
        for uid, info in self.data.items():
            if info['age'] == "Not Filled":
                continue
            if int(self.value) == int(info['age']):
                self.result += 1
                self.t.add_row([uid, info['firstName'], info['lastName'], info['age'], info['gender'], info['major']])
        return print("{} result(s) found\n".format(self.result), self.t.get_string(sortby="Age")) if self.result else print(
            "No Record Found")


    def findByFirstName(self):
        for uid, info in self.data.items():
            if self.value == info['firstName']:
                self.result += 1
                self.t.add_row([uid, info['firstName'], info['lastName'], info['age'], info['gender'], info['major']])
        return print("{} result(s) found\n".format(self.result),
                     self.t.get_string(sortby="Last Name")) if self.result else print(
            "No Record Found")

    def findByLastName(self):
        for uid, info in self.data.items():
            if self.value == info['lastName']:
                self.result += 1
                self.t.add_row([uid, info['firstName'], info['lastName'], info['age'], info['gender'], info['major']])
        return print("{} result(s) found\n".format(self.result),
                     self.t.get_string(sortby="First Name")) if self.result else print(
            "No Record Found")

    def findByGender(self):
        for uid, info in self.data.items():
            if self.value == info['gender']:
                self.result += 1
                self.t.add_row([uid, info['firstName'], info['lastName'], info['age'], info['gender'], info['major']])
        return print("{} result(s) found\n".format(self.result),
                     self.t.get_string(sortby="First Name")) if self.result else print(
            "No Record Found")

    def findByMajor(self):
        for uid, info in self.data.items():
            if self.value == info['major']:
                self.result += 1
                self.t.add_row([uid, info['firstName'], info['lastName'], info['age'], info['gender'], info['major']])
        return print("{} result(s) found\n".format(self.result),
                     self.t.get_string(sortby="First Name")) if self.result else print(
            "No Record Found")