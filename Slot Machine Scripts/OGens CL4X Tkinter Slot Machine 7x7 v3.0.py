import secrets
import time
import json
import os
import tkinter as tk
from tkinter import messagebox, simpledialog
from colorama import init, Fore, Style
import math

# Initialize colorama
init()

# Define slot machine symbols
SYMBOLS = ["🍒", "🔔", "🍋", "7️⃣", "⭐", "💎", "🍉", "🍊"]
REELS = 7  # 7 reels
ROWS = 7   # 7 rows
SYMBOL_COUNT = len(SYMBOLS)

# Payout table
PAYOUTS = {
    "🍒": 1,
    "🔔": 2,
    "🍋": 1,
    "7️⃣": 4,
    "⭐": 3,
    "💎": 6,
    "🍉": 1,
    "🍊": 1
}

# Bonus and jackpot settings
BONUS_TRIGGER = ["💎"] * REELS
FREE_SPINS = 5
JACKPOT_BASE = 1000
JACKPOT_INCREMENT = 1

# Emoji to text mapping
SYMBOL_TO_IMAGE = {
    "🍒": "Cherry", "🔔": "Bell", "🍋": "Lemon", "7️⃣": "Seven",
    "⭐": "Star", "💎": "Diamond", "🍉": "Watermelon", "🍊": "Orange"
}

# Store items
STORE_ITEMS = {
    "Extra Spin": {"cost": 50, "description": "Gain 1 extra spin"},
    "Balance Boost": {"cost": 100, "description": "Add 100 coins to balance"},
    "Jackpot Boost": {"cost": 200, "description": "Increase jackpot by 500 coins"},
    "Free Spins Purchase": {"cost": 250, "description": "Trigger 5 free spins"},
    "Mystery Prize": {"cost": 75, "description": "Receive a random reward: 50-100 coins, 50-100 credits, or an extra spin"},
    "Bonus Spin Chance": {"cost": 100, "description": "Increase the chance of triggering free spins by 10% for your next spin"}
}

def load_game():
    """Load player data from a file."""
    try:
        if os.path.exists("slot_machine_save.json"):
            with open("slot_machine_save.json", "r") as f:
                data = json.load(f)
                return (
                    int(data.get("balance", 100)),
                    int(data.get("jackpot", JACKPOT_BASE)),
                    data.get("stats", {"spins": 0, "wins": 0, "total_won": 0, "total_bet": 0}),
                    int(data.get("extra_spins", 0)),
                    int(data.get("credits", 0))
                )
    except (json.JSONDecodeError, IOError) as e:
        print(f"{Fore.RED}Failed to load save file: {e}. Starting new game.{Style.RESET_ALL}")
    return 100, JACKPOT_BASE, {"spins": 0, "wins": 0, "total_won": 0, "total_bet": 0}, 0, 0

def save_game(balance, jackpot, stats, extra_spins, credits):
    """Save player data to a file."""
    try:
        data = {"balance": int(balance), "jackpot": int(jackpot), "stats": stats, "extra_spins": int(extra_spins), "credits": int(credits)}
        with open("slot_machine_save.json", "w") as f:
            json.dump(data, f)
    except IOError as e:
        print(f"{Fore.RED}Failed to save game: {e}.{Style.RESET_ALL}")

def reset_game():
    """Delete JSON files and reset game state."""
    try:
        for file in ["slot_machine_save.json", "leaderboard.json"]:
            if os.path.exists(file):
                os.remove(file)
        return 100, JACKPOT_BASE, {"spins": 0, "wins": 0, "total_won": 0, "total_bet": 0}, 0, 0
    except OSError as e:
        print(f"{Fore.RED}Failed to reset game: {e}.{Style.RESET_ALL}")
        return 100, JACKPOT_BASE, {"spins": 0, "wins": 0, "total_won": 0, "total_bet": 0}, 0, 0

def load_leaderboard():
    """Load leaderboard from a file."""
    try:
        if os.path.exists("leaderboard.json"):
            with open("leaderboard.json", "r") as f:
                return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []
    return []

