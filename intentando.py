import sqlite3


conn = sqlite3.connect('spotify.db')  # You can create a new database by changing the name within the quotes
c = conn.cursor()

c.execute('''DROP TABLE ARTIST''')
c.execute('''CREATE TABLE ARTIST (id text PRIMARY KEY, name text, age integer, self text, albums text, tracks text )''')

c.execute('''DROP TABLE ALBUM''')
c.execute('''CREATE TABLE ALBUM (id text PRIMARY KEY, name text, genre text, self text , artist text, tracks text , artist_id text, FOREIGN KEY (artist_ID) REFERENCES ARTIST(id))''')


c.execute('''DROP TABLE Track''')
c.execute('''CREATE TABLE TRACK (id text PRIMARY KEY , name int, duration int, times_played int, artist text, album text, self text, album_id, FOREIGN KEY (album_id) REFERENCES ALBUM(id))''')

keys_list = ("a", "b")
values_list = [1, 2]
zip_iterator = zip(keys_list, values_list)
a_dictionary = dict(zip_iterator)

print(a_dictionary)