
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


import time
import pandas as pd
from datetime import datetime



def MarketVersion(market, driver):
    driver.get(market)
    #print(driver.title)

def spliter(List_market_data):
    List_market_data_split = []
    
    for marketsElements in List_market_data:
        marketsElements = str(marketsElements)
        item1 = marketsElements.split()
        List_market_data_split.append(item1)
    return List_market_data_split


# merge items 6 and 7 in lists as they are the same value
def merger_lists(List_market_data_split):
    print()
    counter = 0
    for market_no_item in List_market_data_split:
        #print(market_no_item)
        if counter != 0:
            try:
                #clean share price
                market_no_item[6] = float(float(market_no_item[6]) + float(market_no_item[7]))
                del market_no_item[7]
                #clean market cap
                market_no_item[5] = market_no_item[5][0:-2]
                market_no_item[5] = float(market_no_item[5])
            except:
                try:
                    #clean share price
                    market_no_item[5] = float(float(market_no_item[5]) + float(market_no_item[6]))
                    del market_no_item[6]
                    #clean market cap
                    market_no_item[4] = market_no_item[4][0:-2]
                    market_no_item[4] = float(market_no_item[4])
                except:
                    try:
                        #clean share price
                        market_no_item[4] = float(float(market_no_item[4]) + float(market_no_item[5]))
                        del market_no_item[5]
                        #clean market cap
                        market_no_item[3] = market_no_item[3][0:-2]
                        market_no_item[3] = float(market_no_item[3])
                    except:
                        pass
        else:
            pass
            #clean market cap

        counter += 1
    return List_market_data_split


def cleanData(driver, List_of_Markets):
    List_market_data = []
    List_market_data2 = []
    List_market_data3 = []
    List_market_data4 = []
    List_market_data5 = []
    List_market_data6 = []
    List_market_data7 = []
    
    # load entire table before continuing
    time.sleep(10)

    # Get MarketCap
    row = driver.find_elements_by_tag_name("tr")
    data = driver.find_elements_by_tag_name("td")

    print('Rows --> {}'.format(len(row)))
    print('Data --> {}'.format(len(data)))

    # LIST has a max capacity so only bring in so many market rows from table -     180 = capacity
    list_capacity = 0

    # CREATE list of lists of shares data
    for value in row:
        #print(value.text)
        if list_capacity <= 100:
            List_market_data.append(str(value.text))
        elif list_capacity >= 101 and list_capacity <= 200:
            List_market_data2.append(str(value.text))
        elif list_capacity >= 201 and list_capacity <= 300:
            List_market_data3.append(str(value.text))
        elif list_capacity >= 301 and list_capacity <= 400:
            List_market_data4.append(str(value.text))
        elif list_capacity >= 401 and list_capacity <= 500:
            List_market_data5.append(str(value.text))
        elif list_capacity >= 501 and list_capacity <= 600:
            List_market_data6.append(str(value.text))
        elif list_capacity >= 601 and list_capacity <= 720:
            List_market_data7.append(str(value.text))
        else:
            pass
        list_capacity += 1

    # delete unnescary row value
    del List_market_data[1]
    #print(List_market_data)
    #print('\n')


    # Split row data into cells and add back to list of lists
    List_market_data_split = []
    List_market_data_split2 = []
    List_market_data_split3 = []
    List_market_data_split4 = []
    List_market_data_split5 = []
    List_market_data_split6 = []
    List_market_data_split7 = []

    List_market_data_split = spliter(List_market_data)
    List_market_data_split2 = spliter(List_market_data2)
    List_market_data_split3 = spliter(List_market_data3)
    List_market_data_split4 = spliter(List_market_data4)
    List_market_data_split5 = spliter(List_market_data5)
    List_market_data_split6 = spliter(List_market_data6)
    List_market_data_split7 = spliter(List_market_data7)


    List_market_data_split = merger_lists(List_market_data_split)
    List_market_data_split2 = merger_lists(List_market_data_split2)
    List_market_data_split3 = merger_lists(List_market_data_split3)
    List_market_data_split4 = merger_lists(List_market_data_split4)
    List_market_data_split5 = merger_lists(List_market_data_split5)
    List_market_data_split6 = merger_lists(List_market_data_split6)
    List_market_data_split7 = merger_lists(List_market_data_split7)

    #print("----------------------------------------------------------------------------------")
    #print(List_market_data_split)
    #print("----------------------------------------------------------------------------------")
    #print(List_market_data_split2)
    return List_market_data_split, List_market_data_split2, List_market_data_split3, List_market_data_split4, List_market_data_split5, List_market_data_split6, List_market_data_split7








