"""
Dynaconf Settings
"""
from dynaconf import Dynaconf, Validator

settings = Dynaconf(
    environments=True,
    envvar_prefix=False,
    load_dotenv=True,
    settings_files=["mast/settings.toml"],
    validators=[
        Validator("CORS_ENABLED", default=False),
        Validator("root_path", default=""),
        Validator("S3_ENDPOINT_HOSTNAME", must_exist=True),
        Validator("S3_ENDPOINT_PROTOCOL", must_exist=True),
        Validator("S3_ACCESS_KEY_ID", must_exist=True),
        Validator("S3_SECRET_ACCESS_KEY", must_exist=True),
        Validator("S3_REGION", must_exist=True, default="EU"),
        Validator("S3_Bucket", must_exist=True),
        Validator("S3_Key", must_exist=True, default=""),
        Validator("AUTH_SERVER"),
        Validator("POSTGRES_HOST", default="localhost"),
        Validator("POSTGRES_PORT", default=5432),
        Validator("POSTGRES_USER", default="postgres"),
        Validator("POSTGRES_PASSWORD", default="password"),
        Validator("POSTGRES_DB", default="postgres"),
    ],
)

CORS_ENABLED: bool = settings.CORS_ENABLED  # type: ignore
root_path: str = settings.root_path  # type: ignore
S3_Key: bool = settings.S3_Key  # type: ignore
S3_Key: str = settings.S3_Key  # type: ignore
