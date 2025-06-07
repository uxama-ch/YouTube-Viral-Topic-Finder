import streamlit as st
import requests
import csv
import io
from datetime import datetime, timedelta
from isodate import parse_duration
from urllib.parse import urlencode
from collections import defaultdict
import hashlib

# Streamlit App Title
st.set_page_config(page_title="YouTube Viral Topics Tool", layout="wide")
st.title("\U0001F4FA YouTube Viral Topics Tool")

# Caching Decorators
@st.cache_data(ttl=600)
def fetch_url(url, params):
    try:
        full_url = f"{url}?{urlencode(params)}"
        response = requests.get(full_url)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

# Inputs
st.sidebar.header("Configuration")
API_KEY = st.sidebar.text_input("YouTube API Key", type="password")
days = st.sidebar.slider("Search Recent Days", min_value=1, max_value=30, value=5)
keywords_input = st.sidebar.text_area("Keywords (one per line)", """Affair Relationship Stories
Reddit Relationship Advice
Reddit Cheating
Reddit Marriage
True Cheating Story
Wife Cheated I Can't Forgive""")
subscriber_limit = st.sidebar.number_input("Max Subscriber Count", min_value=0, value=3000)
min_view_count = st.sidebar.number_input("Min View Count (Optional)", min_value=0, value=1000)
filter_duration = st.sidebar.selectbox("Filter by Duration", ["Any", "Short (<4min)", "Medium (4-20min)", "Long (>20min)"])
sort_option = st.sidebar.selectbox("Sort Results By", ["Views", "View-to-Sub Ratio", "Recency"])

keywords = [k.strip() for k in keywords_input.split("\n") if k.strip()]

# Button Trigger
if st.button("\U0001F50D Fetch Viral Videos"):
    if not API_KEY:
        st.error("API Key is required!")
    else:
        start_date = (datetime.utcnow() - timedelta(days=int(days))).isoformat("T") + "Z"
        seen_videos = set()
        all_results = []

        for keyword in keywords:
            st.info(f"Fetching: {keyword}")

            search_params = {
                "part": "snippet",
                "q": keyword,
                "type": "video",
                "order": "viewCount",
                "publishedAfter": start_date,
                "maxResults": 5,
                "key": API_KEY,
            }

            search_data = fetch_url("https://www.googleapis.com/youtube/v3/search", search_params)

            if "items" not in search_data:
                st.warning(f"No results for: {keyword}")
                continue

            video_ids = []
            channel_ids = []
            video_data_map = {}

            for item in search_data["items"]:
                vid = item["id"].get("videoId")
                cid = item["snippet"].get("channelId")
                if not vid or not cid:
                    continue
                if vid in seen_videos:
                    continue
                seen_videos.add(vid)
                video_ids.append(vid)
                channel_ids.append(cid)
                video_data_map[vid] = item

            if not video_ids:
                continue

            stats_data = fetch_url("https://www.googleapis.com/youtube/v3/videos", {
                "part": "snippet,statistics,contentDetails",
                "id": ",".join(video_ids),
                "key": API_KEY
            })

            channel_data = fetch_url("https://www.googleapis.com/youtube/v3/channels", {
                "part": "statistics",
                "id": ",".join(channel_ids),
                "key": API_KEY
            })

            for video, channel in zip(stats_data.get("items", []), channel_data.get("items", [])):
                try:
                    vid = video["id"]
                    title = video["snippet"]["title"]
                    desc = video["snippet"]["description"][:200]
                    thumb = video["snippet"]["thumbnails"]["medium"]["url"]
                    published = video["snippet"]["publishedAt"]
                    views = int(video["statistics"].get("viewCount", 0))
                    duration_iso = video["contentDetails"]["duration"]
                    duration_sec = parse_duration(duration_iso).total_seconds()
                    subs = int(channel["statistics"].get("subscriberCount", 0))

                    if subs > subscriber_limit or views < min_view_count:
                        continue

                    if filter_duration == "Short (<4min)" and duration_sec > 240:
                        continue
                    if filter_duration == "Medium (4-20min)" and (duration_sec < 240 or duration_sec > 1200):
                        continue
                    if filter_duration == "Long (>20min)" and duration_sec < 1200:
                        continue

                    view_to_sub = round(views / subs, 2) if subs else 0
                    all_results.append({
                        "Title": title,
                        "Description": desc,
                        "URL": f"https://www.youtube.com/watch?v={vid}",
                        "Thumbnail": thumb,
                        "Published": published,
                        "Views": views,
                        "Subscribers": subs,
                        "Ratio": view_to_sub
                    })
                except Exception as e:
                    st.warning(f"Skipped one video due to: {e}")

        # Sort Logic
        if sort_option == "Views":
            all_results.sort(key=lambda x: x["Views"], reverse=True)
        elif sort_option == "View-to-Sub Ratio":
            all_results.sort(key=lambda x: x["Ratio"], reverse=True)
        elif sort_option == "Recency":
            all_results.sort(key=lambda x: x["Published"], reverse=True)

        # Display Summary
        st.success(f"Found {len(all_results)} relevant videos.")
        st.write("---")

        # Display Results
        for r in all_results:
            cols = st.columns([1, 3])
            with cols[0]:
                st.image(r["Thumbnail"])
            with cols[1]:
                st.markdown(f"**[{r['Title']}]({r['URL']})**")
                st.caption(f"Published: {r['Published']}")
                st.write(f"\U0001F441 Views: {r['Views']} | \U0001F465 Subs: {r['Subscribers']} | Ratio: {r['Ratio']}")
                st.write(r['Description'])

        # CSV Export
        if all_results:
            csv_data = io.StringIO()
            csv_writer = csv.DictWriter(csv_data, fieldnames=all_results[0].keys())
            csv_writer.writeheader()
            csv_writer.writerows(all_results)
            st.download_button("Download CSV", csv_data.getvalue(), "viral_videos.csv", "text/csv")
