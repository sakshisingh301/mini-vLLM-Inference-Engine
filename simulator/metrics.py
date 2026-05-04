class MetricsCollector:
    def __init__(self):
        self.total_generated_tokens = 0
        self.completed_requests = 0
        self.latencies = []
        self.wait_times = []

        self.memory_usage_over_time = []
        self.memory_utilization_over_time = []
        self.peak_memory_pages = 0

    def record_token_generated(self, num_tokens: int = 1):
        self.total_generated_tokens += num_tokens

    def record_request_completed(self, request):
        self.completed_requests += 1

        latency = request.finish_time - request.arrival_time
        wait_time = request.start_time - request.arrival_time

        self.latencies.append(latency)
        self.wait_times.append(wait_time)

    def record_memory(self, used_pages: int, utilization: float):
        self.memory_usage_over_time.append(used_pages)
        self.memory_utilization_over_time.append(utilization)
        self.peak_memory_pages = max(self.peak_memory_pages, used_pages)

    def summary(self, total_time: int, allocation_failures: int = 0) -> dict:
        avg_latency = sum(self.latencies) / len(self.latencies) if self.latencies else 0
        avg_wait = sum(self.wait_times) / len(self.wait_times) if self.wait_times else 0
        throughput = self.total_generated_tokens / total_time if total_time > 0 else 0

        avg_memory_util = (
            sum(self.memory_utilization_over_time) / len(self.memory_utilization_over_time)
            if self.memory_utilization_over_time
            else 0
        )

        return {
            "completed_requests": self.completed_requests,
            "total_generated_tokens": self.total_generated_tokens,
            "average_latency": round(avg_latency, 2),
            "average_wait_time": round(avg_wait, 2),
            "throughput_tokens_per_tick": round(throughput, 2),
            "peak_memory_pages": self.peak_memory_pages,
            "average_memory_utilization_percent": round(avg_memory_util * 100, 2),
            "allocation_failures": allocation_failures,
        }