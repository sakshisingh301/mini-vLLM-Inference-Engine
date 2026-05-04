from simulator.workload import generate_fake_requests
from simulator.engine import SimulatorEngine


if __name__ == "__main__":
    requests = generate_fake_requests(num_requests=20)

    engine = SimulatorEngine(
        requests=requests,
        max_batch_size=4,
        total_pages=256
    )

    summary = engine.run()

    print("\nSimulation Summary")
    print(summary)