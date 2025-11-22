from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Configuración de la aplicación.
    Lee las variables de entorno desde el archivo .env
    """
    # Información del proyecto
    PROJECT_NAME: str
    
    # Configuración de la base de datos
    DATABASE_URL: str
    
    # Configuración de seguridad JWT
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    
    # Entorno de ejecución
    ENVIRONMENT: str
    
    # Configuración para leer desde .env
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True
    )


# Crear una instancia única de configuración
settings = Settings()
