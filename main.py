from simulator.workload import generate_fake_requests
from simulator.engine import SimulatorEngine


def main():
    requests = generate_fake_requests(num_requests=20, seed=42)

    print("Generated Requests:")
    for r in requests:
        print(
            f"Request {r.request_id}: "
            f"arrival={r.arrival_time}, "
            f"prompt_len={r.prompt_length}, "
            f"max_new_tokens={r.max_new_tokens}"
        )

    print("\nStarting simulation...\n")

    engine = SimulatorEngine(requests=requests, max_batch_size=4)
    results = engine.run()

    print("\nSimulation Complete.\n")
    print("Results:")
    for key, value in results.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()