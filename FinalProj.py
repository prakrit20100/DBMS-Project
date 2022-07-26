from unittest import result
import mysql.connector
import pwinput
from datetime import date

def insert_trains():
  # Function to insert train details in mysql database
  sql = "insert into Train values (%s ,%s ,%s ,%s ,%s ,%s ,%s)"
  val1 = ("00001","Delhi-Agra Shatabdi","Delhi","Agra","3","08:00","12:00")
  mycursor.execute(sql, val1)
  val2 = ("00002","Agra-Jaipur Shatabdi","Agra","Jaipur","3","06:00","11:00")
  mycursor.execute(sql, val2)
  val3 = ("00003","Mumbai-Pune Shatabdi","Mumbai","Pune","3","13:00","16:00")
  mycursor.execute(sql, val3)
  val4 = ("00004","Agra-Delhi Shatabdi","Agra","Delhi","3","13:00","17:00")
  mycursor.execute(sql, val4)
  val5 = ("00005","Pune-Mumbai Shatabdi","Pune","Mumbai","3","17:00","20:00")
  mycursor.execute(sql, val5)
  val6 = ("00006","Del-Jai Shatabdi","Delhi","Jaipur","3","07:00","14:00")
  mycursor.execute(sql, val6)
  val7 = ("00007","Jai-Mum Shatabdi","Jaipur","Mumbai","3","10:00","18:00")
  mycursor.execute(sql, val7)
  val8 = ("00008","Del-Mum Rajdhani","Delhi","Mumbai","3","21:00","09:00")
  mycursor.execute(sql, val8)
  val9 = ("00009","Pune-Agra Express","Pune","Agra","3","23:00","13:00")
  mycursor.execute(sql, val9)
  val10 = ("00010","Pune-Delhi Rajdhani","Pune","Delhi","3","22:30","14:00")
  mycursor.execute(sql, val10)
  val11 = ("00011","Del-Agr Rajdhani","Delhi","Agra","3","22:30","14:00")
  mycursor.execute(sql, val11)
  mydb.commit()

def main_menu():
  print("To book a ticket: \n Register as a customer -> Book a ticket")
  print("1. Register as a customer")
  print("2. Book a ticket")
  print("3. Print Ticket Details")
  print("4. To login as an employee")
  print("5. To cancel your ticket.")
  print("6. To check availability and schedule of trains")
  print("Any other number to terminate program")
  opt = int(input("\nEnter choice: "))
  return opt

def getContactNumber(aadhaarNo):
  x = int(input("Enter the number of phone numbers you wish to enter: "))
  for i in range(x):
   phnNo = input("Phone Number: ")
   sql = "insert into Customer_contact values (%s, %s)"
   val = (aadhaarNo, phnNo)
   mycursor.execute(sql, val)



def customer_registration():
  print("Enter the following details: ")
  aadhaarNo = input("Aadhaar Number: ")
  firstName = input("First Name: ")
  lastName = input("Last Name: ")
  email = input("Email Address: ")
  username = input("Username: ")    #Check if the username is taken
  password = pwinput.pwinput("Password: ")    # Input Password twice and check using recursive function
  dob = input("Date of Birth (YYYY-MM-DD): ") #Check the format
  age = 0
  gender = input("Gender(M/F): ") #Check valid input
  print("\n\nADDRESS DETAILS:\n")
  houseNo = input("House No: ")
  street = input("Street: ")
  city = input("City: ")
  state = input("State: ")
  pincode = input("PINCODE: ")

  sql = "insert into Customer values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
  val = (aadhaarNo, firstName, lastName, email, username, password, dob, age, gender, houseNo, street, city, state, pincode)

  mycursor.execute(sql, val)
  print("\n")
  getContactNumber(aadhaarNo)
  mydb.commit()


