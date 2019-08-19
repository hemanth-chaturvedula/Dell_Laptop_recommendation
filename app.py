from flask import Flask,render_template,request
import csv
import os

app = Flask(__name__)	#initialising flask


@app.route('/', methods=["POST","GET"])
def index():
    return render_template("test.html")

@app.route('/send', methods=["POST"])
def post():
	link1=request.form.get('link1')
	link2=request.form.get('link2')
	link3=request.form.get('link3')
	link4=request.form.get('link4')    
	link5=request.form.get('link5')
	if link1 == "":
		return "No link given"
	file = open("registered.csv", "a")
	writer = csv.writer(file)
	writer.writerow((link1))
	return render_template("success.html")
@app.route('/recommendation', methods=["POST","GET"])
def recommend():
	rec = ""
	ptr = open("dell_case1.csv","r+")
	i = 0
	for line in ptr:
		i+=1
		if(i==1):
			continue
		line = line.split(",")
		print(line)
		rec += "<h2>" + line[0] + line[1] + " - ₹ " + line[-1] + "</h2><br/>Inches: " + line[2] + "</br>Screen Resolution:"
		rec += line[3] + "</br>CPU: " + line[4] + "</br>RAM: " + line[5] + "</br>Memory: "
		rec += line[6] + "</br>GPU: " + line[7] + "</br>OS: "+ line[8] + "</br>Weight: " + line[9] + "<br/><br/>"
	return render_template("recommendation.html",recommend=rec)

@app.route('/rating',methods=["POST","GET"])
def review():
	rating=request.form.get('sel1')
	review=request.form.get('review')
	file = open("review.csv","a")
	writer = csv.writer(file)
	writer.writerow((rating,review))
	file.close()
	return render_template("rating.html")

if(__name__=='__main__'):
    app.run(debug=True)
