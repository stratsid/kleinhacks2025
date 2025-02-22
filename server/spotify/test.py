#6AI3ezQ4o3HUoP6Dhudph3
import requests
import pandas as pd
import apitokenaccess

# 🔹 Your Spotify API Access Token
ACCESS_TOKEN = apitokenaccess.access_token

# 🔹 Spotify Playlist ID (RapCaviar or any playlist you prefer)
PLAYLIST_ID = "18EmXIwVHNGJPLuTvPKeBG"  # Example playlist

# 🔹 Get Playlist Tracks
def get_playlist_tracks(playlist_id, access_token):
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    data = response.json()

    # Debug: Check if the expected data is returned
    if "items" not in data:
        print("Error: 'items' key not found in the playlist response.")
        print("Response:", data)
        return []
    
    tracks = []
    for item in data["items"]:
        track = item.get("track", {})
        # Skip local tracks (they don't have audio features)
        if track.get("is_local"):
            print(f"Skipping local track: {track.get('name')}")
            continue
        song_name = track.get("name", "Unknown")
        artist_name = track.get("artists", [{}])[0].get("name", "Unknown")
        track_id = track.get("id")
        if track_id:
            tracks.append({
                "title": song_name, 
                "artist": artist_name, 
                "track_id": track_id
            })
    return tracks

# 🔹 Get Audio Features (BPM, danceability, energy, etc.)
def get_audio_features(track_id, access_token):
    url = f"https://api.spotify.com/v1/audio-features/{track_id}"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        #print(f"Error fetching audio features for track_id {track_id}: {response.status_code}")
        #print("Response:", response.text)
        return {}  # Return an empty dict on error

    data = response.json()
    # Check if the expected keys are present; if not, print a message for debugging
    if not data:
        print(f"No audio features found for track_id {track_id}")
        return {}
    return data

# 🔹 Fetch Songs & Audio Features
print(get_audio_features("11dFghVXANMlKmJXsNCbNl", ACCESS_TOKEN))
