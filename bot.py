# B0NTI BOT V.0.1

import os
import time
import sys
import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from colorama import Fore
from colorama import Style
from colorama import init

# print current date time of moment bontibot is kicked off
now = datetime.now()

# load up all shipping/payment data from json files
ReadshippingData = open('shipping.json',)
shippingData = json.load(ReadshippingData)

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
# BestBuyLink = "https://www.bestbuy.com/site/insignia-ultra-thin-wrap-case-for-apple-iphone-11-smoky-black/6359015.p?skuId=6359015"
BestBuyLink = "https://www.bestbuy.com/site/balan-wonderworld-nintendo-switch/6413951.p?skuId=6413951"
# BestBuyLink = 'https://www.bestbuy.com/site/msi-aegis-zs-gaming-desktop-amd-ryzen-3700x-16gb-memory-rx-5600xt-512gb-ssd-black/6431203.p?skuId=6431203'
# Set the path to the chrome driver, keep this shit relative to the rest of the package
PATH = os.getcwd() + "/chromedriver"
driver = webdriver.Chrome(PATH)

# have selenium navigate to item
print("------------------------------------------")
driver.get(BestBuyLink)

# do some bullshit here to return the Item Name bc nested value
titlePage = (driver.title)
itemName = titlePage.replace(" - Best Buy", "")
print(f'* Checking for Item: {Fore.GREEN}%s{Style.RESET_ALL}' % (itemName))

# Variablize Availability
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
    time.sleep(7)
    AddToCartButton = driver.find_element_by_class_name('add-to-cart-button')
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
time.sleep(5)

# Manage Quantity
DesiredQuantity = "1"
print(Fore.CYAN + "Quantity of desired item is %s" % (DesiredQuantity))
selectOneItem = Select(
    driver.find_element_by_class_name('fluid-item__quantity'))
selectOneItem.select_by_visible_text(DesiredQuantity)
print("* Quantity Updated.")

# Begin Checkout
print(Fore.YELLOW + "Beginning Checkout Process...")
CheckoutButton = driver.find_element_by_class_name('btn-primary')
CheckoutButton.click()
time.sleep(5)
# Checkout As Guest // Not sure why CSS selection is the only thing that works here? shit stupid
print("* Checking out as Guest")
GuestCheckout = driver.find_element_by_css_selector('.guest')
GuestCheckout.click()

# Shipping Information
time.sleep(6)

# Input firstname
firstnamebox = driver.find_element_by_id(
    'consolidatedAddresses.ui_address_2.firstName')
firstnamebox.send_keys(shippingData['FirstName'])

# Input lastname
lastnamebox = driver.find_element_by_id(
    'consolidatedAddresses.ui_address_2.lastName')
lastnamebox.send_keys(shippingData['LastName'])

# Street Address Interactive box nonsense
addressbox = driver.find_element_by_id(
    'consolidatedAddresses.ui_address_2.street')
addressbox.send_keys(shippingData['Address'])

# Im a fucking god -- Escape the dropdown for street address
webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()

# Click Apartment dropdown box if apartment number is present in JSON otherwise skip it
if shippingData['AptNumber'] != None:
    aptDropdownButton = driver.find_element_by_class_name(
        'address-form__showAddress2Link')
    aptDropdownButton.click()
    # wait time here to allow the element to load
    time.sleep(1)
    aptDropdownBox = driver.find_element_by_id(
        'consolidatedAddresses.ui_address_2.street2')
    aptDropdownBox.send_keys(shippingData['AptNumber'])
else:
    pass

# Pass in city
citybox = driver.find_element_by_id(
    'consolidatedAddresses.ui_address_2.city')
citybox.send_keys(shippingData['City'])

# Input state, probably a cleaner way to do this
state = shippingData['State']
selectOneItem = Select(
    driver.find_element_by_class_name('smart-select'))
selectOneItem.select_by_visible_text(state)

# Input zip code
addressbox = driver.find_element_by_id(
    'consolidatedAddresses.ui_address_2.zipcode')
addressbox.send_keys(shippingData['Zip'])

# Contact Information - email
emailBox = driver.find_element_by_id(
    'user.emailAddress')
emailBox.send_keys(shippingData['email'])

# Contact Information - phone number
phoneBox = driver.find_element_by_id(
    'user.phone')
phoneBox.send_keys(shippingData['phone'])

# Continue to payment info button
print(Fore.YELLOW + "Proceeding to Payment Information...")
pyamentButton = driver.find_element_by_class_name('btn-lg')
pyamentButton.click()
