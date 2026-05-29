import os
import re
import datetime
import subprocess
import random
from pathlib import Path
from urllib.parse import quote
import requests
import time

# ---------------- CONFIG ----------------

# LANGUAGE SETTINGS (Change this for different languages)
LANGUAGE_CONFIG = {
    "name": "Polish",          # Language name for prompts
    "native_name": "polsku",   # Native name (e.g., "po polsku") for instructions
    "voice": "pl-PL-ZofiaNeural", # Edge-TTS voice
    "vosk_model": "vosk-model-small-pl-0.22",
    "vosk_url": "https://alphacephei.com/vosk/models/vosk-model-small-pl-0.22.zip",
    "vosk_zip": "vosk-model-pl.zip",
    "subtitle_font": "Comic Sans MS"
}

# For German, you would just change to:
# LANGUAGE_CONFIG = {
#     "name": "German",
#     "native_name": "auf Deutsch",
#     "voice": "de-DE-KatjaNeural",
#     "vosk_model": "vosk-model-small-de-0.15", 
#     ...
# }

NUM_IMAGES = 8  # 8 unique scenes (faster generation)
IMAGE_WIDTH = 1080
IMAGE_HEIGHT = 1920
IMAGE_MODEL = "flux"

STORY_MAX_WORDS = 130

TOPICS_FILE = "topics.txt"

IMAGES_DIR = Path("images")
OUTPUT_DIR = Path("output")
AUDIO_DIR = Path("audio")

MUSIC_FILE = AUDIO_DIR / "music.mp3"

NARRATION_FILE = OUTPUT_DIR / "narration.mp3"
STORY_FILE = OUTPUT_DIR / "story.txt"
SCENES_FILE = OUTPUT_DIR / "scenes.txt"
SUBS_FILE = OUTPUT_DIR / "subtitles.ass"
ANIMATED_VIDEO = OUTPUT_DIR / "animated.mp4"
VIDEO_WITH_SUBS = OUTPUT_DIR / "video_with_subs.mp4"
FINAL_VIDEO = OUTPUT_DIR / "final_video.mp4"

WHISPER_MODEL_NAME = "small"

# ----------------------------------------

def ensure_dirs():
    IMAGES_DIR.mkdir(exist_ok=True)
    OUTPUT_DIR.mkdir(exist_ok=True)
    AUDIO_DIR.mkdir(exist_ok=True)
    
    # Clean old images
    for f in IMAGES_DIR.glob("*.jpg"):
        f.unlink()
        
    # Clean old output files to prevent staying state
    for f in OUTPUT_DIR.glob("*"):
        if f.is_file() and f.name != ".gitkeep":
            try:
                f.unlink()
            except Exception:
                pass

def choose_topic_for_today():
    if not os.path.exists(TOPICS_FILE):
        print(f"[topics] {TOPICS_FILE} not found!")
        return "Cute Animal Adventure"

    with open(TOPICS_FILE, "r", encoding="utf-8") as f:
        topics = [line.strip() for line in f if line.strip()]
    if not topics:
        print("[topics] No topics found! Using fallback.")
        return "Mały miś w lesie"
    
    # Select from the top 5 topics randomly for variety
    # (In case the push fails, we don't always get the exact same one)
    sample_size = min(len(topics), 5)
    selected_index = random.randint(0, sample_size - 1)
    selected_topic = topics.pop(selected_index)
    
    # 2. Save to used topics history
    with open("used_topics.txt", "a", encoding="utf-8") as f:
        f.write(f"{datetime.datetime.now().strftime('%Y-%m-%d')} - {selected_topic}\n")
    
    # 3. Remove from topics.txt
    with open(TOPICS_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(topics) + "\n")
    
    print(f"[topics] Selected and consumed topic: {selected_topic}")
    return selected_topic

