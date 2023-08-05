from .panels.csrf_multi_scheme import CSRFMultiSchemeDebugPanel


def includeme(config):
    """
    Pyramid API hook
    """
    config.add_debugtoolbar_panel(CSRFMultiSchemeDebugPanel)
