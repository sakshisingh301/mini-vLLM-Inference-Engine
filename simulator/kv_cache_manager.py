class KVCacheManager:
    def __init__(self, total_pages: int):
        self.total_pages = total_pages
        self.free_pages = set(range(total_pages))
        self.page_table = {}  # request_id -> list[page_id]
        self.allocation_failures = 0

    def allocate(self, request_id: int, num_pages: int) -> bool:
        if num_pages <= 0:
            return True

        if len(self.free_pages) < num_pages:
            self.allocation_failures += 1
            return False

        allocated = []
        for _ in range(num_pages):
            allocated.append(self.free_pages.pop())

        self.page_table.setdefault(request_id, []).extend(allocated)
        return True

    def free(self, request_id: int):
        pages = self.page_table.pop(request_id, [])
        self.free_pages.update(pages)

    def used_pages(self) -> int:
        return self.total_pages - len(self.free_pages)

    def free_page_count(self) -> int:
        return len(self.free_pages)

    def utilization(self) -> float:
        return self.used_pages() / self.total_pages if self.total_pages > 0 else 0.0

    def pages_owned_by(self, request_id: int) -> int:
        return len(self.page_table.get(request_id, []))