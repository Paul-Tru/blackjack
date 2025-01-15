import customtkinter as ctk
import generate_number as gen_num

usr_cards:list = []
usr_sum:int = 0

def setup():
    global usr_sum, usr_cards
    for _ in range(2):
        card = gen_num.card()
        usr_sum = usr_sum + card
        usr_cards.append(card)

    curr_num_label.configure(text=usr_sum)

def hit():
    global usr_sum, usr_cards

    card = gen_num.card()
    if card == 11 and card + usr_sum > 21:
        card = 1
    usr_sum = usr_sum + card
    curr_num_label.configure(text=usr_sum)

    if usr_sum > 21:
        if 11 in usr_cards:
            usr_cards.remove(11)
            usr_cards.append(1)
            usr_sum = usr_sum - 10
            curr_num_label.configure(usr_sum)
        else:
            end(f"Bust\n {usr_sum}")

    usr_cards.append(card)

    print(usr_cards, usr_sum)

def stand():
    dealer_num, dealer_over, dealer_cards = gen_num.dealer()
    print(dealer_cards)
    if dealer_over:
        end(f"Dealer busted\n\n"
            f"{dealer_num}")
    else:
        if dealer_num == usr_sum:
            end(f"Push\n\n"
                f"Dealer: {dealer_num} You: {usr_sum}")
        elif dealer_num > usr_sum:
            end(f"You lost\n\n"
                f"Dealer: {dealer_num}\n"
                f"You: {usr_sum}")
        elif dealer_num < usr_sum:
            end(f"You won!\n\n"
                f"You: {usr_sum}\n"
                f"Dealer: {dealer_num}\n")

def end(text):
    curr_num_label.configure(text=text,
                             font=("Arial", 30, "bold"))
    hit_btn.configure(text="Replay", command=replay)
    stand_btn.configure(text="Close", command=close)

def replay():
    global usr_sum, usr_cards
    usr_sum = 0
    usr_cards = []
    gen_num.reset()
    setup()
    hit_btn.configure(text="Hit", command=hit)
    stand_btn.configure(text="Stand", command=stand)

def close():
    app.destroy()

app = ctk.CTk()

curr_num_label = ctk.CTkLabel(app, text="0",
                              font=("Arial",50, "bold"))
curr_num_label.grid(row=0, column=0, columnspan=3, sticky="we",
                    padx=15, pady=8)
setup()

usr_cards_label = ctk.CTkLabel(app, text="",
                               font=("Arial", 25))
usr_cards_label.grid(row=1, column=0, columnspan=3, sticky="we",
                     padx=15, pady=3)

hit_btn = ctk.CTkButton(app, text="Hit", command=hit)
hit_btn.grid(row=2, column=0,
             padx=15, pady=10)

stand_btn = ctk.CTkButton(app, text="Stand", command=stand)
stand_btn.grid(row=2, column=2,
               padx=15, pady=10)

app.mainloop()
