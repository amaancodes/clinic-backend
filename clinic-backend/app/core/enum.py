import enum

class Role(str, enum.Enum):
    admin = "admin"
    doctor = "doctor"
    member = "member"

class AppointmentStatus(str, enum.Enum):
    SCHEDULED = "scheduled"
    COMPLETED = "completed"
    CANCELLED = "cancelled"