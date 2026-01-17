from datetime import datetime
from textblob import TextBlob
from colorama import Fore, Style, init


init(autoreset=True)


print(Fore.LIGHTBLUE_EX + Style.BRIGHT + "SENTIMENT SPY")
print(Fore.LIGHTMAGENTA_EX + "Enter your name: ", end="")
name = input().strip() or "Agent"
print(Fore.LIGHTCYAN_EX + f"Welcome, {name}")
print(Fore.WHITE + "Commands: help | history | stats | reset | exit\n")


history = []
start_time = datetime.now()


def analyze(text):
    polarity = round(TextBlob(text).sentiment.polarity, 3)
    confidence = round(abs(polarity) * 100, 2)

    if polarity > 0.3:
        return "Positive", polarity, confidence, Fore.LIGHTGREEN_EX
    elif polarity < -0.3:
        return "Negative", polarity, confidence, Fore.LIGHTRED_EX
    else:
        return "Neutral", polarity, confidence, Fore.LIGHTYELLOW_EX


def show_help():
    print(Fore.LIGHTCYAN_EX + "\nAvailable Commands:")
    print(Fore.WHITE + "  :help     - Show commands")
    print(Fore.LIGHTBLUE_EX + "  :history  - Sentiment history")
    print(Fore.LIGHTMAGENTA_EX + "  :stats    - Session summary")
    print(Fore.LIGHTYELLOW_EX + "  :reset    - Clear history")
    print(Fore.LIGHTRED_EX + "  :exit     - Quit program\n")


def show_history():
    if not history:
        print(Fore.LIGHTRED_EX + "No history available")
        return

    for i, h in enumerate(history, 1):
        print(
            f"{Fore.LIGHTCYAN_EX}{i}. "
            f"{Fore.LIGHTBLUE_EX}[{h['time']}] "
            f"{Fore.WHITE}{h['sentiment']} "
            f"{Fore.LIGHTMAGENTA_EX}({h['polarity']})"
        )
