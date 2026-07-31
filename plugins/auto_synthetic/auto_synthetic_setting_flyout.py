from __future__ import annotations

from qfluentwidgets import FluentIcon

from one_dragon_qt.utils.config_utils import get_prop_adapter
from one_dragon_qt.widgets.app_setting.app_setting_flyout import AppSettingFlyout
from one_dragon_qt.widgets.setting_card.switch_setting_card import SwitchSettingCard
from . import auto_synthetic_const
from .auto_synthetic_config import AutoSyntheticConfig


class AutoSyntheticSettingFlyout(AppSettingFlyout):

    def _setup_ui(self, layout) -> None:

        self.auto_synthetic_hifi_master_copy = SwitchSettingCard(icon=FluentIcon.GAME, title='高保真母盘')
        layout.addWidget(self.auto_synthetic_hifi_master_copy)

    def init_config(self) -> None:
        config: AutoSyntheticConfig = self.ctx.run_context.get_config(
            app_id=auto_synthetic_const.APP_ID,
            instance_idx=self.ctx.current_instance_idx,
            group_id=self.group_id,
        )
        self.auto_synthetic_hifi_master_copy.init_with_adapter(get_prop_adapter(config, 'hifi_master_copy'))