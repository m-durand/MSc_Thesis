# This function takes as argument 4 policies of length 365 (the whole year)
# and returns one array of length 4 with the money on day 365 for each agent / returns 4 numbers assigned to 4 money variables, one for each agent / dictionary
def evaluate_world_policies(retail_policy, wholesale_policy, regional_warehouse_policy, factory_policy,
                            fields_supply_supply,
                            customer_demand_demand):   
    for agent in agents:
        agent.inventory = agent.initial_inventory
        agent.total_warehousing_costs = 0
        agent.total_money = 0
        agent.backlog = 0
        
    for day in range(365):
        day = day + 1
        # Factory
        fulfilled_to_factory = min(factory_policy[day-1],
                                   max(fields_supply_supply[day-1] - factory_policy[day-1],0))
        factory_agent.receive_upstream(fulfilled_to_factory)
        factory_agent.pay_for_warehousing()
        #print('Factory now has %s inventory and %s money' % (factory_agent.inventory, factory_agent.total_money))
        # Regional Warehouse
        fulfilled_to_regional_warehouse = factory_agent.give_downstream(regional_warehouse_policy[day-1])
        regional_warehouse_agent.receive_upstream(fulfilled_to_regional_warehouse)
        regional_warehouse_agent.pay_for_warehousing()
        #factory_agent.policy_inventory[day-1] = factory_agent.inventory
        #print('Regional WH now has %s inventory and %s money' % (regional_warehouse_agent.inventory, regional_warehouse_agent.total_money))
        # Wholesale
        fulfilled_to_wholesale = regional_warehouse_agent.give_downstream(wholesale_policy[day-1])
        wholesale_agent.receive_upstream(fulfilled_to_wholesale)
        wholesale_agent.pay_for_warehousing()
        #regional_warehouse_agent.policy_inventory[day-1] = regional_warehouse_agent.inventory
        #print('Wholesale now has %s inventory and %s money' % (wholesale_agent.inventory, wholesale_agent.total_money))
        # Retail
        fulfilled_to_retail = wholesale_agent.give_downstream(retail_policy[day-1])
        retail_agent.receive_upstream(fulfilled_to_retail)
        retail_agent.pay_for_warehousing()
        #wholesale_agent.policy_inventory[day-1] = wholesale_agent.inventory
        #print('Retail now has %s inventory and %s money' % (retail_agent.inventory, retail_agent.total_money))
        # Customer
        fulfilled_to_customer = retail_agent.give_downstream(customer_demand_demand[day-1])
        #retail_agent.policy_inventory[day-1] = retail_agent.inventory
        
    return factory_agent.total_money, regional_warehouse_agent.total_money, wholesale_agent.total_money, factory_agent.total_money


##############################################################################
################### EVALUATION: NO FIELDS RESTRICTION ########################
##############################################################################
# Compare two scenarios:
# 1. Everyone acts according to the optimal policy, and field restriction is in place
# 2. Everyone acts according to the optimal policy, no field restriction
total_epochs = 10000 

customer_demand_daily = pd.read_csv("./../../aux_documents/customer_trend.csv")
fields_supply_daily = pd.read_csv("../../aux_documents/fields_trend.csv")
fields_supply_infinite = pd.read_csv("../../aux_documents/fields_trend_infinite.csv")

eval_policies_df = pd.DataFrame(columns=['iteration', 'scenario', 'agent', 'money']) 

# Run the restricted realization #############################################

# Getting customer_demand and field_supply trends
customer_demand = customer_demand_daily
fields_supply = fields_supply_daily

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

exec(open("players.py").read())
exec(open("world.py").read())
np.random.seed(20170130)
exec(open("policy_iteration.py").read())

# Optimal: algorithm results
restricted_retail_policy = retail_agent.best_policy
restricted_wholesale_policy = wholesale_agent.best_policy
restricted_regional_warehouse_policy = regional_warehouse_agent.best_policy
restricted_factory_policy = factory_agent.best_policy

restricted_retail_final_money, restricted_wholesale_final_money, restricted_regional_warehouse_final_money, restricted_factory_final_money = evaluate_world_policies(restricted_retail_policy,
                                        restricted_wholesale_policy,
                                        restricted_regional_warehouse_policy,
                                        restricted_factory_policy,
                                        fields_supply['Supply'],
                                        customer_demand['Demand'])

# zeroes policy

zeroes_policy = np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])

zeroes_retail_final_money, zeroes_wholesale_final_money, zeroes_regional_warehouse_final_money, zeroes_factory_final_money = evaluate_world_policies(zeroes_policy,
                                        zeroes_policy,
                                        zeroes_policy,
                                        zeroes_policy,
                                        fields_supply['Supply'],
                                        customer_demand['Demand'])

