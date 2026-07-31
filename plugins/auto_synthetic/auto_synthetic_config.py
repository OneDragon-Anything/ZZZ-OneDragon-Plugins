from one_dragon.base.operation.application.application_config import ApplicationConfig


class AutoSyntheticConfig(ApplicationConfig):
    def __init__(self, instance_idx: int, group_id: str) -> None:
        ApplicationConfig.__init__(self, 'auto_synthetic', instance_idx, group_id)

    @property
    def hifi_master_copy(self) -> bool:
        return self.get('hifi_master_copy', True)

    @hifi_master_copy.setter
    def hifi_master_copy(self, value: bool) -> None:
        self.update('hifi_master_copy', value)

