#Daniel Fryer
#Assignment 7.2
#2/20/2026


""" import statements """
import mysql.connector # to connect
from mysql.connector import errorcode
 
import dotenv # to use .env file
from dotenv import dotenv_values
import os

#using our .env file
script_dir = os.path.dirname(__file__)
env_path = os.path.join(script_dir, ".env")
secrets = dotenv_values(env_path)

 
""" database config object """
config = {
    "user": secrets["USER"],
    "password": secrets["PASSWORD"],
    "host": secrets["HOST"],
    "database": secrets["DATABASE"],
    "raise_on_warnings": True #not in .env file
}

# Display function
def show_films(cursor, title):
    cursor.execute("""
        SELECT 
            film.film_name AS Name,
            film.film_director AS Director,
            genre.genre_name AS Genre,
            studio.studio_name AS Studio
        FROM film
        INNER JOIN genre ON film.genre_id = genre.genre_id
        INNER JOIN studio ON film.studio_id = studio.studio_id;
    """)
    
    films = cursor.fetchall()
    
    print()
    print(f"  -- {title} --")
    for film in films:
        print("Film Name: {}\nDirector: {}\nGenre Name ID: {}\nStudio Name: {}\n".format(film[0], film[1], film[2], film[3]))

#MySQL: mysql_test.py. Connection test codetry:
""" try/catch block for handling potential MySQL database errors """ 
try:
    db = mysql.connector.connect(**config) # connect to the movies database 
        
    cursor = db.cursor()
    show_films(cursor,"DISPLAYING FILMS")
    
    #Step 7 & 8 Inserting a new film and display
    insert = """
        INSERT INTO film(film_name, film_releaseDate, film_runtime, film_director, studio_id, genre_id)
        VALUES ('Jurassic Park', '1993', 126, 'Steven Spielberg', 3, 2)"""
    cursor.execute(insert)
    db.commit()
    
    show_films(cursor, "DISPLAYING FILMS AFTER INSERT")
    
    #Step 9 & 10 update alien to horror
    updates = """
        UPDATE film
        SET genre_id = 1
        WHERE film_name = 'Alien'"""
    cursor.execute(updates)
    db.commit()
    
    show_films(cursor, "DISPLAYING FILMS AFTER UPDATE - Changed Alien to Horror")
    
    #Step 11 & 12 Delete the show Gladiator
    removeFilm = """
        DELETE FROM film
        WHERE film_name = 'Gladiator'"""
    cursor.execute(removeFilm)
    db.commit()
    
    show_films(cursor, "DISPLAYING FILMS AFTER DELETE")
    
        
except mysql.connector.Error as err:
    """ on error code """
 
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("  The supplied username or password are invalid")

    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("  The specified database does not exist")

    else:
        print(err)
 
finally:
    #""" close the connection to MySQL """
 
    db.close()