# LLM Field Extraction API

Extract fields from product descriptions using a (mocked) LLM.

## Repo structure

All code is in `src` and assumes it to be the working directory of the API.

`http` contains HTTP request examples. You can run them against a hostname with various IDE extensions (eg [VS Code Rest Client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client)).

## Build & Run

This API is shipped with a Dockerfile.

You can build the Docker image & run it in a local container with:

```sh
make dev
# service is reachable on localhost:8080
# will stream logs
```

and also:

```sh
make logs # to show the full logs
make kill # stop the container
```

Or you can run the API directly with live reload (requires a virtual env):

```sh
make live
```

Then you can hit the following endpoints:

## Endpoints

Or check the examples in [http](http) (to be run with [VS Code Rest Client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client)).

### Liveness

Check that your container is live by visiting http://localhost:8080.

```http
GET /
```

### Extract fields

```htt
POST /extract
Content-Type: application/json

{
    "models": "camellm",
    "tasks": [
        {
            "product_description": "Lave linge 142x142cm",
            "fields_to_extract": [
                "EF000032", "EF00042"
            ]
        }
    ]
}
```
