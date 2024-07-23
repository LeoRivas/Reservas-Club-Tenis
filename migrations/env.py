from __future__ import with_statement
from alembic import context
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig
import logging

from flask import current_app

# Interpret the config file for Python logging.
fileConfig(context.config.config_file_name)
logger = logging.getLogger('alembic.env')

config = context.config

# this will overwrite the ini-file sqlalchemy.url path
# with the path given in the Flask app config
section = config.config_ini_section
config.set_section_option(section, "sqlalchemy.url", str(current_app.config.get("SQLALCHEMY_DATABASE_URI")))

target_metadata = current_app.extensions['migrate'].db.metadata

def run_migrations_offline():
    context.configure(
        url=config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool)

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
