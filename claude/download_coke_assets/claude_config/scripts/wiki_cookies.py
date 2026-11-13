# /// script
# requires-python = ">=3.10"
# dependencies = ["browser-cookie3", "pycryptodomex"]
# ///
"""Extract wiki.corp.adobe.com cookies from Chrome for use by wiki scripts."""
import browser_cookie3


def get_cookie_header():
    """Return a Cookie header string for wiki.corp.adobe.com from Chrome."""
    cj = browser_cookie3.chrome(domain_name="wiki.corp.adobe.com")
    parts = [f"{c.name}={c.value}" for c in cj]
    return "; ".join(parts)


if __name__ == "__main__":
    print(get_cookie_header())
