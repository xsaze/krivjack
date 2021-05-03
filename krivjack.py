import random
import time
#DECK BUILDING
deck_strings = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']
deck_values = [11,2,3,4,5,6,7,8,9,10,10,10,10,11,2,3,4,5,6,7,8,9,10,10,10,10,11,2,3,4,5,6,7,8,9,10,10,10,10,11,2,3,4,5,6,7,8,9,10,10,10,10]
hearts = '♥'
spades = '♠'
diamonds = '♦'
clubs = '♣'
deck_hearts = [sub + hearts for sub in deck_strings]
deck_spades = [sub + spades for sub in deck_strings]
deck_diamonds = [sub + diamonds for sub in deck_strings]
deck_clubs = [sub + clubs for sub in deck_strings]
deck = list(deck_hearts+deck_spades+deck_diamonds+deck_clubs)
deck_dict = dict(zip(deck,deck_values))
#-------------------------------------------------------------
#Dealing cards
def deal_cards(): #Option to add amount to bet in ()
    # DEALER
    global deck_inplay, d1, d2, d_hand_string, d_hand_value, dealer, p1, p2, p_hand_string, p_hand_value, aces, p_hand_list, d_hand_list, bet, balance, balance_string
    aces = ['A♠', 'A♥', 'A♣', 'A♦']
    deck_inplay = list(deck)
    d1 = random.choice(deck_inplay)
    deck_inplay.remove(d1)
    d2 = random.choice(deck_inplay)
    deck_inplay.remove(d2)
    d_hand_string = '|' + str(d1) + '|??|'
    d_hand_value = deck_dict[d1] + deck_dict[d2]  # Dealer hand value
    dealer = "\nDEALER:" + '{}'.format(d_hand_string)
    # PLAYER
    p1 = random.choice(deck_inplay)
    deck_inplay.remove(p1)
    p2 = random.choice(deck_inplay)
    deck_inplay.remove(p2)
    p_hand_string = '|' + str(p1) + '|' + str(p2) + '|'
    p_hand_value = deck_dict[p1] + deck_dict[p2]  # Player hand value
    p_hand_list = [p1, p2]
    d_hand_list = [d1, d2]
    print('\n'*80)
    balance_string = str('Balance:' + str(balance))
    print(balance_string)
    bet = input('Choose amount to bet: ')
    bet = int(bet)
    if balance < bet:
        bet = input('Insufficient funds. Please deposit or choose other amount: ')
        bet = int(bet)
    balance = balance - bet
    balance_string = str('Balance:' + str(balance))
    check_bj()
#Check for blackjack
def check_bj():
    global framework, balance
    player = "\nPLAYER:{:<55} {:<3}:{}".format(p_hand_string,'TOTAL',(p_hand_value))
    framework = (line+'\n')*6 + dealer + '\n' + player + '\n' + line+'\n' + balance_string
    print('\n*80')
    print(framework)
    if p_hand_value == 21:
        print("Blackjack! You win!\n Press any key to start a new game.")
        input()
        balance += bet*2.5
        deal_cards()
    else:
        player_choice()
def dealer_bj():
    global framework, balance
    dealer = "\nDEALER:{:<55} {:<3}:{}".format(d_hand_string,'TOTAL',(d_hand_value))
    framework = (line+'\n')*6 + dealer + '\n' + player + '\n' + line+'\n' + balance_string
    print('\n*80')
    print(framework)
    if d_hand_value == 21:
        print("Dealer has blackjack! You lose!\n Press any key to start a new game.")
        input()
        deal_cards()
    else:
        dealer_turn()

#PLAYER TURN
def player_choice(): #PLAYER TURN
    global p_hand_string, p_hand_value, player, framework, aces, p_hand_list, d_hand_string, balance
    check = any(card in p_hand_string for card in aces)
    #VISUAL\
    if check is True:
        player = "\nPLAYER:{:<55} {:<3}:{}/{}".format(p_hand_string,'TOTAL',(p_hand_value - 10),(p_hand_value))
    else:
        player = "\nPLAYER:{:<55} {:<3}:{}".format(p_hand_string,'TOTAL',(p_hand_value))
    choice_message = '\nPress a number to: [1] Hit, [2] Stand'
    framework = (line + '\n') * 6 + dealer + '\n' + player + '\n' + line + '\n' + balance_string
    print('\n*80')
    print(framework)
    #VISUAL/
    if p_hand_value > 21:
        if check is True:
            p_hand_value -= 10
            card_remove = ([i for i in p_hand_list if i in aces])
            aces.remove(card_remove[0])
            player_choice()
        else:
            print('BUST! You lose!')
            input('Press any key to start new game')
            deal_cards()
    print(choice_message)
    choice = int(input())
    if choice == 1:
        new_card = random.choice(deck_inplay)
        p_hand_string += str(new_card) + '|'
        p_hand_value += deck_dict[new_card]
        p_hand_list.append(new_card)
    if choice == 2:
        d_hand_string = '|' + str(d1) + '|' + str(d2) + '|'
        dealer_bj()
        return
    player_choice()
def dealer_turn():
    global d_hand_string, d_hand_value, dealer, player, framework, aces, d_hand_list, bet, balance

    #Visual

    check = any(card in d_hand_string for card in aces)
    if check is True:
        dealer = "\nDEALER:{:<55} {:<3}:{}/{}".format(d_hand_string,'TOTAL',(d_hand_value - 10),(d_hand_value))
    else:
        dealer = "\nDEALER:{:<55} {:<3}:{}".format(d_hand_string,'TOTAL',(d_hand_value))
    framework = (line+'\n')*6 + dealer + '\n' + player + '\n' + line+'\n' + balance_string
    print('\n*80')
    print(framework)

    #Logic

    if d_hand_value > 21:
        if check is True:
            d_hand_value -= 10
            card_remove = ([i for i in d_hand_list if i in aces])
            aces.remove(card_remove[0])
            dealer_turn()
        else:
            print('Dealer busts. You win!')
            input('Press any key to start new game')
            balance += bet*2
            deal_cards()
    if d_hand_value < 17:
        new_card = random.choice(deck_inplay)
        d_hand_string += str(new_card) + '|'
        d_hand_value += deck_dict[new_card]
        d_hand_list.append(new_card)
    else:
        if p_hand_value > d_hand_value:
            print('You win!')
            input('Press any key to start new game')
            balance += bet*2
            deal_cards()
        elif p_hand_value == d_hand_value:
            print('Draw!')
            balance += bet
        else:
            print('You lose!')
            input('Press any key to start new game')
            deal_cards()
    time.sleep(1.5)
    dealer_turn()


balance=100
line = '========================================================================='
deal_cards()




