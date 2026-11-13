import json
from pathlib import Path

from hp3p import realism
from hp3p.openai_client import TEXT_MODEL
from hp3p.reference_blue import attachments
from hp3p.scap import FIELDS, ScapProfiles, digest, save

POLICY = "scap-adaptive-background-v3-semantic-environment-explicit-no-statistics-fallback-v1"
GATES = {
    "No relevant same-product environment cohort",
    "User prompt has no supported environment; do not silently borrow a cohort",
}
FALLBACK_DIRECTION = """
EXPLICIT USER-APPROVED NO-STATISTICS FALLBACK:
No supported same-product environment cohort was retrieved. Do not invent,
borrow or claim statistics, component frequencies, density assessments or
retrieved decor. CURRENT_SCENE is the existing Stage B scene, not a statistical
enrichment. Preserve its components and their placements. Apply the same
text-only realism direction to its existing surfaces and lighting only.
Return only scene/look/conflicts and realism_plan. Statistics omission records
are fixed by code and are not material to the image prompt.
"""


class FallbackProfiles(ScapProfiles):
    def __init__(self, path):
        super().__init__(path, realism=True)
        self.identity.update(
            policy=POLICY, fallback_instructions_sha256=digest(FALLBACK_DIRECTION.encode()),
            fallback_implementation_sha256=digest(Path(__file__).read_bytes()),
        )

    def select(self, prompt, category, selection=None):
        if (not isinstance(selection, dict)
                or set(selection) != {"environment", "prompt_quote", "reason"}
                or any(not isinstance(value, str) or not value.strip() for value in selection.values())):
            raise ValueError("Invalid semantic environment selection")
        if selection["prompt_quote"] not in prompt:
            raise ValueError("Environment evidence is not an exact original user prompt quote")
        try:
            return super().select(prompt, category, selection)
        except ValueError as exc:
            if str(exc) not in GATES:
                raise
            family = {"laptop": "Laptop", "printer": "Printer", "monitor": "Monitor"}.get(category)
            if family is None:
                raise ValueError("No matching statistics product family") from exc
            allowed = {p["environment"] for p in self.profiles}
            from hp3p.scap import ENVIRONMENTS

            allowed.update(name for name, _ in ENVIRONMENTS)
            if selection["environment"] not in allowed | {"unsupported"}:
                raise ValueError("Unknown semantic environment label") from exc
            return {
                "statistics_disabled": True, "family": family,
                "requested_environment": selection["environment"], "matched_environment": None,
                "exact_environment_match": False, "match_reason": str(exc),
                "original_user_prompt": prompt, "environment_selection": selection, "fields": {},
                "cohort_n": None, "cohort_original_n": None, "cohort_added_n": None,
                "fallback_policy": POLICY,
                "fallback_reason": "User approved a clearly labelled no-statistics fallback.",
            }

    def rewrite(self, client, context, system, text, images, out):
        if not context.get("statistics_disabled"):
            return super().rewrite(client, context, system, text, images, out)
        base = json.loads((out / "scap_base_writing_response.json").read_text())
        audit = {
            "stats_usage": [],
            "stats_omissions": [{"group": group, "reason": context["fallback_reason"]} for group in FIELDS],
            "background_density": {
                "level": "not_assessed", "reason": "No statistical density assessment was made.",
                "existing_components": [], "additions": [],
                "omission_reason": "No cohort retrieved; preserve Stage B components without additions.",
            },
        }
        approved = {**{key: base[key] for key in ("scene", "look", "conflicts")}, **audit}
        schema = {
            "type": "object", "additionalProperties": False,
            "required": ["scene", "look", "conflicts"],
            "properties": {key: {"type": "string"} for key in ("scene", "look", "conflicts")},
        }
        schema = realism.rewrite_schema(schema)
        system += "\n\n" + realism.INSTRUCTIONS + "\n\n" + FALLBACK_DIRECTION
        text += "\n\nCURRENT_SCENE:\n" + json.dumps(approved)
        text += "\n\nREALISM_DIRECTION:\n" + realism.REALISM_DIRECTION
        save(out / "realism_rewrite_request.json", {
            "model": TEXT_MODEL, "system": system, "text": text, "schema": schema,
            "images": attachments(images), "max_retries": 0, **self.identity,
            "statistics_disabled": True,
        })
        response = {**client.chat_json(system, text, images, schema), **audit}
        realism.validate_rewrite(response, approved)
        save(out / "realism_rewrite_response.json", response)
        save(out / "no_statistics_fallback.json", context)
        return response
