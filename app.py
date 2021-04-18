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
        return jsonify({"ERROR": "no JSON found."})

    name = json_data["name"]
    age = json_data["age"]
    ID = b64encode(name.encode()).decode('utf-8')[0:22]  
    albums = f"{link}/artists/{ID}/albums"
    tracks = f"{link}/artists/{ID}/tracks"
    Self = f"{link}/artists/{ID}"

    #hacer if si ya existe
    artists[ID] = {"id": ID, "name" : name, "age" : age, "albums": albums, "tracks" : tracks, "self" : Self}

    if artists[ID]:
        return jsonify(artists[ID]) ,200 #con esto cambio el codigo
    else:
        return jsonify({
            "ERROR": "no name found, please send a name."
        })


#get de artista
@app.route('/artists/<artist_ID>', methods=['GET'])
def get_artist(artist_ID):

    artista = artists[artist_ID]
    if artista:
        return jsonify(artista)
    else:
        return jsonify({
            "ERROR": "no name found, please send a name."
        })


#get de artistas
@app.route('/artists', methods=['GET'])
def get_artists():

    artista = list(artists.values())
    if artista:
        return jsonify(artista)
    else:
        return jsonify({})


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

        return jsonify({
            "BIEN": "artista eliminado exitosamente"
        })

    else:
        return jsonify({
            "ERROR": "No existe ese album"
        })


#PUT de un artista
@app.route('/artists/<artist_ID>/play', methods=['PUT'])
def put_artist(artist_ID):

    if artist_ID in artists.keys():
        todas_canciones = list(tracks.values())
        for cancion in todas_canciones:
            if albums[cancion["album_id"]]["artist_id"] == artist_ID:
                tracks[cancion["id"]]["times_played"]+=1

        return jsonify({
            "BIEN": "artista reproducido exitosamente"
        })

    else:
        return jsonify({
            "ERROR": "No existe ese album"
        })


###########################ALBUMES###########################################


# Post de albumes
@app.route('/artists/<artist_ID>/albums', methods=['POST'])
def post_album(artist_ID):
    json_data = request.json
    if json_data ==None:
        return jsonify({"ERROR": "no JSON found."})

    name = json_data["name"]
    genre = json_data["genre"]
    artist_ID = artist_ID
    id_pre_cod= f"{name}:{artist_ID}"
    ID = b64encode(id_pre_cod.encode()).decode('utf-8')[0:22]    
    Self = f"{link}/albums/{ID}"
    tracks = f"{link}/albums/{ID}/tracks"
    artist = f"{link}/artists/{artist_ID}"

    #hacer if si ya existe
    albums[ID] = {"id": ID, "name" : name, "genre" : genre, "self": Self, "tracks" : tracks, "artist" : artist, "artist_id" : artist_ID}

    if albums[ID]:
        return jsonify(albums[ID])
    else:
        return jsonify({
            "ERROR": "no name found, please send a name."
        })


#get de album
@app.route('/albums/<album_ID>', methods=['GET'])
def get_album(album_ID):

    album = albums[album_ID]
    if album:
        return jsonify(album)
    else:
        return jsonify({
            "ERROR": "no name found, please send a name."
        })


#get de todos los albumes
@app.route('/albums', methods=['GET'])
def get_albums():

    album = list(albums.values())
    if album:
        return jsonify(album)
    else:
        return jsonify({})


#get de todos los albumes de un artista
@app.route('/artists/<artist_ID>/albums', methods=['GET'])
def get_albums_of_artist(artist_ID):
    album = list(albums.values())
    albumes_artista =[]
    for elemento in album:
        if elemento["artist_id"] == artist_ID:
            albumes_artista.append(elemento)

    if albumes_artista:
        return jsonify(albumes_artista)
    else:
        return jsonify({
            "ERROR": "no hay albumes de este artista"
        })


