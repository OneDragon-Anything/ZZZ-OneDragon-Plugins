from __future__ import annotations

import time
from typing import TYPE_CHECKING

from one_dragon.base.geometry.rectangle import Rect
from one_dragon.base.operation.operation_edge import node_from
from one_dragon.base.operation.operation_node import operation_node
from one_dragon.base.operation.operation_round_result import OperationRoundResult
from one_dragon.utils import cv2_utils, str_utils
from zzz_od.operation.goto.goto_menu import GotoMenu
from zzz_od.operation.zzz_operation import ZOperation

if TYPE_CHECKING:
    from zzz_od.context.zzz_context import ZContext
    from ..auto_synthetic_config import AutoSyntheticConfig

class EtherBatterySynthesisOp(ZOperation):
    """电池合成操作"""

    def __init__(self, ctx: ZContext, config: AutoSyntheticConfig) -> None:
        ZOperation.__init__(self, ctx, op_name='电池合成')
        self.config = config
        self.max_synthetic_quantity: int = 0
        self.max_synthetic_quantity_from_battery_charge: int = 0
        self.max_synthetic_quantity_from_prepaid_power_card: int = 0

    @operation_node(name='打开菜单', is_start_node=True)
    def open_menu(self) -> OperationRoundResult:
        op = GotoMenu(self.ctx)
        return self.round_by_op_result(op.execute())

    @node_from(from_name='打开菜单')
    @operation_node(name='首次计算合成数量')
    def calculation_max_synthetic_quantity_from_battery_charge(self) -> OperationRoundResult:
        """根据电量计算合成的最大数量"""
        area = self.ctx.screen_loader.get_area('菜单', '文本-电量')
        part = cv2_utils.crop_image_only(self.last_screenshot, area.rect)
        ocr_result = self.ctx.ocr.run_ocr_single_line(part)
        digit = str_utils.get_positive_digits(ocr_result, None)

        if digit is None:
            return self.round_retry('未识别到电量', wait=1)

        self.max_synthetic_quantity_from_battery_charge = int(digit / 60)
        self.max_synthetic_quantity = self.max_synthetic_quantity_from_battery_charge

        if self.max_synthetic_quantity_from_battery_charge < 1:
            return self.round_success(status="电量不足")
        return self.round_success(f'电量可以合成的电池数量为：{self.max_synthetic_quantity}个')

    @node_from(from_name='首次计算合成数量')
    @operation_node(name='前往仓库')
    def goto_storage(self) -> OperationRoundResult:
        """前往仓库界面"""
        return self.round_by_find_and_click_area(self.last_screenshot, '菜单', '底部-仓库')

    @node_from(from_name='前往仓库')
    @operation_node(name='前往材料道具')
    def goto_storage_materials_tools(self) -> OperationRoundResult:
        """前往材料道具界面"""
        # 必须等待1秒，不然会因为仓库界面没有完全加载导致操作卡在下个节点
        time.sleep(1)
        self.ctx.controller.click(Rect(*(1605, 124, 1676, 212)).center)
        return self.round_success()

    @node_from(from_name='前往材料道具')
    @operation_node(name='前往合成')
    def goto_synthesis(self) -> OperationRoundResult:
        """前往电池合成界面"""
        return self.round_by_find_and_click_area(self.last_screenshot, '仓库-材料道具', "道具处理")

    @node_from(from_name='前往合成')
    @operation_node(name='检查合成条件')
    def check_synthesis(self) -> OperationRoundResult:
        """检查合成条件"""
        # 截至到绝区零2.7版本道具处理界面的首位可合成物品是以太电池，所以有了下面的逻辑
        # 不排除存在后续版本更新导致这个方法逻辑失效，插件的支持还是太少了，如果可以使用主程序的模板识别功能会好很多
        area = self.ctx.screen_loader.get_area('仓库-材料道具-道具处理', '以太电池')
        result = self.round_by_ocr(self.last_screenshot, "以太电池", area=area)
        if result.is_success:
            return self.round_by_find_and_click_area(
                self.last_screenshot, '仓库-材料道具-道具处理', "图像-储值电卡"
            )
        else:
            # 移除了模板匹配电池图片的逻辑
            if self.max_synthetic_quantity_from_battery_charge < 1:
                return self.round_success(status='电量不足')
            else:
                return self.round_success(status='储值电卡数量不足')

    @node_from(from_name='检查合成条件')
    @operation_node(name='第二次计算合成数量')
    def calculation_max_synthetic_quantity_from_prepaid_power_card(self) -> OperationRoundResult:
        """根据储值电卡数量计算合成的最大数量"""
        area = self.ctx.screen_loader.get_area('仓库-材料道具-道具处理', '储值电卡数量')
        part = cv2_utils.crop_image_only(self.last_screenshot, area.rect)
        ocr_result = self.ctx.ocr.run_ocr_single_line(part)
        digit = str_utils.get_positive_digits(ocr_result, None)

        self.round_by_find_and_click_area(
            self.last_screenshot, '仓库-材料道具-道具处理', "图像-储值电卡"
        )

        if digit is None:
            return self.round_retry('未识别到储值电卡数量', wait=1)

        self.max_synthetic_quantity_from_prepaid_power_card = digit

        return self.round_success(f'电量可以合成的电池数量为：{self.max_synthetic_quantity_from_prepaid_power_card}个')

    @node_from(from_name='第二次计算合成数量')
    @operation_node(name='更新合成数量')
    def update_the_synthesis_quantity(self) -> OperationRoundResult:
        if self.max_synthetic_quantity_from_prepaid_power_card < self.max_synthetic_quantity:
            self.max_synthetic_quantity = self.max_synthetic_quantity_from_prepaid_power_card

        return self.round_success(f'更新后合成的电池数量为：{self.max_synthetic_quantity}个')

    @node_from(from_name='更新合成数量')
    @operation_node(name='选择合成数量')
    def add_quantity(self) -> OperationRoundResult:
        clicks = self.config.get_battery_click_count(self.max_synthetic_quantity)

        if clicks > 0 and not self._click_increase_button(clicks):
            return self.round_retry(status='未找到数量增加按钮', wait=1)

        return self.round_success()

    def _click_increase_button(self, number: int) -> bool:
        """点击增加按钮"""
        for _ in range(number):
            self.round_by_click_area('仓库-材料道具-道具处理', "按钮-增加")
            time.sleep(0.2)
        return True

    @node_from(from_name='选择合成数量')
    @operation_node(name='执行合成')
    def perform_synthesis(self) -> OperationRoundResult:
        """执行合成"""
        result = self.round_by_find_and_click_area(
            self.last_screenshot,"仓库-材料道具-道具处理", "按钮-合成"
        )
        if result.is_success:
            return self.round_success()
        return self.round_retry(wait=1)

    @node_from(from_name='执行合成')
    @operation_node(name='确认合成')
    def confirm(self) -> OperationRoundResult:
        """确认合成"""
        result = self.round_by_find_and_click_area(
            self.last_screenshot,
            "仓库-材料道具-道具处理",
            "按钮-确认",
        )
        if result.is_success:
            return self.round_success()
        return self.round_retry(wait=1)

    @node_from(from_name='首次计算合成数量', status='电量不足')
    @node_from(from_name='检查合成条件', status='电量不足')
    @node_from(from_name='检查合成条件', status='储值电卡数量不足')
    @node_from(from_name='确认合成')
    @operation_node(name='返回')
    def back(self) -> OperationRoundResult:
        """点击左上角返回按钮"""
        result = self.round_by_click_area("画面-通用", "返回")
        if result.is_success:
            return self.round_success(result.status, wait=1)
        return self.round_retry(wait=1)

    @node_from(from_name='返回')
    @operation_node(name='前往大世界')
    def goto_world(self) -> OperationRoundResult:
        return self.round_by_find_and_click_area(self.last_screenshot, '画面-通用', '左上角-街区')

def __debug() -> None:
    from zzz_od.context.zzz_context import ZContext
    from ..auto_synthetic_config import AutoSyntheticConfig

    ctx = ZContext()
    ctx.init()
    ctx.run_context.start_running()
    config = AutoSyntheticConfig(instance_idx=ctx.current_instance_idx, group_id="one_dragon")
    op = EtherBatterySynthesisOp(ctx, config)
    op.execute()


if __name__ == '__main__':
    __debug()