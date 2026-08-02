"""以太电池（电卡合成）插件应用。

流程:
1. 返回大世界
2. 打开快捷手册
3. 点击"前往"
4. 点击"确认"（传送确认）
5. 点击"自动战斗"
6. 点击"前往合成"
7. 循环: 点击"合成"(下半屏) -> 点击"确认" -> 点击"确认"(二次确认)
8. 素材不足或超过3次点击"合成"无反应则退出
9. 循环点击返回/关闭按钮直到返回大世界
"""

from typing import TYPE_CHECKING

from one_dragon.base.geometry.rectangle import Rect
from one_dragon.base.operation.operation_edge import node_from
from one_dragon.base.operation.operation_node import operation_node
from one_dragon.base.operation.operation_notify import NotifyTiming, node_notify
from one_dragon.base.operation.operation_round_result import OperationRoundResult
from one_dragon.base.screen.screen_area import ScreenArea
from zzz_od.application.zzz_application import ZApplication
from zzz_od.operation.back_to_normal_world import BackToNormalWorld

from . import ether_battery_const
from .ether_battery_config import EtherBatteryConfig

if TYPE_CHECKING:
    from zzz_od.context.zzz_context import ZContext

# 画面区域坐标 (1080p)
_RECT_MATERIAL_SHORTAGE = (1235, 835, 1855, 975)  # "合成素材不足" 文字区域
_RECT_SYNTHESIS_BUTTON = (1525, 995, 1855, 1065)  # "合成" 按钮区域


