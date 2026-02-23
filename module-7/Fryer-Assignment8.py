import json
import os

def loadJson():
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, "student.json")
    
    with open(file_path, "r") as file:
        students = json.load(file)
        
    return students
        
def printJson(students):
    for student in students:
        print(f"{student['L_Name']}")

def main():
    print("HI")

    students = loadJson()
    
    printJson(students)


if __name__ == "__main__":
    main()