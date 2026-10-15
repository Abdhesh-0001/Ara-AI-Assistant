from youtube_transcript_api import YouTubeTranscriptApi

video_id = "jNQXAC9IVRw"
try:
    api = YouTubeTranscriptApi()
    transcript = api.fetch(video_id)
    print(f"✅ SUCCESS! Got {len(transcript)} snippets")
except Exception as e:
    print(f"❌ ERROR: {type(e).__name__}: {e}")
