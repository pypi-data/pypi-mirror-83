Hemlock-Demographics is a <a href="https://dsbowen.github.io/hemlock/" target="_blank">hemlock</a> extension which allows you to add demographics items to a hemlock project.

## Installation

With hemlock-CLI (recommended):

```
$ hlk install hemlock-demographics
```

With pip:

```
$ pip install hemlock-demographics
```

## Quickstart

```python
from hemlock import Branch, Page, Label, route
from hemlock_demographics import comprehensive_demographics

@route('/survey')
def start():
    return Branch(
        comprehensive_demographics(page=True),
        Page(
            Label('<p>The end.</p>'), 
            terminal=True
        )
    )
```

## Citation

Hemlock-Demographics is based largely on the demographics section of the [World Values Survey](http://www.worldvaluessurvey.org/).

```
@software{bowen2020hemlock-demographics,
  author = {Dillon Bowen},
  title = {Hemlock-Demographics},
  url = {https://dsbowen.github.io/hemlock-demographics/},
  date = {2020-10-05},
}

@dataset{inglehart2014wvs,
    author = {Inglehart, R., and C. Haerpfer, and A. Moreno, and C. Welzel, and K. Kizilova, and J. Diez-Medrano, and M. Lagos, and P. Norris, and E. Ponarin and B. Puranen and et al.},
    title={World Values Survey: Round Six},
    url = {http://www.worldvaluessurvey.org/},
    date = {2014.}
}
```

## License

Users must cite this package in any publications which use it.

It is licensed with the MIT [License](https://github.com/dsbowen/docstr-md/blob/master/LICENSE).