class Course:
    def __init__(self, url):
        self.url = url
        
        self.symbol = None
        self.name = None
        self.mark = None
        self.average = None
        self.checked = False


    def __str__(self):
        return f"{self.symbol} - {self.name}\nYour mark:\t{self.mark}\nAverage:\t\t{self.average}"
