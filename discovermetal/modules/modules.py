class DiscoverModule(object):
    pass


def discovery_modules():
    return DiscoverModule.__subclasses__()
