import os
from mangum import Mangum
from sys import path
from os.path import abspath
from os.path import join
import inject
import uvicorn  # type: ignore

# Adjust the paths
path.insert(0, abspath(join(__file__, "../", "../")))

# Run the ASGI server
from app.bootstrap import api  as app
from base.settings import CoreSettings

settings = inject.instance(CoreSettings)

handler = Mangum(app)
