"""Test-session defaults that keep the template independent of parent environments."""

import os

_SETTINGS_ENVIRONMENT_VARIABLES = (
    "ENVIRONMENT",
    "API_PREFIX",
    "APP_NAME",
    "APP_VERSION",
    "OPENAPI_URL",
    "SCALAR_PATH",
    "CORS_ALLOW_ORIGINS",
    "CORS_ALLOW_CREDENTIALS",
    "CORS_ALLOW_METHODS",
    "CORS_ALLOW_HEADERS",
    "CORS_EXPOSE_HEADERS",
    "CORS_MAX_AGE",
    "SERVER_HOST",
    "SERVER_PORT",
    "SERVER_RELOAD",
    "LOG_LEVEL",
    "LOG_DIR",
    "LOG_FILE",
    "LOG_MAX_BYTES",
    "LOG_BACKUP_COUNT",
)

for environment_variable in _SETTINGS_ENVIRONMENT_VARIABLES:
    os.environ.pop(environment_variable, None)

os.environ["ENV_FILE"] = ".env.dev"
