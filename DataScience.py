from tkinter import *
from tkinter import filedialog
from tkinter import scrolledtext
from tkinter import messagebox
import pandas as pd
from pathlib import Path 







def init_df():
    global df
    global df2
    global query
    global list_columns
    global list_rows
    global ID
    global view_column_flag
    global view_row_flag 
    global query_column_flag 

    global view_row_key
    global view_row_operator

    global query_column_column
    global query_column_key
    global query_column_operator

    ID = ''

    pd.set_option('display.width', 600)
    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', None)
    pd.set_option('max_colwidth', 400)

    view_column_flag = False
    view_row_flag = False
    query_column_flag = False

    view_row_key = []
    view_row_operator = []

    query_column_column = []
    query_column_key = []
    query_column_operator = []


    file = open(query, 'r')
    lines = file.readlines()

    list_columns = []
    list_rows = []
    list_columns = lines[0].split(',')

    for i in range (1, len(lines)):
        list_rows += lines[i][0]

    last_index = len(list_columns) - 1
    list_columns[last_index] = list_columns[last_index][0:len(list_columns[last_index]) - 1]

    ID = list_columns[0]
    list_columns = list_columns[1:]
    
    df = pd.read_csv(csv_file, delimiter=',')
    df.set_index(ID, inplace=True)
    df2 = df.copy()

    print("ID: " + str(ID))
    print("Columns: [" + str(df.shape[1]) + "] " + str(list_columns))
    print("Rows: [" + str(df.shape[0]) + "]")

    

    
def choose_file():
    global query
    global csv_file 
    global file_name

    exit_flag = False

    while exit_flag == False:    
        query = filedialog.askopenfilename()

        if not query:
            exit_flag = True
            exit(0)
        if query[len(query) - 3: len(query)] != "csv":
            messagebox.showerror("File Error", "Please open a .csv file!")
        else:
            exit_flag = True
    
    file_name = Path(query).stem
    csv_file = open(query)
    print("Opening: " + query)
    init_df()
    file_view()

#-----------------------------------------------------------------------------------------------------------------------
    #QUERY

def query_column(key, operator, column):
    global df2
    global df

    global query_column_flag
    global query_column_key
    global query_column_operator
    global query_column_column

    global query_column_flag

    global view_row_flag
    global view_row_key
    if type(key) != list and not (key in query_column_key):
        try:
            if operator == '<' or operator == '>':
                key = int(key)
        except:
            messagebox.showerror("Input Error", "Strings can only be queried using '='")
            return 0
        query_column_key.append(key) 
        query_column_operator.append(operator) 
        query_column_column.append(column)
        query_column_flag = True


    df2 = df.copy()

    for i in range(0, len(query_column_key)):
        
        if query_column_operator[i] == '=':
            df2 = df2.query(str(f'`{query_column_column[i]}`' + ' == ' + f'"{str(query_column_key[i])}"'))
        if query_column_operator[i] == '<':
            df2 = df2.query(str(f'`{query_column_column[i]}`' + ' < ' + str(query_column_key[i])))
        if query_column_operator[i] == '>':
            df2 = df2.query(str(f'`{query_column_column[i]}`' + ' > ' + str(query_column_key[i])))
    


def view_column(key_index):
    global view_column_flag
    global view_column_key 
    global df2

    if view_column_flag == True:
        reset_columns()

    
    view_column_key = key_index
    view_column_flag = True

    df2 = df2.loc[:, [key_index]]
    print("Viewing Column: " + key_index)
        
    
