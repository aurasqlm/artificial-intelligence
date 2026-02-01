import random
from colorama import init, Fore, Style

init(autoreset=True)

def display_choices():
    print()
    print(Fore.YELLOW + "1. Rock")
    print(Fore.YELLOW + "2. Paper")
    print(Fore.YELLOW + "3. Scissors")
    print()

def get_choice_name(choice):
    if choice == 1:
        return Fore.RED + "Rock"
    if choice == 2:
        return Fore.BLUE + "Paper"
    if choice == 3:
        return Fore.GREEN + "Scissors"

def player_choice():
    while True:
        try:
            choice = int(input(Fore.CYAN + "Enter your choice (1-3): "))
            if choice in (1, 2, 3):
                return choice
            else:
                print(Fore.RED + "Invalid choice. Pick between 1 and 3.")
        except ValueError:
            print(Fore.RED + "Invalid input. Enter a number.")

def ai_choice():
    return random.randint(1, 3)

def check_winner(player, ai):
    if player == ai:
        return "Tie"
    if (player == 1 and ai == 3) or (player == 2 and ai == 1) or (player == 3 and ai == 2):
        return "Player"
    return "AI"

def rock_paper_scissors():
    print(Fore.MAGENTA + Style.BRIGHT + "Rock Paper Scissors Game")

    while True:
        display_choices()
        player = player_choice()
        ai = ai_choice()

        print()
        print(Fore.GREEN + "Player chose: " + get_choice_name(player))
        print(Fore.RED + "AI chose: " + get_choice_name(ai))
        print()

        result = check_winner(player, ai)

        if result == "Player":
            print(Fore.GREEN + "Player wins!")
        elif result == "AI":
            print(Fore.RED + "AI wins!")
        else:
            print(Fore.YELLOW + "It's a tie!")

        play_again = input(Fore.CYAN + "Do you want to play again? (yes/no): ").strip().lower()
        if play_again != "yes":
            print(Fore.MAGENTA + "Thank you for playing!")
            break

if __name__ == "__main__":
    rock_paper_scissors()