def makePayment(selected_train, coachNumber, noOfAvailableSeats, amountToBePaid, username):
  print("\n\tPAYMENT PORTAL")
  print("\n\nAmount to be paid: Rs", amountToBePaid)
  print("\nPlease transfer the above amount from your bank to the Account Number: 1234567890")
  ac_no = input("\nAfter transfer enter your Account Number for verification: ")
  today = date.today()

  print("\nTransaction Successful!!")
  seatNo = str(coachNumber) + "-" + str(noOfAvailableSeats)
  status = ""
  if noOfAvailableSeats <= 0:
    status = "Waiting"
  else:
    status = "Confirmed"


  sql = "SELECT * FROM Ticket"

  mycursor.execute(sql)
  result = mycursor.fetchall()

  ticketNo = "S" + str(int(result[len(result)-1][0][1:]) + 1)

  # Embedded SQL query to insert values
  if status == "Waiting":
    seatNo = "-----"
  sql = "insert into Ticket values (%s ,%s ,%s ,%s ,%s)"
  val = (ticketNo, status, today, seatNo, selected_train)
  mycursor.execute(sql, val)

  sql = "SELECT * FROM Transactions"
  mycursor.execute(sql)
  result = mycursor.fetchall()
  transactionNo = "T" + str(int(result[len(result)-1][0][1:])+1)
  # Embedded SQL query to insert values
  sql = "insert into Transactions values (%s ,%s ,%s ,%s ,%s)"
  val = (transactionNo, today, amountToBePaid, ac_no, ticketNo)
  mycursor.execute(sql, val)


  # Embedded SQL query to insert values - DIFFICULT query
  sql = "SELECT Aadhaar_Number FROM Customer WHERE Username = %s"
  val = (username, )
  mycursor.execute(sql, val)
  result = mycursor.fetchall()
  aadh_no = result[0][0]

  sql = "insert into Passenger values (%s ,%s ,%s)"
  val = (aadh_no, ticketNo, selected_train)
  mycursor.execute(sql, val)

  mydb.commit()

  print("\nKindly make note of the Ticket ID:", ticketNo, "for the pupose of printing the ticket.\n")

  main()


def ticket_booking():
  print("Inside ticket booking")
  print()
  input_username = input("Enter username: ")
  input_pass = pwinput.pwinput("Enter Password: ")
  # Embedded SQL query - optimized by indexing
  sql = "SELECT * FROM Customer WHERE Username = %s and Password = %s"
  adr = (input_username, input_pass)

  mycursor.execute(sql, adr)
  result = mycursor.fetchall()

  if len(result) == 0:
    print("Invalid Username or Password! Try Again.")
    return

  else:
    print("Logged In Successfully!!\n")

  input_source = input("Enter Source: ")
  input_destination = input("Enter Destination: ")
  # Embedded SQL Query
  sql = "SELECT * FROM Train WHERE LOWER(Source) = %s and LOWER(Destination) = %s"  # Using SQL string functions
  adr = (input_source.lower(), input_destination.lower())

  mycursor.execute(sql, adr)
  result = mycursor.fetchall()

  # print(len(result))
  train_numbers = []
  if len(result) == 0:
    print("Sorry, No trains currently available for selected Source and Destination")
    return

  else:
    print("\n The Following Trains are available: ")

    for x in result:
      print()
      train_numbers.append(x[0])
      print("Train Number: ", x[0])
      print("Train Name: ", x[1])
      print("Departure Time: ", x[5])
      print("Arrival Time: ", x[6])

    print()


  selected_train = input("Enter the Train Number You wish to book ticket for: ")

  if selected_train not in train_numbers:
    print("Invalid Train Number Entered. Try Again.")
    return
  else:
    print("\nFollowing are the details of category of seats available:")
    # Embedded SQL Query:
    sql = "SELECT * FROM Category_of_seats WHERE Train_Number = %s"  # Using SQL string functions
    adr = (selected_train,)
    mycursor.execute(sql, adr)
    result = mycursor.fetchall()

    for x in result:  
      print()
      print("Coach Number:", x[1], "\tSeat Type:", x[0], "\n Cost = Rs", x[2])
    # print("Your desired train is selected.") # Add condition for waiting list
    # inp = input("Do you wish to proceed to the payment to make payment and confirm your ticket")

    print()
    coachNumber = input("Enter the desired coach number: ")

    # Embedded SQL Query:
    sql = "SELECT * FROM Category_of_seats WHERE Train_Number = %s and Coach_number = %s"  # Using SQL string functions
    adr = (selected_train, coachNumber)
    mycursor.execute(sql, adr)
    result = mycursor.fetchall()

    noOfAvailableSeats = 0
    amountToBePaid = 0.00
    for x in result:  
      noOfAvailableSeats = x[3]
      amountToBePaid = x[2]

    print()
    if noOfAvailableSeats <= 0:
      print("You will be alotted in waiting list after payment of half the cost.")
      amountToBePaid /= 2
    else:
      print("Your ticket will be confirmed after payment")
      # Embedded SQL query for updating the table
      sql = "UPDATE Category_of_seats SET No_of_seats = %s WHERE Train_Number = %s and Coach_number = %s"  # Using SQL string functions
      adr = (noOfAvailableSeats-1, selected_train, coachNumber)
      mycursor.execute(sql, adr)
      mydb.commit()

    makePayment(selected_train, coachNumber, noOfAvailableSeats, amountToBePaid, input_username)


