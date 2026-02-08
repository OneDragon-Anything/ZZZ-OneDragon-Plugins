"""以太电池（电卡合成）插件常量定义。"""

# ============ 核心常量 (必需) ============
APP_ID = "ether_battery"
APP_NAME = "以太电池"
DEFAULT_GROUP = True  # True: 出现在一条龙列表, False: 不出现
NEED_NOTIFY = True  # 启用通知（开始/成功/失败）

# ============ 画面区域坐标 (1080p) ============
# 合成界面 - "合成素材不足" 文字区域
RECT_MATERIAL_SHORTAGE = (1235, 835, 1855, 975)
# 合成界面 - "合成" 按钮区域
RECT_SYNTHESIS_BUTTON = (1525, 995, 1855, 1065)

# ============ 插件元数据 (可选，用于 GUI 显示) ============
PLUGIN_AUTHOR = "Usagi-wusaqi"
PLUGIN_HOMEPAGE = "https://github.com/Usagi-wusaqi/zzz-onedragon-plugins"
PLUGIN_VERSION = "1.0.0"
PLUGIN_DESCRIPTION = "自动合成以太电池（电卡）的插件"
