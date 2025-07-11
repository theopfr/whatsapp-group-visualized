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