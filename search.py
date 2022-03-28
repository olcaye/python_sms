import dataProcess

def showAll():
    dataProcess.showAll()

def findByAge():
    print("Enter The Age")
    student = dataProcess.studentFinder()
    student.value = input()
    student.findByAge()

def findByFirstName():
    print("Enter The Name")
    student = dataProcess.studentFinder()
    student.value = input()
    student.findByFirstName()

def findByLastName():
    print("Enter The Last Name")
    student = dataProcess.studentFinder()
    student.value = input()
    student.findByLastName()

def findByGender():
    print("Gender? (Male or Female)")
    student = dataProcess.studentFinder()
    student.value = input()
    student.findByGender()


def findByMajor():
    print("Enter the Major")
    student = dataProcess.studentFinder()
    student.value = input()
    student.findByMajor()


menu = {
    "1": ("Find By Age", findByAge),
    "2": ("Find By First Name", findByFirstName),
    "3": ("Find By Last Name", findByLastName),
    "4": ("Find By Gender", findByGender),
    "5": ("Find By Major", findByMajor),
}

def invalid():
    print("invalid option!")

def callMenu():
    showAll()
    print("\n")
    for key in sorted(menu.keys()):
        print(key + ":" + menu[key][0])

    ans = input("Make A Choice:\n")
    menu.get(ans, [None, invalid])[1]()


callMenu()
