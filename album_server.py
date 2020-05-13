from bottle import route
from bottle import run
from bottle import HTTPError
from bottle import request

import album


@route("/albums/<artist>")
def albums(artist):
	albums_list = album.find_artist(artist)

	if not albums_list:
		message = f"Альбомов {artist} не найдено!"
		return HTTPError(404, message)
	else:
		album_names = [album.album for album in albums_list]
		result = f"Количество альбомов {artist} - {len(albums_list)}:<br>"
		result += "<br>".join(album_names)
	return result


@route("/albums", method = "POST")
def new():
	year = request.forms.get("year")
	artist = request.forms.get("artist")
	genre = request.forms.get("genre")
	album_name = request.forms.get("album")

	try:
		year = int(year)
	except ValueError:
		return HTTPError(400, "Указан некорректный год альбома!")

	
	try:
		new_album = album.save_album(year, artist, genre, album_name)
	
	except AssertionError as err:
		result = HTTPError(400, str(err))
	
	except album.AlreadyExists as err:
		result = HTTPError(409, str(err))
	
	else:
		print(f"New #{new_album.id} album successfully saved")
		result = f"Альбом #{new_album.id} успешно сохранен"

	return result



if __name__ == '__main__':
	run(host="localhost", port=8080, debug=True)