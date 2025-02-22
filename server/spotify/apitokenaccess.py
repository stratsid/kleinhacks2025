import requests
import base64
import webbrowser


def make_token(token):
    return token
# 🔹 Your Spotify API credentials
CLIENT_ID = "318a9e6a85d54db1953715890bf639a2"
CLIENT_SECRET = "116d22c6d7d0421bb88199d4fc597dde"
REDIRECT_URI = "http://localhost:8888/callback"
SCOPES = "user-top-read user-read-recently-played"

# 🔹 Step 1: Redirect user to login
AUTH_URL = f"https://accounts.spotify.com/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope={SCOPES}"
print("Open this URL in your browser and log in:", AUTH_URL)
webbrowser.open(AUTH_URL)

# 🔹 Step 2: Paste the authorization code from the redirected URL
code = input("Paste the authorization code here: ").strip()

# 🔹 Step 3: Exchange the authorization code for an access token
def get_access_token(auth_code):
    auth_bytes = f"{CLIENT_ID}:{CLIENT_SECRET}".encode("utf-8")
    auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")

    headers = {"Authorization": f"Basic {auth_base64}", "Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": REDIRECT_URI,
    }
    response = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=data)
    
    if response.status_code != 200:
        print("Error fetching access token:", response.json())
        return None

    return response.json()["access_token"]

access_token = get_access_token(code)
print("✅ User Access Token:", access_token)
def make_token():
    if access_token:
        #print("✅ User Access Token:", access_token)
        return access_token




'''curl --request GET ^
  --url https://api.spotify.com/v1/audio-features/11dFghVXANMlKmJXsNCbNl ^
  --header "Authorization: Bearer BQD8o8ROVqxum5hEa-u1bwpNDw61KGMJDVVabfLnQg2OhhKaX4Ba4JnB2D_210NHcjXcWCj1TpBXieFIZEBikHulLSHw8ZuF38zohmbapsRSkzhLoW5RS
F_5lsRyGXNeDDsj7kd7DV2fOV292vRggK-PdBfKRTEyrjKStomvQCCn93Pj-QO8cUQ2_D4DsVuu3FIHZmDih5kUM2QRdY-2e6S5rfSfOc-SzwruPsSdnAVxwPDO"
'''