import urllib.request
import os

REPO_BASE = "https://raw.githubusercontent.com/Indrajit1465/GPS-Route-Tracking/main/"

# (GitHub path, Local path)
FILES = [
    # Tracker templates — friend stores them at tracker/templates/ (no subdirectory)
    ("tracker/templates/home.html",     "tracker/templates/home.html"),
    ("tracker/templates/login.html",    "tracker/templates/login.html"),
    ("tracker/templates/register.html", "tracker/templates/register.html"),
    # Admin panel templates
    ("admin_panel/templates/admin_panel/dashboard.html",   "admin_panel/templates/admin_panel/dashboard.html"),
    ("admin_panel/templates/admin_panel/user_detail.html", "admin_panel/templates/admin_panel/user_detail.html"),
]

def main():
    print("=" * 60)
    print("  SYNCING TEMPLATES FROM FRIEND'S GITHUB REPO")
    print("  https://github.com/Indrajit1465/GPS-Route-Tracking")
    print("=" * 60)

    success = 0
    failed  = 0

    for github_path, local_path in FILES:
        url = REPO_BASE + github_path
        try:
            print(f"\n  Downloading: {github_path}")
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                content = response.read()

            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            with open(local_path, "wb") as f:
                f.write(content)

            print(f"  ✓ Saved to: {local_path} ({len(content)} bytes)")
            success += 1
        except Exception as e:
            print(f"  ✗ FAILED: {e}")
            failed += 1

    print("\n" + "=" * 60)
    print(f"  DONE: {success} succeeded, {failed} failed")
    print("=" * 60)
    print("\nNext steps:")
    print("  1. pip install django-ratelimit")
    print("  2. python manage.py makemigrations")
    print("  3. python manage.py migrate")
    print("  4. python manage.py runserver")

if __name__ == "__main__":
    main()
