from flask import Flask,render_template,request
app=Flask(__name__)
import csv
@app.route('/')
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
    with open("recommend.txt","r") as file:
        reader=file.read()
        return render_template("recommendation.html",recommend=reader)
    
@app.route('/rating',methods=["POST","GET"])
def review():
    rating=request.form.get('sel1')
    review=request.form.get('review')
    file = open("review.csv","a")
    writer = csv.writer(file)
    writer.writerow((rating,review))
    file.close()
    return render_template("rating.html")    