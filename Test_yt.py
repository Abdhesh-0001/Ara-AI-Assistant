from youtube_transcript_api import YouTubeTranscriptApi

video_id = "5AM5nVZZxfE"

try:
    api = YouTubeTranscriptApi()
    transcript = api.fetch(video_id)
    print(f"SUCCESS! Got {len(transcript)} snippets")
    print(transcript[0].text)
except Exception as e:
    print(f"ERROR: {type(e).__name__}: {e}")
