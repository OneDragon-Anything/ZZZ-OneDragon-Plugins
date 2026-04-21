from __future__ import annotations

from typing import TYPE_CHECKING

from one_dragon.base.operation.application import application_const
from one_dragon.base.operation.operation_edge import node_from
from one_dragon.base.operation.operation_node import operation_node
from one_dragon.base.operation.operation_round_result import OperationRoundResult
from zzz_od.application.zzz_application import ZApplication
from zzz_od.operation.back_to_normal_world import BackToNormalWorld
from . import auto_synthetic_const
from .operations.ether_battery_synthesis_op import EtherBatterySynthesisOp
from .operations.hifi_master_synthesis_op import HifiMasterSynthesisOp

if TYPE_CHECKING:
    from zzz_od.context.zzz_context import ZContext
    from .auto_synthetic_config import AutoSyntheticConfig


class AutoSyntheticApp(ZApplication):
    TASK_HIFI_MASTER = '母盘合成'
    TASK_ETHER_BATTERY = '电池合成'

    def __init__(self, ctx: ZContext) -> None:
        ZApplication.__init__(
            self,
            ctx=ctx,
            app_id=auto_synthetic_const.APP_ID,
            op_name=auto_synthetic_const.APP_NAME,
        )
        self.config: AutoSyntheticConfig = self.ctx.run_context.get_config(
            app_id=auto_synthetic_const.APP_ID,
            instance_idx=self.ctx.current_instance_idx,
            group_id=application_const.DEFAULT_GROUP_ID,
        )

        self._task_queue: list[str] = []
        self.current_task_index: int = 0

    @operation_node(name='检查配置', is_start_node=True)
    def check_config(self) -> OperationRoundResult:
        """检查配置，构建任务队列"""
        self._task_queue = []

        if self.config.hifi_master_copy:
            self._task_queue.append(self.TASK_HIFI_MASTER)
        if self.config.source_ether_battery:
            self._task_queue.append(self.TASK_ETHER_BATTERY)

        if not self._task_queue:
            return self.round_success(status='无任务')

        self.current_task_index = 0

        return self._get_next_task_status()

    def _get_next_task_status(self) -> OperationRoundResult:
        """获取下一个任务的状态"""
        if self.current_task_index >= len(self._task_queue):
            return self.round_success(status='全部完成')

        current_task = self._task_queue[self.current_task_index]

        return self.round_success(status=current_task)

    # ==================== 母盘合成节点 ====================

    @node_from(from_name='检查配置', status='母盘合成')
    @operation_node(name='母盘合成')
    def hifi_master(self) -> OperationRoundResult:
        """执行母盘合成操作"""
        op = HifiMasterSynthesisOp(self.ctx)
        result = self.round_by_op_result(op.execute())

        if result.is_success:
            self.current_task_index += 1
            return self._get_next_task_status()
        return result

    # ==================== 电池合成节点 ====================

    @node_from(from_name='检查配置', status='电池合成')
    @node_from(from_name='母盘合成', status='电池合成')
    @operation_node(name='电池合成')
    def source_ether_battery(self) -> OperationRoundResult:
        """执行电池合成操作"""
        op = EtherBatterySynthesisOp(self.ctx, self.config)
        result = self.round_by_op_result(op.execute())

        if result.is_success:
            self.current_task_index += 1
            return self._get_next_task_status()
        return result

    # ==================== 完成节点 ====================

    @node_from(from_name='检查配置', status='全部完成')
    @node_from(from_name='检查配置', status='无任务')
    @node_from(from_name='母盘合成', status='全部完成')
    @node_from(from_name='电池合成', status='全部完成')
    @operation_node(name='最终返回')
    def final_return(self) -> OperationRoundResult:
        """最终返回大世界"""
        op = BackToNormalWorld(self.ctx)
        return self.round_by_op_result(op.execute())

def __debug() -> None:
    from zzz_od.context.zzz_context import ZContext

    ctx = ZContext()
    ctx.init()
    ctx.run_context.start_running()
    app = AutoSyntheticApp(ctx)
    app.execute()


if __name__ == '__main__':
    __debug()