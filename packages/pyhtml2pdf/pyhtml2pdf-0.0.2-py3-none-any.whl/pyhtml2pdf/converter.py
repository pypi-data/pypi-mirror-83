import sys
import json
import base64

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import staleness_of
from webdriver_manager.chrome import ChromeDriverManager

from .compressor import __compress


def convert(source: str, target: str, timeout: int = 2, compress: bool = False, power: int = 0):
    '''
    Convert a given html file or website into PDF

    :param str source: source html file or website link
    :param str target: target location to save the PDF
    :param int timeout: timeout in seconds. Default value is set to 2 seconds
    :param bool compress: whether PDF is compressed or not. Default value is False
    :param int power: power of the compression. Default value is 0. This can be 0: default, 1: prepress, 2: printer, 3: ebook, 4: screen
   '''

    result = __get_pdf_from_html(source, timeout)

    if compress:
        __compress(result, target, power)
    else:
        with open(target, 'wb') as file:
            file.write(result)

def __send_devtools(driver, cmd, params={}):
    resource = "/session/%s/chromium/send_command_and_get_result" % driver.session_id
    url = driver.command_executor._url + resource
    body = json.dumps({'cmd': cmd, 'params': params})
    response = driver.command_executor._request('POST', url, body)

    if not response:
        raise Exception(response.get('value'))

    return response.get('value')


def __get_pdf_from_html(path: str, timeout: int, print_options={}):
    webdriver_options = Options()
    webdriver_options.add_argument('--headless')
    webdriver_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=webdriver_options)

    driver.get(path)

    try:
       WebDriverWait(driver, timeout).until(staleness_of(driver.find_element_by_tag_name('html')))
    except TimeoutException:
        calculated_print_options = {
            'landscape': False,
            'displayHeaderFooter': False,
            'printBackground': True,
            'preferCSSPageSize': True,
        }
        calculated_print_options.update(print_options)
        result = __send_devtools(driver, "Page.printToPDF", calculated_print_options)
        driver.quit()
        return base64.b64decode(result['data'])
