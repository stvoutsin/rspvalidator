# RSP Validator

RSP Validator is a Python project designed to validate the Rubin Science Platform (RSP). It includes automated tests for various RSP components using Playwright for browser automation.

## Project Structure

- `src/`: Contains the source code for the project.
  - `rspvalidator/`: Main package for the project.
    - `config.py`: Configuration file for the project.
    - `models/`: Contains data models used in the project.
    - `services/`: Contains service classes for various functionalities.
    - `tests/`: Contains test cases for validating RSP functionalities.

## Requirements

- Handled via tox

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/stvoutsin/rspvalidator.git
    cd rspvalidator
    ```

2. Install `tox`:
    ```sh
    pip install tox
    ```

## Configuration

Set the following environment variables as needed:

- `HOSTNAME`: The hostname for the RSP instance (default: `data-dev.lsst.cloud`).
- `HEADLESS`: Run browser in headless mode (`true` or `false`, default: `false`).
- `TOKEN`: Authentication token for accessing RSP.

## Setup Authentication

This library uses an auth.json configuration file that stores the cookies needed to access the protected RSP pages.
To generate an auth.json file the first time is a bit of a hassle, but it can be done either manually or using playwright.
To use playwright to generate it, run:
    ```sh
    playwright codegen  https://data-dev.lsst.cloud --save-storage=auth.json
    ```
Then point AUTH_FILE in config.py to the path of the auth.json file generated.

## Running Tests

To run the tests using `tox` (Only available in HEADLESS mode), use the following command:
```sh
tox

Note: A recently added feature is to compare snapshots taken during a particular test. This is currently enabled for a portal test & a squareone test.
To enable this part of the test you'll need to set the environment variable SNAPSHOTS = True
If this is enabled, the first time you run the tests, the snapshots will be generated and stored in a directory in the test directory, but the test will fail with a message indicating this. 
You'll then have to run the tests a second time to actually test and compare properly
