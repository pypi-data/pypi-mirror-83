from typing import List, Dict, Any
from uuid import uuid4

from spintop.env import SpintopEnv, alias_for
from spintop.messages import SpintopMessagePublisher, Topics
from spintop.models.lifecycles import FileHandlingContext, reserve_lifecycle_streams

from .bootstrap import gcp_bootstrap, no_provider_bootstrap, not_implemented_bootstrap

from .services.dbt_cloud import DbtCloudInterface

class SpintopDeployEnv(SpintopEnv):
    _env_side_input = None

    SPINTOP_DEPLOY_UUID: str = None

    SPINTOP_STAGE: str = 'dev'
    SPINTOP_DATABASE_STAGE: str = 'dev'
    SPINTOP_CLOUD_PROVIDER: str = 'none'

    # GCP
    GOOGLE_CLOUD_PROJECT: str = None
    GAE_VERSION: str = None # Google App Engine
    PUBSUB_EMULATOR_HOST: str = None # Local emulator if set
    COMMIT_SHA: str = None

    # Dbt Cloud
    DBT_CLOUD_AUTH_TOKEN: str = None

    @property
    def uuid(self):
        if self.SPINTOP_DEPLOY_UUID is None:
            self.SPINTOP_DEPLOY_UUID = uuid4()
        return str(self.SPINTOP_DEPLOY_UUID)

    def provider_modules(self):
        return ProviderModules(self.deployment_provider_modules().modules)

    def deployment_provider_modules(self):
        providers = {
            'gcp': gcp_bootstrap,
            'aws': not_implemented_bootstrap,
            'none': no_provider_bootstrap
        }
        cloud_provider = self.SPINTOP_CLOUD_PROVIDER
        bootstrap_fn = providers.get(cloud_provider)

        if bootstrap_fn:
            return bootstrap_fn(self)
        else:
            raise ValueError(f'Invalid cloud provider: SPINTOP_CLOUD_PROVIDER={cloud_provider!r}')

    def file_handling_context(self, filename):
        return FileHandlingContext(filename, self)

    def dbt_cloud_factory(self):
        return DbtCloudInterface(self)

class ProviderModules(object):
    def __init__(self, _modules):
        self._modules = _modules

    def __getattr__(self, name):
        return self._modules[name]

    def get_secret(self, secret_name):
        param_provider = self.param_provider
        return param_provider.get_environ_or_param_value(secret_name)
