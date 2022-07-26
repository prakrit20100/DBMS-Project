from unittest import result
import mysql.connector
import pwinput
from datetime import date
from tkinter import *

root1 = Tk()
ChoiceChosen = 0
MenuCanavs = Canvas(root1, width=1500, height=1530)
MenuCanavs.pack()
ChoiceEntry = Entry(root1)
MenuCanavs.create_window(725, 700, window=ChoiceEntry)

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

  ticketNo = "S" + str(ticketNoTemplate + len(result))

  # Embedded SQL query to insert values
  if status == "Waiting":
    seatNo = "-----"
  sql = "insert into Ticket values (%s ,%s ,%s ,%s ,%s)"
  val = (ticketNo, status, today, seatNo, selected_train)
  mycursor.execute(sql, val)

  transactionNo = "T" + str(transactionNoTemplate + len(result))
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
  # Embedded SQL query
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

  opt = int(input("\nChoose an option from the list above: "))

  if opt not in range(1,8):
    print("Invalid input.")
    return

  if opt == 1:
    if result[0][1] == "Database Administrator":
      Employee_details_input()
    else:
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
    opt = int(input("Enter your choice: "))
    if opt == 1:
      # Difficult embedded SQL query using aggregation function
      sql = "SELECT Train_Number, s FROM(SELECT Train_Number, SUM(No_of_seats) as s FROM Category_of_seats GROUP BY Train_Number) as T WHERE s = (SELECT MIN(s) FROM (SELECT Train_Number, SUM(No_of_seats) s FROM Category_of_seats GROUP BY Train_Number) as T1)"
      mycursor.execute(sql)
      result = mycursor.fetchall()
      print("Train Number with maximum no of bookings: ", result[0][0], "with", result[0][1], "seats remaining.")
    
    elif opt == 2:
      # SQl Query using aggregation function
      sql = "SELECT AVG(Amount) FROM Transactions"
      mycursor.execute(sql)
      result = mycursor.fetchall()
      print("Average amount of each transaction =", result[0][0])

    elif opt == 3:
      sql = "SELECT Category_Name, k FROM(SELECT Category_Name, SUM(No_of_seats) k FROM Category_of_seats GROUP BY Category_Name) as T1 WHERE k = (SELECT MAX(s) FROM (SELECT Category_Name, SUM(No_of_seats) s FROM Category_of_seats GROUP BY Category_Name) AS T)"
      mycursor.execute(sql)
      result = mycursor.fetchall()
      print("The category with maximum number of seats remaining is:", result[0][0], "with", result[0][1], "number of seats remaining.")

    elif opt == 4:
      sql = "SELECT SUM(Amount) FROM Transactions"
      mycursor.execute(sql)
      result = mycursor.fetchall()
      print("THe total revenue earned is Rs", result[0][0])
    # Most passengers in a train
    # Avg transaction
    # Most favoured category of seats
    # Total revenue earned


def cancellation_menu():
  ticketNo = input("Enter the ticket number of the train you wish to cancel: ")
  

def GetChoiceChosen():
    ChoiceChosen = ChoiceEntry.get()

    print(ChoiceChosen)

    lbl = Label(root1, bd=0, relief=RIDGE, text="Choice Chosen:"+ChoiceChosen, fg="black", bg="white",font=("times new roman", 20))
    MenuCanavs.create_window(725,760,window=lbl)

    if(ChoiceChosen == 1):
      customer_registration()
    elif(ChoiceChosen == 2):
      ticket_booking()
    elif(ChoiceChosen == 3):
      print_ticket()
    elif(ChoiceChosen == 4):
      employee_menu()
    elif(ChoiceChosen == 5):
      print("Cancellation Menu:\n")
      # cancellation_menu()
    else:
      exit()

    return ChoiceChosen

