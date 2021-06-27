You can play with EOLANG here, in a few simple steps:

First, clone this repo to your local machine and go
to the `sandbox` directory (you will need
[Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
installed):

```bash
$ git clone https://github.com/nikololiahim/eo-python.git
$ cd eo-python/sandbox
```

Then you are going to need to setup the Python virtual environment (`venv`) which will execute the generated Python code.
This can be done by running `setup_python_env.sh`:
```bash
$ ./setup_python_env.sh
```
This script will:
* Create a Python virtual environment in the `venv` directory.
* `pip install` all the necessary dependencies ([`eo2py`](https://pypi.org/project/eo2py/) and [`black`](https://github.com/psf/black) to format the code)
* `activate` the virtual environment

Then, compile the code (you will need
[Maven 3.3+](https://maven.apache.org/)
and [Java SDK 8+](https://www.java.com/en/download/) installed):

```bash
$ ./run.sh
```
This script will:
* Run `eo2py-maven-plugin` configured in the `pom.xml` of this repository
* Format the resulting `.py` files with `black`
* Dataize object `EOapp` from `app.eo.py` and print the result

Intermediary `*.xml` files will be generated in the `target` directory (it will
be created). Also, there will be `.py` files in `target/generated-sources` folder. Feel free to analyze
them: EO is parsed into XML by [eo-parser v0.1.25](https://mvnrepository.com/artifact/org.eolang/eo-parser), then translated to Python.
