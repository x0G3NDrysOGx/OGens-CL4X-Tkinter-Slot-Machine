# Slot Machine Game README (8x8 Version)

## Overview
This is an advanced Python-based slot machine game with an 8x8 grid, featuring 50 paylines, a variety of Fantasy RPG-themed symbols, and engaging mechanics such as regular spins, free spins, a jackpot, extra credits, and an in-game store. Built using `tkinter` for the GUI and `secrets` for true randomness, the game offers an immersive experience with persistent player data, a leaderboard, and customizable bets. Players can win coins and credits, track stats, and purchase items, including a Mystery Prize and Sage’s Wisdom, to enhance gameplay.

## Game Features

### Game Setup
- **Grid**: 8 reels × 8 rows, displaying 64 symbols per spin.
- **Symbols**: 🗡️ (Sword), 🛡️ (Shield), 📜 (Scroll), 💍 (Ring), 🔥 (Fire), 🏰 (Castle, also the wild symbol), ⚔️ (Crossed Swords), 🧙 (Wizard).
- **Paylines**: 50 predefined paylines (horizontal, vertical, diagonal, and patterns like V-shape, zigzag, W-shape, and inverted V-shape) checked for wins.
- **Currency**:
  - **Coins**: Used for betting and added to the balance when won.
  - **Credits**: Earned from winning paylines and used to purchase items in the store.
- **Persistence**: Player data (balance, jackpot, stats, extra spins, credits) is saved to `slot_machine_save.json`. Leaderboard data is saved to `leaderboard.json`.
- **Randomness**: Uses `secrets` module for cryptographically secure random symbol selection and credit generation.

### Betting and Spinning
- **Bet Adjustment**: Players set bets (1–100 coins) via a text entry or +/- buttons, limited by their balance. The bet can be adjusted without spinning.
- **Regular Spins**: Deduct the bet amount from the balance (unless using an extra spin) and increment the jackpot by 1 coin per bet (`JACKPOT_INCREMENT = 1`).
- **Extra Spins**: Can be used instead of regular spins, costing no coins and not contributing to the jackpot. Obtained by purchasing from the store (50 credits) or via the Mystery Prize (1-in-3 chance). Extra spins provide the same win opportunities as regular spins (paylines, extra credits, or free spins trigger).
- **Free Spins**: Triggered by eight 🏰 symbols in the middle row or by purchasing from the store, granting 5 free spins (`FREE_SPINS = 5`). Free spins use the current bet for payouts but do not deduct from the balance.

### Payline Wins
When a payline is hit (i.e., all symbols in a payline are the same or include the wild symbol 🏰), the payout is calculated as:
**Payout = floor(Bet × Multiplier)** for the matching symbol, ensuring integer payouts.
The multipliers are defined in the `PAYOUTS` dictionary:
- 🗡️: 1x
- 🛡️: 2x
- 📜: 1x
- 💍: 4x
- 🔥: 3x
- 🏰: 6x
- ⚔️: 1x
- 🧙: 1x

For paylines with fewer than 8 symbols, the multiplier is halved (integer division) for symbols 🗡️, 📜, ⚔️, and 🧙; otherwise, the full multiplier applies.
**Example**: If your bet is 10 coins and you hit an 8-symbol payline with 🗡️ symbols, you win `floor(10 × 1) = 10 coins`. For a 5-symbol payline with 🗡️, you win `floor(10 × (1 // 2)) = 0 coins`. For a 5-symbol payline with 💍, you win `floor(10 × (4 // 2)) = 20 coins`.

Multiple paylines can contribute to the total payout if multiple winning combinations are hit in a single spin. This applies to both **regular spins** and **free spins**.

### Extra Credits
For each winning payline, you also receive **random extra credits** (between 1 and 50, generated using `secrets.randbelow(50) + 1`). If Sage’s Wisdom is active, extra credits are doubled (2–100 per winning payline) for the next spin.
These credits are added to your total credits, which can be used to purchase items in the store (e.g., extra spins, balance boosts, Mystery Prize, or Sage’s Wisdom).

