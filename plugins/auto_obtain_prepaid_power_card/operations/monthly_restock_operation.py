from __future__ import annotations

import time
from typing import TYPE_CHECKING

from one_dragon.base.operation.operation_edge import node_from
from one_dragon.base.operation.operation_node import operation_node
from one_dragon.base.operation.operation_round_result import OperationRoundResult
from one_dragon.base.screen import screen_utils
from one_dragon.utils import cv2_utils, str_utils
from zzz_od.operation.back_to_normal_world import BackToNormalWorld
from zzz_od.operation.zzz_operation import ZOperation

if TYPE_CHECKING:
    from zzz_od.context.zzz_context import ZContext
    from ..auto_obtain_prepaid_power_card_config import AutoObtainPrepaidPowerCardConfig


class MonthlyRestockOperation(ZOperation):
    """情报板商店操作。"""

    def __init__(self, ctx: ZContext, config: AutoObtainPrepaidPowerCardConfig) -> None:
        ZOperation.__init__(self, ctx, op_name='情报板商店')
        self.config: AutoObtainPrepaidPowerCardConfig = config
        self._max_quantity: int = 0

    # ==================== 主题相关节点 ====================

    @operation_node(name="返回大世界", is_start_node=True)
    def back_to_world(self) -> OperationRoundResult:
        """确保在大世界。"""
        op = BackToNormalWorld(self.ctx)
        return self.round_by_op_result(op.execute())

    @node_from(from_name='返回大世界')
    @operation_node(name='前往功能导览')
    def goto_function_menu(self) -> OperationRoundResult:
        """前往主功能导览"""
        result = self.round_by_find_and_click_area(
            self.last_screenshot, '大世界-普通', '功能导览'
        )

        if result.is_success:
            return self.round_success()

        return self.round_retry(wait=1)

    @node_from(from_name='前往功能导览')
    @operation_node(name='进入情报板')
    def enter_info_board(self) -> OperationRoundResult:
        """进入情报板"""
        result = self.round_by_find_and_click_area(self.last_screenshot, "功能导览", "文本-情报板")
        if result.is_success:
            time.sleep(1)
            return self.round_success(status='已点击情报板')
        return self.round_retry(wait=1)

    @node_from(from_name='进入情报板')
    @operation_node(name='点击点数兑换')
    def click_point_exchange(self) -> OperationRoundResult:
        """点击点数兑换"""
        result = self.round_by_find_and_click_area(self.last_screenshot, "情报板", '点数兑换')
        if result.is_success:
            time.sleep(1)
            return self.round_success(status='已点击点数兑换')
        return self.round_retry(wait=1)

    # ==================== 商店操作节点 ====================

    @node_from(from_name='点击点数兑换')
    @operation_node(name='计算最大获取数量')
    def calculate_max_quantity(self) -> OperationRoundResult:
        """计算最大获取数量"""
        area = self.ctx.screen_loader.get_area("自动获取储值电卡-通用", '文本-货币数量')
        part = cv2_utils.crop_image_only(self.last_screenshot, area.rect)
        ocr_result = self.ctx.ocr.run_ocr_single_line(part)
        digit = str_utils.get_positive_digits(ocr_result, None)

        if digit is None:
            return self.round_retry('未识别到贡献点数', wait=1)

        self._max_quantity = int(digit / 120)

        if self._max_quantity < 1:
            return self.round_success(status="贡献点数不足")

        return self.round_success(f'在情报板商店可以获取的储值电卡数量为: {self._max_quantity}个')

    @node_from(from_name='计算最大获取数量')
    @operation_node(name='选择储值电卡')
    def select_prepaid_card(self) -> OperationRoundResult:
        """选择储值电卡"""
        area = self.ctx.screen_loader.get_area("自动获取储值电卡-通用", "道具列表")
        result = self.round_by_ocr_and_click(self.last_screenshot, "储值电卡", area)
        if result.is_success:
            time.sleep(0.5)
            return self.round_success(status=result.status)

        # 向下滚动并重试
        screen_utils.scroll_area(self.ctx, area)
        return self.round_retry(wait=1)

    @node_from(from_name='选择储值电卡')
    @operation_node(name='检查获取条件')
    def check_synthesis(self) -> OperationRoundResult:
        """检查获取条件"""
        result = self.round_by_find_area(self.last_screenshot, "自动获取储值电卡-通用", "已售罄")
        if result.is_success:
            return self.round_success(status='已售罄')
        else:
            return self.round_success(status='可获取')

    @node_from(from_name='检查获取条件', status="可获取")
    @operation_node(name='选择获取数量')
    def select_quantity(self) -> OperationRoundResult:
        """选择获取数量"""
        time.sleep(0.5)
        max_clicks = self._max_quantity - 1
        clicks = min(self.config.outpost_logistics_obtain_number, max_clicks)
        if clicks > 0 and not self._click_increase_button(clicks):
            return self.round_retry(status='未找到数量增加按钮', wait=1)
        return self.round_success()

    def _click_increase_button(self, number: int) -> bool:
        """点击增加按钮"""
        for _ in range(number):
            self.round_by_click_area("自动获取储值电卡-通用", "按钮-增加")
            time.sleep(0.2)
        return True

    @node_from(from_name='选择获取数量')
    @operation_node(name='确认')
    def confirm_purchase(self) -> OperationRoundResult:
        """确认购买"""
        result = self.round_by_find_and_click_area(
            self.last_screenshot, "自动获取储值电卡-通用", "按钮-确认"
        )
        if result.is_success:
            return self.round_success(result.status, wait=1)
        return self.round_retry(wait=1)

    @node_from(from_name='计算最大获取数量', status='贡献点数不足')
    @node_from(from_name='检查获取条件', status='已售罄')
    @node_from(from_name='确认')
    @operation_node(name='完成后返回大世界')
    def return_to_world(self) -> OperationRoundResult:
        """返回大世界"""
        op = BackToNormalWorld(self.ctx)
        return self.round_by_op_result(op.execute())

    @node_from(from_name='完成后返回大世界')
    @operation_node(name='完成')
    def complete(self) -> OperationRoundResult:
        """完成"""
        return self.round_success()