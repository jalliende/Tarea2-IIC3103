from flask import Flask, request, jsonify
from base64 import b64encode
from markupsafe import escape
import sqlite3



app = Flask(__name__)
app.config["DEBUG"] = True





###########################ARTISTAS###########################################
# Post de artista
@app.route('/artists', methods=['POST'])
def post_artist():
    link= "https://tarea2jalliende.herokuapp.com"
    columnas= ("id","name","age","self","albums","tracks")
    conn = sqlite3.connect('spotify.db')

    json_data = request.json
    if json_data ==None:
        conn.close()
        return '', 400 #input invalido

    name = json_data["name"]
    age = json_data["age"]

    if type(name)!=str or type(age)!=int:
        conn.close()
        return '', 400    #input invalido

    ID = b64encode(name.encode()).decode('utf-8')[0:22]

    query= """SELECT * FROM ARTIST WHERE id=? ;"""

    cursor = conn.cursor()
    artistas = cursor.execute(query, (ID,)).fetchone()

    if artistas:
        zip_iterator = zip(columnas, artistas)
        a_dictionary = dict(zip_iterator)
        conn.close()
        
        return jsonify(a_dictionary) , 409 #Artista ya existe

    albu = f"{link}/artists/{ID}/albums"
    trac = f"{link}/artists/{ID}/tracks"
    Self = f"{link}/artists/{ID}"


    
    query= """INSERT INTO ARTIST (id, name, age, Self, albums, tracks) VALUES (?, ?, ?, ?, ?, ?)"""
    record = (ID, name, age, Self, albu, trac)
    cursor.execute(query, record)
    conn.commit()
    conn.close()
    return jsonify({"id": ID, "name" : name, "age" : age, "albums": albu, "tracks" : trac, "self" : Self}) , 201 #exitoso


#get de artista
@app.route('/artists/<artist_ID>', methods=['GET'])
def get_artist(artist_ID):
    conn = sqlite3.connect('spotify.db')
    columnas= ("id","name","age","self","albums","tracks")
    query= """SELECT * FROM ARTIST WHERE id=? ;"""
    
    cursor = conn.cursor()
    artistas = cursor.execute(query, (artist_ID,)).fetchone()

    if artistas:
        zip_iterator = zip(columnas, artistas)
        a_dictionary = dict(zip_iterator)
        conn.close()
        return jsonify(a_dictionary) , 200 #exitoso
    
    conn.close()
    return '', 404 #No existe



#get de artistas
@app.route('/artists', methods=['GET'])
def get_artists():
    conn = sqlite3.connect('spotify.db')
    columnas= ("id","name","age","self","albums","tracks")
    query= """SELECT * FROM ARTIST;"""
    
    cursor = conn.cursor()
    artistas = cursor.execute(query).fetchall()
    lista_artistas= []

    for elemento in artistas:
        zip_iterator = zip(columnas, elemento)
        a_dictionary = dict(zip_iterator)
        lista_artistas.append(a_dictionary)

    conn.close()
    return jsonify(lista_artistas), 200 #Siempre retorna exitoso


#DELETE de un artista
@app.route('/artists/<artist_ID>', methods=['DELETE'])
def delete_artist(artist_ID):

    conn = sqlite3.connect('spotify.db')
    conn.execute("PRAGMA foreign_keys = ON")
    columnas= ("id","name","age","self","albums","tracks")
    query= """SELECT * FROM ARTIST WHERE id=? ;"""

    cursor = conn.cursor()
    artistas = cursor.execute(query, (artist_ID,)).fetchone()

    if artistas:
        query_2= """DELETE FROM ARTIST WHERE id=? ;"""
        cursor.execute(query_2, (artist_ID,))
        conn.commit()

        return '', 204 #Artista Eliminado

    else:
        return '', 404 #Artista inexistente


#PUT de un artista
@app.route('/artists/<artist_ID>/albums/play', methods=['PUT'])
def put_artist(artist_ID):
    link= "https://tarea2jalliende.herokuapp.com"
    conn = sqlite3.connect('spotify.db')
    query= """SELECT * FROM ARTIST WHERE id=? ;"""
    cursor = conn.cursor()
    artist = cursor.execute(query, (artist_ID,)).fetchone()


    if not artist:
        conn.commit()
        return '', 404 #Artista no encontrado

    query= """SELECT id, times_played FROM TRACK WHERE artist=? ;"""
    tracks = cursor.execute(query, (f"{link}/artists/{artist_ID}",)).fetchall()

    for cancion in tracks:
        times_played= cancion[1] + 1
        query_2= '''UPDATE TRACK SET times_played = ? WHERE id = ?;'''
        cursor.execute(query_2, (times_played, cancion[0],))
        conn.commit()
    
    return '', 200 #Artista reproducido



