#!/usr/bin/env python3
'''Tool to extract data from LDAP'''

# MIT License

# Copyright (c) 2020 Luke Strohm

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


from argparse import ArgumentParser
import datetime
import hashlib

import xlsxwriter
from ldap3 import ALL, Connection, Server, Tls
from tzlocal import get_localzone

# Global variables. Change these to suit your environment
SERVER = "madhs01dc3.mlsd.local"
BASE_DN = "OU=Madison,DC=mlsd,DC=local"
STU_SEARCH = "(&(objectclass=Person)(employeeID=*)(company=student)\
    (|(userAccountControl=514)(userAccountControl=546)))"
STA_SEARCH = "(&(objectclass=Person)(company=staff)\
    (|(userAccountControl=514)(userAccountControl=546))\
    (!(cn=*admin*))(!(cn=*mad-help*))(!(cn=*gads*))(!(cn=*rrabbit*))(!(cn=*cgriswold*)))"

# Connects and binds to LDAP server
with open("/home/lstrohm/Scripts/ADcreds.txt", "r", encoding="utf-8") as creds:
    lines = creds.readlines()
    username = lines[0]
    password = lines[1]
tls = Tls(
    local_private_key_file=None,
    local_certificate_file=None,
)
s = Server("madhs01dc3.mlsd.local", use_ssl=True, get_info=ALL, tls=tls)
CON = Connection(s, user=username.strip(), password=password.strip())

CON.bind()

# Variable for current date and time (for filename).
now = datetime.datetime.now()
date = now.strftime("%m-%d-%Y_%H-%M")
# Creates Excel workbook
WB = xlsxwriter.Workbook(
    "/home/lstrohm/LDAP-Extract-" + date + ".xlsx",
    {"strings_to_numbers": True},
)
# Various cell formatting variables
WB.add_format({"align": "left", "valign": "vcenter"})
CENTER = WB.add_format({"align": "center"})
BOLD = WB.add_format({"bold": True})
RED_BOLD = WB.add_format(
    {"bold": True, "font_color": "red", "align": "center"}
)
RED_BG = WB.add_format({"bg_color": "#f2a8a8", "align": "center"})
YELLOW_BG = WB.add_format({"bg_color": "#faf849", "align": "center"})
# Creates the Data sheet
worksheet_data = WB.add_worksheet("Data")
blds = [
    "Eastview",
    "Mifflin",
    "South",
    "Middle School",
    "High School",
    "Board Office",
    "Bus Garage",
    "Lincoln Heights",
    "Total",
]
grds = [
    "Kdg",
    "1st",
    "2nd",
    "3rd",
    "4th",
    "5th",
    "6th",
    "7th",
    "8th",
    "9th",
    "10th",
    "11th",
    "12th",
    "Total Students",
]
# Writes header row and column in Data sheet
worksheet_data.write_row("B1", blds, BOLD)
worksheet_data.write_column("A2", grds, BOLD)
# Creates the Charts sheet
WB.add_worksheet("Charts")


class Color:
    '''Colors'''
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    DARKCYAN = "\033[36m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"


def cred():
    '''Credentials'''
    print(
        Color.DARKCYAN
        + "\n"
        + "*********************************\n"
        + "*    Script to Extract User     *\n"
        + "*    Account Data From LDAP     *\n"
        + "*                               *\n"
        + "*  Written and maintained by:   *\n"
        + "*        Luke Strohm            *\n"
        + "*    strohm.luke@gmail.com      *\n"
        + "*  https://github.com/strohmy86 *\n"
        + "*********************************\n"
        + "\n"
        + Color.END
    )


