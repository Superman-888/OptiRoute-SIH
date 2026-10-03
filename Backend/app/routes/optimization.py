from fastapi import APIRouter, HTTPException, Query
import numpy as np

from app.schemas.optimization import OptimizationRequest
from app.services.qpso_service import optimize_routes
from app.optimization.qpso_solver import QPSOSolver
from app.optimization.fitness import calculate_fitness


router = APIRouter()


@router.post("/optimization")
def optimization(request: OptimizationRequest):
    try:
        return optimize_routes(request)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Optimization failed: {str(error)}",
        )


@router.get("/optimization/benchmark")
def optimization_benchmark(
    customer_counts: str = Query(
        default="5,10,20",
        description="Comma-separated synthetic customer counts, e.g. 5,10,20",
    ),
    runs: int = Query(default=3, ge=1, le=10),
    particles: int = Query(default=30, ge=5, le=100),
    iterations: int = Query(default=100, ge=1, le=500),
):
    """
    Measure QPSO on deterministic synthetic VRP matrices.
    These are solver-only benchmarks, not real-road-network benchmarks.
    """
    try:
        sizes = [int(value.strip()) for value in customer_counts.split(",")]
        if not sizes or any(size < 2 or size > 100 for size in sizes):
            raise ValueError("Customer counts must be between 2 and 100.")
        if len(sizes) > 6:
            raise ValueError("Use at most 6 customer counts per request.")

        results = []

        for customer_count in sizes:
            # Fixed seed makes the synthetic instance reproducible.
            rng = np.random.default_rng(1000 + customer_count)
            node_count = customer_count + 1  # depot + customers

            raw = rng.uniform(1000.0, 15000.0, size=(node_count, node_count))
            distance_matrix = (raw + raw.T) / 2.0
            np.fill_diagonal(distance_matrix, 0.0)

            travel_time_matrix = distance_matrix / 8.33  # approx. 30 km/h, seconds
            traffic_cost_matrix = distance_matrix * 0.02

            demands = rng.integers(5, 21, size=customer_count).astype(float).tolist()
            vehicle_count = max(2, int(np.ceil(customer_count / 5)))
            capacities = [100.0] * vehicle_count
            earliest_times = [0.0] * customer_count
            latest_times = [1_000_000.0] * customer_count
            service_times = [0.0] * customer_count

            run_results = []

            for run_index in range(runs):
                def fitness_function(particle):
                    return calculate_fitness(
                        particle,
                        distance_matrix,
                        travel_time_matrix,
                        traffic_cost_matrix,
                        demands,
                        capacities,
                        earliest_times,
                        latest_times,
                        service_times,
                    )

                solver = QPSOSolver(
                    fitness_function=fitness_function,
                    dimensions=customer_count * 2,
                    num_particles=particles,
                    max_iterations=iterations,
                    beta=0.5,
                    seed=42 + run_index,
                )
                result = solver.solve()
                run_results.append({
                    "run": run_index + 1,
                    "solver_runtime_seconds": result["solver_runtime_seconds"],
                    "best_fitness": result["best_fitness"],
                    "iterations_completed": result["iterations_completed"],
                    "convergence_history": result["convergence_history"],
                })

            runtimes = [item["solver_runtime_seconds"] for item in run_results]
            fitness_values = [item["best_fitness"] for item in run_results]

            results.append({
                "customer_count": customer_count,
                "vehicle_count": vehicle_count,
                "runs": runs,
                "particles": particles,
                "iterations": iterations,
                "runtime_seconds": {
                    "average": float(np.mean(runtimes)),
                    "min": float(np.min(runtimes)),
                    "max": float(np.max(runtimes)),
                },
                "best_fitness": {
                    "average": float(np.mean(fitness_values)),
                    "min": float(np.min(fitness_values)),
                    "max": float(np.max(fitness_values)),
                },
                "run_results": run_results,
            })

        return {
            "status": "success",
            "benchmark_type": "synthetic_solver_only",
            "note": (
                "Measurements cover QPSO solver execution on deterministic synthetic "
                "matrices only. They exclude road-graph/matrix preparation, database "
                "writes, and real road-network routing. Fitness is an objective score, "
                "not kilometres or deviation from an optimal solution."
            ),
            "configuration": {
                "runs_per_size": runs,
                "particles": particles,
                "iterations": iterations,
            },
            "results": results,
        }

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Benchmark failed: {str(error)}",
        )
