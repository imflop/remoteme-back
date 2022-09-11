from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..dal.jobs import JobRepository
from .base import async_session_factory


def job_repository_factory(db: AsyncSession = Depends(async_session_factory)) -> JobRepository:
    return JobRepository(db)
