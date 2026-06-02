"""自动获取储值电卡插件配置。"""

from enum import Enum

from one_dragon.base.config.config_item import ConfigItem
from one_dragon.base.operation.application.application_config import ApplicationConfig

from . import auto_obtain_prepaid_power_card_const


class OutpostLogisticsObtainNumber(Enum):
    """后勤商店获取数量选项。"""

    ALL = ConfigItem('全部', 9)
    ONE = ConfigItem('1个', 0)
    TWO = ConfigItem('2个', 1)
    THREE = ConfigItem('3个', 2)
    FOUR = ConfigItem('4个', 3)
    FIVE = ConfigItem('5个', 4)
    SIX = ConfigItem('6个', 5)
    SEVEN = ConfigItem('7个', 6)
    EIGHT = ConfigItem('8个', 7)
    NINE = ConfigItem('9个', 8)


class MonthlyRestockObtainNumber(Enum):
    """情报板商店获取数量选项。"""

    ALL = ConfigItem('全部', 4)
    ONE = ConfigItem('1个', 0)
    TWO = ConfigItem('2个', 1)
    THREE = ConfigItem('3个', 2)
    FOUR = ConfigItem('4个', 3)


class FadingSignalObtainNumber(Enum):
    """信号残响获取数量选项。"""

    ALL = ConfigItem('全部', 19)
    ONE = ConfigItem('1个', 0)
    TWO = ConfigItem('2个', 1)
    THREE = ConfigItem('3个', 2)
    FOUR = ConfigItem('4个', 3)
    FIVE = ConfigItem('5个', 4)
    SIX = ConfigItem('6个', 5)
    SEVEN = ConfigItem('7个', 6)
    EIGHT = ConfigItem('8个', 7)
    NINE = ConfigItem('9个', 8)
    TEN = ConfigItem('10个', 9)
    ELEVEN = ConfigItem('11个', 10)
    TWELVE = ConfigItem('12个', 11)
    THIRTEEN = ConfigItem('13个', 12)
    FOURTEEN = ConfigItem('14个', 13)
    FIFTEEN = ConfigItem('15个', 14)
    SIXTEEN = ConfigItem('16个', 15)
    SEVENTEEN = ConfigItem('17个', 16)
    EIGHTEEN = ConfigItem('18个', 17)
    NINETEEN = ConfigItem('19个', 18)


class AutoObtainPrepaidPowerCardConfig(ApplicationConfig):
    """自动获取储值电卡插件配置类。"""

    def __init__(self, instance_idx: int, group_id: str) -> None:
        ApplicationConfig.__init__(
            self,
            instance_idx=instance_idx,
            app_id=auto_obtain_prepaid_power_card_const.APP_ID,
            group_id=group_id,
        )

    @property
    def outpost_logistics(self) -> bool:
        """是否启用后勤商店。"""
        return self.get('outpost_logistics', False)

    @outpost_logistics.setter
    def outpost_logistics(self, value: bool) -> None:
        self.update('outpost_logistics', value)

    @property
    def monthly_restock(self) -> bool:
        """是否启用情报板商店。"""
        return self.get('monthly_restock', False)

    @monthly_restock.setter
    def monthly_restock(self, value: bool) -> None:
        self.update('monthly_restock', value)

    @property
    def fading_signal(self) -> bool:
        """是否启用信号残响。"""
        return self.get('fading_signal', False)

    @fading_signal.setter
    def fading_signal(self, value: bool) -> None:
        self.update('fading_signal', value)

    @property
    def outpost_logistics_obtain_number(self) -> int:
        """后勤商店获取数量。"""
        return self.get('outpost_logistics_obtain_number', OutpostLogisticsObtainNumber.ALL.value.value)

    @outpost_logistics_obtain_number.setter
    def outpost_logistics_obtain_number(self, value: int) -> None:
        self.update('outpost_logistics_obtain_number', value)

    @property
    def monthly_restock_obtain_number(self) -> int:
        """情报板商店获取数量。"""
        return self.get("monthly_restock_obtain_number", MonthlyRestockObtainNumber.ALL.value.value)

    @monthly_restock_obtain_number.setter
    def monthly_restock_obtain_number(self, value: int) -> None:
        self.update('monthly_restock_obtain_number', value)

    @property
    def fading_signal_obtain_number(self) -> int:
        """信号残响获取数量。"""
        return self.get("fading_signal_obtain_number", FadingSignalObtainNumber.ALL.value.value)

    @fading_signal_obtain_number.setter
    def fading_signal_obtain_number(self, value: int) -> None:
        self.update('fading_signal_obtain_number', value)