import datetime
import pymysql
import string
import random

def db_connect():
    return pymysql.connect(user='root',
                           host='127.0.0.1',
                           password='TeamSpirit2021',
                           db='logistics',
                           charset='utf8mb4')

def db_init():
    connection = pymysql.connect(user='root',
                                 host='127.0.0.1',
                                 password='TeamSpirit2021',
                                 charset='utf8mb4')
    with connection:
        cur = connection.cursor()
        cur.execute('SELECT VERSION()')
        version = cur.fetchone()
        print("Database version: {}".format(version[0]))

        try:
            # Create MySQL database
            cur.execute('CREATE DATABASE IF NOT EXISTS Logistics;')
        except Exception as e:
            print("Error: {}".format(e))
            return

        print('Database "Logistics" has been created')
        return

def db_destroy():
    con = pymysql.connect(host='127.0.0.1',
                          user='root',
                          password='TeamSpirit2021',
                          charset='utf8mb4')
    cur = con.cursor()

    try:
        cur.execute('DROP DATABASE Logistics;')
    except Exception as e:
        print("Error: {}".format(e))
        return
    print('Database "Logistics" has been destroyed')
    return

def db_create(connection):
    cur = connection.cursor()
    try:
        cur.execute('CREATE TABLE Cargo_types' 
                    '(' 
                    '    Id INT PRIMARY KEY AUTO_INCREMENT,' 
                    '    Type NVARCHAR(100) UNIQUE' 
                    ');')
        cur.execute('CREATE TABLE Cargo' 
                    '(' 
                    '    Id INT PRIMARY KEY AUTO_INCREMENT,' 
                    '    Name NVARCHAR(100) NOT NULL,' 
                    '    Cargo_type_Id INT,' 
                    '    Ordered_weight INT,' 
                    '    FOREIGN KEY (Cargo_type_Id) REFERENCES Cargo_types (Id)' 
                    ');')
        cur.execute('CREATE TABLE Trucks' 
                    '(' 
                    '    Id INT PRIMARY KEY AUTO_INCREMENT,'
                    '    Register_number NVARCHAR(6) UNIQUE,' 
                    '    Cargo_type_Id INT,' 
                    '    Carrying_capacity INT,' 
                    '    Cost INT,' 
                    '    Downtime_costs INT,' 
                    '    Route_costs INT,' 
                    '    Empty_costs INT,'
                    '    Sold BOOL,' 
                    '    FOREIGN KEY (Cargo_type_Id) REFERENCES Cargo_types (Id)' 
                    ');')
        cur.execute('CREATE TABLE Cities' 
                    '(' 
                    '   Id INT PRIMARY KEY AUTO_INCREMENT,' 
                    '   Name NVARCHAR(100) NOT NULL UNIQUE,' 
                    '   Shipped_weight INT,' 
                    '   Accepted_weight INT' 
                    ');')
        cur.execute('CREATE TABLE Protocol_truck_city' 
                    '(' 
                    '    Id INT PRIMARY KEY AUTO_INCREMENT,'
                    '    City_Id INT,' 
                    '    Truck_Id INT,' 
                    '    Start_downtime DATE,' 
                    '    End_downtime DATE,' 
                    '    FOREIGN KEY (City_Id) REFERENCES Cities (Id),' 
                    '    FOREIGN KEY (Truck_Id) REFERENCES Trucks (Id)' 
                    ');')
        cur.execute('CREATE TABLE Routes' 
                    '(' 
                    '    Id INT PRIMARY KEY AUTO_INCREMENT,' 
                    '    City1_Id INT,' 
                    '    City2_Id INT,' 
                    '    Distance INT NOT NULL,' 
                    '    FOREIGN KEY (City1_Id) REFERENCES Cities (Id),' 
                    '    FOREIGN KEY (City2_Id) REFERENCES Cities (Id)' 
                    ');')
        cur.execute('CREATE TABLE Rates' 
                    '(' 
                    '    Id INT PRIMARY KEY AUTO_INCREMENT,' 
                    '    Cargo_type_Id INT,' 
                    '    Transportation_cost INT,' 
                    '    FOREIGN KEY (Cargo_type_Id) REFERENCES Cargo_types (Id)' 
                    ');')
        cur.execute('CREATE TABLE Sell_Truck' 
                    '(' 
                    '    Id INT PRIMARY KEY AUTO_INCREMENT,' 
                    '    Cost INT NOT NULL,' 
                    '    Customer NVARCHAR(100) NOT NULL,'  
                    '    Date DATE NOT NULL'  
                    ');')
        cur.execute('CREATE TABLE Buy_Truck' 
                    '(' 
                    '    Id INT PRIMARY KEY AUTO_INCREMENT,'  
                    '    Seller NVARCHAR(100) NOT NULL,' 
                    '    Date DATE NOT NULL,' 
                    '    Cost INT,' 
                    '    Truck_Id INT NOT NULL,'
                    '    FOREIGN KEY (Truck_Id) REFERENCES Trucks (Id)'
                    ');')
        cur.execute('CREATE TABLE Orders' 
                    '(' 
                    '    Id INT PRIMARY KEY AUTO_INCREMENT,' 
                    '    Date DATE NOT NULL,' 
                    '    Payment INT' 
                    ');')
        cur.execute('CREATE TABLE Order_items' 
                    '(' 
                    '    Id INT PRIMARY KEY AUTO_INCREMENT,' 
                    '    Order_Id INT,' 
                    '    Route_Id INT,' 
                    '    Truck_Id INT,' 
                    '    Rate_Id INT,' 
                    '    Cargo_Id INT,' 
                    '    Weight INT,' 
                    '    FOREIGN KEY (Order_Id) REFERENCES Orders (Id),' 
                    '    FOREIGN KEY (Route_Id) REFERENCES Routes (Id),' 
                    '    FOREIGN KEY (Truck_Id) REFERENCES Trucks (Id),' 
                    '    FOREIGN KEY (Rate_Id) REFERENCES Rates (Id),' 
                    '    FOREIGN KEY (Cargo_Id) REFERENCES Cargo (Id)' 
                    ');')
        cur.execute('CREATE TABLE Route_Date' 
                    '('
                    '    Id INT PRIMARY KEY AUTO_INCREMENT,' 
                    '    Route_Id INT,' 
                    '    Truck_Id INT,' 
                    '    Departure_Date DATE,' 
                    '    Arrival_Date DATE,' 
                    '    Having_Cargo BOOL,'
                    '    FOREIGN KEY (Route_Id) REFERENCES Routes (Id),'
                    '    FOREIGN KEY (Truck_Id) REFERENCES Trucks (Id)' 
                    ');')
        cur.execute('CREATE TABLE Cur_Date' 
                    '(' 
                    '    Date DATE'
                    ');')
        cur.execute('CREATE TABLE Speed' 
                    '(' 
                    '    Trucks_speed INT' 
                    ');')
    except Exception as e:
        print("Error: {}".format(e))
        return

