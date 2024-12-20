"""This package contains the functionality of the target app.

The target app is used to track the number of daily applications made for a user. The
user can update the target amount in the target update page. If the target is met for 
a given day, the target is reset for the next day, the total_targets_met is incremented,
as well as the current_streak and a target task is created. 

The Streak instance tracks the current and longest streak for the user. A small effort 
to gamify the job hunting proccess, helping users to achieve their goals.

The target task is a task object created daily as a task for the user to complete, 
alongside other tasks.
"""
