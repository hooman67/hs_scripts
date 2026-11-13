import requests  # type: ignore[import-untyped]
from datetime import datetime, timezone
import argparse
import sys
import os
import csv

# --- SETTINGS ---
# Kalshi market data comes from the public Trading API (no auth required for market data):
# - Prod: https://api.elections.kalshi.com/trade-api/v2
# - Demo: https://demo-api.kalshi.co/trade-api/v2
KALSHI_API_ROOT = os.environ.get("KALSHI_API_ROOT", "https://api.elections.kalshi.com/trade-api/v2")

# Kalshi `notional_value_dollars` is not a useful “total traded volume” field (often constant).
# The most practical proxy available in GetMarkets is `volume` (contracts) or `open_interest`.
MIN_VOLUME_CONTRACTS = 30_000  # interpreted as min `volume` (contracts)

# "Stable Favorite" band (defaulting to your stricter sweet spot)
TARGET_NO_PRICE_MIN = 0.55
TARGET_NO_PRICE_MAX = 0.85

# Time windows
SEVEN_DAY_CENTER_HOURS = 7 * 24
SEVEN_DAY_TOLERANCE_HOURS = 8        # 7 days +/- 8 hours
FOUR_HOUR_CENTER_HOURS = 4
FOUR_HOUR_TOLERANCE_HOURS = 0.5      # 4 hours +/- 30 mins

# Bankroll + Kelly sizing
# Note: This is a mathematical sizing helper, not financial advice.
BANKROLL_USD = 1_000
KELLY_FRACTION = 0.25  # "Quarter-Kelly" to reduce risk vs full Kelly
P_WIN_7DAY = 0.89
P_WIN_4H = 0.95
P_WIN_DEFAULT = 0.89  # conservative default for watchlist items

# If nothing is in the strict 7-day/4-hour windows right now, print a "watchlist" of
# candidates that already match your edge filters and are resolving soon.
WATCHLIST_MAX_DAYS_LEFT = 365
WATCHLIST_MAX_RESULTS = 25

# Stability proxy: Gamma doesn't expose full price history here, but it *does* give 1-day change.
# This approximates "flat line for last 24h" (tweak to be stricter/looser).
STABLE_MAX_ABS_1D_CHANGE = 0.03

# Category filtering via event tags (best-effort; tweak as desired)
# Default behavior: EXCLUDE sports/sports-related markets by tags.
SPORTS_TAG_SLUGS = {
    "sports",
    "nfl",
    "nba",
    "nhl",
    "mlb",
    "soccer",
    "football",
    "basketball",
    "hockey",
    "tennis",
    "golf",
    "ufc",
    "mma",
    "boxing",
    "fifa-world-cup",
    "world-cup",
    "super-bowl",
    "stanley-cup",
    "cfb",
    "college-football",
    "ncaa-football",
    "national-championship",
    "cfb-playoffs",
    "afc",
    "nfc",
}
# ----------------


def _parse_float(value, default=None):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _parse_dollars_str(value, default=0.0) -> float:
    """
    Kalshi often returns dollar fields as strings like "0.5600".
    """
    if value is None:
        return default
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value)
        except ValueError:
            return default
    return default


def _mid_price_from_bid_ask_cents(bid: int | None, ask: int | None) -> float | None:
    """
    Convert Kalshi bid/ask in cents (0-100) to a probability-like price in [0,1].
    Returns None if both sides are missing/0.
    """
    b = bid if isinstance(bid, int) else None
    a = ask if isinstance(ask, int) else None
    if b is not None and b > 0 and a is not None and a > 0:
        return (b + a) / 200.0
    if a is not None and a > 0:
        return a / 100.0
    if b is not None and b > 0:
        return b / 100.0
    return None


def _kalshi_url(market_ticker: str | None, event_ticker: str | None) -> str:
    # Kalshi’s web URLs can vary; provide best-effort links.
    if market_ticker:
        return f"https://kalshi.com/markets/{market_ticker}"
    if event_ticker:
        return f"https://kalshi.com/markets/{event_ticker}"
    return ""