def generate_story_with_pollinations(topic: str) -> str:
    """Generate a short children's story in the target language using paid Pollinations API."""
    api_key = os.getenv("POLLINATIONS_API_KEY")
    if not api_key:
        raise ValueError("POLLINATIONS_API_KEY is missing! Paid API access is required for story generation.")

    lang_name = LANGUAGE_CONFIG["name"]
    
    system = (
        f"You are a creative writer specializing in children's stories in {lang_name} language. "
        f"Write a short, interesting children's story (3-8 years old) in {lang_name} about the given topic. "
        f"Keep the story to 80-130 words. Use simple, engaging language appropriate for young children. "
        f"Focus on the specific topic provided. "
        f"Include no title, just the story content."
    )
    prompt = f"Topic: {topic}. Write a wonderful children's story about this topic in {lang_name} language."

    url = f"https://gen.pollinations.ai/text/{quote(prompt)}"
    headers = {"Authorization": f"Bearer {api_key}"}
    params = {
        "model": "openai", # High quality text model for stories
        "temperature": 1.0,
        "system": system,
        "json": False
    }

    print(f"[story] Generating {lang_name} story for topic: {topic} (Paid API)")
    try:
        # Add random seed for variety
        params["seed"] = random.randint(1, 1000000)
        
        r = requests.get(url, headers=headers, params=params, timeout=60)
        r.raise_for_status()
        text = r.text.strip()
    except Exception as e:
        print(f"[story] Error with Paid API: {e}")
        raise e

    words = text.split()
    if len(words) > STORY_MAX_WORDS:
        text = " ".join(words[:STORY_MAX_WORDS])

    with open(STORY_FILE, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"[story] {lang_name} story generated ({len(text.split())} words)")
    return text

def generate_visual_prompts(story: str) -> list:
    """Generate 8 distinct ENGLISH visual descriptions from the story using Paid API."""
    print(f"[scenes] Generowanie opisów wizualnych po angielsku (Paid API)...")
    
    api_key = os.getenv("POLLINATIONS_API_KEY")
    lang_name = LANGUAGE_CONFIG["name"]
    
    system = (
        f"You are an expert at creating image prompts for 3D animations. "
        f"Read this {lang_name} story and generate exactly {NUM_IMAGES} distinct, detailed visual image descriptions in ENGLISH. "
        f"Focus on character expressions, cute animals, and beautiful backgrounds. "
        f"Styling: Pixar/Disney 3D animation. "
        f"Output ONLY the descriptions, one per line. No numbering, no extra text."
    )
    
    prompt = f"Story: {story}\n\nGenerate {NUM_IMAGES} detailed visual descriptions for images in English."
    
    url = f"https://gen.pollinations.ai/text/{quote(prompt)}"
    headers = {"Authorization": f"Bearer {api_key}"}
    params = {
        "model": "openai",
        "system": system,
        "seed": random.randint(1, 1000),
        "json": False
    }
    
    try:
        r = requests.get(url, headers=headers, params=params, timeout=60)
        r.raise_for_status()
        text = r.text.strip()
        
        # Clean up lines
        lines = [line.strip().lstrip('0123456789.- ') for line in text.split('\n') if line.strip()]
        
        # Ensure we have enough scenes
        if len(lines) < NUM_IMAGES:
            while len(lines) < NUM_IMAGES:
                lines.append(lines[-1] if lines else "Cute animal in magical forest")
        
        scenes = lines[:NUM_IMAGES]
        
    except Exception as e:
        print(f"[scenes] Error generating prompts with Paid API: {e}")
        scenes = ["Cute animal character in forest, high detail 3D"] * NUM_IMAGES

    # Save scenes
    with open(SCENES_FILE, "w", encoding="utf-8") as f:
        for i, scene in enumerate(scenes):
            f.write(f"{i+1}. {scene}\n")
    
    print(f"[scenes] Created {len(scenes)} visual descriptions")
    return scenes

