def calculate_capacity_penalty(
    routes,
    customer_demands,
    vehicle_capacities
):
    penalty = 0.0

    for route in routes:

        vehicle_id = route.vehicle_id

        capacity = vehicle_capacities[
            vehicle_id
        ]

        total_demand = sum(
            customer_demands[customer_id]
            for customer_id in route.customers
        )

        if total_demand > capacity:

            excess = (
                total_demand - capacity
            )

            penalty += excess * 1000.0

    return penalty


def calculate_time_window_penalty(
    routes,
    travel_time_matrix,
    earliest_times,
    latest_times,
    service_times=None
):
    penalty = 0.0

    depot = 0

    for route in routes:

        previous_node = depot

        current_time = 0.0

        for customer_id in route.customers:

            node = customer_id + 1

            # Travel to customer
            current_time += travel_time_matrix[
                previous_node,
                node
            ]

            # Late arrival penalty
            if current_time > latest_times[customer_id]:

                lateness = (
                    current_time
                    - latest_times[customer_id]
                )

                penalty += lateness * 1000.0

            # Wait if arriving early
            if current_time < earliest_times[customer_id]:

                current_time = earliest_times[
                    customer_id
                ]

            # Service
            if service_times is not None:

                current_time += service_times[
                    customer_id
                ]

            previous_node = node

    return penalty