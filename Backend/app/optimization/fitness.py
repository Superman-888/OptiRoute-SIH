import numpy as np

from app.optimization.constraints import (
    calculate_capacity_penalty,
    calculate_time_window_penalty
)

from app.optimization.solution import VehicleRoute


def decode_particle(
    particle,
    num_customers,
    num_vehicles
):
    """
    Decode a QPSO particle into vehicle routes.

    Particle structure:

    [customer_order_values | vehicle_assignment_values]

    First half:
        Determines delivery order.

    Second half:
        Determines which vehicle serves each customer.
    """

    # ---------------------------------------------------------
    # 1. Split particle
    # ---------------------------------------------------------

    order_values = particle[:num_customers]

    vehicle_values = particle[num_customers:]

    # ---------------------------------------------------------
    # 2. Determine customer delivery order
    # ---------------------------------------------------------

    customer_order = np.argsort(order_values)

    # ---------------------------------------------------------
    # 3. Determine vehicle assignment
    # ---------------------------------------------------------

    vehicle_assignment = np.floor(
        vehicle_values * num_vehicles
    ).astype(int)

    vehicle_assignment = np.clip(
        vehicle_assignment,
        0,
        num_vehicles - 1
    )

    # ---------------------------------------------------------
    # 4. Build vehicle routes
    # ---------------------------------------------------------

    routes = []

    for vehicle_id in range(num_vehicles):

        assigned_customers = [
            int(customer_id)
            for customer_id in customer_order
            if vehicle_assignment[customer_id] == vehicle_id
        ]

        routes.append(
            VehicleRoute(
                vehicle_id=vehicle_id,
                customers=assigned_customers
            )
        )

    return routes


def calculate_fitness(
    particle,
    distance_matrix,
    travel_time_matrix,
    traffic_cost_matrix,
    customer_demands,
    vehicle_capacities,
    earliest_times=None,
    latest_times=None,
    service_times=None,
    alpha=1.0,
    beta=1.0,
    gamma=1.0
):
    """
    Calculate the fitness of a QPSO particle.

    Fitness considers:

    1. Total distance
    2. Total travel time
    3. Traffic cost
    4. Vehicle capacity penalty
    5. Time-window penalty
    6. Service time
    """

    num_customers = len(customer_demands)
    num_vehicles = len(vehicle_capacities)

    # ---------------------------------------------------------
    # 1. Decode particle
    # ---------------------------------------------------------

    routes = decode_particle(
        particle,
        num_customers,
        num_vehicles
    )

    # ---------------------------------------------------------
    # 2. Initialize totals
    # ---------------------------------------------------------

    total_distance = 0.0
    total_time = 0.0
    total_traffic_cost = 0.0

    depot = 0

    # ---------------------------------------------------------
    # 3. Evaluate every vehicle route
    # ---------------------------------------------------------

    for route in routes:

        previous_node = depot

        current_time = 0.0

        for customer_id in route.customers:

            # Matrix indexing:
            #
            # 0 = depot
            # 1 = customer 0
            # 2 = customer 1
            # 3 = customer 2
            # ...

            node = customer_id + 1

            # -------------------------------------------------
            # Travel distance
            # -------------------------------------------------

            distance = distance_matrix[
                previous_node,
                node
            ]

            total_distance += distance

            # -------------------------------------------------
            # Travel time
            # -------------------------------------------------

            travel_time = travel_time_matrix[
                previous_node,
                node
            ]

            total_time += travel_time

            current_time += travel_time

            # -------------------------------------------------
            # Traffic cost
            # -------------------------------------------------

            traffic_cost = traffic_cost_matrix[
                previous_node,
                node
            ]

            total_traffic_cost += traffic_cost

            # -------------------------------------------------
            # Time window
            # -------------------------------------------------

            if earliest_times is not None:

                earliest = earliest_times[
                    customer_id
                ]

                # Vehicle waits if it arrives too early
                if current_time < earliest:

                    waiting_time = (
                        earliest - current_time
                    )

                    current_time += waiting_time

                    total_time += waiting_time

            # -------------------------------------------------
            # Service time
            # -------------------------------------------------

            if service_times is not None:

                service_time = service_times[
                    customer_id
                ]

                current_time += service_time

                total_time += service_time

            # Move to current customer
            previous_node = node

        # -----------------------------------------------------
        # Return vehicle to depot
        # -----------------------------------------------------

        if route.customers:

            return_distance = distance_matrix[
                previous_node,
                depot
            ]

            return_time = travel_time_matrix[
                previous_node,
                depot
            ]

            return_traffic_cost = traffic_cost_matrix[
                previous_node,
                depot
            ]

            total_distance += return_distance

            total_time += return_time

            total_traffic_cost += return_traffic_cost

    # ---------------------------------------------------------
    # 4. Capacity penalty
    # ---------------------------------------------------------

    capacity_penalty = calculate_capacity_penalty(
        routes,
        customer_demands,
        vehicle_capacities
    )

    # ---------------------------------------------------------
    # 5. Time-window penalty
    # ---------------------------------------------------------

    time_window_penalty = 0.0

    if (
        earliest_times is not None
        and latest_times is not None
    ):

        time_window_penalty = calculate_time_window_penalty(
            routes,
            travel_time_matrix,
            earliest_times,
            latest_times,
            service_times
        )

    # ---------------------------------------------------------
    # 6. Total penalty
    # ---------------------------------------------------------

    penalty = (
        capacity_penalty
        + time_window_penalty
    )

    # ---------------------------------------------------------
    # 7. Final fitness
    # ---------------------------------------------------------

    fitness = (
        alpha * total_distance
        + beta * total_time
        + gamma * total_traffic_cost
        + penalty
    )

    return float(fitness)