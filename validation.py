errors = []

def ageValidation(age1, age2):
    if age1 < 7 or age1 > 100:
        errors.append("Error: First value can not be less than 7 and greater than 100")
    elif age2 < 7 or age2 > 100:
        errors.append("Error: Second value can not be less than 7 and greater than 100")
    elif age1 > age2:
        errors.append("Error: First value can not be greater than second value")
    elif age2 < age1:
        errors.append("Error: Second value can not be less than first value")

    return errors

def stringValidation(string):
    if not isinstance(string, str):
        errors.append("Error: Only string is accepted.")
    return string

def numberValidation(userInput):
    if not isinstance(userInput, int):
        errors.append("Error: Only numbers are accepted.")