"""
Multi-Platform Upload Script

Uploads videos to:
- YouTube Shorts
- Instagram Reels
- TikTok
- Facebook Reels

Each platform requires its own API credentials.
"""

import os
from pathlib import Path
import datetime

# Import platform-specific uploaders
from upload_to_youtube import upload_to_youtube
from upload_instagram import upload_to_instagram
from upload_tiktok import upload_to_tiktok
from upload_facebook import upload_to_facebook
from upload_threads import upload_to_threads
from upload_twitter import upload_to_twitter
from upload_vk import upload_to_vk

def main():
    """Upload video to all configured platforms with enhanced error handling."""
    print("\n" + "="*80)
    print("🚀 MULTI-PLATFORM UPLOAD STARTING")
    print("="*80)

    video_file = Path('output/final_video.mp4')

    if not video_file.exists():
        print("[upload] ❌ No video found at output/final_video.mp4")
        print("="*80)
        return

    file_size_mb = video_file.stat().st_size / (1024 * 1024)
    print(f"[upload] ✅ Video file found: {video_file}")
    print(f"[upload] Video size: {file_size_mb:.2f} MB")

    # Read topic from used_topics.txt (unique each run)
    title = "Psychologia i rozwój osobisty"
    if os.path.exists("used_topics.txt"):
        with open("used_topics.txt", "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
            if lines:
                last_line = lines[-1]
                # Remove date prefix if present (format: "YYYY-MM-DD: Topic")
                if ": " in last_line:
                    title = last_line.split(": ", 1)[1]
                elif " - " in last_line:
                    title = last_line.split(" - ", 1)[1]
                else:
                    title = last_line

    # Read content text for description
    story_text = ""
    story_file = Path('output/story.txt')
    if story_file.exists():
        story_text = story_file.read_text(encoding='utf-8')

    # Platform-specific content
    descriptions = {
        'youtube': f"{title}\n\n{story_text}\n\n#Psychologia #RozwójOsobisty #SelfHelp #Shorts",
        'instagram': f"{title}\n\n{story_text}\n\n#Psychologia #RozwójOsobisty #SelfHelp #Shorts",
        'tiktok': f"{title}\n\n{story_text}\n\n#Psychologia #RozwójOsobisty #SelfHelp",
        'facebook': f"{title}\n\n{story_text}\n\n#Psychologia #RozwójOsobisty #SelfHelp",
        'threads': f"{title}\n\n{story_text}\n\n#Psychologia #RozwójOsobisty #SelfHelp",
        'twitter': f"{title}\n\n{story_text}\n\n#Psychologia #RozwójOsobisty #SelfHelp",
        'vk': f"{title}\n\n{story_text}\n\n#Psychologia #RozwójOsobisty #SelfHelp"
    }

    tags = [
        'Psychologia', 'Rozwój osobisty', 'Self Help', 'Polska',
        'Shorts', 'Mindfulness', 'Psychologia pozytywna', 'Polish',
        'Emocje', 'Relacje', 'Motywacja'
    ]

    results = {}
    
    # Upload to YouTube
    if all([
        os.getenv('YT_CLIENT_ID'),
        os.getenv('YT_CLIENT_SECRET'),
        os.getenv('YT_REFRESH_TOKEN')
    ]):
        print("\n" + "="*60)
        print("📺 UPLOADING TO YOUTUBE...")
        print("="*60)
        try:
            result = upload_to_youtube(video_file, title, descriptions['youtube'], tags)
            results['youtube'] = result
            print(f"✅ YouTube: https://youtube.com/shorts/{result['id']}")
        except Exception as e:
            print(f"❌ YouTube failed: {e}")
            results['youtube'] = {'error': str(e)}
    else:
        print("⏭️  Skipping YouTube (credentials not set)")
    
    # Upload to Instagram
    if all([
        os.getenv('IG_ACCESS_TOKEN'),
        os.getenv('IG_USER_ID')
    ]):
        print("\n" + "="*60)
        print("📸 UPLOADING TO INSTAGRAM...")
        print("="*60)
        try:
            result = upload_to_instagram(str(video_file), descriptions['instagram'])
            results['instagram'] = result
            print(f"✅ Instagram: Media ID {result.get('id', 'unknown')}")
        except Exception as e:
            print(f"❌ Instagram failed: {e}")
            results['instagram'] = {'error': str(e)}
    else:
        print("⏭️  Skipping Instagram (credentials not set)")
    
    # Upload to TikTok
    if os.getenv('TIKTOK_ACCESS_TOKEN'):
        print("\n" + "="*60)
        print("🎵 UPLOADING TO TIKTOK...")
        print("="*60)
        try:
            result = upload_to_tiktok(video_file, title, descriptions['tiktok'])
            results['tiktok'] = result
            print(f"✅ TikTok: Video ID {result.get('id', 'unknown')}")
        except Exception as e:
            print(f"❌ TikTok failed: {e}")
            results['tiktok'] = {'error': str(e)}
    else:
        print("⏭️  Skipping TikTok (credentials not set)")
    
    # Upload to Facebook
    if all([
        os.getenv('FB_ACCESS_TOKEN'),
        os.getenv('FB_PAGE_ID')
    ]):
        print("\n" + "="*60)
        print("📘 UPLOADING TO FACEBOOK...")
        print("="*60)
        try:
            result = upload_to_facebook(video_file, descriptions['facebook'])
            results['facebook'] = result
            print(f"✅ Facebook: Post ID {result.get('id', 'unknown')}")
        except Exception as e:
            print(f"❌ Facebook failed: {e}")
            results['facebook'] = {'error': str(e)}
    else:
        print("⏭️  Skipping Facebook (credentials not set)")
    
    # Upload to Threads
    if all([
        os.getenv('THREADS_ACCESS_TOKEN'),
        os.getenv('THREADS_USER_ID')
    ]):
        print("\n" + "="*60)
        print("🧵 UPLOADING TO THREADS...")
        print("="*60)
        try:
            result = upload_to_threads(str(video_file), descriptions['threads'])
            results['threads'] = result
            print(f"✅ Threads: Thread ID {result.get('id', 'unknown')}")
        except Exception as e:
            print(f"❌ Threads failed: {e}")
            results['threads'] = {'error': str(e)}
    else:
        print("⏭️  Skipping Threads (credentials not set)")
    
    # Upload to Twitter/X
    if all([
        os.getenv('TWITTER_API_KEY'),
        os.getenv('TWITTER_API_SECRET'),
        os.getenv('TWITTER_ACCESS_TOKEN'),
        os.getenv('TWITTER_ACCESS_SECRET')
    ]):
        print("\n" + "="*60)
        print("🐦 UPLOADING TO TWITTER/X...")
        print("="*60)
        try:
            result = upload_to_twitter(video_file, descriptions['twitter'])
            results['twitter'] = result
            print(f"✅ Twitter: Tweet ID {result.get('id', 'unknown')}")
        except Exception as e:
            print(f"❌ Twitter failed: {e}")
            results['twitter'] = {'error': str(e)}
    else:
        print("⏭️  Skipping Twitter (credentials not set)")
    
    # Upload to VK
    if all([
        os.getenv('VK_ACCESS_TOKEN'),
        os.getenv('VK_GROUP_ID')
    ]):
        print("\n" + "="*60)
        print("🇷🇺 UPLOADING TO VK...")
        print("="*60)
        try:
            result = upload_to_vk(str(video_file), descriptions['vk'], title)
            results['vk'] = result
            print(f"✅ VK: Post ID {result.get('post_id', 'unknown')}")
        except Exception as e:
            print(f"❌ VK failed: {e}")
            results['vk'] = {'error': str(e)}
    else:
        print("⏭️  Skipping VK (credentials not set)")
    
    # Detailed Summary
    print("\n" + "="*80)
    print("📊 MULTI-PLATFORM UPLOAD SUMMARY")
    print("="*80)

    success_count = 0
    total_count = len(results)

    for platform, result in results.items():
        if result and 'error' not in result:
            status = "✅ SUCCESS"
            success_count += 1
            if platform == 'youtube' and result.get('id'):
                print(f"{platform.capitalize():<12}: {status} - https://youtube.com/shorts/{result['id']}")
            else:
                post_id = result.get('id', 'unknown')
                print(f"{platform.capitalize():<12}: {status} - ID: {post_id}")
        else:
            status = "❌ FAILED"
            error_msg = result.get('error', 'Unknown error') if result else 'Not attempted'
            print(f"{platform.capitalize():<12}: {status} - {error_msg}")

    print("="*80)
    print(f"📈 Success Rate: {success_count}/{total_count} platforms")
    print("="*80)

    if success_count > 0:
        print("🎉 Multi-platform upload completed!")
        print("Check your social media accounts to see the published content.")
    else:
        print("⚠️  No platforms were successfully uploaded to.")
        print("Check your API credentials and try again.")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\n[upload] ❌ Upload pipeline error: {e}")
        print("[upload] Continuing gracefully...")
