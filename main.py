import pymysql

MyDB = pymysql.connect(user='root', host='127.0.0.1', password='TeamSpirit2021', db='logistics')
cursor = MyDB.cursor()

def insert_keklol_truck(connection, cost):
    cursor = connection.cursor()
    cursor.execute('SELECT Id FROM Cargo_types WHERE Type = "сыпучий"')
    cargo_type_id = cursor.fetchone()[0]
    cursor.execute('INSERT INTO Trucks (Cargo_type_Id, Carrying_capacity, Cost, '
                   'Downtime_costs, Route_costs, Empty_costs) '
                   f'VALUES ({cargo_type_id}, 1337, {cost}, 3, 2, 1)')
    connection.commit()

if __name__ == '__main__':
    MyDB = pymysql.connect(user='root', host='127.0.0.1', password='TeamSpirit2021', db='logistics')
    insert_cargo_types(MyDB)
    insert_rates(MyDB)
    cursor.execute('SELECT Id FROM Cargo_types')
    cargo_type = cursor.fetchall()
    print(cargo_type)
