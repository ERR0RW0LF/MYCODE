import pandas as pd
import numpy as np
import os
import sys

# Read in the data
df = pd.read_csv('students.csv')

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