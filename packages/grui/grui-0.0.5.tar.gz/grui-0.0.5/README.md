# Grui

Generated Rest User Interface

This package allow developer to expose function to the web. GRUI will generate a Rest API from the class.
An HTTP page will also be generated. The main idea is to focus the code on the functionality. 

## Code examples 
```python
from typing import *

from grui import AbstractGruiService
from grui.decorator import *

class MySuperService(AbstractGruiService):
    """The documentation will be available to end user.

    Longer description will be display into the help page of the service.
    """

    @Get("my-super-path")
    @NotFoundIfEmpty  # Set the http return code to 404 if it return None. 
    def get_all(self) -> Optional[List[int]]:
        """The method documentation is display to the user as well"""
        return self.whatever
```

## Issues/Bug report or improvement ideas
https://gitlab.com/olive007/grui/-/issues

## License
GNU Lesser General Public License v3 or later (LGPLv3+)
