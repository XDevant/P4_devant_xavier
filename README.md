tournamentmanager.py is designed run a chess tournament with the swiss rules.

The spimplest way to test it is to:
1. Clone the repository on your own computer.

2. Create a new virtual environment in the same folder as scrap.py:

        python -m venv env

3. Activate the virtual environment
    + unix: source env/bin/activate
    + windows: env/Scripts/activate.bat

4. Install the dependencies via the requirement.txt file

        pip install -r requirements.txt

5. Run tournamentmanager.py:

        python3 tournamentmanager.py

Note: flake8-html
run flake8 --format=html --htmldir=flake-report --max-line-length 94
