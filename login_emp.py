from os import PRIO_PGRP
from tkinter import*
from tkinter import ttk
import random
import time
import datetime
from tkinter import messagebox
from tkinter.tix import INTEGER
import mysql.connector



def main():
    win=Tk()
    app=login_window(win)
    win.mainloop()

class login_window:
    def __init__(self,root):
        self.root=root
        self.root.title("login")
        self.root.geometry("1550x800+0+0")

        frame=Frame(self.root,bg="black")
        frame.place(x=610,y=170,width=340,height=450)

        login_head=Label(frame,text="Employee Login",bg="black",fg="red",font=("times new roman",30,"bold"))
        login_head.place(x=80,y=100)

        Empi_id=Label(frame,text="Employee ID",font=("times new roman",15,"bold"),fg="yellow",bg="black")
        Empi_id.place(x=40,y=155)
        self.txtempid=Entry(frame,font=("times new roman",15,"bold"))
        self.txtempid.place(x=40,y=180,width=270)

        login_btn=Button(frame,text="Login",font=("times new roman",15,"bold"),bd=3,relief=RIDGE,fg="black",bg="yellow",command=self.login_func,activebackground="yellow")
        login_btn.place(x=110,y=225,width=120,height=35)

        register_btn=Button(frame,text="Register Employee",borderwidth=0 ,command=self.register_window,font=("times new roman",15,"bold"),bd=3,relief=RIDGE,fg="blue",bg="black")
        register_btn.place(x=50,y=300,width=120)
    
    def register_window(self):
        self.new_window=Toplevel(self.root)
        self.app=Employee(self.new_window)


    def login_func(self):
        if self.txtempid.get()=="":
            messagebox.showerror("Error, please insert Empid")

