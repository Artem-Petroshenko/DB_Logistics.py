import datetime
import pymysql

MyDB = pymysql.connect(user='root',
                       host='127.0.0.1',
                       password='TeamSpirit2021',
                       db='logistics',
                       charset='utf8mb4')

def insert_sell_truck(connection, truck_id, customer, date):
    cur = connection.cursor()
    cur.execute(f'SELECT Cost FROM Trucks WHERE Id = {truck_id}')
    cost = cur.fetchone()[0]
    cur.execute('INSERT INTO Sell_truck (Cost, Customer, Date) '
                f'VALUES ({cost}, "{customer}", "{date}")')
    connection.commit()

def update_protocols(connection, truck_id):
    cur = connection.cursor()
    cur.execute('UPDATE Protocol_truck_city '
                f'SET End_downtime = "{datetime.date.today()}" '
                f'WHERE Truck_Id = {truck_id} AND End_downtime IS NULL')
    connection.commit()

def update_truck(connection, truck_id):
    cur = connection.cursor()
    cur.execute('UPDATE Trucks '
                'SET Sold = 1 '
                f'WHERE Id = {truck_id}')
    connection.commit()