class EtherBatteryApp(ZApplication):
    """以太电池（电卡合成）应用。"""

    def __init__(self, ctx: "ZContext") -> None:
        ZApplication.__init__(
            self,
            ctx=ctx,
            app_id=ether_battery_const.APP_ID,
            op_name=ether_battery_const.APP_NAME,
        )
        self.synthesis_fail_count = 0  # 点击合成无反应的计数器
        self.confirm_fail_count = 0  # 点击确认无反应的计数器
        self.confirm_click_count = 0  # 确认按钮点击次数（合成需要点2次）
        self.synthesis_count = 0  # 已合成次数

        self._config: EtherBatteryConfig | None = None

    @property
    def config(self) -> EtherBatteryConfig:
        if self._config is None:
            self._config = self.ctx.run_context.get_config(ether_battery_const.APP_ID)
        return self._config

    @operation_node(name="返回大世界", is_start_node=True)
    def back_to_world(self) -> OperationRoundResult:
        """确保在大世界。"""
        op = BackToNormalWorld(self.ctx)
        return self.round_by_op_result(op.execute())

    @node_from(from_name="返回大世界")
    @operation_node(name="打开快捷手册")
    def open_compendium(self) -> OperationRoundResult:
        """从大世界直接导航到快捷手册。"""
        return self.round_by_goto_screen(screen_name="快捷手册-训练")

    @node_from(from_name="打开快捷手册")
    @operation_node(name="点击前往", node_max_retry_times=10)
    def click_goto(self) -> OperationRoundResult:
        """全屏识别并点击"前往"。"""
        screen = self.last_screenshot
        if screen is None:
            return self.round_retry(wait=0.5)
        return self.round_by_ocr_and_click(screen, "前往", success_wait=1, retry_wait=1)

    @node_from(from_name="点击前往")
    @operation_node(name="点击确认", node_max_retry_times=10)
    def click_confirm_goto(self) -> OperationRoundResult:
        """点击前往后的确认按钮。"""
        screen = self.last_screenshot
        if screen is None:
            return self.round_retry(wait=0.5)
        return self.round_by_ocr_and_click(screen, "确认", success_wait=1, retry_wait=1)

    @node_from(from_name="点击确认")
    @operation_node(name="点击自动战斗", node_max_retry_times=10)
    def click_auto_battle(self) -> OperationRoundResult:
        """全屏识别并点击"自动战斗"。"""
        screen = self.last_screenshot
        if screen is None:
            return self.round_retry(wait=0.5)
        return self.round_by_ocr_and_click(
            screen, "自动战斗", success_wait=1, retry_wait=1
        )

    @node_from(from_name="点击自动战斗")
    @operation_node(name="点击前往合成", node_max_retry_times=10)
    def click_goto_synthesis(self) -> OperationRoundResult:
        """全屏识别并点击"前往合成"。"""
        screen = self.last_screenshot
        if screen is None:
            return self.round_retry(wait=0.5)
        return self.round_by_ocr_and_click(
            screen, "前往合成", success_wait=1, retry_wait=1
        )

    @node_from(from_name="点击前往合成")
    @node_from(from_name="点击确认按钮", status="继续合成")
    @operation_node(name="点击合成", node_max_retry_times=5)
    def click_synthesis(self) -> OperationRoundResult:
        """检测"素材不足"或点击"合成"按钮。"""
        screen = self.last_screenshot
        if screen is None:
            return self.round_retry(wait=0.5)

        # 检测"合成素材不足"文字
        material_area = ScreenArea(pc_rect=Rect(*_RECT_MATERIAL_SHORTAGE))
        result = self.round_by_ocr(screen, "素材不足", area=material_area)
        if result.is_success:
            return self.round_success(status="素材不足")

        # 点击"合成"按钮
        synthesis_area = ScreenArea(pc_rect=Rect(*_RECT_SYNTHESIS_BUTTON))
        result = self.round_by_ocr_and_click(
            screen, "合成", area=synthesis_area, success_wait=1, retry_wait=0.5
        )

        if result.is_success:
            self.synthesis_fail_count = 0
            self.confirm_click_count = 0  # 重置确认点击计数
            return result

        self.synthesis_fail_count += 1
        if self.synthesis_fail_count >= self.config.synthesis_fail_max:
            return self.round_success(status="退出合成")
        return self.round_retry(wait=0.5)

    @node_from(from_name="点击合成")
    @node_from(from_name="点击确认按钮", status="继续确认")
    @operation_node(name="点击确认按钮", node_max_retry_times=10)
    def click_confirm(self) -> OperationRoundResult:
        """循环点击确认按钮（合成确认 + 获得物品确认）。

        合成流程需要点击两次确认:
        1. 第一次: 合成确认对话框
        2. 第二次: 获得物品确认

        如果连续3次找不到确认（可能是素材不足），则退出合成流程。
        """
        screen = self.last_screenshot
        if screen is None:
            return self.round_retry(wait=0.5)

        result = self.round_by_ocr_and_click(
            screen, "确认", success_wait=0.5, retry_wait=0.5
        )

        if result.is_success:
            self.confirm_fail_count = 0
            self.confirm_click_count += 1
            # 第二次确认后返回继续合成
            if self.confirm_click_count >= 2:
                self.confirm_click_count = 0
                self.synthesis_count += 1
                if (
                    self.config.max_daily_synthesis > 0
                    and self.synthesis_count >= self.config.max_daily_synthesis
                ):
                    return self.round_success(status="达到合成上限", wait=0.5)
                return self.round_success(status="继续合成", wait=0.5)
            return self.round_success(status="继续确认")

        self.confirm_fail_count += 1
        if self.confirm_fail_count >= self.config.confirm_fail_max:
            return self.round_success(status="素材不足")
        return self.round_retry(wait=0.5)

    @node_from(from_name="点击合成", status="退出合成")
    @node_from(from_name="点击合成", status="素材不足")
    @node_from(from_name="点击确认按钮", status="素材不足")
    @node_from(from_name="点击确认按钮", status="达到合成上限")
    @node_notify(when=NotifyTiming.PREVIOUS_DONE, send_image=True, detail=True)
    @operation_node(name="关闭合成界面")
    def close_synthesis(self) -> OperationRoundResult:
        """点击左上角返回按钮关闭合成界面。

        BackToNormalWorld 的"完成"模板会误匹配合成界面的"合成"按钮，
        导致反复点击无法退出。需要先手动关闭合成 UI。
        """
        self.round_by_click_area("画面-通用", "返回")
        return self.round_success(wait=1)

    @node_from(from_name="关闭合成界面")
    @operation_node(name="结束返回大世界")
    def back_to_world_final(self) -> OperationRoundResult:
        """返回大世界。"""
        op = BackToNormalWorld(self.ctx)
        return self.round_by_op_result(op.execute())


def __debug() -> None:
    from zzz_od.context.zzz_context import ZContext

    ctx = ZContext()
    ctx.init()
    app = EtherBatteryApp(ctx)
    app.execute()


if __name__ == "__main__":
    __debug()
