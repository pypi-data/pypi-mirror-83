# PyPlating
PyPlating is a Python3 templating library with support for nesting.

## Templates

All commands for PyPlating are wrapped in double curly braces: `{{such and such}}`

In order to have double curly braces in your input data be ignored by PyPlating, simply use backslash character prefixes: `\{{not a command\}}`

### Simple Replacements

Assuming a substitution "such and such" is defined (either via Python or via the method described in the section below), the following will be replaced: `{{such and such}}`

### Replacements w/ Arguments

Substitutions can be invoked with a set of arguments (`name=value` pairs separated by `&` characters) in the following format (in this example `name` is invoked with `x` equal to `such and such` and `y` equal to `so and so`): `{{name:x=such \& such&y=so \& so}}`

Arguments to a substitution will shadow any existing definitions of the same name previously defined.

Arguments can also include replacement instructions within them: `{{name:x=this \& that&y={{nested}} and what not}}`

## Python

Usage of the PyPlating is centred primarily around the `Collection` class:

```
import pyplating
c = pyplating.Collection(debug=True)
```

With a `Collection` instance, one can now define some substitutions:

```
c.add("something", "some text and {{in file:arg=this and that}}")
c.addByFile("in file", "directory/file.txt")
```

These substitutions can now be applied to some input text:

```
c.evaluate("input text {{something}}")
c.evaluateByFile("directory/subdir/file.txt")
```

