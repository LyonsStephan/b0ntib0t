# B0NTI BOT V.0.2

import os
import time
import sys
import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from colorama import Fore
from colorama import Style
from colorama import init

# print current date time of moment bontibot is kicked off
now = datetime.now()

# load up all shipping/payment data from json files
ReadUserData = open('user.json',)
UserData = json.load(ReadUserData)

print('  ____   ___  _   _ _______ _____       ____   ____ _______ ')
print(' |  _ \ / _ \| \ | |__   __|_   _|     |  _ \ / __ \__   __|')
print(' | |_) | | | |  \| |  | |    | |       | |_) | |  | | | |   ')
print(' |  _ <| | | | . ` |  | |    | |       |  _ <| |  | | | |   ')
print(' | |_) | |_| | |\  |  | |   _| |_      | |_) | |__| | | |   ')
print(' |____/ \___/|_| \_|  |_|  |_____|     |____/ \____/  |_|   ')
print('')
print('B0NTI B0T STARTED AT :', now)

init(autoreset=True)
# Throw the full URL in this thing until I can create a cleaner variable // Using two links here, available and unavailable to test
#BestBuyLink = "https://www.bestbuy.com/site/msi-mech-oc-amd-radeon-rx-5700-xt-8gb-gddr6-pci-express-4-0-graphics-card-black/6374966.p?skuId=6374966"
BestBuyLink = "https://www.bestbuy.com/site/rocketfish-90-degree-coaxial-cable-adapter-2-pack-gold/5722600.p?skuId=5722600"

# Set the path to the chrome driver, keep this shit relative to the rest of the package
PATH = os.getcwd() + "/Resources/chromedriver"
driver = webdriver.Chrome(PATH)

# have selenium navigate to item
print("------------------------------------------")
driver.get(BestBuyLink)

# do some bullshit here to return the Item Name bc nested value
titlePage = (driver.title)
itemName = titlePage.replace(" - Best Buy", "")
print(f'* Checking for Item: {Fore.GREEN}%s{Style.RESET_ALL}' % (itemName))

# Variablize Availability
WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.CLASS_NAME, "add-to-cart-button")))
AddToCartButton = driver.find_element_by_class_name('add-to-cart-button')
Availability = (AddToCartButton.get_property('innerText'))

# Output availability to debug, comment this in place later
if Availability == "Sold Out":
    print("Item is sold out. Entering while loop sequence")
    # see While loop on line 50
elif Availability == "Add to Cart":
    print("Item is available!")
else:
    print(Fore.RED + "Theres some weird shit going on here, item is not available for online purchase?")
    print("Printing Output below... Then Quitting until I can account for this... Try another Item.")
    print(Availability)
    # Using close here instead of quit, when close called then only tab with FOCUS is closed. Allows multiple runs
    driver.close()
    exit()

while Availability == "Sold Out":
    print(Fore.RED + 'Item - %s is sold out. Retrying...' % (itemName))
    driver.refresh()
    AddToCartButton = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, "add-to-cart-button")))
    Availability = (AddToCartButton.get_property('innerText'))
    print(Availability)
    if Availability == "Add to Cart":
        print(Fore.LIGHTBLUE_EX + "ITEM IS AVAILABLE NOW!")
        break

# Once item is available add to cart
print(Fore.CYAN + '* Adding to Cart: %s' % (itemName))
AddToCartButton.click()

# Start Prepping Cart
print('Preparing Cart...')
cart = 'https://bestbuy.com/cart'
driver.get(cart)

# Manage Quantity
DesiredQuantity = "1"
print(Fore.CYAN + "Quantity of desired item is %s" % (DesiredQuantity))
WebDriverWait(driver, 30).until(EC.presence_of_element_located(
    (By.CLASS_NAME, "fluid-item__quantity")))
selectQuantity = Select(
    driver.find_element_by_class_name("fluid-item__quantity"))
selectQuantity.select_by_visible_text(DesiredQuantity)
print("* Quantity Updated.")

# Begin Checkout
print(Fore.YELLOW + "Beginning Checkout Process...")
WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.CLASS_NAME, "btn-primary")))
CheckoutButton = driver.find_element_by_class_name('btn-primary')
CheckoutButton.click()

