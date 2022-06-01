"""Birthday Paradox Simulation
 originally created by Al Sweigart and used as the basis
  for my personal take on this game"""
import random as r
import datetime as dt

def get_birthdates(bday_count):
    """Returns a list of random date objects for bdays."""
    birthdates = []
    for i in range(bday_count):
        year_start = dt.date(2000,1,1)

        random_day_number = dt.timedelta(r.randint(0,364))
        birthdate= year_start + random_day_number
        birthdates.append(birthdate)
    return birthdates

def find_match(birthdates):
    """Returns the date object of a bdaythat occurs more than once."""
    if len(birthdates)==len(set(birthdates)):
        return None #all unique bdays
    #compare each bday to every other
    for x, birthdate1 in enumerate(birthdates):
        for y, birthdate2 in enumerate(birthdates[x + 1 :]):
            if birthdate1 == birthdate2:
                return birthdate1

#Intro display
print('''Birthday Paradox shows us that in a group of X people, the odds
 of two people having a birthday on the same day is larger than one would expect
 Here we utilize my personal implementation of the Monte Carlo simulation to further delve into this topic''')

MONTHS = ('Jan','Feb','Mar','Apr','May','Jun',
          'Jul','Aug','Sep','Oct','Nov','Dec')

while True: #continue to ask until valid input
    print('How many birthdates should we generate?')
    reply = input('> ')
    if reply.isdecimal() and (0 < int(reply) <= 1000):
        bday_count = int(reply)
        break
print()

print('Here are ',bday_count, ' birthdays: ')
birthdates = get_birthdates(bday_count)
for x, birthdate in enumerate(birthdates):
    if x != 0:
        print(', ', end='')
    month_name = MONTHS[birthdate.month-1]
    date_text = "{} {}".format(month_name, birthdate.day)
    print(date_text, end = '')
print()
print()

#determine a match
gemini = find_match(birthdates)

print('In this simulation, ' , end='')
if gemini != None:
    month_name=MONTHS[gemini.month-1]
    date_text = '{} {}'.format(month_name, gemini.day)
    print('multiple people have a birthday on ', date_text)
else:
    print("There are no matching birthdays.")
print()

#Run through 100,000 simulatons:
print('Generating',bday_count, 'random birthdays 100,000 times...')
input("Press enter to begin...")

print("Let\'s run another 100,000 simulations")
simul_match = 0 #how many matching bdays within the simulation
for i in range(100000):
    #report every 10,000 parses
    if i % 10000 == 0:
        print(i," simulations run...")
    birthdates = get_birthdates(bday_count)
    if find_match(birthdates) != None:
        simul_match = simul_match + 1
print('100,000 simulations completed')

#Display simulation results:
probability = round(simul_match/100000 * 100, 2)
print('Out of 100,000 simulations of', bday_count, 'people, there was a')
print('matching birthday in that group', simul_match, 'times. This means')
print('that', bday_count, 'people have a', probability, '% chance of')
print('having a matching birthday in their group.')