def generate_image(scene: str, idx: int) -> Path:
    """Generate high-quality 3D animated animal image for each scene using Pollinations AI."""
    # Create unique seed for each image based on scene content + index
    seed = hash(scene + str(idx)) % 1000000
    
    # Build detailed, high-quality prompt for 3D animated kids content
    prompt = (
        f"Masterpiece, professional 3D render, Pixar style animation, Disney quality, {scene}, "
        f"hyper-detailed character design, cute adorable animals with expressive eyes, "
        f"vibrant cinematography, cinematic lighting, magical colorful environment, "
        f"octane render, 8k resolution, extreme detail, soft studio light, "
        f"perfect anatomy, no deformations, no warped limbs, no extra fingers, "
        f"no distorted faces, clear sharp focus, extremely cute, high quality textures, "
        f"magical atmosphere, child-friendly world"
    )
    safe_prompt = quote(prompt)
    
    api_key = os.getenv("POLLINATIONS_API_KEY")
    if not api_key:
        raise ValueError("POLLINATIONS_API_KEY is missing! Paid API access is required for image generation.")
        
    url = f"https://gen.pollinations.ai/image/{safe_prompt}"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    params = {
        "width": IMAGE_WIDTH,
        "height": IMAGE_HEIGHT,
        "model": IMAGE_MODEL,
        "seed": seed,
        "nologo": "true"
    }

    out = IMAGES_DIR / f"scene_{idx:02d}.jpg"
    print(f"[image] Generowanie obrazu 3D {idx+1}/{NUM_IMAGES} (Flux Paid): {scene[:50]}...")
    
    
    # Retry logic with exponential backoff (longer waits for rate limits)
    max_retries = 5
    for attempt in range(max_retries):
        try:
            # Use params for query string
            r = requests.get(url, headers=headers, params=params, timeout=180)
            r.raise_for_status()
            out.write_bytes(r.content)
            time.sleep(2)  # Small delay between successful requests
            return out
        except requests.exceptions.HTTPError as e:
            # Handle 429 rate limits with much longer waits
            if e.response.status_code == 429:
                wait_time = (attempt + 1) * 20  # 20, 40, 60, 80, 100 seconds
                if attempt < max_retries - 1:
                    print(f"[image] Rate limited! Retry {attempt+1}/{max_retries} (waiting {wait_time}s)")
                    time.sleep(wait_time)
                else:
                    print(f"[image] Failed to generate image {idx+1}: Rate limit exceeded")
                    raise e
            else:
                wait_time = (attempt + 1) * 5
                if attempt < max_retries - 1:
                    print(f"[image] HTTP {e.response.status_code}. Retry {attempt+1}/{max_retries} (waiting {wait_time}s)")
                    time.sleep(wait_time)
                else:
                    print(f"[image] Failed to generate image {idx+1}: {e}")
                    raise e
        except Exception as e:
            wait_time = (attempt + 1) * 5
            if attempt < max_retries - 1:
                print(f"[image] Retry {attempt+1}/{max_retries} (waiting {wait_time}s)")
                time.sleep(wait_time)
            else:
                print(f"[image] Failed to generate image {idx+1}: {e}")
                raise e
    return out

def generate_images(scenes: list):
    """Generate unique 3D animated images for each scene SEQUENTIALLY (avoids rate limits)"""
    print(f"[image] Generowanie {NUM_IMAGES} obrazów 3D sekwencyjnie (unikanie limitów)...")
    return [generate_image(scene, i) for i, scene in enumerate(scenes)]

def generate_tts(story: str):
    """Generate narration using edge-tts (free Microsoft TTS)."""
    import asyncio
    try:
        import edge_tts
    except ImportError:
        subprocess.run(["pip", "install", "edge-tts"], check=True)
        import edge_tts
    
    lang_name = LANGUAGE_CONFIG["name"]
    voice = LANGUAGE_CONFIG["voice"]
    print(f"[tts] Generowanie narracji ({lang_name}) z edge-tts...")
    
    async def generate():
        communicate = edge_tts.Communicate(story, voice)
        await communicate.save(str(NARRATION_FILE))
    
    asyncio.run(generate())
    print(f"[tts] Narration saved to {NARRATION_FILE}")

