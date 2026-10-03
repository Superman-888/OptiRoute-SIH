import numpy as np

from app.optimization.fitness import calculate_fitness


distance_matrix = np.array([
    [0, 5, 8, 6, 7],
    [5, 0, 4, 7, 3],
    [8, 4, 0, 3, 6],
    [6, 7, 3, 0, 4],
    [7, 3, 6, 4, 0]
], dtype=float)


travel_time_matrix = np.array([
    [0, 10, 16, 12, 14],
    [10, 0, 8, 14, 6],
    [16, 8, 0, 6, 12],
    [12, 14, 6, 0, 8],
    [14, 6, 12, 8, 0]
], dtype=float)


traffic_cost_matrix = np.array([
    [0, 2, 4, 3, 2],
    [2, 0, 2, 4, 1],
    [4, 2, 0, 1, 3],
    [3, 4, 1, 0, 2],
    [2, 1, 3, 2, 0]
], dtype=float)


customer_demands = [
    20,
    30,
    10,
    25
]


vehicle_capacities = [
    50,
    50
]


particle = np.array([
    0.70,
    0.10,
    0.90,
    0.30,
    0.10,
    0.80,
    0.20,
    0.70
])


fitness = calculate_fitness(
    particle,
    distance_matrix,
    travel_time_matrix,
    traffic_cost_matrix,
    customer_demands,
    vehicle_capacities
)


print("VRP fitness:", fitness)