def save_leaderboard(score, name):
    """Save high score to leaderboard (top 5)."""
    leaderboard = load_leaderboard()
    leaderboard.append({"name": name, "score": int(score)})
    leaderboard = sorted(leaderboard, key=lambda x: x["score"], reverse=True)[:5]
    try:
        with open("leaderboard.json", "w") as f:
            json.dump(leaderboard, f)
    except IOError as e:
        print(f"{Fore.RED}Failed to save leaderboard: {e}.{Style.RESET_ALL}")

def spin_reels():
    """Spin the reels and return a 7x7 grid of random symbols using true randomness."""
    return [[secrets.choice(SYMBOLS) for _ in range(REELS)] for _ in range(ROWS)]

def check_paylines(reels, bet):
    """Check all 40 paylines for wins, including wild substitutions, and award random credits."""
    payout = 0
    win_lines = []
    extra_credits = 0
    paylines = [
        # Horizontal paylines (7 rows)
        [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6)],  # Row 1
        [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6)],  # Row 2
        [(2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6)],  # Row 3
        [(3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6)],  # Row 4
        [(4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6)],  # Row 5
        [(5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6)],  # Row 6
        [(6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6)],  # Row 7
        # Vertical paylines (7 columns)
        [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0)],  # Column 1
        [(0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1)],  # Column 2
        [(0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2)],  # Column 3
        [(0, 3), (1, 3), (2, 3), (3, 3), (4, 3), (5, 3), (6, 3)],  # Column 4
        [(0, 4), (1, 4), (2, 4), (3, 4), (4, 4), (5, 4), (6, 4)],  # Column 5
        [(0, 5), (1, 5), (2, 5), (3, 5), (4, 5), (5, 5), (6, 5)],  # Column 6
        [(0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6)],  # Column 7
        # Diagonal paylines
        [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6)],  # Top-left to bottom-right
        [(0, 6), (1, 5), (2, 4), (3, 3), (4, 2), (5, 1), (6, 0)],  # Top-right to bottom-left
        # V-shape paylines
        [(0, 0), (1, 1), (2, 2), (3, 3), (4, 2), (5, 1), (6, 0)],  # V-shape 1
        [(0, 6), (1, 5), (2, 4), (3, 3), (4, 4), (5, 5), (6, 6)],  # V-shape 2
        # Zigzag paylines
        [(0, 0), (1, 2), (2, 4), (3, 6), (4, 4), (5, 2), (6, 0)],  # Zigzag 1
        [(0, 6), (1, 4), (2, 2), (3, 0), (4, 2), (5, 4), (6, 6)],  # Zigzag 2
        # Inverted V-shape paylines
        [(0, 0), (1, 1), (2, 2), (3, 1), (4, 2), (5, 3), (6, 4)],  # Inverted V 1
        [(0, 6), (1, 5), (2, 4), (3, 5), (4, 4), (5, 3), (6, 2)],  # Inverted V 2
        # W-shape paylines
        [(0, 0), (1, 1), (2, 0), (3, 1), (4, 0), (5, 1), (6, 0)],  # W-shape 1
        [(0, 6), (1, 5), (2, 6), (3, 5), (4, 6), (5, 5), (6, 6)],  # W-shape 2
        # Shorter paylines (4 or 5 symbols)
        [(0, 0), (0, 1), (0, 2), (0, 3)],  # 4-symbol horizontal (row 1, left)
        [(0, 3), (0, 4), (0, 5), (0, 6)],  # 4-symbol horizontal (row 1, right)
        [(3, 0), (3, 1), (3, 2), (3, 3), (3, 4)],  # 5-symbol horizontal (row 4, left)
        [(0, 0), (1, 0), (2, 0), (3, 0)],  # 4-symbol vertical (column 1, top)
        [(3, 3), (4, 3), (5, 3), (6, 3)],  # 4-symbol vertical (column 4, bottom)
        [(0, 2), (1, 3), (2, 4), (3, 5), (4, 6)],  # 5-symbol diagonal
        # Additional paylines to reach 40 (10 new paylines)
        [(0, 0), (1, 2), (2, 1), (3, 3), (4, 5), (5, 4), (6, 6)],  # Zigzag 3
        [(0, 6), (1, 4), (2, 5), (3, 3), (4, 1), (5, 2), (6, 0)],  # Zigzag 4
        [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 5)],  # Diagonal variant 1
        [(0, 5), (1, 4), (2, 3), (3, 2), (4, 1), (5, 0), (6, 1)],  # Diagonal variant 2
        [(0, 0), (1, 0), (2, 1), (3, 2), (4, 1), (5, 0), (6, 0)],  # M-shape 1
        [(0, 6), (1, 6), (2, 5), (3, 4), (4, 5), (5, 6), (6, 6)],  # M-shape 2
        [(2, 0), (2, 1), (2, 2), (2, 3)],  # 4-symbol horizontal (row 3, left)
        [(4, 3), (4, 4), (4, 5), (4, 6)],  # 4-symbol horizontal (row 5, right)
        [(0, 1), (1, 1), (2, 1), (3, 1), (4, 1)],  # 5-symbol vertical (column 2, top)
        [(2, 5), (3, 5), (4, 5), (5, 5), (6, 5)]   # 5-symbol vertical (column 6, bottom)
    ]
    for i, line in enumerate(paylines):
        symbols = [reels[row][col] for row, col in line]
        ref_symbol = next((s for s in symbols if s != "💎"), symbols[0])
        if all(s == ref_symbol or s == "💎" for s in symbols):
            multiplier = PAYOUTS.get(ref_symbol, 0)
            if len(line) < 7 and ref_symbol in ["🍒", "🍋", "🍉", "🍊"]:
                multiplier = 1
            else:
                multiplier = multiplier // 2 if len(line) < 7 else multiplier
            line_payout = math.floor(bet * multiplier)
            payout += line_payout
            extra_credits += secrets.randbelow(50) + 1
            win_lines.append((i + 1, ref_symbol, line_payout, line))
    return payout, win_lines, extra_credits

