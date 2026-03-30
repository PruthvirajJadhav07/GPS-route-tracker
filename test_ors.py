import requests
import json

ORS_API_KEY = "eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6IjYxOGYzYzNjN2U3YjRlMDBiYmM3Y2VmNmYwYzg2YmNhIiwiaCI6Im11cm11cjY0In0="

def test_match():
    # A few points in India (since the map centers at 20.5937, 78.9629, let's use some points)
    # Actually just a standard straight line segment that would be recorded
    coords = [
        [72.8777, 19.0760],
        [72.8778, 19.0761],
        [72.8779, 19.0762],
        [72.8780, 19.0763],
        [72.8781, 19.0764],
        [72.8782, 19.0765]
    ]

    url = "https://api.openrouteservice.org/match/v2/driving-car"
    body = {
        "coordinates": coords,
        "radiuses": [25] * len(coords)
    }

    print("Sending request...")
    r = requests.post(
        url,
        json=body,
        headers={
            "Authorization": ORS_API_KEY,
            "Accept": "application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8",
            "Content-Type": "application/json; charset=utf-8"
        },
        timeout=20
    )

    print("Status:", r.status_code)
    print("Response:", r.text)

if __name__ == "__main__":
    test_match()
