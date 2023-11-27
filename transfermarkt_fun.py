transfer_dict={
    'all': 'alle',
    'summer': 'sommer',
    'winter': 'winter'
}
position_dict={
    'all':'',
    'goalkeepers':'Torwart',
    'defenders':'Abwehr',
    'midfielders':'Mittelfeld',
    'forward':'Sturm'
}
age_dict={
    'all':'',
    'u15':'u15',
    'u16':'u16',
    'u17':'u17',
    'u18':'u18',
    'u19':'u19',
    'u20':'u20',
    'u21':'u21',
    'u22':'u22',
    'u23':'u23',
    '23-30':'23-30',
    'o30':'o30',
    'o31':'o31',
    'o30':'o30',
    'o32':'o32',
    'o33':'o33',
    'o34':'o34',
    'o35':'o35'
}

def season_fun():
    season=input('Which season do you want to analyze (format xxxx/xxxx)? ')
    if not('/' in season):
        print('Input not valid. Use the indicated format.')
        return season_fun()
    elif int(season.split('/')[0])!=int(season.split('/')[1])-1:
        print('Input not valid. The indicated season does not exist.')
        return season_fun()
    elif not(int(season.split('/')[0])>1870):
        print('Input not valid. You cannot go before 1870.')
        return season_fun()
    else:
        print(f'You have selected season {season}.')
        return season

def transfer_window_fun():
    transfer_window=input('Which window are you interested in (all, summer, winter)? ')
    if not(transfer_window.lower() in transfer_dict.keys()):
        print('Input not valid (avoid spaces).')
        return transfer_window_fun()
    else:
        print(f'You have selected the following transfer window: {transfer_window}.')
        return transfer_window

def position_fun():
    position=input('Which position are you interested in (all, goalkeepers, defenders, midfielders, forwards)? ')
    if not(position.lower() in position_dict.keys()):
        print('Input not valid (avoid spaces).')
        return position_fun()
    else:
        print(f'You have selected the following position: {position}.')
        return position
def age_fun():
    age=input('Which position are you interested in (all, goalkeepers, defenders, midfielders, forwards)? ')
    if not(age.lower() in age_dict.keys()):
        print('Input not valid (avoid spaces).')
        return age_fun()
    else:
        print(f'You have selected the following age: {age}.')
        return age
