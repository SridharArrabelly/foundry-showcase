"""Required integration bindings. There is deliberately no direct-model fallback."""

import os
import re
from dataclasses import dataclass
from urllib.parse import parse_qs, urlparse


@dataclass(frozen=True)
class Settings:
    project_endpoint: str
    model_connection: str
    toolbox_endpoint: str
    memory_enabled: bool

    @classmethod
    def from_environment(cls) -> "Settings":
        canonical = os.environ.get("FOUNDRY_PROJECT_ENDPOINT", "").strip()
        legacy = os.environ.get("AZURE_AI_PROJECT_ENDPOINT", "").strip()
        if canonical and legacy and canonical.rstrip("/") != legacy.rstrip("/"):
            raise ValueError("Foundry project endpoint bindings disagree.")
        project = (canonical or legacy).rstrip("/")
        if not project:
            raise ValueError("Missing integration binding: AZURE_AI_PROJECT_ENDPOINT")
        names = ("VOLT_MODEL_CONNECTION", "TOOLBOX_ENDPOINT")
        values = {name: os.environ.get(name, "").strip() for name in names}
        missing = [name for name, value in values.items() if not value]
        if missing:
            raise ValueError(f"Missing integration bindings: {', '.join(missing)}")
        for name, value in (("project endpoint", project), ("TOOLBOX_ENDPOINT", values["TOOLBOX_ENDPOINT"])):
            parsed = urlparse(value)
            if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
                raise ValueError(f"{name} must be an HTTPS URL without embedded credentials.")
        if not urlparse(project).hostname.endswith(".services.ai.azure.com"):
            raise ValueError("The project endpoint must be a Microsoft Foundry service.")
        if not re.fullmatch(r"[A-Za-z0-9_-]+", values["VOLT_MODEL_CONNECTION"]):
            raise ValueError("VOLT_MODEL_CONNECTION must identify one managed gateway connection.")
        toolbox = urlparse(values["TOOLBOX_ENDPOINT"])
        if (
            not values["TOOLBOX_ENDPOINT"].startswith(project + "/toolboxes/")
            or not re.search(r"/toolboxes/[^/]+/versions/[^/]+/mcp$", toolbox.path)
            or parse_qs(toolbox.query).get("api-version") != ["v1"]
        ):
            raise ValueError("Pin a toolbox version from the same Foundry project.")
        enabled = os.environ.get("VOLT_MEMORY_ENABLED", "false").strip().lower()
        if enabled not in ("true", "false"):
            raise ValueError("VOLT_MEMORY_ENABLED must be true or false.")
        return cls(project, values["VOLT_MODEL_CONNECTION"], values["TOOLBOX_ENDPOINT"], enabled == "true")
