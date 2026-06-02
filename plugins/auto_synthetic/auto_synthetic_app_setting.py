from one_dragon_qt.services.app_setting.app_setting_provider import (
    AppSettingProvider,
    SettingType,
)
from .auto_synthetic_const import APP_ID


class AutoSyntheticAppSetting(AppSettingProvider):
    app_id = APP_ID                             # 从 const 模块导入
    setting_type = SettingType.FLYOUT       # 或 SettingType.FLYOUT

    @staticmethod
    def get_setting_cls() -> type:
        from .auto_synthetic_setting_flyout import AutoSyntheticSettingFlyout    # 惰性导入，避免循环引用
        return AutoSyntheticSettingFlyout