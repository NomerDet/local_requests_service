from dataclasses import dataclass
from typing import List, Optional


@dataclass
class DBSettings:
    host: str
    database: str
    user: str
    password: str


@dataclass
class PassController:
    db_creds: Optional[DBSettings] = None
    object_id: Optional[int] = None
    post_id: Optional[int] = None


@dataclass
class ClassParams:
    pass_controller: PassController


@dataclass
class ActionMaker:
    class_params: ClassParams


@dataclass
class Common:
    action_maker: ActionMaker


@dataclass
class ActionParams:
    pass_controller: PassController


@dataclass
class CameraParams:
    action_params: ActionParams


@dataclass
class Gates:
    points: List[CameraParams]


@dataclass
class ConfigSettings:
    common: Common
    gates: List[Gates]
