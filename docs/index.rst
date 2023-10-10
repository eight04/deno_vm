.. automodule:: deno_vm
   :show-inheritance:

   deno_vm API reference
   =====================

   A Python 3 to Deno + vm binding, helps you execute JavaScript safely.
   
   Also checkout the `readme <https://github.com/eight04/deno_vm>`_.
   
   Functions
   ---------
   
   .. autofunction:: eval
   
   Classes
   -------
   
   .. autoclass:: BaseVM
      :members: __enter__, __exit__, create, destroy
   
   .. autoclass:: VM
      :members: run, call, event_que
   
   .. autoclass:: VMServer
      :members: __enter__, __exit__, start, close
   