# common sense policy
commonsense_retail_policy = np.array([2,1.15,1.11,1.26,1.4,1.326,1.334,1.312,1.29,1.216,1.142,1.2,1.326,1.334,1.312,1.29,1.216,1.142,1.2,1.326,1.334,1.312,1.29,1.216,1.142,1.2,1.326,1.334,1.312,1.29,1.216,1.142,1.2,1.326,1.334,1.312,1.29,1.216,1.142,1.2,1.326,1.334,1.312,1.29,1.216,1.142,1.2,1.326,1.334,1.312,1.29,1.216,1.142,1.2,1.326,1.334,1.312,1.29,1.216,1.142,1.2,1.326,1.334,1.312,1.29,1.216,1.142,1.2,1.326,1.334,1.312,1.29,1.216,1.142,1.2,1.326,1.334,1.312,1.29,1.216,1.142,1.2,1.326,1.334,1.312,1.29,1.216,1.142,1.2,1.326,1.334,1.312,1.29,1.216,1.142,1.2,1.326,1.334,1.312,1.29,1.216,1.142,1.2,1.326,1.334,1.312,1.29,1.216,1.142,1.2,1.326,1.334,1.312,1.29,1.216,1.142,1.2,1.326,1.334,1.312,1.26,1.194,1.09,1.104,1.2,1.326,1.334,1.312,1.29,1.216,1.142,1.2,1.326,1.334,1.312,1.29,1.216,1.142,1.2,1.326,1.334,1.312,1.29,1.216,1.142,1.2,1.326,1.334,1.312,1.29,1.216,1.142,1.2,1.326,1.334,1.312,1.29,1.216,1.142,1.2,1.326,1.334,1.312,1.29,1.216,1.142,1.2,1.326,1.334,1.312,1.29,1.216,1.142,1.2,1.326,1.334,1.312,1.29,1.216,1.142,1.2,1.326,1.334,1.312,1.29,1.216,1.142,1.2,1.326,1.334,1.312,1.29,1.216,1.142,1.2,1.326,1.334,1.312,1.29,1.216,1.142,1.2,1.326,1.334,1.312,1.29,1.216,1.142,1.2,1.326,1.334,1.312,1.26,1.194,1.09,1.104,1.2,1.326,1.334,1.312,1.29,1.216,1.142,1.2,1.326,1.334,1.312,1.29,1.216,1.142,1.2,1.326,1.334,1.312,1.29,1.216,1.142,1.2,1.326,1.334,1.312,1.29,1.216,1.142,1.2,1.326,1.334,1.312,1.29,1.216,1.142,1.2,1.326,1.334,1.312,1.29,1.216,1.646,2.296,2.422,2.43,2.408,1.882,1.216,1.142,1.2,1.326,1.334,1.312,1.29,1.216,1.142,1.2,1.326,1.334,1.312,1.29,1.216,1.142,1.2,1.326,1.334,1.312,1.29,1.216,1.142,1.2,1.326,1.334,1.312,1.29,1.216,1.142,1.2,1.326,1.334,1.312,1.29,1.216,1.142,1.2,1.326,1.334,1.312,1.26,1.194,1.09,1.104,1.2,1.326,1.334,1.312,1.29,1.216,1.142,1.2,1.326,1.334,1.312,1.29,1.216,1.142,1.2,1.326,1.334,1.312,1.29,1.216,1.142,1.2,1.326,1.334,1.312,1.29,1.216,1.142,1.2,1.326,1.334,1.312,1.29,1.216,1.142,1.2,1.326,1.334,1.312,1.29,1.216,1.142,1.2,1.652,1.898,2.076,2.284,2.432,2.284,2.4,2.652,2.668,2.624,2.58,2.432,2.284,2.4])
commonsense_wholesale_policy = np.array([2,1.15,1.11,1.26,1.384,1.2492,1.286,1.3264,1.3324,1.2956,1.2588,1.232,1.2348,1.2436,1.2628,1.2924,1.2956,1.2588,1.232,1.2348,1.2436,1.2628,1.2924,1.2956,1.2588,1.232,1.2348,1.2436,1.2628,1.2924,1.2956,1.2588,1.232,1.2348,1.2436,1.2628,1.2924,1.2956,1.2588,1.232,1.2348,1.2436,1.2628,1.2924,1.2956,1.2588,1.232,1.2348,1.2436,1.2628,1.2924,1.2956,1.2588,1.232,1.2348,1.2436,1.2628,1.2924,1.2956,1.2588,1.232,1.2348,1.2436,1.2628,1.2924,1.2956,1.2588,1.232,1.2348,1.2436,1.2628,1.2924,1.2956,1.2588,1.232,1.2348,1.2436,1.2628,1.2924,1.2956,1.2588,1.232,1.2348,1.2436,1.2628,1.2924,1.2956,1.2588,1.232,1.2348,1.2436,1.2628,1.2924,1.2956,1.2588,1.232,1.2348,1.2436,1.2628,1.2924,1.2956,1.2588,1.232,1.2348,1.2436,1.2628,1.2924,1.2956,1.2588,1.232,1.2348,1.2436,1.2628,1.2924,1.2956,1.2588,1.232,1.2348,1.2436,1.2628,1.2864,1.2852,1.238,1.192,1.1696,1.1828,1.2108,1.2552,1.2924,1.2956,1.2588,1.232,1.2348,1.2436,1.2628,1.2924,1.2956,1.2588,1.232,1.2348,1.2436,1.2628,1.2924,1.2956,1.2588,1.232,1.2348,1.2436,1.2628,1.2924,1.2956,1.2588,1.232,1.2348,1.2436,1.2628,1.2924,1.2956,1.2588,1.232,1.2348,1.2436,1.2628,1.2924,1.2956,1.2588,1.232,1.2348,1.2436,1.2628,1.2924,1.2956,1.2588,1.232,1.2348,1.2436,1.2628,1.2924,1.2956,1.2588,1.232,1.2348,1.2436,1.2628,1.2924,1.2956,1.2588,1.232,1.2348,1.2436,1.2628,1.2924,1.2956,1.2588,1.232,1.2348,1.2436,1.2628,1.2924,1.2956,1.2588,1.232,1.2348,1.2436,1.2628,1.2924,1.2956,1.2588,1.232,1.2348,1.2436,1.2628,1.2864,1.2852,1.238,1.192,1.1696,1.1828,1.2108,1.2552,1.2924,1.2956,1.2588,1.232,1.2348,1.2436,1.2628,1.2924,1.2956,1.2588,1.232,1.2348,1.2436,1.2628,1.2924,1.2956,1.2588,1.232,1.2348,1.2436,1.2628,1.2924,1.2956,1.2588,1.232,1.2348,1.2436,1.2628,1.2924,1.2956,1.2588,1.232,1.2348,1.2436,1.2628,1.2924,1.2956,1.3596,1.552,1.774,2.002,2.2404,2.2876,2.0716,1.8156,1.5696,1.3532,1.2436,1.2628,1.2924,1.2956,1.2588,1.232,1.2348,1.2436,1.2628,1.2924,1.2956,1.2588,1.232,1.2348,1.2436,1.2628,1.2924,1.2956,1.2588,1.232,1.2348,1.2436,1.2628,1.2924,1.2956,1.2588,1.232,1.2348,1.2436,1.2628,1.2924,1.2956,1.2588,1.232,1.2348,1.2436,1.2628,1.2864,1.2852,1.238,1.192,1.1696,1.1828,1.2108,1.2552,1.2924,1.2956,1.2588,1.232,1.2348,1.2436,1.2628,1.2924,1.2956,1.2588,1.232,1.2348,1.2436,1.2628,1.2924,1.2956,1.2588,1.232,1.2348,1.2436,1.2628,1.2924,1.2956,1.2588,1.232,1.2348,1.2436,1.2628,1.2924,1.2956,1.2588,1.232,1.2348,1.2436,1.2628,1.2924,1.2956,1.2588,1.232,1.3,1.4216,1.5936,1.822,2.0684,2.1948,2.2952,2.4104,2.4872,2.5256,2.5848,2.5912,2.5176,2.464])
commonsense_regional_warehouse_policy = np.array([2,1.15,1.11,1.26,1.3808,1.23064,1.25784,1.30112,1.3156,1.29792,1.29984,1.28904,1.27072,1.25296,1.2464,1.25312,1.26584,1.27064,1.26832,1.26272,1.25296,1.2464,1.25312,1.26584,1.27064,1.26832,1.26272,1.25296,1.2464,1.25312,1.26584,1.27064,1.26832,1.26272,1.25296,1.2464,1.25312,1.26584,1.27064,1.26832,1.26272,1.25296,1.2464,1.25312,1.26584,1.27064,1.26832,1.26272,1.25296,1.2464,1.25312,1.26584,1.27064,1.26832,1.26272,1.25296,1.2464,1.25312,1.26584,1.27064,1.26832,1.26272,1.25296,1.2464,1.25312,1.26584,1.27064,1.26832,1.26272,1.25296,1.2464,1.25312,1.26584,1.27064,1.26832,1.26272,1.25296,1.2464,1.25312,1.26584,1.27064,1.26832,1.26272,1.25296,1.2464,1.25312,1.26584,1.27064,1.26832,1.26272,1.25296,1.2464,1.25312,1.26584,1.27064,1.26832,1.26272,1.25296,1.2464,1.25312,1.26584,1.27064,1.26832,1.26272,1.25296,1.2464,1.25312,1.26584,1.27064,1.26832,1.26272,1.25296,1.2464,1.25312,1.26584,1.27064,1.26832,1.26272,1.25296,1.2464,1.25192,1.26256,1.2632,1.25288,1.23424,1.21352,1.19864,1.20208,1.22216,1.24736,1.26256,1.2668,1.26272,1.25296,1.2464,1.25312,1.26584,1.27064,1.26832,1.26272,1.25296,1.2464,1.25312,1.26584,1.27064,1.26832,1.26272,1.25296,1.2464,1.25312,1.26584,1.27064,1.26832,1.26272,1.25296,1.2464,1.25312,1.26584,1.27064,1.26832,1.26272,1.25296,1.2464,1.25312,1.26584,1.27064,1.26832,1.26272,1.25296,1.2464,1.25312,1.26584,1.27064,1.26832,1.26272,1.25296,1.2464,1.25312,1.26584,1.27064,1.26832,1.26272,1.25296,1.2464,1.25312,1.26584,1.27064,1.26832,1.26272,1.25296,1.2464,1.25312,1.26584,1.27064,1.26832,1.26272,1.25296,1.2464,1.25312,1.26584,1.27064,1.26832,1.26272,1.25296,1.2464,1.25312,1.26584,1.27064,1.26832,1.26272,1.25296,1.2464,1.25192,1.26256,1.2632,1.25288,1.23424,1.21352,1.19864,1.20208,1.22216,1.24736,1.26256,1.2668,1.26272,1.25296,1.2464,1.25312,1.26584,1.27064,1.26832,1.26272,1.25296,1.2464,1.25312,1.26584,1.27064,1.26832,1.26272,1.25296,1.2464,1.25312,1.26584,1.27064,1.26832,1.26272,1.25296,1.2464,1.25312,1.26584,1.27064,1.26832,1.26272,1.25296,1.2464,1.25312,1.26584,1.2908,1.35248,1.45472,1.59664,1.7856,1.9712,2.07512,2.08344,1.99696,1.81952,1.61072,1.44896,1.34432,1.28952,1.27064,1.26832,1.26272,1.25296,1.2464,1.25312,1.26584,1.27064,1.26832,1.26272,1.25296,1.2464,1.25312,1.26584,1.27064,1.26832,1.26272,1.25296,1.2464,1.25312,1.26584,1.27064,1.26832,1.26272,1.25296,1.2464,1.25312,1.26584,1.27064,1.26832,1.26272,1.25296,1.2464,1.25192,1.26256,1.2632,1.25288,1.23424,1.21352,1.19864,1.20208,1.22216,1.24736,1.26256,1.2668,1.26272,1.25296,1.2464,1.25312,1.26584,1.27064,1.26832,1.26272,1.25296,1.2464,1.25312,1.26584,1.27064,1.26832,1.26272,1.25296,1.2464,1.25312,1.26584,1.27064,1.26832,1.26272,1.25296,1.2464,1.25312,1.26584,1.27064,1.26832,1.26272,1.25296,1.2464,1.25312,1.26584,1.27064,1.26832,1.27576,1.3016,1.3612,1.47384,1.64112,1.82008,1.9948,2.15816,2.2912,2.38264,2.46064,2.51984,2.54128,2.53664])
commonsense_factory_policy = np.array([2,1.15,1.11,1.26,1.38016,1.226288,1.247856,1.28608,1.2972,1.280624,1.294464,1.300704,1.294624,1.282096,1.271792,1.262448,1.257808,1.257792,1.260864,1.264128,1.264096,1.260208,1.256704,1.256208,1.257792,1.260864,1.264128,1.264096,1.260208,1.256704,1.256208,1.257792,1.260864,1.264128,1.264096,1.260208,1.256704,1.256208,1.257792,1.260864,1.264128,1.264096,1.260208,1.256704,1.256208,1.257792,1.260864,1.264128,1.264096,1.260208,1.256704,1.256208,1.257792,1.260864,1.264128,1.264096,1.260208,1.256704,1.256208,1.257792,1.260864,1.264128,1.264096,1.260208,1.256704,1.256208,1.257792,1.260864,1.264128,1.264096,1.260208,1.256704,1.256208,1.257792,1.260864,1.264128,1.264096,1.260208,1.256704,1.256208,1.257792,1.260864,1.264128,1.264096,1.260208,1.256704,1.256208,1.257792,1.260864,1.264128,1.264096,1.260208,1.256704,1.256208,1.257792,1.260864,1.264128,1.264096,1.260208,1.256704,1.256208,1.257792,1.260864,1.264128,1.264096,1.260208,1.256704,1.256208,1.257792,1.260864,1.264128,1.264096,1.260208,1.256704,1.256208,1.257792,1.260864,1.264128,1.264096,1.260208,1.256464,1.255312,1.255408,1.255392,1.25296,1.24528,1.232496,1.220272,1.214128,1.216752,1.22656,1.240192,1.25232,1.25848,1.258288,1.2564,1.256208,1.257792,1.260864,1.264128,1.264096,1.260208,1.256704,1.256208,1.257792,1.260864,1.264128,1.264096,1.260208,1.256704,1.256208,1.257792,1.260864,1.264128,1.264096,1.260208,1.256704,1.256208,1.257792,1.260864,1.264128,1.264096,1.260208,1.256704,1.256208,1.257792,1.260864,1.264128,1.264096,1.260208,1.256704,1.256208,1.257792,1.260864,1.264128,1.264096,1.260208,1.256704,1.256208,1.257792,1.260864,1.264128,1.264096,1.260208,1.256704,1.256208,1.257792,1.260864,1.264128,1.264096,1.260208,1.256704,1.256208,1.257792,1.260864,1.264128,1.264096,1.260208,1.256704,1.256208,1.257792,1.260864,1.264128,1.264096,1.260208,1.256704,1.256208,1.257792,1.260864,1.264128,1.264096,1.260208,1.256464,1.255312,1.255408,1.255392,1.25296,1.24528,1.232496,1.220272,1.214128,1.216752,1.22656,1.240192,1.25232,1.25848,1.258288,1.2564,1.256208,1.257792,1.260864,1.264128,1.264096,1.260208,1.256704,1.256208,1.257792,1.260864,1.264128,1.264096,1.260208,1.256704,1.256208,1.257792,1.260864,1.264128,1.264096,1.260208,1.256704,1.256208,1.257792,1.260864,1.264128,1.264096,1.260208,1.256704,1.256208,1.261824,1.281728,1.323392,1.392096,1.496048,1.632128,1.776656,1.9024,1.982464,1.989248,1.917152,1.79192,1.644096,1.502608,1.392832,1.324352,1.287104,1.268832,1.260208,1.256704,1.256208,1.257792,1.260864,1.264128,1.264096,1.260208,1.256704,1.256208,1.257792,1.260864,1.264128,1.264096,1.260208,1.256704,1.256208,1.257792,1.260864,1.264128,1.264096,1.260208,1.256704,1.256208,1.257792,1.260864,1.264128,1.264096,1.260208,1.256464,1.255312,1.255408,1.255392,1.25296,1.24528,1.232496,1.220272,1.214128,1.216752,1.22656,1.240192,1.25232,1.25848,1.258288,1.2564,1.256208,1.257792,1.260864,1.264128,1.264096,1.260208,1.256704,1.256208,1.257792,1.260864,1.264128,1.264096,1.260208,1.256704,1.256208,1.257792,1.260864,1.264128,1.264096,1.260208,1.256704,1.256208,1.257792,1.260864,1.264128,1.264096,1.260208,1.256704,1.256208,1.257792,1.260864,1.266736,1.276432,1.295504,1.336144,1.410704,1.519568,1.658208,1.8176,1.981072,2.129376,2.257488,2.362496,2.43912,2.488208])


