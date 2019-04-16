setwd("/Users/aytacozkan/works/heuristic.space.maximization/csv/")

ga_fname = "GA/Results/GA_Results_1555372486.csv"
pso_fname = "PSO/Results/PSO_Results_1555372138.csv"

ga_set <- scan(ga_fname, sep = ",", what = numeric(0), quiet = TRUE)
pso_set <- scan(pso_fname, sep = ",", what = numeric(0),quiet = TRUE)
# ga_set <- read.csv(ga_fname,header = FALSE, sep=",",colClasses = NA, nrows = -1)

str(ga_set)
head(ga_set)

mean(ga_set)
median(ga_set)
summary(ga_set,digits=7,maxsum=7)
max(ga_set)

mean(pso_set)
median(pso_set)
summary(pso_set)
max(pso_set)


library(dplyr)
compare_them <- function(ga_data,pso_data) {
  ga_sum <- summary(ga_data) 
  pso_sum <- summary(pso_data) 
  
  names(ga_sum) <- paste0(names(ga_sum),"1")
  names(pso_sum) <- paste0(names(pso_sum),"2")
  
  final <- cbind(ga_sum,pso_sum)
  
  final1 <- t(final) 
  
  final2 <- final1[order(row.names(final1)), ]
  
  final_1 <- t(final2) %>% data.frame()
  final_1
}
 
compare_them(ga_set,pso_set) %>% View()

polygon = c(c(10,10),c(10,300),c(250,300),c(350,130),c(200,10))

# Student t-Test
t.test(x=polygon, mu=10, conf.level=0.95)

# Manually calculate p-value
t.value = (mean(polygon) - 10) / (sd(polygon) / sqrt(length(polygon)))
p.value = dt(t.value, df=length(polygon) - 1)





