import requests
import json

DEF_SHOP = "shopicruit"
DEF_LINK = "https://shopicruit.myshopify.com/admin/orders.json"
###Shopify Calculator
# This script will submit a request to the appropriate link,
# parse the resulting json object,
# and caculate the total amount of revenue from all orders

#Function that manages all data aquisition and print statements
def mainFunction():
    shouldRun = ''
    print("Welcome To Shopify Calculator!")
    while((shouldRun != "y") & (shouldRun != "n")):
        shouldRun = raw_input("Would you like to run revenue calculation for shop '" + DEF_SHOP + "' (y/n)? ")
    if(shouldRun == "y"):
        print("Calculating orders...")
        orders = reqOrders(DEF_LINK)
        revenue = calculateRevenue(orders)
        nativeCurrency = orders[0]["currency"]
        print("Total revenue in native currency " + str(nativeCurrency) + " is: $" + str(revenue["totalRevenueNativeCurrency"]) + "\nTotal revenue in USD is: $" + str(revenue["totalRevenueUsd"]))
    else:
        print("Input of 'n', exiting program...")

#Takes shop link and performs a get request to all order pages
#Returns a list of all appended orders
def reqOrders(link):
    i = 1
    orders = []
    while (True):
        params= (('page', i), ('access_token', 'c32313df0d0ef512ca64d5b336a0d7c6'))

        try:
            r = (requests.get(link, params=params)).json()
        except requests.exceptions.RequestException as e:
            print e
            break;

        if(r["orders"] != []):
            orders+=(r["orders"])
            i+=1
        else:
            break

    return orders

#Takes 'list' of orders and calculates sum of all 'total_price' and 'total_price_usd' properties
#Returns sum of all purchases in  native and USD currency
def calculateRevenue(orders):
    totalRevenueNativeCurrency = 0
    totalRevenueUsd = 0

    for order in orders:
        totalRevenueNativeCurrency += float(order["total_price"])
        totalRevenueUsd += float(order["total_price_usd"])
    return {"totalRevenueNativeCurrency":totalRevenueNativeCurrency, "totalRevenueUsd":totalRevenueUsd}

#Calls main function to initiate calculation
mainFunction()