def Employee_details_input():
  print("Enter the following details: ")
  # Embedded SQL query that uses aggregation functions
  sql = "SELECT COUNT(*) FROM Employee"
  mycursor.execute(sql)
  result = mycursor.fetchall()

  Emp_ID = str(employeeNoTemplate + result[0][0])
  firstName = input("First Name: ")
  lastName = input("Last Name: ")
  DOB = input("Date of Birth (YYYY-MM-DD): ") #Check the format
  age = 0
  gender = input("Gender(M/F): ") #Check valid input
  Salary=float(input("Salary: "))
  print("\n\nADDRESS DETAILS:\n")
  houseNo = input("House No: ")
  street = input("Street: ")
  city = input("City: ")
  state = input("State: ")
  pincode = input("PINCODE: ")
  Designation= input("Designation: ")

  sql = "insert into Employee values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
  val = (Emp_ID, firstName, lastName,DOB, age, gender,Salary,houseNo, street, city, state, pincode,Designation)

  mycursor.execute(sql, val)
  mydb.commit()

  x = int(input("Enter the number of phone numbers you wish to enter: "))
  for i in range(x):
        phnNo = input("Phone Number: ")
        sql = "insert into Employee_contact values (%s, %s)"
        val = (phnNo, Emp_ID)
        mycursor.execute(sql, val)
  mydb.commit()

  print("\nEmployee registered in Database Successfully. The unique Employee ID is:", Emp_ID)

def print_ticket():
  no = input("Enter the Ticket Number: ")
  # Embedded SQL Query:
  sql = "SELECT * FROM Ticket WHERE Ticket_number = %s"
  adr = (no,)
  mycursor.execute(sql, adr)
  result = mycursor.fetchall()

  if len(result) == 0:
    print("\nInvalid Ticket Number. Try Again\n")
    return

  print("\n\t\tTICKET DETAILS")
  for x in result:
    print("\nTicket Number:", x[0], "\t\tDate of Booking:", x[2])
    print()

    # Difficult Query to fetch Passenger Details
    sql1 = "SELECT First_Name, Last_Name FROM Customer C, Passenger P WHERE P.Aadhaar_Number = C.Aadhaar_Number and P.Ticket_number = %s"
    adr1 = (x[0],)
    mycursor.execute(sql1, adr1)
    result1 = mycursor.fetchall()
    print("Passenger Name:", result1[0][0], result1[0][1])

    print("\nTrain Number:", x[4])
    print("Status:", x[1], end = "\t")
    if x[1].lower() != "waiting":
      print("Seat Number:", x[3], end = "\t")
      # Difficult query to fetch category of seat & Optimised query
      sql1 = "SELECT Category_Name FROM Category_of_seats C, Transactions T WHERE T.Ticket_number = %s and C.Train_Number = %s and C.Cost = T.Amount"
      adr1 = (x[0], x[4])
      mycursor.execute(sql1, adr1)
      result1 = mycursor.fetchall()
      print("Category of seat:", result1[0][0])

    print()

