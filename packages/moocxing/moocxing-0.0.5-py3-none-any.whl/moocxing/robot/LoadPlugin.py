import pkgutil
from moocxing.robot import constants

def loadPlugin(SKILL):
    _plugins_query = []
    nameSet = set()
    locations = [
        constants.PLUGIN_PATH
    ]

    for finder, name, ispkg in pkgutil.walk_packages(locations):
        loader = finder.find_module(name)
        mod = loader.load_module(name)

        if not hasattr(mod, 'Plugin'):
            continue

        plugin = mod.Plugin(SKILL)

        if plugin.SLUG in nameSet:
            continue

        nameSet.add(plugin.SLUG)
        _plugins_query.append(plugin)
        print(f"{plugin.SLUG}插件加载成功")

    return _plugins_query