def view_row(key_index, operator_key):
    global df2
    global ID

    global view_row_flag
    global view_row_key
    global view_row_operator

    if type(key_index) != list:
        try:
            key_index = int(key_index)

        except:
            messagebox.showerror("Input Error", "Please enter an integer.")
            return 0
        
        if operator_key != ">" and operator_key != "<" and operator_key != "=":
            messagebox.showerror("Input Error", "Please select an operator.")
            return 0
        
        if not (key_index in view_row_key): #element doesn't exist in list 
            view_row_key.append(key_index)
            view_row_operator.append(operator_key)


    for i in range(0, len(view_row_key)):
        key = view_row_key[i]
        print("KEY: "+ str(key))
        if view_row_operator[i] == '=':
            df2 = df2.query(str(ID) + " == " + str(view_row_key[i]))
        elif view_row_operator[i] == '<':
            df2 = df2.query(str(ID) + " < " + str(view_row_key[i]))
        elif view_row_operator[i] == '>':
            df2 = df2.query(str(ID) + " > " + str(view_row_key[i]))

    view_row_flag = True

    print("Viewing Row: " + str(key_index))
    

#-----------------------------------------------------------------------------------------------------------------------
    #HELPER FUNCTIONS

def reset_columns():
    global df2

    global view_row_flag
    global view_row_key
    global view_row_operator


    global query_column_column
    global query_column_flag
    global query_column_key
    global query_column_operator

    global view_column_key
    global view_column_flag


    df2 = df.copy()
    if query_column_flag == True:
        query_column(query_column_key, query_column_operator, query_column_column)
    view_column_flag = False
    view_column_key = ''


def reset_rows():
    global df2

    global view_row_flag
    global view_row_key
    global view_row_operator


    global query_column_column
    global query_column_flag
    global query_column_key
    global query_column_operator

    global view_column_key
    global view_column_flag

    view_row_flag == False
    view_row_key.clear()
    view_row_operator.clear()
    
    df2 = df.copy()
    if query_column_flag == True:
        query_column(query_column_key, query_column_operator, query_column_column)
    if view_column_flag == True:
        view_column(view_column_key)
        



def execute_queries():
    global df2

    global view_row_flag
    global view_row_key
    global view_row_operator


    global query_column_column
    global query_column_flag
    global query_column_key
    global query_column_operator

    global view_column_key
    global view_column_flag

    df2 = df.copy()

    try:
        if query_column_flag == True:
            print(query_column_key," ",query_column_operator," ",query_column_column)
            query_column(query_column_key, query_column_operator, query_column_column)
        if view_column_flag == True:
            view_column(view_column_key)
        if view_row_flag == True:
            view_row(view_row_key, view_row_operator)

        file_view()
        
    except Exception as e:
        print(e)
        messagebox.showerror("Data Error", "Error processing data. Please reset and try again.")

def reset():
    global df2
    global view_column_key
    global view_column_flag

    global query_column_operator
    global query_column_column
    global query_column_key
    global query_column_flag

    global view_row_operator
    global view_row_key
    global view_row_flag 

    view_row_flag = False
    query_column_flag = False
    view_column_flag = False

    view_row_key = []
    view_row_operator = []

    query_column_operator = []
    query_column_column = []
    query_column_key = []

    view_column_key = ''
    
    df2 = df.copy()




#-----------------------------------------------------------------------------------------------------------------------
    #TKINTER DISPLAY

def file_view():
    global df
    global csv_file
    global file_name
    global view_row_key
    global query_column_key    
    
    win = Tk()
    win.geometry('1280x720')
    win.resizable(False,False)
    win.title('CSV Viewer')

    canvas = Canvas(win, height=720, width=1280 ,bg='black')
    canvas.pack()

    title = Label(win, text="Opened File", bg='black', fg='white')
    title.config(font='Verdana 16')
    canvas.create_window(640, 30, anchor='n', window=title)

    title_2 = Label(win, text=str(file_name), bg='black', fg='light yellow')
    title_2.config(font='Verdana 16')
    canvas.create_window(640, 80, anchor='n', window=title_2)
    
    file_contents = scrolledtext.ScrolledText(win, wrap=WORD)
    file_contents.config(bg='black', fg='white')
    if df2.empty:
        file_contents.insert('1.0', "No data to display. Time to reset!")
        file_contents.config(font='Verdana 16')
        canvas.create_window(640, 360, height=420, width = 1280, anchor='center', window=file_contents)
    else:
        file_contents.insert('1.0', df2.head())
        canvas.create_window(640, 360, height=420, width = 1280, anchor='center', window=file_contents)

    reset_btn = Button(win, text='Reset', command=lambda:[win.destroy(), reset(), file_view()])
    reset_btn.config(font='Verdana 10', fg='black', bg='light blue')
    canvas.create_window(640, 670, anchor='n', window=reset_btn)

    change_file_btn = Button(win, text='Change File', command=lambda:[win.destroy(), choose_file()])
    change_file_btn.config(font='Verdana 14', fg='black', bg='light yellow')
    canvas.create_window(640, 610, anchor='n', window=change_file_btn)

