from colorama import Fore, Style, init
from textblob import TextBlob
from datetime import datetime

init(autoreset=True)

print(f"{Fore.BLUE} {Style.BRIGHT} SENTIMENT SPY")
name = input(f"{Fore.MAGENTA}Enter your name: ").strip() or "Agent"
print(f"{Fore.CYAN}Welcome, {name}")
print(f"{Fore.CYAN}Commands: :help :stats :reset :exit\n")

history = []

def analyze(text):
    polarity = round(TextBlob(text).sentiment.polarity, 3)
    confidence = round(abs(polarity) * 100, 2)

    if polarity >= 0.3:
        return "Positive", polarity, confidence, Fore.GREEN
    if polarity <= -0.3:
        return "Negative", polarity, confidence, Fore.RED
    return "Neutral", polarity, confidence, Fore.YELLOW

def show_help():
    print(f"""{Fore.CYAN}
    :help     Show commands
    :stats    Session summary
    :reset    Clear data
    :exit     Exit
    """)