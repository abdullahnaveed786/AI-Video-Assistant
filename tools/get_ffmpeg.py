import os
import sys
import urllib.request
import zipfile
import tempfile

URL = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
OUT_DIR = os.path.join(os.getcwd(), "ffmpeg")
ZIP_PATH = os.path.join(tempfile.gettempdir(), "ffmpeg_release_essentials.zip")

os.makedirs(OUT_DIR, exist_ok=True)

print(f"Downloading FFmpeg from {URL} to {ZIP_PATH} ...")
urllib.request.urlretrieve(URL, ZIP_PATH)
print("Download complete. Extracting...")

with zipfile.ZipFile(ZIP_PATH, 'r') as z:
    z.extractall(path=os.path.join(tempfile.gettempdir(), "ffmpeg_extracted"))

# Find ffmpeg.exe
ffmpeg_exe = None
for root, dirs, files in os.walk(os.path.join(tempfile.gettempdir(), "ffmpeg_extracted")):
    for f in files:
        if f.lower() == 'ffmpeg.exe':
            ffmpeg_exe = os.path.join(root, f)
            break
    if ffmpeg_exe:
        break

if not ffmpeg_exe:
    print("Error: ffmpeg.exe not found in archive.")
    sys.exit(2)

dst = os.path.join(OUT_DIR, 'ffmpeg.exe')
print(f"Copying {ffmpeg_exe} to {dst} ...")
import shutil
shutil.copy(ffmpeg_exe, dst)
print(f"FFmpeg ready at {dst}")
os.remove(ZIP_PATH)
print("Cleanup done.")
print("Done")
