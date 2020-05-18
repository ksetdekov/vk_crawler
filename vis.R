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
plotdata$value <- as.factor(plotdata$value)
png('img/handshakes.png', width = 1280, height = 720, units = "px", pointsize = 18, antialias = "cleartype")
country_choropleth(plotdata, num_colors = 9) +
        scale_fill_brewer(palette = "RdBu") +
        labs(
                title = "Number of handshakes from me to a native",
                subtitle = "person is native if most friends are from same country",
                caption = "source: public Vk.com data by @ksetdekov",
                fill = "Handshakes"
        )
dev.off()
