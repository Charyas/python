#coding=utf-8

from appium import webdriver

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '4.2.2'
desired_caps['deviceName'] = 'Android Emulator'
desired_caps['appPackage'] = 'com.android.calculator2'
desired_caps['appActivity'] = '.Calculator'

driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

driver.find_element_by_android_uiautomator('new UiSelector().text("1")').click()
# driver.find_element_by_name("5").click()
# driver.find_element_by_name("9").click()
# driver.find_element_by_name("delete").click()
# driver.find_element_by_name("9").click()
# driver.find_element_by_name("5").click()
# driver.find_element_by_name("+").click()
# driver.find_element_by_name("6").click()
# driver.find_element_by_name("=").click()

#driver.quit()