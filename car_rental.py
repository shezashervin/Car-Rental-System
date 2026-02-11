import mysql.connector
from prettytable import PrettyTable
def get_connection():
    return mysql.connector.connect(
        user='root',
        password='Sheza9633960909',
        port='3306',
        host='localhost',
        database='car_rental_system')

def view_avail_cars():
    conn=get_connection()
    cur=conn.cursor()
    query="select * from cars where status='Available'"
    cur.execute(query)
    rows=cur.fetchall()
    table=PrettyTable()
    table.field_names=[' ID','MODEL','RATE PER DAY','STATUS']
    for i in rows:
        table.add_row(i)
    print()
    print(table)
    cur.close()
    conn.close()

def rent_car():
    conn=get_connection()
    cur=conn.cursor()
    carid=int(input("Enter the car id you'd like to rent: "))
    q="select rate_per_day from cars where car_id=%s and status='Available'"
    v=(carid,)
    cur.execute(q,v)
    result=cur.fetchone()
    if not result:
        print("Unavailable. Please enter a valid input.")
        cur.close()
        conn.close()
        return
    customer_name=input("Enter your name: ")
    days=int(input("Enter the number of days you'd like to rent for: "))
    total_cost= result[0] * days
    q1="update cars set status='Rented' where car_id=%s" 
    v1=(carid,)
    cur.execute(q1,v1)
    q2="insert into rentals (car_id,customer_name,days,total_cost,Rental_status) values(%s,%s,%s,%s,'Renting')"
    v2=(carid,customer_name,days,total_cost)
    cur.execute(q2,v2)
    conn.commit()
    cur.close()
    conn.close()
    print("Car Rented Succesfully!")

def return_car():
    conn=get_connection()
    cur=conn.cursor()
    carid=int(input("Enter the car id you'd like to return: "))
    q="select * from cars where car_id=%s and status='Rented'"
    v=(carid,)
    cur.execute(q,v)
    result=cur.fetchone()
    if not result:
        print("Unavailable. Please enter a valid input.")
        cur.close()
        conn.close()
        return
    query="update cars join rentals on cars.car_id=rentals.car_id set cars.status='Available',rentals.Rental_status='Returned' where cars.car_id=%s"
    value=(carid,)
    cur.execute(query,value)  
    conn.commit()
    cur.close()
    conn.close()
    print("Car Returned Successfully!")

def view_my_rental():
    conn=get_connection()
    cur=conn.cursor()
    carid=int(input("Enter your id number: "))
    customer_name=input("Enter your name: ")
    query="select * from rentals where car_id=%s and customer_name=%s"
    value=(carid,customer_name)
    cur.execute(query,value)
    result=cur.fetchall()
    if not result:
        print("Unavailable. Please enter a valid input.")
        cur.close()
        conn.close()
        return
    table=PrettyTable()
    table.field_names=['RENT ID','CAR ID','CUSTOMER NAME','DAYS','TOTAL COST','RENTAL STATUS']
    for i in result:
        table.add_row(i)
    print(table)
    cur.close()
    conn.close()

def menu():
    while True:
        print("\n--CAR RENTAL SERVICES--")
        print("\nOptions: \n\n1- View Available Car\n2- Rent a car\n3- Return a car\n4- View My Rentals\n5- Exit program")
        choice=int(input("Enter an option: "))
        if choice==1:
            view_avail_cars()
        elif choice==2:
            rent_car()
        elif choice==3:
            return_car()
        elif choice==4:
            view_my_rental()
        elif choice==5:
            print("Thank You!")
            break
        else:
            print("Invalid! Please enter a valid input.")
menu()