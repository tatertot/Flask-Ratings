from flask import Flask, render_template, redirect, request, url_for, escape, g
import model

app = Flask(__name__)

@app.route("/")
def index():
	user_list = model.session.query(model.User).limit(5).all()
	return render_template("user_list.html", users=user_list)

# createa a new user (signup)
@app.route("/sign_up")
def sign_up():
	
	return render_template("sign_up.html")

@app.route("/create_user", methods=["POST"])
def create_user():
	#get user name
	email = request.form['email']
	#get user password
	password = request.form['password']
	#get age & zipcode
	age = request.form['age']
	zipcode = request.form['zipcode']

	#create query
	user = model.User(email = email, password = password, age = age, zipcode= zipcode)
	#add the object to a session
	model.session.add(user)
    #commit session
	model.session.commit()
	return redirect("/index")

# login as a user 	
@app.route("/login")
def login():
	return render_template("login.html")

# authenticate user	
@app.route("/authenticate", methods=["POST"])
def authenticate():
	email = request.form['email']
	password = request.form['password']
	# capture the userid information from model-database
	user_id = model.authenticate(g.db, email, password)
	session['user_id'] = user_id
	# after getting the session variable back, you have to point it to a page
	return redirect("/")


# view a list of users
@app.route("/users")
def users():
	pass

#click on a user and view list of movies they've rated and their ratings
@app.route("/user_ratings_list/<int:id>", methods=["GET"])
def user_ratings_list(id):
	u_ratings_list = model.session.query(model.Rating).filter_by(user_id=id).all()
	return render_template("user_ratings_list.html", u_ratings_list = u_ratings_list)



# view record for a movie and add or update a personal rating for that movie
@app.route("/movie_record")
def movie_record():
	pass





if __name__ == "__main__":
	app.run(debug = True)