**Example**: If you hit two paylines in a single spin (e.g., one 🗡️ and one 🔥) with Sage’s Wisdom active, you might earn `floor(10 × 1) = 10 coins` (🗡️) + `floor(10 × 3) = 30 coins` (🔥) = 40 coins, plus, for example, 50 × 2 = 100 credits for the 🗡️ payline and 30 × 2 = 60 credits for the 🔥 payline, totaling 160 credits.

### Free Spins Mode
- **Trigger**: Activated by eight 🏰 symbols in the middle row (row 5, index 4, checked via `check_bonus`) or by purchasing "Free Spins Purchase" from the store.
- **Mechanics**: Grants 5 free spins, using the current bet (set before triggering) to calculate payouts. No coins are deducted from the balance.
- **Winnings**: Payouts from paylines and extra credits (1–50 per winning payline, or 2–100 if Sage’s Wisdom was active before triggering) accumulate over the 5 spins. Total coins are added to the balance, and credits are added to the credit balance at the end.
- **Stats**: Each free spin increments the `spins` stat. Winning paylines increment the `wins` stat and add to `total_won` (payouts + extra credits). The `total_bet` stat is not incremented.
- **Limitations**: No additional free spins or jackpot checks occur during free spins.

### Jackpot
- **Base Value**: Starts at 1000 coins (`JACKPOT_BASE = 1000`).
- **Increment**: Increases by 1 coin per bet in regular spins (`JACKPOT_INCREMENT = 1`).
- **Win Condition**: 1-in-1000 chance (`secrets.randbelow(1000) == 0`) for bets of 1–100 coins during regular spins (not free spins or extra spins).
- **Payout**: Awards the entire jackpot, which resets to 1000 coins after a win. The balance is updated, and the win is recorded in stats and the leaderboard.
- **Visuals**: Winning the jackpot highlights all reel symbols in gold.

### In-Game Store
Players can spend credits to purchase items, enhancing gameplay:
- **Extra Spin** (50 credits): Adds 1 extra spin, usable without deducting coins, offering a chance to win paylines, extra credits, or trigger free spins.
- **Balance Boost** (100 credits): Adds 100 coins to the balance.
- **Jackpot Boost** (200 credits): Increases the jackpot by 500 coins.
- **Free Spins Purchase** (250 credits): Triggers 5 free spins immediately.
- **Mystery Prize** (75 credits): Awards a random reward: 50–100 coins, 50–100 credits, or 1 extra spin (determined using `secrets.randbelow(3)` for type and `secrets.randbelow(51) + 50` for coin/credit amounts).
- **Sage’s Wisdom** (100 credits): Doubles extra credits (2–100 per winning payline) on the next spin, enhancing credit earnings without affecting coin payouts.
- **Mechanics**: Select an item from the store listbox and click "Buy Item." The purchase deducts credits and applies the effect. Insufficient credits trigger an error message.

### Stats and Leaderboard
- **Stats Tracking**:
  - **Spins**: Incremented for each regular, extra, or free spin.
  - **Wins**: Incremented for spins with at least one winning payline or a jackpot win.
  - **Total Won**: Sum of all coins and credits won from paylines, jackpots, and Mystery Prizes.
  - **Total Bet**: Sum of coins bet in regular spins (not extra or free spins).
  - **Win Rate**: Calculated as `(wins / spins) × 100` (0% if no spins).
- **Leaderboard**: Stores the top 5 high scores (balance) with player names in `leaderboard.json`. Updated on game quit, when the balance reaches zero (game over), or after a jackpot win.
- **Display**: Stats are shown in the GUI, and the leaderboard is accessible via a button, displayed in a pop-up.