def extract_stu():
    '''Search for all active student accounts in AD'''
    CON.search(
        BASE_DN,
        STU_SEARCH,
        attributes=[
            "displayName",
            "employeeID",
            "mail",
            "cn",
            "l",
            "description",
            "memberOf",
        ],
    )
    users = CON.entries  # Store search results to list
    # Create Students worksheet
    ws_stu = WB.add_worksheet("Students")
    # Open the Data worksheet for writing
    ws_data = WB.get_worksheet_by_name("Data")
    headers = [
        "Name",
        "Username",
        "Email",
        "StudentID",
        "SHA1 Hashed Password",
        "Location",
        "Grade",
        "Group Membership",
    ]
    ws_stu.write_row("A1", headers, BOLD)  # write headers to sheet
    row = 1  # Start data at row 2, below headers (A2)
    col = 0
    # 5, 6, 7, 8, 9, 10, 11, 12
    grd = [0, 0, 0, 0, 0, 0, 0, 0]
    # EAKG, EA1, EA2, EA3, EA4, MIKG, MI1, etc
    bldgr = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
    # Iterates through search results, and writes data to sheet
    for x in users:
        loc = str(x.l.value).strip()
        grade = str(x.description.value).strip()
        name = str(x.displayName.value).strip()
        cn = str(x.cn.value)
        mail = str(x.mail.value).strip()
        ids = str(x.employeeID.value).strip()
        pw = str(x.employeeID.value).strip()
        while len(pw) < 8:  # Ensures all students' pw is min 8 characters
            pw = "0" + pw
        hashed = hashlib.sha1(str(pw).encode("utf-8")).hexdigest()
        groups = str(x.memberOf.value)
        # Adds student count to list based on current grade
        if "5" in grade:
            grd[0] += 1
        elif "6" in grade:
            grd[1] += 1
        elif "7" in grade:
            grd[2] += 1
        elif "8" in grade:
            grd[3] += 1
        elif "9" in grade:
            grd[4] += 1
        elif grade == "10":
            grd[5] += 1
        elif grade == "11":
            grd[6] += 1
        elif grade == "12":
            grd[7] += 1
        # Adds elementary student counts per building
        if "Eastview" in loc and "KG" in grade:
            bldgr[0][0] += 1
        elif "Eastview" in loc and "01" in grade:
            bldgr[0][1] += 1
        elif "Eastview" in loc and "02" in grade:
            bldgr[0][2] += 1
        elif "Eastview" in loc and "03" in grade:
            bldgr[0][3] += 1
        elif "Eastview" in loc and "04" in grade:
            bldgr[0][4] += 1
        elif "Mifflin" in loc and "KG" in grade:
            bldgr[1][0] += 1
        elif "Mifflin" in loc and "01" in grade:
            bldgr[1][1] += 1
        elif "Mifflin" in loc and "02" in grade:
            bldgr[1][2] += 1
        elif "Mifflin" in loc and "03" in grade:
            bldgr[1][3] += 1
        elif "Mifflin" in loc and "04" in grade:
            bldgr[1][4] += 1
        elif "South" in loc and "KG" in grade:
            bldgr[2][0] += 1
        elif "South" in loc and "01" in grade:
            bldgr[2][1] += 1
        elif "South" in loc and "02" in grade:
            bldgr[2][2] += 1
        elif "South" in loc and "03" in grade:
            bldgr[2][3] += 1
        elif "South" in loc and "04" in grade:
            bldgr[2][4] += 1
        ws_stu.write(row, col, name)
        ws_stu.write(row, col + 1, cn)
        ws_stu.write(row, col + 2, mail)
        ws_stu.write(row, col + 3, ids)
        ws_stu.write(row, col + 4, hashed)
        ws_stu.write(row, col + 5, loc)
        ws_stu.write(row, col + 6, grade)
        ws_stu.write(row, col + 7, groups)
        row += 1
    # Opens Charts cheet for writing
    ws_chart = WB.get_worksheet_by_name("Charts")
    # Writes datapoints to the Data sheet
    ws_data.write("B2", bldgr[0][0])
    ws_data.write("B3", bldgr[0][1])
    ws_data.write("B4", bldgr[0][2])
    ws_data.write("B5", bldgr[0][3])
    ws_data.write("B6", bldgr[0][4])
    ws_data.write("C2", bldgr[1][0])
    ws_data.write("C3", bldgr[1][1])
    ws_data.write("C4", bldgr[1][2])
    ws_data.write("C5", bldgr[1][3])
    ws_data.write("C6", bldgr[1][4])
    ws_data.write("D2", bldgr[2][0])
    ws_data.write("D3", bldgr[2][1])
    ws_data.write("D4", bldgr[2][2])
    ws_data.write("D5", bldgr[2][3])
    ws_data.write("D6", bldgr[2][4])
    ws_data.write("E7", grd[0])
    ws_data.write("E8", grd[1])
    ws_data.write("E9", grd[2])
    ws_data.write("E10", grd[3])
    ws_data.write("F11", grd[4])
    ws_data.write("F12", grd[5])
    ws_data.write("F13", grd[6])
    ws_data.write("F14", grd[7])
    ws_data.write_formula("B15", "=SUM(B2:B6)", BOLD)
    ws_data.write_formula("C15", "=SUM(C2:C6)", BOLD)
    ws_data.write_formula("D15", "=SUM(D2:D6)", BOLD)
    ws_data.write_formula("E15", "=SUM(E7:E10)", BOLD)
    ws_data.write_formula("F15", "=SUM(F11:F14)", BOLD)
    ws_data.write_formula("J2", "=SUM(B2:D2)", BOLD)
    ws_data.write_formula("J3", "=SUM(B3:D3)", BOLD)
    ws_data.write_formula("J4", "=SUM(B4:D4)", BOLD)
    ws_data.write_formula("J5", "=SUM(B5:D5)", BOLD)
    ws_data.write_formula("J6", "=SUM(B6:D6)", BOLD)
    ws_data.write_formula("J7", "=E7", BOLD)
    ws_data.write_formula("J8", "=E8", BOLD)
    ws_data.write_formula("J9", "=E9", BOLD)
    ws_data.write_formula("J10", "=E10", BOLD)
    ws_data.write_formula("J11", "=F11", BOLD)
    ws_data.write_formula("J12", "=F12", BOLD)
    ws_data.write_formula("J13", "=F13", BOLD)
    ws_data.write_formula("J14", "=F14", BOLD)
    ws_data.write_formula("J15", "=SUM(J2:J14)", BOLD)
    # Creates chart for student numbers by building
    chart4 = WB.add_chart({"type": "pie"})
    chart4.add_series(
        {
            "name": "Student Location",
            "categories": ["Data", 0, 1, 0, 5],
            "values": ["Data", 14, 1, 14, 5],
        }
    )
    ws_chart.insert_chart("I17", chart4)
    # Creates chart for student numbers per grade level
    chart5 = WB.add_chart({"type": "column"})
    chart5.add_series(
        {
            "name": "Students Per Grade",
            "categories": ["Data", 1, 0, 13, 0],
            "values": ["Data", 1, 9, 13, 9],
        }
    )
    ws_chart.insert_chart("Q1", chart5)
    # Creates chart for elementary student counts per grade and building
    chart6 = WB.add_chart({"type": "column"})
    chart6.add_series(
        {
            "name": "Eastview",
            "categories": ["Data", 1, 0, 5, 0],
            "values": ["Data", 1, 1, 5, 1],
        }
    )
    chart6.add_series(
        {
            "name": "Mifflin",
            "categories": ["Data", 1, 0, 5, 0],
            "values": ["Data", 1, 2, 5, 2],
        }
    )
    chart6.add_series(
        {
            "name": "South",
            "categories": ["Data", 1, 0, 5, 0],
            "values": ["Data", 1, 3, 5, 3],
        }
    )
    chart6.set_title({"name": "Elementary Students Per Building"})
    chart6.set_x_axis({"name": "Grade"})
    chart6.set_y_axis({"name": "Number of Students"})
    ws_chart.insert_chart("Q17", chart6)
    print(Color.GREEN + "Student Extract Done!\n" + Color.END)