# Updates CSV file values
def InsertIntoExcel3(List_market_data, fileLocation, List_market_data2, List_market_data3, List_market_data4, List_market_data5 ,List_market_data6, List_market_data7):
    print(List_market_data[0][0], fileLocation)


    currentDate = datetime.today().strftime('%m-%d-%Y')
    print(currentDate)


    # Convert CSV into alterable dataframe
    df = pd.read_csv(fileLocation)
    print(df.head())

    df.set_index('Date')

    # Create a new row with the current date
    mod_df = df.append({'Date' : str(currentDate)}, ignore_index=True)

    # Append the Market Cap value to thh current row (using the date as the index)
    # With the market value of the appropiate list (the list with the same market ticker as the column)
    # | append new values |
    for col in df.columns:
        #print(col)
        for aMrket in List_market_data:
            if aMrket[1] == str(col): 
                # if column header is the same as the last 3 characters in the list's first item
                # then add to same row (use the date)
                mod_df.loc[mod_df.Date == currentDate, col] = aMrket[-3]
        for aMrket1 in List_market_data2:
            if aMrket1[1] == str(col): 
                # if column header is the same as the last 3 characters in the list's first item
                # then add to same row (use the date)
                mod_df.loc[mod_df.Date == currentDate, col] = aMrket1[-3]
        for aMrket2 in List_market_data3:
            if aMrket2[1] == str(col): 
                # if column header is the same as the last 3 characters in the list's first item
                # then add to same row (use the date)
                mod_df.loc[mod_df.Date == currentDate, col] = aMrket2[-3]
        for aMrket3 in List_market_data4:
            if aMrket3[1] == str(col): 
                # if column header is the same as the last 3 characters in the list's first item
                # then add to same row (use the date)
                mod_df.loc[mod_df.Date == currentDate, col] = aMrket3[-3]
        for aMrket4 in List_market_data5:
            if aMrket4[1] == str(col): 
                # if column header is the same as the last 3 characters in the list's first item
                # then add to same row (use the date)
                mod_df.loc[mod_df.Date == currentDate, col] = aMrket4[-3]
        for aMrket5 in List_market_data6:
            if aMrket5[1] == str(col): 
                # if column header is the same as the last 3 characters in the list's first item
                # then add to same row (use the date)
                mod_df.loc[mod_df.Date == currentDate, col] = aMrket5[-3]
        for aMrket6 in List_market_data7:
            if aMrket6[1] == str(col): 
                # if column header is the same as the last 3 characters in the list's first item
                # then add to same row (use the date)
                mod_df.loc[mod_df.Date == currentDate, col] = aMrket6[-3]
    return mod_df



########################################################################################################################
# website of market data = https://www.listcorp.com/asx/sectors/materials

def main():
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")

    # Home TEST using my driver
    #PATH = "C:\Garas\chromedriver_win32\chromedriver.exe"

    PATH = "W:\Source_Materials\chrome_driver\chromedriver.exe"
    driver = webdriver.Chrome(PATH)

    # Get all markets to use in getting MarketCap
    List_of_Markets = []
    file1 = open('allMarketsListCORP.txt', 'r')
    while True:
        # Get next line from file
        line = file1.readline()
        # if line is empty
        # end of file is reached
        if not line:
            break
        else:
            line = line.strip('\n')
            List_of_Markets.append(str(line))
    file1.close()
    print("List_of_Markets = ", List_of_Markets)


    

    # Stockmarket chooser
    for market in List_of_Markets:
        MarketVersion(market, driver)
        
    # clean obtained data to put into csv
    List_market_data_split, List_market_data_split2, List_market_data_split3, List_market_data_split4, List_market_data_split5, List_market_data_split6, List_market_data_split7 = cleanData(driver, List_of_Markets)


    #MarketCaps2
    # Get excel file and update data
    filename = "MarketCaps3.csv"

    dataframeUpdated = InsertIntoExcel3(List_market_data_split, filename, List_market_data_split2, List_market_data_split3, List_market_data_split4, List_market_data_split5, List_market_data_split6, List_market_data_split7)

    # Save over excel file
    Csv_out = dataframeUpdated.to_csv('MarketCaps3.csv', sep=',', index=0)

    # Close web connection
    driver.quit()

if __name__ == "__main__":
    main()
