from fxtest.running.config import Fxtest
from selenium.webdriver.common.by import By
from fxtest.logging import log
from time import sleep
from fxtest.webdriver import WebDriver


class TestCase(WebDriver):
    
    def assertElementisExist(self,xpath=None,msg=""):
        if xpath is None:
            raise AssertionError("元素未指定")
        elem=Fxtest.driver.find_elements(By.XPATH,xpath)
        for _ in range (Fxtest.timeout):
            
            if len(elem) != 0:
                assert elem[0].is_display(),msg
            else:
                raise AssertionError(msg)

    
    def assertText(self,text=None,msg=""):
        if text is None:
            raise AssertionError ("断言信息为空")
        elem=Fxtest.driver.find_element_by_tag_name("html")
        for _ in range(Fxtest.timeout):           
            try:
                assert text in elem.text,msg
            except AssertionError:
                sleep(1)

    
    def assertElementText(self,text=None,xpath=None,msg=""):
        if xpath is None:
            raise AssertionError("元素未指定")
        elem=Fxtest.driver.find_elements(By.XPATH,elem)
        for _ in range (Fxtest.timeout):
            if len(elem) !=0:
                assert text in elem[0].text,msg
            else:
                raise AssertionError("元素未找到")

            
                    
        
