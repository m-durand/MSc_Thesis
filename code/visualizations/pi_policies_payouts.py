##############################################################

# this script fetches data from the database that contains the experiments
# paarameters and prints various plots 

path_to_write_figures = './../../tesis_tex/figs/'
run_iteration_comparison = False

##############################################################################
# Final policies
fig = plt.figure(figsize=(10,7.5))
st = fig.suptitle("Políticas óptimas aprendidas con restricción estacional", fontsize="x-large") # Optimal Learnt Policies

ax1 = fig.add_subplot(221)
ax1.plot(restricted_retail_policy)
ax1.plot(fields_supply_daily['Supply'])
ax1.set_title("Menudeo") #Retail
plt.xlabel('Día')

ax2 = fig.add_subplot(222)
ax2.plot(restricted_wholesale_policy)
ax2.plot(fields_supply_daily['Supply'])
ax2.set_title("Mayoreo") #Wholesale
plt.xlabel('Día')

ax3 = fig.add_subplot(223)
ax3.plot(restricted_regional_warehouse_policy)
ax3.plot(fields_supply_daily['Supply'])
ax3.set_title("Almacén Regional") #Regional Warehouse
plt.xlabel('Día')

ax4 = fig.add_subplot(224)
ax4.plot(restricted_factory_policy)
ax4.plot(fields_supply_daily['Supply'])
ax4.set_title("Fábrica") #Factory
plt.xlabel('Día')

fig.tight_layout()

# shift subplots down:
st.set_y(0.95)
fig.subplots_adjust(top=0.85)

# save this experiment's result
#figname = path_to_write_figures + "policies_" + experiment_id + ".png"
# save as the latest (mainly so the TeX file can pull it by name)
figname_latest = path_to_write_figures + "policyiteration_policies_restricted.png"
#fig.savefig(figname)
fig.savefig(figname_latest)

##############################################################################
# Final policies
fig = plt.figure(figsize=(10,7.5))
st = fig.suptitle("Políticas óptimas aprendidas sin restricción estacional", fontsize="x-large") # Optimal Learnt Policies

ax1 = fig.add_subplot(221)
ax1.plot(nonrestricted_retail_policy)
ax1.set_title("Menudeo") #Retail
plt.xlabel('Día')

ax2 = fig.add_subplot(222)
ax2.plot(nonrestricted_wholesale_policy)
ax2.set_title("Mayoreo") #Wholesale
plt.xlabel('Día')

ax3 = fig.add_subplot(223)
ax3.plot(nonrestricted_regional_warehouse_policy)
ax3.set_title("Almacén Regional") #Regional Warehouse
plt.xlabel('Día')

ax4 = fig.add_subplot(224)
ax4.plot(nonrestricted_factory_policy)
ax4.set_title("Fábrica") #Factory
plt.xlabel('Día')

fig.tight_layout()

# shift subplots down:
st.set_y(0.95)
fig.subplots_adjust(top=0.85)

# save this experiment's result
#figname = path_to_write_figures + "policies_" + experiment_id + ".png"
# save as the latest (mainly so the TeX file can pull it by name)
figname_latest = path_to_write_figures + "policyiteration_policies_nonrestricted.png"
#fig.savefig(figname)
fig.savefig(figname_latest)


##############################################################################
# Historic payout
fig = plt.figure(figsize=(10,7.5))
st = fig.suptitle("Pago final durante el aprendizaje", fontsize="x-large") #Historical Payouts during Learning

ax1 = fig.add_subplot(221)
ax1.plot(retail_agent.historic_payout)
ax1.set_title("Menudeo") #Retail
plt.xlabel('Iteración')
pylab.ylim([-25000,10000])

ax2 = fig.add_subplot(222)
ax2.plot(wholesale_agent.historic_payout)
ax2.set_title("Mayoreo") #Wholesale
plt.xlabel('Iteración')
pylab.ylim([-25000,10000])

ax3 = fig.add_subplot(223)
ax3.plot(regional_warehouse_agent.historic_payout)
ax3.set_title("Almacén regional") #Regional Warehouse
plt.xlabel('Iteración')
pylab.ylim([-25000,10000])

