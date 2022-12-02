import pandas as pd
import pickle
import requests
import time

from pprint import pprint
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sklearn
from sklearn.ensemble import GradientBoostingClassifier


# for reference
# {'Happy': 0, 'Sad': 1, 'Energetic': 2, 'Calm':3, 'Angry':4, 'Classy': 5})



SPOTIFY_GET_CURRENT_TRACK_URL = 'https://api.spotify.com/v1/me/player/currently-playing'
#https://developer.spotify.com/console/get-users-currently-playing-track/?market=&additional_types=
ACCESS_TOKEN = 'BQDiarmtKvD_9ljswzZe_3dt3bqyiIG4R0qzXhMx6tTA8i9VD8mzxo-l2QrnLCxSBWnR-Bc2e6jRccdprCqqJlKl9qJLxyN7WEJbktlIK-o21PpoLkxI4rLmtzkzbiWJfgJEbfpnvE7VPSaBme0Je-rjlwIeGzxhWPAEuu-A4UkEp74B-czFANnrv7Dc'
CLIENT_ID = '1ef70d044f5c4ab2ac32a3fd8cb9a5c1'
CLIENT_SECRET = '56a2ecbda2574448af8850c12b6b7cdd'


MODEL_FILEPATH = 'models/RandomForestNoKey.sav'
URL = 'http://172.20.10.10:3000/'
# URL = 'http://172.30.68.238:3000/'


def get_current_track(access_token):
	response = requests.get(
		SPOTIFY_GET_CURRENT_TRACK_URL,
		headers={
			"Authorization": f"Bearer {access_token}"
		}
	)
	json_resp = response.json()
	
	try:
		track_id = json_resp['item']['id']
		track_name = json_resp['item']['name']
		artists = [artist for artist in json_resp['item']['artists']]

		link = json_resp['item']['external_urls']['spotify']
	except KeyError:
		print("Access Token Expired")
		return

	artist_names = ', '.join([artist['name'] for artist in artists])

	current_track_info = {
		"id": track_id,
		"track_name": track_name,
		"artists": artist_names,
		"link": link
	}

	return current_track_info


class WrapperClass:
	def __init__(self):
		self.CLIENT_ID = CLIENT_ID
		self.CLIENT_SECRET = CLIENT_SECRET

		self.sp = self.doAuth()

	def doAuth(self, scope="playlist-modify-public"):
		'''
			Funtion: Setup and initialization of credentials manager and 
			master Spotify object

			Returns: Spotify Object
		'''

		credentialsManager = \
		SpotifyClientCredentials(client_id=self.CLIENT_ID, client_secret=self.CLIENT_SECRET)
		
		sp = spotipy.Spotify(client_credentials_manager=credentialsManager)
		return sp 


	def getFeatures(self, songUri):
			popularity = []
			length = []
			danceability = []
			acousticness = []
			energy = []
			instrumentalness = []
			liveness = []
			valence = []
			loudness = []
			speechiness = []
			tempo = []
			key = []
			timeSignature = []
			
			uri = songUri
			if(not isinstance(uri, str)):
				return
			
			features = self.sp.audio_features(uri)
			track = self.sp.track(uri)
			if features != [None]:
				popularity.append(track['popularity'])
				length.append(features[0]['duration_ms'])
				danceability.append(features[0]['danceability'])
				acousticness.append(features[0]['acousticness'])
				energy.append(features[0]['energy'])
				instrumentalness.append(features[0]['instrumentalness'])
				liveness.append(features[0]['liveness'])
				valence.append(features[0]['valence'])
				loudness.append(features[0]['loudness'])
				speechiness.append(features[0]['speechiness'])
				tempo.append(features[0]['tempo'])
				key.append(1)
				timeSignature.append(features[0]['time_signature'])

			data = {
				'popularity': popularity,
				'length':length,
				'danceability': danceability,
				'acousticness': acousticness,
				'energy': energy,
				'instrumentalness': instrumentalness,
				'liveness': liveness,
				'valence': valence,
				'loudness': loudness,
				'speechiness': speechiness,
				'tempo': tempo,
				# 'key':key,
				# 'time_signature': timeSignature,
			}

			return pd.DataFrame(data)

def main():
	w = WrapperClass()
	w.doAuth()
	current_track_id = None
	filename = MODEL_FILEPATH
	loaded_model = pickle.load(open(filename, 'rb'))

	while True:
		current_track_info = get_current_track(ACCESS_TOKEN)
		if current_track_id != None and current_track_info['id'] != current_track_id :
			pprint(
				current_track_info,
				indent=4,
			)


			audio_features = w.getFeatures(current_track_info['id'])
			print(audio_features)
			predictions = loaded_model.predict(audio_features)
			print("Prediction is Code:")
			print(predictions[0])
			print("Song Tempo Is:")
			print(audio_features['tempo'][0])

			data = {'mood' : predictions[0], 'tempo' : audio_features['tempo'][0]}
			try:
				requests.post(URL,data=data)
			except:
				print ("post request failed")


		
		current_track_id = current_track_info['id']
		time.sleep(1)


if __name__ == '__main__':
	main()