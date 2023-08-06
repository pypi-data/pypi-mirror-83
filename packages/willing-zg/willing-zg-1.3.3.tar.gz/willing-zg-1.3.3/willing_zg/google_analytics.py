import logging
import os

from zygoat.constants import Phases
from zygoat.components import Component, FileComponent
from zygoat.constants import Projects
from zygoat.utils.files import use_dir
from zygoat.utils.shell import run

from . import resources

log = logging.getLogger()


class GoogleAnalyticsSettings(FileComponent):
    resource_pkg = resources
    base_path = os.path.join(Projects.FRONTEND, "utils", "constants")
    filename = "google.js"
    overwrite = False


class GoogleAnalyticsUtils(FileComponent):
    resource_pkg = resources
    base_path = os.path.join(Projects.FRONTEND, "zg_utils")
    filename = "google-analytics.js"


class GoogleAnalyticsDependencies(Component):

    @property
    def installed(self):
        completed_process = run(["yarn", "info", "react-ga"])
        return completed_process.returncode == 0

    def create(self):
        with use_dir(Projects.FRONTEND):
            log.info("Installing react-ga Google Analytics plugin for React")
            run(["yarn", "add", "react-ga"])

    def update(self):
        self.call_phase(Phases.CREATE, force_create=True)


class GoogleAnalytics(Component):
    pass


google_analytics = GoogleAnalytics(
    sub_components=[
        GoogleAnalyticsDependencies(),
        GoogleAnalyticsSettings(),
        GoogleAnalyticsUtils(),
    ]
)
