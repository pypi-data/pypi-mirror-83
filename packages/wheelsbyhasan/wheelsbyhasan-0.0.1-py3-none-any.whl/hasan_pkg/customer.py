
class Customer:
    def __init__(self, firstName, lastName):
        self.firstName = firstName
        self.lastName = lastName

    def getName(self):
        return f"{self.firstName} {self.lastName}"
