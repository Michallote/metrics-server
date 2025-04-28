# fastapi-app/main.py
import asyncio
import os

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
DATABASE_URL = (
    f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@db:5432/{POSTGRES_DB}"
)

engine = create_async_engine(DATABASE_URL, echo=False, future=True)
AsyncSessionLocal = sessionmaker(
    bind=engine, expire_on_commit=False, class_=AsyncSession
)
Base = declarative_base()


class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app = FastAPI()


# NEW helper function: wait for DB connection
async def wait_for_postgres(retries: int = 10, delay: float = 2.0):
    for attempt in range(1, retries + 1):
        try:
            async with engine.begin() as conn:
                await conn.execute(select(1))
            print("Connected to PostgreSQL!")
            return
        except Exception as e:
            print(f"Attempt {attempt}: PostgreSQL not ready yet ({e})")
            if attempt == retries:
                raise RuntimeError(
                    "Database is unreachable after several attempts."
                ) from e
            await asyncio.sleep(delay)


@app.on_event("startup")
async def startup_event():
    await wait_for_postgres()
    await init_models()


class ItemIn(BaseModel):
    name: str
    description: str | None = None


class ItemOut(ItemIn):
    id: int


@app.post("/items/", response_model=ItemOut)
async def create_item(item: ItemIn):
    async with AsyncSessionLocal() as session:
        new_item = Item(name=item.name, description=item.description)
        session.add(new_item)
        await session.commit()
        await session.refresh(new_item)
        return new_item


@app.get("/items/", response_model=list[ItemOut])
async def read_items():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Item))
        items = result.scalars().all()
        return items
