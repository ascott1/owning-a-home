# coding: utf-8
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.base import Base

# ELEMENT ID'S FOR TEXTBOXES
DOWN_PAYMENT_AMOUNT_TBOX = "down-payment"  # DOWN PAYMENT AMOUNT TEXTBOX
DOWN_PAYMENT_PERCENT = "percent-down"  # DOWN PAYMENT PERCENTAGE TEXTBOX
HOUSE_PRICE_TBOX = "house-price"  # HOUSE PRICE TEXTBOX

# ELEMENT ID'S FOR DROP DOWN LISTS
ARM_TYPE_DDL = "arm-type"  # ARM TYPE DROPDOWN LIST
LOAN_TERM_DDL = "loan-term"  # LOAN TERM DROPDOWN LIST
LOAN_TYPE_DDL = "loan-type"  # LOAN TYPE DROPDOWN LIST
LOCATION_DDL = "location"  # LOCATION DROPDOWN LIST
RATE_STRUCTURE_DDL = "rate-structure"  # RATE STRUCTURE DROPDOWN LIST
COUNTY_DLL = "county"

# ELEMENT ID'S FOR LABELS/WARNINGS
LOAN_AMOUNT_LABEL = "loan-amount-result"  # LOAN AMOUNT LABEL
COUNTY_WARNING = "#county-warning .warning-text"
HB_WARNING = "#hb-warning .warning-text"

# This label displays range as 700 - 720
SLIDER_RANGE_LABEL = "slider-range"

# CSS SELECTORS
COUNTY_HIDDEN = ".col-7.county.hidden"

# XPATH LOCATORS
RATE_LOCATION = "//h2/*[@class ='location']"
SLIDER_HANDLE = "//div[contains(@class, 'rangeslider__handle')]"
SLIDER = "//div[@class = 'rangeslider']"
RANGE_ALERT = "//div[@class='result-alert credit-alert']/p"


