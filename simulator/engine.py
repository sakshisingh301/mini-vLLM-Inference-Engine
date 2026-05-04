from collections import deque
from simulator.metrics import MetricsCollector
from simulator.kv_cache_manager import KVCacheManager


class SimulatorEngine:
    def __init__(self, requests, max_batch_size: int = 4, total_pages: int = 256):
        self.future_requests = deque(sorted(requests, key=lambda r: r.arrival_time))
        self.waiting_queue = deque()
        self.active_requests = []
        self.finished_requests = []

        self.time = 0
        self.max_batch_size = max_batch_size
        self.metrics = MetricsCollector()

        self.kv_manager = KVCacheManager(total_pages=total_pages)

    def move_arrived_requests_to_queue(self):
        while self.future_requests and self.future_requests[0].arrival_time <= self.time:
            req = self.future_requests.popleft()
            req.status = "waiting"
            self.waiting_queue.append(req)

    def admit_requests(self):
        while len(self.active_requests) < self.max_batch_size and self.waiting_queue:
            req = self.waiting_queue[0]

            # Option A: 1 prompt token = 1 page
            success = self.kv_manager.allocate(
                request_id=req.request_id,
                num_pages=req.prompt_length
            )

            if not success:
                # Not enough memory. Stop admitting for this tick.
                break

            self.waiting_queue.popleft()
            req.status = "active"
            req.start_time = self.time
            self.active_requests.append(req)

    def decode_step(self):
        finished_now = []

        for req in list(self.active_requests):
            # Option A: every generated token needs 1 new page
            success = self.kv_manager.allocate(
                request_id=req.request_id,
                num_pages=1
            )

            if not success:
                # Milestone 2 behavior: request stalls if memory is full.
                # Later Milestone 5 will add eviction.
                continue

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

            # Free all KV cache pages for this request
            self.kv_manager.free(req.request_id)

    def record_memory_metrics(self):
        self.metrics.record_memory(
            used_pages=self.kv_manager.used_pages(),
            utilization=self.kv_manager.utilization()
        )

    def run(self):
        while self.future_requests or self.waiting_queue or self.active_requests:
            self.move_arrived_requests_to_queue()
            self.admit_requests()

            print(
                f"[time={self.time}] "
                f"waiting={len(self.waiting_queue)} "
                f"active={[r.request_id for r in self.active_requests]} "
                f"finished={len(self.finished_requests)} "
                f"used_pages={self.kv_manager.used_pages()} "
                f"free_pages={self.kv_manager.free_page_count()}"
            )

            self.decode_step()
            self.record_memory_metrics()
            self.time += 1

        return self.metrics.summary(
            total_time=self.time,
            allocation_failures=self.kv_manager.allocation_failures
        )