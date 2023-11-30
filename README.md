# LLM Field Extraction API

Extract fields from product descriptions using a (mocked) LLM.

## Available features

1. You can summon either model (`camellm` or `llama` as defined [here](https://github.com/vjern/ml-soft-eng/blob/master/src/extractor.py#L20)) with the `POST /extract` endpoint;
2. You can provide multiple products to extract from (each with its own `fields_to_extract` list);
3. Prompt generation using the model's prompt template and inclusion of examples by drawing from `examples.json`;
4. Extraction tasks (1 description + 1 field) are parallelised using a thread pool (supposing we are actually hitting another service hosting the LLM).

To see the prompts that were built & sent to the LLM, you can add the header `X-Debug-Show-Prompts` to requests sent to `POST /extract`. The prompt will be returned alongside `field_value`. They're returned as lists of strings for readability.

## Repo structure

All code is in `src` and assumes it to be the working directory of the API.

`http` contains HTTP request examples. You can run them against a hostname with various IDE extensions (eg [VS Code Rest Client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client), it's like a very lean Postman).

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

Check that your server is live by visiting http://localhost:8080.

```http
GET /
```

### Extract fields

```htt
POST /extract
Content-Type: application/json

{
    "model": "camellm",
    "products": [
        {
            "description": "Lave linge 142x142cm",
            "fields_to_extract": [
                "EF000040", "EF000008"
            ]
        }
    ]
}
```

## Adding examples to prompts

When building a prompt to extract field `f_id` from a product description, we sample examples from `examples.json` to populate the prompt with examples, e.g. for field `EF000040`:

<details>

<summary> Example prompt </summary>

```
<s>[INST] <<SYS>>
Tu es un assistant qui m'aide à extraire des valeurs depuis un produit.
<</SYS>>

Product description: Radiateur eau chaude REGGANE 3000 STANDARD Type 22S, horizontal blanc, hauteur 400mm , largeur 2700mm, puissance   3493,8 W
Attribute: hauteur (cm)
Answer: 400

Product description: Regg. 3010 Int. 11KV 900x1000, Puissance 1292W (Blanc: RAL9016)
Attribute: hauteur (cm)
Answer: 900

Product description: Série 500 Réfrigérateur Combiné Encastrable niche 1780 mm (L : 546 mm)-Classe E-Froid statique & Congélateur Low Frost - Bac à légumes avec contrôle d`humidité-Compartiment basse température-4 clayettes-Installation glissières - 34dB -Blanc
Attribute: hauteur (cm)
Answer: 1780

Product description: Baignoire d'angle Geberit Bastia avec pieds: 142x142cm
Attribute: hauteur (cm)
Answer: [/INST]
```

</details>

Note that we only use succesful examples (where a value was found for the field) though there would probably be a case to be made about having failed examples so the LLM knows it can return an empty answer as well.

## Addressing the bonus criteria

### Provide multiple products and get the results as list of lists

The initial implementation took a list of products and returned a list of the same size with a mapping `field => value` added to each product.

Parallelising `Extractor.extract` calls which today only take one product and one field to extract meant breaking the results down into atomic `(product, field_value)` tuples. We could always group back these by product (eg by assigning an id to the product, and grouping the output of `tpe.map` on it rather than the raw description) before returning them.

### Extracting multiple attributes in a single prompt

We could probably add more complex examples where we provide field metas (eg options) and answers for each one of the `n` fields to extract, e.g.

```
### User Message
Product description: Radiateur eau chaude REGGANE 3000 STANDARD Type 22S, horizontal blanc, hauteur 400mm , largeur 2700mm, puissance   3493,8 W
Attributes: hauteur (cm), largeur (cm)
Answers: 400, 2700
```

The more fields we want to extract at the same time, the more we would probably dilute the LLM's ability to infer the relationship between the initial description and the answers it needs to find, so there is a trade-off to be made. We may need more examples to compensate, which would get us closer to the context size limit.

### Implementing Chain of Thought

How to cut an existing example into logical propositions ? Not sure how to go about that right now. The behavior would probably have to differ for each field type and whether it involves extra steps like unit conversions.
