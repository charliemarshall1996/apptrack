# AppTrack

[![Build and Test](https://github.com/charliemarshall1996/apptrack/actions/workflows/build-and-test.yml/badge.svg?event=push)](https://github.com/charliemarshall1996/apptrack/actions/workflows/build-and-test.yml) [![codecov](https://codecov.io/gh/charliemarshall1996/apptrack/graph/badge.svg?token=F6THQZBDEL)](https://codecov.io/gh/charliemarshall1996/apptrack)

AppTrack is a web application designed to help candidates track job applications. It allows users to manage the stages of their job search by organizing applications into a structured workflow. The app provides users with an easy-to-use Kanban board, where they can track their progress through various job application stages.

## Features

- **Job Tracking:** Organize job applications into predefined stages: Open, Applied, Shortlisted, Interview, Offer, Rejected, Closed.
- **Kanban Board:** Visualize job applications in different stages using a drag-and-drop interface.
- **Tasks:** A focused 'tasks' view of all user tasks, related to applications and interviews.
- **Interview Calendar:** View a monthly calendar view of all upcoming interviews, with clickable events.
- **Dashboard:** User dashboard with essential stats and overviews of tasks, interviews and jobs.
- **User Accounts:** Each user has their own job tracking board and can manage multiple job applications.
- **User Reports:** Each user can download a .csv file of all the jobs reports from within a given start and end date. This is great if you are claiming JSA or something similar, whereby you must show proof of jobs you have been working towards.

## Apps

As is typical with django projects, AppTrack is speparated into several apps with an aim to tackle specific concerns:

- Accounts
- Blog
- Core
- Interviews
- Jobs
- Tasks

### Accounts

The accounts app manages user registration, logging in and out of AppTrack, the user profile and all associated functionality.

### Blog

The blog app manages the publicly viewable blog for AppTrack, as well as allowing administrators to create and schedule the publishing of blog posts from the admin panel.

### Core

This app manages functionality and inter-operability between the different applications within AppTrack, allowing for a cohesive experience.

### Interviews

This app allows users to schedule job interviews in a calendar layout, add notes about the companies they are interviewing at and view tasks to prepare.

### Jobs

This app provides users with the ability to add jobs they are interested in and track them as they move through the different stages of the application process. It allows for archiving of jobs, as well as the ability to view the different roles in both an interactive kanban-style 'board' layout and a 'list' layout.

### Tasks

This app provides users with the ability to create, view and prioritise tasks for different jobs and interviews, allowing them to ensure they are ready for any job they have or are looking to apply for.
