import numpy as np

from app.database.queries import save_route

from app.schemas.optimization import OptimizationRequest

from app.optimization.qpso_solver import QPSOSolver

from app.optimization.fitness import (
    calculate_fitness,
    decode_particle
)

from app.services.routing_service import (
    build_road_graph,
    build_distance_matrix,
    build_route_geometry
)

from app.services.traffic_service import (
    build_travel_time_matrix,
    build_traffic_cost_matrix
)


def optimize_routes(request: OptimizationRequest):

    # =========================================================
    # 1. Prepare customers and vehicles
    # =========================================================

    customers = request.customers
    vehicles = request.vehicles

    if not customers:
        raise ValueError(
            "At least one customer is required"
        )

    if not vehicles:
        raise ValueError(
            "At least one vehicle is required"
        )

    customer_demands = [
        customer.demand
        for customer in customers
    ]

    vehicle_capacities = [
        vehicle.capacity
        for vehicle in vehicles
    ]

    earliest_times = [
        customer.earliest
        for customer in customers
    ]

    latest_times = [
        customer.latest
        for customer in customers
    ]

    service_times = [
        customer.service_time
        for customer in customers
    ]

    num_customers = len(customers)
    num_vehicles = len(vehicles)

    # =========================================================
    # 2. Get customer coordinates from FRONTEND
    # =========================================================
    #
    # The frontend sends:
    #
    # {
    #     "node_id": 1,
    #     "latitude": 12.95,
    #     "longitude": 77.59,
    #     ...
    # }
    #
    # Therefore we DO NOT query PostgreSQL for coordinates.
    # This allows the user to select any location on the map.
    # =========================================================

    customer_coordinates = {}

    for customer in customers:

        customer_coordinates[customer.node_id] = {
            "latitude": float(customer.latitude),
            "longitude": float(customer.longitude)
        }

    # =========================================================
    # 3. Depot
    # =========================================================
    #
    # Depot coordinates also come directly from frontend.
    #
    # User selects depot on the map.
    # Frontend sends latitude + longitude.
    # =========================================================

    depot_latitude = float(
        request.depot.latitude
    )

    depot_longitude = float(
        request.depot.longitude
    )

    # =========================================================
    # 4. Build locations
    # =========================================================
    #
    # Matrix:
    #
    # 0 = depot
    # 1 = customer 0
    # 2 = customer 1
    # 3 = customer 2
    # ...
    # =========================================================

    locations = [
        {
            "latitude": depot_latitude,
            "longitude": depot_longitude
        }
    ]

    for customer in customers:

        coordinates = customer_coordinates[
            customer.node_id
        ]

        locations.append(
            {
                "latitude": coordinates["latitude"],
                "longitude": coordinates["longitude"]
            }
        )

    # =========================================================
    # 5. Build road graph
    # =========================================================

    graph = build_road_graph(
        depot_latitude,
        depot_longitude,
        distance=5000
    )

    # =========================================================
    # 6. Build real road distance matrix
    # =========================================================

    distance_matrix = build_distance_matrix(
        graph,
        locations
    )

    # =========================================================
    # 7. Traffic context
    # =========================================================

    traffic_context = {
        "day_of_week": "Monday",
        "hour": 20,
        "is_peak": 1,
        "weather": "Rainy",
        "road_capacity": 1500,
        "vehicles": 1318,
        "speed": 20.64,
        "signal_time": 40
    }

    # =========================================================
    # 8. LightGBM travel-time matrix
    # =========================================================

    travel_time_matrix = build_travel_time_matrix(
        locations,
        distance_matrix,
        traffic_context
    )

    # =========================================================
    # 9. Traffic-cost matrix
    # =========================================================

    traffic_cost_matrix = build_traffic_cost_matrix(
        locations,
        distance_matrix,
        traffic_context
    )

    # =========================================================
    # 10. Convert matrices to NumPy arrays
    # =========================================================

    distance_matrix = np.array(
        distance_matrix,
        dtype=float
    )

    travel_time_matrix = np.array(
        travel_time_matrix,
        dtype=float
    )

    traffic_cost_matrix = np.array(
        traffic_cost_matrix,
        dtype=float
    )

    # =========================================================
    # 11. Fitness function
    # =========================================================

    def fitness_function(particle):

        return calculate_fitness(
            particle,
            distance_matrix,
            travel_time_matrix,
            traffic_cost_matrix,
            customer_demands,
            vehicle_capacities,
            earliest_times,
            latest_times,
            service_times
        )

    # =========================================================
    # 12. Run QPSO
    # =========================================================

    dimensions = (
        num_customers
        + num_customers
    )

    solver = QPSOSolver(
        fitness_function=fitness_function,
        dimensions=dimensions,
        num_particles=30,
        max_iterations=100,
        beta=0.5,
        seed=42
    )

    result = solver.solve()

    best_solution = result[
        "best_solution"
    ]

    best_fitness = result[
        "best_fitness"
    ]

    # =========================================================
    # 13. Decode optimized solution
    # =========================================================

    routes = decode_particle(
        best_solution,
        num_customers=num_customers,
        num_vehicles=num_vehicles
    )

    # =========================================================
    # 14. Build route results
    # =========================================================

    optimized_routes = []

    total_distance = 0.0
    total_time = 0.0
    total_traffic_cost = 0.0
    total_demand = 0.0
    constraint_violations = 0

    for route in routes:

        # -----------------------------------------------------
        # Route metrics
        # -----------------------------------------------------

        route_distance = 0.0
        route_time = 0.0
        route_traffic_cost = 0.0

        previous_node = 0

        for customer_index in route.customers:

            matrix_node = customer_index + 1

            route_distance += distance_matrix[
                previous_node,
                matrix_node
            ]

            route_time += travel_time_matrix[
                previous_node,
                matrix_node
            ]

            route_traffic_cost += traffic_cost_matrix[
                previous_node,
                matrix_node
            ]

            previous_node = matrix_node

        # -----------------------------------------------------
        # Return to depot
        # -----------------------------------------------------

        if route.customers:

            route_distance += distance_matrix[
                previous_node,
                0
            ]

            route_time += travel_time_matrix[
                previous_node,
                0
            ]

            route_traffic_cost += traffic_cost_matrix[
                previous_node,
                0
            ]

        # -----------------------------------------------------
        # Route geometry
        # -----------------------------------------------------


        current_time = 0.0
        prev_node = 0
        for cust_idx in route.customers:
            mat_node = cust_idx + 1
            current_time += travel_time_matrix[prev_node, mat_node]
            if earliest_times[cust_idx] > current_time:
                current_time = earliest_times[cust_idx]
            if current_time > latest_times[cust_idx]:
                constraint_violations += 1
            current_time += service_times[cust_idx]
            prev_node = mat_node

        route_path = build_route_geometry(
            graph,
            locations,
            route.customers
        )

        # -----------------------------------------------------
        # Convert reported route distance from metres to km
        # Keep distance_matrix in metres for the solver and
        # traffic-time calculations.
        # -----------------------------------------------------

        route_distance_km = float(route_distance) / 1000.0

        # -----------------------------------------------------
        # Demand
        # -----------------------------------------------------

        route_demand = sum(
            customer_demands[
                customer_index
            ]
            for customer_index in route.customers
        )

        # -----------------------------------------------------
        # Vehicle capacity
        # -----------------------------------------------------

        vehicle_capacity = vehicle_capacities[
            route.vehicle_id
        ]

        utilization = (
            (route_demand / vehicle_capacity) * 100
            if vehicle_capacity > 0
            else 0.0
        )

        if route_demand > vehicle_capacity:
            constraint_violations += 1

        # -----------------------------------------------------
        # Actual vehicle ID
        # -----------------------------------------------------

        vehicle_id = vehicles[
            route.vehicle_id
        ].vehicle_id

        # -----------------------------------------------------
        # Actual customer IDs
        # -----------------------------------------------------

        customer_sequence = [
            customers[
                customer_index
            ].node_id
            for customer_index in route.customers
        ]

        # -----------------------------------------------------
        # Save route to PostgreSQL
        # -----------------------------------------------------

        route_id = None

        if route.customers:

            route_id = save_route(
                vehicle_id=vehicle_id,
                route_sequence=customer_sequence,
                total_distance=route_distance_km,
                total_time=float(
                    route_time
                ),
                total_traffic_cost=float(
                    route_traffic_cost
                ),
                fitness=float(
                    best_fitness
                )
            )

        # -----------------------------------------------------
        # Frontend route response
        # -----------------------------------------------------

        optimized_routes.append(
            {
                "route_id": route_id,

                "vehicle_id": vehicle_id,

                "customers": customer_sequence,

                "path": route_path,

                "distance": route_distance_km,

                "time": float(
                    route_time
                ),

                "traffic_cost": float(
                    route_traffic_cost
                ),

                "total_demand": float(
                    route_demand
                ),

                "capacity": float(
                    vehicle_capacity
                ),

                "utilization": float(
                    utilization
                )
            }
        )

        # -----------------------------------------------------
        # Overall totals
        # -----------------------------------------------------

        total_distance += route_distance_km
        total_time += route_time
        total_traffic_cost += route_traffic_cost
        total_demand += route_demand

    # =========================================================
    # 15. Dashboard metrics
    # =========================================================

    vehicles_used = sum(
        1
        for route in routes
        if route.customers
    )

    total_capacity_used = sum(
        vehicle_capacities[
            route.vehicle_id
        ]
        for route in routes
        if route.customers
    )

    overall_utilization = (
        (total_demand / total_capacity_used) * 100
        if total_capacity_used > 0
        else 0.0
    )

    # =========================================================
    # 16. Final API response
    # =========================================================

    return {
        "status": "success",

        "message": "Optimization completed",
        "convergence_history": result.get("convergence_history", []),

        "best_fitness": float(
            best_fitness
        ),

        "summary": {

            # Distance is reported in kilometres.
            "distance_unit": "km",

            "total_distance": float(
                total_distance
            ),

            "total_time": float(
                total_time
            ),

            "total_traffic_cost": float(
                total_traffic_cost
            ),

            "total_demand": float(
                total_demand
            ),

            "vehicles_used": vehicles_used,

            "total_vehicles": num_vehicles,

            "overall_utilization": float(
                overall_utilization
            ),
            "constraint_violations": int(constraint_violations),
            "solver_runtime_seconds": float(result.get("solver_runtime_seconds", 0.0))
        },

        "routes": optimized_routes
    }