This test suite was created for skill eavluation purposes only.

It contains tests for the WeatherMapDummy application.

All tests are divided into the following groups:

1) Positive tests with correct parameters' values
2) Negative tests with empty parameters' values
3) Negative tests with invalid parameters' values
4) Negative test with parameters' values that are valid, but does not exist in data base
5) Negative tests with absent parameters
6) Other negative tests (request via POST HTTP method, invalid api route, unknown parameter, garbage instead of 
   parameters)

It is assumed that the test suite has read-only access to the same database as application under test - all data
is loaded from the same .json files as in the application under test, so entire object match is checked for returned
objects. Random data from the database is used in the tests, if possible.

report.html will be created in the project directory after test run.

To run application: 
1) copy files into single directory
2) create and enable python virtual environment (not necessary, but recomended)
3) install python 3.8.5 
4) install required dependencies from requirements.txt (pip install -r requirements.txt)
5) start WeatherMapDummy application int the separate terminal according to instructions from it's README.txt
6) adjust host and port values of apllication under test in the begining of the tests.py files
7) run in the terminal "pytest tests.py"

See report.html for full results