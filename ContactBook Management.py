from tkinter import *
from tkinter import ttk, messagebox
import sqlite3

class ContactManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Book")
        self.root.resizable(False,False)
        self.root.configure(bg='#F0F0F0')
        self.root.attributes('-fullscreen', True)
        title = Label(self.root, text="Contact Book", font=("Helvetica", 30, "bold"), bd=18, bg='#333', fg='#F0F0F0')
        title.pack(side=TOP, fill=X)
        self.firstname = StringVar()
        self.lastname = StringVar()
        self.mobile = StringVar()
        self.addr = StringVar()
        self.pin = StringVar()
        Detail_F = Frame(self.root, bd=4, relief=RIDGE, bg='#333')
        Detail_F.place(x=600, y=120, width=350, height=300)
        labels = ['First Name', 'Last Name', 'Mobile No.', 'Address', 'PinCode']
        variables = [self.firstname, self.lastname, self.mobile, self.addr, self.pin]
        for i, (label, var) in enumerate(zip(labels, variables)):
            lbl = Label(Detail_F, text=label, font=("Helvetica", 12, "bold"), bg='#333', fg='white')
            lbl.grid(row=i, column=0, pady=10, padx=20, sticky="w")
            entry = Entry(Detail_F, textvariable=var, font=("Helvetica", 10), bd=3, width=18)
            entry.grid(row=i, column=1, pady=10, sticky="w")
        btnFrame = Frame(self.root, bd=5, relief=RIDGE, bg='#F0F0F0')
        btnFrame.place(x=350, y=450, width=750, height=70)
        btn_texts = ['Add Record', 'Update', 'Delete', 'Reset', 'Display Records']
        btn_commands = [self.addrecord, self.update, self.delete, self.reset, self.display_records]
        for i, (text, cmd) in enumerate(zip(btn_texts, btn_commands)):
            btn = Button(btnFrame, text=text, font=("Helvetica", 12, "bold"), bg='#007ACC', fg='white', width=12, command=cmd)
            btn.grid(row=0, column=i, padx=10, pady=10)

    def addrecord(self):
        if self.firstname.get() == '' or self.lastname.get() == '' or self.mobile.get() == '' or self.addr.get() == '' or self.pin.get() == '':
            messagebox.showerror('Error', 'Please enter details!')
        else:
            con = sqlite3.connect('contactbook.db')
            cur = con.cursor()
            cur.execute("SELECT * FROM contact WHERE mobile=?", (self.mobile.get(),))
            if cur.fetchone():
                messagebox.showerror('Error', 'Duplicate mobile numbers are not allowed!')
                return
            cur.execute("INSERT INTO contact VALUES (?, ?, ?, ?, ?)", (self.firstname.get(), self.lastname.get(), self.mobile.get(), self.addr.get(), self.pin.get()))
            con.commit()
            con.close()
            self.reset()

    def fetch_data(self):
        con = sqlite3.connect('contactbook.db')
        cur = con.cursor()
        cur.execute("SELECT firstname, lastname, mobile, addr, pin FROM contact")
        rows = cur.fetchall()
        con.close()
        return rows

    def display_records(self):
        records_window = Toplevel(self.root)
        records_window.title("Contact Records")
        records_window.geometry("600x400")

        
        recordFrame = Frame(records_window, bd=4, relief=RIDGE, bg='#333')
        recordFrame.pack(fill=BOTH, expand=True)
        
        yscroll = Scrollbar(recordFrame, orient=VERTICAL)
        contact_table = ttk.Treeview(recordFrame, columns=("firstname", "lastname", "mobile", "address", "pin"), yscrollcommand=yscroll.set, selectmode="browse")
        yscroll.pack(side=RIGHT, fill=Y)
        yscroll.config(command=contact_table.yview)

        contact_table.heading("firstname", text="First Name")
        contact_table.heading("lastname", text="Last Name")
        contact_table.heading("mobile", text="Mobile No.")
        contact_table.heading("address", text="Address")
        contact_table.heading("pin", text="PinCode")
        contact_table['show'] = 'headings'
        
        for col in ["firstname", "lastname", "mobile", "address", "pin"]:
            contact_table.column(col, width=100)
        style = ttk.Style()
        style.configure("Treeview", background="#E0E0E0", foreground="black", rowheight=25, fieldbackground="#F0F0F0")
        style.map("Treeview", background=[('selected', '#b6c2d1')])

        contact_table.pack(fill=BOTH, expand=1)
        rows = self.fetch_data()
        for row in rows:
            contact_table.insert('', END, values=row)

        
        def on_record_select(event):
            selected_row = contact_table.focus()
            values = contact_table.item(selected_row, 'values')
            if values:
                self.firstname.set(values[0])
                self.lastname.set(values[1])
                self.mobile.set(values[2])
                self.addr.set(values[3])
                self.pin.set(values[4])
            records_window.destroy()  

        contact_table.bind("<ButtonRelease-1>", on_record_select)

    def update(self):
        if self.mobile.get() == '':
            messagebox.showerror('Error', 'Select a record to update!')
        else:
            con = sqlite3.connect('contactbook.db')
            cur = con.cursor()
            cur.execute("UPDATE contact SET firstname=?, lastname=?, addr=?, pin=? WHERE mobile=?", (self.firstname.get(), self.lastname.get(), self.addr.get(), self.pin.get(), self.mobile.get()))
            messagebox.showinfo('Info', f'Record {self.mobile.get()} updated successfully')
            con.commit()
            con.close()
            self.reset()

    def delete(self):
        if self.mobile.get() == '':
            messagebox.showerror('Error', 'Select a record to delete!')
        else:
            con = sqlite3.connect('contactbook.db')
            cur = con.cursor()
            cur.execute("DELETE FROM contact WHERE mobile=?", (self.mobile.get(),))
            con.commit()
            con.close()
            messagebox.showinfo('Info', f'Record {self.mobile.get()} deleted successfully')
            self.reset()

    def reset(self):
        self.firstname.set('')
        self.lastname.set('')
        self.mobile.set('')
        self.addr.set('')
        self.pin.set('')


class Login:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("300x200")
        self.root.configure(bg='#F0F0F0')
        self.username = StringVar()
        self.password = StringVar()

        Label(self.root, text="Username:", font=("Helvetica", 12, "bold"), bg='#F0F0F0').grid(row=0, column=0, padx=10, pady=10)
        Entry(self.root, textvariable=self.username, font=("Helvetica", 10)).grid(row=0, column=1, padx=10, pady=10)
        
        Label(self.root, text="Password:", font=("Helvetica", 12, "bold"), bg='#F0F0F0').grid(row=1, column=0, padx=10, pady=10)
        Entry(self.root, textvariable=self.password, show="*", font=("Helvetica", 10)).grid(row=1, column=1, padx=10, pady=10)

        Button(self.root, text="Login", font=("Helvetica", 12, "bold"), bg='Red', fg='white', command=self.login).grid(row=2, column=0, padx=10, pady=20)

    def login(self):
        if self.username.get() == "user" and self.password.get() == "admin":
            self.root.destroy()
            r = Tk()
            ContactManager(r)
        else:
            messagebox.showerror("Error", "Invalid username or password")


con = sqlite3.connect('contactbook.db')
cur = con.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS contact (firstname TEXT, lastname TEXT, mobile TEXT PRIMARY KEY, addr TEXT, pin TEXT)')
con.close()

root = Tk()
Login(root)
root.mainloop()
