import pytest
from fastapi.testclient import TestClient
from app.main import app
import math

client = TestClient(app)

def test_benchmark_aggregation():
    response = client.get("/optimization/benchmark?customer_counts=5&runs=2&particles=10&iterations=10")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    
    results = data["results"]
    assert len(results) == 1
    
    res = results[0]
    assert res["customer_count"] == 5
    assert res["runs"] == 2
    assert "runtime_seconds" in res
    assert "average" in res["runtime_seconds"]
    
    # Check aggregation math
    run_results = res["run_results"]
    assert len(run_results) == 2
    avg_runtime = sum(r["solver_runtime_seconds"] for r in run_results) / len(run_results)
    assert abs(res["runtime_seconds"]["average"] - avg_runtime) < 1e-6
    
    avg_fitness = sum(r["best_fitness"] for r in run_results) / len(run_results)
    assert abs(res["best_fitness"]["average"] - avg_fitness) < 1e-6

def test_benchmark_finite_values():
    response = client.get("/optimization/benchmark?customer_counts=5&runs=1&particles=10&iterations=10")
    assert response.status_code == 200
    data = response.json()
    
    for res in data["results"]:
        assert isinstance(res["customer_count"], int)
        assert isinstance(res["runtime_seconds"]["average"], float)
        assert isinstance(res["best_fitness"]["average"], float)
        assert math.isfinite(res["runtime_seconds"]["average"])
        assert math.isfinite(res["best_fitness"]["average"])
        
        # Check convergence history
        for run in res["run_results"]:
            history = run["convergence_history"]
            assert len(history) > 0
            for val in history:
                assert isinstance(val, float)
                assert math.isfinite(val)
