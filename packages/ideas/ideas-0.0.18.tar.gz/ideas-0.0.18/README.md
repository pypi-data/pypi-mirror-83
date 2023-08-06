# ideas

## *Ideas: making it easier to extend Python’s syntax.*

![ideas logo](https://raw.githubusercontent.com/aroberge/ideas/master/ideas.png)


## Documentation

[Everything you need will eventually be found here](https://aroberge.github.io/ideas/docs/html/).

## Installation

```
python -m pip install ideas
```

## Dependencies

Python 3.6+ and [token-utils](https://github.com/aroberge/token-utils).
token-utils used to be included with ideas but has since been made into
its own (single module) package.


## Alternatives

Reading Andrew Barnert's post [Hacking Python without hacking Python](http://stupidpythonideas.blogspot.com/2015/06/hacking-python-without-hacking-python.html)
is a quick way to find out about various ways to use import hooks to
change Python's syntax.

## Usage

Suppose that you want to use `function` as a keyword in Python, to mean
the same thing as `lambda`, enabling you to write

```python
# my_program.py

square = function x: x**2
print(f"{square(4)} is the square of 4.")
```

You can do this using an import hook.
The simplest (but flawed) way to create such an import hook with `ideas`
would be as follows:

```python
from ideas import import_hook

def transform(source, **kwargs):
    return source.replace("function", "lambda")

import_hook.create_hook(transform_source=transform)
```

Then, you'd need to use it. Since there is already an example import hook
that does this, we'll use it instead.  All you have to do
is instruct Python to add your import hook and it will be used
from that point on. Something like the following.

```python
# Lets's call this 'loader.py'

from ideas.examples import function_keyword
function_keyword.add_hook()

import my_program
```

and then run

```
python loader.py
```

So, `my_program.py` , and any other module that could be
loaded by it would recognize that `function` is a valid alternative to `lambda`.

Many more examples can be found in the [documentation](https://aroberge.github.io/ideas/docs/html/), including a better way to create such an import hook and information about
a console (REPL) that supports code transformations.


## Tools

This project uses [black](https://black.readthedocs.io/en/stable/) for formatting,
[pytest](https://docs.pytest.org/en/latest/) for running tests,
and [flake8](https://flake8.pycqa.org/en/latest/) for linting with custom
settings compatible with black.

## Contact

You can either file an issue or email me at <Andre.Roberge@gmail.com>.


## License

MIT


## Infrequently asked questions, comments and answers

As I write (and occasionally update) this README file, nobody else knows
about this project. So, it is impossible for there to be some Frequently Asked
Questions.  In their absence, the following imaginary dialogue has been written.

> _Why?_

Because it is fun. If this is not enough of a justification for you, have a look at
[motivation](https://aroberge.github.io/ideas/docs/html/motivation.html)
which contains a longer, and possibly more serious answer.

> _Is it safe to use in production code?_

No.

> _But your example works perfectly well in my code; can I use it in my
> project?_

I don't think you should if your project is to be used by anyone else
but yourself.

> _I found a bug._

Wonderful, please file an issue so that I can attempt to fix it. Note however
that some examples are just proof of concepts and are not meant to be robust.

> _Can I contribute code for a new example?_

Yes, please, by all means. But I suggest that you first create an issue that gives
an overview of what you wish to accomplish.

> _I found a cool use of import hooks in another project, different from
> all of your examples. Could you include it?_

Please, give me the details and I will see if I can **easily** include
a similar example and if I think it is worthwhile to do so.

> _I think that the explanation you have written for X could be improved upon._

Please tell me more by filing an issue first and possibly creating a pull-request afterwards.

> _I have an idea for a new example, but do not know how to write the code for it._

First, make sure you go through all of the existing examples to confirm that
none can easily be adapted to do what you want.
If that is the case, file an issue ...
but please don't be offended if I don't write code for it
and end up closing the issue: I already have too many ideas of my own
for this project, too many other projects, and not
enough time to do all that I want.

That being said, I do like tinkering with import hooks ...

> _In file X.py, you do not respect convention Y from PEP-8. This is unacceptable
> in a Python project._

**Seriously?**  This project is all about exploring potential changes
to Python's syntax, some of which are downright crazy, and you complain
about a PEP-8 violation? ...

Ok, perhaps you can tell me and it might make sense to change what I wrote.

> _People from the Python-ideas mailing lists mentioned that I should look
> at this project for my idea, but I don't know where to start._

Please, have a look at the [documentation](https://aroberge.github.io/ideas/docs/html/).
If you go through all the examples in the order that they are presented, you
might learn how to implement your idea.

> What about something like `from __future__ import braces`?

**No.** See [Examples that will never be included](https://aroberge.github.io/ideas/docs/html/excluded.html).

> _You're no fun. Anyway, why this silly name for a project?
> The word "ideas" has nothing to do with import hooks in Python._

For this project, I was thinking of using `importhook` (singular) or
`importhooks` (plural). However, there is already a project named
`importhook` on Pypi and I thought that using the plural form would
likely be just too confusing.

I settled on `ideas` as I am guessing that the main application would be
for people to try out suggestions from or for
[python-ideas](https://mail.python.org/archives/list/python-ideas@python.org/).
A few days later, I came up with the above image and this cemented my
highly subjective opinion that this choice of name might not such a bad idea.

Anyway, enough of this banter. If you want to know more about this project,
please consult the [documentation](https://aroberge.github.io/ideas/docs/html/).
