

from prompter import yesno

done = False
while not done:
    try:
        i = int(raw_input("Integer? "))
        done = True
    except ValueError:
        continueit=yesno('Continue? ')
        if continueit:
            done = False
        else:
            done = True
            
