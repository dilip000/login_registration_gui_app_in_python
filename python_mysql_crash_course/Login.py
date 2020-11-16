import tkinter as tk
from tkinter import *
import tkinter.messagebox as mb
import random
import tkinter.ttk

import mysql.connector #mysql connector imported
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password=""
)
#done with db connection
db_cursor= db_connection.cursor(buffered=True)
class LoginApp(tk.Tk):
   def __init__(self):
       super().__init__()
       self.title("Login")
       self.geometry("600x450+351+174")
       self.configure(bg="#000000")
       self.lblHeading =tk.Label(self,text="Welcome to Login Page", font=("Helvetica", 16),bg="black",fg="white")
       self.lbluname = tk.Label(self,text="Enter UserName:", font=("Helvetica", 10),bg="black",fg="white")
       self.lblpsswd = tk.Label(self,text="Enter Password:", font=("Helvetica", 10),bg="black",fg="white")
       self.txtuname = tk.Entry(self,width=60)
       self.txtpasswd = tk.Entry(self,width=60, show="*")
       self.btn_login = tk.Button(self, text="Login",font=("Helvetica", 11),bg="black",fg="white",command=self.login)
       self.btn_clear= tk.Button(self, text="Clear",font=("Helvetica", 11),bg="black",fg="white",command=self.clear_form)
       self.btn_register = tk.Button(self, text="Not Member ? Register", font=("Helvetica", 11),bg="black",fg="yellow",command=self.open_registration_window)
       self.btn_exit = tk.Button(self, text="Exit",font=("Helvetica", 20),bg="black",fg="red",command=self.exit)
       self.lblHeading.place(relx=0.35, rely=0.089, height=50, width=250)
       self.lbluname.place(relx=0.235, rely=0.289, height=21, width=106)
       self.lblpsswd.place(relx=0.242, rely=0.378, height=21, width=102)
       self.txtuname.place(relx=0.417, rely=0.289,height=20, relwidth=0.273)
       self.txtpasswd.place(relx=0.417, rely=0.378,height=20, relwidth=0.273)
       self.btn_login.place(relx=0.45, rely=0.489, height=24, width=52)
       self.btn_clear.place(relx=0.54, rely=0.489, height=24, width=72)
       self.btn_register.place(relx=0.695, rely=0.489, height=24, width=175 )
       self.btn_exit.place(relx=0.75, rely=0.911, height=24, width=61)



   def open_registration_window(self):
       self.withdraw()
       window = RegisterWindow(self)
       window.grab_set()


   def open_login_success_window(self):
       self.withdraw()
       window = Login_Success_Window(self)
       window.grab_set()


   def show(self):
       """"""
       self.update()
       self.deiconify()

   def login(self):
       if db_connection.is_connected() == False:
           db_connection.connect()
       # executing cursor with execute method and pass SQL query
       db_cursor.execute("CREATE DATABASE IF NOT EXISTS User")  # Create a Database Named Bank
       db_cursor.execute("use User")  # Interact with Bank Database
       # creating required tables
       db_cursor.execute("create table if not exists USER(uid VARCHAR(30) NOT NULL  PRIMARY KEY,password VARCHAR(30),fname VARCHAR(30),lname VARCHAR(30),city VARCHAR(20),state VARCHAR(30),mobileno VARCHAR(10))")
       db_connection.commit()


       try:
           global username
           username = str(self.txtuname.get())  # Retrieving entered username
           passwd = str(self.txtpasswd.get())  # Retrieving entered password
           if username == "" :
               mb.showinfo('Information', "Please Enter Username")
               self.txtuname.focus_set()
               return
           if passwd == "" :
               mb.showinfo('Information', "Please Enter Password")
               self.txtpasswd.focus_set()
               return

           print(username)
           print(passwd)
           query ="SELECT * FROM User WHERE uid = '" + username + "' AND password = '" + passwd + "'"
           print(query)
           # implement sql Sentence
           db_cursor.execute(query)
           rowcount = db_cursor.rowcount
           print(rowcount)
           if db_cursor.rowcount == 1:
              mb.showinfo('Information', "Login Successfully")
              self.open_login_success_window()
           else:
               mb.showinfo('Information', "Login failed,Invalid Username or Password.Try again!!!")
       except:
        # Closing Connection
          db_connection.disconnect()


   def clear_form(self):
    self.txtuname.delete(0, tk.END)
    self.txtpasswd.delete(0, tk.END)
    self.txtuname.focus_set()

   def exit(self):
    MsgBox = mb.askquestion('Exit Application', 'Are you sure you want to exit the application',
                                    icon='warning')
    if MsgBox == 'yes':
        self.destroy()

