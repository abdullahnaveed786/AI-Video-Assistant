import yt_dlp
import os
import subprocess
import wave

DOWNLOAD_DIR = 'downloades'
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


def download_youtube_audio(url: str) -> str:
    """Download best audio from YouTube and convert to WAV (16kHz mono)."""
    output_template = os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s")
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_template,
        "quiet": True,
        "nocheckcertificate": True,
        "extractor_args": {
            "youtube": {
                "player_client": ["android", "web"]
            }
        }
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        downloaded = ydl.prepare_filename(info)

    # Convert downloaded file to WAV 16kHz mono
    wav_path = os.path.splitext(downloaded)[0] + "_converted.wav"
    _convert_to_wav_ffmpeg(downloaded, wav_path)
    return wav_path


def _convert_to_wav_ffmpeg(src_path: str, dst_path: str) -> None:
    # Prefer explicit binary from FFMPEG_BIN env var, then ./ffmpeg/ffmpeg.exe, else rely on PATH
    ffmpeg_env = os.getenv("FFMPEG_BIN", "")
    local_bin = os.path.join(os.getcwd(), "ffmpeg", "ffmpeg.exe")

    if ffmpeg_env and os.path.exists(ffmpeg_env):
        ffmpeg_cmd = ffmpeg_env
    elif os.path.exists(local_bin):
        ffmpeg_cmd = local_bin
    else:
        ffmpeg_cmd = "ffmpeg"

    cmd = [
        ffmpeg_cmd,
        "-y",
        "-i",
        src_path,
        "-ar",
        "16000",
        "-ac",
        "1",
        dst_path,
    ]

    subprocess.run(cmd, check=True)


def convert_to_wav(input_path: str) -> str:
    """Convert any audio/video file to WAV (16kHz mono) using ffmpeg."""
    output_path = os.path.splitext(input_path)[0] + "_converted.wav"
    _convert_to_wav_ffmpeg(input_path, output_path)
    return output_path


def chunk_audio(wav_path: str, chunk_minutes: int = 10) -> list:
    """Split a WAV file into multiple WAV chunks (by frames) without pydub.

    Returns a list of chunk file paths.
    """
    chunks = []
    with wave.open(wav_path, "rb") as wf:
        nchannels = wf.getnchannels()
        sampwidth = wf.getsampwidth()
        framerate = wf.getframerate()
        nframes = wf.getnframes()

        frames_per_chunk = chunk_minutes * 60 * framerate

        idx = 0
        for start in range(0, nframes, frames_per_chunk):
            wf.setpos(start)
            frames_to_read = min(frames_per_chunk, nframes - start)
            frames = wf.readframes(frames_to_read)

            chunk_path = f"{wav_path}_chunk_{idx}.wav"
            with wave.open(chunk_path, "wb") as out:
                out.setnchannels(nchannels)
                out.setsampwidth(sampwidth)
                out.setframerate(framerate)
                out.writeframes(frames)

            chunks.append(chunk_path)
            idx += 1

    return chunks


def process_input(source: str) -> list:
    if source.startswith("http://") or source.startswith("https://"):
        print("Detected YouTube URL. Downloading audio...")
        wav_path = download_youtube_audio(source)
    else:
        print("Detected local file. Converting to WAV...")
        wav_path = convert_to_wav(source)

    print("Chunking audio...")
    chunks = chunk_audio(wav_path)
    print(f"Audio ready — {len(chunks)} chunk(s) created.")
    return chunks


