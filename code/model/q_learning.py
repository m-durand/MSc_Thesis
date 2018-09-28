agents = [retail_agent, wholesale_agent, regional_warehouse_agent, factory_agent]

def create_demand(day):
    x = np.random.uniform(0, 1)
    if x < p_exploration:  # exploRation
        return np.random.randint(0,max_demand)  # 70 is the maximum harvest of all year, occurs August 15th
    else:  # exploTation
        # we want to get the action that will take us closer to the optimal
        # historical inventory - this can be purchasing or even not doing anything
        return max(agent.best_inventory[day-1] - agent.inventory[day-1], 0)

# Q LEARNING  ----------------------------------------------------------------

start_time = time.time()
# the vector of lambdas
lambdas = [lambda_q_learning*(lambda_q_learning**n) for n in range(365)]




p_exploration = max(epsilon_greedy_converges_to ,(total_epochs - j) / total_epochs)


# first part of q function: reward ------------------------------------
day = day
state = agent.policy_inventory[day]
action = create_demand(day)

# being on the day "day" then the reward action is
day = 30
# we "cut" the vector starting on the position "day" and append the rest to the end
rewards = agent.q_function_reward_for_action[day:] + agent.q_function_reward_for_action[0:day]
# afterwards we multiply by the vector of lambdas
discounted_rewards = np.multiply(rewards, lambdas)
# finally we sum and get the value of R
r_s_a = np.sum(discounted_rewards)

# second part of q function: max of q on the next state ---------------
# first we identify what is the next state (day+1, inventory at the end of the day)

# two possible outcomes: the state (day+1,inv) exists already or not
# if yes, then we filter the df to find the max q function of that pair (s',a*)

# if no, then we grab the closest possible match inventory-wise




# third part - update Q function for (s,a) ------------------------------
# Check if the specific (state, action) already exists on the df

# if yes, update the value of both R and Q

# if not, append as a new row to the df


















for j in range(total_epochs):
    if j % (total_epochs/20) == 0:
        print(" ")  # These last two lines are used for printing - just make sure every time point appears clearly separated
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
        # If any agent was fulfilled zero, then their action for that period gets reset to zero
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
            agent.q_function_value[day-1] = 
            # Agent decides demand for today, which will (might) be fulfilled tomorrow
            # 1% of total iterations: try to figure out downstream agent's average demand, to have a warm start
            if j < warmstart_proportion * total_epochs:
                agent.average_downstream_demand = np.mean([agent.average_downstream_demand,
                                                           agent.downstream_agent.current_policy[day-1]])
                agent_demand = np.round(agent.average_downstream_demand)  # because should only ask for integers
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

    #for agent in agents:  # At the end of the year, save the final payout they got
    #    if j % (total_epochs/20) == 0:   # I will only print 20 views, doesn't matter how many epochs
    #        print("Year %s Agent %s current payout %s historical best payout %s" % (j, agent.name, agent.current_payout[-1], agent.best_payout[-1]))
    #    agent.historic_payout.append(agent.current_payout[-1])

    # For each day, the value of its Q function is
    
    
    # For each day, if we found a better Q value then we update the optimal inventory

elapsed_time = time.time() - start_time
print("Total elapsed time for %s epochs : %s" % (total_epochs, elapsed_time))