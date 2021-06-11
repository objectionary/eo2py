You can play with EOLANG here, in a few simple steps:

First, clone this repo to your local machine and go
to the `sandbox` directory (you will need
[Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
installed):

```bash
$ git clone https://github.com/cqfn/eo.git
$ cd eo/sandbox
```

Then, compile the code (you will need
[Maven 3.3+](https://maven.apache.org/)
and [Java SDK 8+](https://www.java.com/en/download/) installed):

```bash
$ mvn compile
```

Intermediary `*.xml` files will be generated in the `target` directory (it will
be created). Also, there will be `*.java` and `*.class` files. Feel free to analyze
them: EO is parsed into XML, then translated to Python.