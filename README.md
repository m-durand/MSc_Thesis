# Beer!

_[NOTE: while the README and the code are in English, the document is written in Spanish and the commits are a strange mix of both - depending on my caffeine level, mostly. Trying to make the code accesible while complying to external language requirements has proven a massive challenge. Thank you for being patient!]_

**Reinforcement learning applied to a model based on agents playing _The Beer Distribution Game_.**

The basic structure of this repository is:
1. `aux_documents` contains documents for creating the consumer's demand, fields' supply, and a simple file showing that the explicit solution needs reiteration on itself.
2. `code` contains the following structure:
* `etl`, where the necessary files for creating the PostgreSQL database can be found. This database houses the results of the different iterations
* `model` contains a main file, `clean_run.py`, which calls:
  - `world.py` creates the world for agents
  - `players.py` creates all the agents (retailer, wholesaler, regional warehouse, factory) and non-agents (customer and fields)
  - `policy_iteration.py` trains the agents to solve _The Beer Distribution Game_ using policy iteration
  - `q_learning.py` trains the agents to solve _The Beer Distribution Game_ using Q-learning
  - `insert_experiment_into_[pi/q]_database` which prepares the data on flat tables and inserts them into the database
  - other Jupyter notebooks - temporary files to be removed on the final repo structure - they contain visualizations in _Bokeh_, for which the rendering on Github's inferface is not ideal - feel free to ignore
* `visualizations` which contains mostly R codes to create various plots in R based on outputs
3. `tesis_tex` containg code that generates the final `.tex` file. The subfolder `figs` contains some interesting visualizations. A pdf with the latest version of the document can also be found, so that local compiling would not be necessary.
