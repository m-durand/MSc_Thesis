##############################################################

# this script fetches data from the database that contains the experiments
# paarameters and prints various plots 

path_to_write_figures = './../../tesis_tex/figs/'
run_iteration_comparison = False

##############################################################################
# Gif for training up until policies


##### First take all the csvs and turn them into plots
# Iterate over agents
agent_names = ["retail_agent", "wholesale_agent",
               "regional_warehouse_agent", "factory_agent"]

for agent_name in agent_names:
    k = 0
    # get the csvs for each agent
    def num_string(x):
        num = re.findall(r'\d+', x)
        return(int(num[0]))
    
    agent_csvs = sorted(glob.glob('../../aux_documents/training_gif/csvs/' + agent_name + '*.csv'), key = num_string)
    
    # iterate over each csv, create the corresponding plot
    for agent_csv in agent_csvs:
        # read each file
        current_policy_for_plot = pd.read_csv(agent_csv)
        current_policy_for_plot.set_axis(['día', 'policy'], axis='columns', inplace=True)
        
        # create the plot
        figname_latest = "../../aux_documents/training_gif/figs/" + agent_name +"_" + str(k) + ".png"
        
        sns.set()
        sns.set_style(style='white')
        plt.clf()
        fig = sns.lineplot('día', 'policy', data=current_policy_for_plot)
        fig.set(ylim=(0, 100)) 
        fig_get = fig.get_figure()
        fig_get.savefig(figname_latest)
        
        k = k + 1

# Then grab each agents' pngs and create a gif for each
for agent_name in agent_names:
    agent_figs = sorted(glob.glob('../../aux_documents/training_gif/figs/' + agent_name + '*.png'), key = num_string)
              
    with imageio.get_writer('../../aux_documents/training_gif/' + agent_name  + '.gif', mode='I') as writer:
        for filename in agent_figs:
            image = imageio.imread(filename)
            writer.append_data(image)



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
    iteration_tests = [(x*10000)+10000 for x in range(50)]
    
    eval_iter_df = pd.DataFrame(columns=['agent', 'iterations', 'total_money', 'current_payout']) 
    
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
        eval_iter_df.loc[eval_iter_df.shape[0] + 1] = new_row
        new_row = ['Wholesale',iter_i,wholesale_agent.total_money,wholesale_agent.current_payout[-1]]
        eval_iter_df.loc[eval_iter_df.shape[0] + 1] = new_row
        new_row = ['Regional Warehouse',iter_i,regional_warehouse_agent.total_money,regional_warehouse_agent.current_payout[-1]]
        eval_iter_df.loc[eval_iter_df.shape[0] + 1] = new_row
        new_row = ['Factory',iter_i,factory_agent.total_money,factory_agent.current_payout[-1]]
        eval_iter_df.loc[eval_iter_df.shape[0] + 1] = new_row
    
        eval_iter_df.to_csv('./../../aux_documents/evaluate_payout_iterations.csv')
    
    # Change levels to spanish to have visualization ready for document
    eval_iter_df.columns = ['id', 'agente', 'iteración', 'dinero final', 'pago final']
    eval_iter_df = eval_iter_df.replace(['Retail','Wholesale', 'Regional Warehouse','Factory'],
                                ['Menudeo','Mayoreo', 'Almacén Regional','Fábrica'])
    
    # Plots ##########################  
    
    # Visualizing as a faceted plot
    
    fig = sns.lineplot('iteración', 'dinero final', data=eval_iter_df_1, hue='agente')
    fig.set(ylim=(0, 8000))
    fig.show()
    
    figname_latest = path_to_write_figures + "evaluating_iterations_money_2.png"
    #fig.savefig(figname)
    fig.savefig(figname_latest)

###############################################################################
    
