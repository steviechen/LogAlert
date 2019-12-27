# -*- coding: utf-8 -*-
from src.main.service.impl.LogExQueryConfigService import LogExQueryConfigService

class LogExQueryConfigHandler():
    def __init__(self):
        super().__init__()
        self.logExQueryConfigService = LogExQueryConfigService()

    def get(self):
        return self.logExQueryConfigService.make_procedure()