def generate_word_subtitles():
    """Generate WORD-BY-WORD subtitles using Vosk (lightweight!)."""
    print("[subs] Generowanie napisów słowo po słowie z Vosk...")
    
    import json
    import wave
    from vosk import Model, KaldiRecognizer
    import os
    
    # Download Vosk model if not exists
    model_name = LANGUAGE_CONFIG["vosk_model"]
    model_url = LANGUAGE_CONFIG["vosk_url"]
    zip_path = LANGUAGE_CONFIG["vosk_zip"]
    
    if not os.path.exists(model_name):
        print(f"[subs] Pobieranie modelu Vosk ({model_name})...")
        import urllib.request
        import zipfile
        
        urllib.request.urlretrieve(model_url, zip_path)
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(".")
        
        os.remove(zip_path)
        print("[subs] Model downloaded!")
    
    # Convert MP3 to WAV for Vosk
    wav_file = "output/narration.wav"
    os.system(f'ffmpeg -y -i {NARRATION_FILE} -ar 16000 -ac 1 {wav_file}')
    
    # Load Vosk model
    model = Model(model_name)
    
    # Open WAV file
    wf = wave.open(wav_file, "rb")
    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)  # Enable word-level timestamps
    
    # Process audio
    words = []
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            if 'result' in result:
                for word_info in result['result']:
                    words.append({
                        'word': word_info['word'].upper(),
                        'start': word_info['start'],
                        'end': word_info['end']
                    })
    
    # Final result
    final_result = json.loads(rec.FinalResult())
    if 'result' in final_result:
        for word_info in final_result['result']:
            words.append({
                'word': word_info['word'].upper(),
                'start': word_info['start'],
                'end': word_info['end']
            })
    
    font_name = LANGUAGE_CONFIG.get("subtitle_font", "Arial")
    
    # Create ASS subtitle file with kid-friendly styling
    ass_content = f"""[Script Info]
Title: Bajka dla Dzieci
ScriptType: v4.00+

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,{font_name},20,&H00FFFF00,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,3,2,5,10,10,60,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    
    for word in words:
        start = word['start']
        end = word['end']
        text = word['word']
        
        start_time = f"{int(start//3600)}:{int((start%3600)//60):02d}:{start%60:.2f}"
        end_time = f"{int(end//3600)}:{int((end%3600)//60):02d}:{end%60:.2f}"
        
        ass_content += f"Dialogue: 0,{start_time},{end_time},Default,,0,0,0,,{text}\n"
    
    # Save ASS file
    with open(SUBS_FILE, "w", encoding="utf-8") as f:
        f.write(ass_content)
    
    print(f"[subs] Napisy zapisane ({len(words)} słów)")

def get_audio_duration(audio_file):
    """Get duration of audio file using ffprobe."""
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(audio_file)
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return float(result.stdout.strip())

def create_animated_slideshow(image_paths):
    """Create animated slideshow with Ken Burns zoom effect."""
    print("[video] Creating animated slideshow with Ken Burns effect...")
    
    # Get audio duration to match video length
    duration = get_audio_duration(NARRATION_FILE)
    per_image = duration / len(image_paths)
    
    # Create individual animated clips with zoom effect
    clips = []
    for i, img_path in enumerate(image_paths):
        clip_file = OUTPUT_DIR / f"clip_{i:02d}.mp4"
        clips.append(clip_file)
        
        # Calculate frames (30 fps)
        frames = max(int(per_image * 30), 60)
        
        # Alternate between zoom in and zoom out for variety
        if i % 2 == 0:
            # Zoom in effect
            zoom_start = 1.0
            zoom_end = 1.3
        else:
            # Zoom out effect  
            zoom_start = 1.3
            zoom_end = 1.0
        
        # Simple zoom with scale filter (more reliable on Windows)
        cmd = [
            "ffmpeg", "-y",
            "-loop", "1",
            "-i", str(img_path),
            "-vf", (
                f"scale=8000:-1,"
                f"zoompan=z='if(lte(on,1),{zoom_start},{zoom_start}+(({zoom_end}-{zoom_start})/{frames})*on)':"
                f"d={frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={IMAGE_WIDTH}x{IMAGE_HEIGHT}:fps=30"
            ),
            "-t", str(per_image),
            "-c:v", "libx264",
            "-preset", "slow",  # Better quality
            "-crf", "18",  # High quality (lower = better, 18-23 is good)
            "-pix_fmt", "yuv420p",
            str(clip_file)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"[video] Zoom failed for clip {i+1}, using fallback...")
            # Fallback: simple static with slight movement
            cmd_fallback = [
                "ffmpeg", "-y",
                "-loop", "1",
                "-i", str(img_path),
                "-vf", f"scale={IMAGE_WIDTH}:{IMAGE_HEIGHT}:force_original_aspect_ratio=increase,crop={IMAGE_WIDTH}:{IMAGE_HEIGHT},fps=30",
                "-t", str(per_image),
                "-c:v", "libx264",
                "-pix_fmt", "yuv420p",
                str(clip_file)
            ]
            subprocess.run(cmd_fallback, check=True, capture_output=True)
        
        print(f"[video] Animated clip {i+1}/{len(image_paths)}")
    
    # Create concat list
    concat_file = OUTPUT_DIR / "concat.txt"
    with open(concat_file, "w") as f:
        for clip in clips:
            f.write(f"file '{clip.resolve()}'\n")
    
    # Concatenate all clips
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_file),
        "-c", "copy",
        str(ANIMATED_VIDEO)
    ]
    subprocess.run(cmd, check=True)
    print(f"[video] Animated slideshow saved to {ANIMATED_VIDEO}")
    
    # Cleanup individual clips
    for clip in clips:
        if clip.exists():
            clip.unlink()

def add_subtitles():
    """Overlay ASS subtitles on video."""
    print("[video] Adding UPPERCASE subtitles...")
    
    # Windows path needs special handling for FFmpeg filter
    subs_path = str(SUBS_FILE.resolve()).replace("\\", "/").replace(":", "\\:")
    
    cmd = [
        "ffmpeg", "-y",
        "-i", str(ANIMATED_VIDEO),
        "-vf", f"ass='{subs_path}'",
        "-c:v", "libx264",
        "-preset", "slow",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        str(VIDEO_WITH_SUBS)
    ]
    subprocess.run(cmd, check=True)
    print(f"[video] Video with subtitles saved to {VIDEO_WITH_SUBS}")

def merge_audio():
    """Merge video with narration and background music."""
    print("[merge] Merging audio with background music...")
    
    if MUSIC_FILE.exists():
        # Merge narration + background music (music at lower volume)
        cmd = [
            "ffmpeg", "-y",
            "-i", str(VIDEO_WITH_SUBS),
            "-i", str(NARRATION_FILE),
            "-i", str(MUSIC_FILE),
            "-filter_complex", "[2:a]volume=0.25[bg];[1:a][bg]amix=inputs=2:duration=first[a]",
            "-map", "0:v",
            "-map", "[a]",
            "-shortest",
            "-c:v", "copy",
            str(FINAL_VIDEO)
        ]
    else:
        print("[merge] No music.mp3 found, using narration only")
        cmd = [
            "ffmpeg", "-y",
            "-i", str(VIDEO_WITH_SUBS),
            "-i", str(NARRATION_FILE),
            "-map", "0:v",
            "-map", "1:a",
            "-shortest",
            "-c:v", "copy",
            str(FINAL_VIDEO)
        ]
    
    subprocess.run(cmd, check=True)
    print(f"[merge] Final video saved to {FINAL_VIDEO}")

def main():
    ensure_dirs()

    topic = choose_topic_for_today()
    print("=" * 60)
    print(f"=== Topic: {topic}")
    print("=" * 60)

    # 1. Generate story with Pollinations AI
    story = generate_story_with_pollinations(topic)
    
    # 2. Generate detailed ENGLISH visual prompts from the story
    scenes = generate_visual_prompts(story)
    
    # 3. Generate unique images for each scene
    images = generate_images(scenes)

    # 4. Generate narration with TTS
    generate_tts(story)
    
    # 5. Generate word-level UPPERCASE subtitles with Whisper
    generate_word_subtitles()
    
    # 6. Create animated slideshow with Ken Burns effect
    create_animated_slideshow(images)
    
    # 7. Add subtitles overlay
    add_subtitles()
    
    # 8. Merge audio (narration + background music)
    merge_audio()

    print("=" * 60)
    print(f"✅ DONE. Video ready: {FINAL_VIDEO}")
    print("=" * 60)

if __name__ == "__main__":
    main()
