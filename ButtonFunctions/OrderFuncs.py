import datetime
import math
import pymysql

MyDB = pymysql.connect(user='root',
                       host='127.0.0.1',
                       password='TeamSpirit2021',
                       db='logistics',
                       charset='utf8mb4')

def insert_order(connection, date):
    cur = connection.cursor()
    cur.execute('INSERT INTO Orders (Date, Payment) '
                f'VALUES ("{date}", 0)')
    connection.commit()

def num_of_trips(capacity, weight):
    num = 0
    while weight > 0:
        num += 1
        weight -= capacity
    return num

def send_truck(connection, city1_name, city2_name, cargo_id, weight, date):
    payment = 0
    new_date = date
    cur = connection.cursor()
    cur.execute('SELECT Id FROM Cities '
                f'WHERE Name = "{city1_name}"')
    city1 = cur.fetchone()[0]
    cur.execute('SELECT Id FROM Cities '
                f'WHERE Name = "{city2_name}"')
    city2 = cur.fetchone()[0]
    cur.execute('SELECT Trucks_speed FROM Speed')
    speed = cur.fetchone()[0]
    cur.execute('SELECT Cargo_type_Id FROM Cargo '
                f'WHERE Id = {cargo_id}')
    cargo_type_id = cur.fetchone()[0]
    cur.execute('SELECT Id FROM Rates '
                f'WHERE Cargo_type_Id = {cargo_type_id}')
    rate_id = cur.fetchone()[0]
    cur.execute('SELECT Max(Id) FROM Orders')
    order_id = cur.fetchone()[0]
    cur.execute('SELECT Id FROM Routes '
                f'WHERE City1_Id = {min(city1, city2)} AND City2_Id = {max(city1, city2)}')
    route_id = cur.fetchone()[0]
    cur.execute('SELECT Trucks.Id, Trucks.Carrying_Capacity FROM Trucks '
                'JOIN Protocol_truck_city ON Truck_Id = Trucks.Id '
                f'WHERE City_Id = {city1} AND End_downtime IS NULL AND Trucks.Cargo_type_Id = {cargo_type_id}')
    truck = cur.fetchone()
    cur.execute('SELECT Trucks.Id, Trucks.Carrying_Capacity, Protocol_truck_city.City_Id FROM Trucks '
                'JOIN Protocol_truck_city ON Truck_Id = Trucks.Id '
                f'WHERE End_downtime IS NULL AND Cargo_type_Id = {cargo_type_id}')
    truck_from_other_city = cur.fetchone()
    if truck is None:
        truck_id = truck_from_other_city[0]
        cur.execute('SELECT Route_costs, Empty_costs FROM Trucks '
                    f'WHERE Id = {truck_id}')
        costs = cur.fetchone()
        route_costs = costs[0]
        empty_costs = costs[1]
        trips = num_of_trips(truck_from_other_city[1], weight)
        city_id = truck_from_other_city[2]
        cur.execute('SELECT Id FROM Routes '
                    f'WHERE City1_Id = {min(city_id, city1)} AND City2_Id = {max(city_id, city1)}')
        tmproute_id = cur.fetchone()[0]
        cur.execute('UPDATE Protocol_truck_city '
                    f'SET End_downtime = "{date}" '
                    f'WHERE Truck_Id = {truck_id} AND End_downtime IS NULL')
        cur.execute('SELECT Distance FROM Routes '
                    f'WHERE Id = {tmproute_id}')
        distance = cur.fetchone()[0]
        new_date += datetime.timedelta(math.floor(distance / speed))
        cur.execute('INSERT INTO Route_date (Route_Id, Truck_Id, Departure_date, Arrival_date, Having_Cargo) '                    
                    f'VALUES ({tmproute_id}, {truck_id}, "{date}", "{new_date}", 0)')
        payment += distance * empty_costs
        cur.execute('INSERT INTO Protocol_truck_city (City_Id, Truck_Id, Start_downtime) '
                    f'VALUES ({city1}, {truck_id}, "{new_date}")')
    else:
        trips = num_of_trips(truck[1], weight)
        truck_id = truck[0]
        cur.execute('SELECT Route_costs, Empty_costs FROM Trucks '
                    f'WHERE Id = {truck_id}')
        costs = cur.fetchone()
        route_costs = costs[0]
        empty_costs = costs[1]
    for i in range(trips):
        cur.execute('UPDATE Protocol_truck_city '
                    f'SET End_downtime = "{new_date}" '
                    f'WHERE Truck_Id = {truck_id} AND End_downtime IS NULL')
        cur.execute('SELECT Distance FROM Routes '
                    f'WHERE Id = {route_id}')
        distance = cur.fetchone()[0]
        tmp_date = new_date + datetime.timedelta(math.floor(distance / speed))
        cur.execute('INSERT INTO Route_date (Route_Id, Truck_Id, Departure_Date, Arrival_Date, Having_Cargo) '
                    f'VALUES ({route_id}, {truck_id}, "{new_date}", "{tmp_date}", 1)')
        payment += distance * route_costs
        new_date += datetime.timedelta(math.floor(distance / speed))
        cur.execute('INSERT INTO Protocol_truck_city (City_Id, Truck_Id, Start_downtime) '
                    f'VALUES ({city2}, {truck_id}, "{new_date}")')
        if i != trips - 1:
            cur.execute('UPDATE Protocol_truck_city '
                        f'SET End_downtime = "{new_date}" '
                        f'WHERE Truck_Id = {truck_id} AND End_downtime IS NULL')
            tmp_date = new_date + datetime.timedelta(math.floor(distance / speed))
            cur.execute('INSERT INTO Route_date (Route_Id, Truck_Id, Departure_date, Arrival_date, Having_Cargo) '
                        f'VALUES ({route_id}, {truck_id}, "{new_date}", "{tmp_date}", 0)')
            payment += distance * empty_costs
            new_date += datetime.timedelta(math.floor(distance / speed))
            cur.execute('INSERT INTO Protocol_truck_city (City_Id, Truck_Id, Start_downtime) '
                        f'VALUES ({city1}, {truck_id}, "{new_date}")')
    cur.execute('INSERT INTO Order_items (Order_Id, Route_Id, Truck_Id, Rate_Id, Cargo_Id, Weight) '
                f'VALUES ({order_id}, {route_id}, {truck_id}, {rate_id}, {cargo_id}, {weight})')
    cur.execute('SELECT Max(Id) FROM Orders')
    max_id = cur.fetchone()[0]
    cur.execute('UPDATE Orders '
                f'SET Payment = {payment * 1.1} '
                f'WHERE Id = {max_id}')
    connection.commit()