def check_bonus(reels, bonus_chance=False):
    """Check if any row triggers the bonus (seven 💎), with optional increased chance."""
    if bonus_chance:
        for row in reels:
            if row == BONUS_TRIGGER:
                return True
        return False
    middle_row = reels[3]
    return middle_row == BONUS_TRIGGER

def check_jackpot(bet, jackpot):
    """Check for a jackpot win (1 in 1000 chance for bets 1-100)."""
    if 1 <= bet <= 100 and secrets.randbelow(1000) == 0:
        return int(jackpot)
    return 0

class SlotMachineGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Python Slot Machine (7x7)")
        self.root.configure(bg="black")
        self.root.geometry("800x600")
        self.root.update()
        self.player_name = simpledialog.askstring("Player Name", "Enter your name:", parent=self.root)
        if not self.player_name or self.player_name.strip() == "":
            self.player_name = "Player"

        self.balance, self.jackpot, self.stats, self.extra_spins, self.credits = load_game()
        self.bet = min(1, self.balance)
        self.spinning = False
        self.is_extra_spin = False
        self.bonus_chance = False

        # Reel labels (7x7 grid)
        self.reel_labels = [[tk.Label(root, text="🎰", font=("Arial", 14), fg="yellow", bg="black", width=3, height=2, borderwidth=1, relief="groove")
                            for _ in range(REELS)] for _ in range(ROWS)]
        for i in range(ROWS):
            for j in range(REELS):
                self.reel_labels[i][j].grid(row=i, column=j, padx=1, pady=1)

        # Balance, credits, jackpot, bet, and extra spins display
        self.balance_label = tk.Label(root, text=f"Balance: {self.balance} coins", font=("Arial", 7, "bold"), fg="white", bg="black")
        self.balance_label.grid(row=ROWS, column=0, columnspan=REELS, pady=1)

        self.credits_label = tk.Label(root, text=f"Credits: {self.credits}", font=("Arial", 7, "bold"), fg="white", bg="black")
        self.credits_label.grid(row=ROWS+1, column=0, columnspan=REELS, pady=1)

        self.jackpot_label = tk.Label(root, text=f"Jackpot: {self.jackpot} coins", font=("Arial", 7, "bold"), fg="white", bg="black")
        self.jackpot_label.grid(row=ROWS+2, column=0, columnspan=REELS, pady=1)

        self.bet_label = tk.Label(root, text=f"Bet: {self.bet} coin(s)", font=("Arial", 7, "bold"), fg="white", bg="black")
        self.bet_label.grid(row=ROWS+3, column=0, columnspan=REELS, pady=1)

        self.spins_label = tk.Label(root, text=f"Extra Spins: {self.extra_spins}", font=("Arial", 7, "bold"), fg="white", bg="black")
        self.spins_label.grid(row=ROWS+4, column=0, columnspan=REELS, pady=1)

        # Bet adjustment
        tk.Label(root, text="Bet Amount:", font=("Arial", 7, "bold"), fg="white", bg="black").grid(row=ROWS+5, column=0, pady=1)
        self.bet_entry = tk.Entry(root, width=4, font=("Arial", 7, "bold"))
        self.bet_entry.insert(0, str(self.bet))
        self.bet_entry.grid(row=ROWS+5, column=1, pady=1)
        self.bet_plus = tk.Button(root, text="+", command=self.increase_bet, bg="green", fg="white", activebackground="lightgreen", font=("Arial", 7, "bold"))
        self.bet_plus.grid(row=ROWS+5, column=2, sticky="w", padx=1)
        self.bet_minus = tk.Button(root, text="-", command=self.decrease_bet, bg="green", fg="white", activebackground="lightgreen", font=("Arial", 7, "bold"))
        self.bet_minus.grid(row=ROWS+5, column=2, sticky="e", padx=1)

        # Stats display
        self.stats_label = tk.Label(root, text=self.get_stats_text(), font=("Arial", 7, "bold"), fg="white", bg="black", justify="left")
        self.stats_label.grid(row=0, column=REELS, rowspan=3, padx=3, sticky="n")

        # Store display
        tk.Label(root, text="Store:", font=("Arial", 7, "bold"), fg="white", bg="black").grid(row=3, column=REELS, sticky="n", padx=3)
        self.store_listbox = tk.Listbox(root, height=6, width=30, font=("Arial", 7), bg="black", fg="white", selectbackground="blue", selectforeground="white")
        self.store_listbox.grid(row=4, column=REELS, rowspan=2, padx=3, sticky="n")
        for item, details in STORE_ITEMS.items():
            self.store_listbox.insert(tk.END, f"{item}: {details['cost']} credits - {details['description']}")
        self.buy_button = tk.Button(root, text="Buy Item", command=self.buy_item, bg="yellow", fg="black", activebackground="lightyellow", font=("Arial", 7, "bold"))
        self.buy_button.grid(row=6, column=REELS, pady=1)

        # Payline display
        self.payline_label = tk.Label(root, text="Paylines: None", font=("Arial", 7, "bold"), fg="white", bg="black", justify="left")
        self.payline_label.grid(row=0, column=REELS+1, rowspan=3, padx=3, sticky="n")

        # Status display
        self.status_label = tk.Label(root, text="Welcome! Press Spin to play!", font=("Arial", 7, "bold"), fg="blue", bg="black")
        self.status_label.grid(row=ROWS+6, column=0, columnspan=REELS+2, pady=1)

        # Buttons
        self.spin_button = tk.Button(root, text="Spin", command=self.spin, bg="red", fg="white", activebackground="pink", font=("Arial", 7, "bold"))
        self.spin_button.grid(row=ROWS+7, column=0, columnspan=2, pady=1)
        self.quit_button = tk.Button(root, text="Quit", command=self.quit, bg="purple", fg="white", activebackground="violet", font=("Arial", 7, "bold"))
        self.quit_button.grid(row=ROWS+7, column=2, pady=1)
        self.leaderboard_button = tk.Button(root, text="Leaderboard", command=self.show_leaderboard, bg="blue", fg="white", activebackground="lightblue", font=("Arial", 7, "bold"))
        self.leaderboard_button.grid(row=ROWS+7, column=3, columnspan=1, pady=1)
        self.reset_button = tk.Button(root, text="Reset", command=self.reset_game_prompt, bg="orange", fg="white", activebackground="lightyellow", font=("Arial", 7, "bold"))
        self.reset_button.grid(row=ROWS+7, column=4, columnspan=1, pady=1)

    def get_stats_text(self):
        """Return formatted stats text."""
        win_rate = (self.stats['wins'] / self.stats['spins'] * 100) if self.stats['spins'] > 0 else 0
        return (f"📊 {self.player_name}'s Stats\n"
                f"Spins: {self.stats['spins']}\n"
                f"Wins: {self.stats['wins']}\n"
                f"Won: {self.stats['total_won']}\n"
                f"Bet: {self.stats['total_bet']}\n"
                f"Win Rate: {win_rate:.1f}%")

    def get_leaderboard_text(self):
        """Return formatted leaderboard text."""
        leaderboard = load_leaderboard()
        text = "🏆 Leaderboard\n"
        for i, entry in enumerate(leaderboard, 1):
            text += f"{i}. {entry['name']}: {entry['score']} coins\n"
        return text if leaderboard else "No high scores yet!"

    def show_leaderboard(self):
        """Display leaderboard in a message box."""
        messagebox.showinfo("Leaderboard", self.get_leaderboard_text())

    def reset_game_prompt(self):
        """Prompt for confirmation before resetting the game."""
        if messagebox.askyesno("Reset Game", "Are you sure you want to reset the game? This will delete all progress!"):
            self.balance, self.jackpot, self.stats, self.extra_spins, self.credits = reset_game()
            self.bet = min(1, self.balance)
            self.bet_entry.delete(0, tk.END)
            self.bet_entry.insert(0, str(self.bet))
            self.balance_label.config(text=f"Balance: {self.balance} coins")
            self.credits_label.config(text=f"Credits: {self.credits}")
            self.jackpot_label.config(text=f"Jackpot: {self.jackpot} coins")
            self.bet_label.config(text=f"Bet: {self.bet} coin(s)")
            self.spins_label.config(text=f"Extra Spins: {self.extra_spins}")
            self.stats_label.config(text=self.get_stats_text())
            self.payline_label.config(text="Paylines: None")
            self.status_label.config(text="Game reset! Ready to spin!", fg="blue")
            for i in range(ROWS):
                for j in range(REELS):
                    self.reel_labels[i][j].config(bg="black", fg="yellow")
            save_game(self.balance, self.jackpot, self.stats, self.extra_spins, self.credits)

    def increase_bet(self):
        """Increase bet by 1, up to 100 or current balance."""
        if self.bet < 100 and self.bet < self.balance:
            self.bet += 1
            self.bet_entry.delete(0, tk.END)
            self.bet_entry.insert(0, str(self.bet))
            self.bet_label.config(text=f"Bet: {self.bet} coin(s)")

    def decrease_bet(self):
        """Decrease bet by 1, down to 1."""
        if self.bet > 1:
            self.bet -= 1
            self.bet_entry.delete(0, tk.END)
            self.bet_entry.insert(0, str(self.bet))
            self.bet_label.config(text=f"Bet: {self.bet} coin(s)")

    def buy_item(self):
        """Handle purchasing an item from the store using credits."""
        selection = self.store_listbox.curselection()
        if not selection:
            messagebox.showerror("Error", "Please select an item to purchase!")
            return
        item_name = list(STORE_ITEMS.keys())[selection[0]]
        item = STORE_ITEMS[item_name]
        if self.credits < item["cost"]:
            messagebox.showerror("Error", "Insufficient credits to purchase this item!")
            return
        self.credits -= item["cost"]

        if item_name == "Extra Spin":
            self.extra_spins += 1
            self.spins_label.config(text=f"Extra Spins: {self.extra_spins}")
            self.status_label.config(text="Purchased Extra Spin!", fg="blue")
        elif item_name == "Balance Boost":
            self.balance += 100
            self.balance_label.config(text=f"Balance: {self.balance} coins")
            self.status_label.config(text="Purchased Balance Boost! +100 coins", fg="blue")
        elif item_name == "Jackpot Boost":
            self.jackpot += 500
            self.jackpot_label.config(text=f"Jackpot: {self.jackpot} coins")
            self.status_label.config(text="Purchased Jackpot Boost! +500 to jackpot", fg="blue")
        elif item_name == "Free Spins Purchase":
            self.free_spins_mode(spin_reels())
            self.status_label.config(text="Purchased Free Spins! Enjoy 5 spins!", fg="blue")
        elif item_name == "Mystery Prize":
            prize_type = secrets.randbelow(3)
            if prize_type == 0:
                prize = secrets.randbelow(51) + 50
                self.balance += prize
                self.balance_label.config(text=f"Balance: {self.balance} coins")
                self.status_label.config(text=f"Mystery Prize: {prize} coins!", fg="blue")
            elif prize_type == 1:
                prize = secrets.randbelow(51) + 50
                self.credits += prize
                self.credits_label.config(text=f"Credits: {self.credits}")
                self.status_label.config(text=f"Mystery Prize: {prize} credits!", fg="blue")
            else:
                self.extra_spins += 1
                self.spins_label.config(text=f"Extra Spins: {self.extra_spins}")
                self.status_label.config(text="Mystery Prize: 1 extra spin!", fg="blue")
        elif item_name == "Bonus Spin Chance":
            self.bonus_chance = True
            self.status_label.config(text="Bonus Spin Chance active for next spin!", fg="blue")

        self.credits_label.config(text=f"Credits: {self.credits}")
        save_game(self.balance, self.jackpot, self.stats, self.extra_spins, self.credits)
        if self.bet > self.balance:
            self.bet = max(1, self.balance) if self.balance >= 1 else 0
            self.bet_entry.delete(0, tk.END)
            self.bet_entry.insert(0, str(self.bet))
            self.bet_label.config(text=f"Bet: {self.bet} coin(s)")

    def animate_spin(self, iterations=10, delay=100):
        """Simulate spinning reels with cycling symbols."""
        if iterations <= 0:
            self.spinning = False
            self.finalize_spin()
            return
        for i in range(ROWS):
            for j in range(REELS):
                current = self.reel_labels[i][j].cget("text")
                next_idx = (SYMBOLS.index(current) + 1) % SYMBOL_COUNT if current in SYMBOLS else 0
                self.reel_labels[i][j].config(text=SYMBOLS[next_idx], bg="black", fg="yellow")
        self.status_label.config(text="*Spinning sounds* Whirr... Click!", fg="blue")
        self.root.after(delay, lambda: self.animate_spin(iterations - 1, delay))

    def finalize_spin(self):
        """Display final reel results and process spin."""
        reels = spin_reels()
        for i in range(ROWS):
            for j in range(REELS):
                self.reel_labels[i][j].config(text=reels[i][j], bg="black", fg="yellow")

        payout, win_lines, extra_credits = check_paylines(reels, self.bet)
        jackpot_payout = check_jackpot(self.bet, self.jackpot)
        self.balance += payout + jackpot_payout
        self.credits += extra_credits
        self.stats["spins"] += 1
        self.stats["total_bet"] += self.bet if not self.is_extra_spin else 0

        payline_text = "Paylines: "
        status_text = ""
        if win_lines:
            payline_text += ", ".join(f"{line_num} ({SYMBOL_TO_IMAGE[symbol]})" for line_num, symbol, _, _ in win_lines)
            for _, _, _, line in win_lines:
                for row, col in line:
                    self.reel_labels[row][col].config(bg="lightgreen", fg="yellow")
            self.stats["wins"] += 1
            self.stats["total_won"] += payout + extra_credits
            status_text = f"Won {payout} coins + {extra_credits} credits on {len(win_lines)} payline(s)!"
            self.status_label.config(text=status_text, fg="green")
        elif jackpot_payout:
            self.stats["wins"] += 1
            self.stats["total_won"] += payout + extra_credits
            self.jackpot = JACKPOT_BASE
            status_text = f"JACKPOT! Won {jackpot_payout} coins!"
            self.status_label.config(text=status_text, fg="purple")
            save_leaderboard(self.balance, self.player_name)
            for i in range(ROWS):
                for j in range(REELS):
                    self.reel_labels[i][j].config(bg="gold", fg="yellow")
        else:
            status_text = "No win this time. Try again!"
            self.status_label.config(text=status_text, fg="red")
            payline_text += "None"

        self.payline_label.config(text=payline_text)

        if check_bonus(reels, self.bonus_chance):
            self.free_spins_mode(reels)
        self.bonus_chance = False

        self.balance_label.config(text=f"Balance: {self.balance} coins")
        self.credits_label.config(text=f"Credits: {self.credits}")
        self.jackpot_label.config(text=f"Jackpot: {self.jackpot} coins")
        self.bet_label.config(text=f"Bet: {self.bet} coin(s)")
        self.spins_label.config(text=f"Extra Spins: {self.extra_spins}")
        self.stats_label.config(text=self.get_stats_text())
        save_game(self.balance, self.jackpot, self.stats, self.extra_spins, self.credits)

        if self.bet > self.balance:
            self.bet = max(1, self.balance) if self.balance >= 1 else 0
            self.bet_entry.delete(0, tk.END)
            self.bet_entry.insert(0, str(self.bet))
            self.bet_label.config(text=f"Bet: {self.bet} coin(s)")

        if self.balance <= 0 and self.extra_spins <= 0:
            save_leaderboard(self.balance, self.player_name)
            messagebox.showinfo("Game Over", f"You're out of coins and spins!\n{self.get_leaderboard_text()}")
            self.quit()

    def free_spins_mode(self, initial_reels):
        """Run free spins mode."""
        self.status_label.config(text=f"BONUS! {FREE_SPINS} Free Spins!", fg="blue")
        self.root.update()
        time.sleep(1)
        free_spin_winnings = 0
        for spin in range(FREE_SPINS):
            self.status_label.config(text=f"Free Spin {spin + 1}/{FREE_SPINS}...", fg="blue")
            self.root.update()
            time.sleep(0.5)
            reels = spin_reels()
            for i in range(ROWS):
                for j in range(REELS):
                    self.reel_labels[i][j].config(text=reels[i][j], bg="black", fg="yellow")
            payout, win_lines, extra_credits = check_paylines(reels, self.bet)
            free_spin_winnings += payout + extra_credits
            self.credits += extra_credits
            self.stats["spins"] += 1
            if win_lines:
                self.stats["wins"] += 1
                self.stats["total_won"] += payout + extra_credits
                for _, _, _, line in win_lines:
                    for row, col in line:
                        self.reel_labels[row][col].config(bg="lightgreen", fg="yellow")
            self.stats_label.config(text=self.get_stats_text())
            self.payline_label.config(text="Paylines: " + (", ".join(f"{line_num} ({SYMBOL_TO_IMAGE[symbol]})" for line_num, symbol, _, _ in win_lines) if win_lines else "None"))
            self.root.update()
            time.sleep(0.5)
        self.balance += free_spin_winnings
        self.status_label.config(text=f"Free Spins Done! Won {free_spin_winnings} coins", fg="blue")
        self.balance_label.config(text=f"Balance: {self.balance} coins")
        self.credits_label.config(text=f"Credits: {self.credits}")
        save_leaderboard(self.balance, self.player_name)
        save_game(self.balance, self.jackpot, self.stats, self.extra_spins, self.credits)

        if self.bet > self.balance:
            self.bet = max(1, self.balance) if self.balance >= 1 else 0
            self.bet_entry.delete(0, tk.END)
            self.bet_entry.insert(0, str(self.bet))
            self.bet_label.config(text=f"Bet: {self.bet} coin(s)")

    def spin(self):
        """Handle spin button click."""
        if self.spinning:
            return
        try:
            self.bet = int(self.bet_entry.get())
            if self.bet < 1 or self.bet > 100:
                messagebox.showerror("Error", "Bet must be between 1 and 100 coins!")
                return
            if self.bet > self.balance:
                messagebox.showerror("Error", "Bet cannot exceed your balance!")
                return
            self.is_extra_spin = False
            if self.extra_spins > 0:
                self.extra_spins -= 1
                self.spins_label.config(text=f"Extra Spins: {self.extra_spins}")
                self.status_label.config(text="Using extra spin!", fg="blue")
                self.is_extra_spin = True
            else:
                self.balance -= self.bet
                self.jackpot += self.bet * JACKPOT_INCREMENT
            self.spinning = True
            self.animate_spin()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number!")

    def quit(self):
        """Handle quit button click."""
        save_leaderboard(self.balance, self.player_name)
        messagebox.showinfo("Thanks for Playing!", f"Final balance: {self.balance} coins\n{self.get_stats_text()}\n\n{self.get_leaderboard_text()}")
        save_game(self.balance, self.jackpot, self.stats, self.extra_spins, self.credits)
        self.root.quit()

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = SlotMachineGUI(root)
        root.mainloop()
    except Exception as e:
        print(f"{Fore.RED}Game crashed: {e}. Please check tkinter setup.{Style.RESET_ALL}")