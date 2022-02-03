# import required packages
from flask import Flask, render_template, g, request
import sqlite3
import random

app = Flask(__name__)

def get_message_db():
    """
    This function is creating the database
    of messages.
    ---------------------------------------
    """

    # Check whether there is a database
    # connect to that database if not
    if 'message_db' not in g:
        g.message_db = sqlite3.connect("messages_db.sqlite")

    # create table if not exists messages
    cursor = g.message_db.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS messages (id INTEGER, handle TEXT, message TEXT)")

    # return the database
    return g.message_db

def insert_message(request):
    """
    This function is inserting a user message
    into the database of messages.
    ---------------------------------------
    """

    # Extract the message and the handle
    message = request.form["message"]
    handle = request.form["handle"]

    # connect to the database
    db = get_message_db()

    # Using cursor to insert the message
    # into the message database
    cursor = db.cursor()
    cursor.execute("INSERT INTO messages (message, handle) VALUES (?, ?)", (message, handle))

    # ensure the row insertion has been saved
    db.commit()

    # close the database connection
    cursor.close()
    db.close()

def random_messages(n):
    """
    This function will return a collection
    of n random messages from the message_db.
    ---------------------------------------
    """

    # connect to the database
    db = get_message_db()

    # Using cursor to insert the random message
    # from the message table
    cursor = db.cursor()
    message = cursor.execute(f'SELECT handle, message FROM messages ORDER BY RANDOM() LIMIT {n}')
    message = message.fetchmany(n)

    # close the database connection
    cursor.close()
    db.close()

    # return to the message
    return message

@app.route("/")
def main():
    """
    This function will return the base.html template
    """

    return render_template("base.html")

@app.route("/submit/", methods = ['POST', 'GET'])
def submit():
    """
    This function will return the submit.html template
    """

    # adding messages and name
    if request.method == "GET":
        return render_template("submit.html")
    # return information when submitted message and name
    else:
        insert_message(request)
        return render_template("submit.html", submitted = True)

@app.route("/view/")
def view():
    """
    This function will return the view.html template
    """

    # make a cap for the random messages
    return render_template("view.html", messages = random_messages(3))