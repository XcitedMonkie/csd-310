#Daniel Fryer
#Assignment 6.3
#2/14/2026


""" import statements """
import mysql.connector # to connect
from mysql.connector import errorcode
 
import dotenv # to use .env file
from dotenv import dotenv_values
import os

#using our .env file
#secrets = dotenv_values(".env") DF- This way was not finding the .env file finding the path based on where the file was located.
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

#MySQL: mysql_test.py. Connection test codetry:
""" try/catch block for handling potential MySQL database errors """ 
try:
    db = mysql.connector.connect(**config) # connect to the movies database 
        
    cursor = db.cursor()
    cursor.execute("SELECT * FROM studio")
    studios = cursor.fetchall()
    
    print("\n-- DISPLAYING Studio RECORDS --")
    for studio in studios:
        print(f"Studio ID: {studio[0]} \nStudio Name: {studio[1]}\n")
        
    cursor.execute("SELECT * FROM genre")
    genres = cursor.fetchall()
    
    print("\n-- DISPLAYING Genre RECORDS --")
    for genre in genres:
        print(f"Genre ID: {genre[0]} \nGenre Name: {genre[1]}\n")
        
    print("\n-- DISPLAYING Short Film RECORDS --")
    cursor.execute("SELECT film_name, film_runtime FROM film WHERE film_runtime <= 120")
    films = cursor.fetchall()
    for film in films:
        print(f"Film ID: {film[0]} \nRuntime: {film[1]}\n")
        
    print("\n-- DISPLAYING Director RECORDS in ORDER --")
    cursor.execute("SELECT film_name, film_director FROM film ORDER BY film_director")
    directorsFilms = cursor.fetchall()
    for df in directorsFilms:
        print(f"Film Name: {df[0]} \nDirector: {df[1]}\n")
 
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