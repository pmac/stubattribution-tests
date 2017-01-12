import os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


desired_cap = {
    'platform': "Windows 10",
    'browserName': "chrome",
    'version': "54.0",
}

username=os.environ["SAUCE_USERNAME"]
key=os.environ["SAUCE_ACCESS_KEY"]
sauce_creds=':'.join([username,key])

driver = webdriver.Remote(
   command_executor='http://%s@ondemand.saucelabs.com:80/wd/hub' % sauce_creds,
   desired_capabilities=desired_cap)


driver.get("https://www-demo4.allizom.org/en-US/firefox/new/?utm_source=google&utm_medium=paidsearch&utm_campaign=Brand-US-GGL-Exact&utm_term=download%20firefox")
#downloadButton = WebDriverWait(driver, 10).until(lambda s: len(s.find_element_by_class_name('download-link button button-green').is_displayed()))
driver.implicitly_wait(10)
downloadButton = driver.find_element_by_id("download-button-desktop-release")
downloadButton.click()
driver.implicitly_wait(8)
downloadLink = driver.find_element_by_id("direct-download-link").get_attribute("href")
print "Stub Attribution download link is: %s" % downloadLink

driver.quit()
