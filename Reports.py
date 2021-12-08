import datetime
import pymysql
from PyQt5 import QtCore, QtWidgets

MyDB = pymysql.connect(user='root',
                       host='127.0.0.1',
                       password='TeamSpirit2021',
                       db='logistics',
                       charset='utf8mb4')

def useless_run_koef(connection, filename, date_from, date_to):
    cur = connection.cursor()
    f = open(filename, 'w')
    f.write('Id грузовика;' + 'Коэффициент;' + '\n')
    cur.execute('SELECT Id FROM trucks WHERE Sold = 0 ORDER BY Id')
    trucks = cur.fetchall()
    sum = 0
    n = 0
    for truck in trucks:
        cur.execute(f'SELECT IFNULL(SUM(Distance), 0) FROM routes WHERE Id IN '
                    f'(SELECT Route_Id FROM route_date WHERE Truck_Id = {truck[0]} AND Having_Cargo = 0 AND '
                    f'Departure_Date >= "{date_to}" AND Arrival_Date <= "{date_from}")')
        empty = cur.fetchone()[0]
        cur.execute(f'SELECT IFNULL(SUM(Distance), 0) FROM routes WHERE Id IN '
                    f'(SELECT Route_Id FROM route_date WHERE Truck_Id = {truck[0]} AND Having_Cargo = 1 AND '
                    f'Departure_Date >= "{date_to}" AND Arrival_Date <= "{date_from}")')
        full = cur.fetchone()[0]
        try:
            koef = float(empty) / float(full)
            sum += koef
            n += 1
        except:
            koef = 'Infinity'
        f.write(str(truck[0]) + ';' + str(koef) + '\n')
    try:
        average = sum / n
    except:
        average = 'Infinity'
    f.write('Средний показатель;' + str(average) + '\n')
    f.close()

def downtime_koef(connection, filename, date_from, date_to):
    cur = connection.cursor()
    f = open(filename, 'w')
    f.write('Id грузовика;' + 'Коэффициент;' + '\n')
    cur.execute('SELECT Id FROM trucks WHERE Sold = 0 ORDER BY Id')
    trucks = cur.fetchall()
    all_downtime = datetime.timedelta(0)
    all_driving_time = datetime.timedelta(0)
    for truck in trucks:
        downtime = datetime.timedelta(0)
        cur.execute(f'SELECT Start_downtime, IF("{date_from}" < IFNULL(End_downtime, "{date_from}"), '
                    f'"{date_from}", IFNULL(End_downtime, "{date_from}")) FROM protocol_truck_city '
                    f'WHERE Truck_Id = {truck[0]} AND '
                    f'Start_downtime >= "{date_to}" AND Start_downtime <= "{date_from}"')
        downtime_dates = cur.fetchall()
        for date in downtime_dates:
            try:
                date1 = datetime.date.fromisoformat(date[1])
            except:
                date1 = date[1]
            try:
                date0 = datetime.date.fromisoformat(date[0])
            except:
                date0 = date[0]
            downtime += date1 - date0
        driving_time = datetime.timedelta(0)
        cur.execute(f'SELECT Departure_Date, IF("{date_from}" < Arrival_Date, "{date_from}", Arrival_Date) FROM route_date '
                    f'WHERE Truck_Id = {truck[0]} AND '
                    f'Departure_Date >= "{date_to}" AND Departure_Date <= "{date_from}"')
        driving_dates = cur.fetchall()
        for date in driving_dates:
            try:
                date1 = datetime.date.fromisoformat(date[1])
            except:
                date1 = date[1]
            try:
                date0 = datetime.date.fromisoformat(date[0])
            except:
                date0 = date[0]
            driving_time += date1 - date0
        try:
            koef = float(downtime.days) / float(driving_time.days)
        except:
            koef = 'Infinity'
        f.write(str(truck[0]) + ';' + str(koef) + '\n')
        all_downtime += downtime
        all_driving_time += driving_time
    try:
        all_koef = float(all_downtime.days) / float(all_driving_time.days)
    except:
        all_koef = 'Infinity'
    f.write('Общий показатель;' + str(all_koef) + '\n')
    f.close()

def city_activity(connection, filename):
    cur = connection.cursor()
    f = open(filename, 'w')
    f.write('Город;' + 'Отправленный груз;' + 'Принятый груз' + '\n')
    cur.execute('SELECT Name, Shipped_weight, Accepted_weight FROM cities ORDER BY Name')
    cities = cur.fetchall()
    for city in cities:
        f.write(str(city[0]) + ';' + str(city[1]) + ';' + str(city[2]) + '\n')
    f.close()

