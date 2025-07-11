import dash
from dash import html, dcc, Input, Output, dash_table
from data import message_count, prepare_data, top_emojis
from plots import (
    plot_message_count_pie,
    plot_message_count_bar,
    plot_average_message_length,
    plot_monthly_activity,
    plot_monthly_activity_stacked,
    plot_weekly_activity_group,
    plot_user_weekly_activity,
    plot_sentiment_ratios,
    plot_emoji_density,
    plot_mentions_heatmap,
    plot_direct_mentions_heatmap,
    plot_message_type_distribution,
    plot_link_distribution,
    plot_monthly_sentiment_line
)
from utils import load_json


CONFIG = load_json("./data/config.json")

group_name = CONFIG["groupName"]

wa_df = prepare_data(CONFIG)

contains_sentiments = "sentiment" in wa_df.columns and "score" in wa_df.columns

app = dash.Dash(__name__)
app.title = f"WhatsApp Group Analyzed"

user_message_counts = message_count(wa_df.copy())
top_3_most_messages = user_message_counts["sender_name"].tolist()[:3]

user_selections = [{"label": user, "value": user} for user in sorted(wa_df["sender_name"].dropna().unique())]
emoji_df = top_emojis(wa_df.copy(), top_n=3)

style_section = {
    "backgroundColor": "#f0f0f0",
    "borderRadius": "5px",
    "padding": "20px",
    "marginBottom": "20px"
}

image_dist_plot, top_image_sender = plot_message_type_distribution(wa_df.copy(), "image", "Images")
sticker_dist_plot, top_sticker_sender = plot_message_type_distribution(wa_df.copy(), "sticker", "Stickers")
map_dist_plot, top_map_sender = plot_message_type_distribution(wa_df.copy(), "map", "Maps")
deleted_dist_plot, top_deleted_sender = plot_message_type_distribution(wa_df.copy(), "deleted", "Deleted")
link_dist_plot, top_link_sender = plot_link_distribution(wa_df.copy())


def section(children, **style):
    return html.Div(children, style={"backgroundColor": "#f0f0f0", "borderRadius": "5px", "padding": "20px", "marginBottom": "20px", **style})

def flex_row(children):
    return html.Div(children, style={"display": "flex", "flexWrap": "wrap"})

def render_medals(top_users):
    return html.Div([
        html.H3(f"🥇 {top_users[0]}"),
        html.H3(f"🥈 {top_users[1]}"),
        html.H3(f"🥉 {top_users[2]}"),
    ], style={"display": "flex", "flexDirection": "row", "gap": "20px", "justifyContent": "center"})


def render_media_row(fig, title, name, emoji):
    return html.Div([
        html.Div([
            html.H2(f"{emoji} {title}: {name}"),
        ], style={
            "marginTop": "auto",
            "marginBottom": "auto",
            "padding": "10px",
            "textAlign": "center",
            "minWidth": "200px"
        }),
        dcc.Graph(figure=fig, style={"flex": 1, "flexGrow": 1, "height": "100%", "minWidth": "500px"})
    ], style={
        "display": "flex",
        "flexDirection": "column",
        "flex": 1,
        "alignItems": "center"
    })


