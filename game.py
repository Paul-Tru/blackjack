import random
import logging

cards_original:list = [2, 2, 2, 2,
                       3, 3, 3, 3,
                       4, 4, 4, 4,
                       5, 5, 5, 5,
                       6, 6, 6, 6,
                       7, 7, 7, 7,
                       8, 8, 8, 8,
                       9, 9, 9, 9,
                       10, 10, 10, 10,
                       10, 10, 10, 10,
                       10, 10, 10, 10,
                       10, 10, 10, 10,
                       11, 11, 11, 11]

cards: list = cards_original.copy()

dealer_cards: list = []
dealer_sum: int = 0

def dealer_first_card():
    global dealer_cards, dealer_sum
    logging.debug("Setting up Dealer's first card")
    dealer_card = draw_card()
    dealer_cards.append(dealer_card)
    dealer_sum = dealer_sum + dealer_card
    cards.remove(dealer_card)

def dealer():
    global dealer_sum, dealer_cards, dealer_over
    logging.debug("Setting up Dealer")

    while dealer_sum < 17:
        dealer_card = draw_card()
        dealer_sum = dealer_sum + dealer_card
        dealer_cards.append(dealer_card)
        if dealer_sum > 21:
            if dealer_card == 11 and dealer_card + dealer_sum > 21:
                logging.debug("Dealer: Got two aces")
                dealer_sum = dealer_sum - 10
                dealer_cards.remove(11)
                dealer_cards.append(1)
            else:
                break

    return dealer_sum, dealer_cards

def draw_card():
    logging.debug("Getting random card")
    card = random.choice(cards)
    cards.remove(card)
    return card

usr_cards: list = []
usr_sum: int = 0

def setup():
    global usr_sum, usr_cards

    dealer_first_card()
    usr_cards = []
    usr_sum = 0

    for _ in range(2):
        new_card = draw_card()
        usr_sum += new_card
        usr_cards.append(new_card)

    return usr_sum, usr_cards

def hit():
    global usr_sum, usr_cards

    usr_card = draw_card()

    usr_sum = usr_sum + usr_card

    if usr_sum > 21:
        if 11 in usr_cards:
            logging.debug("User: Got ace")
            usr_cards.remove(11)
            usr_cards.append(1)
            usr_sum = usr_sum - 10
        else:
            logging.info(f"User: Bust ({usr_sum}: {usr_cards})")
            usr_cards.append(usr_card)
            return f"Bust\n {usr_sum}"

    usr_cards.append(usr_card)
    logging.info(f"User: Hit ({usr_sum}: {usr_cards})")
    return usr_sum, usr_cards

def stand():
    global dealer_sum, dealer_cards
    logging.info(f"User: Stand ({usr_sum}: {usr_cards})")
    dealer()
    logging.info(f"Dealer: Cards: {dealer_sum}: {dealer_cards}")

    if dealer_sum > 21:
        return f"Dealer busted\n\nDealer: {dealer_sum}"
    elif dealer_sum == usr_sum:
        return f"Push\n\nBoth: {usr_sum}"
    elif dealer_sum > usr_sum:
        return f"You lost\n\nDealer: {dealer_sum}\nYou: {usr_sum}"
    else:
        return f"You won!\n\nYou: {usr_sum}\nDealer: {dealer_sum}"

def reset():
    logging.debug("Resetting cards...")
    global cards, cards_original, usr_sum, usr_cards, dealer_sum, dealer_cards
    cards = cards_original.copy()
    usr_sum = 0
    usr_cards = []

    dealer_sum = 0
    dealer_cards = []
