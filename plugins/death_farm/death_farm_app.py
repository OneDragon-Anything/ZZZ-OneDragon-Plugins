"""往死里薅 - 自动刷怪应用

传送 → 循环：右移 → 前进 → 弹刀×3 → 脱离卡死 → 回到右移

已接入:
  - OCR 脱离卡死（battle_menu.yml：按钮-脱离卡死 / 按钮-脱离卡死-确认）

TODO:
  - 传送目标「港口工厂旧址 - 小型矿场北侧」需要主程序 map_area.yml 加入对应区域和传送点
    加入后可用 Transport(ctx, '[空洞]港口工厂旧址', '小型矿场北侧') 自动传送
    目前需手动传送到位后再启动插件
  - 黄光检测弹刀优化：dodge_context.check_dodge_flash() 依赖 init_auto_op() 加载 FlashClassifier
    当前插件场景无战斗配置器，模型不会自动初始化
    未来可在 handle_init 中手动初始化 FlashClassifier 并在弹刀节点使用
"""

from __future__ import annotations

import time
from typing import TYPE_CHECKING

from one_dragon.base.operation.operation_edge import node_from
from one_dragon.base.operation.operation_node import operation_node
from one_dragon.base.operation.operation_round_result import OperationRoundResult
from one_dragon.utils.log_utils import log
from zzz_od.application.zzz_application import ZApplication
from zzz_od.context.zzz_context import ZContext

from . import death_farm_const

if TYPE_CHECKING:
    pass


class DeathFarmApp(ZApplication):

    def __init__(self, ctx: ZContext):
        ZApplication.__init__(
            self,
            ctx=ctx,
            app_id=death_farm_const.APP_ID,
            op_name=death_farm_const.APP_NAME,
        )
        self._dodge_count: int = 0
        self._round_count: int = 0

    def handle_init(self):
        ZApplication.handle_init(self)
        self._round_count = 0

    # TODO: 传送节点 — 等主程序 map_area.yml 加入
    #   「港口工厂旧址」区域和「小型矿场北侧」传送点后，
    #   可取消注释以下代码实现自动传送
    #
    # from zzz_od.operation.transport import Transport
    # @operation_node(name='传送', is_start_node=True)
    # def teleport(self) -> OperationRoundResult:
    #     op = Transport(self.ctx, '[空洞]港口工厂旧址', '小型矿场北侧')
    #     return self.round_by_op_result(op.execute())

    @operation_node(name='右移', is_start_node=True)
    def move_right(self) -> OperationRoundResult:
        """按住 D 向右移动约 1 秒"""
        self._dodge_count = 0
        self._round_count += 1
        log.info(f'往死里薅 第 {self._round_count} 轮开始')

        self.ctx.controller.btn_press('d', press_time=1.0)
        time.sleep(0.7)
        return self.round_success()

    @node_from(from_name='右移')
    @operation_node(name='前进')
    def move_forward(self) -> OperationRoundResult:
        """连续点按 W 向前移动约 2 秒"""
        for _ in range(20):
            self.ctx.controller.btn_tap('w')
            time.sleep(0.05)
        time.sleep(0.5)
        return self.round_success()

    @node_from(from_name='前进')
    @operation_node(name='弹刀')
    def dodge(self) -> OperationRoundResult:
        """按空格弹刀，固定间隔约 3 秒，重复 3 次

        TODO: 接入黄光检测优化弹刀时机
            需要手动初始化 FlashClassifier（当前通过 dodge_context.init_auto_op 依赖战斗配置器）
            初始化后可替换为:
                self.screenshot()
                should_dodge = self.ctx.auto_battle_context.dodge_context.check_dodge_flash(
                    self.last_screenshot, self.last_screenshot_time
                )
                if should_dodge:
                    self.ctx.controller.btn_tap('space')
        """
        if self._dodge_count >= 3:
            return self.round_success(status='弹刀完成')

        self.ctx.controller.btn_tap('space')
        self._dodge_count += 1
        log.info(f'弹刀 {self._dodge_count}/3')
        time.sleep(3.0)
        return self.round_success(status='继续弹刀')

    @node_from(from_name='弹刀', status='继续弹刀')
    @operation_node(name='弹刀循环')
    def dodge_loop(self) -> OperationRoundResult:
        """回到弹刀节点"""
        return self.round_success()

    @node_from(from_name='弹刀', status='弹刀完成')
    @operation_node(name='脱离卡死')
    def escape_stuck(self) -> OperationRoundResult:
        """ESC 打开菜单 → OCR 识别并点击「脱离卡死」→ OCR 识别并点击「确认」

        使用内置 battle_menu.yml 定义的按钮区域，
        比固定坐标更稳定，不怕游戏 UI 微调。
        """
        self.ctx.controller.btn_tap('escape')
        time.sleep(2.5)

        # OCR 找「脱离卡死」按钮并点击
        self.screenshot()
        result = self.round_by_find_and_click_area(self.last_screenshot, '战斗-菜单', '按钮-脱离卡死')
        if result.is_success:
            log.info('OCR 识别到脱离卡死按钮')
        else:
            # OCR 识别失败时降级为固定坐标
            log.warning('OCR 未识别到脱离卡死按钮，使用固定坐标降级')
            from one_dragon.base.geometry.point import Point
            self.ctx.controller.click(pos=Point(1672, 1033))
        time.sleep(1.2)

        # OCR 找「确认」按钮并点击
        self.screenshot()
        result = self.round_by_find_and_click_area(self.last_screenshot, '战斗-菜单', '按钮-脱离卡死-确认')
        if result.is_success:
            log.info('OCR 识别到确认按钮')
        else:
            log.warning('OCR 未识别到确认按钮，使用固定坐标降级')
            from one_dragon.base.geometry.point import Point
            self.ctx.controller.click(pos=Point(1065, 632))
        time.sleep(3.2)
        return self.round_success()

    @node_from(from_name='脱离卡死')
    @operation_node(name='循环回到右移')
    def loop_back(self) -> OperationRoundResult:
        """死循环：回到右移"""
        return self.round_success()
