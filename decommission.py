#!/usr/bin/env python3

import csv
import pymysql


def cred():

    print("\n")
    print("*********************************")
    print("*     Device Decommission       *")
    print("*           Utility             *")
    print("*  Written and maintained by:   *")
    print("*        Luke Strohm            *")
    print("*    strohm.luke@gmail.com      *")
    print("*                               *")
    print("*********************************")
    print("\n")


pymysql.install_as_MySQLdb()
conn = pymysql.connect(host='10.14.0.31', user='root', passwd='ujoCheg')
cursor = conn.cursor()


with open(input('What is the name of the csv file to be used?   ')) as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    row_count = sum(1 for row in readCSV)
    for row in readCSV:
        cursor.execute("update asset set assetlocation='',description='',locationid=37,assetstatusid=2 where assetnumber=%s limit %s"[row,row_count])
    conn.commit()
cursor.close()
del cursor
conn.close()

