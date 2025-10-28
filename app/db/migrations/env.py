from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# Importa as configurações do Alembic
config = context.config

# Configura logs do Alembic
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 🚀 Importa os modelos do seu projeto
from app.db.base import Base  # <- certifique-se que app/db/base.py existe e importa todos os models

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Executa migrações no modo offline."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Executa migrações no modo online (conectando ao banco)."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