#Using Toplevel widget to create a new window named Register Successful Window
class Login_Success_Window(tk.Toplevel):
   def __init__(self, parent):
         super().__init__(parent)
         self.original_frame = parent
         self.geometry("800x400")
         self.title("You Have Successfully Login -> "+str(username))
         self.configure(background="#000000")
         self.lbl_Login_success = tk.Label(self, text="Hello "+str(username)+" Welcome to Application", font=("Helvetica", 15), bg="black", fg="white")
         self.lbl_Login_success.place(relx=0.150 , rely=0.111, height=50, width=300)
          

         db_cursor.execute("SELECT * FROM user limit 0,10")
         i=1 
         for user in db_cursor:
            for j in range(len(user)):
                e = Entry(self,bg="black", fg="white") 
                e.grid(row=i, column=j) 
                e.insert(END, user[j])
            i=i+1
         # create OK button
         self.btn_register = tk.Button(self, text="Logout", font=("Helvetica", 11), bg="black", fg="white",command=self.logout)
         #self.btn_register.pack(side = tk.BOTTOM)
         self.btn_register.place(relx=0.467, rely=0.311, height=21, width=50)
   def logout(self):
        mb.showinfo('Information', "You Have Successfully Logout " + str(username))
        self.destroy()
        self.original_frame.show()

