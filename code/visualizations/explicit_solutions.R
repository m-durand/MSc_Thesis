# Plotting different views of the easy analitic solution

# Complete year - not a great way to see it because there's too much detail

wd <- "C:/Users/Fernanda Alcala/Documents/Personal/Tesis_Maestria/aux_documents/"
setwd(wd)

library(readxl)
library(ggplot2)
library(tidyverse)
library(reshape2)
library(forcats)

# Read data ----------------------------------------------------------------
solution_0 <- read_excel("explicit_solution.xlsx", sheet = 3,
                         skip = 25) %>% 
  melt(id.vars = c("AGENT / DAY ->")) %>% 
  mutate(name_english = factor(`AGENT / DAY ->`, levels = c("retail", "wholesale", "regional_warehouse", "factory") )) %>% 
  mutate(name_spanish = fct_recode(name_english, "Menudeo" = "retail",
                                   "Mayoreo" = "wholesale",
                                   "Almacen regional" = "regional_warehouse",
                                   "Fabrica" = "factory")) %>% 
  mutate(day = as.numeric(variable)) 


#Create a custom color scale for agents - lets use throughout the whole doc -----
library(RColorBrewer)
# english scale
myColors_en <- c("#F60027", "#FDB34B", "#F76B50", "#006D6F")
# c("#FE0068", "#F60027", "#FDB34B", "#F76B50", "#006D6F", "#6CAE3C") # if it contains customer and fields
names(myColors_en) <- levels(solution_0$name_english)
agents_colors_en <- scale_colour_manual(name = "name_english",values = myColors_en)
# english scale
myColors_es <- c("#F60027", "#FDB34B", "#F76B50", "#006D6F")
# c("#FE0068", "#F60027", "#FDB34B", "#F76B50", "#006D6F", "#6CAE3C") # if it contains customer and fields
names(myColors_es) <- levels(solution_0$name_spanish)
agents_colors_es <- scale_colour_manual(name = "name_spanish",values = myColors_es)

# Infinite supply ---------------------------------------------------------------------------------

# First month with varying initial inventories

month <- ggplot(solution_0 %>% filter(day <=30), aes(x = day, y = value, color = name_spanish)) +
  geom_line(size = 1)  +
  theme_minimal(base_size = 8) +
  ggtitle("Demanda de los agentes en el primer mes del año - todos comienzan con inventarios diferentes",
          subtitle = "El tiempo de adecuamiento al patron depende de los inventarios iniciales") + 
  theme(axis.text.y=element_blank()) +
  xlab("Dia") +
  ylab("Demanda") + guides(color=guide_legend(title="Agente"))  +
  agents_colors_es

#20, 30, 15, 20
ggsave("~/Personal/Tesis_Maestria/tesis_tex/figs/analytic_solution_0_all_0_inv.png", month, device = "png", width = 246.8, height = 102.5, units = "mm")

# Last month

month <- ggplot(solution_0 %>% filter(day >=335), aes(x = day, y = value, color = name_spanish)) +
  geom_line(size = 1)  +
  theme_minimal(base_size = 8) +
  ggtitle("Demanda de los agentes en el primer mes del año - todos comienzan con inventarios diferentes",
          subtitle = "El tiempo de adecuamiento al patron depende de los inventarios iniciales") + 
  theme(axis.text.y=element_blank()) + 
  xlab("Dia") +
  ylab("Demanda") + guides(color=guide_legend(title="Agente"))  +
  agents_colors_es


ggsave("~/Personal/Tesis_Maestria/tesis_tex/figs/analytic_solution_0_last_month.png", month, device = "png", width = 246.8, height = 102.5, units = "mm")

# Not infinite supply -----------------------------------------------------------------


solution_1 <- read_excel("explicit_solution.xlsx", sheet = 4,
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

# english scale
myColors_en <- c("#FE0068", "#F60027", "#FDB34B", "#F76B50", "#006D6F", "#6CAE3C") # if it contains customer and fields
names(myColors_en) <- levels(solution_1$name_english)
agents_colors_en <- scale_colour_manual(name = "name_english",values = myColors_en)

# english scale
myColors_es <- c("#FE0068", "#F60027", "#FDB34B", "#F76B50", "#006D6F", "#6CAE3C") # if it contains customer and fields
names(myColors_es) <- levels(solution_1$name_spanish)
agents_colors_es <- scale_colour_manual(name = "name_spanish",values = myColors_es)

# preparing data for plot
demand <- solution_1 %>% filter(name_english %in% c("consumer")) %>% select(day, demand = value)
supply <- solution_1 %>% filter(name_english %in% c("fields")) %>% select(day, supply = value)

with_fields_restriction <- solution_1 %>% 
  filter(name_english %in% c("retail", "wholesale", "regional_warehouse", "factory")) %>% 
  left_join(demand) %>% 
  left_join(supply) %>% 
  ggplot(aes(x = day)) +
  geom_area(aes(y = demand), alpha = 0.25, fill = "#FE0068") +
  geom_area(aes(y = supply), alpha = 0.25, fill = "#6CAE3C")+
  geom_area(aes(y = value), color = "black", size = 0.1)  +
  theme_minimal(base_size = 8)   +
  ggtitle("Demanda de cada agente durante el año, suponiendo falta de almacenes",
          subtitle = "Cuando la oferta (verde) es menor a la demanda (rosa), las politicas toman la forma de la oferta; cuando es mayor, toman la de la demanda") + 
  theme(axis.text.y=element_blank()) +
  xlab("Dia") +
  ylab("Demanda") + guides(color=guide_legend(title="Agente"))  +
  agents_colors_es +
  facet_wrap(~name_spanish, nrow = 4) +
  theme(legend.position="none") #+
  #geom_segment
  # geom_label o geom_text

ggsave("~/Personal/Tesis_Maestria/tesis_tex/figs/analytic_with_fields_restriction.png", with_fields_restriction, device = "png", width = 246.8, height = 102.5, units = "mm")
