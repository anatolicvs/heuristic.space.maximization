setwd("/Users/aytacozkan/works/heuristic.space.maximization/csv/")

ga_fname = "GA/Results/GA_Results_1555309458.csv"
pso_fname = "PSO/Results/PSO_Results_1555309173.csv"

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
compare_them <- function(data1,data2) {
  sum1 <- apply(data1,2,summary) %>% data.frame() 
  sum2 <- apply(data2,2,summary) %>% data.frame() 
  
  names(sum1) <- paste0(names(sum1),"1")
  names(sum2) <- paste0(names(sum2),"2")
  
  final <- cbind(sum1,sum2)
  
  final1 <- t(final) 
  
  final2 <- final1[order(row.names(final1)), ]
  
  final_1 <- t(final2) %>% data.frame()
  final_1
}

compare_them(ga_set,pso_set*2) %>% View()





