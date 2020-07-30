
# @class_declaration community_sync #
class community_sync(flsyncppal):

    def community_sync_get_customer(self):
        return "community"

    def __init__(self, context=None):
        super().__init__(context)

    def get_customer(self):
        return self.ctx.community_sync_get_customer()

