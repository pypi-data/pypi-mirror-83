from typing import List, Union, Any, Dict

from spintop.models import BaseDataClass, get_serializer, FilterSpec

class TableSpec(BaseDataClass):
    filters: List[FilterSpec] = list

class EnvDataspecs(BaseDataClass):
    steps: TableSpec = None

class OrgDataEnv(BaseDataClass):
    name: str
    vars: dict = dict
    dataspecs: EnvDataspecs = None

class Dashboard(BaseDataClass):
    name: str
    base_url: str = None
    sharing_secret: str = None
    sharing_token: str = None
    url: str = None

class Organization(BaseDataClass):
    key: str
    project_id: str
    default_env: str = None
    dashboards: List[Dashboard] = list
    envs: List[OrgDataEnv] = list

    def find_env(self, env_name):
        for env in self.envs:
            if env.name == env_name:
                return env
        else:
            raise ValueError(f'Org {self.key} has no env named {env_name}')

    def env_dataset_name(self, env_name):
        return f'data__{self.key}__{env_name}'

class ManyOrganizations(BaseDataClass):
    orgs: List[Organization]

    def __iter__(self):
        return iter(self.orgs)
    
    def find_org(self, org_key):
        for org in self.orgs:
            if org.key == org_key:
                return org
        else:
            raise ValueError(f'No org named {org_key}')
    

class User(BaseDataClass):
    username: str = None
    user_id: str
    scope: List[str]
    permissions: List[str]
    user_type: str
    organizations: List[Organization]

class UnitMatch(BaseDataClass):
    lc_type: str
    match: str