#-----------------------------------------------------------------------------------------------------------------------
    #VIEW ROW
    
    row_select_var = StringVar()
    less_than_switch = Radiobutton(win, text="<", variable = row_select_var, value='<', indicatoron=False)
    less_than_switch.config(font='Verdana 8')
    canvas.create_window(320, 640, anchor='n', window=less_than_switch)

    greater_than_switch = Radiobutton(win, text=">", variable = row_select_var, value='>', indicatoron=False)
    greater_than_switch.config(font='Verdana 8')
    canvas.create_window(360, 640, anchor='n', window=greater_than_switch)

    equal_to_switch = Radiobutton(win, text="=", variable = row_select_var, value='=', indicatoron=False)
    equal_to_switch.config(font='Verdana 8')
    canvas.create_window(340, 640, anchor='n', window=equal_to_switch)

    number_entry = StringVar()
    row_entry = Entry(textvariable=number_entry)
    canvas.create_window(340, 610, anchor='n', width=120, window=row_entry)

    view_row_btn = Button(win, text='Select Row', bg='light yellow', command=lambda:[win.destroy(), view_row(number_entry.get(), row_select_var.get()), execute_queries()])
    view_row_btn.config(font='Verdana 8')
    canvas.create_window(345, 680, anchor='nw', window=view_row_btn)


    reset_row_btn = Button(win, text='Reset Rows', bg='light yellow', command=lambda:[win.destroy(), reset_rows(), file_view()])
    view_row_btn.config(font='Verdana 8')
    canvas.create_window(335, 680, anchor='ne', window=reset_row_btn)

#-----------------------------------------------------------------------------------------------------------------------
    #QUERY COLUMN
    
    

    select_var = StringVar()
    less_than_switch = Radiobutton(win, text="<", variable = select_var, value='<', indicatoron=False)
    less_than_switch.config(font='Verdana 8')
    canvas.create_window(880, 620, anchor='ne', window=less_than_switch)

    greater_than_switch = Radiobutton(win, text=">", variable = select_var, value='>', indicatoron=False)
    greater_than_switch.config(font='Verdana 8')
    canvas.create_window(900, 620, anchor='ne', window=greater_than_switch)

    equal_to_switch = Radiobutton(win, text="=", variable = select_var, value='=', indicatoron=False)
    equal_to_switch.config(font='Verdana 8')
    canvas.create_window(900, 680, anchor='ne', window=equal_to_switch)

    query_entry = StringVar()
    query_box = Entry(win, textvariable=query_entry)
    canvas.create_window(1040, 600, anchor='ne', width=80, height= 20, window = query_box)

    query_column_var = StringVar(win)
    list_names = list_columns

    list_sel = OptionMenu(win, query_column_var, *list_names)
    canvas.create_window(1040, 640, anchor = 'ne', width= 80, height=30, window=list_sel)

    #MAKE PASS TO SEE IF THEY ENTER A NUMBER
    query_column_btn = Button(win,text='Query Column', bg='light yellow', command=lambda:[win.destroy(), query_column(query_entry.get(), select_var.get(),query_column_var.get()), execute_queries()])
    query_column_btn.config(font='Verdana 8')
    canvas.create_window(1040, 680, anchor='ne', window=query_column_btn)