commonsense_retail_final_money, commonsense_wholesale_final_money, commonsense_regional_warehouse_final_money, commonsense_factory_final_money = evaluate_world_policies(commonsense_retail_policy,
                                        commonsense_wholesale_policy,
                                        commonsense_regional_warehouse_policy,
                                        commonsense_factory_policy,
                                        fields_supply['Supply'],
                                        customer_demand['Demand'])

# Plot containing customer demand, and for one agent their smart, common sense and zeroes policies
smart_helper = np.array([15,  3,  0, 12,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
        0,  0,  0,  0,  0, 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
        0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
        0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
        0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
        0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
        0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
        0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
        0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
       0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
        0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
        0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,
        0,  0,  0,  0,  0,  0,  0, 10,  6,  0,  0,  0, 25,  5,  0,  0, 32,
       10,  2,  3, 16, 23, 33,  0, 26,  0,  1, 19, 23, 11, 29, 10, 23,  3,
       17,  0, 12,  5, 13,  2, 16,  0,  0,  0,  2,  0, 11, 35,  0,  0,  0,
        2,  0,  0, 31, 29,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
        0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
        0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
        0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
        0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
        0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 0,  0,  0,  0,  0,
        0,  0,  0,  0,  0,  0,  0,  0])
axis_helper = np.array([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,142,143,144,145,146,147,148,149,150,151,152,153,154,155,156,157,158,159,160,161,162,163,164,165,166,167,168,169,170,171,172,173,174,175,176,177,178,179,180,181,182,183,184,185,186,187,188,189,190,191,192,193,194,195,196,197,198,199,200,201,202,203,204,205,206,207,208,209,210,211,212,213,214,215,216,217,218,219,220,221,222,223,224,225,226,227,228,229,230,231,232,233,234,235,236,237,238,239,240,241,242,243,244,245,246,247,248,249,250,251,252,253,254,255,256,257,258,259,260,261,262,263,264,265,266,267,268,269,270,271,272,273,274,275,276,277,278,279,280,281,282,283,284,285,286,287,288,289,290,291,292,293,294,295,296,297,298,299,300,301,302,303,304,305,306,307,308,309,310,311,312,313,314,315,316,317,318,319,320,321,322,323,324,325,326,327,328,329,330,331,332,333,334,335,336,337,338,339,340,341,342,343,344,345,346,347,348,349,350,351,352,353,354,355,356,357,358,359,360,361,362,363,364,365])

