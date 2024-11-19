# Authenticating External Services for LangChain in Python

An example Python app demonstrating how to integrate Pangea's [Vault][] service
to authenticate with external services.

## Prerequisites

- Python v3.12 or greater.
- pip v24.2 or [uv][] v0.5.2.
- A [Pangea account][Pangea signup] with Vault enabled.
- An [OpenAI API key][OpenAI API keys] stored in Vault. Save the ID of the Vault
  item for later.

## Setup

```shell
git clone https://github.com/pangeacyber/python-service-authn.git
cd python-service-authn
```

If using pip:

```shell
python -m venv .venv
source .venv/bin/activate
pip install .
```

Or, if using uv:

```shell
uv sync
source .venv/bin/activate
```

## Usage

```
Usage: python -m service_authn [OPTIONS] PROMPT

Options:
  --vault-item-id TEXT  The item ID of the OpenAI API key item in Pangea
                        Vault.  [required]
  --vault-token SECRET  Pangea Vault API token. May also be set via the
                        `PANGEA_VAULT_TOKEN` environment variable.  [required]
  --pangea-domain TEXT  Pangea API domain. May also be set via the
                        `PANGEA_DOMAIN` environment variable.  [default:
                        aws.us.pangea.cloud; required]
  --model TEXT          OpenAI model.  [default: gpt-4o-mini; required]
  --help                Show this message and exit.
```

This example fetches the OpenAI API key from Vault and uses it to authenticate
with the OpenAI API to generate chat completions.

```
$ python -m service_authn --vault-item-id pvi_1234567890 "What is MFA?"
```

[Vault]: https://pangea.cloud/docs/vault/
[Pangea signup]: https://pangea.cloud/signup
[OpenAI API keys]: https://platform.openai.com/api-keys
[uv]: https://docs.astral.sh/uv/
