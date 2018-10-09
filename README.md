# Skema

A visualization tool for use by UNBC faculty and staff to view and provide feedback on draft course schedules


***

**Instructions for first time development setup**

    git clone $(this_repository)
    cd Skema
    sudo apt-get install virtualenv
    virtualenv skema_venv
    . skema_venv/bin/activate
    ./setup.sh

Now that your environment is set up you can use 

    flask run
    
to run the app. Once the app is running, open a browser and navigate to 

    localhost:5000/skema
    
If everything is working correctly, you will see the app landing page

***

**Instructions for subsequent development setup**

    cd Skema
    . skema_venv/bin/activate
    
***

**Instructions for running unit tests**

    cd Skema/test
    nosetests
    
The nosetests command will run all unit tests found in the tests folder and any subfolder. All new code should be unit 
tested and all unit tests should be able to pass in under 1 second before a new pull request is made.
If you are reviewing someones pull request, please ensure you pull down their branch and ensure unit tests are passing
before approving the request

***

**Instructions for manipulating the database**


Database can be be manipulated with multiple different calls from within the virtual environment:

    flask init_database

will create a table called schedules, and replace an existing table with a new one.

    flask fill_database <file>

will fill the database with the data in the file.  An error is thrown if the file does not contain the correct data.  Currently using sample_data_2017.csv as a test file.

    flask fetch_database <column-name>

will print all the data in the requested column.  The options are: 

- crn
- course_id
- component_id 
- start_date
- end_date
- day
- start_time
- duration
- pattern_day
- pattern_start_time
- pattern_duration
- building_id
- room_number
- professor

These replace the \<column-name> in the above call.

    flask destroy_database

will remove the schedules table from the database.
