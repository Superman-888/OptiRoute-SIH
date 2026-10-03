import time

import numpy as np


class QPSOSolver:

    def __init__(
        self,
        fitness_function,
        dimensions,
        num_particles=30,
        max_iterations=100,
        beta=0.5,
        seed=None
    ):
        self.fitness_function = fitness_function
        self.dimensions = dimensions
        self.num_particles = num_particles
        self.max_iterations = max_iterations
        self.beta = beta

        if seed is not None:
            np.random.seed(seed)

    def initialize_particles(self):
        """
        Create the initial particle population.
        """

        particles = np.random.rand(
            self.num_particles,
            self.dimensions
        )

        return particles

    def solve(self):
        """
        Run QPSO and record measured runtime and convergence history.
        """
        solver_start = time.perf_counter()

        particles = self.initialize_particles()

        personal_best = particles.copy()
        personal_best_fitness = np.array([
            self.fitness_function(particle)
            for particle in personal_best
        ])

        best_index = np.argmin(personal_best_fitness)

        global_best = personal_best[best_index].copy()
        global_best_fitness = personal_best_fitness[best_index]
        convergence_history = [float(global_best_fitness)]

        for iteration in range(self.max_iterations):
            mean_best = np.mean(personal_best, axis=0)

            for i in range(self.num_particles):
                u = np.random.rand(self.dimensions)
                phi = np.random.rand(self.dimensions)

                attractor = (
                    phi * personal_best[i]
                    + (1 - phi) * global_best
                )

                sign = np.where(u < 0.5, -1, 1)

                particle = attractor + (
                    sign
                    * self.beta
                    * np.abs(mean_best - particles[i])
                    * np.log(1 / np.maximum(u, 1e-10))
                )

                particle = np.clip(particle, 0.0, 1.0)
                particles[i] = particle

                fitness = self.fitness_function(particle)

                if fitness < personal_best_fitness[i]:
                    personal_best[i] = particle.copy()
                    personal_best_fitness[i] = fitness

                    if fitness < global_best_fitness:
                        global_best = particle.copy()
                        global_best_fitness = fitness

            convergence_history.append(float(global_best_fitness))

        solver_runtime_seconds = time.perf_counter() - solver_start

        return {
            "best_solution": global_best,
            "best_fitness": float(global_best_fitness),
            "solver_runtime_seconds": float(solver_runtime_seconds),
            "iterations_completed": self.max_iterations,
            "num_particles": self.num_particles,
            "convergence_history": convergence_history,
        }
