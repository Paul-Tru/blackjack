import logging
import customtkinter as ctk
import game

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%d-%m-%Y %H:%M:%S"
)

coins = 1000

def hit(event=None):
    result = game.hit()

    if isinstance(result, tuple):
        usr_sum, usr_cards = result
        curr_num_label.configure(text=str(usr_sum))
        usr_cards_label.configure(text=", ".join(map(str, usr_cards)))  # Fix
    else:
        end(result)


def stand(event=None):
    winner = game.stand()
    end(winner)


def end(text):
    curr_num_label.configure(text=text, font=("Arial", 30, "bold"))
    usr_cards_label.configure(text=", ".join(map(str, game.usr_cards)))

    hit_btn.configure(text="Replay", command=replay)
    stand_btn.configure(text="Close", command=close)


def replay(event=None):
    global usr_sum, usr_cards
    game.reset()
    game.setup()

    hit_btn.configure(text="Hit", command=hit)
    stand_btn.configure(text="Stand", command=stand)

    curr_num_label.configure(text=str(game.usr_sum))
    usr_cards_label.configure(text=", ".join(map(str, game.usr_cards)))


def close():
    app.destroy()


app = ctk.CTk()
app.title("Blackjack")

# grid configuration for dynamic sizing
app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=1)
app.grid_columnconfigure(2, weight=1)

app.grid_rowconfigure(1, weight=1)
app.grid_rowconfigure(2, weight=1)
app.grid_rowconfigure(3, weight=1)

fullscreen:bool = False
shifted:bool = False

def is_fullscreen(event=None):
    global fullscreen
    found_window_state:bool = (app.winfo_width() >= app.winfo_screenwidth() and
                          app.winfo_height() >= app.winfo_screenheight())
    if fullscreen is not found_window_state:
        fullscreen = found_window_state
        logging.debug(f"Window state changed, fullscreen: {fullscreen}")

        if fullscreen:
            shift_elements_right()

app.bind("<Configure>", is_fullscreen)

def shift_elements_right():
    for widget in app.winfo_children():
        info = widget.grid_info()
        if "column" in info:
            widget.grid(column=info["column"] + 1)

def normalize_elements():
    global shifted
    if shifted:
        for widget in app.winfo_children():
            info = widget.grid_info()
            if "column" in info:
                widget.grid(column=info["column"] - 1)
        shifted = False


coins_label = ctk.CTkLabel(app, text=f"Coins: {str(coins)}",
                           font=("Arial", 12))
coins_label.grid(row=0, column=0,
                 padx=15, pady=8)

coins_label = ctk.CTkLabel(app, text=f"Coins: {coins}", font=("Arial", 12))
coins_label.grid(row=0, column=0, padx=15, pady=8)

curr_num_label = ctk.CTkLabel(app, text=str(game.usr_sum), font=("Arial", 50, "bold"))
curr_num_label.grid(row=1, column=0, columnspan=3, sticky="we", padx=15, pady=8)

usr_cards_label = ctk.CTkLabel(app, text=", ".join(map(str, game.usr_cards)), font=("Arial", 20))  # Fix
usr_cards_label.grid(row=2, column=0, columnspan=3, sticky="we", padx=15, pady=3)

hit_btn = ctk.CTkButton(app, text="Hit", command=hit)
hit_btn.grid(row=3, column=0, padx=15, pady=10)

stand_btn = ctk.CTkButton(app, text="Stand", command=stand)
stand_btn.grid(row=3, column=2, padx=15, pady=10)

usr_sum, usr_cards = game.setup()
curr_num_label.configure(text=str(game.usr_sum))
usr_cards_label.configure(text=", ".join(map(str, game.usr_cards)))

def handle_return(event):
    if hit_btn.cget("text") == "Hit":
        hit()
    else:
        replay()

app.bind("<space>", handle_return)
app.bind("<Return>", stand)

app.mainloop()