def cargo_popularity(connection, filename):
    cur = connection.cursor()
    f = open(filename, 'w')
    f.write('Груз;' + 'Заказанный вес' + '\n')
    cur.execute('SELECT Name, Ordered_weight FROM cargo ORDER BY Name')
    cargoes = cur.fetchall()
    for cargo in cargoes:
        f.write(str(cargo[0]) + ';' + str(cargo[1]) + '\n')
    f.close()

def financial_report(connection, filename, year):
    cur = connection.cursor()
    f = open(filename, 'w')
    year_income = 0
    year_expenses = 0
    f.write('Год;' + 'Квартал;' + 'Месяц;' + 'Доходы;' + 'Расходы;' + 'Прибыль' + '\n')
    quarters = ['I', 'II', 'III', 'IV']
    months = ['Январь', 'Февраль', 'Март',
              'Апрель', 'Май', 'Июнь',
              'Июль', 'Август', 'Сентябрь',
              'Октябрь', 'Ноябрь', 'Декабрь']
    for quarter in range(1, 5):
        quarter_income = 0
        quarter_expenses = 0
        for month in range((quarter - 1) * 3 + 1, quarter * 3 + 1):
            month_income = 0
            month_expenses = 0
            date_from = datetime.date(year, month, 1)
            if month == 12:
                date_to = datetime.date(year + 1, 1, 1)
            else:
                date_to = datetime.date(year, month + 1, 1)
            cur.execute('SELECT Cost FROM buy_truck '
                        f'WHERE Date >= "{date_from}" AND Date <= "{date_to}"')
            bt_costs = cur.fetchall()
            for bt_cost in bt_costs:
                month_expenses += bt_cost[0]
            cur.execute('SELECT Cost FROM sell_truck '
                        f'WHERE Date >= "{date_from}" AND Date <= "{date_to}"')
            st_costs = cur.fetchall()
            for st_cost in st_costs:
                month_income += st_cost[0]
            cur.execute('SELECT Payment FROM orders '
                        f'WHERE Date >= "{date_from}" AND Date <= "{date_to}"')
            o_costs = cur.fetchall()
            for o_cost in o_costs:
                month_income += (o_cost[0] / 1.1) * 0.1
            cur.execute('SELECT Id, Downtime_costs FROM trucks WHERE Sold = 0 ORDER BY Id')
            trucks = cur.fetchall()
            for truck in trucks:
                cur.execute(f'SELECT IF(Start_downtime < "{date_from}", "{date_from}", Start_downtime), '
                            f'IF("{date_to}" < IFNULL(End_downtime, "{date_to}"), '
                            f'"{date_to}", IFNULL(End_downtime, "{date_to}")) FROM protocol_truck_city '
                            f'WHERE Truck_Id = {truck[0]} AND '
                            f'Start_downtime <= "{date_to}" AND '
                            f'"{date_to}" <= IFNULL(End_downtime, "{date_to}")')
                downtime_dates = cur.fetchall()
                downtime = datetime.timedelta(0)
                for date in downtime_dates:
                    try:
                        date1 = datetime.date.fromisoformat(date[1])
                    except:
                        date1 = date[1]
                    try:
                        date0 = datetime.date.fromisoformat(date[0])
                    except:
                        date0 = date[0]
                    downtime += date1 - date0
                month_expenses += downtime.days * truck[1]
            quarter_income += month_income
            quarter_expenses += month_expenses
            f.write(str(year) + ';' + quarters[quarter - 1] + ';' + months[month - 1] + ';' +
                    str(month_income) + ';' + str(month_expenses) + ';' +
                    str(month_income - month_expenses) + '\n')
        year_income += quarter_income
        year_expenses += quarter_expenses
        f.write(str(year) + ';' + quarters[quarter - 1] + ';' + 'Итого:;' +
                str(quarter_income) + ';' + str(quarter_expenses) + ';' +
                str(quarter_income - quarter_expenses) + '\n')
    f.write(str(year) + ';' + 'Итого:;' + ';' + str(year_income) + ';' + str(year_expenses) + ';' +
            str(year_income - year_expenses) + '\n')
    f.close()
if __name__ == '__main__':
    downtime_koef(MyDB, 'test.csv', '2021-12-02', '2021-12-07')