def update_cities(connection, city1, city2, weight):
    cur = connection.cursor()
    cur.execute('SELECT Shipped_weight FROM cities '
                f'WHERE Name = "{city1}"')
    city1_weight = cur.fetchone()[0]
    cur.execute('UPDATE Cities '
                f'SET Shipped_weight = {city1_weight + weight} '
                f'WHERE Name = "{city1}"')
    cur.execute('SELECT Accepted_weight FROM cities '
                f'WHERE Name = "{city2}"')
    city2_weight = cur.fetchone()[0]
    cur.execute('UPDATE Cities '
                f'SET Accepted_weight = {city2_weight + weight} '
                f'WHERE Name = "{city2}"')
    connection.commit()

def update_cargo(connection, cargo, weight):
    cur = connection.cursor()
    cur.execute('SELECT Ordered_weight FROM Cargo '
                f'WHERE Id = {cargo}')
    cargo_weight = cur.fetchone()[0]
    cur.execute('UPDATE Cargo '
                f'SET Ordered_weight = {cargo_weight + weight} '
                f'WHERE Id = {cargo}')
    connection.commit()

if __name__ == '__main__':
    insert_order(MyDB, datetime.date.today())
    send_truck(MyDB, 'Москва', 'Краснодар', 1, 11000, datetime.date.today())
    update_cargo(MyDB, 1, 10000)
