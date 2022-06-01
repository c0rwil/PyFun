import sys

bitmap = """
....................................................................
    *****************************************************************
   ********************* ** **    * **** ****  **   ************ 
  **      *****************       ******************************
           *************          **  * **** ** ************** *
        *    *********    *        *******   **************** * *
             ********        ** **  ***************************  *
    *        * **** ***  *     **  *************** ******  ** *
                ****  *         ***************   *** ***  *
     *         **    ******         *************    **   **  *
      *            ********        *************    *  ** ***
       *     **        ********         ********          * *** ****
                    *********         ******  *        **** ** * **
          **          *********         ****** * *           *** *   *
                      ******          ***** **             *****   *
        **              *****            **** *            ********
                     *****             ****              *********
      **        **       ****              **                 *******   *
                     ***         *                      *        *    *
 *   *         **     *      ***              *
...................................................................."""

print('Bitmap Message')
print('Enter the words to display with the bitmap.')
message = input('> ')
if message == '':
    sys.exit()

# Loop over each line in the bitmap:
for line in bitmap.splitlines():
    # Loop over each character in the line:
    for x, bit in enumerate(line):
        if bit == ' ':
            # Print an empty space since there's a space in the bitmap:
            print(' ', end='')
        else:
            # Print a character from the message:
            print(message[x % len(message)], end='')
    print()  # Print a newline.