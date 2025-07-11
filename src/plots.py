import pandas as pd
import plotly.express as px
from utils import transparent_fig
from data import (
    average_message_length,
    count_link_messages,
    count_mentions,
    emoji_density,
    message_activity,
    message_activity_stack,
    message_count,
    message_type_distribution,
    monthly_sentiment_score,
    sentiment_counts,
    weekly_activity,
)


def get_color_map(df: pd.DataFrame):
    sender_names = sorted(df["sender_name"].dropna().unique())
    colors = px.colors.qualitative.Plotly
    return {name: colors[i % len(colors)] for i, name in enumerate(sender_names)}


def plot_message_count_pie(df: pd.DataFrame):
    color_map = get_color_map(df)
    user_counts = message_count(df)
    return transparent_fig(
        px.pie(
            user_counts,
            names="sender_name",
            values="count",
            color="sender_name",
            title="Messages per Person (Pie)",
            color_discrete_map=color_map,
        )
    )


def plot_message_count_bar(df: pd.DataFrame):
    return transparent_fig(
        px.bar(
            message_count(df),
            x="sender_name",
            y="count",
            title="Messages per Person (Bar)",
        )
    )


def plot_average_message_length(df: pd.DataFrame):
    return transparent_fig(
        px.bar(
            average_message_length(df),
            x="sender_name",
            y="message_length",
            title="Average Message Length",
        )
    )


def plot_monthly_activity(df: pd.DataFrame):
    color_map = get_color_map(df)
    return transparent_fig(
        px.line(
            message_activity(df, users="*"),
            x="month_year",
            y="message_count",
            color="user",
            title="Monthly Activity per User",
            color_discrete_map=color_map,
        )
    )


def plot_monthly_activity_stacked(df: pd.DataFrame):
    return transparent_fig(
        px.bar(
            message_activity_stack(df),
            x="month_year",
            y="message_count",
            color="user",
            title="Monthly Activity Stacked",
        )
    )


def plot_weekly_activity_group(df: pd.DataFrame):
    return transparent_fig(
        px.bar(
            weekly_activity(df),
            x="weekday",
            y="count",
            title="Group Activity per Weekday",
        )
    )


def plot_sentiment_ratios(df: pd.DataFrame):
    return transparent_fig(
        px.bar(
            sentiment_counts(df),
            x="sender_name",
            y="ratio",
            color="sentiment",
            title="Positive vs Negative Sentiment Ratios",
            labels={
                "ratio": "Ratio",
                "sender_name": "Sender",
                "sentiment": "Sentiment",
            },
            color_discrete_map={
                "positive_ratio": "#637eeb",
                "negative_ratio": "#ed5b51",
            },
        )
    )


def plot_emoji_density(df: pd.DataFrame):
    color_map = get_color_map(df)
    return transparent_fig(
        px.treemap(
            emoji_density(df),
            path=["sender_name"],
            values="count",
            title="Emoji Density per User",
            color="sender_name",
            color_discrete_map=color_map,
        )
    )


def plot_mentions_heatmap(df: pd.DataFrame, alias_dict: dict = None):
    return transparent_fig(
        px.imshow(
            count_mentions(df, alias_dict=alias_dict),
            labels=dict(y="Mentioned User", x="Sender", color="Mentions"),
            color_continuous_scale="Plasma",
            aspect="auto",
            title="Mentions Between Users",
        )
    )


def plot_direct_mentions_heatmap(df: pd.DataFrame, alias_dict: dict = None):
    return transparent_fig(
        px.imshow(
            count_mentions(df, direction_mentions=True, alias_dict=alias_dict),
            labels=dict(y="@ User", x="Sender", color="Mentions"),
            color_continuous_scale="Plasma",
            aspect="auto",
            title="Direct Mentions (@) Between Users",
        )
    )


def plot_message_type_distribution(df: pd.DataFrame, type_label: str, title: str):
    df_type = message_type_distribution(df)
    filtered = df_type[df_type["message_type_label"] == type_label]
    color_map = get_color_map(df)
    
    fig = px.pie(
        filtered,
        names="sender_name",
        values="count",
        title=title,
        color="sender_name",
        color_discrete_map=color_map,
    )
    
    fig.update_layout(margin=dict(t=0))
    
    return (
        transparent_fig(fig),
        filtered.loc[filtered["count"].idxmax(), "sender_name"],
    )


def plot_link_distribution(df: pd.DataFrame):
    link_dist_df = count_link_messages(df)
    color_map = get_color_map(df)
    
    fig = px.pie(
        link_dist_df,
        names="sender_name",
        values="link_message_count",
        title="Links",
        color="sender_name",
        color_discrete_map=color_map,
    )
    
    fig.update_layout(margin=dict(t=0))
    
    return (
        transparent_fig(fig),
        link_dist_df.loc[link_dist_df["link_message_count"].idxmax(), "sender_name"],
    )


def plot_monthly_sentiment_line(df: pd.DataFrame, average: bool = False):
    df_sentiment = monthly_sentiment_score(df, average=average)
    return transparent_fig(
        px.line(
            df_sentiment,
            x="month_year",
            y="sentiment_score",
            color="sender_name",
            title="Sentiments over Time" + (" Average" if average else " per User"),
            labels={
                "month_year": "Month",
                "ratio": "Sentiment Ratio",
                "sender_name": "User",
                "sentiment": "Sentiment",
            },
        )
    )


def plot_user_weekly_activity(df: pd.DataFrame, user: str):
    user_weekly_df = weekly_activity(df, user=user)
    return transparent_fig(
        px.bar(
            user_weekly_df, x="weekday", y="count", title=f"Weekly Activity for {user}"
        )
    )
