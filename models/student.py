class Student:
    def __init__(self, id, name, classname, age, gender):
        self.id = id
        self.name = name
        self.classname = classname
        self.age = age
        self.gender = gender
    
    def getId(self):
        return self.id
    
    def getName(self):
        return self.name

    def getClassname(self):
        return self.classname
    
    def getAge(self):
        return self.age

    def getGender(self):
        return self.gender