from tkinter import *
import os

def read_tasks_from_file():
    with open('tasks.txt', 'r') as tasks_file:
        content = tasks_file.readlines()

    for x in content:
        x = x.strip()
        tasks_dict[x.split(",")[0]] = x.split(",")[1]
    return tasks_dict

def complete():
    tasks_dict[tasks.get(ACTIVE)] = 'True'
    tasks.itemconfig(list(tasks_dict).index(tasks.get(ACTIVE)), foreground='grey')
    tasks.selection_clear(0, END)

def incomplete():
    tasks_dict[tasks.get(ACTIVE)] = 'False'
    tasks.itemconfig(list(tasks_dict).index(tasks.get(ACTIVE)), foreground='black')
    tasks.selection_clear(0, END)

def add_item():
    new_task = new_item_entry.get()
    
    check = True
    for task in tasks_dict:
        if(new_task.lower().strip() == task.lower().strip()):
            check = False
    if(new_task != '' and check):
        tasks_dict[new_task] = 'False'
        tasks.insert(END, new_task)
        new_item_entry.delete(0, END)
        status.config(text="Task Added")
    else:
        if(new_task == ''):
            status.config(text="Please enter a task")
        else:
            status.config(text="Task already present")

def delete_item():
    del tasks_dict[tasks.get(ACTIVE)]
    tasks.delete(ACTIVE)
    status.config(text="Task Deleted")

def on_closing():
    with open('tasks.txt', 'w') as final:
        for element in tasks_dict:
            final.write(element+","+tasks_dict[element]+"\n")
    root.destroy()


if __name__ == '__main__':
    tasks_dict = {}

    if not (os.path.exists('tasks.txt')):
        #Creating the txt file
        file = open('tasks.txt', 'x')
        file.close()
    
    tasks_dict = read_tasks_from_file()

    # Initializing the python to do list GUI window
    root = Tk()
    root.title('To-Do')
    root.geometry('300x460')
    root.resizable(0, 0)
    root.config(bg="PaleVioletRed")

    # Heading Label
    Label(root, text='Python To Do List', bg='PaleVioletRed', font=("Comic Sans MS", 15), wraplength=300).place(x=35, y=0)

    # Listbox with all the tasks with a Scrollbar
    tasks = Listbox(root, selectbackground='Gold', bg='Silver', font=('Helvetica', 12), height=12, width=25)

    scroller = Scrollbar(root, orient=VERTICAL, command=tasks.yview)
    scroller.place(x=260, y=50, height=232)

    tasks.config(yscrollcommand=scroller.set)

    tasks.place(x=35, y=50)

    count = 0
    #Populate the ListBox
    for task in tasks_dict:
        tasks.insert(END, task)
        if(tasks_dict[task] == 'True'):
            tasks.itemconfig(count, foreground='grey')
        count += 1

    # Creating the Entry widget where the user can enter a new item
    new_item_entry = Entry(root, width=37)
    new_item_entry.place(x=35, y=310)

    # Creating the Buttons
    Button(root, text='Add Item', bg='Azure', width=10, font=('Helvetica', 12),
                     command=add_item).place(x=45, y=350)

    Button(root, text='Delete Item', bg='Azure', width=10, font=('Helvetica', 12),
                     command=delete_item).place(x=150, y=350)

    Button(root, text='Complete', bg='Azure', width=10, font=('Helvetica', 12),
                     command=complete).place(x=45, y=390)

    Button(root, text='Incomplete', bg='Azure', width=10, font=('Helvetica', 12),
                     command=incomplete).place(x=150, y=390)

    status = Label(root, text='', fg='white', bg='PaleVioletRed', font=("Comic Sans MS", 12), wraplength=300)
    status.place(x=65, y=430)

    # Finalizing the window
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
