# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 10:42:02 2019

@author: User
"""
import pandas as pd
import csv

def find_one_off(ad_df,year=2019,month=1):
    id_list = ad_df[ad_df['收到年']==year][ad_df['收到月']==month][ad_df['V單次/定期捐款']=='單次捐款']['V捐款者編號'].unique()
    id_list = list(id_list)
    #drop nan in the list
    drop_list = []
    for i in range(len(id_list)):
        if pd.isnull(id_list[i]):
            drop_list.append(i)
    drop_list.reverse()
    
    for i in range(len(drop_list)):
        id_list.pop(drop_list.pop(0))
    
    #make sure the donors are really only one-off donors, instead of regular donors
    one_off_id = []
    for i in range(len(id_list)):
        if '定期捐款' not in ad_df[ad_df['V捐款者編號']==id_list[i]]['V單次/定期捐款'].unique():
            one_off_id.append(id_list[i])
            
    return one_off_id

def write_files(id_list):
    #write files
    csv_file = "./資料/one_off_ws.csv"
    #use 'w' if you want to start writing a new file
    #use 'a' if you want to append data to existing file
    with open( csv_file , 'a') as f: 
        for content in id_list:
            f.write("%s\n"%(content))

def delete_duplicate():
    csv_file = "./資料/one_off_ws.csv"
    
    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        all_list = list(reader)
    
    id_set = set()
    for id in all_list:
        id_set.add(id[0])
    final_list = list(id_set)
    
    with open(csv_file , 'w') as f: 
        for content in final_list:
            f.write("%s\n"%(content))
    