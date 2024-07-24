from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    database_user: str = Field(..., json_schema_extra={"env": "DATABASE_USER"})
    database_password: str = Field(..., json_schema_extra={"env": "DATABASE_PASSWORD"})
    database_host: str = Field(..., json_schema_extra={"env": "DATABASE_HOST"})
    database_port: int = Field(..., json_schema_extra={"env": "DATABASE_PORT"})
    redis_host: str = Field(..., json_schema_extra={"env": "REDIS_HOST"})
    redis_port: int = Field(..., json_schema_extra={"env": "REDIS_PORT"})

    class Config:
        env_file = ".env"

    def validate_env_variables(self) -> str | None:
        missing_vars = []
        for field in self.__annotations__.keys():
            if not getattr(self, field):
                missing_vars.append(field)
        if missing_vars:
            return f"Missing required environment variables: {', '.join(missing_vars)}"
        return None

class ConfigManager:
    _config_instance = None

    @classmethod
    def init_config(cls) -> None:
        if cls._config_instance is None:
            cls._config_instance = Settings()
            validate = cls._config_instance.validate_env_variables()
            if validate:
                raise RuntimeError(validate)
    
    @classmethod
    def get_config(cls) -> Settings:
        return cls._config_instance
    
    @classmethod
    def close_config(cls) -> None:
        if cls._config_instance is not None:
            cls._config_instance = None