def employee_menu():
  emp_id = input("Enter your unique Employee ID: ")
  # EMbedded SQL Query and Optimised query fetching only required columns and once only
  sql = "SELECT Emp_ID, Designation FROM Employee WHERE Emp_ID = %s"
  adr = (emp_id,)
  mycursor.execute(sql, adr)
  result = mycursor.fetchall()

  if len(result) == 0:
    print("Invalid unique Employee ID entered.")
    return

  print("Logged in successfully. \n\nEnter an option from the list: ")
  print("1. Add record of new employee in the database.")
  print("2. Remove an employee from database.")
  print("3. Change designation of an employee")
  print("4. Add a new train in schedule.")
  print("5. Reschedule a train.")
  print("6. Delete a train from schedule.")
  print("7. To analyze transactions and bookings.")
  print("8. Get the contact details(Phone Number and Email ID) of the customer.")

  opt = int(input("\nChoose an option from the list above: "))

  if opt not in range(1,9):
    print("Invalid input.")
    return

  if opt == 1:
    if result[0][1] == "Database Administrator":
      Employee_details_input()
    else:
      # Constraints on who can modify data - GRANT feature
      print("Only Database Administrator has the permission to add a new employee in database")
      return

  elif opt == 2:
    if result[0][1] == "Database Administrator":
      deleteEmpID = input("\nEnter the Employee ID whose record you wish to delete: ")
      # Embedded SQL query that uses delete
      # DELETION requires delete from both tables
      sql = "DELETE FROM Employee_contact WHERE Emp_ID = %s"
      adr = (deleteEmpID,)
      mycursor.execute(sql, adr)
      mydb.commit()

      sql = "DELETE FROM Employee WHERE Emp_ID = %s"
      adr = (deleteEmpID,)
      mycursor.execute(sql, adr)
      mydb.commit()

      print("\nDeletion Successful")
    else:
      print("Only Database Administrator has the permission to add a new employee in database")
      return

  elif opt == 3:
    if result[0][1] == "Database Administrator": 
      modifyEmpID = input("\nEnter the Employee ID whose designation you wish to change: ")
      desgn = input("Enter new designation: ")
      # Embedded SQL query for update
      sql = "UPDATE Employee SET Designation = %s WHERE Emp_ID = %s"
      adr = (desgn, modifyEmpID)
      mycursor.execute(sql, adr);
      mydb.commit()
      print("Designation updated sucessfully!!")
    else:
      print("Only Database Administrator has the permission modify employee records in database")
      return

  elif opt == 4:
    if result[0][1] == "Chief Controller":
      train_no = input("\nEnter the Train Number: ")
      train_name = input("Enter the name of the train: ")
      src = input("Enter from where will the train start: ")
      dest = input("Enter the destination of the train: ")
      noCoaches = int(input("Enter no of coaches in the train: "))
      start_time = input("Enter the departure time of train(HH:MM): ")
      end_time = input("Enter the arrival time of the train(HH:MM): ")
      sql = "INSERT INTO Train VALUES (%s, %s, %s, %s, %s, %s, %s)"
      adr = (train_no, train_name, src, dest, noCoaches ,start_time, end_time)
      mycursor.execute(sql, adr)
      mydb.commit()

      for x in range(noCoaches):
        print("\nEnter details of Coach", x+1)
        seatCat = input("Category Name: ")
        coachNum = x+1
        seatCost = float(input("Enter the cost: "))
        numOfSeats = int(input("Enter the number of seats in the coach: "))
        sql = "INSERT INTO Category_of_seats VALUES (%s, %s, %s, %s, %s)"
        adr = (seatCat, x+1, seatCost, numOfSeats, train_no)
        mycursor.execute(sql, adr)
        mydb.commit()

    else:
      print("Only Chief Controller has the permission to add a new train in database")
      return

  elif opt == 5:
    if result[0][1] == "Chief Controller" or result[0][1] == "Station Master":
      train_no = input("\nEnter the Train Number of train to be rescheduled: ")
      start_time = input("Enter the new departure time of train(HH:MM): ")
      end_time = input("Enter the new arrival time of the train(HH:MM): ")
      # Embedded SQL Query for update
      sql = "UPDATE Train SET Start_Time = %s, End_Time = %s WHERE Train_Number = %s"
      adr = (start_time, end_time, train_no)
      mycursor.execute(sql, adr)
      mydb.commit()
      print("\nTrain Rescheduled")
    else:
      print("Only Chief Controller or Station Master has the permission to reschedule a train")
      return

  elif opt == 6:
    if result[0][1] == "Chief Controller" or result[0][1] == "Station Master":
      train_no = input("\nEnter the Train Number of train to be cancelled: ")
      # Embedded SQL Query for deletion
      # Moderate Query - requires deletion from 2 tables
      sql = "DELETE FROM Category_of_seats  WHERE Train_Number = %s"
      adr = (train_no,)
      mycursor.execute(sql, adr)
      mydb.commit()


      sql = "DELETE FROM Train WHERE Train_Number = %s"
      adr = (train_no, )
      mycursor.execute(sql, adr)
      mydb.commit()

      print("\nTrain Cancelled")
    else:
      print("Only Chief Controller or Station Master has the permission to cancel a train")
      return

  elif opt == 7:

    print("Analyze data")
    print("\nChoose any option out of the following: ")
    print("1. To find the train that has maximum number of bookings.")
    print("2. To find the average cost of transactions done.")
    print("3. To find category of seat that has most no of empty seats across all trains.")
    print("4. To find the total revenue earned.")
    opti = int(input("Enter your choice: "))
    if opti == 1:
      # Difficult embedded SQL query using aggregation function
      sql = "SELECT Train_Number, s FROM(SELECT Train_Number, SUM(No_of_seats) as s FROM Category_of_seats GROUP BY Train_Number) as T WHERE s = (SELECT MIN(s) FROM (SELECT Train_Number, SUM(No_of_seats) s FROM Category_of_seats GROUP BY Train_Number) as T1)"
      mycursor.execute(sql)
      result = mycursor.fetchall()
      print("Train Number with maximum no of bookings: ", result[0][0], "with", result[0][1], "seats remaining.")
    
    elif opti == 2:
      # SQl Query using aggregation function
      sql = "SELECT AVG(Amount) FROM Transactions"
      mycursor.execute(sql)
      result = mycursor.fetchall()
      print("Average amount of each transaction =", result[0][0])

    elif opti == 3:
      sql = "SELECT Category_Name, k FROM(SELECT Category_Name, SUM(No_of_seats) k FROM Category_of_seats GROUP BY Category_Name) as T1 WHERE k = (SELECT MAX(s) FROM (SELECT Category_Name, SUM(No_of_seats) s FROM Category_of_seats GROUP BY Category_Name) AS T)"
      mycursor.execute(sql)
      result = mycursor.fetchall()
      print("The category with maximum number of seats remaining is:", result[0][0], "with", result[0][1], "number of seats remaining.")

    elif opti == 4:
      sql = "SELECT SUM(Amount) FROM Transactions"
      mycursor.execute(sql)
      result = mycursor.fetchall()
      print("The total revenue earned is Rs", result[0][0])
    # Most passengers in a train
    # Avg transaction
    # Most favoured category of seats
    # Total revenue earned

  elif opt == 8:
    inp_aadhaar = input("Enter the Aadhaar Number of the customer whose contact details you wish to get: ")
    # Embedded SQL query using views
    sql = "SELECT Phone_no, Email FROM Customer_Contact_Details WHERE Aadhaar_Number = %s"
    adr = (inp_aadhaar,)
    mycursor.execute(sql, adr)
    result = mycursor.fetchall()
    if len(result) == 0:
      print("Invalid Customer Aadhaar Number")
      return

    print("\nEmail:", result[0][1])
    print("\nPhone Nos:")
    for x in range(len(result)):
      print("\t", result[x][0])


