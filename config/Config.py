import os
from typing import Tuple, Set, Dict

import yaml
from dataclass_wizard import fromdict

from config.Data import ConfigSettings


class Config:

    def __init__(self):
        self.config_path = os.environ.get('CONFIG', '/app/configs/config.yaml')
        self.config_dicts: Dict = self._get_config_dict()
        self.config_settings: ConfigSettings = self._get_config_settings()

    def _get_config_dict(self) -> Dict:
        with open(self.config_path, "r") as config_file:
            config_dict = yaml.safe_load(config_file)
        return config_dict

    def _get_config_settings(self) -> ConfigSettings:
        return fromdict(ConfigSettings, self.config_dicts)

    def get_database_settings(self) -> Tuple[str, str, str, str]:
        user = self.config_settings.common.action_maker.class_params.pass_controller.db_creds.user
        password = self.config_settings.common.action_maker.class_params.pass_controller.db_creds.password
        host = self.config_settings.common.action_maker.class_params.pass_controller.db_creds.host
        database = self.config_settings.common.action_maker.class_params.pass_controller.db_creds.database

        return user, password, host, database

    def get_object_id(self) -> int:
        return self.config_settings.common.action_maker.class_params.pass_controller.object_id

    def get_post_ids(self) -> Set[int]:
        return set(
            [
                point.action_params.pass_controller.post_id for gate in self.config_settings.gates
                for point in gate.points
            ]
        )
