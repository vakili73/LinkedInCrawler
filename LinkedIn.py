from selenium import webdriver


class LinkedIn:
    def __init__(self, driver=webdriver.Firefox()):
        self.__driver = driver
        self.__is_link_opened = False

    def openLink(self, link='https://www.linkedin.com/'):
        self.__driver.get(link)

    def login(self, email, password):
        if not self.__is_link_opened:
            self.openLink()
        
        pass

    def setProxy(self):
        pass

    def getPerson(self):
        pass


if __name__ == "__main__":
    linkedin = LinkedIn()
