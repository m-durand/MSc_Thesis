# Beer!

Thesis written to obtain the degree of MSc in Data Science, received honours. This work explores reinforcement learning, namely policy iteration and Q-learning, to solve the famous business problem of the Beer Distribution Game. Furthermore, some assumptions regarding the behavior of the consumer demand and fields supply are changed, in order to make the problem more applicable to the real world. It was concluded that policy iteration works and is flexible and quick enough to implement. The “whiplash effect” was observed, and a valuable business insight was found: entities towards the middle of a supply chain have the highest need for well performing data science models and data scientists.

The final document can be found [here](https://github.com/m-durand/MSc_Thesis/blob/master/final_docs/TesisM.pdf)

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
* `visualizations` which contains mostly R codes to create various plots in R based on outputs
3. `tesis_tex` containg code that generates the final `.tex` file. The subfolder `figs` contains some interesting visualizations.
4. `final_documents` where the final thesis `pdf` and `pptx` files can be found, so that local compiling is not necessary
