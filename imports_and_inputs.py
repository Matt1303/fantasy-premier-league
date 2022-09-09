import pandas as pd
import numpy as np
import datetime
from datetime import date
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import cross_val_score, KFold
from sklearn.linear_model import Ridge, Lasso
from pulp import *

# Perform the necessary imports
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

import warnings
warnings.filterwarnings("ignore")

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('mode.chained_assignment', None)
pd.set_option('display.float_format', lambda x: '%.2f' % x)

folder_location = r'C:\Users\msmith'

my_players = ['Robert Sánchez',
            'Diogo Dalot Teixeira',
            'Trent Alexander-Arnold',
            'Kieran Trippier',
            'Reece James',
            'Mohamed Salah',
            'Luis Díaz',
            'Ilkay Gündogan',
            'Gabriel Martinelli Silva',
            'Erling Haaland',
            'Gabriel Fernando de Jesus']

my_bench_players = ['Danny Ward',
                    'Neco Williams',
                    'Andreas Hoelgebaum Pereira',
                    'Sam Greenwood']

# players to exclude from considering transfer out
no_transfer = [] #['Erling Haaland', 'Mohamed Salah', 'Robert Sánchez'] #['Erling Haaland']

default_min_gw = 7
default_max_gw = 11

default_starting_budget = 82
default_bench_budget = 18

default_num_transfers = 2

default_minimum_chance_of_playing = 50

default_form_window = 5