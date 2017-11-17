agents = [retail_agent, wholesale_agent, regional_warehouse_agent, factory_agent]

# TODO create a function that doesn't learn, only
# asks on t for what the downstream agent asked for on t-1
# this would be the equivalent of ordering upstream what the client ordered the previous day
def order_by_the_day(agent,day):
    return agent.downstream_agent.current_policy[day-1]

def create_demand(day):
    x = np.random.uniform(0, 1)
    if x < p_exploration:  # exploRation
        return np.random.randint(0,max_demand)  # 70 is the maximum harvest of all year, occurs August 15th
    else:  # exploTation
        return agent.best_policy[day-1]

# POLICY ITERATION  ----------------------------------------------------------------

start_time = time.time()

for j in range(total_epochs):
    #if j % (total_epochs/20) == 0:
        #print(" ")  # These last two lines are used for printing - just make sure every time point appears clearly separated
    # starts in 1 ends in the first number so it always explores a bit
    p_exploration = max(epsilon_greedy_converges_to ,(total_epochs - j) / total_epochs)
    day = 0
    # Reinitialize inventories and money, etc at the beginning of the year
    # The only things that should stay are best policies and payout, this is what the agent learns over time
    for agent in agents:
        agent.inventory = agent.initial_inventory
        agent.total_warehousing_costs = 0
        agent.total_money = 0
        agent.backlog = 0

    while day < 365:  # one year
        #print('')
        #print('Day %s' % (day))
        day+=1
        # PART 1
        # Transactions for previous day happen. These are fixed.
        # Orders are fulfilled first time in the morning
        # Everyone gets their shippings at the same time
        # Factory
        fulfilled_to_factory = min(factory_agent.current_policy[day-1],
                                   max(fields_agent.current_policy[day-1] - factory_agent.current_policy[day-1],0))
        factory_agent.receive_upstream(fulfilled_to_factory)
        #print('Factory now has %s inventory and %s money' % (factory_agent.inventory, factory_agent.total_money))
        # Regional Warehouse
        fulfilled_to_regional_warehouse = factory_agent.give_downstream(regional_warehouse_agent.current_policy[day-1])
        regional_warehouse_agent.receive_upstream(fulfilled_to_regional_warehouse)
        factory_agent.policy_inventory[day-1] = factory_agent.inventory
        #print('Regional WH now has %s inventory and %s money' % (regional_warehouse_agent.inventory, regional_warehouse_agent.total_money))
        # Wholesale
        fulfilled_to_wholesale = regional_warehouse_agent.give_downstream(wholesale_agent.current_policy[day-1])
        wholesale_agent.receive_upstream(fulfilled_to_wholesale)
        regional_warehouse_agent.policy_inventory[day-1] = regional_warehouse_agent.inventory
        #print('Wholesale now has %s inventory and %s money' % (wholesale_agent.inventory, wholesale_agent.total_money))
        # Retail
        fulfilled_to_retail = wholesale_agent.give_downstream(retail_agent.current_policy[day-1])
        retail_agent.receive_upstream(fulfilled_to_retail)
        wholesale_agent.policy_inventory[day-1] = wholesale_agent.inventory
        #print('Retail now has %s inventory and %s money' % (retail_agent.inventory, retail_agent.total_money))
        # Customer
        fulfilled_to_customer = retail_agent.give_downstream(customer_agent.current_policy[day-1])
        retail_agent.policy_inventory[day-1] = retail_agent.inventory

        for agent in agents:
            # PART 2
            # How much money did the agent end up with yesterday's decisions?
            agent.current_payout[day-1] = agent.total_money
            # Agent decides demand for today, which will (might) be fulfilled tomorrow
            # First iteration: see what happens if agent doesn't make any decisions, demanding zero
            if j == 0:
                agent_demand = 0
            # 1% of total iterations: try to figure out downstream agent's average demand, to have a warm start
            elif j < warmstart_proportion * total_epochs:
                agent.average_downstream_demand = np.mean([agent.average_downstream_demand,
                                                           agent.downstream_agent.current_policy[day-1]])
                agent_demand = np.floor(agent.average_downstream_demand)  # floor because should only ask for integers
            else:
                agent_demand = create_demand(day)
                #agent_demand = 0  #If we want to evaluate any static policy
            agent.current_policy[day-1] = agent_demand
            # Paying for warehousing at the end of the day
            agent.pay_for_warehousing()
            if agent.current_payout[day-1] > agent.best_payout[day-1]:  # payout the day before
                #print("I have found a better policy! Year %s " % (j))
                agent.best_policy[day-1] = agent.current_policy[:][day-1]  # [:] because they're mutable
                agent.best_payout[day-1] = agent.current_payout[:][day-1]
                #print("UPDATED! Year %s Agent %s current payout %s updated best payout %s" % (j, agent.name, agent.current_payout[-1], agent.best_payout[-1]))

    for agent in agents:  # At the end of the year, save the final payout they got
        #if j % (total_epochs/20) == 0:   # I will only print 20 views, doesn't matter how many epochs
            #print("Year %s Agent %s current payout %s current best payout %s" % (j, agent.name, agent.current_payout[-1], agent.best_payout[-1]))
        agent.historic_payout.append(agent.current_payout[-1])

elapsed_time = time.time() - start_time
#print("Total elapsed time for %s epochs : %s" % (total_epochs, elapsed_time))