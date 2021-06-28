# eo-python

![build](https://github.com/nikololiahim/eo-python/actions/workflows/maven.yml/badge.svg) [![codecov](https://codecov.io/gh/nikololiahim/eo-python/branch/main/graph/badge.svg?token=CuHSiScipH)](https://codecov.io/gh/nikololiahim/eo-python)

A Python implementation of [EO](https://github.com/cqfn/eo).

## This repository contains:
* Transcompiler
    * Maven plugin that applies XSL transformations to .eo programs and yields .py programs.
* Python runtime environment
    * Implementation of atoms and data objects as a [pip package](https://pypi.org/project/eo2py/).
* Examples of translated programs in `eo-python-runtime/tests/example_programs` as `pytest` unit tests.
* Sandbox to compile and execute your own EO programs! 
## How to use
Check out `README.md` in `sandbox` directory.


## Supported features:
* Abstraction
* Application in order of occurence of free attributes
* Decoration (nested decoration, free decoratees)
* Dataization
* Inner objects, both closed and abstract
* Varargs


## Unsupported features:
* Array literals (Implemented in Python API, not yet integrated into translator)
    * Workaround: arrays are available as varargs
     ``` 
     [items...] > array
       [i] > get
         get. > @
           items
           i
           
    array 1 2 3 4 5 > numbers
    numbers.get 4 > last
     ```
* Metas
* Constants (`!`)
* Memory atom
* Regexes
* Arbitrary partial application, argument labels
* $\varphi$ with free attributes
* Anonymous abstract objects (as arguments to copying)
* Maybe some more (whenever you experience a bug, feel free to submit an issue)





## Code mappings

### Abstraction

At the time of declaration, abstract and closed objects map to classes. In `__init__()` method, special (`@`, `$`, and `^`) attributes are created, and free attributes are initialized to `DataizationError()` ([more about this](#DataizationError)). Bound attributes become methods decorated with `@property`.
Projections of object and attribute names get prefixes `EO` and `attr_` correspondingly to avoid name collisions between user-defined and inner entities.

```=
[isbn] > book
  "Object Thinking" > title
```

```python=
class EObook(ApplicationMixin, Object):
    
    def __init__(self):
        self.attr__self = self # corresponds to `$`
        self.attr__parent = DataizationError() # corresponds to `^`
        self.attr__phi = DataizationError() # corresponds to `@`
        self.attr_isbn = DataizationError() # corresponds to `isbn`
        
        self.attributes = ["isbn", ]
    
    @property
    def attr_title(self):
        return (String("Object Thinking"))
```

#### Inner Objects 
Attribute might be tied to an abstract object. Our translation model utilizes class objects, and exploits `partial()` method defined in `functools` (Python standard library package) to specify $\rho$ a.k.a. `^` a.k.a. `attr__parent` object:
```=
[x y] > point
  [to] > distance
    length. > @
      vector
        to.x.sub (^.x)
        to.y.sub (^.y)
```


```python=
class EOpoint(ApplicationMixin, Object):

    def __init__(self):
        # omitted for brevity 
        self.attributes = ["x", "y", ]

    @property
    def attr_distance(self):
        return partial(EOpointEOdistance, self)
        

class EOpointEOdistance(ApplicationMixin, Object):

    def __init__(self, attr__parent):
        # omitted for brevity
        self.attributes = ["to", ]

    @property
    def attr__phi(self):
        return (Attribute(
                   (EOvector()
                       (Attribute((Attribute((self.attr_to), "x")), "sub")
                            (Attribute((self.attr__parent), "x")))
                       (Attribute((Attribute((self.attr_to), "y")), "sub")
                            (Attribute((self.attr__parent), "y")))),
                "length"))

```

### Decoration
Functionality of decoration is achieved via `attr__phi` attribute combined with class-wrapper `Attribute`.
Whenever specific attribute is needed, `dataize()` in `Attribute` searches for the attribute in object itself; upon failure recursively searches for it in object bound to `attr__phi`.

```=
[] > a
  "nothing else matters" > a_message

[] > b
  a > @
  
[] > c
  b.a_message > c_message
```

```python=
class EOa(ApplicationMixin, Object):
    
    def __init__(self):
        # special & free attributes handling
    
    @property
    def attr_a_message(self):
        return (String("nothing else matters"))
    

class EOb(ApplicationMixin, Object):
    
    def __init__(self):
        # special & free attributes handling
        
    @property
    def attr__phi(self):
        return (EOa())
        


class EOc(ApplicationMixin, Object):
    
    def __init__(self):
        # special & free attributes handling
    
    @property
    def attr_c_message(self):
        return (Attribute((EOb()), "a_message"))
```




### Application

Being a copy of objects in EO with some arguments, application is class instantiation in Python. Current implementation supports only full positional application (in absence of free attributes in decoratee) as overwritten `__call__()` methods. In order to apply some argument to an object you need to `__call__()` an object with this argument. `__call__()` return an object itself, which means that these 'applications' can be chained as follows:

```=
obj(arg1)(arg2)(arg3)...
```

The particular implementation of `__call__()` is injected into each `Object` with the `ApplicationMixin` class defined in [atoms.py](https://github.com/nikololiahim/eo-python/blob/main/eo-python-runtime/src/eo2py/atoms.py), whom all classes inherit from:

```=
[truth_value] > answer
  truth_value.if "yes" "no" > @
```

```python=
class EOanswer(ApplicationMixin, Object):
    
    def __init__(self):
        # special attributes
        
        self.attributes = ["truth_value", ]
    
    @property
    def attr__phi(self):
        return (Attribute((self.attr_truth_value), "if")
                   (String("yes"))
                   (String("no")))
```

#### Varargs
As per [EO paper](https://github.com/cqfn/eo/tree/master/paper), all the varargs are packaged into an `Array` atom and can be accessed by index using `get` attribute:

```=
[arg1, arg2, varargs...] > obj
  stdout > @
    sprintf
      "%d %d %d"
      get.
        varargs
        3
      arg1
      arg2
```

```python=
class EOobj(ApplicationMixin, Object):
    def __init__(self):
        # Free attributes
        self.attr__parent = DataizationError()
        self.attr__self = self

        self.attributes = ["arg1", "arg2", "varargs"]
        self.attr_arg1 = DataizationError()
        self.attr_arg2 = DataizationError()
        self.attr_varargs = Array()
        self.varargs = True

    @property
    def attr__phi(self):
        return Stdout()(
                   Sprintf()
                       (String("%d %d %d"))
                       (Attribute(self.attr_varargs, "get")
                           ((Number(3)))
                       (self.attr_arg1)
                       (self.attr_arg2)
        )

```


### Dataization
All classes (think, abstract object), both auto-generated and atomic, implement an `Object` interface with only one method - `dataize()`. This method is responsible for reducing a complex object to some `Atom` object. The `Atom` object, in turn, can not be dataized any further and will simply return itself whenever it receives a dataization request. 

```python=
class Atom(Object):

    def dataize(self):
        return self
        
    @abstractmethod
    def data(self):
        raise NotImplementedError()
```

You can query the actual data associated with the `Atom` object by calling its `data()` method. This method will return the actual Python data (`str`, `int`, `object` or `None`), whereas `dataize()` only returns an `Atom` object.

The dataization process can be summed up as follows:
* If an auto-generated `Object` is dataized, it returns `self.attr__phi.dataize()`
* If an atomic `Object` (e.g. `Attrubute`) is dataized, it returns some `Atom` based on its internal implementation, potentially with some side effects (`Stdout`).
* If an `Atom` is dataized, it returns itself.

If for some reason an object does not define `attr__phi` attribute, then its dataization would result in an `AttributeError`.

#### `DataizationError`
All the uninitialized free attributes are initialized as a special `DataizationError` object. As its name suggests, an attempt to `dataize()` it would yield a runtime exception in Python, resulting in immediate termination of the program. Attributes initialized with `DataizationError` are intended to be assigned some value at runtime.


<!-- ## Justification of design decisions -->
<!-- мне эта секция кажется немного лишней если честно, мне кажется что примеры говорят сами за себя
**bruh**
хм, ну ок, можно написать что у нас был итеративный дизайн, TDD и все такое, и что мы пришли к этим идеям путем проб и ошибок (как и было на самом деле)
да, там просто вот:
- Описать подход к реализации проекций, а также обоснование сделанных проектных решений - тоже краткий документ.
НУ КОНЕЧНО МОЖНО УБРАТЬ
если ему интересна мотивация, пусть предыдущий док читает


окей да.
кстати, когда будет с ним встреча????
з****? надо спросить
можно скинуть ридми и он призовется
лан, все, убираем эту секцию к 
е****? дададад, сегодня допишем и скинем сразу же
в polystat тоже можно скинуть, пусть посмотрят
да!
тупо пасхалка
ахаха
шизаа-->
<!-- The mapping abstract objects -> Python classes, closed objects -> Python objects seemed natural at first.
МБ убрать это вообще?

Free attributes - not in init, see application

Bound attributes decorated with @property to simulate declarative behavior (in particular, to avoid compile time recursion in creation of fibonacci objects)

Inner Objects -> existing parser

dataize() everywhere to account for "every object has a special $\delta$ attribute"
If obj does not have it, maybe 
 -->
<!--`Attribute` object exists for multiple reasons:
* It encapsulates attribute lookup logic, deferring the Python's default lookup mechanism. 
* 

Application as `__call__` methods — to ease translation in XSLT sheets

Special $\varphi$ attribute instead of inheritance mainly because of impossibility of dynamic inheritance in the latter approach
-->


## Further considerations

We are yet to come up with examples of:
* Partial application
* Application of abstract object
* Accessing the free attributes of decoratees (O_o)

If you have an example of programs using such constructs of EO, feel free to submit an issue, then we'll see what we can do about it. 

### A note on partial application
We are thinking of a different way to achieve functionality of the partial application other than object instantiation. The reason is that instantiation in Python makes an object out of class, which is  structurally different, whilst objects in EO, as a set, 'are closed' under operation of application.
So idea is to either work with objects or classes ([proof of concept drafts](https://gist.github.com/eyihluyc/c5f7c481ad6c97c5b8d131addba710ec) for classes)
