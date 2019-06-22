import os
import subprocess
from flask import Flask, render_template, request
app = Flask(__name__)


APP_ROOT = os.path.dirname(os.path.abspath(__file__))



@app.route('/')
def index():
	return render_template('home.html')
	
	
@app.route('/', methods = ['POST'])
def upload():
	text = request.form['insert_code']
	f = open("input.c","w")
	f.write(text)
	f.close()
	subprocess.run(["python","cgrammar.py"],stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE, check = True)
	return render_template('about.html')
	

@app.route('/QueueArray')
def QueueArray():
	return render_template('QueueArray.html')
	
	
if __name__ == '__main__':
    app.run(debug = True,port = 8080)
    
