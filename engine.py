from flask import Flask, render_template, request,flash, redirect, render_template, send_file,jsonify
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
import requests
import os
from flask_json import FlaskJSON, JsonError, json_response, as_json
from datetime import datetime
from glob import glob
import os
import sys
from flask import Flask
import sys
import time

def getFolderPath():
	_getFilePath= os.getcwd()
	_getFilePath=_getFilePath+r'\\files\\'
	#print(_getFilePath)
	return _getFilePath
def getInstallPath():
	desktop = os.path.normpath(os.path.expanduser("~/Desktop"))
	return desktop


def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app = Flask(__name__)
app.secret_key = "secret key"
TEMPLATE_FOLDER=""
DOWNLOAD_FOLDER=""
FILE_FOLDER = getFolderPath()
UPLOAD_FOLDER =getFolderPath()
FOLDERPATH=getFolderPath()
allFiles=[]

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','mp3','mp4'])

FlaskJSON(app)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/uploader')
def upload_form():
	return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
	if request.method == 'POST':
        # check if the post request has the files part
		if 'files[]' not in request.files:
			flash('No file part')
			return redirect(request.url)
		files = request.files.getlist('files[]')
		for file in files:
			if file and allowed_file(file.filename):
				filename = secure_filename(file.filename)
				file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		flash('File(s) successfully uploaded')
		return redirect('/')
@app.route('/download',methods=['GET'])
def download_file():
	
	#path = "html2pdf.pdf"
	#path = "info.xlsx"
	path = "/abc.png"
	#path = "sample.txt"
	path=UPLOAD_FOLDER+path
	return send_file(path, as_attachment=True)

@app.route('/download/<name>',methods=['GET'])
def download_filebyname(name):
	#path = "html2pdf.pdf"
	#path = "info.xlsx"
	path = UPLOAD_FOLDER+name
	#path = "sample.txt"
	return send_file(path, as_attachment=True)

@app.route('/time_now')
def get_time():
    now = datetime.utcnow()
    return json_response(time=now,test1="test1",test2="test2",test3="test3")

@app.route('/increment_value', methods=['POST'])
def increment_value():
    # We use 'force' to skip mimetype checking to have shorter curl command.
    data = request.get_json(force=True)
    try:
        value = int(data['value'])
    except (KeyError, TypeError, ValueError):
        raise JsonError(description='Invalid value.')
    return json_response(value=value + 1)


filedata = []

def findMusicFiles():
	
	_getFilePath= os.getcwd()
	#full_path = os.path.realpath(__file__)
	#print(full_path)
	#print(_getFilePath)
	#UPLOAD_FOLDER=_getFilePath+r'\uploads'
	#print(filepath)
	testFile=glob(_getFilePath+r'\uploads\*.mp3')
	#print(testFile)
	filedata.clear()
	for test in testFile:
		_newstr=test.split(_getFilePath+'\\uploads\\')
		#print("->",_newstr[1]) 
		allFiles.clear()
		allFiles.append(_newstr[1])
		filedata.append({'id':1,'filename':_newstr[1],'size':'456'})
	print(filedata)

def jsonCreator():
	for file in allFiles:
		filedata.append({'id':1,'filename':file,'size':'456'})

@app.route('/get_value',methods=['GET'])
def get_value():
	findMusicFiles()
	return jsonify({'filedata':filedata})

@app.route('/est_conn')
def est_conn():
	return "Connection request." 

if __name__ == "__main__":
    print(getFolderPath())
    print(getInstallPath())
    IP="127.0.0.1"
    PORT = 5000
    app.run(host= IP,port=PORT)
 