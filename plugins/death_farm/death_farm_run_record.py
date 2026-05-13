"""往死里薅运行记录"""

from one_dragon.base.operation.application_run_record import AppRunRecord

from . import death_farm_const


class DeathFarmRunRecord(AppRunRecord):
    """往死里薅运行记录"""

    def __init__(
        self, instance_idx: int | None = None, game_refresh_hour_offset: int = 0
    ):
        AppRunRecord.__init__(
            self,
            app_id=death_farm_const.APP_ID,
            instance_idx=instance_idx,
            game_refresh_hour_offset=game_refresh_hour_offset,
        )

    @property
    def round_count(self) -> int:
        """累计刷取轮数"""
        return self.get("round_count", 0)

    @round_count.setter
    def round_count(self, new_value: int) -> None:
        self.update("round_count", new_value)
