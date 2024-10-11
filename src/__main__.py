import sys
from os.path import abspath
from os.path import join

import inject
import uvicorn  # type: ignore

# Adjust the paths
sys.path.insert(0, abspath(join(__file__, "../", "../")))

# Run the ASGI server
from app.bootstrap import api  # noqa
from base.settings import CoreSettings

settings = inject.instance(CoreSettings)

if __name__ == "__main__":
    uvicorn.run(
        "app.bootstrap:api",
        host=settings.app_host,
        port=settings.app_port,
    )
else:
    uvicorn.run(
        api,
        host=settings.app_host,
        port=settings.app_port,
    )