def mainMenu():
    # root.title("IRCTC Main Menu")
    # root.geometry("1540x800+0+0")

    Title = Label(root1, bd=20, relief=RIDGE, text="IRCTC Main Menu", fg="black", bg="white",font=("times new roman", 50, "bold"),)
    MenuCanavs.create_window(750,100,window=Title)
    # FrameforChoices = LabelFrame(root,bd=20,padx=20,relief=RIDGE,font=("times new roman",20,"bold"))
    # FrameforChoices.place(x=0,y=130,width=1530,height=300)
    Choices = Label(root1, bd=20, relief=RIDGE, text="Select a choice :)", fg="black", bg="white",font=("times new roman", 30, "bold"))
    MenuCanavs.create_window(750,250,window=Choices)
    Choice1 = Label(root1, bd=0, relief=RIDGE, text="\n1. Register as a customer", fg="black", bg="white",font=("times new roman", 20))
    MenuCanavs.create_window(150,350,window=Choice1)
    Choice2 = Label(root1, bd=0, relief=RIDGE, text="2. Book a ticket(If not registered, register as a customer first)", fg="black", bg="white",font=("times new roman", 20))
    MenuCanavs.create_window(340,410,window=Choice2)
    Choice3 = Label(root1, bd=0, relief=RIDGE, text="3. Print Ticket Details", fg="black", bg="white",font=("times new roman", 20))
    MenuCanavs.create_window(130,450,window=Choice3)
    Choice4 = Label(root1, bd=0, relief=RIDGE, text="4. To login as an employee", fg="black", bg="white",font=("times new roman", 20))
    MenuCanavs.create_window(155,490,window=Choice4)
    Choice5 = Label(root1, bd=0, relief=RIDGE, text="5. To cancel your ticket.", fg="black", bg="white",font=("times new roman", 20))
    MenuCanavs.create_window(140,530,window=Choice5)
    Choice6 = Label(root1, bd=0, relief=RIDGE, text="Enter any other number to quit\n\n", fg="black", bg="white",font=("times new roman", 20))
    MenuCanavs.create_window(175,600,window=Choice6)

    EntryLabel = Label(root1, bd=0, relief=RIDGE, text="Enter the choice you want :", fg="black", bg="white",font=("times new roman", 20))
    MenuCanavs.create_window(500, 700, window=EntryLabel)



    EnterButton = Button(text="Enter your choice",command=GetChoiceChosen)
    MenuCanavs.create_window(725,725,window=EnterButton)


    EnterButton1 = Button(text="Choose 1",command=CustomerRegistration)
    MenuCanavs.create_window(350,350,window=EnterButton1)
    root1.mainloop()

root2 = Tk()
AadharNo = 0
FirstName = ""
LastName = ""
Email = ""
Username = ""
Password = ""
DOB = ""
Gender = ""
Age = 0
HouseNo = 0
Street = ""
State = ""
City = ""
Pincode = ""
CustomerRegistrationCanvas = Canvas(root2,width=1500,height=1530)
AadharEntry = Entry(root2)
CustomerRegistrationCanvas.create_window(300,350,window=AadharEntry)
FirstNameEntry = Entry(root2)
CustomerRegistrationCanvas.create_window(300,400,window=FirstNameEntry)
LastNameEntry = Entry(root2)
CustomerRegistrationCanvas.create_window(300,450,window=LastNameEntry)
EmailEntry = Entry(root2)
CustomerRegistrationCanvas.create_window(300,500,window=EmailEntry)
UsernameEntry = Entry(root2)
CustomerRegistrationCanvas.create_window(300,550,window=UsernameEntry)
PasswordEntry = Entry(root2)
CustomerRegistrationCanvas.create_window(300,600,window=PasswordEntry)
DOBEntry = Entry(root2)
CustomerRegistrationCanvas.create_window(300,650,window=DOBEntry)
GenderEntry = Entry(root2)
CustomerRegistrationCanvas.create_window(300,700,window=GenderEntry)
HouseNoEntry = Entry(root2)
CustomerRegistrationCanvas.create_window(1020,400,window=HouseNoEntry)
StreetEntry = Entry(root2)
CustomerRegistrationCanvas.create_window(1020,450,window=StreetEntry)
CityEntry = Entry(root2)
CustomerRegistrationCanvas.create_window(1020,500,window=CityEntry)
StateEntry = Entry(root2)
CustomerRegistrationCanvas.create_window(1020,550,window=StateEntry)
PincodeEntry = Entry(root2)
CustomerRegistrationCanvas.create_window(1020,600,window=PincodeEntry)

def RegisterCustomer():

    AadharNo = AadharEntry.get()
    FirstName = FirstNameEntry.get()
    LastName = LastNameEntry.get()
    Email = EmailEntry.get()
    Username = UsernameEntry.get()
    Password = PasswordEntry.get()
    DOB = DOBEntry.get()
    age = 0
    Gender = GenderEntry.get()
    HouseNo = HouseNoEntry.get()
    Street = StreetEntry.get()
    City = CityEntry.get()
    State = StateEntry.get()
    Pincode = PincodeEntry.get()

    sql = "insert into Customer values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (AadharNo, FirstName, LastName, Email, Username, Password, DOB, age,Gender, HouseNo, Street, City, State, Pincode)
    
    mycursor.execute(sql, val)
    # print("\n")
    # getContactNumber(aadhaarNo)
    mydb.commit()

    lbl = Label(root2, bd=0, relief=RIDGE, text="Details Registered!", fg="black", bg="white",font=("times new roman", 20))
    CustomerRegistrationCanvas.create_window(725,740,window=lbl)

