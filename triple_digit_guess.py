"""Pentaseer game: Guess the 5 digit password to win. You have 15 chances."""
import random
GUESS_ALLOWANCE = 15
DIGIT_COUNT = 5


def main():
    print(''' A classic game archetype with a thematic twist. Pentaseer is a guessing game.
    
    You need to correctly guess the {} digit password that contains no repeated digit.
    The key for this cipher is:
    
    'Pock'      signifies that a given digit is present in the password but has been entered at the wrong index.
    'Ziko'      signifies that a given digit is both present and in the correct index, in other words, a correct guess.
    'Wani'      signifies that no digit is correct.
    
    In example, if the password was 30149 and your input was 94102, the clues would be .'''.format(DIGIT_COUNT))
    while True: #loop for game

        root_password =                                                              get_root_password()
        print("You found the lock.")
        print("You have {} chances to crack it".format(GUESS_ALLOWANCE))
        chances_wasted = 1

        while chances_wasted <= GUESS_ALLOWANCE:
            attempt = ''
            while len(attempt) != DIGIT_COUNT or not attempt.isdecimal():
                print('Attempt #{}:'.format(chances_wasted))
                attempt = input('> ')

            hints = get_hints(attempt, root_password)
            chances_wasted += 1
            print(hints)

            if attempt == root_password:
                break #leave game loop, game over if they guessed it
            if chances_wasted > GUESS_ALLOWANCE:
                print('You failed to crack the password in time')
                print('The answer was {}'.format(root_password))

        print("Would you like to try again? (yes or no)")
        if not input('> ').upper().startswith('Y'):
            break
    print("Nice try, at least you attempted what most could not.")

def get_root_password():
    """Returns a string made up of a certain amount of unique randomized digits"""
    digits = list('0123456789') #list 0-9
    random.shuffle(digits) #shuffles digits

    #get first digits in the list for secret number
    root_password=''

    for x in range(DIGIT_COUNT):
      root_password += str(digits[x])

    return root_password


def get_hints(attempt, root_password):
    """Will return a string with the key words
    being utilized to implement a hint and password pairing"""
    if attempt == root_password:
        return 'Nice job!'
    hints = []

    for x in range(len(attempt)):
        if attempt[x] == root_password[x]:
            #something is right
            hints.append('Ziko')
        elif attempt[x] in root_password:
            #something is right but in the wrong place
            hints.append('Pock')
    if len(hints) == 0:
        return 'Wani' #no correct guesses whatsoever
    else:
        #sort hints in alphabetical order
        hints.sort()
        #make single string from list of hints
        return ' '.join(hints)


#If ran instead of imported
if __name__ == '__main__':
    main()