def schedule():
  src = input("Enter starting point of the train: ")
  dest = input("Enter your destination: ")
  #  Query using views
  sql = "SELECT * FROM train_schedule WHERE lower(Source) = %s and LOWER(Destination) = %s"
  adr = (src.lower(), dest.lower())
  mycursor.execute(sql, adr)
  result = mycursor.fetchall()
  if len(result) == 0:  
    print("No trains for this route")
    return

  for x in result:
    print("Train Name:", x[0])
    print("Start Time:", x[3], "\tEnd Time", x[4])
    print()

def cancellation_menu():
  ticketNo = input("Enter the ticket number of the train you wish to cancel: ")
  # Difficult Sequence of queries to perform the cancellation of ticket. Changes required in 4 tables
  
  sql = "SELECT Train_Number FROM Passenger WHERE Ticket_number = %s"
  adr = (ticketNo,)
  mycursor.execute(sql, adr)
  result = mycursor.fetchall()
  trainNo = result[0][0]

  sql = "DELETE FROM Passenger WHERE Ticket_number = %s"
  adr = (ticketNo,)
  mycursor.execute(sql, adr)
  sql = "SELECT Amount FROM Transactions WHERE Ticket_Number = %s"
  adr = (ticketNo,)
  mycursor.execute(sql, adr)
  result = mycursor.fetchall()
  amt = result[0][0]

  sql = "DELETE FROM Transactions WHERE Ticket_number = %s"
  adr = (ticketNo,)
  mycursor.execute(sql, adr)

  if amt >= 800:
    cn = 1
  elif amt >= 500:
    cn = 2
  else:
    cn = 3

  sql = "SELECT No_of_seats FROM Category_of_seats WHERE Train_Number = %s and Coach_number = %s"
  adr = (trainNo, cn)
  mycursor.execute(sql, adr)
  result = mycursor.fetchall()
  n_seats = result[0][0]
  sql = "UPDATE Category_of_seats SET No_of_seats = %s WHERE Train_Number = %s and Coach_number = %s"
  adr = (n_seats+1, trainNo, cn)
  mycursor.execute(sql, adr)

  sql = "DELETE FROM Ticket WHERE Ticket_number = %s"
  adr = (ticketNo,)
  mycursor.execute(sql, adr)
  mydb.commit()

  # print(n_seats, trainNo, cn)
  print("Cancellation Executed, refund of 80% will be transferred in your account.")