#Using Toplevel widget to create a new window named RegisterWindow to register a new user
class RegisterWindow(tk.Toplevel):
   def __init__(self, parent):
         super().__init__(parent)
         self.original_frame = parent
         self.geometry("600x450+485+162")
         self.title("Register")
         self.configure(background="#000000")

         self.lblRegister = tk.Label(self, text="Register", font=("Helvetica", 16), bg="black", fg="white")
         self.lblFName = tk.Label(self, text="Enter FirstName:", font=("Helvetica", 10), bg="black", fg="white")
         self.lblLName= tk.Label(self, text="Enter LastName:", font=("Helvetica", 10), bg="black", fg="white")
         self.lblLName = tk.Label(self, text="Enter LastName:", font=("Helvetica", 10), bg="black", fg="white")
         self.lblUId = tk.Label(self, text="Enter UserId:", font=("Helvetica", 10), bg="black", fg="white")
         self.lblPwd = tk.Label(self, text="Enter Password:", font=("Helvetica", 10), bg="black", fg="white")
         #self.lblPin = tk.Label(self, text="Enter Pin:", font=("Helvetica", 10), bg="blue", fg="yellow")
         self.lblContactNo = tk.Label(self, text="Enter Contact No:", font=("Helvetica", 10), bg="black", fg="white")
         self.lblCity = tk.Label(self, text="Enter City:", font=("Helvetica", 10), bg="black", fg="white")
         self.lblState = tk.Label(self, text="Enter State:", font=("Helvetica", 10), bg="black", fg="white")

         self.txtFName = tk.Entry(self)
         self.txtLName = tk.Entry(self)
         self.txtUId = tk.Entry(self)
         self.txtPwd = tk.Entry(self)
         self.txtContact = tk.Entry(self)
         self.txtCity = tk.Entry(self)
         self.txtState = tk.Entry(self)

         self.btn_register = tk.Button(self, text="Register", font=("Helvetica", 11), bg="black", fg="white",
                                    command=self.register)
         self.btn_cancel = tk.Button(self, text="Back To Login", font=("Helvetica", 11), bg="black", fg="white",
                                    command=self.onClose)

         self.lblRegister.place(relx=0.467, rely=0.111, height=21, width=100)
         self.lblFName.place(relx=0.318, rely=0.2, height=21, width=100)
         self.lblLName.place(relx=0.319, rely=0.267, height=21, width=100)
         self.lblUId.place(relx=0.355, rely=0.333, height=21, width=78)
         self.lblPwd.place(relx=0.319, rely=0.4, height=21, width=100)
         self.lblContactNo.place(relx=0.310, rely=0.467, height=21, width=105)
         self.lblCity.place(relx=0.375, rely=0.533, height=21, width=66)
         self.lblState.place(relx=0.369, rely=0.6, height=21, width=70)
         self.txtFName.place(relx=0.490, rely=0.2, height=20, relwidth=0.223)
         self.txtLName.place(relx=0.490, rely=0.267, height=20, relwidth=0.223)
         self.txtUId.place(relx=0.490, rely=0.333, height=20, relwidth=0.223)
         self.txtPwd.place(relx=0.490, rely=0.4, height=20, relwidth=0.223)
         self.txtContact.place(relx=0.490, rely=0.467, height=20, relwidth=0.223)
         self.txtCity.place(relx=0.490, rely=0.533, height=20, relwidth=0.223)
         self.txtState.place(relx=0.490, rely=0.6, height=20, relwidth=0.223)
         self.btn_register.place(relx=0.500, rely=0.660, height=24, width=63)
         self.btn_cancel.place(relx=0.605, rely=0.660, height=24, width=150)

   def register(self):

       if db_connection.is_connected()== False:
             db_connection.connect()
        # executing cursor with execute method and pass SQL query
       db_cursor.execute("CREATE DATABASE IF NOT EXISTS User")  # Create a Database Named AradhanaBank
       db_cursor.execute("use User")  # Interact with Bank Database
       # creating required tables
       db_cursor.execute("Create table if not exists USER(uid VARCHAR(30) NOT NULL  PRIMARY KEY,password VARCHAR(30),fname VARCHAR(30),lname VARCHAR(30),city VARCHAR(20),state VARCHAR(30),mobileno VARCHAR(10))")

       db_connection.commit()

       fname = self.txtFName.get()  # Retrieving entered first name
       lname = self.txtLName.get()  # Retrieving entered last name
       uid = self.txtUId.get()  # Retrieving entered user id
       pwd = self.txtPwd.get()  # Retrieving entered password
       #pin = self.txtPin.get()  # Retrieving entered ATM pin number
       contact_no = self.txtContact.get()  # Retrieving entered contact number
       city = self.txtCity.get()  # Retrieving entered city name
       state = self.txtState.get()  # Retrieving entered state name
       # validating Entry Widgets
       if fname == "":
           mb.showinfo('Information', "Please Enter Firstname")
           self.txtFName.focus_set()
           return
       if lname == "":
           mb.showinfo('Information', "Please Enter Lastname")
           self.txtLName.focus_set()
           return
       if uid == "":
           mb.showinfo('Information', "Please Enter User Id")
           self.txtUId.focus_set()
           return
       if pwd == "":
           mb.showinfo('Information', "Please Enter Password")
           self.txtPwd.focus_set()
           return
       
       if contact_no  == "":
           mb.showinfo('Information', "Please Enter Contact Number")
           self.txtContact.focus_set()
           return
       if city == "":
           mb.showinfo('Information', "Please Enter City Name")
           self.txtCity.focus_set()
           return
       if state  == "":
           mb.showinfo('Information', "Please Enter State Name")
           self.txtState.focus_set()
           return
       #Inserting record into bank table of bank database
       db_cursor.execute("use User")  # Interact with Bank Database
       query ="INSERT INTO User(uid,password,fname,lname,city,state,mobileno) VALUES ('%s','%s','%s','%s','%s','%s','%s')" %(uid,pwd,fname,lname,city,state,contact_no )

       try:
            # implement sql Sentence
            db_cursor.execute(query)
            mb.showinfo('Information', "Data inserted Successfully")
            # Submit to database for execution
            db_connection.commit()
       except:
            mb.showinfo('Information', "Data insertion failed!!!")
            # Rollback in case there is any error
            db_connection.rollback()
            #Close database connection
            db_connection.close()


   def onClose(self):
       """"""
       self.destroy()
       self.original_frame.show()

if __name__ == "__main__":
  app = LoginApp()
  app.mainloop()#tells Python to run the Tkinter event loop.
   #This method listens for events, such as button clicks or keypresses,
   #and blocks any code that comes after it from running until the window it's called on is closed.
   #Go ahead and close the window you've created, and you'll see a new prompt displayed in the shell