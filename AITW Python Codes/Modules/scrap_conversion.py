# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 17:54:42 2019

@author: User
"""

import pandas as pd
from time import sleep



def load_conversion():
    file_name = input("Please enter file name: ")
    
    try:
        conversion_df = pd.read_csv('./資料/'+file_name+'.csv', encoding = 'big5')
        print("File loaded succesfully!")
    except FileNotFoundError:
        print("Wrong file name. Please run this cell again!")
    return conversion_df

def load_tm():
    file_name = input("Please enter file name: ")
    
    try:
        tm_df = pd.read_csv('./資料/'+file_name+'.csv', encoding = 'utf-8')
        print("File loaded succesfully!")
    except FileNotFoundError:
        print("Wrong file name. Please run this cell again!")
    return tm_df


def scrap_info(tm_df,conversion_df,driver):
    #write info of conversion into the conversion file
    columns = list(conversion_df.columns)[2:]
    key_words = ['Email','Phone']

    for word in key_words:
        for i in range(conversion_df.shape[0]):
            if pd.isnull(conversion_df['FB-ID'][i]):
                driver.get('https://www.amnesty.tw/civicrm/contact/search?reset=1')
                sleep(1)
                #search for our followers
                search = driver.find_elements_by_xpath('//*[@class="crm-form-elem crm-form-textfield"]/input')
                #look up for data in TMlist
                key_word = tm_df.loc[tm_df['Serial Number']==conversion_df['Serial Number'][i],:][word].reset_index()[word][0]
                search[0].send_keys(key_word)
                #click 搜尋
                pager = driver.find_element_by_xpath('//*[@class="crm-button crm-button-type-refresh crm-button_qf_Basic_refresh"]')
                pager.click()
                sleep(3)
                try:
                    #click into the info page
                    display_name = driver.find_elements_by_xpath('//*[contains(@class,"crm-search-display_name")]')
                    display_name[0].click()
                    sleep(1)
                except:
                    continue
                try:
                    data = driver.find_elements_by_xpath('//*[@class="html-adjust crm-custom-data"]')
                    for j in range(27,32):
                        conversion_df[columns[j-27]][i] = data[j].text

                except:
                    continue
        print(word+' completed!')