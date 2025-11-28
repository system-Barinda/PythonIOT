class Database:
    def __init__(self):
        database_url = os.getenv(
            "DATABASE_URL",
            "postgresql+asyncpg://postgres:YOUR_PASSWORD@localhost:5432/iot_db"
        )

        # Convert normal postgres URL → async URL
        if database_url.startswith("postgresql://"):
            database_url = database_url.replace("postgresql://", "postgresql+asyncpg://")

        self.engine = create_async_engine(database_url, echo=False)
        self.SessionLocal = async_sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )
