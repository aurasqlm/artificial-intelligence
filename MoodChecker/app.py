import pandas as pd
from textblob import TextBlob
from colorama import init, Fore, Style

init(autoreset=True)

df = pd.read_csv("imdb_top_1000.csv")

genres = sorted(set(g.strip() for x in df["Genre"].dropna() for g in x.split(",")))

moods = {
    "1": ("Happy", 0.2),
    "2": ("Relaxed", 0.1),
    "3": ("Sad", -0.2),
    "4": ("Excited", 0.3),
    "5": ("Dark", -0.3)
}

def recommended(genre, mood_threshold, limit=5):
    data = df[df["Genre"].str.contains(genre, case=False, na=False)]
    result = []

    for _, row in data.sample(frac=1).iterrows():
        if pd.isna(row["Overview"]):
            continue

        polarity = TextBlob(row["Overview"]).sentiment.polarity

        if (mood_threshold >= 0 and polarity >= mood_threshold) or \
           (mood_threshold < 0 and polarity <= mood_threshold):

            result.append(
                (row["Series_Title"], row["Released_Year"], round(polarity, 2))
            )

        if len(result) == limit:
            break

    return result

def main():
    print(Fore.BLUE + Style.BRIGHT + "\n Movie Reccomendation Syste\n")
    name = input(Fore.CYAN + "Enter your name: " + Fore.WHITE).strip()
    print(Fore.YELLOW + "\nAvailable Genres:")
    for i,g in enumerate(genres,1):
        print(f"{Fore.WHITE}{i}. {Fore.GREEN}{g}")

    while True:
        g = input(Fore.MAGENTA + "\nSelect genre (number or name): " + Fore.WHITE) 
