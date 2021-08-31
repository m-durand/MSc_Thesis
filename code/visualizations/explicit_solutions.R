# Plotting different views of the easy analitic solution

# Complete year - not a great way to see it because there's too much detail

# Read data ----------------------------------------------------------------
solution_0 <- read_excel("../../aux_documents/explicit_solution.xlsx", sheet = 3,
                         skip = 25) %>% 
  melt(id.vars = c("AGENT / DAY ->")) %>% 
  mutate(name_english = factor(`AGENT / DAY ->`, levels = c("retail", "wholesale", "regional_warehouse", "factory") )) %>% 
  mutate(name_spanish = fct_recode(name_english, "Menudeo" = "retail",
                                   "Mayoreo" = "wholesale",
                                   "Almacen regional" = "regional_warehouse",
                                   "Fabrica" = "factory")) %>% 
  mutate(day = as.numeric(variable)) 

# Infinite supply ---------------------------------------------------------------------------------

# First month with varying initial inventories

month <- ggplot(solution_0 %>% filter(day <=30), aes(x = day, y = value, color = name_spanish)) +
  geom_line(size = 1)  +
  theme_minimal(base_size = 14) +
  #ggtitle("Demanda de los agentes en el primer mes del anio" ) + #,
  #        subtitle = "El tiempo de adecuamiento al patron depende de los inventarios iniciales") + 
  theme(axis.text.y=element_blank()) +
  xlab("Dia") +
  ylab("Cantidad") + guides(color=guide_legend(title="Agente"))  +
  agents_colors_es

#20, 30, 15, 20
ggsave("../../tesis_tex/figs/analytic_solution_0_all_0_inv.png", month, device = "png", width = 246.8, height = 102.5, units = "mm")

# Last month

month <- ggplot(solution_0 %>% filter(day >=335), aes(x = day, y = value, color = name_spanish)) +
  geom_line(size = 1)  +
  theme_minimal(base_size = 8) +
  #ggtitle("Demanda de los agentes en el ultimo mes del anio" ) + #,
          #subtitle = "El tiempo de adecuamiento al patron depende de los inventarios iniciales") + 
  theme(axis.text.y=element_blank()) + 
  xlab("Dia") +
  ylab("Demanda") + guides(color=guide_legend(title="Agente"))  +
  agents_colors_es


ggsave("../../tesis_tex/figs/analytic_solution_0_last_month.png", month, device = "png", width = 246.8, height = 102.5, units = "mm")

# Not infinite supply -----------------------------------------------------------------

solution_1 <- read_excel("../../aux_documents/explicit_solution.xlsx", sheet = 4,
                         skip = 25) %>% 
  melt(id.vars = c("AGENT / DAY ->")) %>% 
  mutate(name_english = factor(`AGENT / DAY ->`, levels = c("consumer", "retail", "wholesale", "regional_warehouse", "factory", "fields") )) %>% 
  mutate(name_spanish = fct_recode(name_english, "Consumidor" = "consumer",
                                   "Menudeo" = "retail",
                                   "Mayoreo" = "wholesale",
                                   "Almacen regional" = "regional_warehouse",
                                   "Fabrica" = "factory",
                                   "Campos" = "fields")) %>% 
  mutate(day = as.numeric(variable)) 

# preparing data for plot
demand <- solution_1 %>% filter(name_english %in% c("consumer")) %>% select(day, demand = value)
supply <- solution_1 %>% filter(name_english %in% c("fields")) %>% select(day, supply = value)

# how does inventory decrease?
inventory_decrease <- read_excel("../../aux_documents/explicit_solution.xlsx", sheet = 4,n_max = 21) %>% 
  filter(`DAY ->` == "inventory") %>% 
  melt(id.vars = c("AGENT", "DAY ->")) %>% 
  transmute(name_english = AGENT,
            day = as.double(variable),
            inventory = value)

with_fields_restriction <- solution_1 %>% 
  filter(name_english %in% c("retail", "wholesale", "regional_warehouse", "factory")) %>% 
  left_join(demand) %>% 
  left_join(supply) %>% 
  left_join(inventory_decrease) %>% 
  ggplot(aes(x = day)) +
  geom_area(aes(y = demand), alpha = 0.25, fill = "#FE0068") +
  geom_area(aes(y = supply), alpha = 0.25, fill = "#6CAE3C")+
  geom_area(aes(y = value), color = "black", size = 0.1)  +
  geom_line(aes(y = inventory), color = "black", size = 0.1)  +
  theme_minimal(base_size = 14)   +
  #ggtitle("Demanda de cada agente durante el a?o, suponiendo falta de almacenes",
  #        subtitle = "Cuando la oferta (verde) es menor a la demanda (rosa), las politicas toman la forma de la oferta; cuando es mayor, toman la de la demanda") + 
  theme(axis.text.y=element_blank()) +
  xlab("Dia") +
  ylab("Demanda") + guides(color=guide_legend(title="Agente"))  +
  agents_colors_es +
  facet_wrap(~name_spanish, nrow = 4) +
  theme(legend.position="none") #+
  #geom_segment
  # geom_label o geom_text

ggsave("../../tesis_tex/figs/analytic_with_fields_restriction.png", with_fields_restriction, device = "png", width = 246.8, height = 102.5, units = "mm")
