#!/usr/bin/env python

import sqlite3, datetime, logging as log

DB_FILE='Tasks.db'
SQL_CREATE="""create table tasks(
id integer primary key autoincrement,
url text not null,
output text not null,
`order` integer,
total long,
done long,
state long,
current integer,
average integer,
left integer,
used integer,
thsize integer,
thdone text,
maxspeed integer,
headers text,
speed integer,
update_time timestamp default current_timestamp,
errmsg text,
downloads text,
ua text)
"""

def reset_database():
    dbc = sqlite3.connect(DB_FILE)
    cursor = dbc.cursor()
    cursor.execute("drop table if exists tasks")
    cursor.execute(SQL_CREATE)
    dbc.commit()
    dbc.close()

def select_tasks(**kwargs):
    dbc = sqlite3.connect(DB_FILE)
    cursor = dbc.cursor()
    SQL = "select * from tasks"
    

    if kwargs:
        SQL += " where "
        for key, value in kwargs.items():
            if type(value) is int:
                SQL += " `%s` = %s " % (key, value)
            else:
                SQL += " `%s` %s " % (key, value)
    
    SQL += " order by `order`, `id`"
    log.debug(SQL)
    cursor.execute(SQL)
    dbc.commit()
    tasks = []
    for row in cursor:
        tasks.append({"id": row[0], 
                      "url": row[1], 
                      "output": row[2], 
                      "order": row[3], 
                      "total": row[4], 
                      "done": row[5], 
                      "state": row[6], 
                      "current": row[7], 
                      "average": row[8], 
                      "left": row[9], 
                      "used": row[10], 
                      "thsize": row[11], 
                      "thdone": row[12],
                      "maxspeed": row[13],
                      "headers": row[14],
                      "speed": row[15],
                      "update_time": row[16],
                      "errmsg": row[17],
                      "downloads": row[18],
                      "ua": row[19]})
    dbc.close()
    return tasks

def insert_task(**kwargs):
    if not kwargs:
        return

    dbc = sqlite3.connect(DB_FILE)
    cursor = dbc.cursor()
    
    columns = list()
    values = list()
    for key, value in kwargs.items():
        columns.append("`%s`" % key)
        values.append("%s" % value if type(value) is int else "'%s'" % value)
    columns.append("`update_time`")
    values.append("'%s'" % datetime.datetime.now())
    columns = ", ".join(columns)
    values = ", ".join(values)
    SQL = "insert into tasks (%s) values (%s)" % (columns, values)
    log.debug(SQL)
    cursor.execute(SQL)
    dbc.commit()
    tid = cursor.lastrowid
    dbc.close()
    return tid

def delete_tasks(ids):
    if not ids:
        return

    dbc = sqlite3.connect(DB_FILE)
    cursor = dbc.cursor()
    
    SQL = "delete from tasks where "
    SQL += " id = %s " % ids if type(ids) is int else \
        " id in (%s) " % ", ".join([str(did) for did in ids])

    log.debug(SQL)
    cursor.execute(SQL)
    dbc.commit()
    dbc.close()

def update_tasks(dids, **kwargs):
    if not dids or not kwargs:
        return

    dbc = sqlite3.connect(DB_FILE)
    cursor = dbc.cursor()

    SQL = "update tasks set "

    sets = []
    for key, value in kwargs.items():
        sets.append(" `%s` = %s " % (key, value) if type(value) is int else \
            " `%s` = '%s' " % (key, value))
    sets.append(" `update_time` = '%s' " % datetime.datetime.now())
    SQL += ",".join(sets)

    SQL += " where id = %s " % dids if type(dids) is int else \
        " where id in (%s) " % ", ".join([str(did) for did in dids])

    log.debug(SQL)
    cursor.execute(SQL)
    dbc.commit()
    dbc.close()

def test_select():
    return select_tasks(**{'output':"like \'%CentOS%\'"})

def test_create():
    return insert_task(**{'url': 'http://mirrors.163.com/centos/6.2/isos/x86_64/CentOS-6.2-x86_64-LiveCD.iso', 'output':'CentOS-6.2-x86_64-LiveCD.iso'})

def test_update():
    return update_task([1,2], **{'state':3})

def test_delete():
    return delete_task([1, 2])

def test():
    #print 'test create new task'
    #print test_create()

    #print 'test update tasks'
    #print test_update()

    print 'test delete task'
    print test_delete()

    print 'test select tasks:'
    print test_select()

if __name__ == '__main__':
    reset_database()
