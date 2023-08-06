# ou-tm129-py
Python package for installing Python packages required for TM129

This repo is exploring how we might distribute Python packages to students via a single installable package.

A Python package can be "empty" other than requiring the presence of particular packages.

We can define multiple levels of requirement using `install_requires=[]` for necessary packages and `extras_require={}` for optional packages.

Optional package collections can be installed via eg `pip install .[jupyter,production]`, using `extras_require` dictionary keys for the additional package collections we want to install.

So for example, we could deliver:

- core packages that configure a base Python environment: `pip install PACKAGE`;
- core packages and packages that customise a Jupyter environment in a particular way: `pip install PACKAGE[jupyter]`;
- core packages and packages that customise a Jupyter environment in a particular way and provides additional packages for ALs: `pip install PACKAGE[jupyter,AL]`;
- core packages plus production / development packages: `pip install PACKAGE[dev]`;
- core packages plus packages required to customise an OU hosted environment: `pip install PACKAGE[ouhosted]`;
- etc.

We could also use a package to deliver payloads to the student desktop, either in terms of files or services. eg we could supply command line utilites, a simple webserver/homepage, or a data files via a Python package.

Using Package version numbers (or `extras_require`) we could easily manage slightly different package versions/distributions for different module presentations.

Using `pip install --upgrade PACKAGE` gives us a way of pushing updates to students.

Note that installing from repos is increasingly tricky to do; it's no longer supported from PyPi installed packages, so if things were only available from a (public) repo they'd have to be done manually. (We could provide a cli tool to do this, installed from the package; eg `tm129_utils install-extras` that runs a `pip git+...` set of installs.)

I'm not sure if [Python package namespaces](https://packaging.python.org/guides/packaging-namespace-packages/) are also relevant? These let you package separate distributions but under the same namespace. Eg we could have separate packages for different modules but all under the `ou` or `openuni` or `openuniversity` namespace? (So we'd have things like `from openuniversity import tm351` etc. and installed via `pip install openuni-tm351` or `pip install openuni-tm129==2020.10.1` or whatever (is there a restriction or limits on the version numbering convention? Does it have to be numeric? Inside a certain range?)

Identifying what packages can support an effective teaching and learning environment is an act of curation, and as such is somewhere where we can add value. By sharing environments that may be useful to others:

- we support folk in their own teaching and learning, work and play;
- we raise awareness of the OU and OU modules, getting a presence on PyPi, maybe using `ou` and course code identifiers in package names etc;
- if we ship useful commmand line utilities, they can occasionly print OU advertising messages when run...
- if we ship a a simple web server, it can include module marketing information, "are you read for..?" activities or even sample module content;
- if we bundle files in the package, these can be retrieved on the student desktop via a simple CLI command; (can we also get desktop shortcuts onto a desktop some how?)
- the same package could be used to easily support related OpenLearn content;
