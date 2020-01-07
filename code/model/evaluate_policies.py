# Compare three sets of policies:
# 1. Everyone acts according to the optimal policy found by policy iteration (RL algorithm)
# 2. Only one agent acts "optimally", the others act with a "last n-periods rolling average" policy (dumb)
# 3. Only one agent acts "optimally", the others act with a constant policy (dumber)

customer_demand_daily = pd.read_csv("./../../aux_documents/customer_trend.csv")['Demand']*5
fields_supply_daily = pd.read_csv("../../aux_documents/fields_trend.csv")['Supply']

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

#retail_policy = optimal_retail_policy
#wholesale_policy = optimal_wholesale_policy
#regional_warehouse_policy = optimal_regional_warehouse_policy
#factory_policy = optimal_factory_policy

# This function takes as argument 4 policies of length 365 (the whole year)
# and returns one array of length 4 with the money on day 365 for each agent / returns 4 numbers assigned to 4 money variables, one for each agent / dictionary
def evaluate_world_policies(retail_policy, wholesale_policy, regional_warehouse_policy, factory_policy):   
    for agent in agents:
        agent.inventory = agent.initial_inventory
        agent.total_warehousing_costs = 0
        agent.total_money = 0
        agent.backlog = 0
        
    for day in range(365):
        day = day + 1
        # Factory
        fulfilled_to_factory = min(factory_policy[day-1],
                                   max(fields_supply_daily[day-1] - factory_policy[day-1],0))
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
        fulfilled_to_customer = retail_agent.give_downstream(customer_demand_daily[day-1])
        #retail_agent.policy_inventory[day-1] = retail_agent.inventory
        
    return factory_agent.total_money, regional_warehouse_agent.total_money, wholesale_agent.total_money, factory_agent.total_money

###### Declare the optimal, dumb and dumber policies

# Optimal: algorithm results
optimal_retail_policy = retail_agent.best_policy
optimal_wholesale_policy = wholesale_agent.best_policy
optimal_regional_warehouse_policy = regional_warehouse_agent.best_policy
optimal_factory_policy = factory_agent.best_policy

# Dumb: only one agent learnt (retail) the others have constant demand equal to average yearly demand
average_daily_demand = np.mean(customer_demand_daily)
dumb_retail_policy = np.repeat(average_daily_demand,365)
dumb_wholesale_policy = np.repeat(average_daily_demand,365)
dumb_regional_warehouse_policy = regional_warehouse_agent.best_policy
dumb_factory_policy = np.repeat(average_daily_demand,365)

# Dumb: all agents have constant demand equal to average yearly demand
dumber_retail_policy = np.repeat(average_daily_demand,365)
dumber_wholesale_policy = np.repeat(average_daily_demand,365)
dumber_regional_warehouse_policy = np.repeat(average_daily_demand,365)
dumber_factory_policy = np.repeat(average_daily_demand,365)


smart_retail_final_money, smart_wholesale_final_money, smart_regional_warehouse_final_money, smart_factory_final_money = evaluate_world_policies(optimal_retail_policy,
                                        optimal_wholesale_policy,
                                        optimal_regional_warehouse_policy,
                                        optimal_factory_policy)
dumb_retail_final_money, dumb_wholesale_final_money, dumb_regional_warehouse_final_money, dumb_factory_final_money = evaluate_world_policies(dumb_retail_policy,
                                       dumb_wholesale_policy,
                                       dumb_regional_warehouse_policy,
                                       dumb_factory_policy)
dumber_retail_final_money, dumber_wholesale_final_money, dumber_regional_warehouse_final_money, dumber_factory_final_money = evaluate_world_policies(dumber_retail_policy,
                                       dumber_wholesale_policy,
                                       dumber_regional_warehouse_policy,
                                       dumber_factory_policy)