app.layout = html.Div([
    html.H1(f"🔎 {group_name} - Analyzed", style={**style_section}),

    html.H2("👄 Biggest Yappers", style={**style_section}),    
    section([
        flex_row([
            dcc.Graph(figure=plot_message_count_pie(wa_df.copy()), style={"flex": 1, "flexGrow": 1, "minWidth": "500px", "height": "100%"}),
            dcc.Graph(figure=plot_message_count_bar(wa_df.copy()), style={"flex": 1, "flexGrow": 1, "minWidth": "500px", "height": "100%"}),
            dcc.Graph(figure=plot_average_message_length(wa_df.copy()), style={"flex": 1, "flexGrow": 1, "minWidth": "500px", "height": "100%"}),
        ]),
        render_medals(top_3_most_messages)
    ]),

    html.H2("🖇️ Most Co-Dependent", style={**style_section}),
    section(flex_row([
        dcc.Graph(figure=plot_monthly_activity(wa_df.copy()), style={"flex": 1, "flexGrow": 1, "minWidth": "500px", "height": "100%"}),
        dcc.Graph(figure=plot_monthly_activity_stacked(wa_df.copy()), style={"flex": 1, "flexGrow": 1, "minWidth": "500px", "height": "100%"}),
    ])),
    
    section(flex_row([
        dcc.Graph(figure=plot_weekly_activity_group(wa_df.copy()), style={"flex": 1, "flexGrow": 1, "minWidth": "500px", "height": "100%"}),
        html.Div([
            dcc.Graph(id="weekly-activity-plot", style={"flexGrow": 1, "minWidth": "500px", "height": "100%", "width": "100%"}),
            html.Div(dcc.Dropdown(
                id="user-dropdown",
                options=user_selections,
                value=user_selections[0]["value"],
                style={"width": "150px"}
            ), style={"display": "flex", "justifyContent": "center"})
        ], style={"flex": 1, "width": "50%", "margin": "auto", "display": "flex", "flexDirection": "column", "alignItems": "center"})
    ])),
    
    section(flex_row([
        dcc.Graph(figure=plot_mentions_heatmap(wa_df.copy(), alias_dict=CONFIG["senderAliases"]), style={"flex": 1, "flexGrow": 1, "minWidth": "500px", "height": "100%"}),
        dcc.Graph(figure=plot_direct_mentions_heatmap(wa_df.copy(), alias_dict=CONFIG["senderAliases"]), style={"flex": 1, "flexGrow": 1, "minWidth": "500px", "height": "100%"})
    ])),

    html.H2("❤️ Pure Emotions", style={**style_section}),    
    section([
        flex_row([
            html.Div(dash_table.DataTable(
                data=emoji_df.to_dict("records"),
                columns=[{"name": col, "id": col} for col in emoji_df.columns],
                style_cell={"textAlign": "center", "fontSize": 22},
                style_header={"fontWeight": "bold", "backgroundColor": "#f9f9f9"},
                style_table={"margin": "100px auto", "width": "80%"},
                fixed_rows={"headers": True},
                page_action="none",
                style_as_list_view=False,
            ), style={"flex": 1, "height": "100%", "minWidth": "500px"}),
            html.Div(dcc.Graph(figure=plot_emoji_density(wa_df.copy())), style={"flex": 1, "flexGrow": 1, "height": "100%", "minWidth": "500px"}),
        ]),
        html.Div([
            dcc.Graph(figure=plot_sentiment_ratios(wa_df.copy())),
            dcc.Graph(id="monthly-sentiment-plot"),
            html.Div(dcc.Dropdown(
                id="sentiment-mode-dropdown",
                options=["all", "average"],
                value="all",
                style={"width": "150px"}
            ), style={"display": "flex", "justifyContent": "center"})
        ]) if contains_sentiments else None
    ]),
 
    html.H2("📱 Multi Media", style={**style_section}),   
    section([
        flex_row([
            render_media_row(image_dist_plot, "Meme Lord", top_image_sender, "🖼️"),
            render_media_row(sticker_dist_plot, "Sticker Collector", top_sticker_sender, "🎫"),
        ]),
        flex_row([
            render_media_row(map_dist_plot, "Navigator", top_map_sender, "🗺️"),
            render_media_row(link_dist_plot, "Intel-Man", top_link_sender, "🔗"),
        ]),
        flex_row([
            render_media_row(deleted_dist_plot, "Retractor", top_deleted_sender, "❌"),
            html.Div()  # Empty block for alignment (since odd number)
        ]),
    ])

], style={"margin": "25px"})


@app.callback(
    Output("weekly-activity-plot", "figure"),
    Input("user-dropdown", "value")
)
def update_weekly_activity(selected_user):
    return plot_user_weekly_activity(wa_df.copy(), user=selected_user)


if contains_sentiments:
    @app.callback(
        Output("monthly-sentiment-plot", "figure"),
        Input("sentiment-mode-dropdown", "value")
    )
    def update_monthly_sentiment(mode):
        return plot_monthly_sentiment_line(wa_df.copy(), average=(mode == "average"))



if __name__ == "__main__":
    import os
    
    if os.environ.get("ENV", "dev") == "dev":
        app.run(debug=True)
    else:
        app.run(host="0.0.0.0")
