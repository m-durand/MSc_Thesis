import pandas as pd
import numpy as np
import time
import os
import psycopg2
import random
import hashlib

#os.chdir('C:\\Users\\Fernanda Alcala\\Documents\\Tesis_Maestria\\code\\model\\')
os.chdir('/Users/fernandaalcala/Documents/Tesis_Maestria/code/model/')

## Setup hyperparameters for policy iteration ##########################
np.random.seed(20170130)

total_epochs = 1000 # 10000 epochs is a good number to play, need to find a better way to constraint
# 10,000 epochs takes about 6 minutes to train
# 100,000 eopchs takes about 40 minutes to train
warmstart_proportion = 0.05  # How much time will the agents spend observing what the downstream agent does, not exploring
max_demand = 100  # The maximum quantity an agent can ask for during one day
epsilon_greedy_converges_to = 0.005


## Necessary world information #########################################

# Getting customer_demand and field_supply trends
customer_demand = pd.read_csv("./../../aux_documents/customer_trend.csv")
fields_supply = pd.read_csv("../../aux_documents/fields_trend.csv")

# Prices and Costs
# Prices of one beer at each level of the supply chain.
retail_price = 100
wholesale_price = 90
regional_warehouse_price = 80
factory_price = 70
field_price = 60
# Cost of holding one beer during one day on warehouse.
# Assumed to be the same for all levels
warehouse_price = 1000 #1/365 = 0.002739 it is still profitable to keep beer
# on the warehouse for almost a year just so they don't get backlog
# Cost of backlog: non fulfilled orders
backlog_cost = 50

# Initial Inventories
retail_ininv = 1
wholesale_ininv = 1
regional_warehouse_ininv = 1
factory_ininv = 1

# Create world #
# Create the agents that will comprise our supply chain,
# and then assign the relationships (upstream, downstream) between them.
exec(open("players.py").read())
exec(open("world.py").read())

# Policy Iteration #
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
exec(open("policy_iteration.py").read())

# Prepare results and insert into Postgresql database #
connection_params = """dbname='reinforcement_learning' user='experiments'
                    host='localhost' password='learning'"""

exec(open("insert_experiment_into_database.py").read())