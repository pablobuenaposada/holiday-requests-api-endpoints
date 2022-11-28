STATUS_PENDING = "pending"
STATUS_APPROVED = "approved"
STATUS_REJECTED = "rejected"
STATUS = [
    (STATUS_APPROVED, "Approved"),
    (STATUS_REJECTED, "Rejected"),
    (STATUS_PENDING, "Pending"),
]
MANAGER_TYPE = "manager"
WORKER_TYPE = "worker"
USER_TYPES = ((MANAGER_TYPE, "Manager"), (WORKER_TYPE, "Worker"))
