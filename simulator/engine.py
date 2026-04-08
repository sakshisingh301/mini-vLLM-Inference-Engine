from collections import deque
from simulator.metrics import MetricsCollector


class SimulatorEngine:
    def __init__(self, requests, max_batch_size: int = 4):
        self.future_requests = sorted(requests, key=lambda r: r.arrival_time)
        self.waiting_queue = deque()
        self.active_requests = []
        self.finished_requests = []

        self.time = 0
        self.max_batch_size = max_batch_size
        self.metrics = MetricsCollector()

    def move_arrived_requests_to_queue(self):
        while self.future_requests and self.future_requests[0].arrival_time <= self.time:
            req = self.future_requests.pop(0)
            self.waiting_queue.append(req)

    def admit_requests(self):
        while len(self.active_requests) < self.max_batch_size and self.waiting_queue:
            req = self.waiting_queue.popleft()
            req.status = "active"
            req.start_time = self.time
            self.active_requests.append(req)

    def decode_step(self):
        finished_now = []

        for req in self.active_requests:
            req.generated_tokens += 1
            self.metrics.record_token_generated(1)

            if req.is_finished():
                req.status = "finished"
                req.finish_time = self.time + 1
                finished_now.append(req)

        for req in finished_now:
            self.active_requests.remove(req)
            self.finished_requests.append(req)
            self.metrics.record_request_completed(req)

    def run(self):
        while self.future_requests or self.waiting_queue or self.active_requests:
            self.move_arrived_requests_to_queue()
            self.admit_requests()

            print(
                f"[time={self.time}] "
                f"waiting={len(self.waiting_queue)} "
                f"active={[r.request_id for r in self.active_requests]} "
                f"finished={len(self.finished_requests)}"
            )

            self.decode_step()
            self.time += 1

        return self.metrics.summary(self.time)