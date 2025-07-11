import argparse
from joblib import Parallel, delayed
import pandas as pd
from textblob_de import TextBlobDE
from textblob import TextBlob
from tqdm import tqdm


tqdm.pandas()


def analyze_sentiment(classifer, text: str):
    if not isinstance(text, str) or text.strip() == "":
        return ("neutral", 0.0)
    blob = classifer(text)
    score = blob.sentiment.polarity
    if score >= 0.666:
        return ("positive", score)
    elif score <= -0.666:
        return ("negative", score)
    else:
        return ("neutral", score)
    

def get_message_sentiments(df: pd.DataFrame, out_path: str, language: str) -> pd.DataFrame:
    classifiers = {
        "german": TextBlobDE,
        "english": TextBlob
    }
    
    classifier = classifiers.get(language, TextBlob)
        
    results = Parallel(n_jobs=8)(
        delayed(analyze_sentiment)(classifier, text) for text in tqdm(df["text_data"])
    )
    
    sentiment_df = pd.DataFrame(results, index=df.index, columns=["sentiment", "score"])

    df = df.copy()
    df[["sentiment", "score"]] = sentiment_df
    
    df.to_csv(out_path, index=False)
    
    return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sentiment analysis of chat data.")
    parser.add_argument("--language", type=str, default="english", choices=["english", "german"], help="Language of the text data")
    parser.add_argument("--input", type=str, default="./data/group-chat.csv", help="Path to input CSV file")
    parser.add_argument("--output", type=str, default="./data/group-chat-sentiments.csv", help="Path to output CSV file")
    
    args = parser.parse_args()

    df = pd.read_csv(args.input)
    get_message_sentiments(df, out_path=args.output, language=args.language)