def extract_staff():
    '''searches for active staff accounts in AD'''
    # Gets today's date for pw expiration check
    today = str(datetime.datetime.today())[:-16]
    today2 = datetime.datetime.strptime(today, "%Y-%m-%d")
    # Searches for active staff accounts in LDAP
    CON.search(
        BASE_DN,
        STA_SEARCH,
        attributes=[
            "displayName",
            "title",
            "mail",
            "cn",
            "physicalDeliveryOfficeName",
            "department",
            "lastLogon",
            "memberOf",
        ],
    )
    users = CON.entries  # Stores search results in a list
    # Adds the Staff worksheet for writing
    ws_sta = WB.add_worksheet("Staff")
    # Opens the Data sheet for writing
    ws_data = WB.get_worksheet_by_name("Data")
    headers = [
        "Name",
        "Username",
        "Email",
        "Title",
        "Department",
        "Location",
        "Last AD Login",
        "Group Membership",
    ]
    ws_sta.write_row("A1", headers, BOLD)  # Writes headers for Staff sheet
    row = 1  # Starts data on row 2 (A2)
    col = 0
    clfcn = [0, 0, 0, 0]  # Classified, Certified, Not Labeled, Contracted
    loca = [0, 0, 0, 0, 0, 0, 0, 0]  # EA, MI, SO, MS, HS, BO, BG, JB
    # Iterates through search results and writes data to sheet
    for x in users:
        logstr = str(x.lastLogon.value)
        # Checks for last login date and time
        if len(logstr) == 0:
            last_logon = "Never"
            logdate2 = last_logon
        elif len(logstr) == 25:
            logdate = datetime.datetime.strptime(
                logstr, "%Y-%m-%d %H:%M:%S%z"
            ).astimezone(get_localzone())
            last_logon = logdate.strftime("%m/%d/%Y at %I:%M %p")
            logdate2 = datetime.datetime.strptime(logstr[:-15], "%Y-%m-%d")
        else:
            last_logon = "Never"
            logdate2 = last_logon
        title = str(x.title.value)
        loc = str(x.physicalDeliveryOfficeName.value)
        dept = str(x.department.value)
        name = str(x.displayName.value)
        cn = str(x.cn.value)
        mail = str(x.mail.value)
        groups = str(x.memberOf.value)
        # Checks employee classification (Classified or Certified)
        if "CLSFD" in dept:
            clfcn[0] += 1
        elif "CERT" in dept:
            clfcn[1] += 1
        elif "Contracted" in dept:
            clfcn[3] += 1
        else:  # Sets not categorized
            clfcn[2] += 1
        # Checks to see what building the employee is assigned to
        if "Eastview" in loc:
            loca[0] += 1
        elif "Mifflin" in loc:
            loca[1] += 1
        elif "South" in loc:
            loca[2] += 1
        elif "Middle" in loc:
            loca[3] += 1
        elif "High" in loc:
            loca[4] += 1
        elif "Board" in loc:
            loca[5] += 1
        elif "Transportation" in loc:
            loca[6] += 1
        elif "Early" in loc:
            loca[7] += 1
        ws_sta.write(row, col, name)
        ws_sta.write(row, col + 1, cn)
        ws_sta.write(row, col + 2, mail)
        ws_sta.write(row, col + 3, title)
        ws_sta.write(row, col + 4, dept)
        ws_sta.write(row, col + 5, loc)
        # Formats cell based on last login time
        if last_logon == "Never" and logdate2 == "Never":
            ws_sta.write(row, col + 6, last_logon, RED_BG)
        elif logdate2 < today2 - datetime.timedelta(days=180):
            ws_sta.write(row, col + 6, last_logon, YELLOW_BG)
        else:
            ws_sta.write(row, col + 6, last_logon, CENTER)
        ws_sta.write(row, col + 7, groups)
        row += 1
    # Opens Charts sheet for writing
    ws_chart = WB.get_worksheet_by_name("Charts")
    # Writes datapoints to Data sheet for use in Charts
    ws_data.write("A21", "Classified", BOLD)
    ws_data.write("A22", "Certified", BOLD)
    ws_data.write("A23", "Contracted", BOLD)
    ws_data.write("A24", "Not Labeled", BOLD)
    ws_data.write("B21", clfcn[0])
    ws_data.write("B22", clfcn[1])
    ws_data.write("B23", clfcn[3])
    ws_data.write("B24", clfcn[2])
    # Creates chart to show employee classification
    chart2 = WB.add_chart({"type": "pie"})
    chart2.add_series(
        {
            "name": "Employee Classification",
            "categories": ["Data", 20, 0, 23, 0],
            "values": ["Data", 20, 1, 23, 1],
        }
    )
    ws_chart.insert_chart("A17", chart2)
    # Writes datapoints to Data sheet for use in Charts
    ws_data.write("A26", "Staff")
    ws_data.write("B26", loca[0])
    ws_data.write("C26", loca[1])
    ws_data.write("D26", loca[2])
    ws_data.write("E26", loca[3])
    ws_data.write("F26", loca[4])
    ws_data.write("G26", loca[5])
    ws_data.write("H26", loca[6])
    ws_data.write("I26", loca[7])
    ws_data.write_formula("J26", "=SUM(B26:I26)", BOLD)
    # Creates chart to show number of employees per building
    chart3 = WB.add_chart({"type": "pie"})
    chart3.add_series(
        {
            "name": "Employee Location",
            "categories": ["Data", 0, 1, 0, 8],
            "values": ["Data", 25, 1, 25, 8],
        }
    )
    ws_chart.insert_chart("I1", chart3)
    print(Color.GREEN + "Staff Extract Done!\n" + Color.END)

