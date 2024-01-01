# PROJECT-TEAMREPORT

# Project Management App

## Overview

This project management app is built using Django and Bootstrap to facilitate project development, test case management, and reporting.

## Features

- **Test Case Management:**
  - Create, update, and delete test cases.
  - Assign test cases to specific projects or sprints.

- **Test Execution:**
  - Run test cases and record test results.
  - Track test execution progress.

- **Reporting:**
  - Generate detailed reports on test case execution.
  - View project progress and testing statistics.

## Tech Stack

- **Backend:**
  - Django

- **Frontend:**
  - Bootstrap
  - HTML

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/shailender-shrma/team-report-app.git
   cd team-report-app
   ## Setup Instructions
   # Install dependencies using Pipenv
   pipenv install
    
   # Activate the virtual environment
   pipenv shell
    
   # Run migrations
   python manage.py migrate
    
   # Create a superuser (admin)
   python manage.py createsuperuser
    
   # Run the development server
   python manage.py runserver

