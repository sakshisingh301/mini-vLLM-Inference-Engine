from dataclasses import dataclass
from typing import Optional


@dataclass
class Request:
    request_id: int
    arrival_time: int
    prompt_length: int
    max_new_tokens: int

    generated_tokens: int = 0
    status: str = "waiting"
    start_time: Optional[int] = None
    finish_time: Optional[int] = None

    def is_finished(self) -> bool:
        return self.generated_tokens >= self.max_new_tokens