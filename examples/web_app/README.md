A very simple React and FastAPI web application using aiobungie's REST client only.

This doens't have to be a React app. You can use it with any language/framework you want but this is the easiet.

# App structure.
- Typescript and React frontend.
- Python and FastAPI backend with RESTClient.

## How this app works.
We proxy our backend rest server with the react app in `package.json` so we can make requests to it.

Flow.

```
React request +----> Rest client request --> JSON response +----> View Data.
```

Since all requests returns JSON objects we serialize them in our react app and view them.

# Install

```sh
pip install -r requirements.txt
```

In `frontend` directory, run.

```
yarn install
```

# Running
Run `python launcher.py`