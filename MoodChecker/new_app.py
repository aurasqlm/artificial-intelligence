import pandas as pd
from textblob import TextBlob
from colorama import init, Fore, Style

init(autoreset=True)

df = pd.read_csv("imdb_top_100.csv")

df["Overview"] = df["Overview"].fillna("")
df["Sentiment"] = df["Overview"].apply(
    lambda x: TextBlob(x).sentiment.polarity
)

genres = sorted(set(
    g.strip()
    for x in df["Genre"].dropna()
    for g in x.split(",")
))

moods = {
    "1": ("Happy", 0.2),
    "2": ("Relaxed", 0.1),
    "3": ("Sad", -0.2),
    "4": ("Excited", 0.3),
    "5": ("Dark", -0.3)
}

def recommend(genre, mood_threshold, limit=5):

    data = df[df["Genre"].str.contains(genre, case=False, na=False)]

    if data.empty:
        return []

    if mood_threshold >= 0:
        filtered = data[data["Sentiment"] >= mood_threshold]
    else:
        filtered = data[data["Sentiment"] <= mood_threshold]

    if filtered.empty:
        return []

    filtered = filtered.sort_values(
        by="IMDB_Rating", ascending=False
    )

    top = filtered.head(limit)

    return [
        (row["Series_Title"], row["Released_Year"], row["IMDB_Rating"], round(row["Sentiment"], 2))
        for _, row in top.iterrows()
    ]


def main():

    print(Fore.BLUE + Style.BRIGHT + "\n Movie Recommendation System (Top 100 Edition)\n")

    name = input(Fore.CYAN + "Enter your name: " + Fore.WHITE).strip()

    print(Fore.YELLOW + "\nAvailable Genres:")
    for i, g in enumerate(genres, 1):
        print(f"{Fore.WHITE}{i}. {Fore.GREEN}{g}")

    while True:
        g = input(Fore.MAGENTA + "\nSelect genre (number or name): " + Fore.WHITE).strip()

        if g.isdigit() and 1 <= int(g) <= len(genres):
            genre = genres[int(g) - 1]
            break

        if g.title() in genres:
            genre = g.title()
            break

        print(Fore.RED + "Invalid genre selection. Try again.")

    print(Fore.CYAN + f"\nSelected Genre: {genre}")

    print(Fore.YELLOW + "\nSelect Your Mood:")
    for k, v in moods.items():
        print(f"{Fore.WHITE}{k}. {Fore.GREEN}{v[0]}")

    while True:
        m = input(Fore.MAGENTA + "Enter mood number: " + Fore.WHITE).strip()

        if m in moods:
            mood_name, mood_value = moods[m]
            break

        print(Fore.RED + "Invalid mood selection. Try again.")

    movies = recommend(genre, mood_value)

    print(Fore.YELLOW + Style.BRIGHT +
          f"\nRecommendations for {name} ({mood_name} mood):\n")

    if not movies:
        print(Fore.RED + "No matching movies found.")
        return

    for i, (title, year, rating, sentiment) in enumerate(movies, 1):
        sentiment_color = Fore.GREEN if sentiment >= 0 else Fore.RED

        print(
            f"{Fore.WHITE}{i}. {Fore.GREEN}{title} "
            f"{Fore.CYAN}({year}) "
            f"{Fore.WHITE}| IMDb: {rating} "
            f"| Sentiment: {sentiment_color}{sentiment:.2f}"
        )


if __name__ == "__main__":
    main()