# SPDX-FileCopyrightText: 2020 2020
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import print_function
from __future__ import absolute_import
from builtins import str
from builtins import zip
from .base_component import BaseComponent, Selector
from .dropdown import Dropdown
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import re
import time
import copy
from selenium.common import exceptions

class Table(BaseComponent):
    """
    Component: Table
    Base class of Input & Configuration table
    """
    def __init__(self, browser, container, mapping=dict(),wait_for_seconds = 10):
        """
            :param browser: The selenium webdriver
            :param container: Container in which the table is located. Of type dictionary: {"by":..., "select":...}
            :param mapping= If the table headers are different from it's html-label, provide the mapping as dictionary. For ex, {"Status": "disabled"}
        """
        
        super(Table, self).__init__(browser, container)
        self.header_mapping = mapping
        
        self.elements.update({
            "rows": Selector(select=container.select + " tr.apps-table-tablerow"),
            "header": Selector(select=container.select + " th"),
            "app_listings": Selector(select=container.select + " tbody.app-listings"),
            "action_values": Selector(select=container.select + " td.col-actions a"),
            "col": Selector(select=container.select + " td.col-{column}"),
            "col-number": Selector(select=container.select + " td:nth-child({col_number})"),
            "edit": Selector(select="a.edit"),
            "clone": Selector(select="a.clone"),
            "delete": Selector(select="a.delete"),
            "delete_prompt": Selector(select=".modal-dialog div.delete-prompt"),
            "delete_btn": Selector(select=".modal-dialog .submit-btn"),
            "delete_cancel": Selector(select=".modal-dialog .cancel-btn"),
            "delete_close": Selector(select=".modal-dialog button.close"),
            "delete_loading": Selector(select=".modal-dialog .msg-loading"),
            "waitspinner": Selector(select=container.select + " div.shared-waitspinner"),
            "count": Selector(select=container.select +" .shared-collectioncount"),
            "filter": Selector(select=container.select + " input.search-query"),
            "filter_clear": Selector(select=container.select + " a.control-clear"),
            "more_info": Selector(select=container.select + " td.expands"),
            "more_info_row": Selector(select=container.select + " tr.expanded + tr"),
            "more_info_key": Selector(select="dt"),
            "more_info_value":Selector(select="dd"),
            "switch_to_page": Selector(select=container.select + " .pull-right li a")
        })
        self.wait_for_seconds = wait_for_seconds

    def get_count_title(self):
        """
        Get the count mentioned in the table title
        """
        return self.get_clear_text(self.count) 

    def get_row_count(self):
        """
        Count the number of rows in the page.
        """
        return len(list(self._get_rows()))

    def get_headers(self):
        """
        Get list of headers from the table
        """
        return [self.get_clear_text(each) for each in self.get_elements("header")]

    def get_sort_order(self):
        """
        Get the column-header which is sorted rn.
        Warning: It depends on the class of the headers and due to it, the returned result might give wrong answer.
        :returns : a dictionary with the "header" & "ascending" order
        """
        for each_header in self.get_elements("header"):
            if re.search(r"\basc\b", each_header.get_attribute("class")):
                return {
                    "header": self.get_clear_text(each_header),
                    "ascending": True
                }
            elif re.search(r"\bdesc\b", each_header.get_attribute("class")):
                return {
                    "header": self.get_clear_text(each_header),
                    "ascending": False
                }

    def sort_column(self, column, ascending=True):
        """
        Sort a column in ascending or descending order
            :param column: The header of the column which should be sorted
            :param ascending: True if the column should be sorted in ascending order, False otherwise
        """
        for each_header in self.get_elements("header"):
            
            if self.get_clear_text(each_header).lower() == column.lower():
                if "asc" in each_header.get_attribute("class") and ascending:
                    # If the column is already in ascending order, do nothing
                    return
                elif "asc" in each_header.get_attribute("class") and not ascending:
                    # If the column is in ascending order order and we want to have descending order, click on the column-header once
                    each_header.click()
                    self._wait_for_loadspinner()
                    return
                elif "desc" in each_header.get_attribute("class") and not ascending:
                    # If the column is already in descending order, do nothing
                    return
                elif "desc" in each_header.get_attribute("class") and ascending:
                    # If the column is in descending order order and we want to have ascending order, click on the column-header once
                    each_header.click()
                    self._wait_for_loadspinner()
                    return
                else:
                    # The column was not sorted before
                    if ascending:
                        # Click to sort ascending order
                        each_header.click()
                        self._wait_for_loadspinner()
                        return
                    else:
                        # Click 2 times to sort in descending order

                        #Ascending
                        each_header.click()
                        self._wait_for_loadspinner()
                        #Decending
                        # The existing element changes (class will be changed), hence, it can not be referenced again.
                        # So we need to get the headers again and do the same process.
                        self.sort_column(column, ascending=False)
                        return
        

    def _wait_for_loadspinner(self):
        """
        There exist a loadspinner when sorting/filter has been applied. This method will wait until the spinner is dissapeared 
        """
        try:
            self.wait_for("waitspinner", timeout=5)
            self.wait_until("waitspinner")
        except:
            print("Waitspinner did not appear")

    def wait_for_rows_to_appear(self, row_count=1):
        """
        Wait for the table to load row_count rows
            :param row_count: number of row_count to wait for. 
        """
        def _wait_for_rows_to_appear(driver):
            return self.get_row_count() >= row_count
        self.wait_for(_wait_for_rows_to_appear, msg="Expected rows : {} to be greater or equal to {}".format(row_count, self.get_row_count()))

    def wait_for_column_to_appear(self, column_name):
        """
        Wait for the table to load the column with the given column name.
            :param column_name: Name of the column to wait for.
        """
        def _wait_for_column_to_appear(driver):
            return column_name in self.get_headers()
        self.wait_for(_wait_for_column_to_appear, msg="Column {} not found in the table".format(column_name))

    def get_table(self):
        """
        Get whole table in dictionary form. The row_name will will be the key and all header:values will be it's value.
        {row_1 : {header_1: value_1, . . .}, . . .}
        """

        table = dict()
        headers = list(self.get_headers())

        for each_row in self._get_rows():
            row_name = self._get_column_value(each_row, "name")
            table[row_name] = dict()
            for each_col in headers:
                each_col = each_col.lower()
                if each_col:
                        table[row_name][each_col] = self._get_column_value(each_row, each_col) 
        return table

    def get_cell_value(self, name, column):
        """
        Get a specific cell value.
            :param name: row_name of the table
            :param column: column header of the table
        """
        _row = self._get_row(name)
        return self._get_column_value(_row, column)
    
    def get_column_values(self, column):
        """
        Get list of values of  column
            :param column: column header of the table
        """
        value_list = []
        for each_row in self._get_rows():
            value_list.append(self._get_column_value(each_row, column))
        return value_list


    def get_list_of_actions(self, name):
        """
        Get list of possible actions for a specific row
        :param name: The name of the row
        """
        _row = self._get_row(name)
        _row.find_element(*list(self.elements["action_values"]._asdict().values()))
        return [self.get_clear_text(each_element) for each_element in self.get_elements("action_values")]

    def edit_row(self, name):
        """
        Edit the specified row. It will open the edit form(entity). The opened entity should be interacted with instance of entity-class only.
            :param name: row_name of the table
        """
        _row = self._get_row(name)
        _row.find_element(*list(self.elements["edit"]._asdict().values())).click()

    def clone_row(self, name):
        """
        Clone the specified row. It will open the edit form(entity). The opened entity should be interacted with instance of entity-class only.
            :param name: row_name of the table
        """
        _row = self._get_row(name)
        _row.find_element(*list(self.elements["clone"]._asdict().values())).click()

    def delete_row(self, name, cancel=False, close=False, prompt_msg=False):
        """
        Delete the specified row. Clicking on delete will open a pop-up. Delete the row if neither of (cancel, close) specified.
            :param name: row_name of the table
            :param cancel: if provided, after the popup is opened, click on cancel button and Do Not delete the row
            :param close:  if provided, after the popup is opened, click on close button and Do Not delete the row
        """

        # Click on action
        _row = self._get_row(name)
        _row.find_element(*list(self.elements["delete"]._asdict().values())).click()        

        self.wait_for("delete_prompt")
        if cancel:
            self.delete_cancel.click()
            self.wait_until("delete_cancel")
            return True
        elif close:
            self.delete_close.click()
            self.wait_until("delete_close")
            return True  
        elif prompt_msg:
            self.wait_for_text("delete_prompt")
            return self.get_clear_text(self.delete_prompt)  
        else:
            self.delete_btn.click()
            self.wait_for("app_listings")
            
            
    def set_filter(self, filter_query):
        """
        Provide a string in table filter.
            :param filter_query: query of the filter
            :returns : resultant list of filtered row_names
        """
        self.filter.clear()
        self.filter.send_keys(filter_query)
        self._wait_for_loadspinner()
        return self.get_column_values("name")

    def clean_filter(self):
        """
        Clean the filter textbox
        """
        self.filter.clear()
        self._wait_for_loadspinner()

    def _get_column_value(self, row, column):
        """
        Get the column from a specific row provided.
        :param row: the webElement of the row
        :param column: the header name of the column
        """
        find_by_col_number = False
        if column.lower().replace(" ","_") in self.header_mapping:
            column = self.header_mapping[column.lower().replace(" ","_")]
            find_by_col_number = isinstance(column, int)
        else:
            column=column.lower().replace(" ","_")

        if not find_by_col_number:
            col = copy.deepcopy(self.elements["col"])
            col = col._replace(select=col.select.format(column=column))
            self.wait_for("app_listings")
            return self.get_clear_text(row.find_element(*list(col._asdict().values())))
        else:
            # Int value 
            col = copy.deepcopy(self.elements["col-number"])
            col = col._replace(select=col.select.format(col_number=column))
            self.wait_for("app_listings")
            return self.get_clear_text(row.find_element(*list(col._asdict().values())))
            
    def _get_rows(self):
        """
        Get list of rows
        """
        for each_row in self.get_elements("rows"):
            yield each_row

    def _get_row(self, name):
        """
        Get the specified row.
        :param name: row name 
        """
        for each_row in self._get_rows():
            if self._get_column_value(each_row, "name") == name:
                return each_row
        else:
            raise ValueError("{} row not found in table".format(name)) 

    def get_action_values(self, name):
        _row = self._get_row(name)
        return [self.get_clear_text(each) for each in self.get_elements("action_values")]

    def get_count_number(self):
        row_count = self.get_count_title()
        return int(re.search(r'\d+', row_count).group())

    def get_more_info(self, name, cancel=True):
        _row = self._get_row(name)
        _row.find_element(*list(self.elements["more_info"]._asdict().values())).click()
        keys = self.more_info_row.find_elements(*list(self.elements["more_info_key"]._asdict().values()))
        values = self.more_info_row.find_elements(*list(self.elements["more_info_value"]._asdict().values()))        
        more_info = {self.get_clear_text(key): self.get_clear_text(value) for key, value in zip(keys, values)}

        if cancel:
            _row = self._get_row(name)
            _row.find_element(*list(self.elements["more_info"]._asdict().values())).click()

        return more_info

    def switch_to_page(self, value):
        for each in self.get_elements('switch_to_page'):
            if self.get_clear_text(each).lower() not in ['prev','next'] and self.get_clear_text(each) == str(value):
                each.click()
                return True
        else:
            raise ValueError("{} not found".format(value))

    def switch_to_prev(self):
        for page_prev in self.get_elements('switch_to_page'):
            if self.get_clear_text(page_prev).lower() == "prev":
                page_prev.click()
                return True
        else:
            raise ValueError("{} not found".format(page_prev))

    def switch_to_next(self):
        for page_next in self.get_elements('switch_to_page'):
            if self.get_clear_text(page_next).lower() == "next":
                page_next.click()
                return True
        else:
            raise ValueError("{} not found".format(page_next))

        