fig = plt.figure()
ax1 = fig.add_subplot(111)

ax1.plot(axis_helper, fields_supply['Supply'], c='lightgreen', label='Oferta de campos')
ax1.plot(axis_helper, smart_helper, c='blue', label='Inteligencia')
ax1.plot(axis_helper, commonsense_factory_policy, c='grey', label='Sentido Común')
ax1.plot(axis_helper, zeroes_policy, c='orange',label='Inacción')
ax1.plot(axis_helper, customer_demand['Demand'], c='pink', label='Demanda de consumidor')
#plt.legend(loc='upper left');
plt.show()


# Run the nonrestricted realization ##########################################

# Getting customer_demand and field_supply trends
customer_demand = customer_demand_daily
fields_supply = fields_supply_infinite

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

exec(open("players.py").read())
exec(open("world.py").read())
np.random.seed(20170130)
exec(open("policy_iteration.py").read())

# Optimal: algorithm results
nonrestricted_retail_policy = retail_agent.best_policy
nonrestricted_wholesale_policy = wholesale_agent.best_policy
nonrestricted_regional_warehouse_policy = regional_warehouse_agent.best_policy
nonrestricted_factory_policy = factory_agent.best_policy

nonrestricted_retail_final_money, nonrestricted_wholesale_final_money, nonrestricted_regional_warehouse_final_money, nonrestricted_factory_final_money = evaluate_world_policies(nonrestricted_retail_policy,
                                        nonrestricted_wholesale_policy,
                                        nonrestricted_regional_warehouse_policy,
                                        nonrestricted_factory_policy,
                                        fields_supply['Supply'],
                                        customer_demand['Demand'])

