library("RSQLite")
library(dplyr)
library(ggplot2)
library(openxlsx)
library(choroplethr)
library(choroplethrMaps)
## connect to db
con <- dbConnect(drv = RSQLite::SQLite(), dbname = "clean.sqlite")



steps <- dbGetQuery(conn = con,
                    statement = "SELECT name, steps FROM Countries JOIN Steps on
                    Countries.id = Steps.id ORDER by steps")
dbDisconnect(con)

steps <- steps[steps$steps != 47, ]
steps <- steps %>% rename(region = name, value = steps)
match <- read.xlsx("match.xlsx")
steps$region

for(i in 1:185){
    steps[steps$region==match$from[i] & is.na(steps$region)==FALSE,1] <- match$to[i]
}

plotdata <- steps[complete.cases(steps),]

country_choropleth(plotdata, num_colors = 9) +
        scale_fill_brewer(palette = "YlOrRd") +
        labs(
                title = "Number of handshakes from me to a country",
                subtitle = "VK data, @k",
                caption = "source: Vk.com data by @ksetdekov",
                fill = "Handshakes"
        )
