import csv
import datetime
import time


def mark_attendance(employee):
    """
        receives employee and adds to his attendance the date from the computer
        :param employee: Employee object
        :return: employee.attendance: self.attendance for Employee object
        """
    # loads date from computer
    today = datetime.datetime.now()
    mark = today.strftime("%d/%m/%Y %H:%M")
    # adds to attendance list in object
    employee.attendance.append(mark)
    return employee.attendance


def atten_employee(list_emp, name):
    """
        receives employees list and name of employee
        writes attendance log by the dates marked in employee attendance section from employee log
        :param list_emp: lists of Employee object
        :param name: str
        :return: void
        """
    with open("attendance_log.txt", "w") as attendance_by_emp:
        attendance_by_emp.seek(0)
        attendance_by_emp.write("Employee Attendance Report:\n")
        for worker in list_emp:
            if worker.name == name:
                attendance_by_emp.write("%s-\n" % worker.name)
                for date in worker.attendance:
                    attendance_by_emp.write("\t" + date + '\n')
                print("Report issued!\n")
                return
    print("%s is not in employee log\n" % name)
    return


def atten_date(list_emp, name, start_rep, end_rep):
    """
        receives employees list and name of employee and dates for report
        writes attendance log by the dates marked in employee attendance section from employee log
        that are in between the dates given
        :param list_emp:  list of Employee objects
        :param name: str
        :param start_rep: str
        :param end_rep: str
        :return: void
        """
    with open("attendance_log.txt", "w") as attendance_by_emp:
        # writes new\re writes attendance_log from the beginning
        attendance_by_emp.seek(0)
        attendance_by_emp.write("Employee Attendance Report %s-%s:\n" % (start_rep, end_rep))
        for worker in list_emp:
            if worker.name == name:
                # found worker name in list
                attendance_by_emp.write("%s-\n" % worker.name)
                for date in worker.attendance:
                    # writing dates in same representation for comparison
                    date_log = time.strptime(date[:10:], "%d/%m/%Y")
                    start_date = time.strptime(start_rep, "%d/%m/%Y")
                    end_date = time.strptime(end_rep, "%d/%m/%Y")
                    # comparing dates
                    if date_log > start_date:
                        if date_log < end_date:
                            attendance_by_emp.write("\t" + date + '\n')
                # finished going through dates
                print("Report issued!\n")
                return
        # worker  not found in list
        print("Sorry, worker not in log")
        return


def atten_month(list_emp, month):
    """
        receives employees list and month to issue report
        writes attendance log by the dates marked in employee attendance section from employee log
        that are on the month given
        :param list_emp:  list of Employee objects
        :param month: str
        """
    count = 0
    with open("attendance_log.txt", "w") as attendance_by_emp:
        # writes new\re writes attendance_log from the beginning
        attendance_by_emp.seek(0)
        attendance_by_emp.write("Monthly Attendance Report:\n")
        # for each worker
        for worker in list_emp:
            # going through all dates marked
            for date in worker.attendance:
                # getting only month
                date_list = date[:10:].split("/")
                if int(date_list[1]) == int(month):
                    count += 1
                    # first date in report for this worker so need to write name first
                    if count == 1:
                        attendance_by_emp.write("%s-\n\t%s\n" % (worker.name, date))
                    # not first date for this worker, write only date
                    else:
                        attendance_by_emp.write("\t%s\n" % date)
            count = 0
    print("Report issued!\n")


def atten_late(list_emp, month):
    """
        receives employees list and month to issue report
        writes attendance log by the dates marked in employees attendance section from employee log
        that are on the month given and marked after 09:30am
        :param list_emp:  list of Employee objects
        :param  month: str
            """
    count = 0
    with open("attendance_log.txt", "w") as attendance_by_emp:
        # writes new\re writes attendance_log from the beginning
        attendance_by_emp.seek(0)
        attendance_by_emp.write("Late Attendance Report:\n")
        for worker in list_emp:
            for date in worker.attendance:
                # dividing date to d\m\y
                date_list = date[:10:].split("/")
                # getting only month
                if int(date_list[1]) == int(month):
                    # getting only time and dividing by :
                    hour_list = date[10::].split(":")
                    # if past 09:30
                    if ((int(hour_list[0]) == 9) & (int(hour_list[1]) > 30)) | (int(hour_list[0]) > 9):
                        count += 1
                        # first late mark for this worker, need to write name
                        if count == 1:
                            attendance_by_emp.write("%s-\n\t%s\n" % (worker.name, date))
                        # not first late mark for this worker write only date
                        else:
                            attendance_by_emp.write("\t%s\n" % date)
            count = 0
    print("Report issued!\n")


def read_rep():
    """
         reads latest report issued to attendance_log and makes list out of it by name of worker and dates
         :return attendance_list
             """
    import re
    name = ''
    date_list = []
    attendance_list = []
    with open("attendance_log.txt", "r+") as attendance_log:
        # reads report from beginning
        attendance_log.seek(0)
        text = attendance_log.readline()
        # reads till the end of file
        while text:
            # skips title
            if not re.search("Report:", text):
                x = re.search(r'[\w]*-', text)
                # found name
                if x:
                    # took name
                    name = text[:x.end() - 1:]
                    date_list = []
                    # next line
                    text = attendance_log.readline()
                # y finds date pattern
                y = re.search(r'[0-9]{2}/[0-9]{2}/[0-9]{4}\s[0-9]{2}:[0-9]{2}', text)
                # while y = more dates
                while y:
                    # took date to list of dates
                    date_list.append(text[y.start():y.end():])
                    # next line
                    text = attendance_log.readline()
                    # date in next line?
                    y = re.search(r'[0-9]{2}/[0-9]{2}/[0-9]{4}\s[0-9]{2}:[0-9]{2}', text)
                # appends to a list that contains name of employee and his list of dates found
                attendance_list.append([name, date_list])
            else:
                # didn't find name- next line
                text = attendance_log.readline()
        return attendance_list


def export_rep(name):
    """
        receives name for file to make
        reads latest report issued to attendance_log makes csv file and copies the report to csv table
        :param name: str
        :return attendance_list
        """
    attendance_list = read_rep()
    try:
        with open(name + '.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            # makes table in Excel by employee and attendance dates
            writer.writerow(["Employee", "Attendance"])
            for worker in attendance_list:
                count = 0
                for date in worker[1]:
                    if not count:
                        # first date needs to add name of worker
                        writer.writerow([worker[0], date])
                        count += 1
                    # write only date
                    else:
                        writer.writerow(['', date])
            print("csv file made")
            return attendance_list
    except PermissionError:
        print("file is opened, please close and try again")
    return attendance_list
