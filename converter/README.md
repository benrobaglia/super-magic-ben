# Converter DApp

Converter is a simple DApp written in Python that performs text transformations on strings, returning the result as a notice.
The DApp receives a JSON string as input, containing both the string to be converted and the transformation to be performed on it.

This DApp receives as input a JSON string in the following format:

```json
{ "transform": "upper", "message": "hello from cartesi" }
```

Where `message` indicates the text to be converted, and `transform` specifies the operation to be performed on it.
Valid values for `transform` are `upper`, `lower`, `capitalize`, `reverse`, `alternate` or `random`.

## Interacting with the application

We can use the [frontend-console](../frontend-console) application to interact with the DApp.
Ensure that the [application has already been built](../frontend-console/README.md#building) before using it.

First, go to a separate terminal window and switch to the `frontend-console` directory:

```shell
cd frontend-console
```

Then, send an input as follows:

```shell
yarn start input send --payload '{"transform": "upper", "message": "hello from cartesi"}'
```

In order to verify the notices generated by your inputs, run the command:

```shell
yarn start notice list
```

The response should be something like this:

```json
[{ "epoch": "0", "input": "1", "notice": "0", "payload": "HELLO FROM CARTESI" }]
```

## Running the back-end in host mode

When developing an application, it is often important to easily test and debug it. For that matter, it is possible to run the Cartesi Rollups environment in [host mode](../README.md#host-mode), so that the DApp's back-end can be executed directly on the host machine, allowing it to be debugged using regular development tools such as an IDE.

This DApp's back-end is written in Python, so to run it in your machine you need to have `python3` installed.

The next step is to run the converter back-end in your machine. The application is written in Python, so you need to have `python3` installed.

In order to start the converter back-end, run the following commands in a dedicated terminal:

```shell
cd converter/
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
ROLLUP_HTTP_SERVER_URL="http://127.0.0.1:5004" python3 converter.py
```

This will run the converter back-end and send the corresponding notices to port `5004`.
It can optionally be configured in an IDE to allow interactive debugging using features like breakpoints.

You can also use a tool like [entr](https://eradman.com/entrproject/) to restart the back-end automatically when the code changes. For example:

```shell
ls *.py | ROLLUP_HTTP_SERVER_URL="http://127.0.0.1:5004" entr -r python3 converter.py
```

After the back-end successfully starts, it should print an output like the following:

```log
INFO:__main__:HTTP rollup_server url is http://127.0.0.1:5004
INFO:__main__:Sending finish
```

After that, you can interact with the application normally [as explained above](#interacting-with-the-application).