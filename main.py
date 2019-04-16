from impl.ga_impl import GA
from impl.pso_impl import PSO

Nb_Cycles = 100
Nb_Indiv = 20
polygon = ((10, 10), (10, 300), (250, 300), (350, 130), (200, 10))
w = 0.9
ro_max = 1

pso = PSO(polygon=polygon, nb_Cycles=Nb_Cycles, nb_Indiv=Nb_Indiv, w=w, ro_max=ro_max)

# PSO Algorithm
# rgb(245,245,220)#
# rgb(220,20,60)
print(pso.__exec__())
# print(pso.__isvalid__(polygon=polygon))
print(pso.__draw__(name="PSO", polygon=polygon, color=(255, 250, 250), clname="Blue"))
print(pso.__csv__(name="PSO"))

# GA Algorithm
# rgb(250,235,215)
# rgb(0,191,255)
# ga = GA(polygon=polygon, nb_Cycles=Nb_Cycles, nb_Indiv=Nb_Indiv, w=w, ro_max=ro_max)

# print(ga.__exec__())
# print(ga.__draw__(name="GA", polygon=polygon, color=(255, 250, 250), clname="White"))
# print(ga.__csv__(name="GA"))