#DELETE de un album
@app.route('/albums/<album_ID>', methods=['DELETE'])
def delete_album(album_ID):

    if album_ID in albums.keys():
        todas_canciones= list(tracks.values())
        for cancion in todas_canciones:
            if cancion['album_id']==album_ID:
                del tracks[cancion["id"]]

        del albums[album_ID]

        return jsonify({
            "BIEN": "Album eliminado exitosamente"
        })

    else:
        return jsonify({
            "ERROR": "No existe ese album"
        })


#PUT de un album
@app.route('/albums/<album_ID>/play', methods=['PUT'])
def put_album(album_ID):

    if album_ID in albums.keys():
        todas_canciones= tracks.values()
        for cancion in todas_canciones:
            if cancion['album_id']==album_ID:
                cancion["times_played"] +=1

        return jsonify({
            "BIEN": "Album reproducido exitosamente"
        })

    else:
        return jsonify({
            "ERROR": "No existe ese album"
        })

###########################TRACKS###########################################


# Post de tracks
@app.route('/albums/<album_ID>/tracks', methods=['POST'])
def post_track(album_ID):
    json_data = request.json
    if json_data ==None:
        return jsonify({"ERROR": "no JSON found."})

    name = json_data["name"]
    duration = json_data["duration"]
    album_ID = album_ID
    times_played = 0 ##Esto es 0 solo si recien fue creada
    id_pre_cod= f"{name}:{album_ID}"
    ID = b64encode(id_pre_cod.encode()).decode('utf-8')[0:22]    
    Self = f"{link}/tracks/{ID}"
    album = f"{link}/albums/{album_ID}"
    artist_ID=albums[album_ID]["artist_id"]
    artist = f"{link}/artists/{artist_ID}"

    #hacer if si ya existe
    tracks[ID] = {"id": ID, "album_id": album_ID, "name" : name, "duration" : duration,"times_played": times_played, "self": Self, "artist" : artist, "album" : album}

    if tracks[ID]:
        return jsonify(tracks[ID])
    else:
        return jsonify({
            "ERROR": "no name found, please send a name."
        })

#get de un track
@app.route('/tracks/<track_ID>', methods=['GET'])
def get_track(track_ID):

    if track_ID not in tracks.keys():
         return jsonify({
            "ERROR": "No existe esa cancion."
        })

    track = tracks[track_ID]
    return jsonify(track)
    


#get de todos los tracks
@app.route('/tracks', methods=['GET'])
def get_tracks():

    track = list(tracks.values())
    if track:
        return jsonify(track)
    else:
        return jsonify({})


#get de todos los tracks de un artista
@app.route('/artists/<artist_ID>/tracks', methods=['GET'])
def get_tracks_of_artist(artist_ID):
    track = list(tracks.values())
    tracks_artista =[]
    for cancion in track:
        if albums[cancion["album_id"]]["artist_id"] == artist_ID:
            tracks_artista.append(cancion)

    if tracks_artista:
        return jsonify(tracks_artista)
    else:
        return jsonify({
            "ERROR": "no hay tracks de este artista"
        })

#get de todos los tracks de un album
@app.route('/albums/<album_ID>/tracks', methods=['GET'])
def get_tracks_of_album(album_ID):
    track = list(tracks.values())
    tracks_album =[]
    for cancion in track:
        if cancion["album_id"] == album_ID:
            tracks_album.append(cancion)

    if tracks_album:
        return jsonify(tracks_album)
    else:
        return jsonify({
            "ERROR": "no hay tracks de este album"
        })


#DELETE de un track
@app.route('/tracks/<track_ID>', methods=['DELETE'])
def delete_track(track_ID):

    if track_ID in tracks.keys():
        del tracks[track_ID]
        return jsonify({
            "BIEN": "Cancion eliminada exitosamente"
        })

    else:
        return jsonify({
            "ERROR": "No existe esa cancion"
        })


#PUT de un track
@app.route('/tracks/<track_ID>/play', methods=['PUT'])
def put_track(track_ID):

    if track_ID in tracks.keys():
        tracks[track_ID]["times_played"]+=1
        return jsonify({
            "BIEN": "Cancion reproducida exitosamente"
        })

    else:
        return jsonify({
            "ERROR": "No existe esa cancion"
        })



if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)