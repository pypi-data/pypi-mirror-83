class NotFound(Exception):
    """Basic exception for errors raised by NotFounds"""
    obj = None

    def __init__(self, obj_name):
        super(NotFound, self).__init__('{} is not found: {}'.format(self.obj, obj_name))


class TopicNotFound(NotFound):
    obj = 'Topic'


class SubscriptionNotFound(NotFound):
    obj = 'Subscription'


class IdentifierRequiredException(Exception):
    pass