def CustomerRegistration():
    CustomerRegistrationCanvas.pack()

    Title = Label(root2, bd=20, relief=RIDGE, text="IRCTC Customer Registration", fg="black", bg="white",font=("times new roman", 50, "bold"),)
    CustomerRegistrationCanvas.create_window(750,100,window=Title)

    EnterDetailsLabel = Label(root2, bd=20, relief=RIDGE, text="Enter details:", fg="black", bg="white",font=("times new roman", 25, "bold"))
    CustomerRegistrationCanvas.create_window(750,250,window=EnterDetailsLabel)

    AadharLabel = Label(root2, bd=0, relief=RIDGE, text="\nAadhar Number:", fg="black", bg="white",font=("times new roman", 15))
    CustomerRegistrationCanvas.create_window(150,350,window=AadharLabel)

    FirstNameLabel = Label(root2, bd=0, relief=RIDGE, text="First Name:", fg="black", bg="white",font=("times new roman", 15))
    CustomerRegistrationCanvas.create_window(150,400,window=FirstNameLabel)

    LastNameLabel = Label(root2, bd=0, relief=RIDGE, text="Last Name:", fg="black", bg="white",font=("times new roman", 15))
    CustomerRegistrationCanvas.create_window(150,450,window=LastNameLabel)

    EmailLabel = Label(root2, bd=0, relief=RIDGE, text="Email:", fg="black", bg="white",font=("times new roman", 15))
    CustomerRegistrationCanvas.create_window(150,500,window=EmailLabel)

    UsernameLabel = Label(root2, bd=0, relief=RIDGE, text="Username:", fg="black", bg="white",font=("times new roman", 15))
    CustomerRegistrationCanvas.create_window(150,550,window=UsernameLabel)

    PasswordLabel = Label(root2, bd=0, relief=RIDGE, text="Password:", fg="black", bg="white",font=("times new roman", 15))
    CustomerRegistrationCanvas.create_window(150,600,window=PasswordLabel)

    DOBLabel = Label(root2, bd=0, relief=RIDGE, text="DOB:", fg="black", bg="white",font=("times new roman", 15))
    CustomerRegistrationCanvas.create_window(150,650,window=DOBLabel)

    GenderLabel = Label(root2, bd=0, relief=RIDGE, text="Gender:", fg="black", bg="white",font=("times new roman", 15))
    CustomerRegistrationCanvas.create_window(150,700,window=GenderLabel)

    HouseNoLabel = Label(root2, bd=0, relief=RIDGE, text="HouseNo:", fg="black", bg="white",font=("times new roman", 15))
    CustomerRegistrationCanvas.create_window(900,400,window=HouseNoLabel)

    StreetLabel = Label(root2, bd=0, relief=RIDGE, text="Street:", fg="black", bg="white",font=("times new roman", 15))
    CustomerRegistrationCanvas.create_window(900,450,window=StreetLabel)

    CityLabel = Label(root2, bd=0, relief=RIDGE, text="City:", fg="black", bg="white",font=("times new roman", 15))
    CustomerRegistrationCanvas.create_window(900,500,window=CityLabel)

    StateLabel = Label(root2, bd=0, relief=RIDGE, text="State:", fg="black", bg="white",font=("times new roman", 15))
    CustomerRegistrationCanvas.create_window(900,550,window=StateLabel)

    PincodeLabel = Label(root2, bd=0, relief=RIDGE, text="Pincode:", fg="black", bg="white",font=("times new roman", 15))
    CustomerRegistrationCanvas.create_window(900,600,window=PincodeLabel)


    EnterButton = Button(root2,text="Enter details",command=RegisterCustomer)
    CustomerRegistrationCanvas.create_window(725,700,window=EnterButton)

    MainMenuButton = Button(root2,text = "Back to main menu",command=mainMenu)
    CustomerRegistrationCanvas.create_window(725,750,window=MainMenuButton)


    root2.mainloop()





def main():
  mainMenu()
  # opt = GetChoiceChosen()
  # if(opt == 1):
  #   customer_registration()
  # elif(opt == 2):
  #   ticket_booking()
  # elif(opt == 3):
  #   print_ticket()
  # elif(opt == 4):
  #   employee_menu()
  # elif(opt == 5):
  #   print("Cancellation Menu:\n")
  #   # cancellation_menu()
  # else:
  #   exit()

  


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