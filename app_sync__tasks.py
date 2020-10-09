from YBUTILS import globalValues

from controllers.base.default.managers.task_manager import TaskManager
from controllers.base.magento.drivers.magento import MagentoDriver

from controllers.api.community.orders.controllers.cm_orders_post import CmB2COrdersPost
from controllers.api.community.orders.controllers.cm_orders_process import CmB2COrdersProcess
from controllers.api.community.products.controllers.community_products_upload import communityProductsUpload as communityProducts
from controllers.api.community.points.controllers.cm_points_post import CmB2CPointsPost
from controllers.api.community.points.controllers.cm_points_process import CmB2CPointsProcess
from controllers.api.community.refounds.controllers.cm_refounds_post import CmB2CRefoundsPost
from controllers.api.community.refounds.controllers.cm_refounds_process import CmB2CRefoundsProcess

sync_object_dict = {
    "b2c_orders_post": {
        "sync_object": CmB2COrdersPost
    },
    "b2c_orders_process": {
        "sync_object": CmB2COrdersProcess,
        "driver": MagentoDriver
    },
    "products_community_upload": {
        "sync_object": communityProducts
    },
    "b2c_points_post": {
        "sync_object": CmB2CPointsPost
    },
    "b2c_points_process": {
        "sync_object": CmB2CPointsProcess,
        "driver": MagentoDriver
    },
    "b2c_refounds_post": {
        "sync_object": CmB2CRefoundsPost
    },
    "b2c_refounds_process": {
        "sync_object": CmB2CRefoundsProcess,
        "driver": MagentoDriver
    }
}

task_manager = TaskManager(sync_object_dict)

globalValues.registrarmodulos()
cdDef = 10
