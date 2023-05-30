from trackings.models import Tracking
import json

class Tables:
    EXERCISES_INFO = 1
    TRAININGS = 2
    PROGRAMS = 3
    EXERCISES = 4
    PROGRAMS_TRANSLATIONS = 5

# Never change the order of this list
# l_tables = ['Exercises Info', 'Trainings', 'Programs', 'Exercises', 'Programs Translations' ]
# l_codes = [ Tables.EXERCISES_INFO, Tables.TRAININGS, Tables.PROGRAMS, Tables.EXERCISES, Tables.PROGRAMS_TRANSLATIONS ]
# T_CODES = ((code,table_name) for code, table_name in zip(l_codes, l_tables) )