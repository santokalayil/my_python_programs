
# Creator : Santo K. Thomas

'''Program that asks the user to enter their name and their age. Print out a message addressed to 
them that tells them the year that they will turn 100 years old.'''


import datetime
now = datetime.datetime.now()
this_year = now.year
name = str(input('Enter Your Name?'))

while True:
    try:
        age = int(input('Enter Your Age'))
        break

    except ValueError:
        print('\n\nSorry, I did not get your age! Please try again')
        continue
    
if age > 0:
    if age < 100:
        year = int(this_year+(100-age))
        print('\n\nYour Name is {} \nYour Age is {} \nYou will be turning 100 in the year {}'.format(name.title(), age, year))
    elif (age > 100) and (age <= 120):
        print('\n\nYour Name is {} \nYour Age is {} \nYour are have turned 100 in the year {}'.format(name.title(), age, this_year - (age-100)))
    elif age == 100:
        print('\n\nYou are now 100 years old')
    elif (age > 120) and (age <= 160):
        print('\n\nMy God! I think "You are older than oldest person living now"\nYour Name is {} \nYour Age is {} \nYour are have turned 100 in the year {}'.format(name.title(), age, this_year - (age-100)))
    else:
        print('\n\nI don"t think that you are human to have this lifespan')
else:
    print('\n\nNegative number in age! Please know that you cannot trick me')

