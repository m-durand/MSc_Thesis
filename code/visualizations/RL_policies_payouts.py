#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 13 13:28:51 2018

@author: fernandaalcala
"""
##############################################################

# this script fetches data from the database that contains the experiments
# paarameters and prints various plots 

import matplotlib
from matplotlib import pyplot as plt

path_to_write_figures = '/Users/fernandaalcala/Documents/Tesis_Maestria/tesis_tex/figs/'

##############################################################################
# Final policies
fig = plt.figure(figsize=(10,7.5))
st = fig.suptitle("Optimal Learnt Policies", fontsize="x-large")

ax1 = fig.add_subplot(221)
ax1.plot(retail_agent.best_policy)
ax1.plot(fields_agent.current_policy)
ax1.set_title("Retail")

ax2 = fig.add_subplot(222)
ax2.plot(wholesale_agent.best_policy)
ax2.plot(fields_agent.current_policy)
ax2.set_title("Wholesale")

ax3 = fig.add_subplot(223)
ax3.plot(regional_warehouse_agent.best_policy)
ax3.plot(fields_agent.current_policy)
ax3.set_title("Regional Warehouse")

ax4 = fig.add_subplot(224)
ax4.plot(factory_agent.best_policy)
ax4.plot(fields_agent.current_policy)
ax4.set_title("Factory")

fig.tight_layout()

# shift subplots down:
st.set_y(0.95)
fig.subplots_adjust(top=0.85)

# save this experiment's result
figname = path_to_write_figures + "policies_" + experiment_id + ".png"
# save as the latest (mainly so the TeX file can pull it by name)
figname_latest = path_to_write_figures + "policies.png"
#fig.savefig(figname)
fig.savefig(figname_latest)

##############################################################################
# Historic payout
fig = plt.figure(figsize=(10,7.5))
st = fig.suptitle("Historical Payouts during Learning", fontsize="x-large")

ax1 = fig.add_subplot(221)
ax1.plot(retail_agent.historic_payout)
ax1.set_title("Retail")

ax2 = fig.add_subplot(222)
ax2.plot(wholesale_agent.historic_payout)
ax2.set_title("Wholesale")

ax3 = fig.add_subplot(223)
ax3.plot(regional_warehouse_agent.historic_payout)
ax3.set_title("Regional Warehouse")

ax4 = fig.add_subplot(224)
ax4.plot(factory_agent.historic_payout)
ax4.set_title("Factory")

fig.tight_layout()

# shift subplots down:
st.set_y(0.95)
fig.subplots_adjust(top=0.85)

# save this experiment's result
figname = path_to_write_figures + "payouts_" + experiment_id + ".png"
# save as the latest (mainly so the TeX file can pull it by name)
figname_latest = path_to_write_figures + "payouts.png"
#fig.savefig(figname)
fig.savefig(figname_latest)