### Game Interface
- **GUI**: Built with `tkinter`, featuring an 8x8 grid of reel labels, balance/credits/jackpot/bet/extra spins displays, a bet adjustment entry/buttons, a store listbox, payline/status displays, and buttons for Spin, Quit, Leaderboard, and Reset. The window size is 900x700 pixels.
- **Visual Feedback**:
  - Spins animate with cycling symbols for 10 iterations (100ms delay).
  - Winning paylines highlight in light green; jackpots highlight in gold.
  - Status messages indicate wins (green), losses (red), free spins (blue), or jackpots (purple). Sage’s Wisdom activation is shown in blue.
- **Player Name**: Prompted at game start (defaults to "Player" if empty).

### Game Flow
- **Start**: Load saved data or start with 100 coins, 1000-coin jackpot, 0 extra spins, 0 credits, and zeroed stats.
- **Spin**:
  - Regular spins deduct the bet and check for paylines, jackpot, or free spins.
  - Extra spins (if available) deduct no coins and can trigger paylines, extra credits, or free spins.
  - Free spins trigger on eight 🏰 symbols (middle row) or store purchase, running 5 spins.
- **Game Over**: Triggered when balance and extra spins reach zero, showing the leaderboard and final stats before quitting.
- **Quit**: Saves balance and leaderboard, showing final stats and leaderboard.
- **Reset**: Deletes save files, resetting balance to 100, jackpot to 1000, and stats/spins/credits to 0.

### Technical Details
- **Dependencies**: `tkinter`, `colorama`, `json`, `os`, `secrets`, `time`, `math`.
- **Files**:
  - `slot_machine_save.json`: Stores balance, jackpot, stats, extra spins, credits.
  - `leaderboard.json`: Stores top 5 high scores.
- **Error Handling**: Catches JSON/IO errors for loading/saving, `tkinter` setup issues, and invalid bet inputs (must be 1–100 and not exceed balance).
- **Randomness**: Uses `secrets` for secure random symbol selection, credit generation, jackpot checks, and Mystery Prize outcomes.
- **Payout Precision**: Uses `math.floor` to ensure integer payouts in `check_paylines`.

## Example Scenario
- **Setup**: Bet set to 10 coins, balance at 100 coins, 0 credits.
- **Regular Spin**:
  - Deducts 10 coins (balance: 90).
  - Hits two paylines (🗡️: `floor(10 × 1) = 10 coins`, 🔥: `floor(10 × 3) = 30 coins`) and earns 50 + 30 = 80 credits.
  - Total: 40 coins + 80 credits added (balance: 130, credits: 80).
  - Jackpot increases by 10 (to 1010).
- **Mystery Prize Purchase**:
  - Spend 75 credits (credits: 5).
  - Random outcome: Awards 80 coins (balance: 210), or 60 credits (credits: 65), or 1 extra spin (extra spins: 1).
- **Sage’s Wisdom Purchase**:
  - Spend 100 credits (credits: 0 or 65, depending on Mystery Prize).
  - Activates Sage’s Wisdom for the next spin, doubling extra credits for winning paylines.
- **Extra Spin** (if awarded by Mystery Prize):
  - Uses 1 extra spin (extra spins: 0), no coins deducted.
  - Hits 🔥 payline (`floor(10 × 3) = 30 coins`, 40 × 2 = 80 credits with Sage’s Wisdom). Balance: 240, credits: 80 or 145.
- **Free Spins** (triggered by eight 🏰 in middle row):
  - 5 spins, each checking paylines with 10-coin bet.
  - Spin 1: Hits 🗡️ payline (`floor(10 × 1) = 10 coins`, 50 credits or 100 credits with Sage’s Wisdom). Total so far: 10 coins, 50 or 100 credits.
  - Spin 2–5: No wins. Final: 10 coins added to balance (now 250), 50 or 100 credits added (now 90 or 155 or 245).
- **Store Purchase**: Spend 100 credits on Balance Boost, adding 100 coins (balance: 350, credits: 0 or 55 or 145).

This README provides a complete overview of the 8x8 slot machine game, covering payouts, extra credits, the Mystery Prize, Sage’s Wisdom, and all mechanics for regular and free spins, ensuring players understand how to play and what to expect from wins.