ax4 = fig.add_subplot(224)
ax4.plot(factory_agent.historic_payout)
ax4.set_title("Fábrica") #Factory
plt.xlabel('Iteración')
pylab.ylim([-25000,10000])

fig.tight_layout()

# shift subplots down:
st.set_y(0.95)
fig.subplots_adjust(top=0.85)

# save this experiment's result
#figname = path_to_write_figures + "payouts_" + experiment_id + ".png"
# save as the latest (mainly so the TeX file can pull it by name)
figname_latest = path_to_write_figures + "policyiteration_payouts.png"
#fig.savefig(figname)
fig.savefig(figname_latest)


###############################################################################
####### COMPARING PERFORMANCE (TOTAL FINAL MONEY) BY TOTAL INTERACIONS ########
###############################################################################

# Run training many times with diferent total epochs ################
if run_iteration_comparison == True:
    # Different iterations that will be tested
    iteration_tests = [100,500,1000,1500,2000,2500,
                       3500,4000,5000,6000,7500,
                       10000,12500,15000,17500,
                       20000,25000,30000,35000,40000,45000,50000,
                       60000,70000,80000, 90000, 100000,125000,150000,
                       200000,250000, 300000, 350000,400000,450000,500000]
    
    eval_iter_df_1 = pd.DataFrame(columns=['agent', 'iterations', 'total_money', 'current_payout']) 
    
    # Setting world parameters for all the simulations
    # For an in-depth explanatiof of parameters please refer to the clean run script
    # Getting customer_demand and field_supply trends
    customer_demand = pd.read_csv("./../../aux_documents/customer_trend.csv")
    fields_supply = pd.read_csv("./../../aux_documents/fields_trend.csv")    
    # Prices and Costs
    retail_price = 100
    wholesale_price = 90
    regional_warehouse_price = 80
    factory_price = 70
    field_price = 60
    warehouse_price = 10/365 
    backlog_cost = 1
    # Initial Inventories
    retail_ininv = 10
    wholesale_ininv = 10
    regional_warehouse_ininv = 10
    factory_ininv = 10
    
    for iter_i in iteration_tests:
        total_epochs = iter_i
        # run the learning iterations, always same parameters and random seed
        # Create world #
        exec(open("players.py").read())
        exec(open("world.py").read())
        # Run learning
        #np.random.seed(20170130)
        exec(open("policy_iteration.py").read())
        # Add final payouts to the main dataframe   
        new_row = ['Retail',iter_i,retail_agent.total_money,retail_agent.current_payout[-1]]
        eval_iter_df_1.loc[eval_iter_df.shape[0] + 1] = new_row
        new_row = ['Wholesale',iter_i,wholesale_agent.total_money,wholesale_agent.current_payout[-1]]
        eval_iter_df_1.loc[eval_iter_df.shape[0] + 1] = new_row
        new_row = ['Regional Warehouse',iter_i,regional_warehouse_agent.total_money,regional_warehouse_agent.current_payout[-1]]
        eval_iter_df_1.loc[eval_iter_df.shape[0] + 1] = new_row
        new_row = ['Factory',iter_i,factory_agent.total_money,factory_agent.current_payout[-1]]
        eval_iter_df_1.loc[eval_iter_df.shape[0] + 1] = new_row
    
        eval_iter_df_1.to_csv('./../../aux_documents/evaluate_payout_iterations_2.csv')
    
    # Change levels to spanish to have visualization ready for document
    eval_iter_df_1.columns = ['agente', 'iteración', 'dinero final', 'pago final']
    eval_iter_df_1 = eval_iter_df.replace(['Retail','Wholesale', 'Regional Warehouse','Factory'],
                                ['Menudeo','Mayoreo', 'Almacén Regional','Fábrica'])
    
    
    # Plots ##########################
    
    # Visualizing as a faceted plot
    
    fig = sns.lineplot('iteración', 'dinero final', data=eval_iter_df.iloc[:116,], hue='agente')
    fig.show()
    
    figname_latest = path_to_write_figures + "evaluating_iterations_money_2.png"
    #fig.savefig(figname)
    fig.savefig(figname_latest)

###############################################################################
    
