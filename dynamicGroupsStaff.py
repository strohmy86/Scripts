#!/usr/bin/env python3

# MIT License

# Copyright (c) 2022 Luke Strohm

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and assoc      'ocumentation files (the "Software\n' +, to deal
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

import time

import paramiko
from ldap3 import (
    ALL,
    MODIFY_ADD,
    MODIFY_DELETE,
    Connection,
    Server,
    Tls,
)

class Color:
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
    print(
        Color.DARKCYAN
        + "\n"
        + "*********************************\n"
        + "*      Python 3 Script For      *\n"
        + "* Maintaining Dynamic Groups in *\n"
        + "*        Active Directory       *\n"
        + "*                               *\n"
        + "*   Written and maintained by   *\n"
        + "*          Luke Strohm          *\n"
        + "*     strohm.luke@gmail.com     *\n"
        + "*  https://github.com/strohmy86 *\n"
        + "*********************************\n"
        + "\n"
        + Color.END
    )

## Connection and Global variables
f = open("/home/lstrohm/Scripts/ADcreds.txt", "r")
lines = f.readlines()
username = lines[0]
password = lines[1]
f.close()
tls = Tls(
        local_private_key_file=None,
        local_certificate_file=None,
    )
s = Server("madhs01dc3.mlsd.local", use_ssl=True, get_info=ALL, tls=tls)
c = Connection(s, user=username.strip(), password=password.strip())
c.bind()
# Specify private key file
k = paramiko.RSAKey.from_private_key_file("/home/lstrohm/.ssh/id_rsa")
# Connects to gcds server via SSH
gcds = paramiko.SSHClient()
gcds.set_missing_host_key_policy(paramiko.AutoAddPolicy())
gcds.connect("madhs01gcds.mlsd.local", username="mlsd\\administrator", pkey=k)

c.search(
    "ou=Madison,DC=mlsd,DC=local",
    "(&(|(mail=*@mlsd.net)(mail=*@madisonadultcc.org))(objectClass=person))",
    attributes=["cn", "memberOf", "department","physicalDeliveryOfficeName",
     "userAccountControl", "title",],
)
users = c.entries