###########################ALBUMES###########################################


# Post de albumes
@app.route('/artists/<artist_ID>/albums', methods=['POST'])
def post_album(artist_ID):
    link= "https://tarea2jalliende.herokuapp.com"
    columnas= ("id","name","genre","self","artist","tracks" , "artist_id")
    conn = sqlite3.connect('spotify.db')


    json_data = request.json
    if json_data ==None:
        conn.close()
        return '', 400 #input invalido

    name = json_data["name"]
    genre = json_data["genre"]

    if type(name) != str or type(genre)!= str:
        conn.close()
        return '', 400 #input invalido

    query= """SELECT * FROM ARTIST WHERE id=? ;"""
    cursor = conn.cursor()
    artistas = cursor.execute(query, (artist_ID,)).fetchone()

    if not artistas:
        conn.close()
        return '' , 422 #Artista no existente



    id_pre_cod= f"{name}:{artist_ID}"
    ID = b64encode(id_pre_cod.encode()).decode('utf-8')[0:22]

    query= """SELECT * FROM ALBUM WHERE id=? ;"""
    cursor = conn.cursor()
    albums = cursor.execute(query, (ID,)).fetchone()

    if albums:
        zip_iterator = zip(columnas, albums)
        a_dictionary = dict(zip_iterator)
        conn.close()
        return jsonify(a_dictionary), 409 #Album ya existe


    Self = f"{link}/albums/{ID}"
    trac = f"{link}/albums/{ID}/tracks"
    artist = f"{link}/artists/{artist_ID}"

    query= """INSERT INTO ALBUM (id, name, genre, self, artist, tracks, artist_id) VALUES (?, ?, ?, ?, ?, ?, ?)"""
    record = (ID, name, genre, Self, artist, trac, artist_ID)
    cursor.execute(query, record)
    conn.commit()
    conn.close()

    return jsonify({"id": ID, "name" : name, "genre" : genre, "self": Self, "tracks" : trac, "artist" : artist, "artist_id" : artist_ID}), 201 #album creado


#get de album
@app.route('/albums/<album_ID>', methods=['GET'])
def get_album(album_ID):

    conn = sqlite3.connect('spotify.db')
    columnas= ("id","name","genre","self","artist","tracks" , "artist_id")
    query= """SELECT * FROM ALBUM WHERE id=? ;"""

    cursor = conn.cursor()
    album = cursor.execute(query, (album_ID,)).fetchone()

    if album:
        zip_iterator = zip(columnas, album)
        a_dictionary = dict(zip_iterator)
        conn.close()

        return jsonify(a_dictionary) , 200 #exitoso
    
    conn.close()
    return '', 404 #Album no encontrado


#get de todos los albumes
@app.route('/albums', methods=['GET'])
def get_albums():
    
    conn = sqlite3.connect('spotify.db')
    columnas= ("id","name","genre","self","artist","tracks" , "artist_id")
    query= """SELECT * FROM ALBUM;"""

    cursor = conn.cursor()
    albumes = cursor.execute(query).fetchall()
    lista_albumes= []

    for elemento in albumes:
        zip_iterator = zip(columnas, elemento)
        a_dictionary = dict(zip_iterator)
        lista_albumes.append(a_dictionary)

    conn.close()
    return jsonify(lista_albumes), 200 #Siempre retorna exitoso
   

#get de todos los albumes de un artista
@app.route('/artists/<artist_ID>/albums', methods=['GET'])
def get_albums_of_artist(artist_ID):

    conn = sqlite3.connect('spotify.db')
    query= """SELECT * FROM ARTIST WHERE id=? ;"""
    cursor = conn.cursor()
    artist = cursor.execute(query, (artist_ID,)).fetchone()

    if not artist:
        conn.commit()
        return '', 404 #Artista no encontrado

    query= """SELECT * FROM ALBUM WHERE artist_id=? ;"""

    columnas= ("id","name","genre","self","artist","tracks" , "artist_id")

    albumes = cursor.execute(query,(artist_ID,)).fetchall()
    lista_albumes= []

    for elemento in albumes:
        zip_iterator = zip(columnas, elemento)
        a_dictionary = dict(zip_iterator)
        lista_albumes.append(a_dictionary)

    conn.close()
    return jsonify(lista_albumes), 200 #Se encontraron todos los albumes