if __name__ == "__main__":
    # Creates argument parser and adds arguements
    parser = ArgumentParser(
        description="Script to extract Staff and/or Student account data from LDAP."
    )
    parser.add_argument(
        "-sta",
        "--staff",
        metavar="Staff",
        default=False,
        action="store_const",
        const=True,
        help="Extract staff account data",
    )
    parser.add_argument(
        "-stu",
        "--student",
        metavar="Student",
        default=False,
        action="store_const",
        const=True,
        help="Extract student account data",
    )
    args = parser.parse_args()
    staff = args.staff
    stu = args.student


    cred()  # Shows credits

    



    # Logic to determine which functions to execute
    if staff and stu:
        extract_staff()
        extract_stu()
        CON.unbind()
        WB.close()
        print(
            Color.CYAN + "Saved as ~/LDAP-Extract-" + date + ".xlsx\n" + Color.END
        )
    elif staff and not stu:
        extract_staff()
        CON.unbind()
        WB.close()
        print(
            Color.CYAN + "Saved as ~/LDAP-Extract-" + date + ".xlsx\n" + Color.END
        )
    elif not staff and stu:
        extract_stu()
        CON.unbind()
        WB.close()
        print(
            Color.CYAN + "Saved as ~/LDAP-Extract-" + date + ".xlsx\n" + Color.END
        )
    else:
        CON.unbind()
        WB.close()
        parser.print_help()
        parser.exit(1)
