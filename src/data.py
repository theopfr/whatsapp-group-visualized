import re
import pandas as pd
from collections import Counter
from utils import MESSAGE_TYPE_MAP, extract_emojis


def message_count(df: pd.DataFrame) -> pd.DataFrame:
    counts = df["sender_name"].value_counts().sort_values(ascending=False)
    return counts.reset_index().rename(columns={"index": "sender_name", "count": "count"})


def message_activity_stack(df: pd.DataFrame) -> pd.DataFrame:
    df["timestamp"] = pd.to_datetime(df["timestamp"] / 1000, unit="s")
    df["month_year"] = df["timestamp"].dt.to_period("M").astype(str)
    
    df = df.groupby(["month_year", "sender_name"]).size().unstack(fill_value=0).sort_index()
    return df.reset_index().melt(id_vars="month_year", var_name="user", value_name="message_count")


def average_message_length(df: pd.DataFrame) -> pd.DataFrame:
    df["message_length"] = df["text_data"].apply(lambda x: len(str(x)))

    average_message_length = df.groupby("sender_name")["message_length"].mean()
    return average_message_length.sort_values(ascending=False).reset_index().rename(columns={"index": "sender_name", "length": "length"})


def message_activity(df: pd.DataFrame, users: list[str] = None) -> pd.DataFrame:
    df["timestamp"] = pd.to_datetime(df["timestamp"] / 1000, unit="s")
    df["month_year"] = df["timestamp"].dt.to_period("M").astype(str)

    if users is None:
        return (
            df["month_year"]
            .value_counts()
            .sort_index()
            .reset_index()
            .rename(columns={"index": "month_year", "month_year": "message_count"})
        )

    if users == "*":
        users = df["sender_name"].dropna().unique()

    all_months = pd.period_range(
        start=df["timestamp"].min().to_period("M"),
        end=df["timestamp"].max().to_period("M"),
        freq="M"
    ).astype(str)

    records = []
    for user in users:
        user_df = df[df["sender_name"] == user]
        monthly_counts = (
            user_df["month_year"]
            .value_counts()
            .reindex(all_months, fill_value=0)
            .sort_index()
        )
        for month, count in monthly_counts.items():
            records.append({"month_year": month, "user": user, "message_count": count})

    return pd.DataFrame(records)

    
def weekly_activity(df: pd.DataFrame, user: str = None) -> pd.DataFrame:
    df["timestamp"] = pd.to_datetime(df["timestamp"] / 1000, unit="s")
    df["weekday"] = df["timestamp"].dt.day_name()
    
    if user:
        df = df[df["sender_name"] == user]

    counts = df["weekday"].value_counts().reset_index()
    counts.columns = ["weekday", "count"]

    weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    counts["weekday"] = pd.Categorical(counts["weekday"], categories=weekday_order, ordered=True)

    counts = counts.sort_values("weekday").reset_index(drop=True)

    return counts




def top_emojis(df: pd.DataFrame, top_n: int | None = 3) -> pd.DataFrame:
    df["emojis"] = df["text_data"].apply(extract_emojis)

    sender_emoji_counts = (
        df.groupby("sender_name")["emojis"]
        .apply(lambda lists: sum(lists, []))
        .apply(Counter)
    )

    top_emojis = {
        sender: [emoji for emoji, _ in counter.most_common()] if top_n is None
        else [emoji for emoji, _ in counter.most_common(top_n)]
        for sender, counter in sender_emoji_counts.items()
    }

    max_len = max(len(emojis) for emojis in top_emojis.values())
    columns = [f"{i+1}." for i in range(max_len)]

    emoji_df = (
        pd.DataFrame.from_dict(top_emojis, orient="index")
        .rename(columns=dict(enumerate(columns)))
        .reset_index()
        .rename(columns={"index": "sender_name"})
    )

    return emoji_df


def emoji_density(df: pd.DataFrame) -> pd.DataFrame:
    df["emojis"] = df["text_data"].apply(extract_emojis)
    df["emoji_count"] = df["emojis"].apply(len)
    return df.groupby("sender_name")["emoji_count"].sum().reset_index(name="count")
    


