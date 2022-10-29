from enum import auto, Enum

class TicketPriority(str, Enum):
    Normal = "Normal"
    Urgent = "Urgent"