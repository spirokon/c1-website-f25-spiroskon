from bakery import assert_equal
from drafter import *
from dataclasses import dataclass, field
import random

def create_deck():
    """Makes a deck of normal cards. No args used."""
    deck = []
    suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
    ranks = ["2","3","4","5","6","7","8","9","10","J","Q","K","A"]
    for suit in suits:
        for rank in ranks:
            deck.append((rank, suit))
    random.shuffle(deck)
    return deck

def hand_value(hand):
    """Takes cards list. Gives number score."""
    total = 0
    aces = 0
    values = {"2":2,"3":3,"4":4,"5":5,"6":6,"7":7,"8":8,"9":9,
              "10":10,"J":10,"Q":10,"K":10,"A":11}

    for rank, suit in hand:
        total += values[rank]
        if rank == "A":
            aces += 1
    while total > 21 and aces > 0:
        total -= 10
        aces -= 1
    return total

def format_hand(hand):
    """Takes cards list. Shows text."""
    out = []
    for rank, suit in hand:
        out.append(rank + " of " + suit)
    return ", ".join(out)

def simulate_single_hand():
    """Plays one game and gives hands and result."""
    deck = create_deck()
    player = [deck.pop(), deck.pop()]
    dealer = [deck.pop(), deck.pop()]

    while hand_value(player) < 16:
        player.append(deck.pop())
    while hand_value(dealer) < 17:
        dealer.append(deck.pop())

    p = hand_value(player)
    d = hand_value(dealer)

    if p > 21:
        result = "You busted! Dealer wins."
    elif d > 21:
        result = "Dealer busts! You win!"
    elif p > d:
        result = "You win!"
    elif p < d:
        result = "Dealer wins."
    else:
        result = "Push (tie)."

    return {
        "player_hand": player,
        "dealer_hand": dealer,
        "player_total": p,
        "dealer_total": d,
        "result": result
    }

@dataclass
class State:
    last_result: str = ""
    logs: list[str] = field(default_factory=list)

@route
def home(s: State) -> Page:
    return Page(s, [
        Header("Welcome to Web Blackjack!", 1),
        Text("Play a single quick auto-hand against the dealer."),
        LineBreak(),
        Text("* Get close to 21 without going over"),
        Text("* Face cards = 10"),
        Text("* Ace = 1 or 11"),
        Text("* Dealer must hit to 17"),
        LineBreak(),
        Button("Play a hand", play),
        Button("History", history)
    ])

@route
def play(s: State) -> Page:
    game = simulate_single_hand()

    p_txt = "Your Hand: " + format_hand(game["player_hand"])
    d_txt = "Dealer Hand: " + format_hand(game["dealer_hand"])
    r_txt = game["result"]

    msg = p_txt + " | Total: " + str(game["player_total"]) + \
          " || " + d_txt + " | Total: " + str(game["dealer_total"]) + \
          " || " + r_txt
    s.logs.append(msg)
    s.last_result = r_txt

    return Page(s, [
        Header("Play Result", 2),
        Text(p_txt),
        Text("Total: " + str(game["player_total"])),
        LineBreak(),
        Text(d_txt),
        Text("Total: " + str(game["dealer_total"])),
        LineBreak(),
        Header("Result: " + r_txt, 3),
        LineBreak(),
        Button("Play Again", play),
        Button("Back Home", home),
        Button("History", history)
    ])

@route
def history(s: State) -> Page:
    stuff = [Header("History")]
    if not s.logs:
        stuff.append(Text("(no hands played yet)"))
    else:
        for x in s.logs:
            stuff.append(Text(x))
    stuff.append(LineBreak())
    stuff.append(Button("Clear", clear_history))
    stuff.append(Button("Back", home))
    return Page(s, stuff)

@route
def clear_history(s: State) -> Page:
    s.logs = []
    return home(s)

# Tests needed
assert_equal(True, home(State()) is not None)
assert_equal(True, simulate_single_hand() is not None)
assert_equal(type(create_deck()), list)
assert_equal(type(format_hand([("A","Hearts")])), str)

# Website Information (must be at bottom)
set_site_information(
    author="Spirokon@udel.edu",
    description="Blackjack website that auto plays a single hand against the dealer.",
    sources=["Drafter"],
    planning=["PlanningImage.jpg"],  
    links=[ 
        "https://github.com/spirokon/c1-website-f25-spiroskon/new/main"  
    ]
)

hide_debug_information()
set_website_title("Blackjack Web Game")
set_website_framed(False)

start_server(State())
