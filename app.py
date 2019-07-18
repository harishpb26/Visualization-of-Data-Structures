import os
import json
import subprocess
from flask import Flask, render_template, request
from flask_cors import CORS
from cgrammar import cgrammarfunc

app = Flask(__name__)
CORS(app)
complist = []

@app.route('/')
def index():
	return render_template('home.html')

@app.route('/', methods = ['POST'])
def upload():
	text = request.form['insert_code']
	global complist
	complist = []
	for i in text.split('\n'):
		if(i.strip()):
			print(i)
			complist.append(json.loads(cgrammarfunc(i)))

	print(complist)
	f = open("input.c","w")
	f.write(text)
	f.close()

	'''
	p = subprocess.run(["python","cgrammar.py"],stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE,check = True)

	p = subprocess.Popen(['python','cgrammar.py'], stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
	p = subprocess.check_output(['python','cgrammar.py'])
	stdout, stderr = p.communicate()
	#rc = p.returncode
	print(p,type(p))
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
	iter = 0
	xpos = 120
	ypos = 60
	height = 50
	width = 120
	xvpos = xpos + width * 5
	yvpos = ypos
	xtemp = xpos
	ytemp = ypos
	xvtemp = xvpos
	yvtemp = yvpos
	#data = {"a": ["int", 10], "p": ["struct Node", {"data": ["int", "?"], "link": ["struct Node*", "?"]}]}
	temp = {}
	print(complist)
	for data in complist:
		for key in data:
			if(key in temp):
				if(isinstance(data[key][1], dict)):
					data[key].insert(2,temp[key][2])
					data[key].insert(3,temp[key][3])
					for content in data[key][1]:
						data[key][1][content].insert(3, temp[key][1][content][3])
						data[key][1][content].insert(2, temp[key][1][content][2])

				else:
					data[key].insert(2,temp[key][2])
					data[key].insert(3, temp[key][3])

			else:
				if(isinstance(data[key][1], dict)):
					data[key].insert(2, [xtemp, ytemp])
					for content_key in data[key][1]:
						ytemp = ytemp + height
						data[key][1][content_key].insert(3, iter)
						data[key][1][content_key].insert(2, [xtemp,ytemp])
						iter += 2
					ytemp = ytemp + height * 2
					xtemp = xpos
					data[key].insert(3, iter)
					iter += 1

				else:
					data[key].insert(2, [xvtemp,yvtemp])
					yvtemp = yvtemp+ height*2.5
					data[key].insert(3, iter)
					iter += 2
				temp[key] = data[key]

	return json.dumps(complist)


@app.route('/QueueArray')
def QueueArray():
	return render_template('QueueArray.html')


@app.route('/Structure')
def Structure():
	return render_template('S.html')


if __name__ == '__main__':
    app.run(debug = True,port = 8080)
