from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str
    redis_url: str

    minio_endpoint: str
    minio_access_key: str
    minio_secret_key: str
    minio_secure: bool = False
    minio_bucket_raw: str = "raw-intel"
    minio_bucket_artifacts: str = "artifacts"

    neo4j_uri: str
    neo4j_user: str
    neo4j_password: str

    jwt_secret: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 720

    cors_origins: str = "http://localhost:3000"

    ipinfo_api_key: str | None = None
    shodan_api_key: str | None = None

settings = Settings()
