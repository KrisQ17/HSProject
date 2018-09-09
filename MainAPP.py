import tkinter as tk
from database import *
from tkinter import messagebox
import time

LARGE_FONT = ("Verdana, 12")
FONT2 = ("Arimo, 16")
FONT3 = ("Arimo, 12")

localtime = time.localtime(time.time())
currenttime = "{:02d}/{:02d}/{} {:02d}:{:02d}".format(localtime[2], localtime[1], localtime[0], localtime[3], localtime[4])

emp = Employees()
login_user = Login()



class LoginCheck():
    pass

LC = LoginCheck()
LC.login = ''
LC.password = ''

class MainAPP(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "Arsenal Palace Schedule")
        self.containers = {}
        self.frames = {}
        self.show_container(LoginPage)
        self.show_frame(LoginPage)

    def show_frame(self, cont):
        container = self.containers[cont]
        frame = cont(container, self)
        self.frames[cont] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()

    def show_container(self, cont):
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)
        self.containers[cont] = container

    def del_frame(self, cont):
        frame = self.frames[cont]
        frame.destroy()

    def del_container(self, cont):
        container = self.containers[cont]
        container.destroy()

    def freeze_MM(self):
        frame = self.frames[MainMenu]
        for child in frame.winfo_children():
            if 'button' in str(child):
                if not 'button7' in str(child): #button7 -> refresh list by updateMMList, can't be disabled
                    child.configure(state='disable')

    def unfreeze_MM(self):
        frame = self.frames[MainMenu]
        for child in frame.winfo_children():
            if 'button' in str(child):
                    child.configure(state='normal')

    def updateMMList(self):
        frame = self.frames[MainMenu]
        frame.invoke_refresh()

class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        login_text = tk.Label(self, text="Login")
        login_text.grid(row=0, column=0, padx=10, pady=10)

        login_entry = tk.Entry(self)
        login_entry.grid(row=0, column=1, padx=10, pady=10)

        password_text = tk.Label(self, text="Password")
        password_text.grid(row=1, column=0, padx=5, pady=10)

        password_entry = tk.Entry(self)
        password_entry.grid(row=1, column=1, padx=5, pady=10)

        login_button = tk.Button(self, text="Log In", font=LARGE_FONT, bd=4,
                                 command=lambda: self.check_password(login_entry.get(), password_entry.get(), controller))
        login_button.grid(row=0, column=3, rowspan=2, padx=10, pady=10, ipadx=10, ipady=10)

    def check_password(self, login, password, controller):
        LC.login = login
        LC.password = password
        if LC.login in login_user.user.keys() and LC.password == login_user.user[LC.login]:
            controller.del_container(LoginPage)
            controller.show_container(MainMenu)
            controller.show_frame(MainMenu)
        else:
            controller.del_container(LoginPage)
            controller.show_container(MainMenu)
            controller.show_frame(MainMenu)
            #messagebox.showwarning('Something went wrong', "Wrong login or password\nPlease, try again!")

