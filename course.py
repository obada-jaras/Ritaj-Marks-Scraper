class Course:
    def __init__(self, url):
        self.url = url
        
        self.symbol = None
        self.name = None
        self.mark = None
        self.average = None
        self.checked = False


    def __str__(self):
        return f"{self.symbol} {self.name} {self.mark} {self.average}" + f" {self.checked} {self.url}" #TODO: remove the second f-string
