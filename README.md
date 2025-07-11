# 💬 WhatsApp Group Visualized

A simple Plotly dashboard for visualizing your WhatsApp group chat patterns.

---

## ✨ Showcase
- Message counts and average message length per user
- Monthly and weekly activity visualizations
- Mentions and direct mentions heatmaps
- Top emojis and emoji usage over time
- Sentiment analysis (optional if data is available)
- Media usage stats

<p align="center">
  <img src="./examples/example1.png" />
  <img src="./examples/example2.png" />
</p>

*See more plots in the [`examples`](./examples) folder.*

---

## 🧑‍💻 Data Extraction
Before using this tool, you'll need to export your WhatsApp group chat data.

See the [DATA_EXTRACTION.md](./DATA_EXTRACTION.md) guide for full instructions. You will end up with a single .csv file.

---

## 📥 Installation
You can either run the project locally using a Python virtual environment or spin it up quickly with Docker.

### Option 1: Local Setup (Python)

#### 1. Clone the repository
```bash
git clone git@github.com:theopfr/whatsapp-group-visualized.git
cd whatsapp-group-visualized
```

#### 2. Create a virtual environment
Using uv (or use venv/virtualenv if you prefer):

```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

### Option 2: Docker Setup
You can run the entire app using Docker Compose.

If you haven't cloned the repo set up your project directory:
```bash
mkdir my-whatsapp-visualizer
cd my-whatsapp-visualizer
```
Then copy these files from the repo:
- docker-compose.yml → ``my-whatsapp-visualizer/docker-compose.yml``
- data/config.json → ``my-whatsapp-visualizer/data/config.json``

Your folder structure then should look like:
```
my-whatsapp-visualizer/
├── data/
│   └── config.json
└── docker-compose.yml
```

The image will be installed the first time you start docker-compose, but you can also do it manually:
```bash
docker pull ghcr.io/theopfr/whatsapp-group-visualized:latest
```

Or build it manually if you cloned the repo:
```bash
docker build -t wa-group-viz .
```

---

## 📊 Preparing Your Data
After you followed the [DATA_EXTRACTION.md guide](./DATA_EXTRACTION.md), place the csv file into your ``data/`` folder and make sure its named ``group-chat.csv``.

Then, add all the relevant data to the ``./data/config.json``. It is already filled with examplary data and consist of the following:
- the groups name (must not match the actual name on WhatsApp)
- the ``jidMap``: Maps the sender-ids to name-identifiers which will be shown in the visualization, this needs to be done manually (must not match the actual names on WhatsApp)
- ``other``: Names to be grouped into a "other", for example for inactive users (names must have been defined in ``jidMap``)
- ``excludeOthers``: Wether to show data for the "other" or ignore in in the visualizations
- ``senderAliases``: Aliases/pet-names for the senders, needed to visualize who mentions who the most even when not addressing them with the real name

---

## 🚀 Running the Dashboard
##### If using local setup:
```bash
python src/dashboard.py
```

##### If using Docker:

```bash
docker-compose up
```

Then open http://localhost:8050 in your browser.


## Sentiment Analysis
Supported languages: English and German. If you chat in another language these plots won't make much sense unfortunately but you can enhance this script to support your lanuage if possible (for example using HuggingFace models).

In order to show plots regarding sentiment, you need to run the ``src/sentiment_analysis.py`` script on your ``data/group-chat.csv``.
For that you should follow the instructions above for the local setup. Once set up you can run the script:

```bash
python src/sentiment_analysis.py --language english
```

Full usage description of the script:
```
usage: sentiment_analysis.py [-h] [--language {english,german}] [--input INPUT] [--output OUTPUT]

Sentiment analysis of chat data.

options:
  -h, --help            show this help message and exit
  --language            {english,german}, default: english
                        Language of the text data
  --input INPUT         Path to input CSV file, default: ./data/group-chat.csv
  --output OUTPUT       Path to output CSV file default: ./data/group-chat-sentiments.csv
```

This will create new .csv ``./data/group-chat-sentiments.csv``. You can rename it to ``group-chat.csv`` and use that file from now on. Once done, you will have two more plots in the dashboards showing the sentiment information.