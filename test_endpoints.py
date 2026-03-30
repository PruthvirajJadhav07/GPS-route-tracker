import requests

ORS_API_KEY = "eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6IjYxOGYzYzNjN2U3YjRlMDBiYmM3Y2VmNmYwYzg2YmNhIiwiaCI6Im11cm11cjY0In0="

coords = [
    [72.8777, 19.0760],
    [72.8778, 19.0761],
    [72.8779, 19.0762]
]

urls_to_test = [
    "https://api.openrouteservice.org/v2/match/driving-car",
    "https://api.openrouteservice.org/match/v2/driving-car",
    "https://api.openrouteservice.org/v2/match/driving-car/geojson",
    "https://api.openrouteservice.org/match/v1/driving-car",
    "https://api.openrouteservice.org/v2/matching/driving-car",
    "https://api.openrouteservice.org/matching/v2/driving-car"
]

for u in urls_to_test:
    r = requests.post(
        u,
        json={"coordinates": coords},
        headers={
            "Authorization": ORS_API_KEY,
            "Accept": "application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8",
            "Content-Type": "application/json; charset=utf-8"
        },
        timeout=10
    )
    if "404 Not Found" not in r.text and r.status_code != 404:
        print(f"SUCCESS or non-404: {u} -> {r.status_code}")
        if r.status_code == 200:
            print("Response length:", len(r.text))
            break
    else:
        print(f"Failed 404: {u}")