#DELETE de un album
@app.route('/albums/<album_ID>', methods=['DELETE'])
def delete_album(album_ID):

    conn = sqlite3.connect('spotify.db')
    conn.execute("PRAGMA foreign_keys = ON")
    query= """SELECT * FROM ALBUM WHERE id=? ;"""

    cursor = conn.cursor()
    album = cursor.execute(query, (album_ID,)).fetchone()


    if album:
        query_2= """DELETE FROM ALBUM WHERE id=? ;"""
        cursor.execute(query_2, (album_ID,))
        conn.commit()
        return '', 204 #album eliminado

    else:
        return '', 404 #album no encontrado


#PUT de un album
@app.route('/albums/<album_ID>/tracks/play', methods=['PUT'])
def put_album(album_ID):

    conn = sqlite3.connect('spotify.db')
    query= """SELECT * FROM ALBUM WHERE id=? ;"""
    cursor = conn.cursor()
    album = cursor.execute(query, (album_ID,)).fetchone()


    if not album:
        conn.commit()
        return '', 404 #album no encontrado


    query= """SELECT id, times_played FROM TRACK WHERE album_id=? ;"""
    tracks = cursor.execute(query, (album_ID,)).fetchall()

    for cancion in tracks:
        times_played= cancion[1] + 1
        query_2= '''UPDATE TRACK SET times_played = ? WHERE id = ?;'''
        cursor.execute(query_2, (times_played, cancion[0],))
        conn.commit()
    
    return '', 200 #Cancion reporducida
        

###########################TRACKS###########################################


