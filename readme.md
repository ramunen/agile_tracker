To install package:  
pip install --editable .  
  
To run in dev mode with existing data :  
export FLASK_APP=flaskr  
export FLASK_ENV=development  
flask run  
  
To clear db:  
flask init-db  
  
Testing:  
pytest -v
