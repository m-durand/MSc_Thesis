import pandas as pd
import numpy as np
import time
import os
import psycopg2
import random
import hashlib
import datetime
import dill
import matplotlib.pyplot  as plt
import seaborn as sns
import pylab
import shelve
import glob
import re
import imageio
from matplotlib.ticker import FuncFormatter

# For my Windows (work) computer
#os.chdir('C:\\Users\\Fernanda Alcala\\Documents\\GitHub\\Tesis_Maestria\\code\\model\\')
# For my Mac (personal) computer
os.chdir('/Users/fernandaalcala/Documents/Tesis_Maestria/code/model/')

## Setup hyperparameters for policy iteration ##########################
np.random.seed(20170130)

total_epochs = 2000000 # 10000 epochs is a good number to play, need to find a better way to constraint
# 10,000 epochs takes about 6 minutes to train
# 100,000 eopchs takes about 40 minutes to train
# for q learning
# around 125 iterations per hour
warmstart_proportion = 0.005  # How much time will the agents spend observing what the downstream agent does, not exploring
max_demand = 75  # The maximum quantity an agent can ask for during one day
epsilon_greedy_converges_to = 0.005
lambda_q_learning = 0.9

## Necessary world information #########################################

# Getting customer_demand and field_supply trends
customer_demand = pd.read_csv("./../../aux_documents/customer_trend.csv")
fields_supply = pd.read_csv("./../../aux_documents/fields_trend.csv")

# Prices and Costs
# Prices of one beer at each level of the supply chain.
retail_price = 100
wholesale_price = 90
regional_warehouse_price = 80
factory_price = 70
field_price = 60
# Cost of holding one beer during one day on warehouse.
# Assumed to be the same for all levels
warehouse_price = 10/365 #1/365 = 0.002739 it is still profitable to keep beer
# on the warehouse for almost a year just so they don't get backlog
# Cost of backlog: non fulfilled orders
backlog_cost = 2

# Initial Inventories
retail_ininv = 10
wholesale_ininv = 10
regional_warehouse_ininv = 10
factory_ininv = 10

# Create world #
# Create the agents that will comprise our supply chain,
# and then assign the relationships (upstream, downstream) between them.
exec(open("players.py").read())
exec(open("world.py").read())

# Choose which algorithms we want to run
run_policy_iteration = True
run_q_learning = False


# Policy Iteration ############################################################
# Basic idea of policy iteration:
#    1. Start all agents with the [0]*365 policy, this would be just selling what they have and never restocking or making any decisions. This is the starting benchmark (best policy).
#    2. For each agent, for every day of the year, repeat `total_epochs` times:
#        2.1 Create a random (epsilon-greedy based) policy (upstream demand) for the day
#        2.2 Next morning: make all transactions based on that demand
#        2.3 Evaluate the payout of that policy. If the payout is higher than the payout of the best policy, it becomes the new best policy; else, nothing changes.
# Note that it might be possible that they don't actually converge to these maximum payouts
# think about this as a game: the Nash equilibria don't have to be Pareto optima.
# Maybe an agent's maximum payout was obtained with a comibnation of policies that the other three agents will never use again.
# Also, towards the end of the learning process, they tend to stick to the best policy they found during the exploration phase,
# so if this policy combined with the best policy of another agent leads them to start losing and losing...
# I'm just saying it could happen.
if run_policy_iteration == True:
    exec(open("policy_iteration.py").read())
    
    connection_params = """dbname='reinforcement_learning' user='experiments'
                        host='localhost' password='learning'"""
    
    # TODO this is deactivated for now - need to reconfigure database on computer
    #exec(open("insert_experiment_into_pi_database.py").read())

# Q learning ##################################################################
# Basic idea of Q-learning:
# TODO [missing]

# Prepare results and insert into Postgresql database #
if run_q_learning == True:
    exec(open("q_learning.py").read())
#

#connection_params = """dbname='reinforcement_learning' user='experiments'
#                    host='localhost' password='learning'"""

#exec(open("insert_experiment_into_q_database.py").read())
