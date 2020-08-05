from YBUTILS import globalValues

from controllers.base.default.managers.task_manager import TaskManager

from controllers.api.community.orders.controllers.cm_orders_post import CmB2COrdersPost
from controllers.api.community.orders.controllers.cm_orders_process import CmB2COrdersProcess
from controllers.api.community.products.controllers.community_products_upload import communityProductsUpload as communityProducts

sync_object_dict = {
    "b2c_orders_post": {
        "sync_object": CmB2COrdersPost
    },
    "b2c_orders_process": {
        "sync_object": CmB2COrdersProcess
    },
    "products_community_upload": {
        "sync_object": communityProducts
    }
}

task_manager = TaskManager(sync_object_dict)

globalValues.registrarmodulos()
cdDef = 10
