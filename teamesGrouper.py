from __future__ import annotations
from re import A
from tkinter import Menu
from turtle import st

import urwid

import pandas as pd
import numpy as np
import os
import sys
import random

from urwid.widget.widget import Widget
import typing


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


# Create a list of students
def create_students_list(df):
    students = []
    for index, row in df.iterrows():
        students.append([row['first name'], row['last name'], False])
    return students
# print(students)


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

# Terminal UI 1: Select the absent students
# absents | first name | last name
# [ ]     | John       | Doe
# [ ]     | Jane       | Doe
# ...
class AbsentStudentsWidget(urwid.WidgetWrap):
    def __init__(self, students):
        self.students = students
        self.listbox = urwid.ListBox(urwid.SimpleFocusListWalker(self._create_widgets()))
        super().__init__(self.listbox)
    
    #       UI:
    #       absents | first name | last name
    #       [ ]     | John       | Doe
    #       [ ]     | Jane       | Doe
    #       ...
    #       [ ] ist eine Checkbox die wenn man während sie ausgewählt ist und dann enter gedrückt wird erst den schüler als abwesend markiert wodurch aus [ ] ein [X] wo das X rot ist wird und dann zum nächsten schüler springt
    def _create_widgets(self):
        widgets = []

        # Add headers
        headers = ['Abwesenheit', 'Vorname', 'Nachname']
        widgets.append(urwid.Columns([urwid.Text(h) for h in headers], dividechars=1))

        # Add students
        for student in self.students:
            checkbox = urwid.CheckBox('')
            firstname = urwid.Text(student[0])
            lastname = urwid.Text(student[1])
            columns = urwid.Columns([checkbox, firstname, lastname], dividechars=1)
            widgets.append(columns)

        return widgets
    
    def listbox(self):
        return self.listbox



# UI View
class MenuView(urwid.WidgetWrap):
    palette: typing.ClassVar[tuple[str, str, str, ...]] = [
        ("body", "black", "light gray", "standout"),
        ("header", "white", "dark red", "bold"),
        ("screen edge", "light blue", "dark cyan"),
        ("main shadow", "dark gray", "black"),
        ("line", "black", "light gray", "standout"),
        ("bg background", "light gray", "black"),
        ("bg 1", "black", "dark blue", "standout"),
        ("bg 1 smooth", "dark blue", "black"),
        ("bg 2", "black", "dark cyan", "standout"),
        ("bg 2 smooth", "dark cyan", "black"),
        ("button normal", "light gray", "dark blue", "standout"),
        ("button select", "white", "dark green"),
        ("line", "black", "light gray", "standout"),
        ("pg normal", "white", "black", "standout"),
        ("pg complete", "white", "dark magenta"),
        ("pg smooth", "dark magenta", "black"),
        ("absent student", "white", "dark red", "standout")
    ]
    def __init__(self, students):
        self.students = students
        
        super().__init__(self.main_window())
    def _create_widgets(self):
        widgets = []
        blank = urwid.Divider()
        for student in self.students:
            widgets.append(urwid.Text(student[0] + " " + student[1]))
        
        print(widgets)
        widgets.append(blank)
        print(widgets)
        student_widget = AbsentStudentsWidget(students=self.students)._create_widgets()
        print(student_widget)
        widgets.append(student_widget)
        
        return widgets
    
    def keypress(self, size, key):
        if key in ("Q", "q", "esc"):
            raise urwid.ExitMainLoop()
        elif key == "enter":
            #self.listbox.body.append(urwid.Text("You pressed enter"))
            return super().keypress(size, key)
        else:
            return super().keypress(size, key)

    def mouse_event(self, size, event, button, col, row, focus):
        # This method will be called when a mouse event occurs.
        # You can implement your mouse handling logic here.
        pass
    
    def main_window(self):
        self.listbox = urwid.ListBox(urwid.SimpleListWalker(self._create_widgets()))
        w = self.listbox
        #w = urwid.LineBox(urwid.SimpleListWalker(self.listbox))
        return w
    

# UI Controller
class MenuController:
    def __init__(self, students):
        self.students = students
        self.view = MenuView(students=self.students)
    
    def unhandled_input(self, key):
        size = ('unknown', 'unknown')
        return self.view.keypress(size, key)
    
    
    def main(self):
        self.loop = urwid.MainLoop(self.view, self.view.palette, handle_mouse=True, unhandled_input=self.unhandled_input)
        self.loop.run()

def main():
    # Read in the data
    df = pd.read_csv('students.csv', header=0)
    students = create_students_list(df=df)
    print(students)
    print(sort_students(students=students, sorting_mode=2))
    MenuController(students=students).main()


if __name__ == '__main__':
    main()