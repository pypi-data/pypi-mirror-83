# Python Stream Machine API client driver

This library can be used to package events into a serialization format of choice, and sends them to the Stream Machine Gateway.


## Releasing to PyPi and Test PyPi

For now, we release without a Gitlab CI. We should create that soon though. In the `Makefile`, there are two commands:
- `make release`: release to prod PyPi
- `make release-test`: release to test PyPi

When running either commands, you're prompted for a username and password. We're not using the actual username and password, but an API token (see LastPass for users PyPi and Test PyPi, as well as the release/prod API token). When using an API token, fill out the following:
- `username` = `__token__`
- `password` = `<api_token>` (including `pypi-` part)
