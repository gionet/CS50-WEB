from django.test import TestCase, Client
from .models import Posts, User
import os
import pathlib
import unittest
import time 

from django.contrib.auth import get_user_model

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

class CustomUserTests(TestCase):
    
    def test_create_user(self):
        User = get_user_model()
        p1 = User.objects.create_user(
            username='gionet',
            email='gionet@gmail.com',
            password='gionet'
        )
        self.assertEqual(p1.username, 'gionet')
        self.assertEqual(p1.email, 'gionet@gmail.com')

# Finds the Uniform Resourse Identifier of a file
def file_uri(filename):
    return pathlib.Path(os.path.abspath(filename)).as_uri()

# Sets up web driver using Google chrome
driver = webdriver.Chrome()

# Standard outline of testing class
page = 'http://127.0.0.1:8000/'

class WebpageTests(unittest.TestCase):
    
    def test_title(self):
        driver.get(page)
        expected_title = "TimeStamp"
        self.assertEqual(driver.title, expected_title)
        
    def test_register_password_mismatch(self):
        driver.get(page + '/register')
        username = driver.find_element(By.NAME, "username")
        username = username.send_keys("test")
        
        email = driver.find_element(By.NAME, "email")
        email = email.send_keys("test@testing.com")
        
        password = driver.find_element(By.NAME, "password")
        password = password.send_keys('testing')
        
        confirmation = driver.find_element(By.NAME, "confirmation")
        confirmation = confirmation.send_keys("test")
        
        register = driver.find_element(By.NAME, "register")
        register.click()

        message_element = driver.find_element(By.ID, "message")
        expected_url = page + 'register'
        
        self.assertEqual(driver.current_url, expected_url)
        self.assertEqual(message_element.text, "Passwords must match.")
        
    def test_tick_button(self):
        driver.get(page)
        move = driver.find_element(By.ID, "addToDoListButton")
        move.click()
        inputBox = driver.find_element(By.ID, "addToDoListInput")
        user_input = "hello"
        
        inputBox.send_keys(user_input)
        inputBox.send_keys(Keys.ENTER)
        time.sleep(1)
        rows = driver.find_element(By.CSS_SELECTOR, '.table-hover tr[data-id]')
        largest_id = None
        highest_row = None
        
        dataset_id = int(rows.get_attribute('data-id'))
        
        if largest_id is None or dataset_id > largest_id:
            largest_id = dataset_id
            # highest_row = row
                
        # if highest_row is not None:
        #     userInput = 
        userInput = rows.find_element(By.CSS_SELECTOR, 'td:nth-child(2)')
                
        self.assertEqual(userInput.text, user_input)
        

if __name__ == "__main__":
    unittest.main()