class RateChecker(Base):

    def __init__(self, logger, directory, base_url=r'http://localhost/',
                 driver=None, driver_wait=10, delay_secs=0):
        super(RateChecker, self).__init__(logger, directory, base_url,
                                          driver, driver_wait, delay_secs)
        self.logger = logger
        self.driver_wait = driver_wait

    # ALERTS
    def get_warning_button_class(self):
        element = self.driver.find_element_by_xpath(SLIDER_HANDLE)
        return element.get_attribute("class")

    def get_range_alert_text(self):
        l_wait = 5
        msg = 'Alert was not visible within %s seconds' % l_wait

        try:
            element = self.driver.find_element_by_xpath(RANGE_ALERT)
            return element.get_attribute("textContent")
        except NoSuchElementException:
            return False

    def get_county_alert_text(self, alert_text):
        l_wait = 5
        msg = 'County alert text was not visible within %s seconds' % l_wait

        try:
            WebDriverWait(self.driver, l_wait)\
                .until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,
                       COUNTY_WARNING), alert_text), msg)
            return True
        except TimeoutException:
            return False

    def get_hb_alert_text(self, alert_text):
        l_wait = 5
        msg = 'HB alert text was not visible within %s seconds' % l_wait

        try:
            WebDriverWait(self.driver, l_wait)\
                .until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,
                       HB_WARNING), alert_text), msg)
            return True
        except TimeoutException:
            return False

    # CHART AREA
    def get_chart_location(self):
        # This label is invisible on page load
        # We wait for the element to become visible before extracting the text
        l_wait = 30
        msg = 'Location was not visible within %s seconds' % l_wait
        WebDriverWait(self.driver, l_wait)\
            .until(EC.visibility_of_element_located((By.XPATH,
                                                    RATE_LOCATION)), msg)

        element = self.driver.find_element_by_xpath(RATE_LOCATION)
        return element.text

    # CREDIT SCORE RANGE
    def get_credit_score_range(self):
        element = self.driver.find_element_by_id(SLIDER_RANGE_LABEL)
        # Return the entire text of the credit score range
        return element.text

    def set_credit_score_range(self, slider_direction):
        actions = ActionChains(self.driver)
        # Get the pixel width of the slider control
        slider_element = self.driver.find_element_by_xpath(SLIDER)
        slider_width = int(slider_element.get_attribute("scrollWidth"))

        self.logger.info("width: %s" % slider_width)

        element = self.driver.find_element_by_xpath(SLIDER_HANDLE)

        # Move the slider 1/4 of the total width to the right
        if(slider_direction == "right"):
            xOffset = (slider_width/4)
        # Move the slider 1/4 of the total width to the left
        elif(slider_direction == "left"):
            xOffset = (slider_width/-4)
        # Move the slider 1/2 of the total width to the left
        elif(slider_direction == "lowest"):
            xOffset = (slider_width/-2)
        # Move the slider 1/2 of the total width to the right
        elif(slider_direction == "highest"):
            xOffset = (slider_width/2)

        actions.click_and_hold(element)
        actions.move_by_offset(xOffset, 0)
        actions.release()
        actions.perform()

    # LOCATION
    def get_location(self):
        # Wait for the Geolocator to display the location above the chart
        WebDriverWait(self.driver, self.driver_wait)\
            .until(EC.visibility_of_element_located((By.XPATH, RATE_LOCATION)))

        # Get the selected Index from the Location dropdown list
        element = Select(self.driver.find_element_by_id(LOCATION_DDL))
        option = element.first_selected_option

        # Then Get the corresponding text from the selected Index
        return option.get_attribute('text')

    def set_location(self, state_name):
        select = Select(self.driver.find_element_by_id(LOCATION_DDL))
        select.select_by_visible_text(state_name)

    # HOUSE PRICE
    def get_house_price(self):
        element = self.driver.find_element_by_id(HOUSE_PRICE_TBOX)

        # If the textbox is empty then return the placeholder amount
        if (element.get_attribute("value") == ''):
            return element.get_attribute("placeholder")
        else:
            # Return the value attribute from the House Price textbox
            return element.get_attribute("value")

    def set_house_price(self, house_price):
        # Clear any existing text
        script = "document.getElementById('house-price').value=''"
        self.driver.execute_script(script)
        element = self.driver.find_element_by_id(HOUSE_PRICE_TBOX)
        element.clear()
        element.send_keys(house_price)

    # DOWN PAYMENT PERCENT
    def get_down_payment_percent(self):
        element = self.driver.find_element_by_id(DOWN_PAYMENT_PERCENT)

        # If the textbox is empty then return the placeholder value
        if (element.get_attribute("value") == ''):
            return element.get_attribute("placeholder")
        else:
            # Return the value attribute from the Down Payment % textbox
            return element.get_attribute("value")

    def set_down_payment_percent(self, down_payment):
        # Clear any existing text
        s = "document.getElementById('" + DOWN_PAYMENT_PERCENT + "').value=''"
        self.driver.execute_script(s)

        # Set the value using jscript
        # This is done because the down payment percent control
        # updates on every keystroke sent
        script = "document.getElementById('" + DOWN_PAYMENT_PERCENT + \
            "').value='" + down_payment + "'"
        self.driver.execute_script(script)

        # Press the ENTER key to trigger the onchange event
        element = self.driver.find_element_by_id(DOWN_PAYMENT_PERCENT)
        element.send_keys(Keys.ENTER)

    # DOWN PAYMENT AMOUNT
    def get_down_payment_amount(self):
        element = self.driver.find_element_by_id(DOWN_PAYMENT_AMOUNT_TBOX)

        # If the textbox is empty then return the placeholder amount
        if (element.get_attribute("value") == ''):
            return element.get_attribute("placeholder")
        else:
            # Return the value attribute from the Down Payment textbox
            return element.get_attribute("value")

    def set_down_payment_amount(self, down_payment):
        # Clear any existing text
        script = "document.getElementById('down-payment').value=''"
        self.driver.execute_script(script)
        element = self.driver.find_element_by_id(DOWN_PAYMENT_AMOUNT_TBOX)
        element.clear()
        element.send_keys(down_payment)

    # LOAN AMOUNT
    def get_loan_amount(self):
        # Get the text from the Loan Amount label
        element = self.driver.find_element_by_id(LOAN_AMOUNT_LABEL)
        return element.text

    # COUNTY
    def is_county_visible(self):
        try:
            self.driver.find_element_by_css_selector(COUNTY_HIDDEN)
            return False
        except NoSuchElementException:
            return True

    def set_county(self, county_name):
        l_wait = 5
        msg = '%s not found after %s seconds' % (county_name, l_wait)

        # Wait for the dropdown list to be populated with county_name
        # before making a selection
        WebDriverWait(self.driver, l_wait)\
            .until(EC.text_to_be_present_in_element((By.ID,
                   COUNTY_DLL), county_name), msg)

        select = Select(self.driver.find_element_by_id(COUNTY_DLL))
        select.select_by_visible_text(county_name)

    # RATE STRUCTURE
    def get_rate_structure(self):
        # First Get the selected Index from the Location dropdown list
        element = Select(self.driver.find_element_by_id(RATE_STRUCTURE_DDL))
        option = element.first_selected_option

        # Then Get the corresponding text from the selected Index
        return option.get_attribute('text')

    def set_rate_structure(self, rate_selection):
        element = Select(self.driver.find_element_by_id(RATE_STRUCTURE_DDL))
        element.select_by_visible_text(rate_selection)

    # LOAN TERM
    def get_loan_term(self):
        # First Get the selected Index from the Loan Term dropdown list
        element = Select(self.driver.find_element_by_id(LOAN_TERM_DDL))
        option = element.first_selected_option

        # Then Get the corresponding text from the selected Index
        return option.get_attribute('text')

    def set_loan_term(self, number_of_years):
        element = Select(self.driver.find_element_by_id(LOAN_TERM_DDL))
        element.select_by_visible_text(number_of_years)

    def is_loan_term_option_enabled(self, loan_term):
        e_xpath = "//select[@id='" + LOAN_TERM_DDL + \
            "']/option[text()='" + loan_term + "']"
        element = self.driver.find_element_by_xpath(e_xpath)

        # If the option is enabled, the disabled attribute returns None
        if (element.get_attribute('disabled') is None):
            return 'enabled'
        # If the option is disabled, the disabled attribute returns true
        elif (element.get_attribute('disabled') == 'true'):
            return 'disabled'
        else:
            return element.get_attribute('disabled')

    # LOAN TYPE
    def get_selected_loan_type(self):
        # First Get the selected Index from the Loan Type dropdown list
        element = Select(self.driver.find_element_by_id(LOAN_TYPE_DDL))
        option = element.first_selected_option

        # Then Get the corresponding text from the selected Index
        return option.get_attribute('text')

    def set_loan_type(self, loan_type):
        element = Select(self.driver.find_element_by_id(LOAN_TYPE_DDL))
        element.select_by_visible_text(loan_type)

    def is_loan_type_option_enabled(self, loan_type):
        e_xpath = "//select[@id='" + LOAN_TYPE_DDL + \
            "']/option[text()='" + loan_type + "']"
        element = self.driver.find_element_by_xpath(e_xpath)

        # If the option is enabled, the disabled attribute returns None
        if (element.get_attribute('disabled') is None):
            return 'enabled'
        # If the option is disabled, the disabled attribute returns true
        elif (element.get_attribute('disabled') == 'true'):
            return 'disabled'
        else:
            return element.get_attribute('disabled')

    # ARM TYPE
    def get_arm_type(self):
        # First Get the selected Index from the Loan Type dropdown list
        element = Select(self.driver.find_element_by_id(ARM_TYPE_DDL))
        option = element.first_selected_option

        # Then Get the corresponding text from the selected Index
        return option.get_attribute('text')

    def set_arm_type(self, arm_type):
        element = Select(self.driver.find_element_by_id(ARM_TYPE_DDL))
        element.select_by_visible_text(arm_type)

    # TABS AND LINKS
    def get_active_tab_text(self):
        element = self.driver.find_element_by_css_selector(".active-tab a")
        return element.text

    def click_link_by_text(self, link_name):
        element = self.driver.find_element_by_link_text(link_name)
        element.click()

    # INTEREST COST OVER YEARS
    def get_primary_interest_rate(self, ordinal, years):
        e_xpath = "//div[contains(@class,'interest-cost-primary')]" + \
            "/h5/span[text()=" + years + "]"
        m = 'Element %s not found after %s secs' % (e_xpath, self.driver_wait)

        # Wait for the label to update itself
        WebDriverWait(self.driver, self.driver_wait)\
            .until(EC.text_to_be_present_in_element((By.XPATH,
                                                    e_xpath), years), m)
        # Return the text from either the First or Second column
        # based on the ordinal passed
        element = self.driver.find_elements_by_xpath(e_xpath)
        return element[ordinal].text

    def get_secondary_interest_rate(self, ordinal, years):
        e_xpath = "//div[contains(@class,'interest-cost-secondary')]" + \
            "/h5/span[text()=" + years + "]"
        m = 'Element %s not found after %s secs' % (e_xpath, self.driver_wait)

        # Wait for the label to update itself
        WebDriverWait(self.driver, self.driver_wait)\
            .until(EC.text_to_be_present_in_element((By.XPATH,
                                                    e_xpath), years), m)
        # Return the text from either the First or Second column
        # based on the ordinal passed
        element = self.driver.find_elements_by_xpath(e_xpath)
        return element[ordinal].text
