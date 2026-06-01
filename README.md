# WhatsApp Chat Analyzer

A simple Streamlit app for analyzing WhatsApp chat exports. Upload one or more exported chat text files, then view summary statistics, timelines, word clouds, and emoji usage.

## Features

- Upload multiple WhatsApp chat text files at once
- Decode common text encodings automatically
- Show statistics for overall chat or selected users
- Display:
  - Total messages
  - Total words
  - Media shared count
  - Links shared count
  - Monthly timeline
  - Daily timeline
  - Most busy users (overall view)
  - Word cloud
  - Emoji analysis

## Requirements

- Python 3.8+
- Streamlit
- pandas
- matplotlib
- wordcloud
- seaborn
- urlextract
- emoji

## Setup

1. Clone or download the repository.
2. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Install dependencies:

```powershell
pip install -r requirements.txt
```

## Run the app

From the project folder, run:

```powershell
streamlit run app.py
```

Then open the local URL shown in the terminal.

## Usage

1. Upload one or more WhatsApp chat text files using the sidebar uploader.
2. Choose `Overall` or a specific user from the dropdown.
3. Review the generated statistics and charts.

## Project files

- `app.py` - Streamlit application UI and upload handling
- `preprocessor.py` - Chat text parsing into a pandas DataFrame
- `helper.py` - Analysis functions for statistics, timelines, word clouds, and emoji counts

## Notes

- The app expects WhatsApp export text files with timestamps like `DD/MM/YYYY, HH:MM -`.
- Group notification entries are excluded from user-level analysis.