def _kelly_fraction_for_binary(price: float, p_win: float) -> float:
    """
    Kelly fraction for a binary bet with payout 1 if it wins else 0,
    where `price` is the cost to buy 1 share (stake per $1 payout).

    If you buy 1 share at price p:
      - Win profit = 1 - p
      - Lose profit = -p
      - Decimal odds = 1/p
      - b = odds - 1 = (1/p) - 1
    Kelly: f* = (b*p_win - (1-p_win)) / b
    """
    if price <= 0 or price >= 1:
        return 0.0
    b = (1.0 / price) - 1.0
    q = 1.0 - p_win
    f = (b * p_win - q) / b
    # Clamp to sane range
    return max(0.0, min(1.0, f))


def _format_tags(tag_slugs: set[str], *, preferred_only: bool) -> str:
    if not tag_slugs:
        return "(none)"
    # Show a short, stable preview of tags
    preview = sorted(tag_slugs)
    if len(preview) > 8:
        preview = preview[:8] + ["..."]
    return ", ".join(preview)


def _is_sports_related(tag_slugs: set[str]) -> bool:
    """
    Best-effort: exclude markets that are clearly sports/sports-adjacent.
    We check both explicit slugs and common substrings used in sports tags.
    """
    if not tag_slugs:
        return False
    if tag_slugs & SPORTS_TAG_SLUGS:
        return True
    keywords = (
        "sport",
        "nfl",
        "nba",
        "nhl",
        "mlb",
        "soccer",
        "football",
        "basketball",
        "hockey",
        "tennis",
        "golf",
        "ufc",
        "mma",
        "boxing",
        "fifa",
        "world-cup",
        "super-bowl",
        "stanley-cup",
        "championship",
        "playoffs",
        "ncaa",
        "cfb",
        "afc",
        "nfc",
    )
    return any(any(k in slug for k in keywords) for slug in tag_slugs)


