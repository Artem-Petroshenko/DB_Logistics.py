import time

import pymysql
import random
import string
from time import perf_counter_ns

MyDB = pymysql.connect(user='root',
                       host='127.0.0.1',
                       password='TeamSpirit2021',
                       db='logistics',
                       charset='utf8mb4')

def random_varchar(length):
    letters = string.ascii_letters
    rand_varchar = ''.join(random.choice(letters) for i in range(length))
    return rand_varchar

def drop_to_start(connection, rownum):
    cur = connection.cursor()
    cur.execute('DROP TABLE IF EXISTS logistics.research;')
    cur.execute('CREATE TABLE Research'
                '('
                '    Id INT PRIMARY KEY AUTO_INCREMENT, '
                '    Name VARCHAR(5), '
                '    Number INT'
                ');')
    for i in range(rownum):
        cur.execute('INSERT INTO Research (Name, Number) '
                    f'VALUES ("{random_varchar(random.randint(1, 5))}", {random.randint(1, rownum)})')
    connection.commit()

def research(connection):
    cur = connection.cursor()
    for n in (1000, 10000, 100000):
        drop_to_start(connection, n)
        key_search(cur, n)
        non_key_search(cur, n)
        mask_search(cur, 'a%b', n)

        drop_to_start(connection, n)
        insert_row(cur, n)

        drop_to_start(connection, n)
        insert_row_group(cur, n)

        drop_to_start(connection, n)
        key_alter(cur, n)

        drop_to_start(connection, n)
        non_key_alter(cur, n)

        drop_to_start(connection, n)
        key_delete(cur, n)

        drop_to_start(connection, n)
        non_key_delete(cur, n)

        drop_to_start(connection, n)
        group_delete(cur, n)

        drop_to_start(connection, n)
        compress_200_del(cur, n)

        drop_to_start(connection, n)
        compress_200_remain(cur, n)
        print('\n\n')

def key_search(cur, rownum):
    for i in range(100):
        random.seed()
        cur.execute(f'SELECT * FROM Research WHERE Id = {random.randint(1, rownum)}')
    start = time.perf_counter_ns()
    for i in range(100):
        random.seed()
        cur.execute(f'SELECT * FROM Research WHERE Id = {random.randint(1, rownum)}')
    timer = time.perf_counter_ns() - start
    timer /= 100
    print("Key search time on", rownum, "elements is:", timer / 1000000)

def non_key_search(cur, rownum):
    start = time.perf_counter_ns()
    for i in range(100):
        random.seed()
        cur.execute(f'SELECT * FROM Research WHERE Number = {random.randint(1, rownum)}')
    timer = time.perf_counter_ns() - start
    timer /= 100
    print("Non key search time on", rownum, "elements is:", timer / 1000000)

def mask_search(cur, mask, rownum):
    start = time.perf_counter_ns()
    for i in range(100):
        cur.execute(f'SELECT * FROM Research WHERE Name LIKE "{mask}"')
    timer = time.perf_counter_ns() - start
    timer /= 100
    print("Mask search time on", rownum, "elements is:", timer / 1000000)

def insert_row(cur, rownum):
    start = time.perf_counter_ns()
    for i in range(100):
        cur.execute('INSERT INTO research (Name, Number) '
                    f'VALUES ("{random_varchar(4)}", {random.randint(1, rownum)})')
    timer = time.perf_counter_ns() - start
    timer /= 100
    print("Row insertion time on", rownum, "elements is:", timer / 1000000)

def insert_row_group(cur, rownum):
    start = time.perf_counter_ns()
    for i in range(100):
        for j in range(200):
            cur.execute('INSERT INTO research (Name, Number) '
                        f'VALUES ("{random_varchar(4)}", {random.randint(1, rownum)})')
    timer = time.perf_counter_ns() - start
    timer /= 100
    print("Group of rows insertion time on", rownum, "elements is:", timer / 1000000)

def key_alter(cur, rownum):
    start = time.perf_counter_ns()
    for i in range(100):
        random.seed()
        cur.execute('UPDATE research '
                    f'SET Number = 62 '
                    f'WHERE Id = {random.randint(1, rownum)}')
    timer = time.perf_counter_ns() - start
    timer /= 100
    print("Key altering time on", rownum, "elements is:", timer / 1000000)

def non_key_alter(cur, rownum):
    start = time.perf_counter_ns()
    for i in range(100):
        random.seed()
        cur.execute('UPDATE research '
                    f'SET Number = 62 '
                    f'WHERE Number = {random.randint(1, rownum)}')
    timer = time.perf_counter_ns() - start
    timer /= 100
    print("Non key altering time on", rownum, "elements is:", timer / 1000000)

def key_delete(cur, rownum):
    start = time.perf_counter_ns()
    for i in range(100):
        random.seed()
        cur.execute('DELETE FROM research '
                    f'WHERE Id = {random.randint(1, rownum)}')
    timer = time.perf_counter_ns() - start
    timer /= 100
    print("Key deleting time on", rownum, "elements is:", timer / 1000000)

def non_key_delete(cur, rownum):
    start = time.perf_counter_ns()
    for i in range(100):
        random.seed()
        cur.execute('DELETE FROM research '
                    f'WHERE Number = {random.randint(1, rownum)}')
    timer = time.perf_counter_ns() - start
    timer /= 100
    print("Non key deleting time on", rownum, "elements is:", timer / 1000000)

def group_delete(cur, rownum):
    start = time.perf_counter_ns()
    cur.execute('DELETE FROM research '
                'LIMIT 200')
    timer = time.perf_counter_ns() - start
    print("Group deleting time on", rownum, "elements is:", timer / 1000000)

def compress_200_del(cur, rownum):
    start = time.perf_counter_ns()
    cur.execute('ALTER TABLE research ROW_FORMAT = COMPRESSED')
    timer = time.perf_counter_ns() - start
    print("Compress DB after deleting 200 elements time on", rownum, "elements is:", timer / 1000000)

def compress_200_remain(cur, rownum):
    cur.execute('DELETE FROM research '
                f'LIMIT {rownum - 200}')
    start = time.perf_counter_ns()
    cur.execute('ALTER TABLE research ROW_FORMAT = COMPRESSED')
    timer = time.perf_counter_ns() - start
    print("Compress DB after remaining 200 elements time on", rownum, "elements is:", timer / 1000000)

if __name__ == '__main__':
    research(MyDB)
