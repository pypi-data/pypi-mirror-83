# openai-python

_Python library and CLI for interfacing with the OpenAI API_

## Editing ##

Ensure that any code you add is compatible with both python2 and python3.
In most cases, this can be accomplished with adding the following at the top of a new python file:
```
from __future__ import absolute_import, division, print_function
```

## Publishing ##

When ready to publish changes to the package, run the following commands from the root directory:
1. `make build`
2. `make upload`

*note: you will only be able to publish changes if you have proper pypi permissions — @gdb is the admin*
