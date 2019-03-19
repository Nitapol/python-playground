class BodyMassIndex:

    BMI_STATUS_LOSE = 0
    BMI_STATUS_HEALTHY = 1
    BMI_STATUS_GAIN = 2

    def __init__(self, first_name, last_name, age, height, weight):
        self._first_name = first_name
        self._last_name = last_name
        self._age = age
        self._height = height
        self._weight = weight

    def get_full_name(self):
        return self._first_name + " " + self._last_name

    def get_bmi(self):
        return (self._weight * 703) / self._height ** 2

    def get_status(self):
        bmi = self.get_bmi()
        if bmi < 18.5:
            status = BodyMassIndex.BMI_STATUS_LOSE
        elif bmi < 25.0:
            status = BodyMassIndex.BMI_STATUS_HEALTHY
        else:
            status = BodyMassIndex.BMI_STATUS_GAIN
        return status

    def get_report(self):
        a = self.get_full_name()
        b = "Your BMI is: {0:.1f}".format(self.get_bmi())
        status_name = ['n unhealthy BMI, lose some weight!',
                       ' healthy BMI',
                       'n unhealthy BMI, gain some weight!']
        c = 'You have a' + status_name[self.get_status()]
        return a + '\n' + b + '\n' + c


if __name__ == '__main__':

    def first_test():
        user_test_list = [
            ("Alex", "Fat",    21, 69, 170, 2),
            ("Josh", "Smart",  17, 69, 169, 1),
            ("Ann", "Full",    19, 69, 126, 1),
            ("Mary", "Skinny", 19, 69, 125, 0),
        ]
        for first, last, age, height, weight, expected in user_test_list:
            user = BodyMassIndex(first, last, age, height, weight)
            print(user.get_report())
            print()

    first_test()

    while True:
        first = input("Enter your first name: ")
        if not first:
            break
        last = input("Enter your last name: ")
        age = int(input("Enter your age: "))
        height = int(input("Enter your height in inches: "))
        weight = int(input("Enter your weight in lbs: "))
        user = BodyMassIndex(first, last, age, height, weight)
        print(user.get_report())
