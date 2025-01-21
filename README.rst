deno_vm
========

.. image:: https://readthedocs.org/projects/deno-vm/badge/?version=latest
   :target: https://deno-vm.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status
   
.. image:: https://github.com/eight04/deno_vm/actions/workflows/test.yml/badge.svg
   :target: https://github.com/eight04/deno_vm/actions/workflows/test.yml
   :alt: test

A Python 3 to Deno + worker-vm binding, helps you execute JavaScript safely.

How it works
------------

The module launches a Deno REPL server, which can be communicated with JSON. All JavaScript code are encoded in JSON and sent to the server. After the server executing the code in vm, the result is sent back to Python.

Pre-requisites
--------------

Deno
^^^^

Follow the instruction here:
https://docs.deno.com/runtime/manual/getting_started/installation

Also make sure ``deno`` command works as expected:
https://docs.deno.com/runtime/manual/getting_started/installation#testing-your-installation

Installation
------------

.. code-block:: sh
   python -m venv .venv
   source .venv/bin/activate # change the script file based on your shell
   pip install deno_vm

Usage
-----

Most of the APIs are bound to `worker-vm <https://github.com/eight04/worker-vm>`__.

Simple eval with output log:

.. code-block:: python

   from deno_vm import eval
   print(eval('["foo", "bar"].join()'), console='inherit')

Use VM:

.. code-block:: python

   from deno_vm import VM
   
   with VM() as vm:
      vm.run("""
         var sum = 0, i;
         for (i = 0; i < 10; i++) sum += i;
      """)
      print(vm.run("sum"))

Use VM and VM Server with custom permissions:

.. code-block:: python

   from deno_vm import VM, VMServer

   with VMServer(permissions={"net": ["jsonplaceholder.typicode.com:443"]}) as vm_server:
      with VM(server=vm_server, permissions={"net": ["jsonplaceholder.typicode.com:443"]}) as vm:
         json = vm.run("fetch('https://jsonplaceholder.typicode.com/todos/1').then(res => res.json());")
         print(json) 
         # {'userId': 1, 'id': 1, 'title': 'delectus aut autem', 'completed': False}
      
It is possible to do async task with Promise:

.. code-block:: python

   from datetime import datetime
   from deno_vm import VM

   js = """
   function test() {
      return new Promise(resolve => {
         setTimeout(() => {
            resolve("hello")
         }, 3000);
      });
   };
   """
   with VM() as vm:
      vm.run(js)
      print(datetime.now())
      print(vm.call("test"))
      print(datetime.now())

API reference
-------------

http://deno_vm.readthedocs.io/

For contributors
----------------

Run tests
^^^^^^^^^

.. code-block:: sh

   python -m unittest -v test

Changelog
---------

- next (Jan 21, 2024)

   - Feat: add `permissions` options when creating `VMServer()` (parent thread) and `VM()` (Deno Worker).

- 0.6.0 (Mar 4, 2024)

   - Change: use `--unstable-worker-options` instead of `--unstable`.
   - Change: vendor deno dependencies. Now `deno_vm` doesn't require network and filesystem write access.
   - Fix: suppres cleanup error.
   - Fix: improve uninitialized error message.

-  0.5.1 (Oct 10, 2023)

   -  Fix: unable to pass initial code to ``VM()``.

-  0.5.0 (Oct 10, 2023)

   -  Switch to `deno_vm`.

