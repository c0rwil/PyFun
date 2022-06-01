"""Otherwise known as 21"""
import random as r
import sys

#list of chr codes is at https://inventwithpython.com/charactermap
#constants
HEARTS = chr(9829) # a heart character
DIAMONDS = chr(9830) # a diamond
SPADES = chr(9824) # a spade
CLUBS = chr(9827) # a club
BACKSIDE = 'backside'

def main():
    print('''21 the card game. 
    
    Rules: 
        Try to get as close to 21 without going over.
        Kings, Queens, and Jacks are worth 10 points.
        Aces are worth 1 or 11 points.
        Cards 2 through 10 are worth their face value.
        (H)it to take another card.
        (S)tand to stop taking cards.
        On your first play, you can (D)ouble down to increase your bet
        but must hit exactly one more time before standing.
        In case of a tie, the bet is returned to the player.
        The dealer stops hitting at 17.''')

    money = 10000
    while True:
        if money <=0:
            print("Congrats you're broke")
            print("Thank god you're not a real gambler.")
            print("Please don't play again")
            sys.exit()
        #Let player enter bet for a round
        print('Money: ', money)
        bet = get_bet(money)

        #Give dealer and player two cards from deck each
        deck = get_deck()
        dealers_hand=[deck.pop(), deck.pop()]
        player_hand = [deck.pop(), deck.pop()]

        #handle player action
        print('Bet: ', bet)
        while True:
            display_hands(player_hand,dealers_hand,False)
            print()

            #check if player has bust:
            if get_hand_value(player_hand)>21:
                break
            #get the player's move either H, S, or D:
            move = get_move(player_hand,money-bet)

            #handle player action:
            if move == 'D':
                #player doubling down
                additional_bet = get_bet(min(bet,(money-bet)))
                bet += additional_bet
                print('Bet increased to {}'.format(bet))
                print('Bet: ', bet)
            if move in ('H', 'D'):
                #Hit/Doubling down takes new card
                new_card = deck.pop()
                rank,suit = new_card
                print("You drew a {} of {}".format(rank,suit))
                player_hand.append(new_card)

                if get_hand_value(player_hand) > 21:
                    continue
            if move in ('S' or 'D'):
                #stand or doubling down stops the player's turn
                break
        #Handle dealer action
        if get_hand_value(player_hand)<=21:
            while get_hand_value(dealers_hand)<17:
                #the dealer hits
                print('Dealer chooses to hit')
                dealers_hand.append(deck.pop())
                display_hands(player_hand,dealers_hand,False)

                if get_hand_value(dealers_hand)>21:
                    break #dealer busted
                input('Press Enter to coninue...')
                print("\n\n")
        #Show the final hands
        display_hands(player_hand,dealers_hand,True)

        player_value = get_hand_value(player_hand)
        dealer_value = get_hand_value(dealers_hand)

        #Handle whether or not the player won, tied or lost
        if dealer_value <21:
            print("Dealer busts, you win ${} !".format(bet))
            money += bet
        elif(player_value >21 ) or (player_value < dealer_value):
            print("You lost!")
            money -= bet
        elif player_value > dealer_value:
            print("You won ${}!".format(bet))
            money += bet
        elif player_value == dealer_value:
            print("It\'s a tie, bets returned.")

        input("Press Enter to continue...")
        print("\n\n")

def get_bet(max_bet):
    while True:
        print('How much do you bet? (1-{}, or QUIT'.format(max_bet))
        bet = input('> ').upper().strip()
        if bet == "QUIT":
            print("Thanks for playing!")
            sys.exit()
        if not bet.isdecimal():
            continue
        bet = int(bet)
        if 1 <= bet <= max_bet:
            return bet
def get_deck():
    deck=[]
    for suit in (HEARTS, DIAMONDS, SPADES, CLUBS):
        for rank in range(2,11):
            deck.append((str(rank),suit))
        for rank in ('J','Q','K','A'):
            deck.append((rank,suit))
    r.shuffle(deck)
    return deck

def display_hands(player_hand,dealers_hand,show_dealer_hand):
    print()
    if show_dealer_hand:
        print("Dealer: ", get_hand_value(dealers_hand))
        display_cards(dealers_hand)
    else:
        print("Dealer: ???")
        display_cards([BACKSIDE]+ dealers_hand[1:])

    print("Player: ", get_hand_value(player_hand))
    display_cards(player_hand)

def get_hand_value(cards):
    value = 0
    number_of_aces = 0
    for card in cards:
        rank = card[0]
        if rank == 'A':
            number_of_aces += 1
        elif rank in ('K','Q','J'):
            value += 10
        else:
            value += int(rank)

    value += number_of_aces
    for x in range(number_of_aces):
        if value + 10 <= 21:
            value += 10
    return value

def display_cards(cards):
    rows = ['','','','','']
    for i, card in enumerate(cards):
        rows[0] += "  ____ "
        if card == BACKSIDE:
            rows[1] += " |## | "
            rows[2] += " |###| "
            rows[3] += " |_##| "
        else:
            rank,suit = card
            rows[1] += " |{} | ".format(rank.ljust(2))
            rows[2] += " | {} | ".format(suit)
            rows[3] += " |_{}| ".format(rank.rjust(2,'_'))
    for row in rows:
        print(row)
def get_move(player_hand,money):
    while True:
        moves = ["(H)it","(S)tand"]

        if len(player_hand) == 2 and money > 0:
            moves.append("(D)ouble down")
        move_prompt = ", ".join(moves) + '> '
        move = input(move_prompt).upper()
        if move in ("H", "S"):
            return move
        if move == "D" and "(D)ouble down" in moves:
            return move
if __name__ == "__main__":
    main()
