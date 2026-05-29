"""
Facebook Reels Upload - Enhanced Version
Uploads video to tmpfiles.org, then uses URL for Facebook Graph API
"""

import os
import requests
import time
from pathlib import Path

def upload_to_facebook(video_path, description):
    """
    Upload video to Facebook Reels via temporary public URL.
    """

    print("\n" + "=" * 60)
    print("📘 FACEBOOK UPLOAD STARTING")
    print("=" * 60)

    # Get credentials
    access_token = os.getenv('FB_ACCESS_TOKEN')
    page_id = os.getenv('FB_PAGE_ID')

    if not access_token:
        error_msg = "❌ FB_ACCESS_TOKEN not set"
        print(f"[facebook] {error_msg}")
        raise ValueError(error_msg)

    if not page_id:
        error_msg = "❌ FB_PAGE_ID not set"
        print(f"[facebook] {error_msg}")
        raise ValueError(error_msg)

    print(f"[facebook] ✅ Credentials loaded")
    print(f"[facebook] Page ID: {page_id}")
    print(f"[facebook] Token length: {len(access_token)} chars")

    # Check video file
    video_path_obj = Path(video_path)
    if not video_path_obj.exists():
        error_msg = f"❌ Video file not found: {video_path}"
        print(f"[facebook] {error_msg}")
        raise FileNotFoundError(error_msg)

    file_size_mb = video_path_obj.stat().st_size / (1024 * 1024)
    print(f"[facebook] ✅ Video file found: {video_path}")
    print(f"[facebook] Video size: {file_size_mb:.2f} MB")

    # Limit description
    description_limited = description[:63206] if len(description) > 63206 else description
    print(f"[facebook] Description length: {len(description_limited)} characters")

    try:
        # Step 1: Upload to tmpfiles.org with retries
        max_attempts = 3
        video_url = None
        for attempt in range(max_attempts):
            try:
                print(f"[facebook] 📤 Step 1: Uploading to temporary hosting (Attempt {attempt+1}/{max_attempts})...")
                with open(video_path_obj, 'rb') as video_file:
                    files = {'file': ('video.mp4', video_file, 'video/mp4')}
                    temp_response = requests.post('https://tmpfiles.org/api/v1/upload', files=files, timeout=120)

                if temp_response.status_code == 200:
                    temp_data = temp_response.json()
                    temp_url = temp_data.get('data', {}).get('url', '')
                    if temp_url:
                        video_url = temp_url.replace('tmpfiles.org/', 'tmpfiles.org/dl/').replace('http://', 'https://')
                        print(f"[facebook] ✅ Temporary URL created: {video_url}")
                        break
                print(f"[facebook] ⚠️ Attempt {attempt+1} failed: {temp_response.status_code}")
            except Exception as e:
                print(f"[facebook] ⚠️ Attempt {attempt+1} failed: {e}")
            if attempt < max_attempts - 1:
                time.sleep(5)

        if not video_url:
            raise Exception("Failed to upload to temporary hosting after multiple attempts")

        # Step 2: Create Facebook video post with video URL
        print(f"[facebook] 📦 Step 2: Creating Facebook video post...")

        # Try different API versions
        api_versions = ['v18.0', 'v19.0', 'v20.0']
        video_id = None

        for api_version in api_versions:
            print(f"[facebook] Trying API version: {api_version}")

            post_url = f"https://graph.facebook.com/{api_version}/{page_id}/videos"
            post_params = {
                'access_token': access_token,
                'description': description_limited,
                'title': 'Bajka dla dzieci',
                'file_url': video_url,  # Use file_url instead of uploading file directly
                'published': True
            }

            print(f"[facebook] Request URL: {post_url}")
            print(f"[facebook] Parameters: title='Bajka dla dzieci', file_url={video_url[:50]}..., description length={len(description_limited)}")

            post_response = requests.post(post_url, params=post_params, timeout=60)

            print(f"[facebook] Response status: {post_response.status_code}")
            print(f"[facebook] Response body: {post_response.text}")

            if post_response.status_code == 200:
                response_data = post_response.json()
                video_id = response_data.get('id')
                if video_id:
                    print(f"[facebook] ✅ Video posted with API {api_version}: {video_id}")
                    break
            else:
                error_data = post_response.json() if post_response.text else {}
                error_msg = error_data.get('error', {}).get('message', 'Unknown error')
                error_code = error_data.get('error', {}).get('code', 'N/A')
                error_type = error_data.get('error', {}).get('type', 'N/A')

                print(f"[facebook] ❌ API {api_version} failed:")
                print(f"[facebook]    Error type: {error_type}")
                print(f"[facebook]    Error code: {error_code}")
                print(f"[facebook]    Error message: {error_msg}")

        if not video_id:
            error_msg = "Failed to create video post with all API versions"
            print(f"[facebook] ❌ {error_msg}")
            raise Exception(error_msg)

        # Step 3: Wait for processing (Facebook usually processes quickly)
        print(f"[facebook] ⏳ Step 3: Waiting for video processing...")
        time.sleep(30)  # Give Facebook time to process

        print(f"[facebook] ✅ SUCCESS! Video published to Facebook!")
        print(f"[facebook] Video ID: {video_id}")
        print(f"[facebook] Check your Facebook Page to see the post!")
        print("=" * 60)

        return {
            'id': video_id,
            'platform': 'facebook',
            'status': 'success'
        }

    except Exception as e:
        print(f"[facebook] ❌ ERROR!")
        print(f"[facebook] {str(e)}")
        print("=" * 60)
        raise

def main():
    """Test upload to Facebook."""
    video_file = Path('output/final_video.mp4')

    if not video_file.exists():
        print(f"[facebook] ❌ Video not found: {video_file}")
        return

    # Read story for description
    story_file = Path('output/story.txt')
    if story_file.exists():
        description = story_file.read_text(encoding='utf-8')[:63206]  # Facebook description limit
    else:
        description = "Bajka dla dzieci 📚 #BajkiDlaDzieci #Polski #Edukacja"

    try:
        result = upload_to_facebook(str(video_file), description)
        print(f"\n✅ Success! Result: {result}")
    except Exception as e:
        print(f"\n❌ Failed: {e}")

if __name__ == '__main__':
    main()
