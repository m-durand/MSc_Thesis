agents = [retail_agent, wholesale_agent, regional_warehouse_agent, factory_agent]


def create_demand(agent):
    x = np.random.uniform(0, 1)
    if x < p_exploration:  # exploRation
        return np.random.randint(0, max_demand)  # 70 is the maximum harvest of all year, occurs August 15th
    else:  # exploTation we want to get the action that maximizes the q function for that state
        subset_current = q_learning_df.loc[(q_learning_df['agent'] == (agent.name)) & (q_learning_df['day'] == (day)) & (q_learning_df['inventory'] == (agent_inventory))]
        subset_current = subset_current.reset_index()
        if subset_current.shape[0] > 0:
            best_action = subset_current.iloc[[subset_current["q_s_a"].idxmax()]]
            return best_action["purchase"].values.item(0)
        else:
            return np.random.randint(0, max_demand)

# Q LEARNING  ----------------------------------------------------------------

start_time = time.time()

# the table that may contain the q learning values, it may be empty
#q_learning_df = [] # TODO return from sql database
q_learning_df = pd.read_csv("../../aux_documents/temp_q_learning_output.csv")
# the vector of lambdas
lambdas = [lambda_q_learning*(lambda_q_learning**n) for n in range(365)]

# epochs for ----
for j in range(total_epochs):
    print("iteration " + str(j) + " time " + str(datetime.datetime.now()))
    if j % (total_epochs/20) == 0:
        print(" ")  # These last two lines are used for printing - just make sure every time point appears clearly separated
    # starts in 1 ends in the first number so it always explores a bit
    p_exploration = max(epsilon_greedy_converges_to, (total_epochs - j) / total_epochs)
    day = 0
    # Reinitialize and money, etc at the beginning of the year
    for agent in agents:
        # we do not reinitialize inventory because we want it to learn that it has to keep some for next year too
        agent.total_warehousing_costs = 0  # we actually wont use this
        agent.total_money = 0
        agent.backlog = 0  # we actually wont use this

    # day for ----
    while day < 365:
        day+=1
        ################################# TRANSACTIONS BETWEEN AGENTS ###############
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
            #print(str(agent.name))
            # PART 2
            # How much money did the agent end up with yesterday's decisions?
            agent.current_payout[day-1] = agent.total_money
            agent.q_function_reward_for_action[day-1] = agent.current_payout[day-1] - agent.current_payout[day-2]
            # Agent decides demand for today, which will (might) be fulfilled tomorrow
            agent_demand = create_demand(agent)
            #agent_demand = 0  #If we want to evaluate any static policy
            agent.current_policy[day-1] = agent_demand
            # Paying for warehousing at the end of the day
            agent.pay_for_warehousing()

            # first part of q function: reward ------------------------------------
            day = day
            agent_inventory = agent.policy_inventory[day-1]

            # Removed because it is better to just use the one-day reward, no need for discounted
            # being on the day "day" then the reward action is ...
            # we "cut" the vector starting on the pos "day" and append the rest to the end
            # rewards = agent.q_function_reward_for_action[day:] + agent.q_function_reward_for_action[0:day]
            # afterwards we multiply by the vector of lambdas
            # discounted_rewards = np.multiply(rewards, lambdas)
            # finally we sum and get the value of R
            # r_s_a = np.sum(discounted_rewards)

            # money it had yesterday minus money it has today
            r_s_a = agent.q_function_reward_for_action[day-1]

            # second part of q function: max of q on the next state ---------------

            # first we identify what is the next state (day+1, inv at the end of the day)
            # two possible outcomes: the state (day+1,inv) exists already or not
            #print("first checkpoint time " + str(datetime.datetime.now()))

            if day == 365:
                next_day = 1
            else:
                next_day = day + 1
            subset_s_prime_a_all = q_learning_df.loc[(q_learning_df['agent'] == (agent.name)) & (q_learning_df['day'] == (next_day)) & (q_learning_df['inventory'] == (agent_inventory + agent_demand))]

            # if yes, then we filter the df to find the max q function of that pair (s',a*)
            # if no, then we set q(s',a*) as zero, the default value
            #print("second checkpoint time " + str(datetime.datetime.now()))
            if subset_s_prime_a_all.shape[0] > 0:
                max_q_s_prime_a_all = subset_s_prime_a_all['q_s_a'].max()
            else:
                max_q_s_prime_a_all = 0

            # Finally get the value of Q!!
            q_s_a = r_s_a + (lambda_q_learning * max_q_s_prime_a_all)

            # third part - update Q function for (s,a) ------------------------------
            # eliminate the row from the data frame (if it existed)
            # print("third checkpoint time " + str(datetime.datetime.now()))
            #q_learning_df = q_learning_df.loc[((q_learning_df['agent'] != (agent.name)) | (q_learning_df['day'] != (day)) | (q_learning_df['inventory'] != (agent_inventory)) | (q_learning_df['purchase'] != (agent_demand)))]
            # append the newly created row to update the value of both R and Q
            new_row = [agent.name, day, agent_inventory, agent_demand, r_s_a, q_s_a]
            q_learning_df.loc[q_learning_df.shape[0] + 1] = new_row
            q_learning_df.sort_values('q_s_a', ascending=False).drop_duplicates(['agent','day','inventory','purchase'])

elapsed_time = time.time() - start_time
print("Total elapsed time for %s epochs : %s" % (total_epochs, elapsed_time))
#iteration 1 time 2019-01-03 16:44:23.911986
#iteration 100 time 2019-01-03 22:29:07.282015
#iteration 200 time 2019-01-05 00:32:39.527549
#iteration 300 time 2019-01-05 19:19:41.775814
#iteration 399 time 2019-01-07 02:15:32.058813
#Total elapsed time for 400 epochs : 294681.67162013054

# TEMP THIS SHOULD GO TO A TABLE, FOR NOW A CSV
q_learning_df.to_csv("../../aux_documents/temp_q_learning_output_from_algorithm" + str(datetime.datetime.now()) + ".csv")