def random_register_number():
    letters = 'авекмнорстух'
    numbers = '1234567890'
    register_number = ''
    register_number += random.choice(letters)
    for i in range(3):
        register_number += random.choice(numbers)
    for i in range(2):
        register_number += random.choice(letters)
    return register_number

def db_insert_rows(connection):
    cur = connection.cursor()
    types_of_cargo = ('сыпучий',
                      'жидкий',
                      'газ',
                      'контейнер',
                      'штучный',
                      'негабаритный')
    for cargo_type in types_of_cargo:
        cur.execute('INSERT INTO Cargo_types (Type) '
                    'VALUES ("{}")'.format(cargo_type))
    cargoes = (('Песок', 1, 0),
               ('Молоко', 2, 0),
               ('Гелий', 3, 0),
               ('Рыба', 4, 0),
               ('Танк', 5, 0),
               ('Трубы', 6, 0))
    for cargo in cargoes:
        cur.execute('INSERT INTO Cargo (Name, Cargo_type_Id, Ordered_weight) '
                    'VALUES ("{}", {}, {})'.format(cargo[0], cargo[1], cargo[2]))
    cities = (('Москва', 0, 0),
              ('Санкт-Петербург', 0, 0),
              ('ЕкатеринБург', 0, 0),
              ('Краснодар', 0, 0),
              ('Архангельск', 0, 0),
              ('Симферополь', 0, 0))
    for city in cities:
        cur.execute('INSERT INTO Cities (Name, Shipped_weight, Accepted_weight) '
                    'VALUES ("{}", {}, {})'.format(city[0], city[1], city[2]))
    rates = ((1, 20),
             (2, 60),
             (3, 60),
             (4, 40),
             (5, 100),
             (6, 70))
    for rate in rates:
        cur.execute('INSERT INTO Rates (Cargo_type_Id, Transportation_cost) '
                    'VALUES ({}, {})'.format(rate[0], rate[1]))
    routes = ((1, 2, 700),
              (1, 3, 1800),
              (1, 4, 1350),
              (1, 5, 1200),
              (1, 6, 1750),
              (2, 3, 2200),
              (2, 4, 2050),
              (2, 5, 1150),
              (2, 6, 2450),
              (3, 4, 2500),
              (3, 5, 1900),
              (3, 6, 2850),
              (4, 5, 2600),
              (4, 6, 450),
              (5, 6, 2650))
    for route in routes:
        cur.execute('INSERT INTO Routes (City1_Id, City2_Id, Distance) '
                    'VALUES ({}, {}, {})'.format(route[0], route[1], route[2]))
    trucks = ((random_register_number(), 1, 10000, 6000, 10, 20, 15, 0),
              (random_register_number(), 2, 10000, 7000, 10, 20, 15, 0),
              (random_register_number(), 3, 10000, 8000, 10, 20, 15, 0),
              (random_register_number(), 4, 10000, 9000, 10, 20, 15, 0),
              (random_register_number(), 5, 10000, 10000, 10, 20, 15, 0),
              (random_register_number(), 6, 10000, 11000, 10, 20, 15, 0),
              (random_register_number(), 1, 10000, 6000, 10, 20, 15, 0),
              (random_register_number(), 2, 10000, 7000, 10, 20, 15, 0),
              (random_register_number(), 3, 10000, 8000, 10, 20, 15, 0),
              (random_register_number(), 4, 10000, 9000, 10, 20, 15, 0),
              (random_register_number(), 5, 10000, 10000, 10, 20, 15, 0),
              (random_register_number(), 6, 10000, 11000, 10, 20, 15, 0),
              (random_register_number(), 1, 10000, 6000, 10, 20, 15, 0),
              (random_register_number(), 2, 10000, 7000, 10, 20, 15, 0),
              (random_register_number(), 3, 10000, 8000, 10, 20, 15, 0),
              (random_register_number(), 4, 10000, 9000, 10, 20, 15, 0),
              (random_register_number(), 5, 10000, 10000, 10, 20, 15, 0),
              (random_register_number(), 6, 10000, 11000, 10, 20, 15, 0),
              (random_register_number(), 1, 10000, 6000, 10, 20, 15, 0),
              (random_register_number(), 2, 10000, 7000, 10, 20, 15, 0),
              (random_register_number(), 3, 10000, 8000, 10, 20, 15, 0),
              (random_register_number(), 4, 10000, 9000, 10, 20, 15, 0),
              (random_register_number(), 5, 10000, 10000, 10, 20, 15, 0),
              (random_register_number(), 6, 10000, 11000, 10, 20, 15, 0),
              (random_register_number(), 1, 10000, 6000, 10, 20, 15, 0),
              (random_register_number(), 2, 10000, 7000, 10, 20, 15, 0),
              (random_register_number(), 3, 10000, 8000, 10, 20, 15, 0),
              (random_register_number(), 4, 10000, 9000, 10, 20, 15, 0),
              (random_register_number(), 5, 10000, 10000, 10, 20, 15, 0),
              (random_register_number(), 6, 10000, 11000, 10, 20, 15, 0),
              (random_register_number(), 1, 10000, 6000, 10, 20, 15, 0),
              (random_register_number(), 2, 10000, 7000, 10, 20, 15, 0),
              (random_register_number(), 3, 10000, 8000, 10, 20, 15, 0),
              (random_register_number(), 4, 10000, 9000, 10, 20, 15, 0),
              (random_register_number(), 5, 10000, 10000, 10, 20, 15, 0),
              (random_register_number(), 6, 10000, 11000, 10, 20, 15, 0))
    for truck in trucks:
        cur.execute('INSERT INTO Trucks (Register_number, Cargo_type_Id, Carrying_capacity, Cost, '
                    'Downtime_costs, Route_costs, Empty_costs, Sold) '
                    'VALUES ("{}", {}, {}, {}, {}, {}, {}, {})'
                    .format(truck[0], truck[1], truck[2], truck[3], truck[4], truck[5], truck[6], truck[7]))
    protocols = ((1, 1, datetime.date.today()),
                 (1, 2, datetime.date.today()),
                 (1, 3, datetime.date.today()),
                 (1, 4, datetime.date.today()),
                 (1, 5, datetime.date.today()),
                 (1, 6, datetime.date.today()),
                 (2, 7, datetime.date.today()),
                 (2, 8, datetime.date.today()),
                 (2, 9, datetime.date.today()),
                 (2, 10, datetime.date.today()),
                 (2, 11, datetime.date.today()),
                 (2, 12, datetime.date.today()),
                 (3, 13, datetime.date.today()),
                 (3, 14, datetime.date.today()),
                 (3, 15, datetime.date.today()),
                 (3, 16, datetime.date.today()),
                 (3, 17, datetime.date.today()),
                 (3, 18, datetime.date.today()),
                 (4, 19, datetime.date.today()),
                 (4, 20, datetime.date.today()),
                 (4, 21, datetime.date.today()),
                 (4, 22, datetime.date.today()),
                 (4, 23, datetime.date.today()),
                 (4, 24, datetime.date.today()),
                 (5, 25, datetime.date.today()),
                 (5, 26, datetime.date.today()),
                 (5, 27, datetime.date.today()),
                 (5, 28, datetime.date.today()),
                 (5, 29, datetime.date.today()),
                 (5, 30, datetime.date.today()),
                 (6, 31, datetime.date.today()),
                 (6, 32, datetime.date.today()),
                 (6, 33, datetime.date.today()),
                 (6, 34, datetime.date.today()),
                 (6, 35, datetime.date.today()),
                 (6, 36, datetime.date.today()))
    for protocol in protocols:
        cur.execute('INSERT INTO Protocol_truck_city (City_Id, Truck_Id, Start_downtime) '
                    'VALUES ({}, {}, "{}")'.format(protocol[0], protocol[1], protocol[2]))
    speed = 720
    cur.execute('INSERT INTO Speed (Trucks_speed) '
                f'VALUES ({speed})')
    connection.commit()


if __name__ == '__main__':
    db_destroy()
    db_init()
    connection = db_connect()
    db_create(connection)
    db_insert_rows(connection)
