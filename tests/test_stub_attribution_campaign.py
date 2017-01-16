import os
import urlparse

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


desired_cap = {
    'platform': "Windows 10",
    'browserName': "chrome",
    'version': "54.0",
}

username = os.environ["SAUCE_USERNAME"]
key = os.environ["SAUCE_ACCESS_KEY"]
sauce_creds = ':'.join([username,key])

driver = webdriver.Remote(
   command_executor = 'http://%s@ondemand.saucelabs.com:80/wd/hub' % sauce_creds,
   desired_capabilities = desired_cap)

def generate_url(source, medium, campaign, term):
    base_url = 'www-demo4.allizom.org'
    generated_url = "https://{}/en-US/firefox/new/?utm_source={}&utm_medium={}&utm_campaign={}&utm_term={}".format(
               base_url, source, medium, campaign, term)
    return generated_url


def derive_url(generated_url):
    driver.get(generated_url)

    #downloadButton = WebDriverWait(driver, 10).until(lambda s: len(s.find_element_by_class_name('download-link button button-green').is_displayed()))
    driver.implicitly_wait(10)
    downloadButton = driver.find_element_by_id("download-button-desktop-release")
    downloadButton.click()
    driver.implicitly_wait(8)
    downloadLink = driver.find_element_by_id("direct-download-link").get_attribute("href")

    print "Stub Attribution download link is:\n %s" % downloadLink

    return downloadLink


def breakout_utm_param_values(generated_url):
    parts = urlparse.urlparse(generated_url)
    scheme, netloc, path, params, query, fragment = parts

    key_value_dict = urlparse.parse_qs(query)

    attribution_code = key_value_dict['attribution_code']

    # The thing is an array -- I don't know why. But there's only one element, so
    # just pick the first item off (ie ...[0])
    first_element = attribution_code[0]

    # split on '&', into an array
    equal_pieces = first_element.split('&')

    # Now split up the bunch of strings with 'a=b' in them, into tuples, of (a, b)
    equal_pieces_as_dict = {}
    for equal_piece in equal_pieces:
        key, value = equal_piece.split('=')
        equal_pieces_as_dict[key] = value
    del equal_pieces_as_dict['content']
    del equal_pieces_as_dict['timestamp']

    return equal_pieces_as_dict


def assert_good(new_dict, source, medium, campaign, term):
    old_dict = {'source': source, 'medium': medium, 'campaign': campaign, 'term': term}
    del old_dict['term']
    print old_dict
    print new_dict
    assert new_dict == old_dict


def test_one(source, medium, campaign, term):
    generated_url = generate_url(source, medium, campaign, term)
    derived_url = derive_url(generated_url)
    new_dict = breakout_utm_param_values(derived_url)
    assert_good(new_dict, source, medium, campaign, term)

test_one("google", "paidsearch", "Fake%20campaign", "test term")


driver.quit()
