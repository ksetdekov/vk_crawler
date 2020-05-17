

data(gapminder, package = "gapminder")


library("RSQLite")
library(dplyr)
library(ggplot2)
## connect to db
con <- dbConnect(drv = RSQLite::SQLite(), dbname = "clean.sqlite")



steps <- dbGetQuery(conn = con,
                    statement = "SELECT name, steps FROM Countries JOIN Steps on
                    Countries.id = Steps.id ORDER by steps")
dbDisconnect(con)

steps <- steps[steps$steps != 47, ]
steps <- steps %>% rename(region = name, value = steps)
library(openxlsx)
match <- read.xlsx("match.xlsx")
steps$region

for(i in seq_along(match$from)) steps$region <- gsub(match$from[i], match$to[i], steps$region, fixed = TRUE)
steps <- steps[complete.cases(steps),]

plotdata <- steps[,]
library(choroplethr)
country_choropleth(plotdata, num_colors = 9) +
        scale_fill_brewer(palette = "YlOrRd") +
        labs(
                title = "Number of handshakes from me to a country",
                subtitle = "VK data, @k",
                caption = "source: Vk.com data by @ksetdekov",
                fill = "Handshakes"
        )
