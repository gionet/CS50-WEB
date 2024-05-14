# CS50 - WEB Capstone

# Overview

This project was inspired by an instagram account that I happened to stumble upon. The account posts the percentage of year progress bar every day.

So, I decided to create my own version of it with added complexity and features for CS50's WEB capstone project, incorporating a To-Do-List CRUD feature without relying on any external libraries. The primary purpose of this project is for me to improve my coding skills as a beginner.

This Web-App is made for people who can't keep themselves accountable.

## Personal goal for this project
* Build a Single-page application
* Use PostgreSQL as backend database
* Use Javascript to implement CRUD function
* Use Docker for development environment

## Distinctiveness and Complexity:

It is distinctly different from the other projects in this course (Search, Wiki, Commerce, Mail, Network), although I did replicate the idea of Single Page Application (SPA) from 'Project 3: Mail'.

The complexity of this Capstone project lies primarily within the frontend development. I've implemented a fully interactive CRUD function using JavaScript on the frontend, with data transmission handled through fetchAPI to the backend, eliminating the need for the page to refresh after each interaction. Additionally, I've incorporated four types of progression bars (Yearly, Monthly, Weekly, Daily) that reflect the to-do-list/goals set for each timeline.

I have applied Object-Oriented Programming (OOP) concepts for Javascript to manage the live timeframe, resulting in cleaner code and reduced redundancy.

In total, there are three categories: To-Do-List, Completed Tasks, and Uncompleted Tasks.

## Documentation / Project Handbook

**Progression Bars**
* There are a total of four buttons (Yearly, Monthly, Weekly, Daily) located at the top left corner, that each display a time frame bar along with it's respective To-Do-List.
* Utilize sessionStorage to persist session data, ensuring that the webpage retains the user's previous session state upon revisiting.

**To-Do-List Category**
* A To-Do-List that tracks progress based on respective timeline. 
* To add a task, simply click "+ Add new item" in blue and it will prompt an empty textbox that says "Hit 'Enter' to submit", press enter on the keyboard to add it to the To-Do-List.
* Once a task has been added, there will be a green button with a tick on the left and a red button with a dustbin on the right.
    * Green button (left): Once clicked, it goes under 'COMPLETED' category.
    * Red button (right): once clicked, the task will be deleted.

**Completed Category**
* Completed To-Do item will displayed under Completed category for a duration of their own respective timeframe.
> Example: *(a post that is listed on date 2024/05/3)*  
> - timeframe 'yearly': 2024-01-01 to 2025-01-01
> - timeframe 'monthly': 2024-05-01 to 2024-06-01
> - timeframe 'weekly': 2024-04-29 to 2024-05-06 *(1 week - Monday to Sunday)*
> - timeframe 'daily': 00:00:00 to 23:59:59 *(Start to end of current day)*
  
* Yellow button (right): Functions as an undo button. Once clicked, it will revert the task back to 'TO DO LIST' category and refresh the listed date as if it were newly created.  
  
**Uncomplete (YYYY-MM-DD to YYYY-MM-DD) Category**
* The uncomplete section consists of tasks that have exceeded their respective timeframe for completion.  
* Any uncompleted task that is in the 'TO-DO-LIST' will automatically go under "UNCOMPLETED" once they have surpassed their designated completion timeframe.

* The tasks will remain in the uncomplete section for the whole period of the current time frame and can't be deleted. *(As a punishment and reflection)*  
> Example: *(assume a post that is listed on date 2024/05/03, Friday)*  
> - timeframe 'yearly': Listed as uncomplete on 2025/01/01 00:00:00 *(Beginning of next year)* **for 1 year**.  
> - timeframe 'monthly': Listed as uncomplete on 2024/06/01 00:00:00 *(Beginning of next month)* **for 1 month**.  
> - timeframe 'weekly': Listed as uncomplete on 2024/05/06 00:00:00, *(Monday)* **for 1 week**.  
> - timeframe 'daily': Listed as uncomplete on 2024/05/04 00:00:00 **for 1 day**.  

**Tabulate CSV**
* There is a button in teal-coloured button labeled 'CSV' beside 'Add new item' that generates a CSV file containing all historical and current raw data of all pending, completed, and uncompleted tasks in CSV format.

## What's contained in each file created
* static > progression.js: Consist of all the Frontend interactions as well as fetch API to make a request to the backend.  
* static > styles.css: Some of the styling aspects of this project.
* templates > homepage.html: Comprises the central visual elements of the entire project.
* templates > layout.html: Contains the Navbar template for the app.
* templates > login.html: Contains the login template for the app.
* templates > register.html: Contains the register template for the app.

* models.py: Consist of the project's model, mainly *Posts*.
* urls.py: Consists of paths for each view
* test.py: Contains server/client testing
    * Server login credentials
    * Client password mismatch
    * Client button functionality

* views.py: Contains endpoints for each view, as well as data filtering from database.

## How to run the application

(REMEMBER TO CHANGE 'settings.py' > 'DATABASES' ACCORDINGLY.)

Run with Docker, *build image*
In the root directory, run command
> docker-compose up -d --build

Run without Docker, *using pip*
> python -m pip install requirements.txt  
> python manage.py runserver

