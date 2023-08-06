# SPDX-FileCopyrightText: 2020 2020
#
# SPDX-License-Identifier: Apache-2.0

import time
from ..base_component import Selector
from .base_control import BaseControl
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class OAuthSelect(BaseControl):
    """
    Entity-Component: OAuthSelect
    OAuthSelect Javascript framework: OAuthSelect
    A dropdown which can select only one value
    """
    def __init__(self, browser, container, searchable=True):
        """
            :param browser: The selenium webdriver
            :param container: The locator of the container where the control is located in. 
        """

        super(OAuthSelect, self).__init__(browser, container)
        self.elements.update({
            "values": Selector(select=container.select + " option")
        })

    def select(self, value, open_dropdown=True):
        if open_dropdown:
            self.container.click()
        for each in self.get_elements('values'):
            if each.text.strip().lower() == value.lower():
                each.click()
                return True
        else:
            raise ValueError("{} not found in select list".format(value))

    def get_value(self):
        """
            Gets the selected value
        """
        try:
            return self.container.get_attribute('value').strip()
        except:
            return ''

    def list_of_values(self):
        """
            Gets the list of value from the Single Select
        """
        selected_val = self.get_value()
        self.container.click()
        first_element = None
        list_of_values = []
        for each in self.get_elements('values'):
            list_of_values.append(each.text.strip())
        return list_of_values    