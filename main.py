# import asyncio
import contextlib
import sys
from seleniumbase import SB
from telegram import Bot

from course import Course
from utils.config import TELEGRAM_API_TOKEN
import telegramHandler_V2



CHECK_EVERY = 15 # seconds
available_marks_courses = []


def run_bot(chatID, user_id, password):
    with SB(uc=True) as sb:
        login(chatID, sb, user_id, password)

        while True:
            check_if_login_needed(chatID, sb, user_id, password)
            get_available_marks_links(sb)

            for course in available_marks_courses:
                try:
                    if not course.checked:
                        get_course_mark(sb, course)
                        send_telegram_message(chatID, str(course))
                        course.checked = True

                        sb.wait(3)

                except Exception as e:
                    # if the user login from his browser, the session will be expired, this try except will handle this case
                    print(e)
                    sb.wait(3)
                    break

            sb.wait(CHECK_EVERY)




def login(chatID, sb, user_id, password):
    sb.open("https://ritaj.birzeit.edu")
    sb.wait(7)


    list_of_checkboxes_selectors = ["# cf-stage > div.ctp-checkbox-container > label > input[type=checkbox]", 
                                    "# challenge-stage > div > input", "# spinner-icon > svg",
                                    "# cf-stage > div.ctp-checkbox-container > label",
                                    "#content > table > tbody"]

    for selector in list_of_checkboxes_selectors:
        with contextlib.suppress(Exception):
            checkbox = sb.find_element(selector)
            sb.click(checkbox)
            sb.wait(5)

    studentID_selector = "#register-login > form > table > tbody > tr:nth-child(1) > td.form-widget > input[type=text]"
    sb.update_text(studentID_selector, user_id)
    sb.wait(0.5)

    password_selector = "#register-login > form > table > tbody > tr:nth-child(2) > td.form-widget > input[type=password]"
    sb.update_text(password_selector, password)
    sb.wait(0.5)

    loginButton_selector = "#register-login > form > table > tbody > tr:nth-child(3) > td > input[type=submit]"
    sb.click(loginButton_selector)
    sb.wait(3)

    if is_logged_in(sb):
        send_telegram_message(chatID, "Logged in successfully!")
        get_student_name(sb, user_id)
        sb.wait(1)
    else:
        send_telegram_message(chatID, "Login failed!")
        telegramHandler_V2.number_of_active_bots -= 1
        sys.exit()



def is_logged_in(sb):
    with contextlib.suppress(Exception):
        loginButton_selector = "#register-login > form > table > tbody > tr:nth-child(3) > td > input[type=submit]"
        sb.find_element(loginButton_selector)
        return False
       
    return True

def check_if_login_needed(chatID, sb, user_id, password):
    if not is_logged_in(sb):
        login(chatID, sb, user_id, password)


def get_student_name(sb, user_id):
    user_icon_selector = "body > div.master-header > div.header-top > div.user-area > ul > li:nth-child(4) > a"
    sb.click(user_icon_selector)
    sb.wait(2)

    name_selector = "body > div.master-header > div.header-top > div.user-area > div > table > tbody > tr:nth-child(2) > td:nth-child(2) > b"
    name = sb.get_text(name_selector)

    with open(f"users/info/{user_id}.txt", "a") as f:
        f.write(f"name: {name}\n")

def is_link_exists(link):
    return any(course.url == link for course in available_marks_courses)

def get_available_marks_links(sb):
    sb.open("https://ritaj.birzeit.edu/student/marks/term-summary")
    # sb.open("https://ritaj.birzeit.edu/student/marks/term-summary?term=1211") #TODO: remove this line
    sb.wait(3)

    cells_selector = "#slave > table > tbody > tr > td:nth-child(5) > a"
    cells = sb.find_elements(cells_selector)
    for cell in cells:
        mark_link = cell.get_attribute("href")
        if not is_link_exists(mark_link):
            available_marks_courses.append(Course(url=mark_link))
    
    sb.wait(2)

def get_course_mark(sb, course):
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


def send_telegram_message(chatID, course):
    bot = Bot(token=TELEGRAM_API_TOKEN)
    bot.send_message(chat_id=chatID, text=course)
