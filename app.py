from flask import Flask, request, jsonify
from base64 import b64encode
from markupsafe import escape


app = Flask(__name__)

#app.config["DEBUG"] = True


#link= "https://tarea2jalliende.herokuapp.com"
link="http://127.0.0.1:5000"
artists={}
albums={}
tracks={}


###########################ARTISTAS###########################################
# Post de artista
@app.route('/artists', methods=['POST'])
def post_artist():
    json_data = request.json
    if json_data ==None:
        return '', 400 #input invalido

    name = json_data["name"]
    age = json_data["age"]

    if type(name)!=str or type(age)!=int:
        return '', 400    #input invalido

    ID = b64encode(name.encode()).decode('utf-8')[0:22]

    if ID in artists.keys():
        return jsonify(artists[ID]) , 409 #Artista ya existe

    albums = f"{link}/artists/{ID}/albums"
    tracks = f"{link}/artists/{ID}/tracks"
    Self = f"{link}/artists/{ID}"

    #hacer if si ya existe
    artists[ID] = {"id": ID, "name" : name, "age" : age, "albums": albums, "tracks" : tracks, "self" : Self}

    return jsonify(artists[ID]) , 201 #exitoso
   

#get de artista
@app.route('/artists/<artist_ID>', methods=['GET'])
def get_artist(artist_ID):

    if artist_ID not in artists.keys():
        return '' , 404 #artista no encontrado
    
    artista = artists[artist_ID]
    return jsonify(artista), 200 #exitoso
    

#get de artistas
@app.route('/artists', methods=['GET'])
def get_artists():

    artista = list(artists.values())
    
    return jsonify(artista), 200 #Siempre retorna exitoso



#DELETE de un artista
@app.route('/artists/<artist_ID>', methods=['DELETE'])
def delete_artist(artist_ID):

    if artist_ID in artists.keys():
        todos_albumes= list(albums.values())
        todas_canciones = list(tracks.values())
        for cancion in todas_canciones:
            if albums[cancion["album_id"]]["artist_id"] == artist_ID:
                del tracks[cancion["id"]]
        
        for album in todos_albumes:
            if album['artist_id']==artist_ID:
                del albums[album["id"]]

        del artists[artist_ID]

        return '', 204 #Artista Eliminado

    else:
        return '', 404 #Artista inexistente


#PUT de un artista
@app.route('/artists/<artist_ID>/albums/play', methods=['PUT'])
def put_artist(artist_ID):

    if artist_ID in artists.keys():
        todas_canciones = list(tracks.values())
        for cancion in todas_canciones:
            if albums[cancion["album_id"]]["artist_id"] == artist_ID:
                tracks[cancion["id"]]["times_played"]+=1

        return '', 200 #Todas las canciones del artista fueron reproducidas

    else:
        return '', 404 #Artista no encontrado

###########################ALBUMES###########################################


# Post de albumes
@app.route('/artists/<artist_ID>/albums', methods=['POST'])
def post_album(artist_ID):
    json_data = request.json
    if json_data ==None:
        return '', 400 #input invalido

    name = json_data["name"]
    genre = json_data["genre"]

    if type(name) != str or type(genre)!= str:
        return '', 400 #input invalido


    if artist_ID not in artists.keys():
        return '', 422 #Artista no existe

    id_pre_cod= f"{name}:{artist_ID}"
    ID = b64encode(id_pre_cod.encode()).decode('utf-8')[0:22]

    if ID in albums.keys():
        return jsonify(albums[ID]), 409 #Albumn ya existe

    Self = f"{link}/albums/{ID}"
    tracks = f"{link}/albums/{ID}/tracks"
    artist = f"{link}/artists/{artist_ID}"

    albums[ID] = {"id": ID, "name" : name, "genre" : genre, "self": Self, "tracks" : tracks, "artist" : artist, "artist_id" : artist_ID}

    return jsonify(albums[ID]), 201 #album creado


#get de album
@app.route('/albums/<album_ID>', methods=['GET'])
def get_album(album_ID):

    if album_ID not in albums.keys():
        return '', 404 #album no encontrado

    album = albums[album_ID]
    return jsonify(album), 200 #Get exitoso


#get de todos los albumes
@app.route('/albums', methods=['GET'])
def get_albums():

    album = list(albums.values())
    
    return jsonify(album), 200 #exitoso, este no falla
   

