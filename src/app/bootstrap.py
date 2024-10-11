import typing

import inject
from src.base.settings import CoreSettings
from src.settings import Settings

from .dependency import configure_dependency

# Configure the Dependencies for the Application
inject.configure(configure_dependency)


def init_app():
    # Loading apps
    # from src.api import demo
    from src.base.bootstrap import create_app

    api_ = create_app(typing.cast(Settings, inject.instance(CoreSettings)))
    return api_


# Create the FAST API app
api = init_app()
