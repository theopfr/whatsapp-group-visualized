from joblib import Parallel, delayed
import pandas as pd
from textblob_de import TextBlobDE
from tqdm import tqdm


tqdm.pandas()


def analyze_sentiment(text):
    if not isinstance(text, str) or text.strip() == "":
        return ("neutral", 0.0)
    blob = TextBlobDE(text)
    score = blob.sentiment.polarity
    if score >= 0.666:
        return ("positive", score)
    elif score <= -0.666:
        return ("negative", score)
    else:
        return ("neutral", score)
    

def get_message_sentiments(df: pd.DataFrame, out_path: str) -> pd.DataFrame:
    results = Parallel(n_jobs=8)(
        delayed(analyze_sentiment)(text) for text in tqdm(df["text_data"])
    )
    
    sentiment_df = pd.DataFrame(results, index=df.index, columns=["sentiment", "score"])

    df = df.copy()
    df[["sentiment", "score"]] = sentiment_df
    
    df.to_csv(out_path, index=False)
    
    return df


if __name__ == "__main__":
    df = pd.read_csv("./data/group-chat-original.csv")
    get_message_sentiments(df, out_path="./data/group-chat-sentiments.csv")
