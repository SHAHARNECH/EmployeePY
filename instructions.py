from employees import add_employee, remove_employee, change_position, read_log, excel_output, excel_import
from utils import valid_id, valid_date, write_log
from attendence import mark_attendance, atten_date, atten_late, atten_month, atten_employee, export_rep


# navigating through 3 main options mark attendance, edit employee log, issuing reports
def instruction():
    to_do = 0
    while to_do != 4:
        to_do = input(
            "mark attendance press 1\n"
            "issue reports press 2\n"
            "edit employee log press 3\n"
            "to quit press q "
        )
        if to_do == '1':
            attendance()
        elif to_do == '2':
            reports()
        elif to_do == '3':
            logs()
        elif to_do == 'q':
            break
        else:
            print("Invalid input")


# navigating through the five editing options of employee log
def logs():
    options = input("To add employee press - 1\n"
                    "Import employees from csv file - press 2\n"
                    "Remove employee press - 3\n"
                    "Change position press - 4\n"
                    "Export employee log to Excel - press 5\n"
                    "Exit - press q")
    if options == '1':
        list_emp = add_employee()
    elif options == '2':
        list_emp = excel_import(input("Enter name of Excel file: "))
    elif options == '3':
        list_emp = remove_employee(input("enter name of employee to remove: "))
    elif options == '4':
        list_emp = change_position(input("enter name of employee to change: "))
    elif options == '5':
        list_emp = excel_output(input("Insert Excel file name: "))
    elif options == 'q':
        return
    else:
        print("wrong input")
        logs()
    write_log(list_emp)


# navigating through the five report options
def reports():
    start_date = False
    end_date = False
    list_emp = read_log()
    print("What report would you like to issue?")
    options = input(
        "Employee attendances - press 1\n"
        "Employee attendances specific dates - press 2\n"
        "Monthly report of all employees - press 3\n"
        "Monthly report of all late workers - press 4\n"
        "Export report to Excel - press 5\n"
        "Exit - press 'q'\n"
    )
    if options == '1':
        atten_employee(list_emp, input("For which employee?"))
    elif options == '2':
        name = input("For which employee?")
        # date not valid loop
        while not start_date:
            start_date = valid_date(input("Start issue on date: "))
            if start_date:
                # date not valid loop
                while not end_date:
                    end_date = valid_date(input("End issue on date: "))
                atten_date(list_emp, name, start_date, end_date)
    elif options == '3':
        month = input("Issue report of month\n"
                      "Jan=1 Feb=2 Mar=3 Apr=4 May=5 Jun=6 Jul=7 Aug= 8 Sep=9 Oct=10 Nov=10 Dec=12: ")
        # month not valid loop
        while int(month) < 1 & int(month) > 12:
            month = input("Invalid month, please insert month number again: ")
        atten_month(list_emp, month)
    elif options == '4':
        month = input("Issue report of month\n"
                      "Jan=1 Feb=2 Mar=3 Apr=4 May=5 Jun=6 Jul=7 Aug= 8 Sep=9 Oct=10 Nov=10 Dec=12: ")
        # date not valid loop
        while int(month) < 1 & int(month) > 12:
            month = input("Invalid month, please insert month number again: ")
        atten_late(list_emp, month)
    elif options == '5':
        export_rep(input("Insert Excel file name: "))
    elif options == 'q':
        return
    else:
        print("wrong input")
        reports()


def attendance():
    # insert employees from log to list
    list_emp = read_log()
    id_num = input("Please enter worker ID: ")
    check = valid_id(id_num)
    # ID not valid loop
    while not check:
        id_num = input("please insert Id number again: ")
        check = valid_id(id_num)
    # going through employee list checking for matches
    for worker in list_emp:
        if worker.employee_id == id_num:
            # marking attendance
            worker.attendance = mark_attendance(worker)
            # updating employee log
            write_log(list_emp)
            print("%s Good Morning!\n" % worker.name)
            return
    option = input("Sorry this Id number isn't in the log.\n"
                   "to try again press enter, to exit press q")
    if option == 'q':
        return
    else:
        attendance()
