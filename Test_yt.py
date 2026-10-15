from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import IpBlocked, TranscriptsDisabled,NoTranscriptFound

def extract_youtube_transcript(video_id):
    try:
        api = YouTubeTranscriptApi()
        transcript_list = api.fetch(video_id)
        return " ".join([item.text for item in transcript_list])
    except IpBlocked:
        return "⚠️ YouTube is temporarily blocking transcript requests from this network. Please try again later or use manual notes."
    except (TranscriptsDisabled, NoTranscriptFound):
        return "⚠️ Transcripts are disabled or unavailable for this video."
    except Exception as e:
        return f"❌ Error retrieving transcript: {str(e)}"
