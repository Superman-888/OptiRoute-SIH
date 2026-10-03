import numpy as np

from app.optimization.qpso_solver import QPSOSolver
from app.optimization.fitness import (
    calculate_fitness,
    decode_particle
)


# --------------------------------------------------
# TEST DATA
# --------------------------------------------------

# Node 0 = Depot
# Node 1 = Customer 0
# Node 2 = Customer 1
# Node 3 = Customer 2
# Node 4 = Customer 3

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


# --------------------------------------------------
# CUSTOMER AND VEHICLE DATA
# --------------------------------------------------

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


# --------------------------------------------------
# FITNESS FUNCTION
# --------------------------------------------------

def fitness_function(particle):

    return calculate_fitness(
        particle,
        distance_matrix,
        travel_time_matrix,
        traffic_cost_matrix,
        customer_demands,
        vehicle_capacities
    )


# --------------------------------------------------
# CREATE QPSO SOLVER
# --------------------------------------------------

solver = QPSOSolver(
    fitness_function=fitness_function,
    dimensions=8,
    num_particles=30,
    max_iterations=100,
    beta=0.5,
    seed=42
)


# --------------------------------------------------
# RUN QPSO
# --------------------------------------------------

result = solver.solve()


# --------------------------------------------------
# DISPLAY BEST PARTICLE
# --------------------------------------------------

print("\n==============================")
print("QPSO OPTIMIZATION RESULT")
print("==============================")

print("\nBest particle:")
print(result["best_solution"])


# --------------------------------------------------
# DISPLAY BEST FITNESS
# --------------------------------------------------

print("\nBest fitness:")
print(result["best_fitness"])


# --------------------------------------------------
# DECODE BEST PARTICLE INTO ROUTES
# --------------------------------------------------

routes = decode_particle(
    result["best_solution"],
    num_customers=len(customer_demands),
    num_vehicles=len(vehicle_capacities)
)


# --------------------------------------------------
# DISPLAY OPTIMIZED ROUTES
# --------------------------------------------------

print("\nOptimized Routes:")
print("------------------------------")

for route in routes:

    print(
        f"Vehicle {route.vehicle_id}: "
        f"Depot -> {route.customers} -> Depot"
    )


# --------------------------------------------------
# DISPLAY ROUTE SUMMARY
# --------------------------------------------------

print("\nRoute Summary:")
print("------------------------------")

for route in routes:

    if len(route.customers) == 0:

        print(
            f"Vehicle {route.vehicle_id}: "
            f"No customers assigned"
        )

    else:

        total_demand = sum(
            customer_demands[customer_id]
            for customer_id in route.customers
        )
        capacity = vehicle_capacities[route.vehicle_id]

        print(
            f"Vehicle {route.vehicle_id}: "
            f"Customers = {route.customers}, "
            f"Demand = {total_demand}, "
            f"Capacity = {capacity}"
        )
        


# --------------------------------------------------
# ROUTE METRICS
# --------------------------------------------------

print("\nRoute Metrics:")
print("-" * 40)

for route in routes:

    total_distance = 0.0

    previous_node = 0

    for customer in route.customers:

        current_node = customer + 1

        total_distance += distance_matrix[
            previous_node,
            current_node
        ]

        previous_node = current_node

    total_distance += distance_matrix[
        previous_node,
        0
    ]

    print(
        f"Vehicle {route.vehicle_id}: "
        f"Distance = {total_distance:.2f} km"
    )


# --------------------------------------------------
# TEST COMPLETE
# --------------------------------------------------

print("\n==============================")
print("TEST COMPLETE")
print("==============================")