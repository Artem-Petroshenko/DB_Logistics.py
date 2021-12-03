import pymysql

MyDB = pymysql.connect(user='root',
                       host='127.0.0.1',
                       password='TeamSpirit2021',
                       db='logistics',
                       charset='utf8mb4')

def insert_truck(connection, register_number, price, capacity, cargo_type_id, downtime_costs, route_costs, empty_costs):
    cur = connection.cursor()
    try:
        cur.execute(f'SELECT Id FROM Trucks WHERE Register_number = "{register_number}"')
        id = cur.fetchone()[0]
    except:
        cur.execute('INSERT INTO Trucks (Register_number, Cargo_type_Id, Carrying_capacity, Cost, '
                    'Downtime_costs, Route_costs, Empty_costs, Sold) '
                    f'VALUES ("{register_number}", {cargo_type_id}, {capacity}, {price}, {downtime_costs}, '
                    f'{route_costs}, {empty_costs}, 0)')
    else:
        cur.execute('UPDATE Trucks '
                    f'SET Sold = 0, Cargo_type_Id = {cargo_type_id}, Carrying_capacity = {capacity}, '
                    f'Cost = {price}, Downtime_costs = {downtime_costs}, Route_costs = {route_costs}, '
                    f'Empty_costs = {empty_costs}'
                    f'WHERE Id = {id}')
    connection.commit()

def insert_purchase(connection, price, seller, date, register_number):
    cur = connection.cursor()
    try:
        cur.execute(f'SELECT Id FROM Trucks WHERE Register_number = "{register_number}"')
    except:
        cur.execute('SELECT Max(Id) FROM Trucks')
    truck_id = cur.fetchone()[0]
    cur.execute('INSERT INTO Buy_truck (Seller, Date, Cost, Truck_Id) ' 
                f'VALUES ("{seller}", "{date}", {price}, {truck_id})')
    connection.commit()

def insert_protocol(connection, city_id, date, register_number):
    cur = connection.cursor()
    try:
        cur.execute(f'SELECT Id FROM Trucks WHERE Register_number = "{register_number}"')
    except:
        cur.execute('SELECT Max(Id) FROM Trucks')
    truck_id = cur.fetchone()[0]
    cur.execute('INSERT INTO Protocol_truck_city (City_Id, Truck_Id, Start_downtime) '
                f'VALUES ({city_id}, {truck_id}, "{date}")')
    connection.commit()

#if __name__ == '__main__':
