import urllib.request
import os

repo_url = "https://raw.githubusercontent.com/Indrajit1465/GPS-Route-Tracking/main/"

files_to_sync = [
    # (GitHub path, Local path)
    ("tracker/templates/home.html", "tracker/templates/tracker/home.html"),
    ("tracker/templates/login.html", "tracker/templates/login.html"),
    ("tracker/templates/register.html", "tracker/templates/register.html"),
]

def main():
    print("Starting frontend template sync from Indrajit1465/GPS-Route-Tracking...")
    
    for github_path, local_path in files_to_sync:
        url = repo_url + github_path
        try:
            print(f"Fetch: {url} -> {local_path}")
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                content = response.read()
                
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            with open(local_path, "wb") as f:
                f.write(content)
                
            print(f"   SUCCESS: Saved {local_path}")
        except Exception as e:
            print(f"   ERROR: Could not download {github_path}. Reason: {e}")

    print("\n--- SYNC COMPLETE ---")
    print("Next steps:")
    print("1. Run: pip install -r requirements.txt (To fix the django_ratelimit error)")
    print("2. Run: python manage.py runserver")

if __name__ == "__main__":
    main()
