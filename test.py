#! python3

from io import StringIO
from unittest import TestCase, main
from unittest.mock import patch

from deno_vm import eval, VM, VMError, VMServer


class Main(TestCase):
    def test_eval(self):
        with self.subTest("one line eval"):
            r = eval("'foo' + 'bar'")
            self.assertEqual(r, "foobar")

        with self.subTest("multiline"):
            r = eval(
                """
                var foo = x => x + 'bar';
                foo('foo');
            """
            )
            self.assertEqual(r, "foobar")

    def test_VM(self):
        with self.subTest("create VM"):
            vm = VM().create()
            r = vm.run("'foo' + 'bar'")
            vm.destroy()
            self.assertEqual(r, "foobar")

        with self.subTest("with statement"):
            with VM() as vm:
                r = vm.run("'foo' + 'bar'")
                self.assertEqual(r, "foobar")

        with self.subTest("with statement and code"):
            with VM("function test() {return 'ok'}") as vm:
                r = vm.call("test")
                self.assertEqual(r, "ok")

    def test_VMError(self):
        with self.assertRaisesRegex(VMError, "foo"):
            eval("throw new Error('foo')")

        # doesn't inherit Error
        with self.assertRaisesRegex(VMError, "foo"):
            eval("throw 'foo'")

    def test_console(self):
        code = "var test = s => console.log(s)"
        with VM(console="inherit") as vm:
            vm.run(code)
            with patch("sys.stdout", new=StringIO()) as out:
                vm.call("test", "Hello")
                self.assertEqual(out.getvalue(), "Hello\n")

        with VM(console="redirect") as vm:
            vm.run(code)
            vm.call("test", "Hello")
            event = vm.event_que.get_nowait()
            self.assertEqual(event["value"], "Hello")

    def test_executable_missing(self):
        with self.assertRaises(VMError) as cm:
            with VMServer("non-exists-executable-node"):
                pass

        self.assertTrue(
            "'non-exists-executable-node' is unavailable" in str(cm.exception)
        )

    def test_freeze_object(self):
        result = eval("Object.freeze({foo: {}})")
        self.assertEqual(result, {"foo": {}})

    def test_random_number(self):
        a = eval("Math.random()")
        b = eval("Math.random()")
        self.assertIsInstance(a, float)
        self.assertTrue(0 <= a < 1)
        self.assertNotEqual(a, b)

    def test_init_error(self):
        with self.assertRaisesRegex(VMError, "not created yet"):
            vm = VM("foo = 1; bar = () => foo; null")
            # vm.create()
            self.assertEqual(vm.call("bar"), 1)
            # vm.destroy()

    def test_location(self):
        # in deno location is not writable
        a = eval("var location = {protocol: 'https:'}; location.protocol")
        self.assertNotEqual(a, "https:")

        a = eval("const location = {protocol: 'https:'}; location.protocol")
        self.assertEqual(a, "https:")

    def test_permissions_prompting(self):
        with self.assertRaisesRegex(VMError, "Invalid value type for"):
            with VMServer(permissions={"net": "jsonplaceholder.typicode.com:443"}):
                pass

        with self.assertRaisesRegex(VMError, "List values must be strings for"):
            with VMServer(
                permissions={"net": ["jsonplaceholder.typicode.com:443", True]}
            ):
                pass

    def test_network_permission(self):
        with self.assertRaisesRegex(
            VMError,
            'NotCapable: Requires net access to "jsonplaceholder.typicode.com:443", run again with the --allow-net flag',
        ):
            eval('fetch("https://jsonplaceholder.typicode.com/todos/1");')

        with self.assertRaisesRegex(
            VMError,
            "Can't escalate parent thread permissions",
        ):
            with VMServer() as vm_server:
                with VM(
                    server=vm_server,
                    permissions={"net": ["jsonplaceholder.typicode.com:443"]},
                ) as vm:
                    vm.run("fetch('https://jsonplaceholder.typicode.com/todos/1')")

        with self.assertRaisesRegex(
            VMError,
            'NotCapable: Requires net access to "jsonplaceholder.typicode.com:443", run again with the --allow-net flag',
        ):
            with VMServer(
                permissions={"net": ["jsonplaceholder.typicode.com:443"]}
            ) as vm_server:
                with VM(
                    server=vm_server,
                ) as vm:
                    vm.run("fetch('https://jsonplaceholder.typicode.com/todos/1')")

        with VMServer(
            permissions={"net": ["jsonplaceholder.typicode.com:443"]}
        ) as vm_server:
            with VM(
                server=vm_server,
                permissions={"net": ["jsonplaceholder.typicode.com:443"]},
            ) as vm:
                json = vm.run(
                    "fetch('https://jsonplaceholder.typicode.com/todos/1').then(res => res.json());"
                )

                self.assertEqual(
                    json,
                    {
                        "completed": False,
                        "id": 1,
                        "title": "delectus aut autem",
                        "userId": 1,
                    },
                )


if __name__ == "__main__":
    main()