# Checkout As Guest // Not sure why CSS selection is the only thing that works here? shit stupid
print("* Checking out as Guest")
WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, ".guest")))
GuestCheckout = driver.find_element_by_css_selector('.guest')
GuestCheckout.click()

# Shipping Information
WebDriverWait(driver, 30).until(EC.presence_of_element_located(
    (By.CLASS_NAME, "btn-primary")))

# Input firstname
firstnamebox = driver.find_element_by_id(
    'consolidatedAddresses.ui_address_2.firstName')
firstnamebox.send_keys(UserData['FirstName'])

# Input lastname
lastnamebox = driver.find_element_by_id(
    'consolidatedAddresses.ui_address_2.lastName')
lastnamebox.send_keys(UserData['LastName'])

# Street Address Interactive box nonsense
addressbox = driver.find_element_by_id(
    'consolidatedAddresses.ui_address_2.street')
addressbox.send_keys(UserData['Address'])

# Im a fucking god -- Escape the dropdown for street address
webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()

# Click Apartment dropdown box if apartment number is present in JSON otherwise skip it
if UserData['AptNumber'] != None:
    aptDropdownButton = driver.find_element_by_class_name(
        'address-form__showAddress2Link')
    aptDropdownButton.click()
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, "consolidatedAddresses.ui_address_2.street2")))
    aptDropdownBox = driver.find_element_by_id(
        'consolidatedAddresses.ui_address_2.street2')
    aptDropdownBox.send_keys(UserData['AptNumber'])
else:
    pass

# Pass in city
citybox = driver.find_element_by_id(
    'consolidatedAddresses.ui_address_2.city')
citybox.send_keys(UserData['City'])

# Input state, probably a cleaner way to do this
state = UserData['State']
selectOneItem = Select(
    driver.find_element_by_class_name('smart-select'))
selectOneItem.select_by_visible_text(state)

# Input zip code
addressbox = driver.find_element_by_id(
    'consolidatedAddresses.ui_address_2.zipcode')
addressbox.send_keys(UserData['Zip'])

# Contact Information - email
emailBox = driver.find_element_by_id(
    'user.emailAddress')
emailBox.send_keys(UserData['email'])

# Contact Information - phone number
phoneBox = driver.find_element_by_id(
    'user.phone')
phoneBox.send_keys(UserData['phone'])

# Continue to payment info button
print(Fore.YELLOW + "Proceeding to Payment Information...")
paymentButton = driver.find_element_by_class_name('btn-lg')
paymentButton.click()

# Collect total order price
WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.CLASS_NAME, "cash-money")))
orderTotal = driver.find_element_by_class_name(
    'order-summary__total').find_element_by_class_name('cash-money')
print(
    f'* Order Total: {Fore.GREEN}%s{Style.RESET_ALL}' % (orderTotal.get_attribute('innerText')))

# Input CC information Print last 4
lastfour_cc_set = UserData['creditcard']
lastfour_cc = (lastfour_cc_set[-4:])
print(
    f'* Using Card Number Ending In: {Fore.GREEN}%s{Style.RESET_ALL}' % (lastfour_cc))

# Input CC info
WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.ID, "optimized-cc-card-number")))
ccbox = driver.find_element_by_id("optimized-cc-card-number")
ccbox.send_keys(UserData['creditcard'])
# Expiration Month
WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.XPATH, "//*[@id='credit-card-expiration-month']/div/div/select")))
expirationMonth = UserData['creditcardMonth']
selectOneItem = Select(
    driver.find_element_by_xpath("//*[@id='credit-card-expiration-month']/div/div/select"))
selectOneItem.select_by_visible_text(expirationMonth)
# Expiration Year
expirationYear = UserData['creditcardYear']
selectOneItem = Select(
    driver.find_element_by_xpath("//*[@id='credit-card-expiration-year']/div/div/select"))
selectOneItem.select_by_visible_text(expirationYear)
# CC CVV
ccbox = driver.find_element_by_id("credit-card-cvv")
ccbox.send_keys(UserData['cvv'])

# SUBMIT THE ORDER
SUBMIT_ORDER_BUTTON = driver.find_element_by_class_name('btn-primary')
SUBMIT_ORDER_BUTTON.click()

print(Fore.MAGENTA + "* Order has been submitted! Please check %s for Order Details." %
      (UserData['email']))
