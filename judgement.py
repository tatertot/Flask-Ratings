from flask import Flask, render_template, redirect, request, url_for, escape, session
import model

app = Flask(__name__)

@app.route("/")
def index():
	user_id = session.get("user_id", None)
	user_list = model.session.query(model.User).limit(5).all()
	return render_template("user_list.html", users=user_list, user_id=user_id)

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
	return redirect("/")

# login as a user 	
@app.route("/login")
def login():
	return render_template("login.html")

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('user_id', None)
    return redirect(url_for('index'))

# authenticate user	
@app.route("/authenticate", methods=["POST"])
def authenticate():
	email = request.form['email']
	password = request.form['password']
	# capture the userid information from model-database
	user_query = model.session.query(model.User).filter_by(email=email,password=password)
	if user_query.first():
		user = user_query.first()
		# after getting the session variable back, you have to point it to a page
		session['user_id'] = user.id
		return redirect("/")
	else:
		flash = "Try again!"
		return redirect("/login")


# view a list of users
@app.route("/users")
def users():
	pass

#click on a user and view list of movies they've rated and their ratings
@app.route("/user_ratings_list/<int:id>", methods=["GET"])
def user_ratings_list(id):
	u_ratings_list = model.session.query(model.Rating).filter_by(user_id=id).all()
	return render_template("user_ratings_list.html", u_ratings_list = u_ratings_list)


@app.route("/user_movie_rating/<int:movie_id>/<int:user_id>", methods=["GET"])
def user_movie_rating(movie_id, user_id):
	ind_rating = model.session.query(model.Rating).filter_by(user_id = user_id, movie_id = movie_id).first()
	return render_template("user_movie_rating.html", ind_rating = ind_rating)


@app.route("/rate_movie", methods=["POST"])
def rate_movie():
	#get user id
	user_id = request.form['user_id']
	#get movie id
	movie_id = request.form['movie_id']
	#get rating
	rating = request.form['rating']

	#create query
	rating = model.Rating(user_id = user_id, movie_id = movie_id, rating = rating)
	#add the object to a session
	model.session.add(rating)
    #commit session
	model.session.commit()
	return redirect("/")


# view record for a movie and add or update a personal rating for that movie
@app.route("/movie_list")
def movie_list():
	movie_list_query = model.session.query(model.Movie).all()
	return render_template("movie_list.html", movie_list = movie_list_query)


@app.route("/movie/<int:id>/", methods=["GET"])
def movie(id):
	user_id = session.get("user_id", None)

	user_rating_query = model.session.query(model.Rating).filter_by(user_id=user_id,movie_id=id)
	try:
		user_rating_query.one()
		rating_status = True
		user = user_rating_query.one()
		
	except:
		rating_status = False
		

	movie = model.session.query(model.Rating).filter_by(movie_id=id).all()
	# after getting the session variable back, you have to point it to a page
	return render_template("movie.html", movie = movie, user_id=user_id, rating_status=rating_status)


@app.route("/view_movie/<int:id>/", methods=["GET"])
def view_movie(id):
	movie = model.session.query(model.Movie).get(id)
	ratings = movie.ratings
	rating_nums = []
	user_rating = None
	for r in ratings:
		if r.user_id == session['user_id']:
			user_rating = r
		rating_nums.append(r.rating)
	ave_rating = float(sum(rating_nums))/len(rating_nums)

	#Prediction code (if user hasn't rated)
	user = model.session.query(model.User).get(session['user_id'])
	prediction = None
	if not user_rating:
		prediction = user.predict_rating(movie)
		effective_rating = prediction
	else: 
		effective_rating = user_rating.rating

	the_eye = model.session.query(model.User).filter_by(email="theeye@ofjudgement.com").one()
	eye_rating = model.session.query(model.Rating).filter_by(user_id=the_eye.id, movie_id=movie.id).first()

	if not eye_rating:
		eye_rating = the_eye.predict_rating(movie)
	else:
		eye_rating = eye_rating.rating
	#difference = abs(eye_rating - effective_rating)

	#messages = [ "I suppose you odn't have such bad taste after all.","I regret every decision that I've...","Words fail me, as your taste in movies has clearly failed you.","That movie is great. For a clown to watch. Idiot."]
	
	#beratement = messages[1]
	#end prediction

	return render_template("view_movie.html", movie=movie, average=ave_rating, user_rating=user_rating, prediction=prediction)


# set the secret key.  keep this really secret:
app.secret_key = 'banana banana banana'

if __name__ == "__main__":
	app.run(debug = True)

