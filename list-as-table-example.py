
import os


def pselect(choices):
    """Ask a user to select one of the enumerated choices. Return the selection."""
    enumerated_choices = dict((i, f) for i, f in enumerate(f for f in choices))
    str_choices=["{: >3} {:<}".format(k,v) for k,v in sorted(enumerated_choices.items())]
    choice = None
    while choice is None:
        for a, b, c in zip(str_choices[::3], str_choices[1::3], str_choices[2::3]):
            print '{:<30}{:<30}{:<}'.format(a, b, c)
        choice = enumerated_choices.get(int(raw_input("Selection? ")))
        if not choice:
            print 'Please make a valid selection'
        else:
            print 'You selected {:s}'.format(choice)

    return (choice)

path="."
print pselect(os.listdir(path))


# files=dict((i, f) for i,f in
#     enumerate(f for f in os.listdir(path) if f.endswith(('.py', '.txt'))))

# print files
# l = files.items()
# l = ["{: >3} {:<}".format(k,v) for k,v in sorted(files.items())]

# l = ['exiv2-devel', 'mingw-libs', 'tcltk-demos', 'fcgi', 'netcdf',
#     'pdcurses-devel',     'msvcrt', 'gdal-grass', 'iconv', 'qgis-devel',
#     'qgis1.1', 'php_mapscript']

#foolist = l



# choice = None
# while choice is None:
#     for a, b, c in zip(foolist[::3], foolist[1::3], foolist[2::3]):
#         print '{:<30}{:<30}{:<}'.format(a, b, c)
#     choice = files.get(int(raw_input('Enter selection: ')))
#     if not choice:
#         print 'Please make a valid selection'
#     else:
#         print "You selected {:s}".format(choice)




#
# if len(l) % 2 != 0:
#     l.append(" ")
#
# split = len(l)/2
# l1 = l[0:split]
# l2 = l[split:]
# for key, value in zip(l1,l2):
# #    print '%-20s %s' % (key, value) )      #python <2.6
#    print "{0:<20s}      {1}".format(key, value) #python 2.6+