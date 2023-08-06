from __future__ import annotations

from dataclasses import dataclass

from shiro.jwk import JsonWebKeySet

from guarani.models import Scope


@dataclass
class Configuration:
    issuer: str
    scopes: list[Scope]
    token_lifespan: int
    id_token_lifespan: int
    keyset: JsonWebKeySet
