from __future__ import annotations

import sys
from typing import Any, cast, override

import click
from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletionChunk
from pangea import PangeaConfig
from pangea.services import Vault
from pangea.services.vault.models.common import ItemType
from pydantic import SecretStr

load_dotenv(override=True)


class SecretStrParamType(click.ParamType):
    name = "secret"

    @override
    def convert(self, value: Any, param: click.Parameter | None = None, ctx: click.Context | None = None) -> SecretStr:
        if isinstance(value, SecretStr):
            return value

        return SecretStr(value)


SECRET_STR = SecretStrParamType()


@click.command()
@click.option(
    "--vault-item-id",
    type=str,
    required=True,
    help="The item ID of the OpenAI API key item in Pangea Vault.",
)
@click.option(
    "--vault-token",
    envvar="PANGEA_VAULT_TOKEN",
    type=SECRET_STR,
    required=True,
    help="Pangea Vault API token. May also be set via the `PANGEA_VAULT_TOKEN` environment variable.",
)
@click.option(
    "--pangea-domain",
    envvar="PANGEA_DOMAIN",
    default="aws.us.pangea.cloud",
    show_default=True,
    required=True,
    help="Pangea API domain. May also be set via the `PANGEA_DOMAIN` environment variable.",
)
@click.option("--model", default="gpt-4o-mini", show_default=True, required=True, help="OpenAI model.")
@click.argument("prompt")
def main(
    *,
    prompt: str,
    vault_item_id: str,
    vault_token: SecretStr,
    pangea_domain: str,
    model: str,
) -> None:
    # Fetch OpenAI API key from Pangea Vault.
    vault = Vault(token=vault_token.get_secret_value(), config=PangeaConfig(domain=pangea_domain))
    vault_result = vault.get_bulk({"id": vault_item_id}, size=1).result
    assert vault_result
    assert vault_result.items[0].type == ItemType.SECRET
    openai_api_key = vault_result.items[0].item_versions[-1].secret
    assert openai_api_key

    # Generate chat completions.
    openai = OpenAI(api_key=openai_api_key)
    stream = openai.chat.completions.create(messages=({"role": "user", "content": prompt},), model=model, stream=True)
    for chunk in stream:  # type: ignore[assignment]
        for choice in cast(ChatCompletionChunk, chunk).choices:
            sys.stdout.write(choice.delta.content or "")
            sys.stdout.flush()

        sys.stdout.flush()

    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
