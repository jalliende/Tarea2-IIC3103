from flask import Flask, request, jsonify
from base64 import b64encode
from markupsafe import escape


app = Flask(__name__)

#app.config["DEBUG"] = True



artists={}
albums={}
tracks={}


###########################ARTISTAS###########################################
# Post de artista
@app.route('/artists', methods=['POST'])
def post_artist():
    link= request.base_url
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
        return jsonify(artists[ID])
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


#get de artista
@app.route('/artists', methods=['GET'])
def get_artists():

    artista = list(artists.values())
    if artista:
        return jsonify(artista)
    else:
        return jsonify({
            "ERROR": "no hay artistas existentes"
        })



###########################ALBUMES###########################################


# Post de albumes
@app.route('/artists/<artist_ID>/albums', methods=['POST'])
def post_album(artist_ID):
    link= request.base_url
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
        return jsonify({
            "ERROR": "no hay artistas existentes"
        })


###########################TRACKS###########################################


# Post de tracks
@app.route('/albums/<album_ID>/tracks', methods=['POST'])
def post_track(album_ID):
    link= request.base_url
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


# A welcome message to test our server
@app.route('/')
def index():
    link= request.base_url
    return f"<h1>Welcome to {link} our server !!</h1>"

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)