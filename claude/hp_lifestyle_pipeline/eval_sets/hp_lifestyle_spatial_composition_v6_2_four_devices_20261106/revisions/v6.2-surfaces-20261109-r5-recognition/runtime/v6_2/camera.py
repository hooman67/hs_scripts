"""Resolve registered camera tags without name-based guesses or object quotas."""
from copy import deepcopy


def resolve_camera(registry, tag):
    if (not isinstance(registry, dict) or not isinstance(registry.get("version"), str)
            or not isinstance(registry.get("profiles"), list)
            or not isinstance(registry.get("aliases", {}), dict)):
        raise ValueError("malformed camera registry")
    if not isinstance(tag, str) or not tag.strip():
        raise ValueError("camera_tag must be a nonempty registered tag")
    profiles = {}
    for profile in registry.get("profiles", []):
        if (not isinstance(profile, dict)
                or any(not isinstance(profile.get(k), str) or not profile[k].strip()
                       for k in ("tag", "device_family", "framing", "elevation", "people_policy"))
                or not isinstance(profile.get("guidance"), list)
                or not profile["guidance"]
                or any(not isinstance(g, str) or not g.strip() for g in profile["guidance"])):
            raise ValueError("malformed camera profile")
        key = profile["tag"].casefold()
        if key in profiles:
            raise ValueError("duplicate camera profile")
        if any(k in profile for k in ("max_local_props", "max_background_details")):
            raise ValueError("V6 camera registry must not contain numeric scene limits")
        profiles[key] = profile
    aliases = {}
    for alias, destination in registry.get("aliases", {}).items():
        if not isinstance(alias, str) or not isinstance(destination, str):
            raise ValueError("malformed camera alias")
        key, canonical = alias.casefold(), destination.casefold()
        if canonical not in profiles or (key in profiles and key != canonical) or (key in aliases and aliases[key] != canonical):
            raise ValueError("invalid or colliding camera alias")
        aliases[key] = canonical
    key = tag.strip().casefold()
    profile = profiles.get(aliases.get(key, key))
    if not profile or profile["framing"] not in ("tight", "medium", "wide"):
        raise ValueError("unsupported camera tag or unreviewed preset")
    return {"requested_tag": tag, "resolved_tag": profile["tag"], "registry_version": registry["version"],
            **{k: deepcopy(profile[k]) for k in ("device_family", "framing", "elevation", "people_policy", "guidance")}}
