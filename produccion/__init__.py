# Django app initialization

# Define __all__ to make the model available at the package level
__all__ = ['ConsumoEnergia']

def __getattr__(name):
    # Lazy loading of the ConsumoEnergia model to avoid circular imports
    if name == 'ConsumoEnergia':
        from .consumo_energia import ConsumoEnergia as _ConsumoEnergia
        return _ConsumoEnergia
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
