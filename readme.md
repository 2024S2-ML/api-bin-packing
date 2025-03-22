# Running the project

First create a venv

```bash

    python -m venv .venv

```

Then activate the .venv

```bash

    source .venv/bin/activate

```
Install requirements.txt

```bash

    pip install -r requirements.txt

```

After setting the environment, let`s setup the DB

```bash

    python populate.py

```

The last step it's just run the main

```bash

    python main.py

```