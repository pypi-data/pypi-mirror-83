from zygoat.components import Component
from zygoat.components.backend.reformat import reformat

from .deployment import deployment
from .tokens import token_util
from .django_willing_zg import django_willing_zg
from .google_analytics import google_analytics
from .get_env import get_env_util


class AllComponents(Component):
    pass


all_components = AllComponents(
    sub_components=[
        deployment,
        token_util,
        reformat,
        get_env_util,
        django_willing_zg,
        google_analytics,
    ]
)
