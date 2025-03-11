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

cards:list = cards_original.copy()

def dealer():
    logging.debug("Setting up Dealer")
    dealer_num: int = 0
    dealer_over: bool = False
    dealer_cards: list = []

    while dealer_num < 17:
        card = random.choice(cards)
        cards.remove(card)
        dealer_num = dealer_num + card
        dealer_cards.append(card)
        dealer_over = False
        if dealer_num > 21:
            if card == 11 and card + dealer_num > 21:
                logging.debug("Dealer: Got two aces")
                dealer_num = dealer_num - 10
                dealer_cards.remove(11)
                dealer_cards.append(1)
            else:
                dealer_over = True
                break
    return dealer_num, dealer_over, dealer_cards

def card():
    logging.debug("Getting random card")
    card = random.choice(cards)
    cards.remove(card)
    return card

def reset():
    logging.debug("Resetting cards...")
    global cards, cards_original
    cards = cards_original.copy()
