import csv
from utils import valid_phone, valid_position, valid_id, valid_name, valid_date, check_import, calculate_age


class Employee:
    def __init__(self, name, employee_id, age, phone_num, position, attendance):
        """
            Class Employee- creates worker with name, id number, age, phone number, position and attendance dates
        :rtype: object
        """
        self.name = name
        self.employee_id = employee_id
        self.phone_num = phone_num
        self.age = age
        self.position = position
        self.attendance = attendance

    def __repr__(self):
        """
            Overrides method in object to represent object employee as we want in log
                """
        return "%s- \n\t id: %s\n\t age: %s\n\t phone: %s\n\t position: %s\n\t attendance: %s\n" % \
               (self.name, self.employee_id, self.age, self.phone_num, self.position, self.attendance)


def read_log():
    """
         reads through employee log and inserts details for each employee to a list
         returns list of employees
             """
    import re
    count_name = 0
    count_att = 0
    idd = False
    phone = False
    ag = False
    pos = False
    emp_attendance = []
    list_emp = []
    dates = []
    with open("employee_file.txt", "r+") as employee_stock:
        employee_stock.seek(0)
        # starts at the beginning of file and reads line by line
        text = employee_stock.readline()
        # loop till the end of file
        while text:
            # search name
            x = re.search(r'[\w]*-', text)
            if x:
                emp_name = text[x.start():x.end() - 1:]
                # found name
                count_name += 1
            # search id number
            x = re.search(r'id:', text)
            if x:
                space = re.search(r'[\s]', text[x.end() + 1::])
                emp_idd = text[x.end() + 1:x.end() + space.start() + 1:]
                idd = True
            # search phone number
            x = re.search(r'phone:', text)
            if x:
                space = re.search(r'[\s]', text[x.end() + 1::])
                emp_phone_num = text[x.end() + 1:x.end() + space.start() + 1:]
                phone = True
            # search age
            x = re.search(r'age:', text)
            if x:
                space = re.search(r'[\s]', text[x.end() + 1::])
                emp_age = text[x.end() + 1:x.end() + space.start() + 1:]
                ag = True
            # search position
            x = re.search(r'position:', text)
            if x:
                space = re.search(r'[\s]', text[x.end() + 1::])
                emp_position = text[x.end() + 1:x.end() + space.start() + 1:]
                pos = True
            # search attendance
            x = re.search(r'attendance:', text)
            if x:
                count_att += 1
                is_next = True
                # loop through dates in attendance
                while is_next:
                    day = re.search(r'\d{2}/\d{2}/\d{4}', text)
                    time = re.search(r'\d{2}:\d{2}', text)
                    if day:
                        # appends date and time to date list
                        dates.append(day.group() + " " + time.group())
                    is_next = re.search(r',', text)
                    # if comma found there are more dates
                    if is_next:
                        # cut text to after comma
                        text = text[is_next.start() + 1::]
                        # there is a comma but line ended- continues to next line
                        if not text:
                            text = employee_stock.readline()
                # saves dates list to employee details
                emp_attendance = dates
            # if all details were found
            if idd & phone & ag & pos & count_name == 1 & count_att == 1:
                new_employee = Employee(emp_name, emp_idd, emp_age, emp_phone_num, emp_position, emp_attendance)
                # append employee object to list of employees
                list_emp.append(new_employee)
                # reset all
                count_name = 0
                count_att = 0
                idd = False
                phone = False
                ag = False
                pos = False
                dates = []
            # get next line for next worker
            text = employee_stock.readline()
    # return list of employee objects
    return list_emp


