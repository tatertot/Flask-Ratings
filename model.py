import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, scoped_session, relationship, backref
from sqlalchemy import ForeignKey
import correlation


# There is a side effect of this change. You no longer need to instantiate the 
# Session class, as it doesn't exist. It's replaced with a session object that 
# is somehow always connected. On top of that, this is safe to use this session 
# directly without explicitly connecting to the database

#This is SQLAlchemy's way of interacting with the db, creating a session
engine = create_engine("sqlite:///ratings.db", echo=False)
session = scoped_session(sessionmaker(bind=engine,autocommit = False, autoflush = False))

Base = declarative_base() #This is required by SQLAlchemy 
Base.query = session.query_property()

### Class declarations go here
class User(Base):

	__tablename__ = "users" # tells SQLAlchemy  instance stored in table named users

	id = Column(Integer, primary_key = True)
	email = Column(String(64), nullable = True)
	password = Column(String(64), nullable  = True)
	age = Column(Integer, nullable = True)
	zipcode = Column(String(15),nullable=True)

	def similarity(self,other):
		#create dictionary to hold user 1's ratings
		u_ratings = {}
		#create pair list
		paired_ratings = []

		#put ratings in dictionary (movie_id=>rating)
		for r in self.ratings:
			u_ratings[r.movie_id] = r 

		#loop through user2's ratings
		for r in other.ratings:
			#you are comparing user 2's movie id(from the rating) and checking if that movie id is in user 1's list 
			u_r = u_ratings.get(r.movie_id) 	
			#if ther's a match, get rating and create & add pair
			if u_r:
				paired_ratings.append((u_r.rating, r.rating))
		#feed pair list to pearson function if there's at least one pair
		if paired_ratings:
			return correlation.pearson(paired_ratings)
		else:
			return 0.0

	def predict_rating(user,movie):
		ratings = user.ratings
		other_ratings = movie.ratings
		other_users = [ r.user for r in other_ratings ]
		similarities = [ (user.similarity(other_user), other_user \
			for other_user in other_users ]
		similarities.sort(reverse = True)
		top_user = similarities[0]
		matched_rating = None
		for rating in other_ratings:
			if rating.user_id == top_user[1].id
				matched_rating = rating
				break
		return matched_rating.rating * top_user[0]

	# apparently don't need this function, it's optional
	# def __init__(self,  email = None, password = None, age = None, zipcode = None):
	# 	self.email = email
	# 	self.password = password
	# 	self.age = age
	# 	self.zipcode = zipcode

class Movie(Base):

	__tablename__ = "movies"

	id = Column(Integer, primary_key = True)
	movie_title = Column(String(128), nullable = True)
	released_at = Column(DateTime(),  nullable = True)	
	imdb_url = Column(String(128), nullable = True)

class Rating(Base):

	__tablename__ = "ratings"

	id = Column(Integer, primary_key = True)
	user_id = Column(Integer(15), ForeignKey('users.id'), nullable = False)
	movie_id = Column(Integer(15), ForeignKey('movies.id'), nullable = False)
	rating = Column(Integer(1), nullable = False)
	released_at = Column(DateTime(),  default=datetime.datetime.now)

	user = relationship("User", backref=backref("ratings", order_by=id))
	movie = relationship("Movie", backref=backref("ratings",order_by=id))


### End class declarations


#moving connect method so we can do multithreading for mulit user application
#def connect(): 
	# global ENGINE
	# global Session

	# #This is SQLAlchemy's way of interacting with the db, creating a session
	# ENGINE = create_engine("sqlite:///ratings.db", echo=True)
	# Session = sessionmaker(bind=ENGINE)

	# return Session()



def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()