##############################################################################
################### EVALUATION: SOME AGENTS ACT DIFFERENTLY ##################
##############################################################################
# Compare three sets of policies:
# 1. Everyone acts according to the optimal policy found by policy iteration (RL algorithm)
# 2. Only one agent acts "optimally", the others act with a "last n-periods rolling average" policy (dumb)
# 3. Only one agent acts "optimally", the others act with a constant policy (dumber)

customer_demand_daily = pd.read_csv("./../../aux_documents/customer_trend.csv")['Demand']*5
fields_supply_daily = pd.read_csv("../../aux_documents/fields_trend.csv")['Supply']

eval_policies_df = pd.DataFrame(columns=['iteration','smart_agent', 'strategy', 'agent', 'money']) 

for agent_i in ["Retail", "Wholesale", "Regional Warehouse", "Factory"]:
    for i in range(250):
        
        print(i)
        print(agent_i)
        
        np.random.seed(None)
        # Prices and Costs
        # Prices of one beer at each level of the supply chain.
        field_price = np.random.uniform(0,50)
        factory_price = np.random.uniform(field_price,1.5*field_price)
        regional_warehouse_price = np.random.uniform(factory_price, 1.5*factory_price)
        wholesale_price = np.random.uniform(regional_warehouse_price,1.5*regional_warehouse_price)
        retail_price = np.random.uniform(wholesale_price,1.5*wholesale_price)
        # Cost of holding one beer during one day on warehouse.
        # Assumed to be the same for all levels
        warehouse_price = 10/365 #1/365 = 0.002739 it is still profitable to keep beer
        # on the warehouse for almost a year just so they don't get backlog
        # Cost of backlog: non fulfilled orders
        backlog_cost = np.random.uniform(0,5)
        
        # Initial Inventories
        retail_ininv = np.random.uniform(0,50)
        wholesale_ininv = np.random.uniform(0,50)
        regional_warehouse_ininv = np.random.uniform(0,50)
        factory_ininv = np.random.uniform(0,50)
        
        # Run small realizations 
        exec(open("players.py").read())
        exec(open("world.py").read())
        np.random.seed(20170130)
        exec(open("policy_iteration.py").read())
        
         ###### Declare the optimal, dumb and dumber policies
        
        # Optimal: algorithm results
        optimal_retail_policy = retail_agent.best_policy
        optimal_wholesale_policy = wholesale_agent.best_policy
        optimal_regional_warehouse_policy = regional_warehouse_agent.best_policy
        optimal_factory_policy = factory_agent.best_policy
        
        # Dumb: only one agent learnt (retail) the others have constant demand equal to average yearly demand
        average_daily_demand = np.mean(customer_demand_daily)
        if agent == "retail":
            dumb_retail_policy = retail_agent.best_policy
            dumb_wholesale_policy = np.repeat(average_daily_demand,365)
            dumb_regional_warehouse_policy = np.repeat(average_daily_demand,365)
            dumb_factory_policy = np.repeat(average_daily_demand,365)
        elif agent == "wholesale":
            dumb_retail_policy = np.repeat(average_daily_demand,365)
            dumb_wholesale_policy = wholesale_agent.best_policy
            dumb_regional_warehouse_policy = np.repeat(average_daily_demand,365)
            dumb_factory_policy = np.repeat(average_daily_demand,365)        
        elif agent == "regional warehouse":
            dumb_retail_policy = np.repeat(average_daily_demand,365)
            dumb_wholesale_policy = np.repeat(average_daily_demand,365)
            dumb_regional_warehouse_policy = regional_warehouse_agent.best_policy
            dumb_factory_policy = np.repeat(average_daily_demand,365)
        elif agent == "factory":
            dumb_retail_policy = np.repeat(average_daily_demand,365)
            dumb_wholesale_policy = np.repeat(average_daily_demand,365)
            dumb_regional_warehouse_policy = np.repeat(average_daily_demand,365)
            dumb_factory_policy = factory_agent.best_policy      
     
        # Dumber: all agents have constant demand equal to average yearly demand
        dumber_retail_policy = np.repeat(average_daily_demand,365)
        dumber_wholesale_policy = np.repeat(average_daily_demand,365)
        dumber_regional_warehouse_policy = np.repeat(average_daily_demand,365)
        dumber_factory_policy = np.repeat(average_daily_demand,365)
        
        
        smart_retail_final_money, smart_wholesale_final_money, smart_regional_warehouse_final_money, smart_factory_final_money = evaluate_world_policies(optimal_retail_policy,
                                                optimal_wholesale_policy,
                                                optimal_regional_warehouse_policy,
                                                optimal_factory_policy,
                                            fields_supply['Supply'],
                                            customer_demand['Demand'])
        dumb_retail_final_money, dumb_wholesale_final_money, dumb_regional_warehouse_final_money, dumb_factory_final_money = evaluate_world_policies(dumb_retail_policy,
                                               dumb_wholesale_policy,
                                               dumb_regional_warehouse_policy,
                                               dumb_factory_policy,
                                            fields_supply['Supply'],
                                            customer_demand['Demand'])
        dumber_retail_final_money, dumber_wholesale_final_money, dumber_regional_warehouse_final_money, dumber_factory_final_money = evaluate_world_policies(dumber_retail_policy,
                                               dumber_wholesale_policy,
                                               dumber_regional_warehouse_policy,
                                               dumber_factory_policy,
                                            fields_supply['Supply'],
                                            customer_demand['Demand'])
        
        # Add new rows to the original df
        new_row = [i,agent_i,'Smart','Retail',smart_retail_final_money]
        eval_policies_df.loc[eval_policies_df.shape[0] + 1] = new_row
        new_row = [i,agent_i,'Smart','Wholesale',smart_wholesale_final_money]
        eval_policies_df.loc[eval_policies_df.shape[0] + 1] = new_row
        new_row = [i,agent_i,'Smart','Regional Warehouse',smart_regional_warehouse_final_money]
        eval_policies_df.loc[eval_policies_df.shape[0] + 1] = new_row
        new_row = [i,agent_i,'Smart','Factory',smart_factory_final_money]
        eval_policies_df.loc[eval_policies_df.shape[0] + 1] = new_row
        new_row = [i,agent_i,'Dumb','Retail',dumb_retail_final_money]
        eval_policies_df.loc[eval_policies_df.shape[0] + 1] = new_row
        new_row = [i,agent_i,'Dumb','Wholesale',dumb_wholesale_final_money]
        eval_policies_df.loc[eval_policies_df.shape[0] + 1] = new_row
        new_row = [i,agent_i,'Dumb','Regional Warehouse',dumb_regional_warehouse_final_money]
        eval_policies_df.loc[eval_policies_df.shape[0] + 1] = new_row
        new_row = [i,agent_i,'Dumb','Factory',dumb_factory_final_money]
        eval_policies_df.loc[eval_policies_df.shape[0] + 1] = new_row
        new_row = [i,agent_i,'Dumber','Retail',dumber_retail_final_money]
        eval_policies_df.loc[eval_policies_df.shape[0] + 1] = new_row
        new_row = [i,agent_i,'Dumber','Wholesale',dumber_wholesale_final_money]
        eval_policies_df.loc[eval_policies_df.shape[0] + 1] = new_row
        new_row = [i,agent_i,'Dumber','Regional Warehouse',dumber_regional_warehouse_final_money]
        eval_policies_df.loc[eval_policies_df.shape[0] + 1] = new_row
        new_row = [i,agent_i,'Dumber','Factory',dumber_factory_final_money]
        eval_policies_df.loc[eval_policies_df.shape[0] + 1] = new_row
        
        eval_policies_df.to_csv('./../../aux_documents/evaluate_policies1.csv')