#get de todos los albumes de un artista
@app.route('/artists/<artist_ID>/albums', methods=['GET'])
def get_albums_of_artist(artist_ID):

    if artist_ID not in artists.keys():
        return '', 404 #artista no encontrado

    album = list(albums.values())
    albumes_artista =[]
    for elemento in album:
        if elemento["artist_id"] == artist_ID:
            albumes_artista.append(elemento)

    return jsonify(albumes_artista), 200 #Se encontraron todos los albumes


#DELETE de un album
@app.route('/albums/<album_ID>', methods=['DELETE'])
def delete_album(album_ID):

    if album_ID in albums.keys():
        todas_canciones= list(tracks.values())
        for cancion in todas_canciones:
            if cancion['album_id']==album_ID:
                del tracks[cancion["id"]]

        del albums[album_ID]

        return '', 204 #album eliminado

    else:
        return '', 404 #album no encontrado

#PUT de un album
@app.route('/albums/<album_ID>/tracks/play', methods=['PUT'])
def put_album(album_ID):

    if album_ID in albums.keys():
        todas_canciones= tracks.values()
        for cancion in todas_canciones:
            if cancion['album_id']==album_ID:
                cancion["times_played"] +=1

        return '', 200 #canciones repoducidas del album
    else:
        return '', 404 #album no encontrado

###########################TRACKS###########################################


# Post de tracks
@app.route('/albums/<album_ID>/tracks', methods=['POST'])
def post_track(album_ID):
    json_data = request.json

    if json_data ==None:
        return '', 400 #input invalido

    name = json_data["name"]
    duration = json_data["duration"]

    if type(name)!=str or (type(duration)!=float and type(duration)!=int): ###ACA ESTOY CONSIDERANDO QUE PUEDE SER INT O FLOAT, creo que solo deberia ser float
        return '', 400 #input invalido

    if album_ID not in albums.keys()
        return '', 422 #album no existe

    times_played = 0
    id_pre_cod= f"{name}:{album_ID}"
    ID = b64encode(id_pre_cod.encode()).decode('utf-8')[0:22]
    
    if ID in tracks.keys():
        return jsonify(tracks[ID]), 409 #Cancion ya existe

    Self = f"{link}/tracks/{ID}"
    album = f"{link}/albums/{album_ID}"
    artist_ID=albums[album_ID]["artist_id"]
    artist = f"{link}/artists/{artist_ID}"

    #hacer if si ya existe
    tracks[ID] = {"id": ID, "album_id": album_ID, "name" : name, "duration" : duration,"times_played": times_played, "self": Self, "artist" : artist, "album" : album}

    return jsonify(tracks[ID]), 201 #cancion creada

#get de un track
@app.route('/tracks/<track_ID>', methods=['GET'])
def get_track(track_ID):

    if track_ID not in tracks.keys():
         return '', 404 #cancion no encontrada

    track = tracks[track_ID]
    return jsonify(track), 200 #cancion encontrada
    


#get de todos los tracks
@app.route('/tracks', methods=['GET'])
def get_tracks():

    track = list(tracks.values())

    return jsonify(track), 200 #No falla, retorna todos los tracks


#get de todos los tracks de un artista
@app.route('/artists/<artist_ID>/tracks', methods=['GET'])
def get_tracks_of_artist(artist_ID):

    if artist_ID not in artists.keys():
        return '', 404 #Artista no encontrado

    track = list(tracks.values())
    tracks_artista =[]
    for cancion in track:
        if albums[cancion["album_id"]]["artist_id"] == artist_ID:
            tracks_artista.append(cancion)

    
    return jsonify(tracks_artista), 200 #Resultados obtenidos


#get de todos los tracks de un album
@app.route('/albums/<album_ID>/tracks', methods=['GET'])
def get_tracks_of_album(album_ID):

    if album_ID not in albums.keys():
        return '', 404 #Album no encontrado

    track = list(tracks.values())
    tracks_album =[]
    for cancion in track:
        if cancion["album_id"] == album_ID:
            tracks_album.append(cancion)

    
    return jsonify(tracks_album), 200 #resultados obtenidos



#DELETE de un track
@app.route('/tracks/<track_ID>', methods=['DELETE'])
def delete_track(track_ID):

    if track_ID in tracks.keys():
        del tracks[track_ID]

        return '', 204 #cancion eliminada

    else:
        return '', 404 #cancion inexistente

#PUT de un track
@app.route('/tracks/<track_ID>/play', methods=['PUT'])
def put_track(track_ID):

    if track_ID in tracks.keys():
        tracks[track_ID]["times_played"]+=1

        return '', 200 #Cancion reporducida

    else:
        return '', 404 #cancion no encontrada


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)