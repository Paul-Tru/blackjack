import logging
import customtkinter as ctk
import game

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%d-%m-%Y %H:%M:%S"
)

hit_var:bool = False

def setup():
    curr_num_label.configure(text="Play?")

def start():
    usr_sum, usr_cards = game.setup()
    curr_num_label.configure(text=str(usr_sum))
    usr_cards_label.configure(text=", ".join(map(str, usr_cards)))

def hit(event=None):
    global hit_var
    if hit:
        for widget in coins_frame.winfo_children():
            if isinstance(widget, ctk.CTkButton):
                widget.configure(state="disabled")
    else:
        for widget in coins_frame.winfo_children():
            if isinstance(widget, ctk.CTkButton):
                widget.configure(state="normal")

    result = game.hit()

    if isinstance(result, tuple):
        usr_sum, usr_cards = result
        curr_num_label.configure(text=str(usr_sum))
        usr_cards_label.configure(text=", ".join(map(str, usr_cards)))  # Fix
    else:
        end(result)

    update_coin_labels()
    hit_var = True


def stand(event=None):
    winner = game.stand()
    end(winner)
    update_coin_labels()


def end(text):
    curr_num_label.configure(text=text, font=("Arial", 30, "bold"))
    usr_cards_label.configure(text=", ".join(map(str, game.usr_cards)))

    hit_btn.configure(text="Replay", command=replay)
    stand_btn.configure(text="Close", command=close)


def replay(event=None):
    global usr_sum, usr_cards, hit_var
    game.reset()
    game.setup()

    hit_btn.configure(text="Hit", command=hit)
    stand_btn.configure(text="Stand", command=stand)

    curr_num_label.configure(text=str(game.usr_sum))
    usr_cards_label.configure(text=", ".join(map(str, game.usr_cards)))

    update_coin_labels()
    hit_var = False


def close(event=None):
    app.destroy()


def handle_percentage(input_percentage: float = None):
    if input_percentage is None:
        input_percentage = set_percentage_slider.get()

    input_percentage = int(input_percentage)
    percentage_label.configure(text=f"{input_percentage}%")

    if set_percentage_slider.get() != input_percentage:
        set_percentage_slider.set(input_percentage)

    game.usr_set_coins = int(game.usr_coins * (input_percentage/100))
    game.usr_coins = game.usr_coins - game.usr_set_coins
    update_coin_labels()
    start()

def update_coin_labels():
    coins_label.configure(text=f"Coins:\n {game.usr_coins}")
    set_coins_label.configure(text=f"Set coins:\n {game.usr_set_coins}")

def handle_return(event):
    if hit_btn.cget("text") == "Hit":
        hit()
    else:
        replay()

# gui
app = ctk.CTk()
app.title("Blackjack")

# grid configuration for dynamic sizing
app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=1)
app.grid_columnconfigure(2, weight=1)

app.grid_rowconfigure(1, weight=1)
app.grid_rowconfigure(2, weight=1)
app.grid_rowconfigure(3, weight=1)

# game frame
game_frame = ctk.CTkFrame(app)
game_frame.grid(row=0, column=1, columnspan=3, rowspan=3, sticky="nsew", padx=10, pady=8)

game_frame.grid_rowconfigure(3, weight=1)

curr_num_label = ctk.CTkLabel(game_frame, text=str(game.usr_sum), font=("Arial", 50, "bold"))
curr_num_label.grid(row=1, column=0, columnspan=3, sticky="n", padx=10, pady=20)

usr_cards_label = ctk.CTkLabel(game_frame, text=", ".join(map(str, game.usr_cards)), font=("Arial", 20))
usr_cards_label.grid(row=2, column=0, columnspan=3, padx=10, pady=3)

game_frame.grid_rowconfigure(3, weight=1)

hit_btn = ctk.CTkButton(game_frame, text="Hit", command=hit)
hit_btn.grid(row=4, column=0, padx=10, pady=10, sticky="sew")

stand_btn = ctk.CTkButton(game_frame, text="Stand", command=stand)
stand_btn.grid(row=4, column=2, padx=10, pady=10, sticky="sew")

# set coin frame
set_coin_frame = ctk.CTkTabview(app)
set_coin_frame.grid(row=2, column=0, sticky="nwes", padx=10, pady=8)

set_coin_frame.add("Percent")
ten_percent_btn = ctk.CTkButton(set_coin_frame.tab("Percent"), text="10%", command=lambda: handle_percentage(10))
ten_percent_btn.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

twenty_five_percent_btn = ctk.CTkButton(set_coin_frame.tab("Percent"), text="25%", command=lambda: handle_percentage(25))
twenty_five_percent_btn.grid(row=0, column=1, sticky="ew", padx=10, pady=10)

fifty_percent_btn = ctk.CTkButton(set_coin_frame.tab("Percent"), text="50%", command=lambda: handle_percentage(50))
fifty_percent_btn.grid(row=1, column=0, sticky="ew", padx=10, pady=10)

seventy_five_percent_btn = ctk.CTkButton(set_coin_frame.tab("Percent"), text="75%", command=lambda: handle_percentage(75))
seventy_five_percent_btn.grid(row=1, column=1, sticky="ew", padx=10, pady=10)

percentage_label = ctk.CTkLabel(set_coin_frame.tab("Percent"), text="50%", font=("Arial", 15))
percentage_label.grid(row=3, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

set_percentage_slider = ctk.CTkSlider(set_coin_frame.tab("Percent"), from_=0, to=100, command=handle_percentage)
set_percentage_slider.grid(row=2, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

set_coin_frame.add("Coins")

coins_frame = ctk.CTkFrame(app)
coins_frame.grid(row=0, column=0, sticky="new", padx=10, pady=8)
coins_label = ctk.CTkLabel(coins_frame, text=f"Coins:\n {game.usr_coins}", font=("Arial", 20))
coins_label.grid(row=0, column=0, padx=10, pady=8)

set_coins_frame = ctk.CTkFrame(app)
set_coins_frame.grid(row=1, column=0, sticky="sew", padx=10, pady=8)
set_coins_label = ctk.CTkLabel(set_coins_frame, text=f"Set coins:\n {game.usr_set_coins}", font=("Arial", 20))
set_coins_label.grid(row=0, column=0, padx=10, pady=8)

app.bind("<space>", handle_return)
app.bind("<Return>", stand)
app.bind("<Escape>", close)

setup()

app.mainloop()