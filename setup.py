import os
os.system('pip3 install git+https://github.com/gstaff/flask-ngrok')
os.system('pip3 install flask-ngrok')
os.system('pip install pymongo')
os.system('Flask_ENV="development"')
os.system('Flask_APP="app"')
os.system('python app.py runserver 0.0.0.0:8000')