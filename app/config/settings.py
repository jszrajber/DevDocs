from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str
    POSTGRES_DB: str

    @property
    def DATABASE_URL(self) -> str:
        """
        Returns valid db url.
        Dynamically assembles the async database connection string 
        using individual PostgreSQL credentials.
        """
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:5432/{self.POSTGRES_DB}"

    @property
    def VECTOR_URL(self) -> str:
        """
        For LangChain / PGVector / psycopg.
        Vectors are created synchronously
        """
        return f"postgresql+psycopg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:5432/{self.POSTGRES_DB}"

    # Shows where to find variables, defines behaviour while loading settings
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")  # Prevents errors if .env contains variables not defined in this class


settings = Settings()
