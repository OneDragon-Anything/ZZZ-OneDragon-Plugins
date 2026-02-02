"""以太电池（电卡合成）运行记录。"""

from one_dragon.base.operation.application_run_record import AppRunRecord

from . import ether_battery_const


class EtherBatteryRunRecord(AppRunRecord):
    """以太电池（电卡合成）运行记录。"""

    def __init__(
        self, instance_idx: int | None = None, game_refresh_hour_offset: int = 0
    ) -> None:
        AppRunRecord.__init__(
            self,
            ether_battery_const.APP_ID,
            instance_idx=instance_idx,
            game_refresh_hour_offset=game_refresh_hour_offset,
        )
