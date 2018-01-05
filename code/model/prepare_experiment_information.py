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


def insert_on_table(name, columns, data):
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
        print("Uploaded data to table %s" % name)
        if conn is not None:
            conn.close()
    except:
        print("I am unable to insert into the %s database" % name)

# Creating the tables
# Identify the number of experiment
# the id is the hash1 of all the concatenated text,
# including timestamp, of the experiment - this would make it robust
# and easy to track for corrupt records
# experiment_id = random.randint(0, 1000000000) # not in use anymore!
experiment_id = hashlib.sha224((str(time.ctime(start_time)) +\
                                str(retail_agent.best_policy) +\
                                str(wholesale_agent.best_policy) +\
                                str(regional_warehouse_agent.best_policy) +\
                                str(factory_agent.best_policy)).encode('utf-8')).hexdigest()

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
                    "data": (experiment_id, max_demand, customer_agent.current_policy.to_string(), fields_agent.current_policy.to_string(), warehouse_price)})

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
                            "best_payout": str(retail_agent.best_payout),
                            "best_policy": str(retail_agent.best_policy),
                            "historic_payout": str(retail_agent.historic_payout),
                            "policy_inventory": str(retail_agent.policy_inventory),
                            "total_money": retail_agent.total_money},
                            {# Wholesale
                            "experiment_id": experiment_id,
                            "agent": wholesale_agent.name,
                            "best_payout": str(wholesale_agent.best_payout),
                            "best_policy": str(wholesale_agent.best_policy),
                            "historic_payout": str(wholesale_agent.historic_payout),
                            "policy_inventory": str(wholesale_agent.policy_inventory),
                            "total_money": wholesale_agent.total_money},
                            {# Regional Warehouse
                            "experiment_id": experiment_id,
                            "agent": regional_warehouse_agent.name,
                            "best_payout": str(regional_warehouse_agent.best_payout),
                            "best_policy": str(regional_warehouse_agent.best_policy),
                            "historic_payout": str(regional_warehouse_agent.historic_payout),
                            "policy_inventory": str(regional_warehouse_agent.policy_inventory),
                            "total_money": regional_warehouse_agent.total_money},
                            {# Factory
                            "experiment_id": experiment_id,
                            "agent": factory_agent.name,
                            "best_payout": str(factory_agent.best_payout),
                            "best_policy": str(factory_agent.best_policy),
                            "historic_payout": str(factory_agent.historic_payout),
                            "policy_inventory": str(factory_agent.policy_inventory),
                            "total_money": factory_agent.total_money})})

# Insert into the database
tables = (experiments, world_parameters, agent_parameters, experiment_results)

for table in tables:
    insert_on_table(table["name"], table["columns"], table["data"])

