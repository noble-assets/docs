<p align="center"><img src="./static/img/logo.svg" width="256" /></p>

<h1 align="center">Noble Chain Documentation</h1>

### Installation

```sh
$ bun
```

### Local Development

```sh
$ bun start
```

This command starts a local development server and opens up a browser window. Most changes are reflected live without having to restart the server.

### Build

```sh
$ bun build
```

This command generates static content into the `build` directory and can be served using any static contents hosting service.

### Updating The Module References

This repository is set up to track the concrete used Noble (and its modules) version and make any required changes to the existing documentation
based on new changes in the repositories.
For this purpose, there is a Python script, that retrieves the latest Mainnet upgrade version from the contained list of upgrades
and checks for the last updated version of the docs.
If there is a mismatch, the diff between the Noble repository tags is retrieved and prompted to an LLM to generate a list of required changes
to this repository.
