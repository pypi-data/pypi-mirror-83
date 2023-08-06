from fxtest.webdriver import WebDriver
from fxtest.running.config import Fxtest
from fxtest.running.config import BrowserConfig
from fxtest.driver import Browser
from fxtest.logging import log
import os 
import time
import pytest
import inspect

def main(browser=None,path=None,timeout=10,htmlpath=None,cmds="-s"):

    if browser is None:
        BrowserConfig.name="chrome"
    else:
        BrowserConfig.name=browser
    if isinstance(timeout, int):
        Fxtest.timeout = timeout
    else:
        raise TypeError("Timeout {} is not integer.".format(timeout))


    """
    
    """
    Fxtest.driver=Browser(name=BrowserConfig.name,grid_url=BrowserConfig.grid_url)
    
    filename="report"
    allure_name="allure-results"
    allure_report_path="allure-report"
    if filename not in os.listdir(os.getcwd()):
        os.mkdir(os.path.join(os.getcwd(), "report"))
    if filename not in os.listdir(os.getcwd()):
        os.mkdir(os.path.join(os.getcwd(),allure_name))
    allure_report=os.path.join(os.getcwd(),allure_name)
    BrowserConfig.allure_path=allure_report

    if htmlpath is None:
        now = time.strftime("%Y_%m_%d_%H_%M_%S")
        report=os.path.join(os.getcwd(),"report",now+"_result.html")
        BrowserConfig.report_path=report

    else:
        report=os.path.join(os.getcwd(),"report",report)
        BrowserConfig.report_path=report
    
    try:
        cmd_list=cmds.split(" ")
    except Exception:
        log.error("参数错误")
    for cmd in cmd_list:
        if "--fxtest-html" in cmd :
            cmd_list.remove(cmd)
    cmd_list.append("--fxtest-html={}".format(BrowserConfig.report_path))
    cmd_list.append("--alluredir={}".format(BrowserConfig.allure_path))
    
    if path is None:
        stack_t = inspect.stack()
        ins = inspect.getframeinfo(stack_t[1][0])
        file_dir = os.path.dirname(os.path.abspath(ins.filename))
        file_path=ins.filename
        if "\\" in file_path:
            this_file=file_path.split("\\")[-1]
        elif "/" in file_path:
            this_file = file_path.split("/")[-1]
        else:
            this_file = file_path
        test_path=os.path.join(file_dir,this_file)
    else:
        if len(path)>3:
            if path[-3]==".py":
                test_path=path
            else:
                test_path=path
    cmd_list.append(test_path)
    Fxtest.driver.maximize_window()

    pytest.main(cmd_list)
    
    allure_generate ="allure generate {0} --clean -o {1}".format(BrowserConfig.allure_path,allure_report_path)
    res=os.system(allure_generate)
    if res == 0:
        log.info("成功生成allure 报告")
    else:
        log.info("生成allure报告失败")
    
    """
    
    """
    Fxtest.driver.quit()


if __name__ == "__main__":
    pass


