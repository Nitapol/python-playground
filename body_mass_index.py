class BMI:

    def __init__(self, firstName, lastName, age, height, weight):
        self.firstName = firstName
        self.lastName = lastName
        self.fullName = firstName + " " + lastName
        self.age = age
        self.height = (height * 0.025) ** 2
        self.weight = weight * 0.45

    def setFullName(self, firstName, lastName):
        self.firstName = firstName
        self.lastName = lastName
        self.fullName = firstName + " " + lastName

        print(self.fullName)

    def setAge(self, age):
        self.age = age

    def setHeight(self, height):
        self.height = (height * 0.025) ** 2

    def setWeight(self, weight):
        self.weight = weight * 0.45

    def getBMI(self):
        bmi = self.weight // self.height
        return bmi

    def getStatus(self):

        getBMI()

        if bmi < 19:
            print("You have an unhealthy BMI, gain some weight!")
        elif bmi > 19 and bmi < 25:
            print("You have a healthy BMI")
        else:
            print("You have an unhealthy BMI, lose some weight!")


firstName = input("Enter your first name: ")

lastName = input("Enter your last name: ")

age = int(input("Enter your age: "))

height = int(input("Enter your height in inches: "))

weight = int(input("Enter your weight in lbs: "))

userInputBMI = BMI(firstName, lastName, age, height, weight)


print(userInputBMI.setFullName(firstName, lastName))

print("Your BMI is:", userInputBMI.getBMI())

print(userInputBMI.getStatus())
