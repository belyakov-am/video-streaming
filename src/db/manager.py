import asyncpg

import db.queries as q


class DBManager:
    """
    Class for communicating with the database.
    It holds a pool of connections and execute queries in an async way.
    """

    def __init__(
            self,
            user: str,
            password: str,
            db: str,
            host: str,
            port: int,
    ) -> None:
        self.user = user
        self.password = password
        self.db = db
        self.host = host
        self.port = port

        self.pool = None

    async def init_connection_pool(self):
        self.pool = await asyncpg.create_pool(
            user=self.user,
            password=self.password,
            database=self.db,
            host=self.host,
            port=self.port,
        )

    async def close_connection_pool(self):
        await self.pool.close()

    async def init_table(self) -> None:
        async with self.pool.acquire() as conn:
            await conn.execute(q.CREATE_VIDEOS_TABLE)

    async def insert_video_info(
            self,
            video_uuid: str,
            name: str,
            description: str,
    ) -> bool:
        async with self.pool.acquire() as conn:
            status = await conn.execute(
                q.INSERT_VIDEO_INFO,
                video_uuid, name, description,
            )

        return status

    async def select_video_info(self):
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(q.SELECT_VIDEO_INFO)

        return rows
