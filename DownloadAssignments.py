#! /usr/bin/env python2

import os
try:
    from itertools import zip_longest
except ImportError:
    from itertools import izip_longest as zip_longest
from time import sleep, strftime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import (UnexpectedTagNameException,
                                       WebDriverException,
                                       NoSuchElementException)

LAB_LINK_TEXT = "CS2501 Lab for CS 2500 - All Sections - Fall 2015"
GRADE_CENTER_TEXT = "Full Grade Center"
LOGIN_PAGE = "https://blackboard.neu.edu"

def formatted(text):
    now = strftime("%Y-%m-%d %H:%M:%S")
    return "["+now+"] "+ text

def fail(text):
    print('\033[91m'+formatted(text)+'\033[0m')

def success(text):
    print('\033[92m'+formatted(text)+'\033[0m')

def grouper(iterable, n, fillvalue=None):
    "Given an iterable, returns an iterable with sub-lists with a length of n"
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def get_login_credentials(file_name):
    """
    Retrieves the login credentials from the given file.
    The file should be formatted so that the first line contains the username
    and the second should contain the password (plaintext).
    """
    assert os.path.exists(file_name), "{} does not exist!".format(file_name)
    with open(file_name, "r") as login_file:
        contents = login_file.readlines()
    username, password = contents
    return username.strip(), password.strip()

def login(username, password):
    """
    Using the given username and password, logs into MyNEU through a
    selenium driver (firefox). Returns the driver object
    """
    opts = Options()
    opts.add_argument("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36")

    driver = webdriver.Chrome(chrome_options=opts)
    # Go to the login page
    login_page = driver.get(LOGIN_PAGE)

    # Find the user and password forms
    user_form = driver.find_element_by_id("username")
    pass_form = driver.find_element_by_id("password")

    # Login in with the given credentias
    user_form.send_keys(username)
    pass_form.send_keys(password)

    # Click the login button
    #button_class = driver.find_element_by_class_name("buttons")
    button = driver.find_element_by_class_name("btn-submit")
    button.click()

    # Return the driver so we can do more with it
    return driver

def navigate_to_lab_page(driver):
    """Navigates the driver to the lab page, assuming we are on the
    home page for blackboard.neu.edu"""
    assert "Blackboard Learn" in driver.title, "Not on main blackboard site!"
    link = driver.find_element_by_link_text(LAB_LINK_TEXT)
    link.click()

def navigate_to_grade_page(driver):
    """Navigates the driver to the main users, assuming we are
    on the 2501 Lab page on blackboard.neu.edu"""
    assert "CS2501" in driver.title, "Not on CS2501 Lab section on blackboard.neu.edu!"
    try:
        link = driver.find_element_by_link_text(GRADE_CENTER_TEXT)
    # If the link is hidden because the Grade Center tab on the left is hidden
    except NoSuchElementException as e:
        # Open it
        driver.find_element_by_partial_link_text("Grade Center").click()
        sleep(1)
        link = driver.find_element_by_link_text(GRADE_CENTER_TEXT)
    link.click()

def navigate_to_jump_to(driver):
    """Navigates the browser so that we can use the jump to button
    Assumes we are on the Grade Center page"""
    assert "Grade Center" in driver.title, "Not on the Grade Center page for CS2501 Lab!"
    table = get_table(driver)
    # Need to move the mouse
    action = webdriver.ActionChains(driver)
    # Get the cell (second cause shenanigans)
    cell = driver.find_element_by_id("cell_1_6")
    # Hover over the cell so we can find that drop-down menu
    action.move_to_element(cell)
    action.perform()
    drop_down = cell.find_element_by_id("cmlink_16").click()
    # Find the view grade details and click
    cell.find_element_by_xpath('//*[@title="View Grade Details"]').click()


def get_table(driver):
    """Gets the main grader table, assumes we are on the grade center page"""
    assert "Grade Center" in driver.title, "Not on the main grade center page for CS2501 Lab!"
    return driver.find_elements_by_class_name("gbtable")


def find_user_with_ps(driver, full_name, ps_num):
    """Searches the user list using the jump to button. Assuming on any
    "Grade Details" page. The name should be at least the first name,
    since it basically types it into the user box. It is VERY lazy.

    I.E: If you type "aoeu", it wil grab the first name that satisfies
    at least part of that (so that could mean the first name in the
    non-alphabatised list that starts with a)

    The problem set should be just a number, int is fine. Start with the
    first one as 1"""
    assert "Grade Details" in driver.title, "Not on a Grade Details page!"
    # Open jump to page
    driver.find_element_by_xpath('//*[@title="Jump to..."]').click()
    # Get the User Selection box
    user_menu = driver.find_element_by_id("userSelect")
    user_menu.click()
    # Kay, now we start typing in the name, then click
    user_menu.send_keys(full_name)
    user_menu.click()

    # Kay, now we gotta select the right problem set
    column_menu = driver.find_element_by_id("itemSelect")
    column_menu.click()
    # Formatting for PS {number}
    column_menu.send_keys("PS {}".format(ps_num))
    column_menu.click()

    # Then hit go
    driver.find_element_by_id("jumpToButton").click()

def download_hw(driver):
    """Assumes we are on a page that find_user_with_ps woul
    navigate to for you"""
    # What a horrible one-liner, I'm so sorry
    driver.find_element_by_class_name("vtbegenerated").find_element_by_tag_name("a").click()

def test():
    username, password = get_login_credentials("creds.txt")
    driver = login(username, password)
    try:
        # Make these return the urls of where we should be?
        # So we can wait? Or maybe just a string...
        sleep(5)
        print("Should be on first page!")

        navigate_to_lab_page(driver)
        sleep(5)
        print("Should be on second page!")

        navigate_to_grade_page(driver)
        sleep(5)
        print("Should be on third page!")

        navigate_to_jump_to(driver)
        sleep(2)
        print("Should be on fourth page!")
        # Just a test person
        find_user_with_ps(driver, "Khyati Singh", 4)
        sleep(5)
        print("Should be on last page!")
        download_hw(driver)
        sleep(1)
    finally:
        pass
        #driver.quit()

def main():
    import sys
    assert len(sys.argv) == 3, (
    "Need to specify two things: file name full of names, and the problem set to fetch")
    FAILURES = 0
    PROBLEM_SET_NUM = sys.argv[2]
    NAME_FILE = sys.argv[1]
    NAMES = []
    with open(NAME_FILE, "r") as name_file:
        for line in name_file.readlines():
            NAMES.append(line.strip())
    TOTAL_USERS = len(NAMES)
    username, password = get_login_credentials("creds.txt")
    driver = login(username, password)
    sleep(2)
    try:
        # Setup
        sleep(7)

        navigate_to_lab_page(driver)
        sleep(5)

        navigate_to_grade_page(driver)
        sleep(5)

        navigate_to_jump_to(driver)
        sleep(2)

        for name in NAMES:
            find_user_with_ps(driver, name, PROBLEM_SET_NUM)
            sleep(5)
            # Try everything to get hw, if can't find, print and continue
            try:
                download_hw(driver)
            # Yeah, yeah bad practice
            except Exception:
                fail("Couldn't find {}'s homework!".format(name))
                FAILURES += 1
            else:
                success("Downloaded {}'s homework".format(name))
            sleep(1)
        print(("Done! Processed \033[94m{} \033[0musers, "
               "with \033[91m{} \033[0mfailures").format(TOTAL_USERS,
                   FAILURES))
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
