from flask import Flask, render_template, request, url_for, redirect, abort, Response
import sqlite3 as sql

# create an instance object of the flask class 
app = Flask(__name__) # main class

# create afunction to handle musicdb connection 
def musicDBConnection():
     #conn variable = sql.connectMethod(path/filename)
    conn = sql.connect('Part14.Flask intro/c7Music.db')
    # row.factory syntax is used access/manipulate the database
    conn.row_factory = sql.Row
    return conn


# connections/links/routes to differnt pages within the website 
" home route"
@app.route('/') #set the route for the index.html
@app.route('/index') # set the route for the index.html
def index():
    # the index function will return the index.html page from the templates folder and display it on the browser
    return render_template('index.html', title="Home")

"retrieve and display songs from database"
@app.route('/songs') # set the route for the songs.html
def songs():
    #conn variable = sql.connectMethod(path/filename)
    conn = sql.connect('Part14.Flask intro/c7Music.db')
    # row.factory syntax is used access/manipulate the database
    conn.row_factory = sql.Row

    cursor = conn.cursor()
    cursor.execute('SELECT * FROM songs')

    getSongs = cursor.fetchall()

    return render_template('songs.html', title ='Songs', songsInDB = getSongs)

@app.route('/contact') # set the route for the songs.html
def contact():
    return render_template('contact.html', title ='Contact')

@app.route('/addsongs', methods=['GET','POST']) # set the route for the songs.html
def addsongs():
    if request.method == 'POST':
        title = request.form['Title']
        artist = request.form['Artist']
        genre = request.form['Genre']

        conn = musicDBConnection()
        cursor = conn.cursor()
        songID  = cursor.lastrowid

        cursor.execute('INSERT INTO songs( songID, title, artist, genre) VALUES (?,?,?,?)', (songID, title, artist, genre))
        conn.commit()
        conn.close()
        return redirect(url_for('songs'))
    return render_template('addsongs.html', title ='Add Songs')

@app.route('/about') # set the route for the songs.html
def about():
    return render_template('about.html', title ='About')


" create a funcion to get songs"
"getSong function has a ecordID as a parameter that determines what song to retrieve"
def getSong(recordID): #pass in recordID as a parameter
    # create an anstance of the db connection from the function musicDBConnection() and passed it to conn variable
    conn = musicDBConnection() 
    cursor = conn.cursor()
# execute sql query to get the record related to bgiven songID value. You get the post with the fetchone() method
    aSong = cursor.execute('SELECT * FROM songs WHERE songID =?', (recordID,)).fetchone()
    conn.close()
# if the post variable has the value none, meaning no result was found in the db, then execute the abort 404
    if aSong is None:
        # abort(404)
        abort(Response(f'No record {aSong} was found in the db'))
    return aSong

"Update Song"
"   get the datatype integer: SongID/update"
@app.route('/<int:songID>/update/', methods = ('GET','POST'))
def update(songID): # passed in the primary key(songID) from the song table
    aSongRecord = getSong(songID)
    if request.method == 'POST':
        title = request.form['Title']
        artist = request.form['Artist']
        genre = request.form['Genre']

        conn = musicDBConnection()
        cursor = conn.cursor()
        cursor.execute('UPDATE songs SET title = ?, artist = ?, genre = ?' 'WHERE songID= ?',(title, artist, genre, songID))
        conn.commit()
        conn.close()
        return redirect(url_for('songs')) # return to the songs page after update
    return render_template('updatesongs.html', title='Update Songs' ,aSongRecord = aSongRecord)



"Delete song"

@app.route('/<int:songID>/delete', methods=('POST',))
def delete(songID):
    conn = musicDBConnection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM songs WHERE songID = ?', (songID,))
    conn.commit()
    conn.close()
    return redirect(url_for('songs')) # return to the songs page after delete


#invoke/call the main class 
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port = 8100)