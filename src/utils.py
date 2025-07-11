import json
import emoji
import plotly.graph_objs as go


def load_json(path: str) -> dict:
    with open(path) as f:
        return json.load(f)
    

def extract_emojis(text) -> list[str]:
    text = str(text)
    return [match["emoji"] for match in emoji.emoji_list(text)]


def transparent_fig(fig: go.Figure):
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    return fig


MESSAGE_TYPE_MAP = {
    "1": "image",
    "13": "image",
    "16": "map",
    "5": "map",
    "20": "sticker",
    "15": "deleted",
}