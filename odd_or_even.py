
# Ask the user for a number. Depending on whether the number is even or odd, print out an appropriate message to the user. Hint: how does an even / odd number react differently when divided by 2?

# created by : Santo K. Thomas

while True:
    try:
        n = int(input('Please input a number'))
        break
    except:
        print('invalid input')
        continue
if n%2 == 0:
    print('\n\nYou have inputed the number {} which is an even number'.format(n))
else:
    print('\n\nYou have inputed the number {} which is an odd number'.format(n))