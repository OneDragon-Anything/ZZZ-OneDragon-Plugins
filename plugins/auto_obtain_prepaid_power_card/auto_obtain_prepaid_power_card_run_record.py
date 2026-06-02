"""自动获取储值电卡插件运行记录。"""

from one_dragon.base.operation.application_run_record import AppRunRecord

from . import auto_obtain_prepaid_power_card_const


class AutoObtainPrepaidPowerCardRunRecord(AppRunRecord):
    """自动获取储值电卡运行记录类。"""

    def __init__(self, instance_idx: int | None = None, game_refresh_hour_offset: int = 0):
        AppRunRecord.__init__(
            self,
            app_id=auto_obtain_prepaid_power_card_const.APP_ID,
            instance_idx=instance_idx,
            game_refresh_hour_offset=game_refresh_hour_offset
        )