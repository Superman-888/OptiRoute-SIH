
import numpy as np

from app.optimization.qpso_solver import QPSOSolver


def sphere_fitness(particle):
    """Simple sphere function for testing the QPSO solver."""
    return float(np.sum(np.square(particle - 0.5)))


def test_qpso_solver_runs():
    solver = QPSOSolver(
	fitness_function=sphere_fitness,
        dimensions=5,
        num_particles=20,
        max_iterations=50,
        beta=0.5,
        seed=42,
    )

    result = solver.solve()

    assert "best_solution" in result
    assert "best_fitness" in result
    assert np.isfinite(result["best_fitness"])
    assert result["best_solution"].shape == (5,)




