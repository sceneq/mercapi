import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Dict, Any

from mercapi.requests import RequestData


@dataclass
class SearchRequestData(RequestData):
    class ShippingMethod(Enum):
        SHIPPING_METHOD_ANONYMOUS = 1
        SHIPPING_METHOD_JAPAN_POST = 2
        SHIPPING_METHOD_NO_OPTION = 3

    class Status(Enum):
        STATUS_ON_SALE = 1
        STATUS_SOLD_OUT = 2
        # STATUS_TRADING = 3

    @dataclass
    class SearchConditions:
        query: str
        categories: List[int] = field(default_factory=list)
        brands: List[int] = field(default_factory=list)
        sizes: List[int] = field(default_factory=list)
        price_min: int = 0
        price_max: int = 0
        item_conditions: List[int] = field(default_factory=list)
        shipping_payer: List[int] = field(default_factory=list)
        colors: List[int] = field(default_factory=list)
        shipping_methods: List["SearchRequestData.ShippingMethod"] = field(
            default_factory=list
        )
        status: List["SearchRequestData.Status"] = field(default_factory=list)
        sort_: str = field(default_factory=str)
        order: str = field(default_factory=str)

    search_conditions: SearchConditions
    page_token: Optional[str]

    @property
    def data(self) -> Dict[str, Any]:
        shipping_methods = [i.name for i in self.search_conditions.shipping_methods]
        status = [i.name for i in self.search_conditions.status]
        if "STATUS_SOLD_OUT" in status:
            status.extend("STATUS_TRADING")

        return {
            "userId": "",
            "pageSize": 120,
            "pageToken": self.page_token or "",
            "searchSessionId": uuid.uuid4().hex,
            "indexRouting": "INDEX_ROUTING_UNSPECIFIED",
            "thumbnailTypes": [],
            "searchCondition": {
                "keyword": self.search_conditions.query,
                "excludeKeyword": "",
                "sort": self.search_conditions.sort_,
                "order": self.search_conditions.order,
                "status": [],
                "sizeId": self.search_conditions.sizes,
                "categoryId": self.search_conditions.categories,
                "brandId": self.search_conditions.brands,
                "sellerId": [],
                "priceMin": self.search_conditions.price_min,
                "priceMax": self.search_conditions.price_max,
                "itemConditionId": self.search_conditions.item_conditions,
                "shippingPayerId": self.search_conditions.shipping_payer,
                "shippingFromArea": [],
                "shippingMethod": shipping_methods,
                "colorId": self.search_conditions.colors,
                "hasCoupon": False,
                "attributes": [],
                "itemTypes": [],
                "skuIds": [],
            },
            "defaultDatasets": [],
            "serviceFrom": "suruga",
        }
