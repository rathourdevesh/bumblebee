"""Common constants."""
from enum import Enum as PyEnum

class UserRole(PyEnum):
    admin = "admin"
    staff = "staff"
    user = "user"
