class Customer:
    """
    This type of agent doesn't learn,
    just interacts with Retail by demanding beer
    """
    def __init__(self, demand_trend):
        self.current_policy = demand_trend['Demand']*5


class Fields:
    """
    This type of agent doesn't learn,
    just interacts with Factory by supplying beer
    """
    def __init__(self, supply_trend):
        self.current_policy = supply_trend['Supply']


class Agent:
    """
    Creates a Beer Supply Chain Agent ready to start interacting
    with other agents and learn.
    input:
    * name (string) indicating the type of agent, can be one of four:
    {Retail,Wholesale,Regional_Warehouse,Factory}
    * inventory (numeric) starting inventory at day 1
    output: an object orders_that_could_be_fulfilled type Agent
    """
    def __init__(self, name, inventory, selling_price,
                 buying_price, warehouse_price):

        # I am letting different levels have different selling & buying prices
        # This could also include different warehousing/backlogs costs
        self.selling_price = selling_price
        self.buying_price = buying_price

        self.name = name
        self.initial_inventory = inventory
        self.inventory = inventory
        self.policy_inventory = [self.initial_inventory] + [-1] * 364
        self.total_warehousing_costs = 0
        self.total_money = 0
        self.backlog = 0
        self.current_policy = np.random.randint(1, max_demand, 365)
        self.current_payout = [-100000000] * 365
        self.q_function_value = [-10000000] * 365
        self.best_policy = self.current_policy
        self.best_payout = [-100000000] * 365
        self.best_inventory = [self.initial_inventory] + [0] * 364
        self.best_q_function_value = [-10000000] * 365
        self.historic_payout = []
        self.time_for_zero_policy = np.random.uniform(0,1)

        # These relationships are assigned after the agents are created
        self.downstream_agent = ""
        self.upstream_agent = ""
        # This is needed for having a warm start and not going crazy
        self.average_downstream_demand = 0

    def pay_for_warehousing(self):
        # Pays for warehousing of inventory: must be done either
        # "first thing in the morning" or "last time in the night"
        self.total_money = self.total_money - \
                (self.inventory * warehouse_price)
        self.total_warehousing_costs = self.total_warehousing_costs + \
                (self.inventory * warehouse_price)
        
    def receive_upstream(self, orders):
        # Receives orders from upstream agent first thing in the morning
        self.inventory = self.inventory + orders
        self.total_money = self.total_money - \
                (orders * self.buying_price)

    def give_downstream(self, orders):
        # Checks if he has availability to fulfill order,
        # fulfills as much as he can
        if self.inventory >= orders:
            self.total_money = self.total_money + \
                (orders * self.selling_price)
            self.inventory = self.inventory - orders
            return orders
        else:
            orders_that_could_be_fulfilled = self.inventory
            # Sells all its inventory
            self.total_money = self.total_money + \
                (orders_that_could_be_fulfilled * self.selling_price)
            # If there were non fulfilled orders, those cause a penalty
            self.backlog = (orders - self.inventory) * backlog_cost
            self.total_money = self.total_money - self.backlog
            self.inventory = 0
            return orders_that_could_be_fulfilled
