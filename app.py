from flask import Flask,render_template,request,redirect
from cs50 import SQL                                # importing the cs50.SQL module to connect db with python    

db = SQL("mysql://root:YES@localhost:3306/db_for_flask")    # connect with the MySQL database with python
app = Flask(__name__)

app.run(debug=True)

REGISTRANTS = {}
sports = ["BasketBall","Table Tennis","VolleyBall","Soccer"]

@app.route("/")
def index():
    return render_template("index.html",sports=sports)

@app.route("/register",methods=['GET','POST'])
def register():
    name = request.form.get("name")
    sport = request.form.get("sport")
    if not name or sport not in sports:
        return render_template("failure.html")
    # to store data in database , which will be permanent until it is deleted
    db.execute("insert into registrants_froshims(name,sport) values (?,?)",name,sport)
    # to store data in dictionary , this way is not good as it is available only once in runtime
    # REGISTRANTS[name] = sport 
    return redirect("/registrants")             # redirectly the user to the registrants route             
    # return render_template("success.html")

@app.route("/registrants")
def registrants():
    registrant = db.execute("select * from registrants_froshims")          # getting the data from the database
    return render_template("registrants.html",registrant=registrant)  

@app.route("/deregister",methods=["POST"])       # deregister 
def deregister():
    id = request.form.get("id") # get the id
    if id:
        db.execute("delete from registrants_froshims where id = ?",id)  # delete the row from database
    return redirect("/registrants")