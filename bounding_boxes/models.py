from dataclasses import dataclass


@dataclass
class DetectedObject:
    top_left: tuple[int, int]
    bottom_right: tuple[int, int]
    class_name: str
    confidence: float

    @property
    def width(self) -> int:
        return self.bottom_right[0] - self.top_left[0]

    @property
    def height(self) -> int:
        return self.bottom_right[1] - self.top_left[1]

    @property
    def center(self) -> tuple[int, int]:
        cx = (self.top_left[0] + self.bottom_right[0]) // 2
        cy = (self.top_left[1] + self.bottom_right[1]) // 2
        return (cx, cy)
