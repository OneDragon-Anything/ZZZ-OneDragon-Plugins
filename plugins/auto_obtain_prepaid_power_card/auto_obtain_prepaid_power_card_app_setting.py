from one_dragon_qt.services.app_setting.app_setting_provider import (
    AppSettingProvider,
    SettingType,
)
from .auto_obtain_prepaid_power_card_const import APP_ID


class AutoObtainPrepaidPowerCardAppSetting(AppSettingProvider):
    app_id = APP_ID                             # 从 const 模块导入
    setting_type = SettingType.FLYOUT       # 或 SettingType.FLYOUT

    @staticmethod
    def get_setting_cls() -> type:
        from .auto_obtain_prepaid_power_card_setting_flyout import AutoObtainPrepaidPowerCardSettingFlyout    # 惰性导入，避免循环引用
        return AutoObtainPrepaidPowerCardSettingFlyout
