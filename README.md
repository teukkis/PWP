# PWP SUMMER 2020
# Food Manager

### Installation

1. Clone or download the repository.
2. If you want to use virtual environment run `virtualenv food_manager_env --python=python3`.
and activate environment `. food_manager_env/bin/activate`. 
3. Browse to the project root directory and run `pip install .` to install foodManager and its dependecies.
4. Set environment variable: `export FLASK_APP=foodManager`.
5. Populated database `foodManager/dev.db` is supplied in the repo. But if you want to initialize and populate it, remove `dev.db` first. Then, initialize and populate database: `flask init-db` and `flask testgen`.
6. Serve flask app: `flask run`.

### Running tests

Unit and functional tests reside in `foodManager/tests`.
To run these tests:
1. Make sure you have pytest installed. If you don't, run `pip install pytest`
2. Navigate to project root and run `pytest tests/`.

In case the above instructions give ModuleNotFoundError, you can try the following:
1. Install pytest inside the environment: `pip install pytest`while the environment is activated.
2. Inside the project root, run `python -m pytest tests/`

# Food Manager Client

### installations
Make sure you have node.js installed.

1. clone or download the repository.
2. `cd` to `client` folder
3. `npm install`
4. `npm start` (starts the development server on port 3000)

### Client documentation

1. `cd` to `client` folder
2. `npm run docz:dev` (documentation server runs on port 3001)


# Group information
* Teemu Varsala, teemu.varsala@gmail.com
* Arttu Käyrä, arttukayra@gmail.com

__Remember to include all required documentation and HOWTOs, including how to create and populate the database, how to run and test the API, the url to the entrypoint and instructions on how to setup and run the client__


