import contextlib
from seleniumbase import SB
from course import Course

CHECK_EVERY = 15 # seconds
STUDENT_ID = "1191319"
PASSWORD = "123127Ob"

available_marks_courses = []


def login():
    sb.open("https://ritaj.birzeit.edu")
    sb.wait(7)

    with contextlib.suppress(Exception):
        human_checkbox_selector = "#cf-stage > div.ctp-checkbox-container > label > input[type=checkbox]"
        if human_checkbox := sb.find_element(human_checkbox_selector):
            sb.click(human_checkbox)
        sb.wait(5)

    studentID_selector = "#register-login > form > table > tbody > tr:nth-child(1) > td.form-widget > input[type=text]"
    sb.update_text(studentID_selector, STUDENT_ID)
    sb.wait(0.5)

    password_selector = "#register-login > form > table > tbody > tr:nth-child(2) > td.form-widget > input[type=password]"
    sb.update_text(password_selector, PASSWORD)
    sb.wait(0.5)

    loginButton_selector = "#register-login > form > table > tbody > tr:nth-child(3) > td > input[type=submit]"
    sb.click(loginButton_selector)
    sb.wait(3)

def check_if_login_needed():
    with contextlib.suppress(Exception):
        loginButton_selector = "#register-login > form > table > tbody > tr:nth-child(3) > td > input[type=submit]"
        sb.find_element(loginButton_selector)
        login()

def is_link_exists(link):
    return any(course.url == link for course in available_marks_courses)

def get_available_marks_links():
    # sb.open("https://ritaj.birzeit.edu/student/marks/term-summary")
    sb.open("https://ritaj.birzeit.edu/student/marks/term-summary?term=1211") #TODO: remove this line
    sb.wait(3)

    cells_selector = "#slave > table > tbody > tr > td:nth-child(5) > a"
    cells = sb.find_elements(cells_selector)
    for cell in cells:
        mark_link = cell.get_attribute("href")
        if not is_link_exists(mark_link):
            available_marks_courses.append(Course(url=mark_link))
    
    sb.wait(2)

def get_course_mark(course):
    sb.open(course.url)
    
    course_symbol_selector = "#slave > table > tbody > tr:nth-child(1) > td"
    course_symbol = sb.get_text(course_symbol_selector)
    course.symbol = course_symbol

    course_name_selector = "#slave > table > tbody > tr:nth-child(2) > td"
    course_name = sb.get_text(course_name_selector)
    course.name = course_name

    course_mark_selector = "#slave > table > tbody > tr:nth-child(4) > td"
    course_mark = sb.get_text(course_mark_selector)
    course.mark = course_mark

    try:
        course_average_selector = "#slave > table > tbody > tr:nth-child(5) > td"
        course_average = sb.get_text(course_average_selector)
        course.average = course_average
    
    except Exception:
        pass


def send_telegram_message(course):
    print(course)

def send_all_available_marks():
    print("Sending all available marks") #TODO: remove this line
    for course in available_marks_courses:
        send_telegram_message(course)

with SB(uc=True) as sb:
    login()

    while True:
        check_if_login_needed()
        get_available_marks_links()

        for course in available_marks_courses:
            try: 
                if not course.checked:
                    get_course_mark(course)
                    send_telegram_message(course)
                    course.checked = True

                    sb.wait(3)
            
            except Exception as e:
                # if the user login from his browser, the session will be expired, this try except will handle this case
                print(e)
                sb.wait(3)
                break

        sb.wait(CHECK_EVERY)
