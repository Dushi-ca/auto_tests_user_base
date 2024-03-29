class Report:
    def __init__(self):
        self.__report_status = True
        self.__report_text = []

    def fail(self, message):
        self.__report_status = False
        self.__report_text.insert(0, message)

    def append(self, message):
        self.__report_text.insert(0, message)

    def __str__(self):
        return '\n'.join(self.__report_text)

    def __bool__(self):
        return self.__report_status

    def check(self):
        assert self, self
        print(self)