#----------------------------------------------------------------------------------------------------------------------- 
    #COLUMN SELECT
    column_select_var = StringVar(win)
    list_names = list_columns

    list_sel = OptionMenu(win, column_select_var, *list_names)
    canvas.create_window(1180, 600, anchor = 'n', width= 80, height=30, window=list_sel)

    view_column_btn = Button(win,text='Column Select', bg='light yellow', command=lambda:[win.destroy() , view_column(column_select_var.get()), execute_queries()])
    view_column_btn.config(font='Verdana 8')
    canvas.create_window(1180, 650, anchor='n', window=view_column_btn)

    reset_column_btn = Button(win,text='Reset Columns', bg='light yellow', command=lambda:[win.destroy(), reset_columns(), execute_queries()])
    reset_column_btn.config(font='Verdana 8')
    canvas.create_window(1180, 680, anchor='n', window=reset_column_btn)


#----------------------------------------------------------------------------------------------------------------------- 
    #LABELS
    numbers_label = Label(text="Numbers", font='Arial 8', fg='light green', bg='black')
    canvas.create_window(900, 600, anchor='ne', window = numbers_label)


    word_label = Label(text="Words", font='Arial 8', fg='light green', bg='black')
    canvas.create_window(900, 660, anchor='ne', window = word_label)

    query_label = Label(text="Query Column", font='Arial 10', fg='light blue', bg='black')
    canvas.create_window(940, 572, anchor='n', window = query_label)

    view_row_label = Label(text="View Row", font='Arial 10', fg='light blue', bg='black')
    canvas.create_window(340, 572, anchor='n', window = view_row_label)

    view_column_label = Label(text="View Column", font='Arial 10', fg='light blue', bg='black')
    canvas.create_window(1180, 572, anchor='n', window = view_column_label)

    if view_row_flag == True and len(view_row_key) > 1:
        selected_row_label = Label(text="Selected Row: (multiple selections)", fg='white', bg='black')
    elif view_row_flag == True:
        selected_row_label = Label(text="Selected Row: " + str(view_row_operator) + str(view_row_key), fg='white', bg='black')
    else:
        selected_row_label = Label(text="Selected Row: None", fg='white', bg='black')
    canvas.create_window(100, 592, anchor='n', window = selected_row_label)

    if query_column_flag == True and len(query_column_key) > 1:
        selected_query_label = Label(text="Selected Query: (multiple queries)", fg='white', bg='black')
    elif query_column_flag == True:
        selected_query_label = Label(text="Selected Query (" + str(query_column_column) + "): " + str(query_column_operator) + str(query_column_key), fg='white', bg='black')
    else:
        selected_query_label = Label(text="Selected Query: None", fg='white', bg='black')
    canvas.create_window(100, 612, anchor='n', window = selected_query_label)

    if view_column_flag == True:
        view_column_label = Label(text="Selected Query: " + str(view_column_key), fg='white', bg='black')
    else:
        view_column_label = Label(text="Selected Column: None", fg='white', bg='black')
    canvas.create_window(100, 632, anchor='n', window = view_column_label)

    column_count_label = Label(text = ("Columns: [" + str(df.shape[1]) + "]"), fg='white', bg='black')
    canvas.create_window(100, 662, anchor='n', window=column_count_label)

    row_count_label = Label(text = ("Rows: [" + str(df.shape[0]) + "]"), fg='white', bg='black')
    canvas.create_window(100, 682, anchor='n', window=row_count_label)


#----------------------------------------------------------------------------------------------------------------------- 
    #FORMAT
    canvas.create_line(1080, 500, 1080, 720, fill='white', width=2)
    canvas.create_line(800, 500, 800, 720, fill='white', width=2)
    canvas.create_line(200, 500, 200, 720, fill='white', width=2)
    canvas.create_line(480, 500, 480, 720, fill='white', width=2)
    canvas.create_line(540, 70, 740, 70, fill='white', width=1)
    win.mainloop()


choose_file()