class Employee:
    def __init__(self,root):
        self.root=root
        self.root.title("Emploee Management System")
        self.root.geometry("1540x800+0+0")

        self.inputempid=StringVar()
        self.inputfname = StringVar()
        self.inputlname = StringVar()
        self.inputdob = StringVar()
        self.inputage = StringVar()
        self.inputsalary = StringVar()
        self.inputdesignation = StringVar()
        self.inputgender = StringVar()
        self.inputhno = StringVar()
        self.inputstreet = StringVar()
        self.inputcity = StringVar()
        self.inputstate = StringVar()
        self.inputpincode = StringVar()

        





        lbltitle=Label(self.root,bd=20,relief=RIDGE,text="Employee Management System",fg="red",bg="white",font=("times new roman",50,"bold"))
        lbltitle.pack(side=TOP,fill=X)


        dataframe=Frame(self.root,bd=20,relief=RIDGE)
        dataframe.place(x=0,y=130,width=1530,height=400)
        dataframeleft=LabelFrame(dataframe,bd=10,relief=RIDGE,padx=10,font=("arial",12,"bold"),text="Employee Information")
        dataframeleft.place(x=0,y=5,width=980,height=350)

     

        detailsframe=Frame(self.root,bd=20,relief=RIDGE)
        detailsframe.place(x=0,y=600,width=1530,height=190)

        lblnameemp_id=Label(dataframeleft,text="Employee ID",font=("times new roman",12,"bold"),padx=2,pady=6)
        lblnameemp_id.grid(row=0,column=0,sticky=W)
        txt_empid=Entry(dataframeleft,font=("arial",13,"bold"),textvariable=self.inputempid,width=35)
        txt_empid.grid(row=0,column=1)

        lblfirst_name = Label(dataframeleft, text="First Name", font=("times new roman", 12, "bold"), padx=2, pady=6)
        lblfirst_name.grid(row=1, column=0, sticky=W)
        txt_fname = Entry(dataframeleft, font=("arial", 13, "bold"),textvariable=self.inputfname, width=35)
        txt_fname.grid(row=1, column=1)

        lbllast_name = Label(dataframeleft, text="Last Name", font=("times new roman", 12, "bold"), padx=2, pady=6)
        lbllast_name.grid(row=2, column=0, sticky=W)
        txt_lname = Entry(dataframeleft, font=("arial", 13, "bold"),textvariable=self.inputlname, width=35)
        txt_lname.grid(row=2, column=1)

        lblDOB = Label(dataframeleft, text="Date Of Birth", font=("times new roman", 12, "bold"), padx=2, pady=6)
        lblDOB.grid(row=3, column=0, sticky=W)
        txt_dob = Entry(dataframeleft, font=("arial", 13, "bold"),textvariable=self.inputdob, width=35)
        txt_dob.grid(row=3, column=1)

        lblAGE = Label(dataframeleft, text="Age", font=("times new roman", 12, "bold"), padx=2, pady=6)
        lblAGE.grid(row=4, column=0, sticky=W)
        txt_age = Entry(dataframeleft, font=("arial", 13, "bold"),textvariable=self.inputage, width=35)
        txt_age.grid(row=4, column=1)

        lblgen = Label(dataframeleft, text="Gender", font=("times new roman", 12, "bold"), padx=2, pady=6)
        lblgen.grid(row=5, column=0, sticky=W)
        txt_gen = Entry(dataframeleft, font=("arial", 13, "bold"),textvariable=self.inputgender, width=35)
        txt_gen.grid(row=5, column=1)

        lblsal= Label(dataframeleft, text="Salary", font=("times new roman", 12, "bold"), padx=2, pady=6)
        lblsal.grid(row=6, column=0, sticky=W)
        txt_sal = Entry(dataframeleft, font=("arial", 13, "bold"),textvariable=self.inputsalary, width=35)
        txt_sal.grid(row=6, column=1)

        lbldesg = Label(dataframeleft, text="Designation", font=("times new roman", 12, "bold"), padx=2, pady=6)
        lbldesg.grid(row=7, column=0, sticky=W)
        txt_desg = Entry(dataframeleft, font=("arial", 13, "bold"),textvariable=self.inputdesignation, width=35)
        txt_desg.grid(row=7, column=1)

        lblhno = Label(dataframeleft, text="House Number", font=("times new roman", 12, "bold"), padx=2, pady=6)
        lblhno.grid(row=0, column=2, sticky=W)
        txt_hno = Entry(dataframeleft, font=("arial", 13, "bold"),textvariable=self.inputhno, width=35)
        txt_hno.grid(row=0, column=3)

        lblstr = Label(dataframeleft, text="Street", font=("times new roman", 12, "bold"), padx=2, pady=6)
        lblstr.grid(row=1, column=2, sticky=W)
        txt_str = Entry(dataframeleft, font=("arial", 13, "bold"),textvariable=self.inputstreet, width=35)
        txt_str.grid(row=1, column=3)

        lblcty = Label(dataframeleft, text="City", font=("times new roman", 12, "bold"), padx=2, pady=6)
        lblcty.grid(row=2, column=2, sticky=W)
        txt_cty = Entry(dataframeleft, font=("arial", 13, "bold"),textvariable=self.inputcity, width=35)
        txt_cty.grid(row=2, column=3)

        lblstate = Label(dataframeleft, text="State", font=("times new roman", 12, "bold"), padx=2, pady=6)
        lblstate.grid(row=3, column=2, sticky=W)
        txt_state = Entry(dataframeleft, font=("arial", 13, "bold"),textvariable=self.inputstate, width=35)
        txt_state.grid(row=3, column=3)

        lblpincode = Label(dataframeleft, text="Pincode", font=("times new roman", 12, "bold"), padx=2, pady=6)
        lblpincode.grid(row=4, column=2, sticky=W)
        txt_pincode = Entry(dataframeleft, font=("arial", 13, "bold"),textvariable=self.inputpincode, width=35)
        txt_pincode.grid(row=4, column=3)


        scroll_x=ttk.Scrollbar(detailsframe, orient=HORIZONTAL)
        scroll_y= ttk.Scrollbar(detailsframe, orient=VERTICAL)
        self.Employee=ttk.Treeview(detailsframe, column=("Emp_ID", "First_Name", "Last_Name", "DOB", "age", "gender" ,"Salary" ,"Designation", "House_No","Street","city","state","PINCODE"), xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x=ttk.Scrollbar(command=self.Employee.xview)
        scroll_y=ttk.Scrollbar(command=self.Employee.yview)

        self.Employee.heading("Emp_ID", text="Employee ID")
        self.Employee.heading("First_Name", text="First Name")
        self.Employee.heading("Last_Name", text="Last Name")
        self.Employee.heading("DOB", text="Date Of Birth")
        self.Employee.heading("age", text="Age")
        self.Employee.heading("gender", text="Gender")
        self.Employee.heading("Salary", text="Salary")
        self.Employee.heading("Designation", text="Designation")
        self.Employee.heading("House_No", text="House Number")
        self.Employee.heading("Street", text="Street")
        self.Employee.heading("city", text="City")
        self.Employee.heading("state", text="State")
        self.Employee.heading("PINCODE", text="Pincode")

        self.Employee["show"]="headings"
        self.Employee.pack(fill=BOTH,expand=1)
        self.fetch_data()
        self.Employee.bind("<ButtonRelease-1>",self.get_cursor)
        buttonframe=Frame(self.root,bd=20,relief=RIDGE)
        buttonframe.place(x=0,y=530,width=1530,height=70)

        btnemployee_details=Button(buttonframe,text="Employee Details",bg="green",font=("arial",12,"bold"),command=self.employeedetails,width=23,height=16,padx=2,pady=6 )
        btnemployee_details.pack(side=RIGHT)
# need to add these functionalirties to other page
        btnupdate=Button(buttonframe,text="Update",font=("arial",12,"bold"),bg="green",command=self.update_data,width=23,height=16,padx=2,pady=6 )
        btnupdate.pack(side=LEFT)

        btndelete=Button(buttonframe,text="Delete",bg="green",font=("arial",12,"bold"),command=self.delete,width=23,height=16,padx=2,pady=6 )
        btndelete.pack(side=TOP)

        # creating the button functionalities

    def employeedetails(self):
        if self.inputempid.get()=="" or self.inputfname.get()=="":
            #messagebox.showerror("Error, Please fill all the details!")
            print()
        else:
            #messagebox.showinfo("Congratulations! Data added in Database")
            con=mysql.connector.connect(host="localhost",user="root",password="",database = "dbms")
            db_cursor=con.cursor()
            db_cursor.execute("insert into Employee values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (self.inputempid.get(), self.inputfname.get(), self.inputlname.get(),self.inputdob.get(), self.inputage.get(),self.inputgender.get(),self.inputsalary.get(),self.inputhno.get(), self.inputstreet.get(),self.inputcity.get(),self.inputstate.get(),self.inputpincode.get(),self.inputdesignation.get()))
            con.commit()
            self.fetch_data()
            con.close()
    
    def fetch_data(self):
        con=mysql.connector.connect(host="localhost",user="root",password="",database = "dbms")
        db_cursor=con.cursor()
        db_cursor.execute("select * from Employee")
        rows=db_cursor.fetchall()
        if len(rows)!=0:
            self.Employee.delete(*self.Employee.get_children())
            for i in rows:
                self.Employee.insert("",END,values=i)
            con.commit()
        con.close()

    
    def get_cursor(self,event=""):
        cursor_rows=self.Employee.focus()
        content=self.Employee.item(cursor_rows)
        row=content["values"]
        self.inputempid.set(row[0])
        self.inputfname.set(row[1])
        self.inputlname.set(row[2])
        self.inputdob.set(row[3])
        self.inputage.set(row[4])
        self.inputsalary.set(row[6])
        self.inputdesignation.set(row[7])
        self.inputgender.set(row[5])
        self.inputhno.set(row[8])
        self.inputstreet.set(row[9])
        self.inputcity.set(row[10])
        self.inputstate.set(row[12])
        self.inputpincode.set(row[11])

    
    def update_data(self):
        con=mysql.connector.connect(host="localhost",user="root",password="",database = "dbms")
        db_cursor=con.cursor()
        db_cursor.execute("update Employee set First_Name=%s,Last_Name=%s,DOB=%s,age=%s,gender=%s,Salary=%s,House_No=%s,Street=%s,city=%s,state=%s,PINCODE=%s,Designation=%s where Emp_ID=%s",(self.inputfname.get(), self.inputlname.get(),self.inputdob.get(), self.inputage.get(),self.inputgender.get(),self.inputsalary.get(),self.inputhno.get(), self.inputstreet.get(),self.inputcity.get(),self.inputstate.get(),self.inputpincode.get(),self.inputdesignation.get(),self.inputempid.get()))
        con.commit()
        con.close()
        self.fetch_data()

    def delete(self):
        con=mysql.connector.connect(host="localhost",user="root",password="",database = "dbms")
        db_cursor=con.cursor()
        query="delete from Employee where Emp_ID=%s"
        value=(self.inputempid.get(),)
        db_cursor.execute(query,value)

        con.commit()
        con.close()
        self.fetch_data()
                





main()