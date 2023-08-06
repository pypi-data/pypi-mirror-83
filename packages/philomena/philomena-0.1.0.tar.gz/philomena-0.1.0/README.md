# How to use:

The Orchestrator
----------------

Write simple tests with the orchestrator:
```
# import Orchestrator
from philomena import Orchestrator

# instantiate a orchestrator object
orchestrator = Orchestrator()

# visit a page
orchestrator.visit("https://www.google.com")
```

Just by calling `.visit()` we issue a test. If the page returns something
other than a 200 OK HTTP status code a `UnexpectedHTTPStatusCode` is raised.

We can expect something else as well however:
```
from philomena import Orchestrator

orchestrator = Orchestrator()

# this is not a page where we expect a 200
# instead we expect a 404 page not found
orchestrator.visit("https://www.googkaflsfdjkle.com", expected=404)
```

A host can be set, if for instance you want to test only a single website:
```
from philomena import Orchestrator

orchestrator = Orchestrator(host="https://www.mywebsite.com/")

# then instead we can pass a relative url
orchestrator.visit("/home")
orchestrator.visit("/login")
```

The Page
--------

We can also check the contents of what are returned:
```
from philomena import Orchestrator

orchestrator = Orchestrator()

# the Orchestrator returns a Page object
page = orchestrator.visit("https://www.google.com")

# we can check things are in the page
assert "Google" in page
```
