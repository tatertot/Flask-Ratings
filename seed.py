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
            print dbRow
        #create an object
            user = model.User(email = "email", password = "password", age = dbRow[1], zipcode=dbRow[4])
        #add the object to a session
            session.add(user)
            session.commit() # do i commit after every iteration or can i commit at the end of the loop
            break

    #commit session

    #repeat until done

    pass

def load_movies(session):
    # use u.item
    pass

def load_ratings(session):
    # use u.data
    pass

def main(session):
    # You'll call each of the load_* functions with the session as an argument
    load_users(session)
    #pass

if __name__ == "__main__":
    s= model.connect()
    main(s)
