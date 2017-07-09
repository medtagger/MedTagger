Backend API
-----------

Repository contains code for backend API written in Python.

### How to setup dev instance?
Requirements:
- Linux (recommended Ubuntu) / macOS
- Python 3.6
- Virtualenv
- Make

**WARNING!:** *Windows has not been tested yet. Feel free to check it out.*

On Linux it's really easy to setup your environment:
1. Clone this repository.
2. Use `make venv` to setup your virtual environment.
3. Activate your environment with `. venv/bin/activate`.

That's all!

### Testing your code
Use `make test` to test your code. It will run PyLint, Flake8 and PyTest
 with all of our unit tests. The same thing happen in GitLab CI, so make
 sure that your code is properly linted and tested!
