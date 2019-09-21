# This Script takes the consolidated table with harvest seasons
#"1. Creates a decent csv that can be read directly as fields trend

# Reading files ##############################################################
fields_no_noise <- read_excel("../../aux_documents/creating_fields_trend.xlsx", sheet = 2,
                               skip = 0)
all_harvests <- list()

# This function creates a vector 
get_harvest<- function(row){
  harvest_dates <- seq(as.Date(fields_no_noise$begin_date[row]), 
                      as.Date(fields_no_noise$end_date[row]), "days")
  active_dates <- seq(as.Date(fields_no_noise$begin_date_active[row]), 
                       as.Date(fields_no_noise$end_date_active[row]), "days")
  
  # We're gonna assume that an "active" day yields twice as a regular day.
  # So baseline: 1 "unit" every regular day
  regular_harvest <- data.frame(Date = harvest_dates,
                                basic_harvest = rep(1, length(harvest_dates)))
  active_harvest <- data.frame(Date = active_dates,
                               active_harvest = rep(1, length(active_dates)))
  
  harvest <- regular_harvest %>% left_join(active_harvest)  %>% 
    mutate(active_harvest= ifelse(is.na(active_harvest), 0, active_harvest),
           total_harvest = basic_harvest + active_harvest,
           harvest_proportion = total_harvest/sum(total_harvest),
           harvest = harvest_proportion*fields_no_noise$harvest[row]) %>%
           select(Date,harvest) 
}

for(i in 1:nrow(fields_no_noise)){
all_harvests[[i]] <- get_harvest(i)
}


fields_no_noise <- do.call("rbind", all_harvests) %>%
  filter(is.na(harvest) == FALSE) %>%
  group_by(Date) %>%
  summarise(total_harvest = sum(harvest)) %>%
  ungroup

# csv should have Month, Day, Supply fields

one_year <- data.frame(Date = seq(as.Date('2013-01-01'),as.Date('2013-12-31'), "days"))

fields_no_noise_for_csv <- one_year %>% left_join(fields_no_noise) %>%
  mutate(Supply= as.numeric(ifelse(is.na(total_harvest), 0, total_harvest)),
         Month = substr(Date, 6,7),
         Month = factor(Month,
            levels = c("01", "02", "03", "04", "05", "06",
                       "07", "08", "09", "10", "11", "12"),
            labels = c("January", "February", "March",
                       "April", "May", "June", "July",
                       "August", "September", "October",
                       "November", "December" )),
         Month = as.character(Month),
         Day = substr(Date, 9,10)) %>%
  select(Month, Day, Supply)


# Plots: Supply ##############################################################
supply_no_noise <- read_csv("../../aux_documents/fields_trend.csv") %>% 
  mutate(Month = factor(Month, levels = c("January", "February", "March",
                                          "April", "May", "June", "July",
                                          "August", "September", "October",
                                          "November", "December" )),
         Mes = fct_recode(Month,
                          "Enero" = "January",
                          "Febrero" = "February",
                          "Marzo" = "March",
                          "Abril" = "April",
                          "Mayo" = "May",
                          "Junio" = "June",
                          "Julio" = "July",
                          "Agosto" = "August",
                          "Septiembre" = "September",
                          "Octubre" = "October",
                          "Noviembre" = "November",
                          "Diciembre" = "December"),
         Day = as.numeric(Day))

all_months_supply <- ggplot(supply_no_noise, aes(x = Day, y = Supply, color = Supply)) + 
  geom_line(size=1) +
  #facet_wrap( ~ Month_a) +
  facet_wrap( ~Mes, ncol=3) +
  guides(color = "none") +
  scale_colour_continuous(low = "darkgrey", high = "firebrick4") +
  scale_y_continuous(limits = c(1, 70)) +
  theme(panel.background = element_rect(fill = "gray95")) + 
  #labs(x = "Day", y = "Demand") +
  #ggtitle("Yearly Beer Demand") +
  labs(x = "Dia", y = "Produccion") +
  # Customer Demand - weekly trend with a peak on Independence Day and increased demand on Christmas Holidays
  #ggtitle("Oferta Anual de los Campos de Cebada", 
  #        subtitle = "Solamente hay producci?n durante el verano, con un pico peque?o al final de junio y uno grande en agosto") +
  theme_minimal(base_size = 8)

ggsave("../../tesis_tex/figs/fields_monthly_supply_ggplot.png", all_months_supply, device = "png")

# Anything below this line is not part of the code, erase if present

#write.csv(fields_no_noise_for_csv, "fields_trend.csv", row.names = FALSE)

