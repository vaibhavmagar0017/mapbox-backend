import inject
from src.service.unit_of_work import UnitOfWork
from src.settings import Settings


class BaseService:
    uow: UnitOfWork


    @inject.autoparams("uow", "settings")
    def __init__(self, uow: UnitOfWork, settings: Settings):
        self.uow = uow
        self.settings = settings
