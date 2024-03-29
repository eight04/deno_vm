from xcute import cute, LiveReload
	
cute(
	pkg_name = "deno_vm",
	lint = [
		'cd {pkg_name}/vm-server && deno task test && cd ..',
		'pylint {pkg_name}'
	],
	test = ['lint', 'python test.py', 'readme_build'],
	bump_pre = 'test',
	bump_post = ['dist', 'release', 'publish', 'install'],
	dist_pre = 'x-clean build dist',
	dist = 'python -m build',
	release = [
		'git add .',
		'git commit -m "Release v{version}"',
		'git tag -a v{version} -m "Release v{version}"'
	],
	publish = [
		'twine upload dist/*',
		'git push --follow-tags'
	],
	publish_err = 'start https://pypi.python.org/pypi/{pkg_name}/',
	install = 'pip install -e .',
	readme_build = [
		'rst2html5.py --no-raw --exit-status=1 --verbose '
			'README.rst | x-pipe build/readme/index.html'
	],
	readme_pre = "readme_build",
	readme = LiveReload("README.rst", "readme_build", "build/readme"),
	doc_build = "sphinx-build docs build/docs",
	doc_pre = "doc_build",
	doc = LiveReload(["{pkg_name}", "docs"], "doc_build", "build/docs")
)
