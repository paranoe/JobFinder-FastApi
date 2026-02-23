from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

class BaseCrud:
    def __init__(self, model):
        self.model = model

    async def get(self, db: AsyncSession, id: int):
        result = await db.execute(select(self.model).filter(self.model.id == id))
        return result.scalars().first()

    async def get_all(self, db: AsyncSession):
        result = await db.execute(select(self.model))
        return result.scalars().all()

    async def create(self, db: AsyncSession, obj_data):
        if isinstance(obj_data, dict):
            instance = self.model(**obj_data)
        else:
            instance = self.model(**obj_data.model_dump())
        db.add(instance)
        await db.flush()
        await db.refresh(instance)
        return instance

    async def update(self, db: AsyncSession, obj_data, id):
        db_obj = await self.get(db, id)
        if db_obj:
            if isinstance(obj_data, dict):
                update_data = obj_data
            else:
                update_data = obj_data.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_obj, key, value)
            await db.commit()
            await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, id):
        db_obj = await self.get(db, id)
        if db_obj:
            await db.delete(db_obj)
            await db.commit()
        return db_obj