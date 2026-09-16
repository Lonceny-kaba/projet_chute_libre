# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 12:11:50 2026

@author: lonce
"""
# Projet: chute verticale avec résistance de l'air

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

h0 = 100
v0 = 0
g = 9.81


# Chute dans le vide 

def vide(t, x):
    
    y = x[0]
    v = x[1]
    
    dydt = v
    dvdt = -g
    
    return [dydt, dvdt]

# impact au sol
def sol(t, x):
    return x[0]

sol.terminal = True
sol.direction = -1 

# les conditions initiales

x0 = [h0, v0]
t_span = [0, 10]
t_eval = np.arange(0, 10.1, 0.1)

#Résolution numérique

solution = solve_ivp(vide, t_span,  x0, events=sol, t_eval=t_eval, rtol = 1e-9, atol = 1e-12 )

#Temps et vitesse d'impacts

t_impact = solution.t_events[0][0]
v_impact = solution.y_events[0][0][1]

print("Temps d'impact dans le vide =",t_impact, "s" )
print("vitesse impact dans le vide =", v_impact, "m/s")

#Résulats numériques

t_numerique = solution.t
y_numerique = solution.y[0]
v_numerique = solution.y[1]

#Solutions Analytiques

v_analytique = v0 - g * t_numerique
 
y_analytique = h0 + v0 * t_numerique  - 0.5 * g *  t_numerique **2 

#Comparaisons du résultat numérique  et analytique

#Erreurs absolues

erreur_v = np.abs(v_numerique - v_analytique)
erreur_y = np.abs(y_numerique - y_analytique)

print("Erreur maximale de la vitesse =", np.max(erreur_v))
print("Erreur maximale de la position =", np.max(erreur_y))

#Calculer des erreurs relatives

# On ne veut pas avoir à diviser par 0 

masque_v = np.abs(v_analytique)> 1e-12
masque_y = np.abs(y_analytique)>1e-12

erreur_relative_v = np.abs((v_numerique[masque_v]-v_analytique[masque_v])/v_analytique[masque_v])*100
erreur_relative_y = np.abs((y_numerique[masque_y]-y_analytique[masque_y])/y_analytique[masque_y])*100

print("erreur relative sur les vitesses :", erreur_relative_v)
print("erreur relative sur les positions :", erreur_relative_y)

#Graphe des positions

plt.figure()

plt.plot(t_numerique, y_numerique, label = "Y numérique dans le vide ")
plt.plot(t_numerique, y_analytique, label = "Y  analytique dans le vide ")

plt.xlabel("Temps (s)")
plt.ylabel("Position y (m)")

plt.title(" Positions dans le vide")

plt.legend()
plt.grid()

plt.savefig("Positions_vide.png", dpi = 300, bbox_inches ="tight")

plt.show()

#Graphe des positions
plt.figure()

plt.plot(t_numerique, v_numerique, label = "V numérique dans le vide ")
plt.plot(t_numerique, v_analytique, label = "V analytique dans le vide ")
plt.xlabel("Temps (s)")
plt.ylabel("Vitesse (m/s)")

plt.title("Vitesses dans le vide")

plt.legend()
plt.grid()

plt.savefig("Vitesses_vide.png", dpi = 300, bbox_inches ="tight")

plt.show()

# Le graphique des deux erreurs absolues


plt.figure()

plt.plot(t_numerique, erreur_v, label = "Erreur numérique sur V dans le vide")
plt.plot(t_numerique, erreur_y, label = "Erreur numérique Y dans le vide")
plt.xlabel("Temps (s)")
plt.ylabel("E(t)")

plt.title("Erreurs absolues dans le vide ")
plt.legend()
plt.grid()

plt.savefig("Erreurs_absolues.png", dpi = 300, bbox_inches ="tight")

plt.show()

#CONCLUSION: les résultats numériques et analytiques   sont presques pareils 
#Et  cela  se voit clairement  sur les représentations graphiques qui font d'ailleurs parties du projet.



#Partie2 :Chute avec frottements


m = 0.1
rho = 1.225
Cd = 0.47
A = 0.01

def frottements(t,X):
    y = X[0]
    v = X[1]
    
    dydt = v
    dvdt = - g - (rho * Cd * A)/(2*m )*(v*np.abs(v))
    
    return [dydt,dvdt ]

# Impact au sol

def sol2(t, X):
    return X[0]

sol2.terminal = True
sol2.direction = - 1

#Les conditions initiales

X0 = [h0, v0]
t_span = [0, 10]
t_eval = np.arange(0, 10.1, 0.1)

#Résolution numérique

solution2 = solve_ivp(frottements, t_span,  X0, events=sol2, t_eval=t_eval, rtol = 1e-9, atol = 1e-12 )

# Temps et vitesse au point d'impact


t_impact_2 = solution2.t_events[0][0]

v_impact_2 = solution2.y_events[0][0][1]

print("Temps d'impact avec frottements =", t_impact_2, "s")
print("Vitesse d'impact avec frottements =", v_impact_2, "m/s")

# Résulats numériques avec frottements
t_numerique_2 = solution2.t
v_numerique_2 = solution2.y[1]
y_numerique_2 = solution2.y[0]

#Vitesse limite Théorique

Vlim = np.sqrt((2*m*g)/(rho * Cd* A))

print("Vitesse limite pour la m1= 0.10 :",Vlim, "m/s" )

#Graphe numérique (Position et Vitesse) 

plt.figure()

plt.plot(t_numerique_2, y_numerique_2, label = "Y numérique avec frottements")
plt.xlabel("Temps (s)")
plt.ylabel("Position y (m)")

plt.title("Positions avec frottements")

plt.grid()
plt.legend()

plt.savefig("Position_frottements.png",dpi = 300, bbox_inches ="tight")

plt.show()

plt.figure()

plt.plot(t_numerique_2, v_numerique_2, label = "V numérique avec frottements")
plt.axhline(-Vlim,color = "red", linestyle = "--", label = "Vitesse limite théorique")
plt.xlabel("Temps (s)")
plt.ylabel("vitesse V (m/s)")

plt.title("Les vitesses ")

plt.grid()
plt.legend()

plt.savefig("Vitesses_frottements.png", dpi = 300, bbox_inches ="tight")

plt.show()

# Comparaison des résultats avec ceux de la chute dans le vide

# Temps d'impact = 4.515236409857306 s
# vitesse impact = -44.294469180700176 m/s

#Temps d'impact avec frottements = 6.7199543410617295 s
#Vitesse d'impact avec frottements = -18.430854658407075 m/s

#Dans le vide le  système va plus vite donc mets moins de temps contrairement à s'il y'a frottement de l'air
# où il va moins vite et mets plus de temps.

#Partie 3: Calcul de la vitesse limite théorique


#la vitisse limite théorique = - 18.460035344133107 m/s

# On remarque bien graphiquement que la vitesse numérique se rapproche de -18.4... or la vitisse limite = - 18.460035344133107 m/s
#par conséquent elle se rapproche bel et bien à sa vitesse limite.




#Partie 4: Etude paramétrrique

m1 = 0.05
m2 = 0.10
m3 = 0.5
rho = 1.225
Cd = 0.47
A = 0.01

def frottements(t,X, m ):
    y = X[0]
    v = X[1]
    
    
    
    dydt = v
    dvdt = - g - (rho * Cd * A)/(2*m) *(v*np.abs(v))
    
    
    return [dydt,dvdt ]
# Impact au sol

def sol2(t, X, m):
    return X[0]

sol2.terminal = True
sol2.direction = - 1

#Les conditions initiales

X0 = [h0, v0]
t_span = [0, 10]
t_eval = np.arange(0, 10.1, 0.1)

solution_m1= solve_ivp(frottements, t_span,  X0,args=(m1,), events=sol2, t_eval=t_eval, rtol = 1e-9, atol = 1e-12 )
solution_m2= solve_ivp(frottements, t_span,  X0,args=(m2,), events=sol2, t_eval=t_eval, rtol = 1e-9, atol = 1e-12 )
solution_m3= solve_ivp(frottements, t_span,  X0,args=(m3,), events=sol2, t_eval=t_eval, rtol = 1e-9, atol = 1e-12 )


v_m1 = solution_m1.y[1]
v_m2 = solution_m2.y[1]
v_m3 = solution_m3.y[1]

v1 = solution_m1.y_events[0][0][1]
v2 = solution_m2.y_events[0][0][1]
v3 = solution_m3.y_events[0][0][1]

t1 = solution_m1.t_events[0][0]
t2 = solution_m2.t_events[0][0]
t3 = solution_m3.t_events[0][0]

Vlim = np.sqrt((2*m*g)/(rho * Cd* A))


print("temps avec m1 =", t1, "s")
print("temps avec m2 =", t2, "s")
print("temps avec m3 =", t3, "s")
print("vitesse avec m1 =",v1, "m/s" )
print("vitesse avec m2 =",v2, "m/s" )
print("vitesse avec m3 =",v3, "m/s"  )

plt.plot(solution_m1.t,v_m1 , label = "Vitesse pour m = 0.05 kg")

plt.plot(solution_m2.t,v_m2 , label = "Vitesse pour m = 0.10 kg")

plt.plot(solution_m3.t,v_m3 , label = "Vitesse pour m = 0.5 kg")

plt.axhline(-Vlim, color = "blue", linestyle = "--", label = "Vitesse théorique")

plt.xlabel("Temps (s)")

plt.ylabel("vitesse v (m/s)")

plt.title("Graphique avec les différentes masses")


plt.grid()
plt.legend()

plt.savefig("Vitesses_des_masses.png", dpi = 300, bbox_inches ="tight")

plt.show()

#Influence de masse sur le système: Plus la masse est grande plus le système descend vite, car sa vitesse est plus grande en valeur absolue
#Logiquement il met moins de temps pour descendre. 


#Difficultés rencontrées: j'ai vraiment du mal de montrer graphiquement que la vitesse numérique 
#se rapproche de la vitesse limite et de représenter gahiquement les vitesses des trois masses.




    
    
    








