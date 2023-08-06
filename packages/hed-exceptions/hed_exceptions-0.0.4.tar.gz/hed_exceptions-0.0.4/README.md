# hed_exceptions

Set of custom exceptions aimed to reduce typing.


## Details

I wander why Python is lacking similar builtin types...


## Catalog

* ArgumentError
    
        def charge(me):
            raise ArgumentError("me")
            
        def recharge(me):  
            raise ArgumentError("me", "Plug not found!")
        ...
        charge("money") 
        # ArgumentError('Bad arg!', Arg(name='me', type=<class 'str'>, value='money'))
        ...
        recharge("battery")
        # ArgumentError('Plug not found!', Arg(name='me', type=<class 'str'>, value='battery'))


## Dependencies

- None


## Installation

    pip install hed_exceptions
