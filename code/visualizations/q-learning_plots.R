# This script takes as input a set of q-learning alrgorithm
# "Semi- outputs" to create analyses about how fast it is converging to a maximum
# Etc


# Specific iteration folder that will be read
# (In reality this should be tables in SQL)
folder_iter <- "iter 2019-09-11/"

############# Part 1: analyze time it takes for each new iteration ###########
# does it grow exponentially?
# Answer: it seems to grow logarithmically but then linearly
# It takes 2.75 days to run 1500 iterations

times_file <- read_csv(paste0("../../aux_documents/", folder_iter,
                              list.files(paste0("../../aux_documents/", folder_iter),
                                pattern = "times")), col_names = FALSE)

time_per_iter <- times_file %>% 
  mutate(time_lag = c(times_file$X1[2:nrow(times_file)], NA)) %>% 
  transmute(iter = 1:n(),
            time_taken = time_lag - X1,
            time_taken = as.numeric(time_taken)) %>% 
  na.omit()

ggplot(time_per_iter, aes (x = iter, y = time_taken)) +
  geom_smooth(method='lm',formula=y~x, size = 0.5, linetype="dotted") +
  geom_line() +
  xlab("Numero de iteracion") +
  ylab("Segundos") +
  theme_minimal()

###### Part 2: iteratively, read in each 10-minute increment file and ########
# understand how the algorithm is getting better and better payouts for each player

iter_partial_files <- list.files(paste0("../../aux_documents/", folder_iter),
                                         pattern = "output")

demands_no_noise <- read_csv("../../aux_documents/customer_trend.csv")

fields_no_noise <- read_csv("../../aux_documents/fields_trend.csv")

# Helper to transform day (1-365) to date on two columns
day_to_date_cols <- fields_no_noise %>% 
  dplyr::select(Month, Day) %>% 
  mutate(day = 1:n())

# Create an empty data frame that will receive the q_s_a payouts to compare over time
q_s_a_over_time <- data_frame(agent = character(),
                              total_q_s_a = numeric(),
                              iter_file = numeric())

# Read in a file
for(i in 1:length(iter_partial_files)){
  iter_file_name <- iter_partial_files[i]
  
  f <- read_csv(paste0("../../aux_documents/", folder_iter, iter_file_name)) %>% 
    left_join(day_to_date_cols) %>% 
    # Figure out the best path for each agent
    group_by(agent, Month, Day) %>% 
    top_n(n = 1, wt = -q_s_a) %>% 
    # If two inventories yield the same payout, it means they were not fulfilled so
    # we just take the lowest ask for purchase
    group_by(agent, Month, Day) %>% 
    top_n(n = 1, wt = purchase) %>% 
    # Figure out the payouts for each agent based on this path
    group_by(agent) %>% 
    summarise(total_q_s_a = sum(q_s_a)) %>% 
    mutate(iter_file = i) %>% 
    mutate(agente = fct_recode(agent, "Menudeo" = "Retail",
                                     "Mayoreo" = "Wholesale",
                                     "Almacen regional" = "Regional_Warehouse",
                                     "Fabrica" = "Factory"))
  
  # # Code to see the optimal paths on a specific iteration file
  # ggplot(f, aes (x = day, y = purchase, color = agent)) +
  #   geom_line() +
  #   agents_colors_en
  
  # Save as a new row on a data frame
  q_s_a_over_time <- q_s_a_over_time %>% 
    bind_rows(f)
}

# Code to see the optimal paths on a specific iteration file
q_s_a_over_time_plot <- ggplot(q_s_a_over_time, aes (x = iter_file, y = total_q_s_a, color = agente)) +
  geom_line() +
  ylab("Funcion Q") +
  xlab("Iteracion") +
  facet_wrap(~agente, ncol = 2) +
  agents_colors_es  +
  theme_minimal() +
  theme(legend.position = "none")

q_s_a_over_time_plot

ggsave("../../tesis_tex/figs/q_function_over_time.png", q_s_a_over_time_plot, device = "png")
  