class MainMenu(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        schedule_button = tk.Button(self, text="Schedule", font=FONT2, width=20)
        schedule_button.grid(row=0, column=0, padx=5, pady=5, sticky='w')

        add_employee = tk.Button(self, text="Add Employee", font=FONT2, width=20,
                                 command=lambda: self.add(controller))
        add_employee.grid(row=1, column=0, padx=5, pady=5, sticky='w')

        delete_employee = tk.Button(self, text="Delete Employee", font=FONT2, width=20,
                                    command=lambda: self.delete(controller))
        delete_employee.grid(row=2, column=0, padx=5, pady=5, sticky='w')

        info_employees = tk.Button(self, text="Edit Employee", font=FONT2, width=20,
                                   command=lambda: self.infoemp(controller))
        info_employees.grid(row=3, column=0, padx=5, pady=5, sticky='w')

        availability = tk.Button(self, text="Availability", font=FONT2, width=20)
        availability.grid(row=4, column=0, padx=5, pady=5, sticky='w')

        notes = tk.Button(self, text="Notes", font=FONT2, width=20, command=lambda: self.notes(controller))
        notes.grid(row=5, column=0, padx=5, pady=5, sticky='w')

        logged = tk.Label(self, text="Logged as: {}".format(LC.login))
        logged.grid(row=6, column=0, columnspan=2, sticky='sw', pady=10)

        employee_list = tk.LabelFrame(self, text="Employees List", font=FONT3)
        employee_list.grid(row=0, rowspan=6, column=1, sticky='n')
        self.ListEmplo = tk.Label(employee_list, text=self.print_employees(), width=20, anchor='nw', justify='left', font=FONT2)
        self.ListEmplo.pack(expand=True)

        self.refresh_button = tk.Button(self, text="Refresh", command=lambda: self.refresh())
        self.refresh_button.grid_forget()

    def refresh(self):
        self.ListEmplo.configure(text=self.print_employees())
    def invoke_refresh(self):
        self.refresh_button.invoke()
    def print_employees(self):
        # Display workers as list (MainMenu)
        ret = ''
        chc = 0
        for worker in sorted(emp.workers):
            chc += 1
            if chc == len(emp.workers):
                ret += worker
            else:
                ret += worker + '\n'
        return (ret)
    def add(self, controller):
        controller.freeze_MM()
        AddEmployee(self, controller)
    def delete(self, controller):
        controller.freeze_MM()
        DeleteEmployee(self, controller)
    def infoemp(self, controller):
        controller.freeze_MM()
        EditEmployees(self, controller)
    def notes(self, controller):
        controller.freeze_MM()
        Notes(self, controller)

class AddEmployee(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.top = tk.Toplevel()

        name = tk.Label(self.top, text="Name")
        name.grid(row=0, column=0, columnspan=2, sticky='w', padx=15, pady=5)
        self.name_entry = tk.Entry(self.top, width=25)
        self.name_entry.grid(row=0, column=1, columnspan=2, sticky='w', padx=15, pady=5)

        surname = tk.Label(self.top, text="Surname")
        surname.grid(row=1, column=0, sticky='w', padx=15, pady=5)
        self.surname_entry = tk.Entry(self.top, width=25)
        self.surname_entry.grid(row=1, column=1, columnspan=2, sticky='w', padx=15, pady=5)

        age = tk.Label(self.top, text="Age")
        age.grid(row=2, column=0, sticky='w', padx=15, pady=5)
        self.age_entry = tk.Entry(self.top, width=25)
        self.age_entry.grid(row=2, column=1, columnspan=2, sticky='w', padx=15, pady=5)

        birthday = tk.Label(self.top, text="Birthday")
        birthday.grid(row=3, column=0, columnspan=2, sticky='w', padx=15, pady=5)
        self.birthday_entry = tk.Entry(self.top, width=25)
        self.birthday_entry.insert(0, 'dd/mm/yyyy')
        self.birthday_entry.grid(row=3, column=1, columnspan=2, sticky='w', padx=15, pady=5)

        info = tk.Label(self.top, text="Information")
        info.grid(row=4, column=0, columnspan=2, sticky='w', padx=15, pady=5)
        self.info_entry = tk.Entry(self.top, width=25)
        self.info_entry.grid(row=4, column=1, columnspan=2, sticky='w', padx=15, pady=5)

        save = tk.Button(self.top, text="Save", width=10, command=lambda: self.saveworker(controller))
        save.grid(row=5, column=0, sticky='s', padx=10, pady=10)

        clear = tk.Button(self.top, text="Clear All", width=10,
                          command=lambda: self.clearframe())
        clear.grid(row=5, column=1, sticky='s', padx=10, pady=10)

        back = tk.Button(self.top, text="Back", width=10, command=lambda: self.closeframe(controller))
        back.grid(row=5, column=2, sticky='s', padx=10, pady=10)

        self.top.resizable(width=False, height=False)
        self.top.protocol("WM_DELETE_WINDOW", lambda: self.closeframe(controller))
        self.top.mainloop()

    def closeframe(self, cont):
        self.top.destroy()
        cont.unfreeze_MM()

    def clearframe(self):
        self.name_entry.delete(0, 'end')
        self.surname_entry.delete(0, 'end')
        self.age_entry.delete(0, 'end')
        self.birthday_entry.delete(0, 'end')
        self.info_entry.delete(0, 'end')

    def saveworker(self, controller):
        emp.add_employee(self.name_entry.get(), self.surname_entry.get(), self.age_entry.get(),
                       self.birthday_entry.get(), self.info_entry.get())
        controller.updateMMList()

class DeleteEmployee(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.top = tk.Toplevel()

        name = tk.Label(self.top, text='Full Name')
        name.grid(row=0, column=0, padx=5, pady=10, sticky='n')

        back = tk.Button(self.top, text='Back', command=lambda: self.closeframe(controller), width=15, bg='cyan')
        back.grid(row=0, column=1, padx=5, pady=10, sticky='n')

        self.show(controller)

        self.top.resizable(width=False, height=False)
        self.top.protocol("WM_DELETE_WINDOW", lambda: self.closeframe(controller))
        self.top.mainloop()

    def show(self, controller):
        self.delete_list = {}
        self.buttons= {}
        it = 0
        for worker in sorted(emp.workers.keys()):
            it += 1
            label = tk.Label(self.top, text=worker, width=15)
            label.grid(row=it, column=0, sticky='w')
            button = tk.Button(self.top, text='Delete', width=20, justify='right', relief='groove',
                               command=lambda i=worker: self.delete(i, controller))
            button.grid(row=it, column=1, pady=5, padx=10)
            self.delete_list[worker] = (label, button)

    def delete(self, name, controller):
        label = self.delete_list[name][0]
        label.configure(text='Done!', fg='red', anchor='e')
        emp.delete(name)
        controller.updateMMList()

    def closeframe(self, cont):
        self.top.destroy()
        cont.unfreeze_MM()

class EditEmployees(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.top = tk.Toplevel()
        self.entries = {}

        name = tk.Label(self.top, text='Name')
        name.grid(row=0, column=0, pady=5)

        surname = tk.Label(self.top, text='Surname')
        surname.grid(row=0, column=1, pady=5)

        age = tk.Label(self.top, text='Age')
        age.grid(row=0, column=2, pady=5)

        birthday = tk.Label(self.top, text='Birthday')
        birthday.grid(row=0, column=3, pady=5)

        info = tk.Label(self.top, text='Extended Info')
        info.grid(row=0, column=4, pady=5)

        back = tk.Button(self.top, text='Back', bg='cyan', width=10,
                         command=lambda: self.closeframe(controller))
        back.grid(row=0, column=5, pady=5)

        self.show(controller)

        self.top.resizable(width=False, height=False)
        self.top.protocol("WM_DELETE_WINDOW", lambda: self.closeframe(controller))
        self.top.mainloop()

    def show(self, controller):
        it = 0
        for et in sorted(emp.workers.keys()):
            name_split = et.split(" ")
            it += 1
            name = tk.Entry(self.top, width=20) #name
            name.insert(0, name_split[0])
            name.configure(state='readonly')
            name.grid(row=it, column=0)
            surname = tk.Entry(self.top, width=20) #surname
            surname.insert(0, name_split[1])
            surname.configure(state='readonly')
            surname.grid(row=it, column=1)
            age = tk.Entry(self.top, width=20) #age
            age.insert(0, emp.workers[et][0])
            age.configure(state='readonly')
            age.grid(row=it, column=2)
            birthday = tk.Entry(self.top, width=20) #birthday
            birthday.insert(0, emp.workers[et][1])
            birthday.configure(state='readonly')
            birthday.grid(row=it, column=3)
            info = tk.Entry(self.top, width=20) #info
            info.insert(0, emp.workers[et][2])
            info.configure(state='readonly')
            info.grid(row=it, column=4)
            button = tk.Button(self.top, text='Edit', width=10, command=lambda i=et: self.edit(i, controller))
            button.grid(row=it, column=5, padx=10, pady=5)
            self.entries[et] = (name, surname, age, birthday, info, button)

    def closeframe(self, cont):
        self.top.destroy()
        cont.unfreeze_MM()

    def edit(self, name, controller):
        ent = self.entries[name]
        for int in range(len(ent)-1):
            entry = ent[int].configure(state='normal')
        button_save = ent[5].configure(text='Save', command=lambda x=name: self.save(x, controller))

    def save(self, name, controller):
        ent = self.entries[name]
        new_key = ent[0].get() + " " + ent[1].get()
        if new_key != name:
            if name in str(emp.workers.keys()):
                emp.workers[new_key] = emp.workers[name]
                emp.workers[new_key] = (ent[2].get(), ent[3].get(), ent[4].get())
                del emp.workers[name]
            if name in str(self.entries.keys()):
                self.entries[new_key] = self.entries[name]
                del self.entries[name]
            for int in range(len(self.entries[new_key]) - 1):
                entry = self.entries[new_key][int].configure(state='readonly')
            button_save = self.entries[new_key][5].configure(text='Edit',
                                                             command=lambda i=new_key: self.edit(i, controller))
        if new_key == name:
            emp.workers[name] = (ent[2].get(), ent[3].get(), ent[4].get())
            button_save = self.entries[name][5].configure(text='Edit', command=lambda i=new_key: self.edit(i, controller))
            for int in range(len(self.entries[name])-1):
                entry = self.entries[name][int].configure(state='readonly')
        controller.updateMMList()

class Notes(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        notes = Notes()

        self.top = tk.Toplevel()

        self.notes_list= {}

        add = tk.Button(self.top, text='Add', width=15, command=lambda: self.add_note(controller))
        add.grid(row=0, column=0, sticky='nw', pady=5, padx=5)

        delete = tk.Button(self.top, text='Delete', width=15)
        delete.grid(row=1, column=0, sticky='nw', pady=5, padx=5)

        edit = tk.Button(self.top, text='Edit', width=15)
        edit.grid(row=2, column=0, sticky='nw', pady=5, padx=5)

        back = tk.Button(self.top, text='Back', width=15, command=lambda: self.closeframe(controller))
        back.grid(row=3, column=0, sticky='s', pady=5, padx=5)

        self.show()

        self.top.resizable(width=False, height=False)
        self.top.protocol("WM_DELETE_WINDOW", lambda: self.closeframe(controller))
        self.top.mainloop()


    def show(self):
        pass
    def add_note(self, controller):
        self.upFrame = tk.Toplevel()

        note = tk.Label(self.upFrame, text='Note')
        note.grid(row=0, column=0, columnspan=3)

        scrollbar = tk.Scrollbar(self.upFrame, orient='vertical', width=20)
        scrollbar.grid(row=1, column=3, ipady=60, sticky='w')

        entry_note = tk.Text(self.upFrame, width=42, height=10, yscrollcommand=scrollbar.set)
        entry_note.grid(row=1, column=0, columnspan=3, padx=(10,0), pady=(10,0))

        scrollbar.config(command = entry_note.yview)

        save = tk.Button(self.upFrame, text='Save', width=14, command=lambda: self.save_note(entry_note.get("1.0", 'end')))
        save.grid(row=2, column=0, sticky='n', padx=(10,0), pady=(0, 10))

        clear = tk.Button(self.upFrame, text='Clear', width=14)
        clear.grid(row=2, column=1, sticky='n', pady=(0, 10))

        back = tk.Button(self.upFrame, text='Back', width=14)
        back.grid(row=2, column=2, sticky='n', pady=(0, 10))

        self.upFrame.resizable(width=False, height=False)
        self.upFrame.protocol("WM_DELETE_WINDOW", lambda: self.close_upFrame())
        self.upFrame.mainloop()

    def save_note(self, text):
        rep = text.replace('\n', ';')
        def d(string):
            if string[-1] == ';':
                return d(string[:-1])
            if string[-1] != ';':
                print(string)
        d(rep)


    def close_upFrame(self):
        self.upFrame.destroy()

    def closeframe(self, cont):
        self.top.destroy()
        cont.unfreeze_MM()






def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        emp.close()
        app.destroy()



app = MainAPP()
app.resizable(width=False, height=False)
#app.protocol("WM_DELETE_WINDOW", on_closing)
app.mainloop()
