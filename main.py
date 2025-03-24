import logging
import customtkinter as ctk
import generate_cards as gen_card

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%d-%m-%Y %H:%M:%S"
)

usr_cards:list = []
usr_sum:int = 0
coins:int = 1000

def setup():
    global usr_sum, usr_cards

    gen_card.dealer_first_card()

    for _ in range(2):
        card = gen_card.card()
        usr_sum = usr_sum + card
        usr_cards.append(card)
        logging.info(f"User: Cards: {usr_sum}: {usr_cards}")

    curr_num_label.configure(text=usr_sum)
    usr_cards_label.configure(text=usr_cards)

def hit():
    global usr_sum, usr_cards

    logging.info(f"User: Hit ({usr_sum}: {usr_cards})")

    card = gen_card.card()

    usr_sum = usr_sum + card
    curr_num_label.configure(text=usr_sum)

    if usr_sum > 21:
        if 11 in usr_cards:
            logging.debug("User: Got ace")
            usr_cards.remove(11)
            usr_cards.append(1)
            usr_sum = usr_sum - 10
            curr_num_label.configure(text=usr_sum)
        else:
            logging.info(f"User: Bust ({usr_sum}: {usr_cards})")
            end(f"Bust\n {usr_sum}")

    usr_cards.append(card)
    usr_cards_label.configure(text=usr_cards)

def stand():
    logging.info(f"User: Stand ({usr_sum}: {usr_cards})")
    dealer_num, dealer_over, dealer_cards = gen_card.dealer()
    logging.info(f"Dealer: Cards: {dealer_num}: {dealer_cards}")
    usr_cards_label.configure(text=usr_cards)

    if dealer_over:
        logging.info(f"Dealer: Busted ({dealer_num}: {dealer_cards})")
        end(f"Dealer busted\n\n"
            f"{dealer_num}")
    else:
        if dealer_num == usr_sum:
            logging.info(f"Push ({usr_sum})")
            end(f"Push\n\n"
                f"Both: {usr_sum}")

        elif dealer_num > usr_sum:
            logging.info(f"User: Lost (Usr: {usr_sum} | Dlr: {dealer_num})")
            end(f"You lost\n\n"
                f"Dealer: {dealer_num}\n"
                f"You: {usr_sum}")

        elif dealer_num < usr_sum:
            logging.info(f"User: Won (Usr: {usr_sum} | Dlr: {dealer_num})")
            end(f"You won!\n\n"
                f"You: {usr_sum}\n"
                f"Dealer: {dealer_num}\n")

def end(text):
    curr_num_label.configure(text=text,
                             font=("Arial", 30, "bold"))

    usr_cards_label.configure(text="")

    hit_btn.configure(text="Replay", command=replay)
    stand_btn.configure(text="Close", command=close)

def replay():
    global usr_sum, usr_cards
    logging.debug("Resetting for new game")
    usr_sum = 0
    usr_cards = []

    gen_card.reset()
    setup()

    usr_cards_label.configure(text=usr_cards)

    hit_btn.configure(text="Hit", command=hit)
    stand_btn.configure(text="Stand", command=stand)

def close():
    logging.info("Closing...")
    app.destroy()

fullscreen:bool = False

app = ctk.CTk()
app.title("Blackjack")

# grid configuration for dynamic sizing
app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=1)
app.grid_columnconfigure(2, weight=1)

app.grid_rowconfigure(1, weight=1)
app.grid_rowconfigure(2, weight=1)
app.grid_rowconfigure(3, weight=1)

def is_fullscreen(event=None):
    global fullscreen
    found_window_state:bool = (app.winfo_width() >= app.winfo_screenwidth() and
                          app.winfo_height() >= app.winfo_screenheight())
    if fullscreen is not found_window_state:
        fullscreen = found_window_state
        logging.debug(f"Window state changed, fullscreen: {fullscreen}")

        if fullscreen:
            print(gen_card.cards)
            shift_elements_right()

app.bind("<Configure>", is_fullscreen)

def shift_elements_right():
    for widget in app.winfo_children():
        info = widget.grid_info()
        if "column" in info:
            widget.grid(column=info["column"] + 1)  # Spalte um 1 erhöhen


coins_label = ctk.CTkLabel(app, text=f"Coins: {str(coins)}",
                           font=("Arial", 12))
coins_label.grid(row=0, column=0,
                 padx=15, pady=8)

curr_num_label = ctk.CTkLabel(app, text=str(usr_sum),
                              font=("Arial",50, "bold"))
curr_num_label.grid(row=1, column=0, columnspan=3, sticky="we",
                    padx=15, pady=8)

usr_cards_label = ctk.CTkLabel(app, text=str(usr_cards),
                               font=("Arial", 20))
usr_cards_label.grid(row=2, column=0, columnspan=3, sticky="we",
                     padx=15, pady=3)

hit_btn = ctk.CTkButton(app, text="Hit", command=hit)
hit_btn.grid(row=3, column=0,
             padx=15, pady=10)

stand_btn = ctk.CTkButton(app, text="Stand", command=stand)
stand_btn.grid(row=3, column=2,
               padx=15, pady=10)

setup()

app.mainloop()