# Now there are four scenarios to compare for each agent:
# Everyone smart, only that agent smart but everyone else dumb,
# only another agent smart but that agent dumb, everyone dumb
# not nesting just to not get confused
eval_policies_df['scenario'] = np.where(eval_policies_df['strategy']== 'Dumber', "No agent learnt", "Pending")
eval_policies_df['scenario'] = np.where((eval_policies_df['strategy']== 'Dumb') & (eval_policies_df['smart_agent'] != eval_policies_df['agent']), "Another agent learnt", eval_policies_df['scenario'])
eval_policies_df['scenario'] = np.where((eval_policies_df['strategy']== 'Dumb') & (eval_policies_df['smart_agent'] == eval_policies_df['agent']), "This agent learnt", eval_policies_df['scenario'])
eval_policies_df['scenario'] = np.where(eval_policies_df['strategy']== 'Smart', "All agents learnt", eval_policies_df['scenario'])

# Create the indices based on the "dumber" policy to interpret uplifts
eval_policies_df_ids = eval_policies_df.pivot_table(index=['iteration','agent'], columns='scenario', values = 'money', aggfunc=np.sum)
eval_policies_df_ids['Dumbest_idx'] = (eval_policies_df_ids['No agent learnt']-eval_policies_df_ids['No agent learnt'])/abs(eval_policies_df_ids['No agent learnt'])
eval_policies_df_ids['Dumber_idx'] = (eval_policies_df_ids['Another agent learnt']-eval_policies_df_ids['No agent learnt'])/abs(eval_policies_df_ids['No agent learnt'])
eval_policies_df_ids['Dumb_idx'] = (eval_policies_df_ids['This agent learnt']-eval_policies_df_ids['No agent learnt'])/abs(eval_policies_df_ids['No agent learnt'])
eval_policies_df_ids['Smart_idx'] = (eval_policies_df_ids['All agents learnt']-eval_policies_df_ids['No agent learnt'])/abs(eval_policies_df_ids['No agent learnt'])
eval_policies_df_ids = eval_policies_df_ids.stack().reset_index()
eval_policies_df_ids = eval_policies_df_ids[eval_policies_df_ids['scenario'].isin(['Dumbest_idx', 'Dumber_idx', 'Dumb_idx', 'Smart_idx'])]
eval_policies_df_ids['scenario'] = eval_policies_df_ids['scenario'].str.slice(0, -4)
eval_policies_df_ids.columns = ['iteration', 'agent', 'scenario', 'index']

