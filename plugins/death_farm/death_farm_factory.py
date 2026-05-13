"""往死里薅工厂"""

from __future__ import annotations

from typing import TYPE_CHECKING

from one_dragon.base.operation.application.application_factory import ApplicationFactory

from . import death_farm_const
from .death_farm_run_record import DeathFarmRunRecord

if TYPE_CHECKING:
    from zzz_od.context.zzz_context import ZContext


class DeathFarmFactory(ApplicationFactory):

    def __init__(self, ctx: ZContext):
        ApplicationFactory.__init__(self, death_farm_const)
        self.ctx: ZContext = ctx

    def create_application(self, instance_idx: int, group_id: str):
        from .death_farm_app import DeathFarmApp
        return DeathFarmApp(self.ctx)

    def create_run_record(self, instance_idx: int):
        return DeathFarmRunRecord(instance_idx=instance_idx)
