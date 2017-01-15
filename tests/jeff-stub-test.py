import os
import urlparse
import urllib

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

DOMAINS = ['.com', '.edu']
SOURCES = ['google.com', 'twitter.com', 'yahoo.com']

username=os.environ["SAUCE_USERNAME"]
key=os.environ["SAUCE_ACCESS_KEY"]
sauce_creds=':'.join([username,key])

driver = webdriver.Remote(
   command_executor='http://%s@ondemand.saucelabs.com:80/wd/hub' % sauce_creds,
   desired_capabilities=desired_cap)


original_url = "https:///en-US/firefox/new/?utm_source=google&utm_medium=paidsearch&utm_campaign=Brand-US-GGL-Exact&utm_term=download%20firefox"


def process_url(source, medium, campaign, term):
    base_url = 'www-demo4.allizom.org'
    modified_url = "https://{}/en-US/firefox/new/?utm_source={}&utm_medium={}&utm_campaign={}&utm_term={}%20firefox".format(
               base_url, source, medium, campaign, term)
#    driver.get(original_url)
    driver.get(modified_url)
    #downloadButton = WebDriverWait(driver, 10).until(lambda s: len(s.find_element_by_class_name('download-link button button-green').is_displayed()))
    driver.implicitly_wait(10)
    downloadButton = driver.find_element_by_id("download-button-desktop-release")
    downloadButton.click()
    driver.implicitly_wait(8)
    downloadLink = driver.find_element_by_id("direct-download-link").get_attribute("href")

    print "Stub Attribution download link is:\n %s" % downloadLink

    return downloadLink

# These are tests

result1 = process_url("google", "paidsearch", "test_Brand-US-GGL-Exact", "download%20firefox")
assert result1 == "https://bouncer-bouncer.stage.mozaws.net/?product=firefox-stub&os=win&lang=en-US&attribution_code=source%3D{}%26medium%3D{}%26campaign%3D{}%26content%3D%28{}%29%26timestamp%3D1484372769&attribution_sig=e026c51a3381b7ab205e51440086f980b037e5333de5537d9161ec27f06f47cf"

result2 = process_url("yahoo", "giveaway", "test_campaign", "download%20firefox")
assert result2 == "https://bouncer-bouncer.stage.mozaws.net/?product=firefox-stub&os=win&lang=en-US&attribution_code=source%3Dgoogle%26medium%3Dpaidsearch%26campaign%3DBrand-US-GGL-Exact%26content%3D%28not+set%29%26timestamp%3D1484372769&attribution_sig=e026c51a3381b7ab205e51440086f980b037e5333de5537d9161ec27f06f47cf"

def interesting_pieces_of_processed_url(url):
    # TODO
    return interesting_pieces

# use however pytest says to do it
# assert interesting_pieces = original_pieces_I_put_in



driver.quit()


'''Stub Attribution download link is: https://bouncer-bouncer.stage.mozaws.net/?product=firefox-stub&os=win&lang=en-US&attribution_code=source%3Dgoogle%26medium%3Dpaidsearch%26campaign%3DBrand-US-GGL-Exact%26content%3D%28not+set%29%26timestamp%3D1484372769&attribution_sig=e026c51a3381b7ab205e51440086f980b037e5333de5537d9161ec27f06f47cf'''
