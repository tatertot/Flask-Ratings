import model
import csv



def load_users(session):
    # use u.user

    #open a file
    with open('seed_data/u.user','rb') as csvfile:
        userList = csv.reader(csvfile, delimiter=' ', quotechar='/')
        #read a line
        for row in userList:
        #parse a line
            dbRow = row[0].split('|')
        #create an object
            user = model.User(email = "email", password = "password", age = dbRow[1], zipcode=dbRow[4])
        #add the object to a session
            session.add(user)
        #commit session
        session.commit()


def load_movies(session):
    # use u.item
        #open a file
    with open('seed_data/u.item','rb') as csvfile:
        movieList = csv.reader(csvfile, delimiter='|', quotechar='/')
        #read a line
        for row in movieList:
            #parse a line
            #convert date month into datetime format
            date_str = row[2]
            if date_str == '':
                date_str = '01-Jan-1980'
            
            formatted_date = model.datetime.datetime.strptime(date_str, "%d-%b-%Y")
            print formatted_date
        #create an object
            movie = model.Movie(movie_title = row[1].decode("latin-1"), released_at= formatted_date, imdb_url=row[4])
        #add the object to a session
            session.add(movie)
        #commit session
        session.commit() # do i commit after every iteration or can i commit at the end of the loop


def load_ratings(session):
    # use u.data
    #open a file
    with open('seed_data/u.data','rb') as csvfile:
        ratingsList = csv.reader(csvfile, delimiter='\t', quotechar='/')
        #read a line
        for row in ratingsList:
        #parse a line
        #create an object
            rating = model.Rating(user_id = row[0], movie_id= row[1], rating = row[2], released_at=model.datetime.datetime.utcfromtimestamp(int(row[3])))
        #add the object to a session
            session.add(rating)
        #commit session
        session.commit() # do i commit after every iteration or can i commit at the end of the loop
            

def main(session):
    # You'll call each of the load_* functions with the session as an argument
    load_users(session)
    load_movies(session)
    load_ratings(session)

if __name__ == "__main__":
    s= model.connect()
    main(s)
