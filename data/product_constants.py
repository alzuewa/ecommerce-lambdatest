from enum import StrEnum


class ProductName(StrEnum):
    IPOD_NANO = 'iPod Nano'
    MACBOOK = 'Macbook'
    PALM_TREO_PRO = 'Palm Treo Pro'


class AvailableProductId(StrEnum):
    IPOD_NANO = '36'
    MACBOOK = '43'
    PALM_TREO_PRO = '29'


class UnvailableProductId(StrEnum):
    PALM_TREO_PRO = '29'
