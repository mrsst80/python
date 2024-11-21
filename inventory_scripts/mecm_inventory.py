#!/usr/bin/env python3
import argparse 
import os
import json
import re
import sys
import configparser

'''
dynamic inventory script read data from mecm mssql database. Requires freetds setup. login_host, login_user and dbname need to be changed to match your environment. For login_password you need to set environment variable MECM_DB_PASSWORD.
'''

PYODBC_IMP_ERR = None
try:
    import pyodbc
except ImportError:
    PYODBC_IMP_ERR = traceback.format_exc()
    pyodbc_found = False
else:
    pyodbc_found = True

if not pyodbc_found:
    exit(missing_required_lib('pyodbc', PYODBC_IMP_ERR))

sql_query = """
select 
    v_R_System.Netbios_Name0, osinfo.Caption0, v_GS_SERVERCIS.LOB0, v_GS_SERVERCIS.Environment0
FROM 
    v_R_System
    LEFT JOIN 
    (
        SELECT DISTINCT ResourceID, BuildNumber0, Caption0, TotalVisibleMemorySize0, LastBootUpTime0,  [TimeStamp], row_number() over (partitiON by ResourceID order by [TimeStamp] desc) AS rn
        FROM v_GS_OPERATING_SYSTEM
    ) 
    AS osinfo ON v_R_System.ResourceID  = osinfo.ResourceID and rn=1
    LEFT JOIN v_GS_SERVERCIS
    ON v_R_System.ResourceID = v_GS_SERVERCIS.ResourceID
WHERE 
    osinfo.Caption0 LIKE '%Server%' AND
    osinfo.Caption0 NOT LIKE '%2008%'
"""

# Define connections credentials
#db_cyberark_cmd = ""
login_host = ""
login_port = "1433"
login_user = ""
dbname = ""

def obtain_db_password():
    # user cyberark agent
    #db_password = os.popen(db_cyberark_cmd).read().strip()

    # use environment variable in AWX
    db_password = os.environ.get("MECM_DB_PASSWORD")

    return db_password

def connect_to_database():
    login_password = obtain_db_password()

    try:
        conn = pyodbc.connect(DRIVER='{FreeTDS}', SERVER=login_host, PORT=login_port, UID=login_user, PWD=login_password, DATABASE=dbname)
    except pyodbc.Error as e:
        print("unable to connect, check login_user and login_password are correct, or alternatively check your @sysconfdir@/freetds.conf / ${HOME}/.freetds.conf")
        exit(1)

    cursor = conn.cursor()
    cursor.execute(sql_query)
    rows = cursor.fetchall()
    conn.close()

    return rows    

def create_inventory(hosts_list):
    inventory = {'_meta': {'hostvars': {}}}

    for line in hosts_list:
        lob = line[2]
        env = line[3]
        result = re.search(r"(\d{4})", line[1])
        if result is None:
            version = "uknown"
        else:
            version = result.group(1)
        if lob not in inventory:
            inventory[lob] = {'hosts': []}
        if env not in inventory:
            inventory[env] = {'hosts': []}
        if version not in inventory:
            inventory[version] = {'hosts': []}

        inventory[env]['hosts'].append(line[0])
        inventory[lob]['hosts'].append(line[0])
        inventory[version]['hosts'].append(line[0])
    
    return inventory

def ini_inventory(inventory, config_name):
    config = configparser.ConfigParser(allow_no_value=True)

    for key in inventory.keys():
        if key == "hostvars":
            continue
        config.add_section(str(key))

        for host in inventory[key]:
            if host == "hostvars":
                continue
            for hostname in inventory[key]['hosts']:
                #print(hostname)
                config.set(key, hostname)

    with open(config_name, 'w') as configfile:
        config.write(configfile)

    return 0

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser( description=__doc__, prog=__file__)
    mandatory_options = arg_parser.add_mutually_exclusive_group()
    mandatory_options.add_argument('--list', action='store', nargs="*", help="Get inventory JSON from our DB")
    mandatory_options.add_argument('--host', action='store',
                                   help="Get variables for specific host, not used but kept for compatability")
    mandatory_options.add_argument('--ini', action='store', nargs="*", help="Create ini formated inventory")
    args = arg_parser.parse_args()

    if args.host:
       print('{"_meta":{}}')
       sys.stderr.write('This script already provides _meta via --list, so this option is really ignored')
    elif type(args.list) is list:
       hosts_list = connect_to_database()
       print(json.dumps(create_inventory(hosts_list), indent=True))
    elif type(args.ini) is list:
        config_name = "inventory.mecm"
        hosts_list = connect_to_database()
        inventory = create_inventory(hosts_list)
        inventory = create_inventory(hosts_list)
        ini_inventory(inventory, config_name)
    else:
       raise ValueError("Valid options are --list or --host <HOSTNAME>")
