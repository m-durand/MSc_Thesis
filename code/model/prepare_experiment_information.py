# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 14:55:20 2017

@author: Fernanda Alcala
"""

# Creates and inserts 4 data frames into the database after each experiment
# 0. Experiments
# 1. World parameters
# 2. Agent parameters
# 3. Experiment results


def insert(name, columns, data):
    '''Function to insert the form data 'data' into table 'table'
    according to the columns in 'columns' '''
    try:
        # Create the connection, insert the data, commit, close
        conn = psycopg2.connect(connection_params)
        # create a new cursor
        cur = conn.cursor()
        # Depending on the table, single ur multiple insertions are needed
        if name == "experiments" or name == "world_parameters":
            sql_query_empty = """INSERT INTO policy_iteration.%s (%s) VALUES %s;"""
            # Create the final query to be executed
            sql_query = sql_query_empty % (name, columns, data)
            # Execute query
            cur.execute(sql_query)
        elif name == "agent_parameters":
            sql_query_semi = "INSERT INTO " + name + "(" + columns + ") " + """VALUES %(experiment_id)s, %(agent)s, %(initial_inventory)s, %(buying_price)s, %(selling_price)s;"""
            # Execute query: for many need a mapping
            # https://stackoverflow.com/questions/8134602/psycopg2-insert-multiple-rows-with-one-query
            cur.executemany(sql_query_semi, data)
        elif name == "experiment_results":
            sql_query_semi = "INSERT INTO " + name + "(" + columns + ") " + """VALUES %(experiment_id)s, %(agent)s, %(best_payout)s, %(best_policy)s, %(historic_payout)s, %(policy_inventory)s, %(total_money)s;"""
            # Execute query: for many need a mapping
            cur.executemany(sql_query_semi, data)
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
        if conn is not None:
            conn.close()
    except:
        print*"I am unable to connect to the database"()

# Creating the tables
# Before everything, identify the number of experiment
# TODO - change the id to hash1 of all the concatenated text,
# including timestamp, of the experiment
experiment_id = random.randint(0, 1000000000)

# 0. Experiments
# Values to be inserted
experiments = ({"name": "experiments",
                "columns": """experiment_id ,datetime, total_epochs,
                            warmstart_proportion,
                            epsilon_greedy_converges_to, elapsed_time""",
                "data": (experiment_id, time.ctime(start_time), total_epochs,
                        warmstart_proportion,
                        epsilon_greedy_converges_to, elapsed_time)})

# 1. World parameters
world_parameters = ({"name": "world_parameters",
                    "columns": """experiment_id, max_demand, customer_demand, fields_supply, warehouse_price""",
                    "data": (experiment_id, max_demand, customer_agent.current_policy, fields_agent.current_policy, warehouse_price)})

# 2. Agent parameters
agent_parameters = ({"name": "agent_parameters",
                     "columns": """experiment_id, agent, initial_inventory, buying_price, selling_price""",
                     "data": ({# Retail
                        "experiment_id": experiment_id,
                        "agent": retail_agent.name,
                        "initial_inventory": retail_agent.initial_inventory,
                        "buying_price": retail_agent.buying_price,
                        "selling_price": retail_agent.selling_price},
                        {# Wholesale
                        "experiment_id": experiment_id,
                        "agent": wholesale_agent.name,
                        "initial_inventory": wholesale_agent.initial_inventory,
                        "buying_price": wholesale_agent.buying_price,
                        "selling_price": wholesale_agent.selling_price},
                        {# Regional Warehouse
                        "experiment_id": experiment_id,
                        "agent": regional_warehouse_agent.name,
                        "initial_inventory": regional_warehouse_agent.initial_inventory,
                        "buying_price": regional_warehouse_agent.buying_price,
                        "selling_price": regional_warehouse_agent.selling_price},
                        {# Factory
                        "experiment_id": experiment_id,
                        "agent": factory_agent.name,
                        "initial_inventory": factory_agent.initial_inventory,
                        "buying_price": factory_agent.buying_price,
                        "selling_price": factory_agent.selling_price})
                     })

# 3. Experiment results
experiment_results = ({"name": "experiment_results",
                    "columns": """experiment_id, agent, best_payout, best_policy, historic_payout, policy_inventory, total_money""",
                    "data": ({# Retail
                            "experiment_id": experiment_id,
                            "agent": retail_agent.name,
                            "best_payout": retail_agent.best_payout,
                            "best_policy": retail_agent.best_policy,
                            "historic_payout": retail_agent.historic_payout,
                            "policy_inventory": retail_agent.policy_inventory,
                            "total_money": retail_agent.total_money},
                            {# Wholesale
                            "experiment_id": experiment_id,
                            "agent": wholesale_agent.name,
                            "best_payout": wholesale_agent.best_payout,
                            "best_policy": wholesale_agent.best_policy,
                            "historic_payout": wholesale_agent.historic_payout,
                            "policy_inventory": wholesale_agent.policy_inventory,
                            "total_money": wholesale_agent.total_money},
                            {# Regional Warehouse
                            "experiment_id": experiment_id,
                            "agent": regional_warehouse_agent.name,
                            "best_payout": regional_warehouse_agent.best_payout,
                            "best_policy": regional_warehouse_agent.best_policy,
                            "historic_payout": regional_warehouse_agent.historic_payout,
                            "policy_inventory": regional_warehouse_agent.policy_inventory,
                            "total_money": regional_warehouse_agent.total_money},
                            {# Factory
                            "experiment_id": experiment_id,
                            "agent": factory_agent.name,
                            "best_payout": factory_agent.best_payout,
                            "best_policy": factory_agent.best_policy,
                            "historic_payout": factory_agent.historic_payout,
                            "policy_inventory": factory_agent.policy_inventory,
                            "total_money": factory_agent.total_money})})

# Insert into the database
tables = (experiments, world_parameters, agent_parameters, experiment_results)

for table in tables:
    insert(table["name"], table["columns"], table["data"])

