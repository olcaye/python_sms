import json
from json import JSONEncoder
import dataProcess
import validation

class Student:

    def __init__(self, **kwargs):
        self.firstName = kwargs['firstName'] if 'firstName' in kwargs else 'Not Filled'
        self.lastName = kwargs['lastName'] if 'lastName' in kwargs else 'Not Filled'
        self.age = kwargs['age']  if 'age' in kwargs else 'Not Filled'
        self.gender = kwargs['gender'] if 'gender' in kwargs else 'Not Filled'
        self.major = kwargs['major'] if 'major' in kwargs else 'Not Filled'

    def firstName(self, firstName = None):
        if firstName: self.firstName = firstName
        return self.firstName

    def lastName(self, lastName = None):
        if lastName: self.lastName = lastName
        return self.lastName

    def age(self, age = None):
        if age: self.age = age
        return self.age

    def gender(self, gender = None):
        if gender: self.gender = gender
        return self.gender

    def major(self, major = None):
        if major: self.major = major
        return self.major


class StudentEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__



def main():
    def menuControl():
        print("Q for quit, B for continue")
        userInput = input()
        if userInput.lower() == "q":
            terminate()
        elif userInput.lower() == "b":
            callMenu()
        else:
            print("Invalid Key")
            return menuControl()


    def addStudent():
        print('How many student do you want to add?')
        count = int(input())
        for x in range(count):
            print('First Name:')
            firstName = input()
            print('Last Name:')
            lastName = input()
            print('Age:')
            age = int(input())
            print('Gender:')
            gender = input()
            print('Major:')
            major = input()

            student = Student(firstName=firstName, lastName=lastName, age=age, gender=gender, major=major)
            studentJSONData = json.dumps(student, indent=4, cls=StudentEncoder)
            dataProcess.addStudent(studentJSONData)
            del student

        menuControl()

    def findStudent():
        print("First Name:")
        firstName = input()
        print("Last Name:")
        lastName = input()
        dataProcess.findStudentByName(firstName, lastName)
        menuControl()

    def showAll():
        dataProcess.showAll()
        menuControl()

    def ageFilter():
        print("Min Age:")
        minAge = input()
        print("Max Age:")
        maxAge = input()
        dataProcess.ageFilter(int(minAge), int(maxAge))
        menuControl()

    def updateStudent():
        print("Enter Full Name of Student")
        fullName = input()
        nameData = fullName.partition(' ')
        print("Which field do you want to change?")
        print("\n"
              "1 -> First Name\n"
              "2 -> Last Name\n"
              "3 -> Age\n"
              "4 -> Gender\n"
              "5 -> Major\n")
        field = input()
        print("Enter the new value of this field")
        newValue = input()
        dataProcess.updateData(nameData[0], nameData[2], int(field), newValue)
        menuControl()

    def deleteStudent():
        print("Enter Full Name of Student")
        fullName = input()
        nameData = fullName.partition(' ')
        dataProcess.findStudentByName(nameData[0], nameData[2])
        print("Are you really want to delete this student? Write 'yes' to delete.")
        answer = input()
        if answer == "yes":
            dataProcess.deleteData(nameData[0], nameData[2])
        menuControl()

    def fetchStudent():
        dataProcess.fetchData(30)
        menuControl()

    def terminate():
        print('The program is terminating now.')
        exit()


    menu = {
            "1": ("Add a new student", addStudent),
            "2": ("Find the student", findStudent),
            "3": ("Show all students", showAll),
            "4": ("Show all students by specific age range", ageFilter),
            "5": ("Edit Student Information", updateStudent),
            "6": ("Delete a Student", deleteStudent),
            "7": ("Fetch Students from database.json", fetchStudent),
            "8": ("Terminate the program", terminate)
            }

    def invalid():
        print("invalid option!")

    def callMenu():
        for key in sorted(menu.keys()):
            print(key + ":" + menu[key][0])

        ans = input("Make A Choice:\n")
        menu.get(ans, [None, invalid])[1]()


    callMenu()


if __name__ == '__main__': main()