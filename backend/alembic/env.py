import sys
from os.path import abspath, dirname
import os
from dotenv import load_dotenv

from logging.config import fileConfig

# --- FIX 1: ADD YOUR PROJECT TO PYTHON'S PATH ---
# This adds your 'backend' folder to the list of places
# Python looks for modules.
sys.path.append(dirname(dirname(abspath(__file__))))
# ------------------------------------------------

from sqlalchemy import engine_from_config, create_engine # <-- Import create_engine
from sqlalchemy import pool

from alembic import context

# --- FIX 2: LOAD .ENV AND IMPORT YOUR MODELS ---
load_dotenv()
from app.models import Base  # <-- Import your Base
# -----------------------------------------------

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata # <-- Point to your Base's metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.
    ...
    """
    
    # --- FIX 3: USE .ENV URL DIRECTLY ---
    url = os.environ["DATABASE_URL"]
    # --------------------------------------
    
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.
    ...
    """
    
    # --- FIX 4: CREATE ENGINE DIRECTLY FROM .ENV URL ---
    connectable = create_engine(os.environ["DATABASE_URL"])
    # ----------------------------------------------------

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()