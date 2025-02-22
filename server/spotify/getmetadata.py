import requests
import pandas as pd
#import apitokenaccess

# 🔹 Your Spotify API Access Token
ACCESS_TOKEN = """BQCIlEdyuOhJlfdImjAW4NrAJpC5cYpUz-sGhc2-bAlMR22Qek5RKa5x2-UQRGE9d4zHRqDnmpUM2PkXSZY1Dj7ibv2ohnDci8aCI3aNU3g86915VZCNQK36ef-wIHxOZKajn3S-g75P40XdGKHFP2x"""

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
        print(f"Error fetching audio features for track_id {track_id}: {response.status_code}")
        print("Response:", response.text)
        return {}  # Return an empty dict on error

    data = response.json()
    # Check if the expected keys are present; if not, print a message for debugging
    if data == {}:
        print(f"No audio features found for track_id {track_id}")
        return {}
    return data

# 🔹 Fetch Songs & Audio Features
songs = get_playlist_tracks(PLAYLIST_ID, ACCESS_TOKEN)
print(songs)
if not songs:
    print("No songs were fetched. Please check your access token and playlist ID.")
    exit()

# 🔹 Add BPM & Other Data to Each Song
for song in songs:
    audio_features = get_audio_features(song["track_id"], ACCESS_TOKEN)
    print(audio_features)
    song["bpm"] = audio_features.get("tempo", None)
    song["danceability"] = audio_features.get("danceability", None)
    song["energy"] = audio_features.get("energy", None)

# 🔹 Save to CSV File
df = pd.DataFrame(songs)
df.to_csv("top_rap_songs.csv", index=False)

print("Data saved to top_rap_songs.csv")


"""curl -X POST "http://localhost:8888/callback" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "grant_type=client_credentials&client_id=your-client-id&client_secret=your-client-secret"
"""