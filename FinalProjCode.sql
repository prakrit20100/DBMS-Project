use Railway_Management_System;
ALTER TABLE Customer_contact ADD FOREIGN KEY (Aadhaar_Number) REFERENCES Customer(AAdhaar_Number);

-- TRIGGER
-- TRIGGER 1
CREATE TRIGGER calc_age after INSERT on Customer_contact for each row update CUSTOMER set CUSTOMER.age = YEAR(CURDATE()) - YEAR(Customer.DOB);
-- TRIGGER 2
CREATE TRIGGER calc_age_emp after INSERT on Employee_contact for each row update Employee set Employee.age = YEAR(CURDATE()) - YEAR(Employee.DOB);

-- TRIGGER 3
delimiter #
create trigger check_phn_no before insert on Customer_contact
for each row
BEGIN
IF(length(NEW.Phone_no) <> 10) THEN
    SET NEW.Phone_no = "XXXXXXXXXX";
END IF;
END#
delimiter ;
-- Statement to check Trigger 3
INSERT into Customer_contact values('123123123', '9999991999');

-- Trigger 4
delimiter #
create trigger check_phn_no_employee before insert on Employee_contact
for each row
BEGIN
IF(length(NEW.phone_no) <> 10) THEN
    SET NEW.phone_no = "XXXXXXXXXX";
END IF;
END#
delimiter ;

-- Testing Trigger 4
INSERT into Employee_contact(Emp_ID, phone_no) values('99998888', '99');

-- Trigger 5
delimiter #
create trigger check_PINCODE before insert on Customer
for each row
BEGIN
IF(length(NEW.PINCODE) <> 6) THEN
    SET NEW.PINCODE = "XXXXXX";
END IF;
END#
delimiter ;

-- VIEWS
CREATE VIEW Customer_Contact_Details AS SELECT cc.Aadhaar_Number, cc.Phone_no, c.Email FROM Customer c, Customer_contact cc WHERE c.Aadhaar_Number=cc.Aadhaar_Number; 
CREATE VIEW train_schedule AS SELECT Train_Name, Source, Destination, Start_Time, End_Time FROM Train;
CREATE VIEW Employee_Comm_Details AS SELECT ec.Emp_ID, ec.Phone_no, e.House_No, e.Street, e.city, e.state, e.PINCODE FROM Employee e, Employee_contact ec WHERE ec.Emp_ID = e.Emp_ID; 

            
-- INDEXING
CREATE INDEX username_password ON Customer (Username, Password);
CREATE UNIQUE INDEX ticket_number_index ON Ticket(Ticket_Number);
CREATE INDEX train_src_dest ON Train(Source, Destination);
CREATE UNIQUE INDEX train_number_index ON Train(Train_Number);
CREATE UNIQUE INDEX Emp_ID_index ON Employee(Emp_ID);


-- GRANTS
GRANT SELECT, INSERT, DELETE, UPDATE ON Employee TO 'root'@localhost;
GRANT SELECT, INSERT, DELETE ON Ticket TO 'Customer1'@localhost;
GRANT SELECT, INSERT, DELETE, UPDATE ON Employee TO 'Admin1'@localhost;

