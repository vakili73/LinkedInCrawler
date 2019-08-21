from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

LINKEDIN_SITE = 'https://www.linkedin.com/'


class State:
    INIT = 'init'
    MAIN = 'main_page'
    HOME = 'homepage_basic'
    PROFILE = 'linkedin_profile'


class LinkedIn:
    def __init__(self,
                 state=State.INIT,
                 driver=webdriver.Firefox(),
                 profile_skills_expanded=False):
        self.__driver = driver
        self.__state = state

        self.__profile_skills_expanded = profile_skills_expanded

    def state(self):
        return self.__state

    def driver(self):
        return self.__driver

    def open(self):
        assert self.__state == State.INIT, 'To open the LinkedIn website your state must be in the State.INIT.'

        try:
            self.__driver.get(LINKEDIN_SITE)
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
            self.__driver.get(LINKEDIN_SITE+'/m/logout/')
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
        '''
            Firefox up to version 47.0.1
            link: https://www.seleniumhq.org/docs/04_webdriver_advanced.jsp#remotewebdriver
            Firefox maintains its proxy configuration in a profile. You can preset the proxy in a profile and use that Firefox Profile or you can set it on profile that is created on the fly as is shown in the following example - deprecated, no longer working with GeckoDriver.
        '''
        pass

    def getSkills(self):
        assert self.__state == State.PROFILE, 'To get profile information your state must be in the State.PROFILE.'

        try:
            if not self.__profile_skills_expanded:
                scrollHeight = self.__driver.execute_script(
                    'return document.body.scrollHeight;')
                for i in range(0, scrollHeight+1000, 5):
                    self.__driver.execute_script('scroll(0, {})'.format(i))
                    try:
                        buttonShowMoreSkills = self.__driver.find_element(By.XPATH,
                                                                          value='/html/body/div[6]/div[6]/div[3]/div/div/div/div/div[2]/div[1]/div[6]/div[3]/div/section/div[2]/button')
                        buttonShowMoreSkills.click()
                    except:
                        continue
                self.__skills_expanded = True

            results = {}

            mainSkillsElements = self.__driver.find_elements_by_xpath(
                '/html/body/div/div/div/div/div/div/div/div/div/div/div/div/section/ol/li/div/div')
            knownSkillsElements = self.__driver.find_elements_by_xpath(
                '/html/body/div/div/div/div/div/div/div/div/div/div/div/div/section/div[2]/div')
            
            ###################### Bug
            if not mainSkillsElements == []:
                for mainSkill in mainSkillsElements:
                    print(mainSkill.text)

            if not knownSkillsElements == []:
                for knownSkill in knownSkillsElements:
                    print(knownSkill.text)
            ###################### Bug
            
            return results

        except Exception as error:
            self.__driver.close()
            raise error

        pass

    def getJobs(self):
        pass

    def getFriends(self):
        pass

    def gotoProfile(self):
        assert self.__state == State.HOME, 'To go to the LinkedIn profile your state must be in the State.HOME.'

        try:
            buttonProfile = self.__driver.find_element(By.XPATH,
                                                       value='/html/body/div[6]/div[6]/div[3]/div/div/div[2]/aside[1]/div[1]/div/div[1]/a[1]')
            self.__driver.get(buttonProfile.get_attribute('href'))

            self.__state = State.PROFILE
            return True

        except Exception as error:
            self.__driver.close()
            raise error


if __name__ == "__main__":

    linkedin = LinkedIn()
    linkedin.open()

    linkedin.login('v.vakili73@gmail.com', '0307019580003')
    linkedin.waitUntil()

    linkedin.gotoProfile()
    linkedin.waitUntil()

    linkedin.getSkills()
