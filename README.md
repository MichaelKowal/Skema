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
    
If everything is working correctly, you will see the app landing page.  Choose a semester that you would like to view and click 'Start Skema'.  This will bring you to the app that allows you to create a course schedule with all of the courses available in your chosen semester.

If there are no semesters available, or if the one you are looking for is not available, semesters can be uploaded by navigating to:

    localhost:5000/skema/admin
    
From here you can choose which semester you'd like and upload a file for that semester.

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
before approving the request.

***

**Instructions for manipulating the database**


The database can only be manipulated with one command line action:

    flask fill_database <file> <semesterName>

will fill the database with the data in the file.  An error is thrown if the file does not contain the correct data.  This works the same as the admin page but is easier to debug with than the page.
