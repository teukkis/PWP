# PWP SUMMER 2020
# Food Manager

### Installation

1. Clone or download the repository.
2. If you want to use virtual environment run `virtualenv food_manager_env --python=python3`.
and activate environment `. food_manager_env/bin/activate`. 
3. Browse to the project root directory and run `pip install .` to install foodManager and its dependecies.
4. Set environment variable: `export FLASK_APP=foodManager`.
5. Initialize and populate database: `flask init-db` and `flask testgen`.
6. Serve flask app: `flask run`.

### Running tests

Unit and functional tests reside in `foodManager/tests`.
To run these tests:
1. Make sure you have pytest installed. If you don't, run `pip install pytest`
2. Navigate to project root and run `pytest tests/`. 

# Group information
* Teemu Varsala, teemu.varsala@gmail.com
* Arttu Käyrä

__Remember to include all required documentation and HOWTOs, including how to create and populate the database, how to run and test the API, the url to the entrypoint and instructions on how to setup and run the client__


