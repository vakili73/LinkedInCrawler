from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class State:
    INIT = 'init'
    MAIN = 'main_page'
    HOME = 'homepage_basic'


class LinkedIn:
    def __init__(self,
                 state=State.INIT,
                 driver=webdriver.Firefox()):
        self.__driver = driver
        self.__state = state

    def state(self):
        return self.__state

    def driver(self):
        return self.__driver

    def open(self):
        assert self.__state == State.INIT, 'To open the LinkedIn website your state must be in the State.INIT.'

        try:
            self.__driver.get('https://www.linkedin.com/')
            self.__state = State.MAIN
            return True

        except Exception as error:
            self.__driver.close()
            raise error

    def login(self, username, password):
        assert self.__state == State.MAIN, 'To login to the LinkedIn website your state must be in the State.MAIN.'

        try:
            inputUsername = self.__driver.find_element(By.XPATH,
                                                       value='/html/body/nav/section[2]/form/div[1]/div[1]/input')
            inputUsername.send_keys(username)

            inputPassword = self.__driver.find_element(By.XPATH,
                                                       value='/html/body/nav/section[2]/form/div[1]/div[2]/input')
            inputPassword.send_keys(password)

            buttonSignIn = self.__driver.find_element(By.XPATH,
                                                      value='/html/body/nav/section[2]/form/div[2]/button')
            buttonSignIn.click()

            self.__state = State.HOME
            return True

        except Exception as error:
            self.__driver.close()
            raise error

    def logout(self):
        assert not (self.__state == State.INIT or self.__state ==
                    State.MAIN), 'Can\'t logout before logged in'

        try:
            self.__driver.get('https://www.linkedin.com/m/logout/')
            self.__state = State.INIT
            self.open()
            return True

        except Exception as error:
            self.__driver.close()
            raise error

    def waitUntil(self, timeout=10,
                  condition=EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'footer'))):
        try:
            WebDriverWait(self.__driver, timeout).until(condition)
            return True

        except Exception as error:
            self.__driver.close()
            raise error

    def setProxy(self):
        pass

    def getProfile(self):
        pass

    def getJobs(self):
        pass

    def getFriends(self):
        pass

    def goto(self, state):
        pass


if __name__ == "__main__":

    linkedin = LinkedIn()
    linkedin.open()

    linkedin.login('v.vakili73@gmail.com', '0307019580003')
    linkedin.logout()
