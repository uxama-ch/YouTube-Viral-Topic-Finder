# YouTube-Viral-Topic-Finder
Search for **viral YouTube videos** from small creators based on keywords and filters.
# YouTube Viral Topics Tool

An interactive Streamlit-based tool to discover potentially viral YouTube videos using custom keyword searches and filters. Ideal for content creators and trend hunters targeting low-subscriber channels with high-performing content.

---

## ✨ Features

### Core Functionalities

* ✅ **Custom Keywords Input** (one per line)
* ✅ **Custom Date Range** (1–30 days)
* ✅ **Max Subscriber Filter** (e.g., < 3000 subs)
* ✅ **Minimum View Count Filter** (optional)
* ✅ **Video Duration Filter** (Short, Medium, Long)
* ✅ **Sort by Views / View-to-Subscriber Ratio / Recency**
* ✅ **View-to-Subscriber Ratio Calculation**
* ✅ **Shows Publish Date and Video Thumbnail**
* ✅ **Duplicate Video Prevention**
* ✅ **Displays in Streamlit Columns UI**
* ✅ **CSV Export of Results**

### UX & Performance Enhancements

* ✅ **Dark Mode Compatible Layout**
* ✅ **Progressive API Caching** (to reduce calls and enhance speed)
* ✅ **Better Error Reporting and Debugging**
* ✅ **Streamlit Sidebar for Easy Configuration**

---

## 🤔 Overlapping Features Handled

| Feature                                     | Handled With                                | Recommendation                                         |
| ------------------------------------------- | ------------------------------------------- | ------------------------------------------------------ |
| View-to-Subscriber Ratio & View Sorting     | Select box for user to pick one sort method | Avoid sorting by both at once                          |
| Duration Filter + Min View Count + Max Subs | All applied in strict sequence              | Ensure filter combinations don’t overly narrow results |
| Duplicate Video Prevention                  | Internal hash set to skip repeats           | No action needed                                       |
| Repeated API Calls                          | Cached with TTL of 10 minutes               | Re-run if data seems stale                             |

---

## 🚀 Installation & Usage

### 1. Clone the Repo

```bash
git clone https://github.com/your-username/youtube-viral-topics-tool.git
cd youtube-viral-topics-tool
```

### 2. Create a Virtual Environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

### 4. Run the App

```bash
streamlit run your_script_name.py
```

---

## ⚡ Requirements

```
streamlit
requests
isodate
```

Create a `requirements.txt` file with:

```txt
streamlit
requests
isodate
```

---

## ✨ API Key

You need a valid YouTube Data API v3 Key. Get it from: [https://console.developers.google.com/](https://console.developers.google.com/)

---

## 🚫 Not Included (Future Roadmap)

* Pagination Controls
* Saved Favorites across sessions
* Tag/topic detection from metadata
* Channel category filters

---

## 🎉 Credits

Built with ❤️ using [Streamlit](https://streamlit.io/) and YouTube Data API.

---

Feel free to fork, star, and contribute to enhance this tool for creators!
