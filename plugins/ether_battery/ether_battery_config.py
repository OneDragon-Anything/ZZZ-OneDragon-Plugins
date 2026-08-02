"""以太电池（电卡合成）插件配置。

配置文件保存到 config/{instance_idx}/{group_id}/ether_battery.yml
"""

from one_dragon.base.operation.application.application_config import ApplicationConfig

from . import ether_battery_const


class EtherBatteryConfig(ApplicationConfig):
    """以太电池配置类。"""

    def __init__(self, instance_idx: int, group_id: str) -> None:
        ApplicationConfig.__init__(
            self,
            app_id=ether_battery_const.APP_ID,
            instance_idx=instance_idx,
            group_id=group_id,
        )

    @property
    def synthesis_fail_max(self) -> int:
        """点击合成无反应的最大容忍次数，超过则退出。"""
        return self.get("synthesis_fail_max", 3)

    @synthesis_fail_max.setter
    def synthesis_fail_max(self, new_value: int) -> None:
        self.update("synthesis_fail_max", new_value)

    @property
    def confirm_fail_max(self) -> int:
        """点击确认无反应的最大容忍次数，超过则判定素材不足。"""
        return self.get("confirm_fail_max", 3)

    @confirm_fail_max.setter
    def confirm_fail_max(self, new_value: int) -> None:
        self.update("confirm_fail_max", new_value)

    @property
    def max_daily_synthesis(self) -> int:
        """每天最多合成次数，0表示不限制（直到素材不足才退出）。"""
        return self.get("max_daily_synthesis", 0)

    @max_daily_synthesis.setter
    def max_daily_synthesis(self, new_value: int) -> None:
        self.update("max_daily_synthesis", new_value)