eval_policies_df_complete = eval_policies_df.set_index(['iteration','scenario','agent']).join(eval_policies_df_ids.set_index(['iteration','scenario','agent'])).reset_index()

#This part creates the same dataframe but in Spanish since the final document needs the viz
eval_policies_df_sp = eval_policies_df_ids
eval_policies_df_sp.columns = ['iteracion', 'agente', 'estrategia', 'desempeño']
eval_policies_df_sp = eval_policies_df_sp.replace(['Retail','Wholesale', 'Regional Warehouse','Factory'],
                            ['Menudeo','Mayoreo', 'Almacén Regional','Fábrica'])
eval_policies_df_sp = eval_policies_df_sp.replace(['Dumbest', 'Dumber','Dumb', 'Smart'],
                            ['Nadie aprendió', 'Solo otro agente aprendió', 'Solo este agente aprendió', 'Todos aprendieron'])

# Getting distributions
eval_policies_df_sp.groupby(['agente', 'estrategia'])['desempeño'].mean().reset_index().pivot(index='agente', columns='estrategia', values='desempeño')
eval_policies_df_sp.groupby(['agente', 'estrategia'])['desempeño'].median().reset_index().pivot(index='agente', columns='estrategia', values='desempeño')


# Visualizing as a faceted plot -----
# preprocessing a bit because outliers mess up the plots
eval_policies_df_sp_no_outl = eval_policies_df_sp[eval_policies_df_sp.desempeño < 5]
eval_policies_df_sp_no_outl = eval_policies_df_sp_no_outl[eval_policies_df_sp_no_outl.desempeño > (10*(-1))]
eval_policies_df_sp_no_outl.to_csv('./../../aux_documents/evaluate_policies_index.csv')


sns.set()
sns.set_style(style='white')
grid = sns.FacetGrid(eval_policies_df_sp_no_outl, 
                     #col='estrategia', 
                     row = 'agente', 
                     hue='estrategia' ,
                     row_order= ["Menudeo","Mayoreo","Almacén Regional","Fábrica"],
                     size=3.2, 
                     aspect=2)
grid.map(sns.kdeplot, 'desempeño', shade=True)
grid.set(xlim=(-1, eval_policies_df_sp_no_outl['desempeño'].max()), ylim=(0,2))
grid.add_legend()


# Add vertical lines for mean age on each plot
def vertical_mean_line_base(x, **kwargs):
    plt.axvline(0, linestyle = '--', color = 'b')

grid.map(vertical_mean_line_base, 'desempeño') 

grid.set_ylabels('Densidad', size=12)

plt.show()


