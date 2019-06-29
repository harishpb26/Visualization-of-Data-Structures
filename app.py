import os
import json
import subprocess
from flask import Flask, render_template, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
	return render_template('home.html')

@app.route('/', methods = ['POST'])
def upload():

	text = request.form['insert_code']
	f = open("input.c","w")
	f.write(text)
	f.close()

	p = subprocess.run(["python","cgrammar.py"],stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE, check = True)

	'''
	p = subprocess.Popen(['python', 'cgrammar.py'], stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
	stdout,stderr = p.communicate()
	#rc = p.returncode
	print(stdout,type(stdout))
	my_json = stdout.decode("utf8").replace("'",'"')
	print(my_json)
	#return json.dumps(my_json)
	'''
	return render_template('about.html')


@app.route('/anime')
def anime():
	with open("var_type.json") as f:
		data = json.load(f)
	return json.dumps(data)

# (xpos , ypos) - coordinate of label  struct


@app.route('/animek')
def animek():
	with open("var_dict.json") as f:
		data = json.load(f)
	#data = {"a": ["int", 10], "p": ["struct Node", {"data": ["int", "?"], "link": ["struct Node*", "?"]}]}
	iter = 0
	xpos = 80
	ypos = 60
	height = 50
	width = 120
	xvpos = xpos
	yvpos = ypos + height*6
	xtemp = xpos
	ytemp = ypos
	xvtemp = xvpos
	yvtemp = yvpos
	for key in data:
		if(isinstance(data[key][1], dict)):
			data[key].insert(2, [xtemp, ytemp])
			for content_key in data[key][1]:
				ytemp = ytemp + height
				data[key][1][content_key].insert(3, iter)
				data[key][1][content_key].insert(2, [xtemp,ytemp])
				iter += 2
			ytemp = ypos
			xtemp = xtemp + width*13
			data[key].insert(3, iter)
			iter += 1
		else:
			data[key].insert(2, [xvtemp,yvtemp])
			xvtemp = xvtemp+ width*1.5
			data[key].insert(3, iter)
			iter += 2

	return json.dumps(data)



@app.route('/QueueArray')
def QueueArray():
	return render_template('QueueArray.html')


@app.route('/Structure')
def Structure():
	return render_template('S.html')


if __name__ == '__main__':
    app.run(debug = True,port = 8080)
