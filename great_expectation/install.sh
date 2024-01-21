python -m venv my_venv

source my_venv/bin/activate

python -m ensurepip --upgrade
python -m pip install great_expectations

great_expectations init