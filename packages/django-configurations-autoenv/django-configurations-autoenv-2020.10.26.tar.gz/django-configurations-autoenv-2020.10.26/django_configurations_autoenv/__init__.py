import os

from configurations import Configuration, values

TRUE_VALUES = ['yes', 'y', 'true', '1']
FALSE_VALUES = ['no', 'n', 'false', '0']


def getvalue(k):
    v = os.getenv(k)
    if v in TRUE_VALUES:
        return True
    if v in FALSE_VALUES:
        return False
    if ',' in v:
        return list(filter(None, v.split(',')))
    return v


class AutoenvMixin:

    @classmethod
    def setup(cls):
        super(AutoenvMixin, cls).setup()
        for k in os.environ.keys():
            name = k.replace('DJANGO_', '')
            if k.find('DJANGO_') >= 0 and not hasattr(cls, name):
                setattr(cls, name, getvalue(k))


class AutoenvConfiguration(Configuration):
    pass
