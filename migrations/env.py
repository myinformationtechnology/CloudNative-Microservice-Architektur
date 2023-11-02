from __future__ import with_statement

import logging
from logging.config import fileConfig

from flask import current_app

from alembic import context

# Das ist das Alembic Config-Objekt, das Zugriff auf die Werte in der verwendeten .ini-Datei bietet.
config = context.config

# Interpretiere die Konfigurationsdatei für das Python-Logging.
fileConfig(config.config_file_name)
logger = logging.getLogger("alembic.env")

# Fügen Sie hier das MetaData-Objekt Ihres Modells hinzu
# für die Unterstützung von "autogenerate"
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
config.set_main_option(
    "sqlalchemy.url",
    str(current_app.extensions["migrate"].db.get_engine().url).replace("%", "%%"),
)
target_metadata = current_app.extensions["migrate"].db.metadata

# Andere Werte aus der Konfiguration, die durch die Anforderungen von env.py definiert sind,
# können abgerufen werden:
# my_important_option = config.get_main_option("my_important_option")
# ... usw.

def run_migrations_offline():
    """Führen Sie Migrationen im 'offline'-Modus aus.

    Dies konfiguriert den Kontext nur mit einer URL
    und nicht mit einem Engine, obwohl hier eine Engine ebenfalls akzeptabel ist. Durch das Überspringen
    der Engine-Erstellung ist es nicht einmal notwendig, dass ein DBAPI verfügbar ist.

    Aufrufe von context.execute() hier geben den angegebenen String an das
    Skriptausgabe aus.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Führen Sie Migrationen im 'Online'-Modus aus.

    In diesem Szenario müssen wir eine Engine erstellen
    und eine Verbindung mit dem Kontext verknüpfen.

    """

    # Dieser Rückruf wird verwendet, um die Generierung einer Auto-Migration zu verhindern
    # wenn keine Änderungen am Schema vorgenommen wurden
    # Verweis: http://alembic.zzzcomputing.com/en/latest/cookbook.html
    def process_revision_directives(context, revision, directives):
        if getattr(config.cmd_opts, "autogenerate", False):
            script = directives[0]
            if script.upgrade_ops.is_empty():
                directives[:] = []
                logger.info("Keine Änderungen im Schema festgestellt.")

    connectable = current_app.extensions["migrate"].db.get_engine()

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            process_revision_directives=process_revision_directives,
            **current_app.extensions["migrate"].configure_args
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

