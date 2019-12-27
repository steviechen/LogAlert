# -*- coding: utf-8 -*-
from src.main.service.impl.LogAlertQueryConfigService import LogAlertQueryConfigService

class LogAlertQueryConfigHandler():
    def __init__(self):
        super().__init__()
        self.LogAlertQueryConfigService = LogAlertQueryConfigService()

    def get(self):
        return self.LogAlertQueryConfigService.make_procedure()
