import contextlib
from pathlib import Path

from fastapi import FastAPI
from sqlalchemy.sql import Select
from sqlalchemy import cast, String
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import ChunkedIteratorResult
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, create_async_engine

try:
    from loggers.logger import logger
    from utils.decorators import utils
    from settings.config import config
    from app.models import Base, UserModel, ReceiptModel
    from app.schemas import (
        RegisterRequestSchema,
        BaseReceiptResponseSchema,
        ReceiptResponseSchema,
        ReceiptListRequestSchema
    )
except ImportError as ie:
    exit(f"{ie} :: {Path(__file__).resolve()}")


class Database:
    _engine: AsyncEngine = create_async_engine(
        url=config.DATABASE["postgres"].format(user=config.DB_USER, password=config.DB_PASS)
    )
    session_factory: sessionmaker[AsyncSession] = sessionmaker(
        bind=_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    @contextlib.asynccontextmanager
    async def init(self, _: FastAPI) -> None:
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        yield
        await self._engine.dispose()

    @contextlib.asynccontextmanager
    async def get_session(self) -> AsyncSession:
        async with self.session_factory() as session:
            try:
                yield session
            except Exception as e:
                await session.rollback()
                raise e
            finally:
                await session.close()

    @utils.async_exception
    async def get_user(self, username: str = None, used_id: int = None) -> UserModel:
        async with self.get_session() as session:
            if username:
                query: Select = select(UserModel).filter_by(username=username)
            elif used_id:
                query: Select = select(UserModel).filter_by(id=used_id)

            result: ChunkedIteratorResult = await session.execute(statement=query)
            return result.scalar_one_or_none()

    @utils.async_exception
    async def create_user(self, new_user: RegisterRequestSchema) -> int:
        async with self.get_session() as session:
            new_user: UserModel = UserModel(**new_user.model_dump())
            session.add(new_user)
            await session.commit()
            return new_user.id

    @utils.async_exception
    async def get_filtered_receipts(self, user_id: int, filters: ReceiptListRequestSchema) -> list[BaseReceiptResponseSchema]:
        async with self.get_session() as session:
            query: Select = select(ReceiptModel).filter_by(user_id=user_id)

            if filters.start_date:
                query: Select = query.filter(ReceiptModel.created_at >= filters.start_date)
            if filters.end_date:
                query: Select = query.filter(ReceiptModel.created_at <= filters.end_date)

            if filters.min_total:
                query: Select = query.filter(ReceiptModel.total >= filters.min_total)

            if filters.payment_type:
                query: Select = query.filter(cast(ReceiptModel.payment.op("->>")("type"), String) == filters.payment_type)

            offset: int = (filters.page - 1) * filters.page_size
            query: Select = query.offset(offset).limit(filters.page_size)

            result: ChunkedIteratorResult = await session.execute(query)
            receipt_filtered: ReceiptModel = result.scalars().all()
            return [BaseReceiptResponseSchema.model_validate(receipt) for receipt in receipt_filtered]

    @utils.async_exception
    async def get_receipt(self, receipt_id: int) -> BaseReceiptResponseSchema:
        async with self.get_session() as session:
            query: Select = select(ReceiptModel).filter_by(id=receipt_id)

            result: ChunkedIteratorResult = await session.execute(statement=query)
            receipt: ReceiptModel = result.scalar_one_or_none()
            return BaseReceiptResponseSchema.model_validate(receipt)

    @utils.async_exception
    async def create_receipt(self, new_receipt: ReceiptResponseSchema) -> BaseReceiptResponseSchema:
        async with self.get_session() as session:
            new_receipt: ReceiptModel = ReceiptModel(**new_receipt.model_dump())
            session.add(new_receipt)
            await session.commit()
            return BaseReceiptResponseSchema.model_validate(new_receipt)


db: Database = Database()
