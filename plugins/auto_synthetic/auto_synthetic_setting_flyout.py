from __future__ import annotations

from qfluentwidgets import FluentIcon

from one_dragon_qt.utils.config_utils import get_prop_adapter
from one_dragon_qt.widgets.app_setting.app_setting_flyout import AppSettingFlyout
from one_dragon_qt.widgets.setting_card.combo_box_setting_card import ComboBoxSettingCard
from one_dragon_qt.widgets.setting_card.switch_setting_card import SwitchSettingCard
from . import auto_synthetic_const
from .auto_synthetic_config import SourceEtherBatteryAutoSyntheticQuantity, AutoSyntheticConfig


class AutoSyntheticSettingFlyout(AppSettingFlyout):

    def _setup_ui(self, layout) -> None:

        self.auto_synthetic_hifi_master_copy = SwitchSettingCard(icon=FluentIcon.GAME, title='高保真母盘')
        layout.addWidget(self.auto_synthetic_hifi_master_copy)

        self.auto_synthetic_source_ether_battery = SwitchSettingCard(icon=FluentIcon.GAME, title='以太电池')
        self.auto_synthetic_source_ether_battery.value_changed.connect(self._on_auto_synthetic_source_ether_battery_toggled)
        layout.addWidget(self.auto_synthetic_source_ether_battery)

        self.source_ether_battery_auto_synthetic_quantity = ComboBoxSettingCard(
            icon=FluentIcon.GAME, title='以太电池自动合成数量', options_enum=SourceEtherBatteryAutoSyntheticQuantity
        )
        layout.addWidget(self.source_ether_battery_auto_synthetic_quantity)

    def init_config(self) -> None:
        config: AutoSyntheticConfig = self.ctx.run_context.get_config(
            app_id=auto_synthetic_const.APP_ID,
            instance_idx=self.ctx.current_instance_idx,
            group_id=self.group_id,
        )
        self.auto_synthetic_hifi_master_copy.init_with_adapter(get_prop_adapter(config, 'hifi_master_copy'))
        self.auto_synthetic_source_ether_battery.init_with_adapter(get_prop_adapter(config, 'source_ether_battery'))
        self.source_ether_battery_auto_synthetic_quantity.init_with_adapter(get_prop_adapter(config, 'source_ether_battery_auto_synthetic_quantity'))

        # 初始化时根据当前配置设置可见性
        self._on_auto_synthetic_source_ether_battery_toggled(config.source_ether_battery)

    def _on_auto_synthetic_source_ether_battery_toggled(self, checked: bool) -> None:
        # 如果开启以太电池自动合成 启用相关控件 否则禁用
        visible = checked
        self.source_ether_battery_auto_synthetic_quantity.setEnabled(visible)