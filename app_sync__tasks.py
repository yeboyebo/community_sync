from YBUTILS import globalValues

from controllers.base.default.managers.task_manager import TaskManager

# from controllers.base.magento.drivers.magento import MagentoDriver
# from controllers.base.store.drivers.psql_store import PsqlStoreDriver

# from controllers.api.community.orders.controllers.egorders_download import EgOrdersDownload
from controllers.api.community.orders.controllers.cm_orders_post import CmB2COrdersPost
from controllers.api.community.products.controllers.community_products_upload import communityProductsUpload as communityProducts

sync_object_dict = {
    # "orders_download": {
    #     "sync_object": EgOrdersDownload,
    #     "driver": MagentoDriver
    # },
    "b2c_orders_post": {
        "sync_object": CmB2COrdersPost
    },
    "products_community_upload": {
        "sync_object": communityProducts
    }
}

task_manager = TaskManager(sync_object_dict)

globalValues.registrarmodulos()
cdDef = 10
