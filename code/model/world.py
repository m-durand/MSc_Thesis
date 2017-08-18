exec(open("players.py").read())

# Creating Supply Chain Agents
customer_agent = Customer(customer_demand)
retail_agent = Agent("Retail", retail_ininv, retail_price, wholesale_price, warehouse_price)
wholesale_agent = Agent("Wholesale", wholesale_ininv, wholesale_price, regional_warehouse_price, warehouse_price)
regional_warehouse_agent = Agent("Regional_Warehouse", regional_warehouse_ininv, regional_warehouse_price, factory_price, warehouse_price)
factory_agent = Agent("Factory", factory_ininv, factory_price, field_price, warehouse_price)
fields_agent = Fields(fields_supply)

# Assigning interactions
retail_agent.downstream_agent = customer_agent
retail_agent.upstream_agent = wholesale_agent
wholesale_agent.downstream_agent = retail_agent
wholesale_agent.upstream_agent = regional_warehouse_agent
regional_warehouse_agent.downstream_agent = wholesale_agent
regional_warehouse_agent.upstream_agent = factory_agent
factory_agent.downstream_agent = regional_warehouse_agent
factory_agent.upstream_agent = fields_agent
