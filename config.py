import os
import pydantic
from appium.options.android import UiAutomator2Options
from typing import Literal, Optional
from dotenv import load_dotenv
import utils.path

EnvContext = Literal['emulate', 'real', 'browserstack']


class Settings(pydantic.BaseSettings):
    context: EnvContext = 'emulate'

    platformName: str = None
    platformVersion: str = None
    deviceName: str = None
    app: Optional[str] = None
    appName: Optional[str] = None
    appWaitActivity: Optional[str] = None
    newCommandTimeout: Optional[int] = 60

    projectName: Optional[str] = None
    buildName: Optional[str] = None
    sessionName: Optional[str] = None

    myName: Optional[str] = None
    accessKey: Optional[str] = None
    udid: Optional[str] = None

    remote_url: str = 'http://127.0.0.1:4723/wd/hub'

    timeout: float = 6.0

    @property
    def run_on_browserstack(self):
        return 'hub.browserstack.com' in self.remote_url

    @property
    def driver_options(self):
        options = UiAutomator2Options()
        if self.deviceName:
            options.device_name = self.deviceName
        if self.platformName:
            options.platform_name = self.platformName
        options.app = (
            utils.path.path_to_apk(self.app)
            if self.app and (self.app.startswith('./') or self.app.startswith('../'))
            else self.app)
        options.new_command_timeout = self.newCommandTimeout
        if self.udid:
            options.udid = self.udid
        if self.appWaitActivity:
            options.app_wait_activity = self.appWaitActivity
        if self.run_on_browserstack:
            options.load_capabilities(
                {
                    'platformVersion': self.platformVersion,
                    'bstack:options': {
                        'projectName': self.projectName,
                        'buildName': self.buildName,
                        'sessionName': self.sessionName,
                        'userName': self.myName,
                        'accessKey':self.accessKey,
                    },
                }
            )

        return options

    @classmethod
    def in_context(cls, env: Optional[EnvContext] = None) -> 'Settings':
        asked_or_current = env or cls().context
        return cls(_env_file=utils.path.path_to_apk(f'config.{asked_or_current}.env'))


settings = Settings.in_context()