def main():
  opt = main_menu()
  if(opt == 1):
    customer_registration()
  elif(opt == 2):
    ticket_booking()
  elif(opt == 3):
    print_ticket()
  elif(opt == 4):
    employee_menu()
  elif(opt == 5):
    # print("Cancellation Menu:\n")
    cancellation_menu()
  elif(opt == 6):
    schedule()
  else:
    exit()

  


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Vishesh2121",
  database = "Railway_Management_System"
)

mycursor = mydb.cursor()

ticketNoTemplate = 333333
transactionNoTemplate = 55555
employeeNoTemplate = 44444444
main()


# Search for difficult queries





# mycursor.execute("DROP TABLE CUSTOMER");
# mycursor.execute("CREATE TABLE CUSTOMER(Aadhaar_Number varchar(20) Primary key not null, First_Name varchar(20), Last_Name varchar(20), Email varchar(30),  Username varchar(20) not null, Password varchar(20) not null, DOB date, age int, Gender char(1), House_No varchar(10), Street varchar(15), city varchar(15), state varchar(15), PINCODE char(6))")
# # FOREIGN KEY MISSING and Emp_ID

# sql = "insert into Customer values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
# val = ('5602230338593516432', 'Marice', 'Fishwick', 'mfishwick0@wp.com', 'mfishwick0', 'kjynxygt', '1964-04-28', 58, 'F', '6941', 'Ramsey', 'Svislach', 'Delhi', '110055')

# mycursor.execute(sql, val)
# mydb.commit()
# myresult = mycursor.fetchall()

# for x in myresult:
#   print(x)