from flask import Flask, jsonify
from dotenv import load_dotenv
import requests, os, base64

#  Carga variables del archivo .env automáticamente
load_dotenv()

app = Flask(__name__)

#  Lee las credenciales de Spotify desde el entorno (.env)
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

#  Ruta para obtener el token de Spotify
@app.route("/token", methods=["GET"])
def get_token():
    if not CLIENT_ID or not CLIENT_SECRET:
        return jsonify({"error": "Spotify credentials not set"}), 500

    auth_header = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()

    try:
        response = requests.post(
            "https://accounts.spotify.com/api/token",
            headers={
                "Authorization": f"Basic {auth_header}",
                "Content-Type": "application/x-www-form-urlencoded"
            },
            data={"grant_type": "client_credentials"}
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

    data = response.json()
    return jsonify({
        "access_token": data.get("access_token"),
        "expires_in": data.get("expires_in")
    })

if __name__ == "__main__":
    app.run(debug=True)