def screen_markets(
    *,
    ignore_category: bool = False,
    ignore_volume: bool = False,
    ignore_no_only: bool = False,
    ignore_time: bool = False,
    csv_path: str | None = None,
):
    run_ts = datetime.now(timezone.utc).isoformat()

    csv_fieldnames = [
        "run_ts_utc",
        "page",
        "cursor",
        "ticker",
        "event_ticker",
        "kalshi_url",
        "title",
        "subtitle",
        "end_date_iso",
        "hours_left",
        "volume_usd",
        "no_price",
        "yes_price",
        "target_side",
        "target_price",
        "one_day_price_change",
        "tags",
        # criteria inputs
        "min_volume_usd",
        "target_price_min",
        "target_price_max",
        "stable_max_abs_1d_change",
        "watchlist_max_days_left",
        # criteria flags (for spreadsheet sorting/filtering)
        "passed_volume",
        "passed_price_band",
        "passed_stability_proxy",
        "passed_category",
        "sports_related",
        "passed_time_constraints",
        # run mode flags
        "flag_c_ignore_category",
        "flag_v_ignore_volume",
        "flag_n_ignore_no_only",
        "flag_t_ignore_time",
        # sizing
        "p_win_used",
        "kelly_full_fraction",
        "kelly_fractional",
        "bankroll_usd",
        "stake_usd",
        "shares",
    ]

    def csv_append_rows(rows: list[dict]):
        if not csv_path or not rows:
            return
        os.makedirs(os.path.dirname(csv_path) or ".", exist_ok=True)
        file_exists = os.path.exists(csv_path)
        with open(csv_path, "a", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=csv_fieldnames, extrasaction="ignore")
            if not file_exists:
                w.writeheader()
            w.writerows(rows)

    def fetch_market_pages(*, page_limit: int = 500, status: str = "open"):
        """
        Yield (cursor_in, cursor_out, markets) using Kalshi cursor pagination.
        """
        cursor = None
        while True:
            params = {"limit": page_limit, "status": status}
            if cursor:
                params["cursor"] = cursor
            try:
                r = requests.get(f"{KALSHI_API_ROOT}/markets", params=params, timeout=30)
                r.raise_for_status()
                data = r.json()
            except Exception as e:
                print(f"ERROR: failed to fetch Kalshi markets (cursor={cursor}): {e}")
                return

            markets = data.get("markets") or []
            next_cursor = data.get("cursor")
            if not markets:
                return
            yield cursor, next_cursor, markets
            if not next_cursor or next_cursor == cursor:
                return
            cursor = next_cursor

    print(f"--- Kalshi Strategy Screener (Checked at {datetime.now().strftime('%H:%M')}) ---")
    print(
        f"Filters: volume>={'ANY (disabled via -v)' if ignore_volume else f'{MIN_VOLUME_CONTRACTS:,.0f} contracts'}, "
        f"NO in [{TARGET_NO_PRICE_MIN:.2f},{TARGET_NO_PRICE_MAX:.2f}], "
        f"stable={'ANY (disabled via -t)' if ignore_time else f'(1dΔ<=±{STABLE_MAX_ABS_1D_CHANGE:.2f})'}, "
        f"category={'ANY (disabled via -c)' if ignore_category else 'EXCLUDE sports tags'}, "
        f"side={'EITHER (disabled NO-only via -n)' if ignore_no_only else 'NO-only favorite'}, "
        f"time={'ANY (disabled via -t)' if ignore_time else '7-day/4-hour + horizon'}"
    )
    if csv_path:
        print(f"CSV output: {csv_path} (appending)")

    # Exclusion breakdown (so you can quickly see if you're filtering too hard)
    stats = {
        "total": 0,
        "low_volume": 0,
        "missing_end": 0,
        "not_in_horizon": 0,
        "bad_prices": 0,
        "not_no_favorite": 0,
        "no_not_in_band": 0,
        "unstable_24h_proxy": 0,
        "missing_event": 0,
        "category_mismatch": 0,
        "matched": 0,
        "watchlist": 0,
        "event_fetch_error": 0,
    }

    # Kalshi: we don't need per-event API calls for this screener; we use the market payload directly.

    # Process paginated markets in chunks of 500, printing results as we go.
    any_printed = False
    total_rows_written = 0
    for page_idx, (cursor_in, cursor_out, markets) in enumerate(fetch_market_pages(page_limit=500, status="open"), start=1):
        watchlist = []
        stats_page = {k: 0 for k in stats.keys()}
        stats_page["total"] = 0
        page_rows: list[dict] = []

        for market in markets:
            stats["total"] += 1
            stats_page["total"] += 1

            # 1. Filter by Volume (contracts)
            volume_contracts = int(market.get("volume") or 0)
            open_interest = int(market.get("open_interest") or 0)
            liquidity_dollars = _parse_dollars_str(market.get("liquidity_dollars"), default=0.0)
            if (not ignore_volume) and volume_contracts < MIN_VOLUME_CONTRACTS:
                stats["low_volume"] += 1
                stats_page["low_volume"] += 1
                continue
            passed_volume = True

            # 2. Time parsing (always try to compute hours_left; only filter when -t is NOT set)
            res_date_str = market.get("close_time") or market.get("expiration_time") or market.get("expected_expiration_time")
            hours_left = None
            if res_date_str:
                try:
                    res_date = datetime.fromisoformat(res_date_str.replace("Z", "+00:00"))
                    time_left = res_date - datetime.now(timezone.utc)
                    hours_left = time_left.total_seconds() / 3600
                except Exception:
                    hours_left = None

            if ignore_time:
                is_seven_day_window = False
                is_four_hour_window = False
                in_strict_window = False
                in_watchlist_horizon = True
                passed_time_constraints = True
            else:
                if hours_left is None or hours_left <= 0:
                    stats["missing_end"] += 1
                    stats_page["missing_end"] += 1
                    continue

                # 3. Strategy Matching Logic (time window)
                is_seven_day_window = abs(hours_left - SEVEN_DAY_CENTER_HOURS) <= SEVEN_DAY_TOLERANCE_HOURS
                is_four_hour_window = abs(hours_left - FOUR_HOUR_CENTER_HOURS) <= FOUR_HOUR_TOLERANCE_HOURS
                in_strict_window = is_seven_day_window or is_four_hour_window
                in_watchlist_horizon = 0 < hours_left <= WATCHLIST_MAX_DAYS_LEFT * 24
                if not (in_strict_window or in_watchlist_horizon):
                    stats["not_in_horizon"] += 1
                    stats_page["not_in_horizon"] += 1
                    continue
                passed_time_constraints = True

            # 4. Get "No" and "Yes" prices from Kalshi best bid/ask (in cents).
            yes_price = _mid_price_from_bid_ask_cents(market.get("yes_bid"), market.get("yes_ask"))
            no_price = _mid_price_from_bid_ask_cents(market.get("no_bid"), market.get("no_ask"))
            if yes_price is None and no_price is None:
                # Fallback: use last_price (in cents) if available
                last_c = market.get("last_price")
                if isinstance(last_c, int) and 0 < last_c < 100:
                    yes_price = last_c / 100.0
                    no_price = 1.0 - yes_price
            if yes_price is None or no_price is None:
                stats["bad_prices"] += 1
                stats_page["bad_prices"] += 1
                continue

            # 5. Side selection + price band
            # Default: "No is favorite" and NO price in band.
            # With -n: allow EITHER side (YES or NO) as the candidate, based on which is the favorite.
            if ignore_no_only:
                favorite_side = "NO" if no_price >= yes_price else "YES"
                favorite_price = no_price if favorite_side == "NO" else yes_price
                if not (TARGET_NO_PRICE_MIN <= favorite_price <= TARGET_NO_PRICE_MAX):
                    stats["no_not_in_band"] += 1
                    stats_page["no_not_in_band"] += 1
                    continue
            else:
                if not (no_price > yes_price):
                    stats["not_no_favorite"] += 1
                    stats_page["not_no_favorite"] += 1
                    continue
                favorite_side = "NO"
                favorite_price = no_price
                if not (TARGET_NO_PRICE_MIN <= no_price <= TARGET_NO_PRICE_MAX):
                    stats["no_not_in_band"] += 1
                    stats_page["no_not_in_band"] += 1
                    continue
            passed_price_band = True

            # 6. 24h stability proxy (disable with -t)
            # Kalshi provides `previous_price` and `last_price` (cents). Use that as a coarse 24h proxy.
            last_c = market.get("last_price")
            prev_c = market.get("previous_price")
            one_day_change = 0.0
            if isinstance(last_c, int) and isinstance(prev_c, int):
                one_day_change = (last_c - prev_c) / 100.0
            if (not ignore_time) and (one_day_change is None or abs(one_day_change) > STABLE_MAX_ABS_1D_CHANGE):
                stats["unstable_24h_proxy"] += 1
                stats_page["unstable_24h_proxy"] += 1
                continue
            passed_stability_proxy = True  # if we got here, it passed (or the filter is disabled via -t)

            # 7. Category / "sports" filter (Kalshi doesn't expose tag slugs in GetMarkets).
            # We approximate by keywording across ticker + event_ticker + title.
            ticker = str(market.get("ticker") or "")
            event_ticker = str(market.get("event_ticker") or "")
            title = str(market.get("title") or "")
            subtitle = str(market.get("subtitle") or "")
            tags_like = {s.lower() for s in [ticker, event_ticker, title, subtitle] if s}
            sports_related = _is_sports_related(tags_like)

            if (not ignore_category) and sports_related:
                stats["category_mismatch"] += 1
                stats_page["category_mismatch"] += 1
                continue

            tags_str = _format_tags(tags_like, preferred_only=False)
            passed_category = True

            if in_strict_window:
                window_label = "7-DAY (89% ACC)" if is_seven_day_window else "4-HOUR (95% ACC)"
                stats["matched"] += 1
                stats_page["matched"] += 1

                p_win = P_WIN_7DAY if is_seven_day_window else P_WIN_4H
                full_kelly = _kelly_fraction_for_binary(favorite_price, p_win)
                qk = full_kelly * KELLY_FRACTION
                stake = BANKROLL_USD * qk
                shares = (stake / favorite_price) if favorite_price > 0 else 0.0

                hours_left_str = "N/A" if hours_left is None else f"{hours_left:.1f}"
                print(f"\n[MATCH FOUND: {window_label}]")
                print(f"Title: {title}")
                print(
                    f"NO Price: ${no_price:.3f} | YES Price: ${yes_price:.3f} | "
                    f"Target: {favorite_side} @ ${favorite_price:.3f} | 1D Δ: {one_day_change:+.3f}"
                )
                print(
                    f"Volume: {volume_contracts:,} contracts | OI: {open_interest:,} | "
                    f"Liquidity: ${liquidity_dollars:,.0f} | Hours Left: {hours_left_str}"
                )
                print(f"Tags: {tags_str}")
                print(
                    f"Kelly sizing (p={p_win:.2f}): full={full_kelly * 100:.1f}% | "
                    f"{KELLY_FRACTION:.2f}-Kelly={qk * 100:.1f}% => ${stake:,.0f} (~{shares:,.0f} shares) "
                    f"on bankroll ${BANKROLL_USD:,.0f}"
                )
                print(f"Link: {_kalshi_url(ticker, event_ticker)}")
                any_printed = True

                page_rows.append(
                    {
                        "run_ts_utc": run_ts,
                        "page": page_idx,
                        "cursor": cursor_in or "",
                        "ticker": ticker,
                        "event_ticker": event_ticker,
                        "kalshi_url": _kalshi_url(ticker, event_ticker),
                        "title": title,
                        "subtitle": subtitle,
                        "end_date_iso": res_date_str or "",
                        "hours_left": hours_left,
                        "volume_usd": float(volume_contracts),
                        "no_price": no_price,
                        "yes_price": yes_price,
                        "target_side": favorite_side,
                        "target_price": favorite_price,
                        "one_day_price_change": one_day_change,
                        "tags": tags_str,
                        "min_volume_usd": MIN_VOLUME_CONTRACTS,
                        "target_price_min": TARGET_NO_PRICE_MIN,
                        "target_price_max": TARGET_NO_PRICE_MAX,
                        "stable_max_abs_1d_change": STABLE_MAX_ABS_1D_CHANGE,
                        "watchlist_max_days_left": WATCHLIST_MAX_DAYS_LEFT,
                        "passed_volume": passed_volume,
                        "passed_price_band": passed_price_band,
                        "passed_stability_proxy": passed_stability_proxy,
                        "passed_category": passed_category,
                        "sports_related": sports_related,
                        "passed_time_constraints": passed_time_constraints,
                        "flag_c_ignore_category": ignore_category,
                        "flag_v_ignore_volume": ignore_volume,
                        "flag_n_ignore_no_only": ignore_no_only,
                        "flag_t_ignore_time": ignore_time,
                        "p_win_used": p_win,
                        "kelly_full_fraction": full_kelly,
                        "kelly_fractional": qk,
                        "bankroll_usd": BANKROLL_USD,
                        "stake_usd": stake,
                        "shares": shares,
                    }
                )
            else:
                stats["watchlist"] += 1
                stats_page["watchlist"] += 1
                watchlist.append(
                    {
                        "hours_left": hours_left,
                        "end_date_iso": res_date_str or "",
                        "ticker": ticker,
                        "event_ticker": event_ticker,
                        "title": title,
                        "subtitle": subtitle,
                        "no_price": no_price,
                        "yes_price": yes_price,
                        "favorite_side": favorite_side,
                        "favorite_price": favorite_price,
                        "one_day_change": one_day_change,
                        "volume": float(volume_contracts),
                        "kalshi_url": _kalshi_url(ticker, event_ticker),
                        "tags_str": tags_str,
                        "passed_volume": passed_volume,
                        "passed_price_band": passed_price_band,
                        "passed_stability_proxy": passed_stability_proxy,
                        "passed_category": passed_category,
                        "sports_related": sports_related,
                        "passed_time_constraints": passed_time_constraints,
                    }
                )

        # Print results for this page
        print(f"\n--- Page {page_idx} (cursor={cursor_in}) scanned: {len(markets)} markets ---")
        if watchlist:
            print(
                f"Results this page (after filters): "
                f"{stats_page.get('matched', 0) + len(watchlist)} "
                f"(strict matches: {stats_page.get('matched', 0)}, watchlist: {len(watchlist)}). "
                f"Printing top {min(len(watchlist), WATCHLIST_MAX_RESULTS)} watchlist rows."
            )
            print(f"Watchlist (page {page_idx}):")

            def _hl_sort_key(x):
                hl = x.get("hours_left")
                if isinstance(hl, (int, float)):
                    return (0, float(hl))
                return (1, 0.0)

            watchlist.sort(key=_hl_sort_key)
            for i, m in enumerate(watchlist[:WATCHLIST_MAX_RESULTS], start=1):
                p_win = P_WIN_DEFAULT
                fav_price = _parse_float(m.get("favorite_price"), default=0.0) or 0.0
                full_kelly = _kelly_fraction_for_binary(fav_price, p_win)
                qk = full_kelly * KELLY_FRACTION
                stake = BANKROLL_USD * qk
                shares = (stake / fav_price) if fav_price > 0 else 0.0

                days_left_str = "N/A"
                hl = m.get("hours_left")
                if isinstance(hl, (int, float)):
                    days_left_str = f"{(float(hl) / 24):.1f}d ({float(hl):.1f}h)"

                print(f"\n[{i}] {m['title']}")
                print(
                    f"NO ${m['no_price']:.3f} | YES ${m['yes_price']:.3f} | "
                    f"Target: {m['favorite_side']} @ ${fav_price:.3f} | "
                    f"1D Δ: {m['one_day_change']:+.3f} | "
                    f"Volume: ${m['volume']:,.0f} | Time left: {days_left_str}"
                )
                print(f"Tags: {m['tags_str']}")
                print(
                    f"Kelly sizing (p={p_win:.2f}): full={full_kelly * 100:.1f}% | "
                    f"{KELLY_FRACTION:.2f}-Kelly={qk * 100:.1f}% => ${stake:,.0f} (~{shares:,.0f} shares) "
                    f"on bankroll ${BANKROLL_USD:,.0f}"
                )
                print(f"Link: {m.get('kalshi_url')}")
                any_printed = True
        else:
            print("No watchlist results on this page with current filters.")

        # Append ALL watchlist results to CSV (not just the printed top N),
        # so CSV row counts match the totals under any flag combination.
        if watchlist:
            for m in watchlist:
                p_win = P_WIN_DEFAULT
                fav_price = _parse_float(m.get("favorite_price"), default=0.0) or 0.0
                full_kelly = _kelly_fraction_for_binary(fav_price, p_win)
                qk = full_kelly * KELLY_FRACTION
                stake = BANKROLL_USD * qk
                shares = (stake / fav_price) if fav_price > 0 else 0.0

                page_rows.append(
                    {
                        "run_ts_utc": run_ts,
                        "page": page_idx,
                        "cursor": cursor_in or "",
                        "ticker": m.get("ticker", ""),
                        "event_ticker": m.get("event_ticker", ""),
                        "kalshi_url": m.get("kalshi_url", ""),
                        "title": m.get("title", ""),
                        "subtitle": m.get("subtitle", ""),
                        "end_date_iso": m.get("end_date_iso", ""),
                        "hours_left": m.get("hours_left"),
                        "volume_usd": m.get("volume"),
                        "no_price": m.get("no_price"),
                        "yes_price": m.get("yes_price"),
                        "target_side": m.get("favorite_side"),
                        "target_price": fav_price,
                        "one_day_price_change": m.get("one_day_change"),
                        "tags": m.get("tags_str"),
                        "min_volume_usd": MIN_VOLUME_CONTRACTS,
                        "target_price_min": TARGET_NO_PRICE_MIN,
                        "target_price_max": TARGET_NO_PRICE_MAX,
                        "stable_max_abs_1d_change": STABLE_MAX_ABS_1D_CHANGE,
                        "watchlist_max_days_left": WATCHLIST_MAX_DAYS_LEFT,
                        "passed_volume": m.get("passed_volume"),
                        "passed_price_band": m.get("passed_price_band"),
                        "passed_stability_proxy": m.get("passed_stability_proxy"),
                        "passed_category": m.get("passed_category"),
                        "sports_related": m.get("sports_related"),
                        "passed_time_constraints": m.get("passed_time_constraints"),
                        "flag_c_ignore_category": ignore_category,
                        "flag_v_ignore_volume": ignore_volume,
                        "flag_n_ignore_no_only": ignore_no_only,
                        "flag_t_ignore_time": ignore_time,
                        "p_win_used": p_win,
                        "kelly_full_fraction": full_kelly,
                        "kelly_fractional": qk,
                        "bankroll_usd": BANKROLL_USD,
                        "stake_usd": stake,
                        "shares": shares,
                    }
                )

        csv_append_rows(page_rows)
        total_rows_written += len(page_rows)
        if csv_path:
            print(f"Rows appended to CSV so far: {total_rows_written}")

        # Cumulative breakdown (totals so far)
        print("Total exclusion breakdown (cumulative):")
        for k in [
            "total",
            "low_volume",
            "missing_end",
            "not_in_horizon",
            "bad_prices",
            "not_no_favorite",
            "no_not_in_band",
            "unstable_24h_proxy",
            "missing_event",
            "category_mismatch",
            "event_fetch_error",
            "matched",
            "watchlist",
        ]:
            print(f"- {k}: {stats[k]}")

    if not any_printed:
        print("\nNo results found across all pages with current filters.")
    else:
        print(f"\nDone. Total markets scanned: {stats['total']}. Total rows appended: {total_rows_written}.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Kalshi strategy screener (Trading API v2 market data).")
    parser.add_argument(
        "-c",
        action="store_true",
        help="Disable category filtering (include all categories, including sports).",
    )
    parser.add_argument(
        "-v",
        action="store_true",
        help="Disable the MIN_VOLUME filter (include low-volume markets).",
    )
    parser.add_argument(
        "-n",
        action="store_true",
        help="Disable NO-only screening (allow EITHER side to be the target if it's the favorite and within the band).",
    )
    parser.add_argument(
        "-t",
        action="store_true",
        help="Disable all time-based constraints (endDate requirement, time horizon/windows, and 24h stability proxy).",
    )
    parser.add_argument(
        "--csv",
        default=os.path.join(os.path.dirname(__file__), "hs_screener_results.csv"),
        help="Path to a CSV file to append results to (open in Excel/Google Sheets).",
    )
    args = parser.parse_args()
    try:
        screen_markets(
            ignore_category=args.c,
            ignore_volume=args.v,
            ignore_no_only=args.n,
            ignore_time=args.t,
            csv_path=args.csv,
        )
    except BrokenPipeError:
        # Allows `python hs_screener.py ... | head` without a noisy stack trace.
        try:
            sys.stdout.close()
        finally:
            sys.exit(0)
