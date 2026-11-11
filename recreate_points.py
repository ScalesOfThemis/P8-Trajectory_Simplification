import numpy as np
import matplotlib.pyplot as plt


def recreate_points(polynomials) :

    points = [[],[],[]]

    lons = polynomials[0]
    lats = polynomials[1]
    times = polynomials[2]


    if not (len(lons) == len(lats) == len(times)) :
        print('Error: Unequal number of polynomials')
        return points


    for i in range(len(times)) :
        step_length = 2
        time = np.arange(start=times[i][0],stop=times[i][1]+step_length,step=step_length).tolist()
        for t in time :
            points[0].append(evaluate_polynomial(lons[i],t))
            points[1].append(evaluate_polynomial(lats[i],t))
            points[2].append(t)
    return points
            

def evaluate_polynomial(coefficients, time) :
    total = 0
    for i in range(len(coefficients)) :
        total += coefficients[i]*time**i
    return total


lons = [[0, 1, 0.5],[-5,6.5]]
lats = [[2,1],[92,2,-1]]
times = [[0,10],[10,20]]

piecewise_polynomial = [lons, lats, times]

recreated_points = recreate_points(piecewise_polynomial)

print(recreated_points)

plt.figure()
plt.plot(recreated_points[0],recreated_points[1])
plt.show()