# Post de tracks
@app.route('/albums/<album_ID>/tracks', methods=['POST'])
def post_track(album_ID):
    link= "https://tarea2jalliende.herokuapp.com"
    columnas= ("id","name","duration","times_played", "artist", "album","self", "album_id")


    conn = sqlite3.connect('spotify.db')
    json_data = request.json

    if json_data ==None:
        return '', 400 #input invalido

    name = json_data["name"]
    duration = json_data["duration"]

    if type(name)!=str or (type(duration)!=float and type(duration)!=int):
        return '', 400 #input invalido

    #Revisar que exista el album
    query= """SELECT * FROM ALBUM WHERE id=? ;"""
    cursor = conn.cursor()
    album = cursor.execute(query, (album_ID,)).fetchone()

    if not album:
        conn.close()
        return '' , 422 #album no existe


    times_played = 0
    id_pre_cod= f"{name}:{album_ID}"
    ID = b64encode(id_pre_cod.encode()).decode('utf-8')[0:22]

    query= """SELECT * FROM TRACK WHERE id=? ;"""
    cursor = conn.cursor()
    tracks = cursor.execute(query, (ID,)).fetchone()

    if tracks:
        zip_iterator = zip(columnas, tracks)
        a_dictionary = dict(zip_iterator)
        conn.close()
        return jsonify(a_dictionary), 409 #Cancion ya existe

    Self = f"{link}/tracks/{ID}"
    album = f"{link}/albums/{album_ID}"

    query= """SELECT * FROM ALBUM WHERE id=? ;"""
    cursor = conn.cursor()
    albums = cursor.execute(query, (album_ID,)).fetchone()

    artist_ID = albums[6] #deberia ser el id del artista
    artist = f"{link}/artists/{artist_ID}"

    query= """INSERT INTO TRACK (id, name, duration, times_played, artist, album, self, album_id)VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
    record = (ID, name, duration, times_played, artist, album, Self, album_ID)
    cursor.execute(query, record)
    conn.commit()
    conn.close()

    
    return jsonify({"id": ID, "album_id": album_ID, "name" : name, "duration" : duration,"times_played": times_played, "self": Self, "artist" : artist, "album" : album}), 201 #cancion creada


#get de un track
@app.route('/tracks/<track_ID>', methods=['GET'])
def get_track(track_ID):

    conn = sqlite3.connect('spotify.db')
    columnas= ("id","name","duration","times_played", "artist", "album","self", "album_id")
    query= """SELECT * FROM TRACK WHERE id=? ;"""

    cursor = conn.cursor()
    track = cursor.execute(query, (track_ID,)).fetchone()

    if track:
        zip_iterator = zip(columnas, track)
        a_dictionary = dict(zip_iterator)
        conn.close()

        return jsonify(a_dictionary) , 200 #exitoso


    conn.close()
    return '', 404 #TRack no encontrado
    


#get de todos los tracks
@app.route('/tracks', methods=['GET'])
def get_tracks():
    conn = sqlite3.connect('spotify.db')
    columnas= ("id","name","duration","times_played", "artist", "album","self", "album_id")
    query= """SELECT * FROM TRACK;"""

    cursor = conn.cursor()
    tracks = cursor.execute(query).fetchall()
    lista_tracks= []

    for elemento in tracks:
        zip_iterator = zip(columnas, elemento)
        a_dictionary = dict(zip_iterator)
        lista_tracks.append(a_dictionary)

    conn.close()
    return jsonify(lista_tracks), 200 #Siempre retorna exitoso



#get de todos los tracks de un artista
@app.route('/artists/<artist_ID>/tracks', methods=['GET'])
def get_tracks_of_artist(artist_ID):
    link= "https://tarea2jalliende.herokuapp.com"
    conn = sqlite3.connect('spotify.db')
    query= """SELECT * FROM ARTIST WHERE id=? ;"""
    cursor = conn.cursor()
    artist = cursor.execute(query, (artist_ID,)).fetchone()

    if not artist:
        conn.commit()
        return '', 404 #Artista no encontrado

    query= """SELECT * FROM TRACK WHERE artist=? ;"""
    columnas= ("id","name","duration","times_played", "artist", "album","self", "album_id")

    tracks = cursor.execute(query,(f"{link}/artists/{artist_ID}",)).fetchall()
    lista_tracks= []

    for elemento in tracks:
        zip_iterator = zip(columnas, elemento)
        a_dictionary = dict(zip_iterator)
        lista_tracks.append(a_dictionary)

    conn.close()
    return jsonify(lista_tracks), 200 #Se devuelven los tracks


#get de todos los tracks de un album
@app.route('/albums/<album_ID>/tracks', methods=['GET'])
def get_tracks_of_album(album_ID):
    conn = sqlite3.connect('spotify.db')
    query= """SELECT * FROM ALBUM WHERE id=? ;"""
    cursor = conn.cursor()
    album = cursor.execute(query, (album_ID,)).fetchone()

    if not album:
        conn.commit()
        return '', 404 #Album no encontrado

    query= """SELECT * FROM TRACK WHERE album_id=? ;"""
    columnas= ("id","name","duration","times_played", "artist", "album","self", "album_id")

    tracks = cursor.execute(query,(album_ID,)).fetchall()
    lista_tracks= []

    for elemento in tracks:
        zip_iterator = zip(columnas, elemento)
        a_dictionary = dict(zip_iterator)
        lista_tracks.append(a_dictionary)

    conn.close()
    return jsonify(lista_tracks), 200 #Se devuelven los tracks



#DELETE de un track
@app.route('/tracks/<track_ID>', methods=['DELETE'])
def delete_track(track_ID):
    conn = sqlite3.connect('spotify.db')
    query= """SELECT * FROM TRACK WHERE id=? ;"""

    cursor = conn.cursor()
    track = cursor.execute(query, (track_ID,)).fetchone()


    if track:
        query_2= """DELETE FROM TRACK WHERE id=? ;"""
        cursor.execute(query_2, (track_ID,))
        conn.commit()
        return '', 204 #track eliminado

    else:
        return '', 404 #track no encontrado



#PUT de un track
@app.route('/tracks/<track_ID>/play', methods=['PUT'])
def put_track(track_ID):
    conn = sqlite3.connect('spotify.db')
    query= """SELECT times_played FROM TRACK WHERE id=? ;"""

    cursor = conn.cursor()
    track = cursor.execute(query, (track_ID,)).fetchone()


    if track:
        times_played= track[0] + 1
        query_2= '''UPDATE TRACK SET times_played = ? WHERE id = ?;'''
        cursor.execute(query_2, (times_played, track_ID,))
        conn.commit()
        return '', 200 #Cancion reporducida

    else:
        return '', 404 #cancion no encontrada



# A welcome message to test our server
@app.route('/')
def index():
    link= "https://tarea2jalliende.herokuapp.com"
    return f"<h1>Welcome to {link} our server !!</h1>"

if __name__ == '__main__':
    app.run()