def main(c, gcds, users):
    #------------------------------911-Notify------------------------------#
    nineoneone_notify_add = [i.entry_dn for i in users 
        if "CN=911-notify,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "911".lower() in str(i.department.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value)]
    nineoneone_notify_del = [i.entry_dn for i in users 
        if "CN=911-notify,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("911".lower() not in str(i.department.value).lower() or "514" in \
        str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value))]
    
    if len(nineoneone_notify_add) > 0:
        c.extend.microsoft.add_members_to_groups(
            nineoneone_notify_add,
            "CN=911-notify,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    if len(nineoneone_notify_del) > 0:
        c.extend.microsoft.remove_members_from_groups(
            nineoneone_notify_del,
            "CN=911-notify,OU=Groups,OU=Madison,DC=mlsd,DC=local",
            )
    time.sleep(0.250)
    

    #------------------------------cabinet------------------------------#
    cabinet_add = [i.entry_dn for i in users 
        if "CN=cabinet,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "Cabinet".lower() in str(i.department.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value)]
    cabinet_del = [i.entry_dn for i in users 
        if "CN=cabinet,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("Cabinet".lower() not in str(i.department.value).lower() or "514" in \
        str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value))]

    if len(cabinet_add) > 0:
        c.extend.microsoft.add_members_to_groups(
            cabinet_add,
            "CN=cabinet,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    if len(cabinet_del) > 0:
        c.extend.microsoft.remove_members_from_groups(
            cabinet_del,
            "CN=cabinet,OU=Groups,OU=Madison,DC=mlsd,DC=local",
            )
    time.sleep(0.250)


    #------------------------------certified------------------------------#
    cert_add = [i.entry_dn for i in users
        if "CN=certified,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "CERT".lower() in str(i.department.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value)]
    cert_del = [i.entry_dn for i in users
        if "CN=certified,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("CERT".lower() not in str(i.department.value).lower() or "514" in \
        str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value))]

    if len(cert_add) > 0:
        c.extend.microsoft.add_members_to_groups(
            cert_add,
            "CN=certified,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    if len(cert_del) > 0:
        c.extend.microsoft.remove_members_from_groups(
            cert_del,
            "CN=certified,OU=Groups,OU=Madison,DC=mlsd,DC=local",
            )
    time.sleep(0.250)


    #------------------------------classified------------------------------#
    clsfd_add = [i.entry_dn for i in users
        if "CN=classified,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "CLSFD".lower() in str(i.department.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value)]
    clsfd_del = [i.entry_dn for i in users
        if "CN=classified,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("CLSFD".lower() not in str(i.department.value).lower() or "514" in \
        str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value))]

    if len(clsfd_add) > 0:
        c.extend.microsoft.add_members_to_groups(
            clsfd_add,
            "CN=classified,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    if len(clsfd_del) > 0:
        c.extend.microsoft.remove_members_from_groups(
            clsfd_del,
            "CN=classified,OU=Groups,OU=Madison,DC=mlsd,DC=local",
            )
    time.sleep(0.250)
    

    #------------------------------mad-mail-1------------------------------#
    mad_mail_1_add = [i.entry_dn for i in users
        if "CN=mad-mail-1,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "1st".lower() in str(i.department.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value)]
    mad_mail_1_del = [i.entry_dn for i in users 
        if "CN=mad-mail-1,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("1st".lower() not in str(i.department.value).lower() or "514" in \
        str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value))]

    if len(mad_mail_1_add) > 0:
        c.extend.microsoft.add_members_to_groups(
            mad_mail_1_add,
            "CN=mad-mail-1,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    if len(mad_mail_1_del) > 0:
        c.extend.microsoft.remove_members_from_groups(
            mad_mail_1_del,
            "CN=mad-mail-1,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    
    
    #------------------------------mad-mail-2------------------------------#
    mad_mail_2_add = [i.entry_dn for i in users
        if "CN=mad-mail-2,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "2nd".lower() in str(i.department.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value)]
    mad_mail_2_del = [i.entry_dn for i in users 
        if "CN=mad-mail-2,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("2nd".lower() not in str(i.department.value).lower() or "514" in \
        str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value))]

    if len(mad_mail_2_add) > 0:
        c.extend.microsoft.add_members_to_groups(
            mad_mail_2_add,
            "CN=mad-mail-2,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    if len(mad_mail_2_del) > 0:
        c.extend.microsoft.remove_members_from_groups(
            mad_mail_2_del,
            "CN=mad-mail-2,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)


    #------------------------------mad-mail-3------------------------------#
    mad_mail_3_add = [i.entry_dn for i in users
        if "CN=mad-mail-3,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "3rd".lower() in str(i.department.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value)]
    mad_mail_3_del = [i.entry_dn for i in users 
        if "CN=mad-mail-3,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("3rd".lower() not in str(i.department.value).lower() or "514" in \
        str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value))]

    if len(mad_mail_3_add) > 0:
        c.extend.microsoft.add_members_to_groups(
            mad_mail_3_add,
            "CN=mad-mail-3,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    if len(mad_mail_3_del) > 0:
        c.extend.microsoft.remove_members_from_groups(
            mad_mail_3_del,
            "CN=mad-mail-3,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)


    #------------------------------mad-mail-4------------------------------#
    mad_mail_4_add = [i.entry_dn for i in users
        if "CN=mad-mail-4,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "4th".lower() in str(i.department.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value)]
    mad_mail_4_del = [i.entry_dn for i in users 
        if "CN=mad-mail-4,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("4th".lower() not in str(i.department.value).lower() or "514" in \
        str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value))]

    if len(mad_mail_4_add) > 0:
        c.extend.microsoft.add_members_to_groups(
            mad_mail_4_add,
            "CN=mad-mail-4,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    if len(mad_mail_4_del) > 0:
        c.extend.microsoft.remove_members_from_groups(
            mad_mail_4_del,
            "CN=mad-mail-4,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)


    #------------------------------mad-mail-5------------------------------#
    mad_mail_5_add = [i.entry_dn for i in users
        if "CN=mad-mail-5,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "5th".lower() in str(i.department.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value)]
    mad_mail_5_del = [i.entry_dn for i in users 
        if "CN=mad-mail-5,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("5th".lower() not in str(i.department.value).lower() or "514" in \
        str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value))]

    if len(mad_mail_5_add) > 0:
        c.extend.microsoft.add_members_to_groups(
            mad_mail_5_add,
            "CN=mad-mail-5,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    if len(mad_mail_5_del) > 0:
        c.extend.microsoft.remove_members_from_groups(
            mad_mail_5_del,
            "CN=mad-mail-5,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)


    #------------------------------mad-mail-6------------------------------#
    mad_mail_6_add = [i.entry_dn for i in users
        if "CN=mad-mail-6,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "6th".lower() in str(i.department.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value)]
    mad_mail_6_del = [i.entry_dn for i in users 
        if "CN=mad-mail-6,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("6th".lower() not in str(i.department.value).lower() or "514" in \
        str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value))]

    if len(mad_mail_6_add) > 0:
        c.extend.microsoft.add_members_to_groups(
            mad_mail_6_add,
            "CN=mad-mail-6,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    if len(mad_mail_6_del) > 0:
        c.extend.microsoft.remove_members_from_groups(
            mad_mail_6_del,
            "CN=mad-mail-6,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)


    #------------------------------mad-mail-k------------------------------#
    mad_mail_k_add = [i.entry_dn for i in users
        if "CN=mad-mail-k,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "k".lower() in str(i.department.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value)]
    mad_mail_k_del = [i.entry_dn for i in users 
        if "CN=mad-mail-k,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("k".lower() not in str(i.department.value).lower() or "514" in \
        str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value))]

    if len(mad_mail_k_add) > 0:
        c.extend.microsoft.add_members_to_groups(
            mad_mail_k_add,
            "CN=mad-mail-k,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    if len(mad_mail_k_del) > 0:
        c.extend.microsoft.remove_members_from_groups(
            mad_mail_k_del,
            "CN=mad-mail-k,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)


    #------------------------------mad-mail-admin------------------------------#
    mad_mail_admin_add = [i.entry_dn for i in users
        if "CN=mad-mail-admin,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "adminteam".lower() in str(i.department.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value)]
    mad_mail_admin_del = [i.entry_dn for i in users 
        if "CN=mad-mail-admin,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("adminteam".lower() not in str(i.department.value).lower() or "514" in \
        str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value))]

    if len(mad_mail_admin_add) > 0:
        c.extend.microsoft.add_members_to_groups(
            mad_mail_admin_add,
            "CN=mad-mail-admin,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    if len(mad_mail_admin_del) > 0:
        c.extend.microsoft.remove_members_from_groups(
            mad_mail_admin_del,
            "CN=mad-mail-admin,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    

    #------------------------------mad-mail-custodian------------------------------#
    mad_mail_cust_add = [i.entry_dn for i in users
        if "CN=mad-mail-custodian,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "custodian".lower() in str(i.title.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value)]
    mad_mail_cust_del = [i.entry_dn for i in users 
        if "CN=mad-mail-custodian,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("custodian".lower() not in str(i.title.value).lower() or "514" in \
        str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value))]

    if len(mad_mail_cust_add) > 0:
        c.extend.microsoft.add_members_to_groups(
            mad_mail_cust_add,
            "CN=mad-mail-custodian,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    if len(mad_mail_cust_del) > 0:
        c.extend.microsoft.remove_members_from_groups(
            mad_mail_cust_del,
            "CN=mad-mail-custodian,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    

    #------------------------------mad-mail-foodsvc------------------------------#
    mad_mail_foodsvc_add = [i.entry_dn for i in users
        if "CN=mad-mail-foodsvc,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "cook".lower() in str(i.department.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value)]
    mad_mail_foodsvc_del = [i.entry_dn for i in users 
        if "CN=mad-mail-foodsvc,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and "cook".lower() not in str(i.department.value).lower() or ("514" in \
        str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value))]

    if len(mad_mail_foodsvc_add) > 0:
        c.extend.microsoft.add_members_to_groups(
            mad_mail_foodsvc_add,
            "CN=mad-mail-foodsvc,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    if len(mad_mail_foodsvc_del) > 0:
        c.extend.microsoft.remove_members_from_groups(
            mad_mail_foodsvc_del,
            "CN=mad-mail-foodsvc,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    

    #------------------------------mad-mail-guidance------------------------------#
    mad_mail_guidance_add = [i.entry_dn for i in users
        if "CN=mad-mail-guidance,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "guidance".lower() in str(i.department.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value)]
    mad_mail_guidance_del = [i.entry_dn for i in users 
        if "CN=mad-mail-guidance,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("guidance".lower() not in str(i.department.value).lower() or "514" in \
        str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value))]

    if len(mad_mail_guidance_add) > 0:
        c.extend.microsoft.add_members_to_groups(
            mad_mail_guidance_add,
            "CN=mad-mail-guidance,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    if len(mad_mail_guidance_del) > 0:
        c.extend.microsoft.remove_members_from_groups(
            mad_mail_guidance_del,
            "CN=mad-mail-guidance,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    
    
    #------------------------------mad-mail-nurse------------------------------#
    mad_mail_nurse_add = [i.entry_dn for i in users
        if "CN=mad-mail-nurse,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "nurse".lower() in str(i.department.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value)]
    mad_mail_nurse_del = [i.entry_dn for i in users 
        if "CN=mad-mail-nurse,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("nurse".lower() not in str(i.department.value).lower() or "514" in \
        str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value))]

    if len(mad_mail_nurse_add) > 0:
        c.extend.microsoft.add_members_to_groups(
            mad_mail_nurse_add,
            "CN=mad-mail-nurse,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    if len(mad_mail_nurse_del) > 0:
        c.extend.microsoft.remove_members_from_groups(
            mad_mail_nurse_del,
            "CN=mad-mail-nurse,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)


    #------------------------------mad-mail-para------------------------------#
    mad_mail_para_add = [i.entry_dn for i in users
        if "CN=mad-mail-para,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "para".lower() in str(i.department.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value)]
    mad_mail_para_del = [i.entry_dn for i in users 
        if "CN=mad-mail-para,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and "para".lower() not in str(i.department.value).lower() or ("514" in \
        str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value))]

    if len(mad_mail_para_add) > 0:
        c.extend.microsoft.add_members_to_groups(
            mad_mail_para_add,
            "CN=mad-mail-para,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    if len(mad_mail_para_del) > 0:
        c.extend.microsoft.remove_members_from_groups(
            mad_mail_para_del,
            "CN=mad-mail-para,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)


    #------------------------------mad-mail-pe------------------------------#
    mad_mail_pe_add = [i.entry_dn for i in users
        if "CN=mad-mail-custodian,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "physed".lower() in str(i.department.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value)]
    mad_mail_pe_del = [i.entry_dn for i in users 
        if "CN=mad-mail-custodian,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("physed".lower() not in str(i.department.value).lower() or "514" in \
        str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value))]

    if len(mad_mail_pe_add) > 0:
        c.extend.microsoft.add_members_to_groups(
            mad_mail_pe_add,
            "CN=mad-mail-pe,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    if len(mad_mail_pe_del) > 0:
        c.extend.microsoft.remove_members_from_groups(
            mad_mail_pe_del,
            "CN=mad-mail-pe,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)


    #------------------------------mad-mail-pltw------------------------------#
    mad_mail_pltw_add = [i.entry_dn for i in users
        if "CN=mad-mail-pltw,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "pltw".lower() in str(i.department.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value)]
    mad_mail_pltw_del = [i.entry_dn for i in users 
        if "CN=mad-mail-pltw,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("pltw".lower() not in str(i.department.value).lower() or "514" in \
        str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value))]

    if len(mad_mail_pltw_add) > 0:
        c.extend.microsoft.add_members_to_groups(
            mad_mail_pltw_add,
            "CN=mad-mail-pltw,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    if len(mad_mail_pltw_del) > 0:
        c.extend.microsoft.remove_members_from_groups(
            mad_mail_pltw_del,
            "CN=mad-mail-pltw,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)


    #------------------------------mad-mail-prin------------------------------#
    mad_mail_prin_add = [i.entry_dn for i in users
        if "CN=mad-mail-prin,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "principal".lower() in str(i.department.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value)]
    mad_mail_prin_del = [i.entry_dn for i in users 
        if "CN=mad-mail-prin,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and "principal".lower() not in str(i.department.value).lower() or ("514" in \
        str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value))]

    if len(mad_mail_prin_add) > 0:
        c.extend.microsoft.add_members_to_groups(
            mad_mail_prin_add,
            "CN=mad-mail-prin,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    if len(mad_mail_prin_del) > 0:
        c.extend.microsoft.remove_members_from_groups(
            mad_mail_prin_del,
            "CN=mad-mail-prin,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    

    #------------------------------mad-mail-secretary------------------------------#
    mad_mail_secretary_add = [i.entry_dn for i in users
        if "CN=mad-mail-secretary,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "secretary".lower() in str(i.department.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value)]
    mad_mail_secretary_del = [i.entry_dn for i in users 
        if "CN=mad-mail-secretary,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and "secretary".lower() not in str(i.department.value).lower() or ("514" in \
        str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value))]

    if len(mad_mail_secretary_add) > 0:
        c.extend.microsoft.add_members_to_groups(
            mad_mail_secretary_add,
            "CN=mad-mail-secretary,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    if len(mad_mail_secretary_del) > 0:
        c.extend.microsoft.remove_members_from_groups(
            mad_mail_secretary_del,
            "CN=mad-mail-secretary,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)


    #------------------------------mad-mail-sis------------------------------#
    mad_mail_sis_add = [i.entry_dn for i in users
        if "CN=mad-mail-sis,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "sis".lower() in str(i.department.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value)]
    mad_mail_sis_del = [i.entry_dn for i in users 
        if "CN=mad-mail-sis,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("sis".lower() not in str(i.department.value).lower() or "514" in \
        str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value))]

    if len(mad_mail_sis_add) > 0:
        c.extend.microsoft.add_members_to_groups(
            mad_mail_sis_add,
            "CN=mad-mail-sis,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    if len(mad_mail_sis_del) > 0:
        c.extend.microsoft.remove_members_from_groups(
            mad_mail_sis_del,
            "CN=mad-mail-sis,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    

    #------------------------------mad-mail-sped------------------------------#
    mad_mail_sped_add = [i.entry_dn for i in users
        if "CN=mad-mail-sped,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "intervention".lower() in str(i.department.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value)]
    mad_mail_sped_del = [i.entry_dn for i in users 
        if "CN=mad-mail-sped,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("intervention".lower() not in str(i.department.value).lower() or "514" in \
        str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value))]

    if len(mad_mail_sped_add) > 0:
        c.extend.microsoft.add_members_to_groups(
            mad_mail_sped_add,
            "CN=mad-mail-sped,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    if len(mad_mail_sped_del) > 0:
        c.extend.microsoft.remove_members_from_groups(
            mad_mail_sped_del,
            "CN=mad-mail-sped,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)


    #------------------------------mad-mail-teacher------------------------------#
    mad_mail_teacher_add = [i.entry_dn for i in users
        if "CN=mad-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and ("teacher".lower() in str(i.title.value).lower() or "principal".lower() in str(i.title.value).lower()) \
        and "514" not in str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value)]
    mad_mail_teacher_del = [i.entry_dn for i in users
        if "CN=mad-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("teacher".lower() not in str(i.title.value).lower() or "principal".lower() not in str(i.title.value).lower()) \
        or ("514" in str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value))]
    
    if len(mad_mail_teacher_add) > 0:
        c.extend.microsoft.add_members_to_groups(
            mad_mail_teacher_add,
            "CN=mad-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    if len(mad_mail_teacher_del) > 0:
        c.extend.microsoft.remove_members_from_groups(
            mad_mail_teacher_del,
            "CN=mad-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)


    #------------------------------mad-mail-title1------------------------------#
    mad_mail_title1_add = [i.entry_dn for i in users
        if "CN=mad-mail-title1,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "title 1".lower() in str(i.department.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value)]
    mad_mail_title1_del = [i.entry_dn for i in users 
        if "CN=mad-mail-title1,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("title 1".lower() not in str(i.department.value).lower() or "514" in \
        str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value))]

    if len(mad_mail_title1_add) > 0:
        c.extend.microsoft.add_members_to_groups(
            mad_mail_title1_add,
            "CN=mad-mail-title1,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    if len(mad_mail_title1_del) > 0:
        c.extend.microsoft.remove_members_from_groups(
            mad_mail_title1_del,
            "CN=mad-mail-title1,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)


    #------------------------------mad-mail-user------------------------------#
    mad_mail_user_add = [i.entry_dn for i in users
        if "CN=mad-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "sub".lower() not in str(i.cn.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value)]
    mad_mail_user_del = [i.entry_dn for i in users
        if "CN=mad-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("514" in str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value))]

    if len(mad_mail_user_add) > 0:
        c.extend.microsoft.add_members_to_groups(
            mad_mail_user_add,
            "CN=mad-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    if len(mad_mail_user_del) > 0:
        c.extend.microsoft.remove_members_from_groups(
            mad_mail_user_del,
            "CN=mad-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)


    #------------------------------mad-tech------------------------------#
    mad_tech_add = [i.entry_dn for i in users
        if "CN=mad-tech,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "Technology Office".lower() in str(i.physicalDeliveryOfficeName.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value)]
    mad_tech_del = [i.entry_dn for i in users
        if "CN=mad-tech,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("Technology Office".lower() not in str(i.physicalDeliveryOfficeName.value).lower() \
        or ("514" in str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value)))]

    if len(mad_tech_add) > 0:
        c.extend.microsoft.add_members_to_groups(
            mad_tech_add,
            "CN=mad-tech,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    if len(mad_tech_del) > 0:
        c.extend.microsoft.remove_members_from_groups(
            mad_tech_del,
            "CN=mad-tech,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)


    #------------------------------mad56-mail-teacher------------------------------#
    mad56_mail_teacher_add = [i.entry_dn for i in users
        if "CN=mad56-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and ("teacher".lower() in str(i.title.value).lower() or "principal".lower() in str(i.title.value).lower()) \
        and "56".lower() in str(i.department.value).lower() and "514" not in str(i.userAccountControl.value) \
        and "546" not in str(i.userAccountControl.value)]
    mad56_mail_teacher_del = [i.entry_dn for i in users
        if "CN=mad56-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and (("teacher".lower() not in str(i.title.value).lower() or "principal".lower() not in str(i.title.value).lower() \
        or "56".lower() not in str(i.department.value).lower()) or ("514" in str(i.userAccountControl.value) or \
        "546" in str(i.userAccountControl.value)))]

    if len(mad56_mail_teacher_add) > 0:
        c.extend.microsoft.add_members_to_groups(
            mad56_mail_teacher_add,
            "CN=mad56-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    if len(mad56_mail_teacher_del) > 0:
        c.extend.microsoft.remove_members_from_groups(
            mad56_mail_teacher_del,
            "CN=mad56-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)


    #------------------------------mad78-mail-teacher------------------------------#
    mad78_mail_teacher_add = [i.entry_dn for i in users
        if "CN=mad78-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and ("teacher".lower() in str(i.title.value).lower() or "principal".lower() in str(i.title.value).lower()) \
        and "78".lower() in str(i.department.value).lower() and "514" not in str(i.userAccountControl.value) \
        and "546" not in str(i.userAccountControl.value)]
    mad78_mail_teacher_del = [i.entry_dn for i in users
        if "CN=mad78-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and (("teacher".lower() not in str(i.title.value).lower() or "principal".lower() not in str(i.title.value).lower() \
        or "78".lower() not in str(i.department.value).lower()) or ("514" in str(i.userAccountControl.value) or \
        "546" in str(i.userAccountControl.value)))]

    if len(mad78_mail_teacher_add) > 0:
        c.extend.microsoft.add_members_to_groups(
            mad78_mail_teacher_add,
            "CN=mad78-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    if len(mad78_mail_teacher_del) > 0:
        c.extend.microsoft.remove_members_from_groups(
            mad78_mail_teacher_del,
            "CN=mad78-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    

    #------------------------------mad56-mail-user------------------------------#
    mad56_mail_user_add = [i.entry_dn for i in users
        if "CN=mad56-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "56".lower() in str(i.department.value).lower() and "514" not in str(i.userAccountControl.value) \
        and "546" not in str(i.userAccountControl.value)]
    mad56_mail_user_del = [i.entry_dn for i in users
        if "CN=mad56-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and "56".lower() not in str(i.department.value).lower() or ("514" in str(i.userAccountControl.value) or \
        "546" in str(i.userAccountControl.value))]

    if len(mad56_mail_user_add) > 0:
        c.extend.microsoft.add_members_to_groups(
            mad56_mail_user_add,
            "CN=mad56-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    if len(mad56_mail_user_del) > 0:
        c.extend.microsoft.remove_members_from_groups(
            mad56_mail_user_del,
            "CN=mad56-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    

    #------------------------------mad78-mail-user------------------------------#
    mad78_mail_user_add = [i.entry_dn for i in users
        if "CN=mad78-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "78".lower() in str(i.department.value).lower() and "514" not in str(i.userAccountControl.value) \
        and "546" not in str(i.userAccountControl.value)]
    mad78_mail_user_del = [i.entry_dn for i in users
        if "CN=mad78-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and "78".lower() not in str(i.department.value).lower() or ("514" in str(i.userAccountControl.value) or \
        "546" in str(i.userAccountControl.value))]

    if len(mad78_mail_user_add) > 0:
        c.extend.microsoft.add_members_to_groups(
            mad78_mail_user_add,
            "CN=mad78-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    if len(mad78_mail_user_del) > 0:
        c.extend.microsoft.remove_members_from_groups(
            mad78_mail_user_del,
            "CN=mad78-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)


    #------------------------------madea-mail-custodian------------------------------#
    madea_mail_custodian_add = [i.entry_dn for i in users
        if "CN=madea-mail-custodian,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "custodian".lower() in str(i.title.value).lower() and "Eastview".lower() \
        in str(i.physicalDeliveryOfficeName.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value)]
    madea_mail_custodian_del = [i.entry_dn for i in users
        if "CN=madea-mail-custodian,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("custodian".lower() not in str(i.title.value).lower() or \
        "Eastview".lower() not in str(i.physicalDeliveryOfficeName.value).lower()) \
        or ("514" in str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value))]
    
    if len(madea_mail_custodian_add) > 0:
        c.extend.microsoft.add_members_to_groups(
            madea_mail_custodian_add,
            "CN=madea-mail-custodian,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    if len(madea_mail_custodian_del) > 0:
        c.extend.microsoft.remove_members_from_groups(
            madea_mail_custodian_del,
            "CN=madea-mail-custodian,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)


    #------------------------------madmi-mail-custodian------------------------------#
    madmi_mail_custodian_add = [i.entry_dn for i in users
        if "CN=madmi-mail-custodian,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "custodian".lower() in str(i.title.value).lower() and "Mifflin".lower() \
        in str(i.physicalDeliveryOfficeName.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value)]
    madmi_mail_custodian_del = [i.entry_dn for i in users
        if "CN=madmi-mail-custodian,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and (("custodian".lower() not in str(i.title.value).lower() or \
        "Mifflin".lower() not in str(i.physicalDeliveryOfficeName.value).lower()) \
        or ("514" in str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value)))]
    
    if len(madmi_mail_custodian_add) > 0:
        c.extend.microsoft.add_members_to_groups(
            madmi_mail_custodian_add,
            "CN=madmi-mail-custodian,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    if len(madmi_mail_custodian_del) > 0:
        c.extend.microsoft.remove_members_from_groups(
            madmi_mail_custodian_del,
            "CN=madmi-mail-custodian,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)


    #------------------------------madso-mail-custodian------------------------------#
    madso_mail_custodian_add = [i.entry_dn for i in users
        if "CN=madso-mail-custodian,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "custodian".lower() in str(i.title.value).lower() and "South".lower() \
        in str(i.physicalDeliveryOfficeName.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value)]
    madso_mail_custodian_del = [i.entry_dn for i in users
        if "CN=madso-mail-custodian,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and (("custodian".lower() not in str(i.title.value).lower() or \
        "South".lower() not in str(i.physicalDeliveryOfficeName.value).lower()) \
        or ("514" in str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value)))]
    
    if len(madso_mail_custodian_add) > 0:
        c.extend.microsoft.add_members_to_groups(
            madso_mail_custodian_add,
            "CN=madso-mail-custodian,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    if len(madso_mail_custodian_del) > 0:
        c.extend.microsoft.remove_members_from_groups(
            madso_mail_custodian_del,
            "CN=madso-mail-custodian,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)


    #------------------------------madms-mail-custodian------------------------------#
    madms_mail_custodian_add = [i.entry_dn for i in users
        if "CN=madms-mail-custodian,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "custodian".lower() in str(i.title.value).lower() and "Middle".lower() \
        in str(i.physicalDeliveryOfficeName.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value)]
    madms_mail_custodian_del = [i.entry_dn for i in users
        if "CN=madms-mail-custodian,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and (("custodian".lower() not in str(i.title.value).lower() or \
        "Middle".lower() in str(i.physicalDeliveryOfficeName.value).lower()) \
        or ("514" in str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value)))]
    
    if len(madms_mail_custodian_add) > 0:
        c.extend.microsoft.add_members_to_groups(
            madms_mail_custodian_add,
            "CN=madms-mail-custodian,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    if len(madms_mail_custodian_del) > 0:
        c.extend.microsoft.remove_members_from_groups(
            madms_mail_custodian_del,
            "CN=madms-mail-custodian,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)


    #------------------------------madhs-mail-custodian------------------------------#
    madhs_mail_custodian_add = [i.entry_dn for i in users
        if "CN=madhs-mail-custodian,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "custodian".lower() in str(i.title.value).lower() and "High".lower() \
        in str(i.physicalDeliveryOfficeName.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value)]
    madhs_mail_custodian_del = [i.entry_dn for i in users
        if "CN=madhs-mail-custodian,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and (("custodian".lower() not in str(i.title.value).lower() or \
        "High".lower() not in str(i.physicalDeliveryOfficeName.value).lower()) \
        or ("514" in str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value)))]
    
    if len(madhs_mail_custodian_add) > 0:
        c.extend.microsoft.add_members_to_groups(
            madhs_mail_custodian_add,
            "CN=madhs-mail-custodian,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    if len(madhs_mail_custodian_del) > 0:
        c.extend.microsoft.remove_members_from_groups(
            madhs_mail_custodian_del,
            "CN=madhs-mail-custodian,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)


    #------------------------------madea-mail-para------------------------------#
    madea_mail_para_add = [i.entry_dn for i in users
        if "CN=madea-mail-para,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "para".lower() in str(i.title.value).lower() and "Eastview".lower() \
        in str(i.physicalDeliveryOfficeName.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value)]
    madea_mail_para_del = [i.entry_dn for i in users
        if "CN=madea-mail-para,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and (("para".lower() not in str(i.title.value).lower() or \
        "Eastview".lower() not in str(i.physicalDeliveryOfficeName.value).lower()) \
        or ("514" in str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value)))]
    
    if len(madea_mail_para_add) > 0:
        c.extend.microsoft.add_members_to_groups(
            madea_mail_para_add,
            "CN=madea-mail-para,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    if len(madea_mail_para_del) > 0:
        c.extend.microsoft.remove_members_from_groups(
            madea_mail_para_del,
            "CN=madea-mail-para,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)


    #------------------------------madmi-mail-para------------------------------#
    madmi_mail_para_add = [i.entry_dn for i in users
        if "CN=madmi-mail-para,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "para".lower() in str(i.title.value).lower() and "Miflin".lower() \
        in str(i.physicalDeliveryOfficeName.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value)]
    madmi_mail_para_del = [i.entry_dn for i in users
        if "CN=madmi-mail-para,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and (("para".lower() not in str(i.title.value).lower() or \
        "Miflin".lower() in str(i.physicalDeliveryOfficeName.value).lower()) \
        or ("514" in str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value)))]
    
    if len(madmi_mail_para_add) > 0:
        c.extend.microsoft.add_members_to_groups(
            madmi_mail_para_add,
            "CN=madmi-mail-para,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    if len(madmi_mail_para_del) > 0:
        c.extend.microsoft.remove_members_from_groups(
            madmi_mail_para_del,
            "CN=madmi-mail-para,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)


    #------------------------------madso-mail-para------------------------------#
    madso_mail_para_add = [i.entry_dn for i in users
        if "CN=madso-mail-para,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "para".lower() in str(i.title.value).lower() and "South".lower() \
        in str(i.physicalDeliveryOfficeName.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value)]
    madso_mail_para_del = [i.entry_dn for i in users
        if "CN=madso-mail-para,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and (("para".lower() not in str(i.title.value).lower() or \
        "South".lower() in str(i.physicalDeliveryOfficeName.value).lower()) \
        or ("514" in str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value)))]
    
    if len(madso_mail_para_add) > 0:
        c.extend.microsoft.add_members_to_groups(
            madso_mail_para_add,
            "CN=madso-mail-para,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    if len(madso_mail_para_del) > 0:
        c.extend.microsoft.remove_members_from_groups(
            madso_mail_para_del,
            "CN=madso-mail-para,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    

    #------------------------------madms-mail-para------------------------------#
    madms_mail_para_add = [i.entry_dn for i in users
        if "CN=madms-mail-para,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "para".lower() in str(i.title.value).lower() and "Middle".lower() \
        in str(i.physicalDeliveryOfficeName.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value)]
    madms_mail_para_del = [i.entry_dn for i in users
        if "CN=madms-mail-para,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and (("para".lower() not in str(i.title.value).lower() or \
        "Middle".lower() in str(i.physicalDeliveryOfficeName.value).lower()) \
        or ("514" in str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value)))]
    
    if len(madms_mail_para_add) > 0:
        c.extend.microsoft.add_members_to_groups(
            madms_mail_para_add,
            "CN=madms-mail-para,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    if len(madms_mail_para_del) > 0:
        c.extend.microsoft.remove_members_from_groups(
            madms_mail_para_del,
            "CN=madms-mail-para,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    

    #------------------------------madhs-mail-para------------------------------#
    madhs_mail_para_add = [i.entry_dn for i in users
        if "CN=madhs-mail-para,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "para".lower() in str(i.title.value).lower() and "High".lower() \
        in str(i.physicalDeliveryOfficeName.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value)]
    madhs_mail_para_del = [i.entry_dn for i in users
        if "CN=madhs-mail-para,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and (("para".lower() not in str(i.title.value).lower() or \
        "High".lower() not in str(i.physicalDeliveryOfficeName.value).lower()) \
        or ("514" in str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value)))]
    
    if len(madhs_mail_para_add) > 0:
        c.extend.microsoft.add_members_to_groups(
            madhs_mail_para_add,
            "CN=madhs-mail-para,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    if len(madhs_mail_para_del) > 0:
        c.extend.microsoft.remove_members_from_groups(
            madhs_mail_para_del,
            "CN=madhs-mail-para,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    

    #------------------------------madea-mail-teacher------------------------------#
    madea_mail_teacher_add = [i.entry_dn for i in users
        if "CN=madea-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and ("teacher".lower() in str(i.title.value).lower() or "principal".lower() in str(i.title.value).lower()) \
        and "Eastview".lower() in str(i.physicalDeliveryOfficeName.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value)]
    madea_mail_teacher_del = [i.entry_dn for i in users
        if "CN=madea-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and (("teacher".lower() not in str(i.title.value).lower() or "principal".lower() not in str(i.title.value).lower() \
        or "Eastview".lower() not in str(i.physicalDeliveryOfficeName.value).lower()) \
        or ("514" in str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value)))]

    if len(madea_mail_teacher_add) > 0:
        c.extend.microsoft.add_members_to_groups(
            madea_mail_teacher_add,
            "CN=madea-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    if len(madea_mail_teacher_del) > 0:
        c.extend.microsoft.remove_members_from_groups(
            madea_mail_teacher_del,
            "CN=madea-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    

    #------------------------------madmi-mail-teacher------------------------------#
    madmi_mail_teacher_add = [i.entry_dn for i in users
        if "CN=madmi-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and ("teacher".lower() in str(i.title.value).lower() or "principal".lower() in str(i.title.value).lower()) \
        and "Mifflin".lower() in str(i.physicalDeliveryOfficeName.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value)]
    madmi_mail_teacher_del = [i.entry_dn for i in users
        if "CN=madmi-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and (("teacher".lower() not in str(i.title.value).lower() or "principal".lower() not in str(i.title.value).lower() \
        or "Mifflin".lower() not in str(i.physicalDeliveryOfficeName.value).lower()) \
        or ("514" in str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value)))]

    if len(madmi_mail_teacher_add) > 0:
        c.extend.microsoft.add_members_to_groups(
            madmi_mail_teacher_add,
            "CN=madmi-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    if len(madmi_mail_teacher_del) > 0:
        c.extend.microsoft.remove_members_from_groups(
            madmi_mail_teacher_del,
            "CN=madmi-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    

    #------------------------------madso-mail-teacher------------------------------#
    madso_mail_teacher_add = [i.entry_dn for i in users
        if "CN=madso-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and ("teacher".lower() in str(i.title.value).lower() or "principal".lower() in str(i.title.value).lower()) \
        and "South".lower() in str(i.physicalDeliveryOfficeName.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value)]
    madso_mail_teacher_del = [i.entry_dn for i in users
        if "CN=madso-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and (("teacher".lower() not in str(i.title.value).lower() or "principal".lower() not in str(i.title.value).lower() \
        or "South".lower() not in str(i.physicalDeliveryOfficeName.value).lower()) \
        or ("514" in str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value)))]

    if len(madso_mail_teacher_add) > 0:
        c.extend.microsoft.add_members_to_groups(
            madso_mail_teacher_add,
            "CN=madso-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    if len(madso_mail_teacher_del) > 0:
        c.extend.microsoft.remove_members_from_groups(
            madso_mail_teacher_del,
            "CN=madso-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    

    #------------------------------madms-mail-teacher------------------------------#
    madms_mail_teacher_add = [i.entry_dn for i in users
        if "CN=madms-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and ("teacher".lower() in str(i.title.value).lower() or "principal".lower() in str(i.title.value).lower()) \
        and "Middle".lower() in str(i.physicalDeliveryOfficeName.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value)]
    madms_mail_teacher_del = [i.entry_dn for i in users
        if "CN=madms-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and (("teacher".lower() not in str(i.title.value).lower() or "principal".lower() not in str(i.title.value).lower() \
        or "Middle".lower() not in str(i.physicalDeliveryOfficeName.value).lower()) \
        or ("514" in str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value)))]

    if len(madms_mail_teacher_add) > 0:
        c.extend.microsoft.add_members_to_groups(
            madms_mail_teacher_add,
            "CN=madms-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    if len(madms_mail_teacher_del) > 0:
        c.extend.microsoft.remove_members_from_groups(
            madms_mail_teacher_del,
            "CN=madms-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    

    #------------------------------madhs-mail-teacher------------------------------#
    madhs_mail_teacher_add = [i.entry_dn for i in users
        if "CN=madhs-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and ("teacher".lower() in str(i.title.value).lower() or "principal".lower() in str(i.title.value).lower()) \
        and "High".lower() in str(i.physicalDeliveryOfficeName.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value)]
    madhs_mail_teacher_del = [i.entry_dn for i in users
        if "CN=madhs-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and (("teacher".lower() not in str(i.title.value).lower() or "principal".lower() not in str(i.title.value).lower() \
        or "High".lower() not in str(i.physicalDeliveryOfficeName.value).lower()) \
        or ("514" in str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value)))]

    if len(madhs_mail_teacher_add) > 0:
        c.extend.microsoft.add_members_to_groups(
            madhs_mail_teacher_add,
            "CN=madhs-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    if len(madhs_mail_teacher_del) > 0:
        c.extend.microsoft.remove_members_from_groups(
            madhs_mail_teacher_del,
            "CN=madhs-mail-teacher,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    

    #------------------------------madea-mail-user------------------------------#
    madea_mail_user_add = [i.entry_dn for i in users
        if "CN=madea-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "Eastview".lower() in str(i.physicalDeliveryOfficeName.value).lower() \
        and "514" not in str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value)]
    madea_mail_user_del = [i.entry_dn for i in users
        if "CN=madea-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("Eastview".lower() not in str(i.physicalDeliveryOfficeName.value).lower() \
        or ("514" in str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value)))]

    if len(madea_mail_user_add) > 0:
        c.extend.microsoft.add_members_to_groups(
            madea_mail_user_add,
            "CN=madea-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    if len(madea_mail_user_del) > 0:
        c.extend.microsoft.remove_members_from_groups(
            madea_mail_user_del,
            "CN=madea-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    

    #------------------------------madmi-mail-user------------------------------#
    madmi_mail_user_add = [i.entry_dn for i in users
        if "CN=madmi-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "Mifflin".lower() in str(i.physicalDeliveryOfficeName.value).lower() \
        and "514" not in str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value)]
    madmi_mail_user_del = [i.entry_dn for i in users
        if "CN=madmi-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("Mifflin".lower() not in str(i.physicalDeliveryOfficeName.value).lower() \
        or ("514" in str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value)))]

    if len(madmi_mail_user_add) > 0:
        c.extend.microsoft.add_members_to_groups(
            madmi_mail_user_add,
            "CN=madmi-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    if len(madmi_mail_user_del) > 0:
        c.extend.microsoft.remove_members_from_groups(
            madmi_mail_user_del,
            "CN=madmi-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    

    #------------------------------madso-mail-user------------------------------#
    madso_mail_user_add = [i.entry_dn for i in users
        if "CN=madso-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "South".lower() in str(i.physicalDeliveryOfficeName.value).lower() \
        and "514" not in str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value)]
    madso_mail_user_del = [i.entry_dn for i in users
        if "CN=madso-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("South".lower() not in str(i.physicalDeliveryOfficeName.value).lower() \
        or ("514" in str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value)))]

    if len(madso_mail_user_add) > 0:
        c.extend.microsoft.add_members_to_groups(
            madso_mail_user_add,
            "CN=madso-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    if len(madso_mail_user_del) > 0:
        c.extend.microsoft.remove_members_from_groups(
            madso_mail_user_del,
            "CN=madso-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    

    #------------------------------madms-mail-user------------------------------#
    madms_mail_user_add = [i.entry_dn for i in users
        if "CN=madms-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "Middle".lower() in str(i.physicalDeliveryOfficeName.value).lower() \
        and "514" not in str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value)]
    madms_mail_user_del = [i.entry_dn for i in users
        if "CN=madms-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("Middle".lower() not in str(i.physicalDeliveryOfficeName.value).lower() \
        or ("514" in str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value)))]

    if len(madms_mail_user_add) > 0:
        c.extend.microsoft.add_members_to_groups(
            madms_mail_user_add,
            "CN=madms-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    if len(madms_mail_user_del) > 0:
        c.extend.microsoft.remove_members_from_groups(
            madms_mail_user_del,
            "CN=madms-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    

    #------------------------------madhs-mail-user------------------------------#
    madhs_mail_user_add = [i.entry_dn for i in users
        if "CN=madhs-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "High".lower() in str(i.physicalDeliveryOfficeName.value).lower() \
        and "514" not in str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value)]
    madhs_mail_user_del = [i.entry_dn for i in users
        if "CN=madhs-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("High".lower() not in str(i.physicalDeliveryOfficeName.value).lower() \
        or ("514" in str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value)))]

    if len(madhs_mail_user_add) > 0:
        c.extend.microsoft.add_members_to_groups(
            madhs_mail_user_add,
            "CN=madhs-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    if len(madhs_mail_user_del) > 0:
        c.extend.microsoft.remove_members_from_groups(
            madhs_mail_user_del,
            "CN=madhs-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    

    #------------------------------madjb-mail-user------------------------------#
    madjb_mail_user_add = [i.entry_dn for i in users
        if "CN=madjb-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "Early Childhood".lower() in str(i.physicalDeliveryOfficeName.value).lower() \
        and "514" not in str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value)]
    madjb_mail_user_del = [i.entry_dn for i in users
        if "CN=madjb-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("Early Childhood".lower() not in str(i.physicalDeliveryOfficeName.value).lower() \
        or ("514" in str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value)))]

    if len(madjb_mail_user_add) > 0:
        c.extend.microsoft.add_members_to_groups(
            madjb_mail_user_add,
            "CN=madjb-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    if len(madjb_mail_user_del) > 0:
        c.extend.microsoft.remove_members_from_groups(
            madjb_mail_user_del,
            "CN=madjb-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    

    #------------------------------madea-mail-cook------------------------------#
    madea_mail_cook_add = [i.entry_dn for i in users
        if "CN=madea-mail-cook,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "cook".lower() in str(i.title.value).lower() and "Eastview".lower() \
        in str(i.physicalDeliveryOfficeName.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value)]
    madea_mail_cook_del = [i.entry_dn for i in users
        if "CN=madea-mail-cook,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("cook".lower() not in str(i.title.value).lower() or \
        "Eastview".lower() not in str(i.physicalDeliveryOfficeName.value).lower()) \
        or ("514" in str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value))]
    
    if len(madea_mail_cook_add) > 0:
        c.extend.microsoft.add_members_to_groups(
            madea_mail_cook_add,
            "CN=madea-mail-cook,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    if len(madea_mail_cook_del) > 0:
        c.extend.microsoft.remove_members_from_groups(
            madea_mail_cook_del,
            "CN=madea-mail-cook,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)


    #------------------------------madmi-mail-cook------------------------------#
    madmi_mail_cook_add = [i.entry_dn for i in users
        if "CN=madmi-mail-cook,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "cook".lower() in str(i.title.value).lower() and "Miflin".lower() \
        in str(i.physicalDeliveryOfficeName.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value)]
    madmi_mail_cook_del = [i.entry_dn for i in users
        if "CN=madmi-mail-cook,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and (("cook".lower() not in str(i.title.value).lower() or \
        "Miflin".lower() not in str(i.physicalDeliveryOfficeName.value).lower()) \
        or ("514" in str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value)))]
    
    if len(madmi_mail_cook_add) > 0:
        c.extend.microsoft.add_members_to_groups(
            madmi_mail_cook_add,
            "CN=madmi-mail-cook,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    if len(madmi_mail_cook_del) > 0:
        c.extend.microsoft.remove_members_from_groups(
            madmi_mail_cook_del,
            "CN=madmi-mail-cook,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    

    #------------------------------madso-mail-cook------------------------------#
    madso_mail_cook_add = [i.entry_dn for i in users
        if "CN=madso-mail-cook,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "cook".lower() in str(i.title.value).lower() and "South".lower() \
        in str(i.physicalDeliveryOfficeName.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value)]
    madso_mail_cook_del = [i.entry_dn for i in users
        if "CN=madso-mail-cook,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and (("cook".lower() not in str(i.title.value).lower() or \
        "South".lower() not in str(i.physicalDeliveryOfficeName.value).lower()) \
        or ("514" in str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value)))]
    
    if len(madso_mail_cook_add) > 0:
        c.extend.microsoft.add_members_to_groups(
            madso_mail_cook_add,
            "CN=madso-mail-cook,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    if len(madso_mail_cook_del) > 0:
        c.extend.microsoft.remove_members_from_groups(
            madso_mail_cook_del,
            "CN=madso-mail-cook,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    

    #------------------------------madms-mail-cook------------------------------#
    madms_mail_cook_add = [i.entry_dn for i in users
        if "CN=madms-mail-cook,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "cook".lower() in str(i.title.value).lower() and "Middle".lower() \
        in str(i.physicalDeliveryOfficeName.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value)]
    madms_mail_cook_del = [i.entry_dn for i in users
        if "CN=madms-mail-cook,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and (("cook".lower() not in str(i.title.value).lower() or \
        "Middle".lower() not in str(i.physicalDeliveryOfficeName.value).lower()) \
        or ("514" in str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value)))]
    
    if len(madms_mail_cook_add) > 0:
        c.extend.microsoft.add_members_to_groups(
            madms_mail_cook_add,
            "CN=madms-mail-cook,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    if len(madms_mail_cook_del) > 0:
        c.extend.microsoft.remove_members_from_groups(
            madms_mail_cook_del,
            "CN=madms-mail-cook,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    

    #------------------------------madhs-mail-cook------------------------------#
    madhs_mail_cook_add = [i.entry_dn for i in users
        if "CN=madhs-mail-cook,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "cook".lower() in str(i.title.value).lower() and "High".lower() \
        in str(i.physicalDeliveryOfficeName.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value)]
    madhs_mail_cook_del = [i.entry_dn for i in users
        if "CN=madhs-mail-cook,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and (("cook".lower() not in str(i.title.value).lower() or \
        "High".lower() not in str(i.physicalDeliveryOfficeName.value).lower()) \
        or ("514" in str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value)))]
    
    if len(madhs_mail_cook_add) > 0:
        c.extend.microsoft.add_members_to_groups(
            madhs_mail_cook_add,
            "CN=madhs-mail-cook,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    if len(madhs_mail_cook_del) > 0:
        c.extend.microsoft.remove_members_from_groups(
            madhs_mail_cook_del,
            "CN=madhs-mail-cook,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    

    #------------------------------madms-halo------------------------------#
    madms_halo_add = [i.entry_dn for i in users
        if "CN=madms-halo,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "halo".lower() in str(i.department.value).lower() and "middle".lower() \
        in str(i.physicalDeliveryOfficeName.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value)]
    madms_halo_del = [i.entry_dn for i in users
        if "CN=madms-halo,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and (("halo".lower() not in str(i.department.value).lower() or \
        "middle".lower() not in str(i.physicalDeliveryOfficeName.value).lower()) \
        or ("514" in str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value)))]

    if len(madms_halo_add) > 0:
        c.extend.microsoft.add_members_to_groups(
            madms_halo_add,
            "CN=madms-halo,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    if len(madms_halo_del) > 0:
        c.extend.microsoft.remove_members_from_groups(
            madms_halo_del,
            "CN=madms-halo,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    

    #------------------------------madhs-halo------------------------------#
    madhs_halo_add = [i.entry_dn for i in users
        if "CN=madhs-halo,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "halo".lower() in str(i.department.value).lower() and "high".lower() \
        in str(i.physicalDeliveryOfficeName.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value)]
    madhs_halo_del = [i.entry_dn for i in users
        if "CN=madhs-halo,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and (("halo".lower() not in str(i.department.value).lower() or \
        "high".lower() not in str(i.physicalDeliveryOfficeName.value).lower()) \
        or ("514" in str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value)))]

    if len(madhs_halo_add) > 0:
        c.extend.microsoft.add_members_to_groups(
            madhs_halo_add,
            "CN=madhs-halo,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    if len(madhs_halo_del) > 0:
        c.extend.microsoft.remove_members_from_groups(
            madhs_halo_del,
            "CN=madhs-halo,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)


    #------------------------------mlea------------------------------#
    mlea_add = [i.entry_dn for i in users
        if "CN=mlea,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "mlea".lower() in str(i.department.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value)]
    mlea_del = [i.entry_dn for i in users
        if "CN=mlea,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("mlea".lower() not in str(i.department.value).lower() \
        or ("514" in str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value)))]
    
    if len(mlea_add) > 0:
        c.extend.microsoft.add_members_to_groups(
            mlea_add,
            "CN=mlea,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    if len(mlea_del) > 0:
        c.extend.microsoft.remove_members_from_groups(
            mlea_del,
            "CN=mlea,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)


    #------------------------------oapse------------------------------#
    oapse_add = [i.entry_dn for i in users
        if "CN=oapse,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "oapse".lower() in str(i.department.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value)]
    oapse_del = [i.entry_dn for i in users
        if "CN=oapse,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("oapse".lower() not in str(i.department.value).lower() \
        or ("514" in str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value)))]
    
    if len(oapse_add) > 0:
        c.extend.microsoft.add_members_to_groups(
            oapse_add,
            "CN=oapse,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    if len(oapse_del) > 0:
        c.extend.microsoft.remove_members_from_groups(
            oapse_del,
            "CN=oapse,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)


    #------------------------------slo-trainers------------------------------#
    slo_trainers_add = [i.entry_dn for i in users
        if "CN=slo-trainers,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "SLO".lower() in str(i.department.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value)]
    slo_trainers_del = [i.entry_dn for i in users 
        if "CN=slo-trainers,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("SLO".lower() not in str(i.department.value).lower() \
        or ("514" in str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value)))]

    if len(slo_trainers_add) > 0:
        c.extend.microsoft.add_members_to_groups(
            slo_trainers_add,
            "CN=slo-trainers,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    if len(slo_trainers_del) > 0:
        c.extend.microsoft.remove_members_from_groups(
            slo_trainers_del,
            "CN=slo-trainers,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)


    #------------------------------titleixcoordinator------------------------------#
    titleixcoordinator_add = [i.entry_dn for i in users
        if "CN=titleixcoordinator,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "Title IX".lower() in str(i.department.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value)]
    titleixcoordinator_del = [i.entry_dn for i in users
        if "CN=titleixcoordinator,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("Title IX".lower() not in str(i.department.value).lower() \
        or ("514" in str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value)))]

    if len(titleixcoordinator_add) > 0:
        c.extend.microsoft.add_members_to_groups(
            titleixcoordinator_add,
            "CN=titleixcoordinator,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    if len(titleixcoordinator_del) > 0:
        c.extend.microsoft.remove_members_from_groups(
            titleixcoordinator_del,
            "CN=titleixcoordinator,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)


    #------------------------------Helpdesk------------------------------#
    helpdesk_add = [i.entry_dn for i in users
        if "CN=Helpdesk,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "Technology Office".lower() in str(i.physicalDeliveryOfficeName.value).lower() \
        and "514" not in str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value)]
    helpdesk_del = [i.entry_dn for i in users
        if "CN=Helpdesk,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("Technology Office".lower() not in str(i.physicalDeliveryOfficeName.value).lower() \
        or ("514" in str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value)))]

    if len(helpdesk_add) > 0:
        c.extend.microsoft.add_members_to_groups(
            helpdesk_add,
            "CN=Helpdesk,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    if len(helpdesk_del) > 0:
        c.extend.microsoft.remove_members_from_groups(
            helpdesk_del,
            "CN=Helpdesk,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)


    #------------------------------mad-mail-emis------------------------------#
    mad_mail_emis_add = [i.entry_dn for i in users
        if "CN=mad-mail-emis,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "EMIS".lower() in str(i.department.value).lower() \
        and "514" not in str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value)]
    mad_mail_emis_del = [i.entry_dn for i in users
        if "CN=mad-mail-emis,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("EMIS".lower() not in str(i.department.value).lower() \
        or ("514" in str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value)))]

    if len(mad_mail_emis_add) > 0:
        c.extend.microsoft.add_members_to_groups(
            mad_mail_emis_add,
            "CN=mad-mail-emis,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    if len(mad_mail_emis_del) > 0:
        c.extend.microsoft.remove_members_from_groups(
            mad_mail_emis_del,
            "CN=mad-mail-emis,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)


    #------------------------------mad-mail-ps------------------------------#
    mad_mail_ps_add = [i.entry_dn for i in users
        if "CN=mad-mail-ps,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "Preschool".lower() in str(i.department.value).lower() \
        and "514" not in str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value)]
    mad_mail_ps_del = [i.entry_dn for i in users
        if "CN=mad-mail-ps,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("Preschool".lower() not in str(i.department.value).lower() \
        or ("514" in str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value)))]
    
    if len(mad_mail_ps_add) > 0:
        c.extend.microsoft.add_members_to_groups(
            mad_mail_ps_add,
            "CN=mad-mail-ps,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    if len(mad_mail_ps_del) > 0:
        c.extend.microsoft.remove_members_from_groups(
            mad_mail_ps_del,
            "CN=mad-mail-ps,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)


    #------------------------------mad-mail-tech------------------------------#
    mad_mail_tech_add = [i.entry_dn for i in users
        if "CN=mad-mail-tech,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "Technology Office".lower() in str(i.physicalDeliveryOfficeName.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value)]
    mad_mail_tech_del = [i.entry_dn for i in users
        if "CN=mad-mail-tech,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("Technology Office".lower() not in str(i.physicalDeliveryOfficeName.value).lower() \
        or ("514" in str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value)))]

    if len(mad_mail_tech_add) > 0:
        c.extend.microsoft.add_members_to_groups(
            mad_mail_tech_add,
            "CN=mad-mail-tech,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    if len(mad_mail_tech_del) > 0:
        c.extend.microsoft.remove_members_from_groups(
            mad_mail_tech_del,
            "CN=mad-mail-tech,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)


    #------------------------------madbo-mail-user------------------------------#
    madbo_mail_user_add = [i.entry_dn for i in users
        if "CN=madbo-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and "Administration Office".lower() in str(i.physicalDeliveryOfficeName.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value)]
    madbo_mail_user_del = [i.entry_dn for i in users
        if "CN=madbo-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and ("Administration Office".lower() not in str(i.physicalDeliveryOfficeName.value).lower() \
        or ("514" in str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value)))]

    if len(madbo_mail_user_add) > 0:
        c.extend.microsoft.add_members_to_groups(
            madbo_mail_user_add,
            "CN=madbo-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    if len(madbo_mail_user_del) > 0:
        c.extend.microsoft.remove_members_from_groups(
            madbo_mail_user_del,
            "CN=madbo-mail-user,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)


    #------------------------------madelem-mail-sped------------------------------#
    madelem_mail_sped_add = [i.entry_dn for i in users
        if "CN=madelem-mail-sped,OU=Groups,OU=Madison,DC=mlsd,DC=local" not in str(i.memberOf.value) \
        and ("Eastview".lower() in str(i.physicalDeliveryOfficeName.value).lower() or \
        "Mifflin".lower() in str(i.physicalDeliveryOfficeName.value).lower() or \
        "South".lower() in str(i.physicalDeliveryOfficeName.value).lower()) \
        and "Intervention".lower() in str(i.department.value).lower() and "514" not in \
        str(i.userAccountControl.value) and "546" not in str(i.userAccountControl.value)]
    madelem_mail_sped_del = [i.entry_dn for i in users
        if "CN=madelem-mail-sped,OU=Groups,OU=Madison,DC=mlsd,DC=local" in str(i.memberOf.value) \
        and (("Eastview".lower() not in str(i.physicalDeliveryOfficeName.value).lower() or \
        "Mifflin".lower() not in str(i.physicalDeliveryOfficeName.value).lower() or \
        "South".lower() not in str(i.physicalDeliveryOfficeName.value).lower()) or \
        "Intervention".lower() not in str(i.department.value).lower() \
        or ("514" in str(i.userAccountControl.value) or "546" in str(i.userAccountControl.value)))]

    if len(madelem_mail_sped_add) > 0:
        c.extend.microsoft.add_members_to_groups(
            madelem_mail_sped_add,
            "CN=madelem-mail-sped,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)
    if len(madelem_mail_sped_del) > 0:
        c.extend.microsoft.remove_members_from_groups(
            madelem_mail_sped_del,
            "CN=madelem-mail-sped,OU=Groups,OU=Madison,DC=mlsd,DC=local"
            )
    time.sleep(0.250)


    c.unbind()

    # Connects to madhs01gcds server via SSH and runs a Google Sync
    stdin, stdout, stderr = gcds.exec_command("C:\Tools\gcds.cmd")
    for line in stdout:
        print(Color.YELLOW + line.strip("\n") + Color.END)

    

cred()
main(c, gcds, users)