def add_employee():
    """
        gets detail from user checks if valid and inserts it to employee log
        returns list of updated employees
        """
    # loads updated employee log
    list_emp = read_log()
    again = True
    # loop to add employees until 'q'
    while again:
        add_emp = input("to insert a new employee enter 'y', to quit enter 'q': ")
        if add_emp == 'y':
            birthdate = False
            emp_name = input("please insert employee name: ")
            check = valid_name(emp_name)
            # name not valid
            while not check:
                emp_name = input("invalid name, please insert name again: ")
                check = valid_name(emp_name)
            emp_idd = input("please insert employee's Id number: ")
            check = valid_id(emp_idd)
            # id number not valid
            while not check:
                emp_idd = input("please insert Id number again: ")
                check = valid_id(emp_idd)
            # list not empty- check if employees already in list
            if list_emp:
                for worker in list_emp:
                    # if name already in log
                    if worker.name == emp_name:
                        print("The name %s is already taken" % emp_name)
                        return add_employee()
                        break
                    # if id number already in log
                    if worker.employee_id == emp_idd:  # worker id on the list
                        print("this id number is already in the log by the name %s" % worker.name)
                        return add_employee()
                # checks valid phone
                emp_phone_num = input("please insert employees phone num: ")
                check = valid_phone(emp_phone_num)
                while not check:
                    emp_phone_num = input("please insert phone number again: ")
                    check = valid_phone(emp_phone_num)
                # checks valid birthday
                while not birthdate:
                    birthdate = valid_date(input("please insert employees birthdate: (mm/dd/yyyy) "))
                emp_age = calculate_age(birthdate)
                # check valid phone
                emp_position = input("please insert employees position: ")
                check = valid_position(emp_position)
                while not check:
                    emp_position = input("please insert position again: ")
                    check = valid_position(emp_position)
            # empty log
            else:
                # checks valid details
                emp_phone_num = input("please insert employees phone num: ")
                check = valid_phone(emp_phone_num)
                while not check:
                    emp_phone_num = input("please insert phone number again: ")
                    check = valid_phone(emp_phone_num)
                while not birthdate:
                    birthdate = valid_date(input("please insert employees birthdate: (mm/dd/yyyy) "))
                emp_age = calculate_age(birthdate)
                emp_position = input("please insert employees position: ")
                check = valid_position(emp_position)
                while not check:
                    emp_position = input("please insert position again: ")
                    check = valid_position(emp_position)
            # makes new employee with all the valid details and appends to list of employee objects
            employee = Employee(emp_name, emp_idd, emp_age, emp_phone_num, emp_position, [])
            list_emp.append(employee)
        elif add_emp == 'q':
            again = False
            print("Finished adding, back to main menu")
        else:
            print(' Oops! not valid input...')
    # returns updated list with added employee object
    return list_emp


def remove_employee(name):
    """
    receives name of worker and removes him from the employee log
    :param name: str
    :return: list_emp: list of updated employees
    """
    # loads updated employee log
    list_emp = read_log()
    for x in list_emp:
        if x.name == name:
            # found worker in list and removes
            list_emp.remove(x)
            print("%s has been removed" % name)
            return list_emp
    # worker not in list
    print("no worker by the name %s" % name)
    return list_emp


def change_position(name):
    """
    receives name of worker and changes his position detail in list
    :param name: str
    :return: list_emp: list of updated employees
    """
    # loads updated employee log
    list_emp = read_log()
    check = False
    for x in list_emp:
        if x.name == name:
            while not check:
                position = input("Change to which position?")
                check = valid_position(position)
            x.position = position
            print("position for %s changed" % name)
            return list_emp
    print("no worker by the name %s" % name)
    return list_emp


def excel_output(name):
    """
        receives name of file to make and outputs employee lof to excel
        :param name: str
        :return: list_emp: list of employees
        """
    # loads updated employee log
    list_emp = read_log()
    try:
        with open(name + '.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            # makes table in Excel by employee details
            writer.writerow(["Name", "ID number", "Age", "Phone number", "Position"])
            for worker in list_emp:
                writer.writerow([worker.name, worker.employee_id, worker.age, worker.phone_num, worker.position])
            print("csv file made")
            return list_emp
    except PermissionError:
        print("file is opened, please close and try again")
    return list_emp


def excel_import(import_log):
    """
        receives name of file to open and import from into employee log
        :param import_log: str
        :return: list_emp: list of employees
        """
    # loads updated employee log
    list_emp = read_log()
    try:
        with open(import_log + '.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                # skips title row
                if not row[0] == "Name":
                    if list_emp:
                        # checks if worker is already in log
                        for worker in list_emp:
                            new = True
                            if worker.name == row[0]:
                                print("Worker %s already in log" % worker.name)
                                new = False
                                break
                            elif worker.employee_id == row[1]:
                                print("In file worker %s has same Id as %s in log, worker skipped" % (
                                    row[0], worker.name))
                                new = False
                                break
                        # worker not in list
                        if new:
                            # checks file for valid details
                            x = check_import(row)
                            if x:
                                # creates employee objects with details and appends to list
                                employee = Employee(x[0], x[1], x[2], x[3], x[4], [])
                                list_emp.append(employee)
                            else:
                                print("Error! worker skipped")
                    else:
                        # list empty
                        x = check_import(row)
                        if x:
                            # creates employee objects with details and appends to list
                            employee = Employee(x[0], x[1], x[2], x[3], x[4], [])
                            list_emp.append(employee)
                        else:
                            print("Error! worker skipped")
        return list_emp
    except FileNotFoundError:
        print("No existing file by the name %s.csv\n" % import_log)
        return list_emp
