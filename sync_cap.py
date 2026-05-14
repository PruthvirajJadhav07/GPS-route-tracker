import os
import shutil

def sync_capacitor():
    print("🚀 Starting manual Capacitor Sync...")
    
    # Paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    src_www = os.path.join(base_dir, 'frontend', 'www')
    dest_public = os.path.join(base_dir, 'android', 'app', 'src', 'main', 'assets', 'public')
    
    src_config = os.path.join(base_dir, 'capacitor.config.json')
    dest_config = os.path.join(base_dir, 'android', 'app', 'src', 'main', 'assets', 'capacitor.config.json')

    # 1. Sync WWW files
    if os.path.exists(dest_public):
        shutil.rmtree(dest_public)
    shutil.copytree(src_www, dest_public)
    print("✅ Copied frontend web assets to Android folder.")

    # 2. Sync Config
    if os.path.exists(src_config):
        shutil.copy2(src_config, dest_config)
        print("✅ Synced capacitor.config.json")

    print("🎉 Sync completed successfully! You can now run the app in Android Studio.")

if __name__ == "__main__":
    sync_capacitor()