def sentiment_counts(df: pd.DataFrame) -> pd.DataFrame:
    filtered = df[df["sentiment"].isin(["positive", "negative"])]

    counts = (
        filtered.groupby(["sender_name", "sentiment"])
        .size()
        .unstack(fill_value=0)
    )

    counts["total_pos_neg"] = counts.sum(axis=1)
    counts["positive_ratio"] = counts.get("positive", 0) / counts["total_pos_neg"]
    counts["negative_ratio"] = counts.get("negative", 0) / counts["total_pos_neg"]

    ratios = counts[["positive_ratio", "negative_ratio"]].reset_index()

    melted = ratios.melt(id_vars="sender_name", value_vars=["positive_ratio", "negative_ratio"], var_name="sentiment", value_name="ratio")

    melted["sentiment_order"] = melted["sentiment"].apply(lambda x: 0 if x == "positive_ratio" else 1)
    melted = melted.sort_values(by=["sentiment_order", "ratio"], ascending=[True, False])
    melted = melted.drop(columns="sentiment_order")

    return melted


def monthly_sentiment_score(df: pd.DataFrame, average: bool = False) -> pd.DataFrame:
    df["date"] = pd.to_datetime(df["timestamp"] / 1000, unit="s", errors="coerce")

    filtered = df[df["sentiment"].isin(["positive", "negative"])].copy()
    filtered["month_year"] = filtered["date"].dt.to_period("M").astype(str)

    counts = (
        filtered.groupby(["sender_name", "month_year", "sentiment"])
        .size()
        .unstack(fill_value=0)
        .reset_index()
    )

    counts["total"] = counts.get("positive", 0) + counts.get("negative", 0)
    counts["sentiment_score"] = counts.apply(
        lambda row: row["positive"] / row["total"] if row["total"] > 0 else 0.5, axis=1
    )
    
    result = counts[["sender_name", "month_year", "sentiment_score"]]
    if not average:
        return result

    avg_scores = (
        result.groupby("month_year")["sentiment_score"]
        .mean()
        .reset_index()
        .assign(sender_name="average")
    )

    return avg_scores

def count_link_messages(df: pd.DataFrame) -> pd.DataFrame:
    df["has_link"] = df["text_data"].str.contains(r"https?://", case=False, na=False)
    link_counts = df.groupby("sender_name")["has_link"].sum().reset_index()
    return link_counts.rename(columns={"has_link": "link_message_count"})


def normalize_name(name: str, alias_dict: dict):
    name = str(name).lower().strip()
    for canonical, aliases in alias_dict.items():
        if name == canonical or name in aliases:
            return canonical
    return name


def count_mentions(df: pd.DataFrame, alias_dict: dict = None, direction_mentions: bool = False) -> pd.DataFrame:
    df = df[df["sender_name"].str.lower() != "other"]
    df["sender_normalized"] = df["sender_name"].apply(lambda n: normalize_name(n, alias_dict))
    senders = df["sender_normalized"].dropna().unique()

    mention_counts = {sender: {other: 0 for other in senders} for sender in senders}

    for sender in senders:
        sender_msgs = df[df["sender_normalized"] == sender]["text_data"].dropna().astype(str)
        for mentioned in senders:
            if mentioned == sender:
                continue

            aliases = alias_dict.get(mentioned, [])
            if direction_mentions:
                aliases = [a for a in aliases if a.isdigit()]
                all_names = aliases
            else:
                all_names = [mentioned] + aliases

            if not all_names:
                continue

            pattern = re.compile(r"\b(" + "|".join(map(re.escape, all_names)) + r")\b", re.IGNORECASE)
            count = sender_msgs.str.count(pattern).sum()
            mention_counts[sender][mentioned] = count

    mention_df = pd.DataFrame(mention_counts)
    return mention_df


def message_type_distribution(df: pd.DataFrame, include_other_types: bool = False) -> pd.DataFrame:
    df["message_type_str"] = df["message_type"].astype(str)
    df["message_type_label"] = df["message_type_str"].map(MESSAGE_TYPE_MAP)
    df = df[df["message_type_str"].isin(MESSAGE_TYPE_MAP.keys())]

    counts = df.groupby(["sender_name", "message_type_label"]).size().reset_index(name="count")

    return counts


def prepare_data(config: dict) -> pd.DataFrame:
    df = pd.read_csv("./data/group-chat.csv")
    
    
    sentiment_columns = ["sentiment", "score"]
    
    contains_sentiments = all(col in df.columns for col in sentiment_columns)
    
    columns_of_interest = ["sender_jid_row_id", "timestamp", "message_type", "text_data"]
    if contains_sentiments:
        columns_of_interest.extend(sentiment_columns)
    
    df = df[columns_of_interest]

    df["sender_jid_row_id"] = df["sender_jid_row_id"].astype(str)
    df["sender_name"] = df["sender_jid_row_id"].map(config["jidMap"])
    df["sender_name"] = df["sender_name"].apply(lambda x: "Other" if x in config["other"] else x)

    if config["excludeOther"]:
        df = df[df["sender_name"].str.lower() != "other"]

    return df


