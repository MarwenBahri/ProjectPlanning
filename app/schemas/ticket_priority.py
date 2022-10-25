from enum import auto, Enum

class TicketPriority(str, Enum):
    Normal = auto()
    Urgent = auto()