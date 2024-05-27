#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '0.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: mssql_query
short_description: sql query to mssql server
version_added: "1.0.0"
description: 
    - This modules executes sql queries on mssql server.
    - Supported standard sql queries and calling stored procedures. 
    - To achieve indempotency there is a option sql_query_check, where you can specity sql query, which if returns result the task will be marked as not changed and the main sql query will not be executed.
author:
    - Stefan Stefanov (@mrsst80)
requirements:
    - pyodbc
    - FreeTDS
options:
    dbname:
        description: Name of the MSSQL database.
        required: true
        type: str
    autocommit:
        description: pyodbc autocommit 
        required: false
        type: bool
    query_type:
        description: SQL query type.
        required: true
        choices: [ 'procedure', 'select', 'insert', 'update']
        type: str
    login_user:
        description: User to connect to MSSQL server
        required: true
        type: str
    login_password:
        description: Password to connect to MSSQL server
        required: true
        type: str
    login_hostname:
        description: Hostname of MSSQL server
        required: true
        type: str
    sql_query:
        description: SQL query 
        required: true
        type: str 
    sql_query_check:
        description: SQL query check for idempotency 
        required: false
        type: str 
'''

EXAMPLES = r'''
# Pass in a message
    - name: Execute SQL procedure
      mssql_query:
        dbname: database_name
        autocommit: true
        query_type: procedure
        login_user: db_username
        login_password: db_password
        login_host: mssql_hostname
        sql_query: sql_procedure_name
        sql_query_check: select_query
      delegate_to: localhost
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
original_message:
    description: The original name param that was passed in.
    type: str
    returned: always
    sample: 'hello world'
message:
    description: The output message that the test module generates.
    type: str
    returned: always
    sample: 'goodbye'
my_useful_info:
    description: The dictionary containing information about your system.
    type: dict
    returned: always
    sample: {
        'foo': 'bar',
        'answer': 42,
    }
'''


import os
import traceback

PYODBC_IMP_ERR = None
try:
    import pyodbc
except ImportError:
    PYODBC_IMP_ERR = traceback.format_exc()
    pyodbc_found = False
else:
    pyodbc_found = True

from ansible.module_utils.basic import AnsibleModule, missing_required_lib

def db_query(conn, cursor, query):
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.commit()
    return rows

def db_query_check(conn, cursor, query):
    cursor.execute(query)
    rows = cursor.fetchone()
    return rows

def db_procedure(conn, cursor, query):
    try:
        cursor.execute(query)
    except pyodbc.Error as s:
        print(f'sqlerror: {s}')

    rows = cursor.rowcount
    if rows == -1:
        rows = cursor.fetchall()

    return rows

def run_module():
    module = AnsibleModule(
        argument_spec=dict(
            dbname=dict(required=True),
            sql_query=dict(required=True),
            sql_query_check=dict(default=''),
            query_type=dict(
                default='select', choices=['select', 'procedure', 'insert', 'update']),
            login_user=dict(default=''),
            login_password=dict(default='', no_log=True),
            login_host=dict(required=True),
            login_port=dict(default='1433'),
            autocommit=dict(type='bool', default=False),
            state=dict(
                default='present', choices=['present', 'absent', 'import'])
        )
    )

    if not pyodbc_found:
        module.fail_json(msg=missing_required_lib('pyodbc'), exception=PYODBC_IMP_ERR)

    dbname = module.params['dbname']
    state = module.params['state']
    autocommit = module.params['autocommit']
    sql_query = module.params['sql_query']
    sql_query_check = module.params['sql_query_check']
    query_type = module.params['query_type']
    login_user = module.params['login_user']
    login_password = module.params['login_password']
    login_host = module.params['login_host']
    login_port = module.params['login_port']

    if login_user != "" and login_password == "":
        module.fail_json(msg="when supplying login_user arguments login_password must be provided")

    try:
        if autocommit:
            conn = pyodbc.connect(DRIVER='{FreeTDS}', SERVER=login_host, PORT=login_port, UID=login_user, PWD=login_password, DATABASE=dbname, autocommit=True)
        else:
            conn = pyodbc.connect(DRIVER='{FreeTDS}', SERVER=login_host, PORT=login_port, UID=login_user, PWD=login_password, DATABASE=dbname)

        cursor = conn.cursor()
    except pyodbc.Error as e:
            module.fail_json(msg="unable to connect, check login_user and login_password are correct, or alternatively check your "
                                 "@sysconfdir@/freetds.conf / ${HOME}/.freetds.conf")

    changed = False

    if sql_query_check:
      rows = db_query_check(conn, cursor, sql_query_check)
      if rows:
        module.exit_json(changed=changed)

    if query_type == 'procedure':
        rows = db_procedure(conn, cursor, sql_query)
        if rows == 0:
            rows = "Stored prodecure executed successfully."
            changed = True
            module.exit_json(changed=changed, rows=rows)
    else:
        rows = [list(row) for row in db_query(conn, cursor, sql_query)]

    conn.close()

    if (rows):
        changed = True
        module.exit_json(changed=changed, rows=rows)
    else:
        module.fail_json(msg="No rows")

    module.exit_json(changed=changed, dbname=dbname)

def main():
    run_module()

if __name__ == '__main__':
    main()
