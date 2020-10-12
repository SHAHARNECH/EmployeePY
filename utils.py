import datetime
import re


def write_log(list_workers):
    """
    updates employee log. receives updated list of employees and writes over employee_file
    :type list_workers: object
    """
    list_emp = list_workers
    with open("employee_file.txt", "w") as employee_stock:
        # go to the beginning of file
        employee_stock.seek(0)
        # writes each employee as represented in Class Employee
        for worker in list_emp:
            employee_stock.write(repr(worker) + "\n")


def valid_name(name):
    """
        checks if name inserted is valid for log- "name"+number for employees with same name
        returns true or false
        :type name: str
        """
    x = re.match(r'^[a-zA-Z]*[\w]$', name)
    if not x:
        print("name not valid")
        return False
    else:
        return True


def valid_id(id_num):
    """
        checks if Id number inserted is valid for log- 7-9 digits
        returns true or false
        :type id_num: str
        """
    x = re.search(r'[\D]', id_num)
    if x:
        print("invalid id number")
        return False
    else:
        if len(id_num) < 7 or len(id_num) > 9:
            print("invalid id number, id number is 7-9 digits")
            return False
        else:
            return True


def valid_phone(phone_num):
    """
        checks if phone number inserted is valid for log-
        10 digits for mobile
        9 for either mobile that starts with zero or 9 for landline
        8 for landline that starts with zero
        valid landline - 02, 03, 05, 08, 09
        valid moblie  - 05
        returns true or false
        :type phone_num: str
        """
    x = re.search(r'[\D]', phone_num)
    if x:
        print("invalid phone number")
        return False
    else:
        if len(phone_num) == 10:
            x = re.search(r'^05', phone_num)
            if not x:
                print("invalid phone number")
                return False
            else:
                return True
        elif len(phone_num) == 9:
            x = re.search(r'^5|(^0?(2|3|5|8|9))', phone_num)
            if not x:
                print("invalid phone number")
                return False
            else:
                return True
        elif len(phone_num) == 8:
            x = re.search(r'^2|^3|^4|^8|^9', phone_num)
            if not x:
                print("invalid phone number")
                return False
            else:
                return True
        else:
            print("invalid phone number, needs 9-10 digits")
            return False


def calculate_age(birthdate):
    """
        calculates age from birthdate given
        returns age
        :type birthdate: str
        """
    today = datetime.date.today()
    # changes todays date to 'dd/mm/YY'
    curr_date = today.strftime("%d/%m/%Y").split('/')
    birth = birthdate.split('/')
    # if birth month has already passed
    if int(curr_date[1]) > int(birth[1]):
        age = int(curr_date[2]) - int(birth[2])
    else:
        # if birth day is today or has passed on birth month
        if (int(curr_date[0]) >= int(birth[0])) & (int(curr_date[1]) == int(birth[1])):
            age = int(curr_date[2]) - int(birth[2])
        else:
            # birthday hasn't passed yet
            age = int(curr_date[2]) - int(birth[2]) - 1
    return age


def valid_position(position):
    """
        checks if position is valid
        returns true or false
        :type position: str
        """
    # if there are non characters word is not valid
    x = re.search(r'[\W]', position)
    if x:
        print("invalid position")
        return False
    else:
        return True


def valid_date(date):
    """
        checks if date given is valid
        returns valid date or 0
        :type date: str
        """
    date_list = date.split("/")
    today = datetime.date.today()
    try:
        # if not valid raises validError
        datetime.datetime(year=int(date_list[2]), month=int(date_list[1]), day=int(date_list[0]))
        # checks if year is not in future
        if date_list[2] <= str(today.year):
            return date
        else:
            print("Invalid date")
            return 0
    except ValueError:
        print("Invalid date")
        return 0


def check_import(row):
    """
        checks if employee details from imported file are valid
        by row: name, id number, age, phone number, position
        returns list of valid employee details or 0
        :type row: str
        """
    name_chk = False
    id_chk = False
    age_chk = False
    phone_chk = False
    pos_chk = False

    # row[0] in excel: name
    check = valid_name(row[0])
    if check:
        name = row[0]
        name_chk = True

    # row[1] in excel: id number
    check = valid_id(row[1])
    if check:
        id_num = row[1]
        id_chk = True

    # row[2] in excel: age
    if (int(row[2]) > 0) & (int(row[2]) < 120):
        age = row[2]
        age_chk = True

    # row[3] in excel: phone number
    check = valid_phone(row[3])
    if check:
        phone_number = row[3]
        phone_chk = True

    # row[4] in excel: position
    check = valid_position(row[4])
    if check:
        position = row[4]
        pos_chk = True

    # if all are valid they are changed to true
    if name_chk & id_chk & age_chk & phone_chk & pos_chk:
        # makes list from detail
        data_list = [name, id_num, age, phone_number, position]
        return data_list
    else:
        return 0
