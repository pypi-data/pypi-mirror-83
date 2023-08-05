def write_to_element_js(driver, element_xpath, input_string):
    """ Function to bypass the send_keys method in selenium when it doesn't work properly.
    Uses JS to do it.
    Found this code by Philipp Doerner in this link: https://stackoverflow.com/questions/18013821/pythons-selenium-send-keys-with-chrome-driver-drops-characters/62135696#62135696
    """
    
    js_command = f'document.evaluate(\'{element_xpath}\', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.value = \'{input_string}\';'
    driver.execute_script(js_command)

def write_to_element(driver, element_xpath, input_string, use_js = True):
    """Giving the choice to use the js or the native selenium methods.

    """
    if(use_js):
        write_to_element_js(driver, element_xpath, input_string)
    else:
        driver.find_element_by_xpath(element_xpath).send_keys(input_string)