"""自动获取储值电卡插件工厂。

工厂文件必须以 _factory.py 结尾才能被自动发现。
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from one_dragon.base.operation.application.application_config import ApplicationConfig
from one_dragon.base.operation.application.application_factory import ApplicationFactory
from one_dragon.base.operation.application_run_record import AppRunRecord

from . import auto_obtain_prepaid_power_card_const

if TYPE_CHECKING:
    from zzz_od.context.zzz_context import ZContext


class AutoObtainPrepaidPowerCardFactory(ApplicationFactory):
    """自动获取储值电卡插件工厂。"""

    def __init__(self, ctx: ZContext):
        ApplicationFactory.__init__(
            self,
            app_id=auto_obtain_prepaid_power_card_const.APP_ID,
            app_name=auto_obtain_prepaid_power_card_const.APP_NAME,
            default_group=auto_obtain_prepaid_power_card_const.DEFAULT_GROUP,
            need_notify=auto_obtain_prepaid_power_card_const.NEED_NOTIFY,
        )
        self.ctx: ZContext = ctx

    def create_application(self, instance_idx: int, group_id: str):
        from .auto_obtain_prepaid_power_card_app import AutoObtainPrepaidPowerCardApp
        return AutoObtainPrepaidPowerCardApp(self.ctx)

    def create_config(self, instance_idx: int, group_id: str) -> ApplicationConfig:
        from .auto_obtain_prepaid_power_card_config import AutoObtainPrepaidPowerCardConfig
        return AutoObtainPrepaidPowerCardConfig(instance_idx, group_id)

    def create_run_record(self, instance_idx: int) -> AppRunRecord:
        from .auto_obtain_prepaid_power_card_run_record import AutoObtainPrepaidPowerCardRunRecord
        return AutoObtainPrepaidPowerCardRunRecord(
            instance_idx=instance_idx,
            game_refresh_hour_offset=self.ctx.game_account_config.game_refresh_hour_offset,
        )