"""以太电池（电卡合成）插件工厂。

工厂文件必须以 _factory.py 结尾才能被自动发现。
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from one_dragon.base.operation.application.application_factory import ApplicationFactory
from one_dragon.base.operation.application_base import Application
from one_dragon.base.operation.application_run_record import AppRunRecord

from . import ether_battery_const

if TYPE_CHECKING:
    from zzz_od.context.zzz_context import ZContext


class EtherBatteryFactory(ApplicationFactory):
    """以太电池（电卡合成）插件工厂。"""

    def __init__(self, ctx: ZContext) -> None:
        ApplicationFactory.__init__(
            self,
            app_id=ether_battery_const.APP_ID,
            app_name=ether_battery_const.APP_NAME,
            need_notify=ether_battery_const.NEED_NOTIFY,
            default_group=ether_battery_const.DEFAULT_GROUP,
        )
        self.ctx = ctx

    def create_application(self, instance_idx: int, group_id: str) -> Application:
        from .ether_battery_app import EtherBatteryApp

        return EtherBatteryApp(self.ctx)

    def create_run_record(self, instance_idx: int) -> AppRunRecord:
        from .ether_battery_run_record import EtherBatteryRunRecord

        return EtherBatteryRunRecord(
            instance_idx=instance_idx,
            game_refresh_hour_offset=self.ctx.game_account_config.game_refresh_hour_offset,
        )
