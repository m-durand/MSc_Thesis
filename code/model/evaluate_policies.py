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
total_epochs = 250000 


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

for agent in ["retail", "wholesale", "regional warehouse", "factory"]:
    for i in range(250):
        
        print(i)
        
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
     
        # Dumb: all agents have constant demand equal to average yearly demand
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
        new_row = [i,agent,'Smart','Retail',smart_retail_final_money]
        eval_policies_df.loc[eval_policies_df.shape[0] + 1] = new_row
        new_row = [i,agent,'Smart','Wholesale',smart_wholesale_final_money]
        eval_policies_df.loc[eval_policies_df.shape[0] + 1] = new_row
        new_row = [i,agent,'Smart','Regional Warehouse',smart_regional_warehouse_final_money]
        eval_policies_df.loc[eval_policies_df.shape[0] + 1] = new_row
        new_row = [i,agent,'Smart','Factory',smart_factory_final_money]
        eval_policies_df.loc[eval_policies_df.shape[0] + 1] = new_row
        new_row = [i,agent,'Dumb','Retail',dumb_retail_final_money]
        eval_policies_df.loc[eval_policies_df.shape[0] + 1] = new_row
        new_row = [i,agent,'Dumb','Wholesale',dumb_wholesale_final_money]
        eval_policies_df.loc[eval_policies_df.shape[0] + 1] = new_row
        new_row = [i,agent,'Dumb','Regional Warehouse',dumb_regional_warehouse_final_money]
        eval_policies_df.loc[eval_policies_df.shape[0] + 1] = new_row
        new_row = [i,agent,'Dumb','Factory',dumb_factory_final_money]
        eval_policies_df.loc[eval_policies_df.shape[0] + 1] = new_row
        new_row = [i,agent,'Dumber','Retail',dumber_retail_final_money]
        eval_policies_df.loc[eval_policies_df.shape[0] + 1] = new_row
        new_row = [i,agent,'Dumber','Wholesale',dumber_wholesale_final_money]
        eval_policies_df.loc[eval_policies_df.shape[0] + 1] = new_row
        new_row = [i,agent,'Dumber','Regional Warehouse',dumber_regional_warehouse_final_money]
        eval_policies_df.loc[eval_policies_df.shape[0] + 1] = new_row
        new_row = [i,agent,'Dumber','Factory',dumber_factory_final_money]
        eval_policies_df.loc[eval_policies_df.shape[0] + 1] = new_row
        
        eval_policies_df.to_csv('./../../aux_documents/evaluate_policies.csv')

# Create the indices based on the "dumber" policy to interpret uplifts
eval_policies_df_ids = eval_policies_df.pivot_table(index=['iteration','agent'], columns='strategy', values = 'money', aggfunc=np.sum)
eval_policies_df_ids['Dumber_idx'] = (eval_policies_df_ids['Dumber']-eval_policies_df_ids['Dumber'])/abs(eval_policies_df_ids['Dumber'])
eval_policies_df_ids['Dumb_idx'] = (eval_policies_df_ids['Dumb']-eval_policies_df_ids['Dumber'])/abs(eval_policies_df_ids['Dumber'])
eval_policies_df_ids['Smart_idx'] = (eval_policies_df_ids['Smart']-eval_policies_df_ids['Dumber'])/abs(eval_policies_df_ids['Dumber'])
eval_policies_df_ids = eval_policies_df_ids.stack().reset_index()
eval_policies_df_ids = eval_policies_df_ids[eval_policies_df_ids['strategy'].isin(['Dumber_idx', 'Dumb_idx', 'Smart_idx'])]
eval_policies_df_ids['strategy'] = eval_policies_df_ids['strategy'].str.slice(0, -4)
eval_policies_df_ids.columns = ['iteration', 'agent', 'strategy', 'index']

eval_policies_df_complete = eval_policies_df.set_index(['iteration','strategy','agent']).join(eval_policies_df_ids.set_index(['iteration','strategy','agent'])).reset_index()

#This part creates the same dataframe but in Spanish since the final document needs the viz
eval_policies_df_sp = eval_policies_df_ids
eval_policies_df_sp.columns = ['iteracion', 'agente', 'estrategia', 'desempeño']
eval_policies_df_sp = eval_policies_df_sp.replace(['Retail','Wholesale', 'Regional Warehouse','Factory'],
                            ['Menudeo','Mayoreo', 'Almacén Regional','Fábrica'])
eval_policies_df_sp = eval_policies_df_sp.replace(['Dumber','Dumb', 'Smart'],
                            ['Nadie óptima','Un agente óptimo', 'Todos óptima'])

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
grid.set(xlim=(-1, eval_policies_df_sp_no_outl['desempeño'].max()), ylim=(0,6))
grid.add_legend()


# Add vertical lines for mean age on each plot
def vertical_mean_line_base(x, **kwargs):
    plt.axvline(0, linestyle = '--', color = 'b')

grid.map(vertical_mean_line_base, 'desempeño') 

grid.set_ylabels('Densidad', size=12)

plt.show()


