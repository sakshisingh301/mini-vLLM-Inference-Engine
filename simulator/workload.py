import random
from simulator.models import Request


def generate_fake_requests(num_requests: int, seed: int = 42) -> list[Request]:
    random.seed(seed)
    requests = []

    current_time = 0
    for i in range(num_requests):
        arrival_gap = random.randint(0, 3)
        current_time += arrival_gap

        prompt_length = random.randint(10, 100)
        max_new_tokens = random.randint(20, 80)

        req = Request(
            request_id=i,
            arrival_time=current_time,
            prompt_length=prompt_length,
            max_new_tokens=max_new_tokens,
        )
        requests.append(req)

    return requests