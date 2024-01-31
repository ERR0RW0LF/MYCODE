import pandas as pd
import numpy as np
import os
import sys
import random
import curses

# Terminal Ui were the user can move up and down the list of students and select the ones that are absent
# The user can also select the number of teams and the number of students per team
# CMD UI
#   absent | first name | last name
#   [ ]    | John       | Doe
#   [ ]    | Jane       | Doe
#
# Teams: 2
# Students per team: 2
#
# Team 1: John Doe, Jane Doe
# Team 2: ...
#
# Press enter to continue

# up and down arrows to move up and down the list
# space to set absent
# enter to continue
# number of teams can be set by the user
# number of students per team will be calculated by the program and if there is a bigger remainder it will be added to the first teams
# the program will print out the teams and the user can press enter to continue
# the program will print out the team members that the program randomly selected and the user can adjust the teams by pressing enter will the pointer is on a student and then press enter again on another student to switch them
# the program will print out the teams again and the user can press enter to continue or adjust the teams again

# students.csv will look like this:
# first name, last name
# John, Doe
# Jane, Doe
# ...

# Seting up the terminal ui
def setup_ui():
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    return stdscr

# Create a list of students
def create_students_list(df):
    students = []
    for index, row in df.iterrows():
        students.append([row['first name'], row['last name'], False])
    return students
# print(students)

# Create terminal ui for selecting absent students
# q: how to make the terminal ui
# a: use curses library
# q: what is curses library?
# a: curses is a terminal ui library for python
# q: how to use curses library?
# a: https://docs.python.org/3/howto/curses.html


# Stop the terminal ui
def stop_ui(stdscr):
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()
    return stdscr

# Sort the students by absent and present, first name or last name
def sort_students(students, sorting_mode: int):
    if students == []:
        return []
    if sorting_mode == 0:   # Mode 0: Absent and present, present first
        # q: how does sorted(students, key=lambda x: (x[2], x[0], x[1]) work?
        # a: https://docs.python.org/3/howto/sorting.html
        return sorted(students, key=lambda x: (x[2], x[0], x[1]))
    elif sorting_mode == 1: # Mode 1: First name, A to Z
        return sorted(students, key=lambda x: (x[0], x[1], x[2]))
    elif sorting_mode == 2: # Mode 2: Last name, A to Z
        return sorted(students, key=lambda x: (x[1], x[0], x[2]))
    else:
        return []


def main():
    # Read in the data
    df = pd.read_csv('students.csv', header=0)
    students = create_students_list(df=df)
    print(students)
    print(sort_students(students=students, sorting_mode=0))