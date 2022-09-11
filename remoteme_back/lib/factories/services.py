from fastapi import Depends

from ..dal.jobs import JobRepository
from ..services.jobs import JobService
from .repositories import job_repository_factory


def job_service_factory(job_repository: JobRepository = Depends(job_repository_factory)) -> JobService:
    return JobService(job_repository)
