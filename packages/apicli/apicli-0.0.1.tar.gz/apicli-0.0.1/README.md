# ApiCli

> ApiCli is a python library that allow using a common code-base to create a REST API and a CLI that can interact with your API.

## TODOs

- Create endpoint from route defined using decorators
- Propose at least bearer authentication from API side
- Expose API endpoints to manage authentication when enabled
- Define commands to authenticate from CLI

## Contribute

Install project dependencies using pipenv. This will install apicli in editable mode from local folder.
```
pipenv install
```

If you want to test generated openapi documentation, you can use swagger-ui.

- If `swagger-ui/` submodule is empty, init submodule using this command
```
git submodule update --init
```

- Then in `swagger-ui/` folder, install dependencies and run web interface with command
```
npm run dev
```
*By default, swagger-ui will be served at http://localhost:3200*

- If you want UI to automatically open the specs from your local apicli server, edit `swagger-ui/dev-helpers/index.html`
