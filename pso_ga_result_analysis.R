library(dplyr)
setwd("/Users/aytacozkan/works/heuristic.space.maximization/csv/")

ga_fname = "GA/Results/GA_Results_1555372486.csv"
pso_fname = "PSO/Results/PSO_Results_1555431041.csv"

ga_set <- scan(ga_fname, sep = ",", what = numeric(0), quiet = TRUE)
pso_set <- scan(pso_fname, sep = ",", what = numeric(0),quiet = TRUE)


compare_them <- function(ga_data,pso_data) {
  ga_sum <- summary(ga_data) 
  pso_sum <- summary(pso_data) 
  
  t.value1 = (mean(ga_data) - 10) / (sd(ga_data) / sqrt(length(ga_data)))
  p.value1 = dt(t.value1, df=length(ga_data) - 1)
  
  t.value2 = (mean(pso_data) - 10) / (sd(pso_data) / sqrt(length(pso_data)))
  p.value2 = dt(t.value2, df=length(pso_data) - 1)
  
  ga_sum$t.value = t.value1
  ga_sum$p.value = p.value1
  
  pso_sum$t.value = t.value2
  pso_sum$p.value = p.value2
  
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





