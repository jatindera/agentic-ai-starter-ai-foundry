- Add async retries & error-handling for Azure outages?
- Add better logging + OpenTelemetry for fast debugging?
- How to create a Settings Registry that automatically loads all config modules
- How to create environment-specific config (dev/prod/staging)
- uv add sqlalchemy --prerelease=allow
- uv sync --prerelease=allow

If you want to only create tables in dev and NOT in prod:

Modify init_database() like this:

import os

async def init_database(engine: AsyncEngine):
    if os.getenv("ENVIRONMENT") != "production":
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)


Add to .env:

ENVIRONMENT=development

- Add logging + OpenTelemetry for SQL queries
