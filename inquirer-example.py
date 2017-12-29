#!/usr/bin/env python

import inquirer
questions = [
  inquirer.List('size',
                message="What size do you need?",
                choices=['Jumbo', 'Large', 'Standard', 'Medium', 'Small', 'Micro'],
            ),
]
answers = inquirer.prompt(questions)
print answers["size"]

# files = dict((str(i), f) for i, f in
#               enumerate(f for f in os.listdir(path) if f.endswith(('.tgz','.tar'))))
# for item in sorted(files.items()):
#     print '[%s] %s' % item
# choice = None
# while choice is None:
#     choice = files.get(raw_input('Enter selection'))
#     if not choice:
#         print 'Please make a valid selection'
