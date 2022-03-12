

## **Introduction**

  

FreJunTeamTaskDjango is Django project for managing Tasks and Teams.

  

## **Setup**

  

-   **Libraries used:**
    1.  Django
    2.  DRF
    3.  SQLITE
    4. Celery
    5. Redis
    

-   **Install Dependencies**
    
    1.  IDE Pycharm
    2.  Run ‘`pip install -r requirements.txt’` to install the remaining necessary packages.
    3. Open your terminal and run command `sudo apt-get install redis-server` to install redis.
        
    

## **Available Apis**

1.  "http://localhost:8000/api/v1/team" -> To create teams, 
2. "http://localhost:8000/api/v1/availabily" -> To check the available members of a team
3. "http://localhost:8000/api/v1/task" -> Create and Update Task.
4. "http://localhost:8000/api/v1/report" -> Get the updates of tasks for a specific date.
    

## **Points to remember**

-   Keep your redis server on.
-  Check the settings.py for broker_url(You might need to change it based on you redis server.)
-  For sending email please set the required environment variables mentions in settings.py


## **Run**

-   Refer / Run _ `python manage.py runserver`.
-  Terminal 2 `celery -A FreJunTeamTaskDjango worker -l info`
