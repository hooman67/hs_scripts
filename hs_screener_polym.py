import requests  # type: ignore[import-untyped]
from datetime import datetime, timezone
import json
import argparse
import sys
import os
import csv

# --- SETTINGS ---
MIN_VOLUME_USD = 30_000  # Only show markets with $50k+ volume

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


def _json_list(value):
    """
    Gamma sometimes returns fields like `outcomes` / `outcomePrices` as JSON-encoded strings.
    Normalize those into Python lists.
    """
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, str):
        s = value.strip()
        if not s:
            return []
        try:
            parsed = json.loads(s)
            return parsed if isinstance(parsed, list) else []
        except json.JSONDecodeError:
            return []
    return []


def _parse_float(value, default=None):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


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
        "offset",
        "market_id",
        "slug",
        "polymarket_url",
        "question",
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

    def fetch_market_pages(*, page_limit: int = 500):
        """Yield lists of markets using Gamma offset pagination."""
        offset = 0
        while True:
            url = (
                "https://gamma-api.polymarket.com/markets"
                f"?active=true&closed=false&limit={page_limit}&offset={offset}"
            )
            try:
                response = requests.get(url, timeout=30)
                response.raise_for_status()
                page = response.json()
            except Exception as e:
                print(f"ERROR: failed to fetch markets from Gamma API at offset={offset}: {e}")
                return

            if not isinstance(page, list) or not page:
                return

            yield offset, page
            if len(page) < page_limit:
                return
            offset += page_limit

    print(f"--- Polymarket Strategy Screener (Checked at {datetime.now().strftime('%H:%M')}) ---")
    print(
        f"Filters: volume>={'ANY (disabled via -v)' if ignore_volume else f'${MIN_VOLUME_USD:,.0f}'}, "
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

    event_cache = {}  # event_id -> set(tag_slugs)

    # Process paginated markets in chunks of 500, printing results as we go.
    any_printed = False
    total_rows_written = 0
    for page_idx, (offset, markets) in enumerate(fetch_market_pages(page_limit=500), start=1):
        watchlist = []
        stats_page = {k: 0 for k in stats.keys()}
        stats_page["total"] = 0
        page_rows: list[dict] = []

        for market in markets:
            stats["total"] += 1
            stats_page["total"] += 1

            # 1. Filter by Volume
            volume = _parse_float(market.get("volume"), default=0.0) or 0.0
            if (not ignore_volume) and volume < MIN_VOLUME_USD:
                stats["low_volume"] += 1
                stats_page["low_volume"] += 1
                continue
            passed_volume = True

            # 2. Time parsing (always try to compute hours_left; only filter when -t is NOT set)
            res_date_str = market.get("endDate") or market.get("endDateIso") or market.get("resolutionDate")
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

            # 4. Get "No" and "Yes" prices (Gamma returns outcomes/outcomePrices as JSON strings)
            try:
                outcomes = _json_list(market.get("outcomes"))
                prices = _json_list(market.get("outcomePrices"))
                if len(outcomes) != len(prices) or len(outcomes) < 2:
                    stats["bad_prices"] += 1
                    stats_page["bad_prices"] += 1
                    continue

                # Find indices by label (avoid assuming ordering)
                label_to_idx = {str(lbl).strip().lower(): i for i, lbl in enumerate(outcomes)}
                if "no" not in label_to_idx or "yes" not in label_to_idx:
                    stats["bad_prices"] += 1
                    stats_page["bad_prices"] += 1
                    continue

                no_price = _parse_float(prices[label_to_idx["no"]])
                yes_price = _parse_float(prices[label_to_idx["yes"]])
                if no_price is None or yes_price is None:
                    stats["bad_prices"] += 1
                    stats_page["bad_prices"] += 1
                    continue
            except (ValueError, IndexError):
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
            one_day_change = _parse_float(market.get("oneDayPriceChange"), default=0.0)
            if (not ignore_time) and (one_day_change is None or abs(one_day_change) > STABLE_MAX_ABS_1D_CHANGE):
                stats["unstable_24h_proxy"] += 1
                stats_page["unstable_24h_proxy"] += 1
                continue
            passed_stability_proxy = True  # if we got here, it passed (or the filter is disabled via -t)

            # 7. Category focus via event tags
            events = market.get("events") or []
            event_id = (events[0].get("id") if events and isinstance(events[0], dict) else None)
            if not event_id:
                stats["missing_event"] += 1
                stats_page["missing_event"] += 1
                tag_slugs = set()
            else:
                if event_id not in event_cache:
                    try:
                        ev = requests.get(f"https://gamma-api.polymarket.com/events/{event_id}", timeout=30).json()
                        tags = ev.get("tags") or []
                        tag_slugs = {str(t.get("slug", "")).strip().lower() for t in tags if isinstance(t, dict)}
                        event_cache[event_id] = tag_slugs
                    except Exception:
                        stats["event_fetch_error"] += 1
                        stats_page["event_fetch_error"] += 1
                        continue

                tag_slugs = event_cache.get(event_id, set())

            # Include markets with no tags (Tags: (none)) as well.
            # Default behavior: remove sports/sports-related markets by tags,
            # unless user disables category filtering via -c.
            if (not ignore_category) and _is_sports_related(tag_slugs):
                stats["category_mismatch"] += 1
                stats_page["category_mismatch"] += 1
                continue

            tags_str = _format_tags(tag_slugs, preferred_only=False)
            sports_related = _is_sports_related(tag_slugs)
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
                print(f"Question: {market.get('question')}")
                print(
                    f"NO Price: ${no_price:.3f} | YES Price: ${yes_price:.3f} | "
                    f"Target: {favorite_side} @ ${favorite_price:.3f} | 1D Δ: {one_day_change:+.3f}"
                )
                print(f"Volume: ${volume:,.0f} | Hours Left: {hours_left_str}")
                print(f"Tags: {tags_str}")
                print(
                    f"Kelly sizing (p={p_win:.2f}): full={full_kelly * 100:.1f}% | "
                    f"{KELLY_FRACTION:.2f}-Kelly={qk * 100:.1f}% => ${stake:,.0f} (~{shares:,.0f} shares) "
                    f"on bankroll ${BANKROLL_USD:,.0f}"
                )
                print(f"Link: https://polymarket.com/event/{market.get('slug')}")
                any_printed = True

                page_rows.append(
                    {
                        "run_ts_utc": run_ts,
                        "page": page_idx,
                        "offset": offset,
                        "market_id": market.get("id"),
                        "slug": market.get("slug"),
                        "polymarket_url": (
                            f"https://polymarket.com/event/{market.get('slug')}"
                            if market.get("slug")
                            else ""
                        ),
                        "question": market.get("question"),
                        "end_date_iso": res_date_str or "",
                        "hours_left": hours_left,
                        "volume_usd": volume,
                        "no_price": no_price,
                        "yes_price": yes_price,
                        "target_side": favorite_side,
                        "target_price": favorite_price,
                        "one_day_price_change": one_day_change,
                        "tags": tags_str,
                        "min_volume_usd": MIN_VOLUME_USD,
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
                        "market_id": market.get("id"),
                        "question": market.get("question"),
                        "no_price": no_price,
                        "yes_price": yes_price,
                        "favorite_side": favorite_side,
                        "favorite_price": favorite_price,
                        "one_day_change": one_day_change,
                        "volume": volume,
                        "slug": market.get("slug"),
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
        print(f"\n--- Page {page_idx} (offset={offset}) scanned: {len(markets)} markets ---")
        if watchlist:
            print(
                f"Results this page (after filters): "
                f"{stats_page.get('matched', 0) + len(watchlist)} "
                f"(strict matches: {stats_page.get('matched', 0)}, watchlist: {len(watchlist)}). "
                f"Printing top {min(len(watchlist), WATCHLIST_MAX_RESULTS)} watchlist rows."
            )
            print(f"Watchlist (page {page_idx}):")
            watchlist.sort(key=lambda x: (x["hours_left"] is None, x["hours_left"] or 0))
            for i, m in enumerate(watchlist[:WATCHLIST_MAX_RESULTS], start=1):
                p_win = P_WIN_DEFAULT
                full_kelly = _kelly_fraction_for_binary(m["favorite_price"], p_win)
                qk = full_kelly * KELLY_FRACTION
                stake = BANKROLL_USD * qk
                shares = (stake / m["favorite_price"]) if m["favorite_price"] > 0 else 0.0

                days_left_str = "N/A"
                if m["hours_left"] is not None:
                    days_left_str = f"{(m['hours_left'] / 24):.1f}d ({m['hours_left']:.1f}h)"

                print(f"\n[{i}] {m['question']}")
                print(
                    f"NO ${m['no_price']:.3f} | YES ${m['yes_price']:.3f} | "
                    f"Target: {m['favorite_side']} @ ${m['favorite_price']:.3f} | "
                    f"1D Δ: {m['one_day_change']:+.3f} | "
                    f"Volume: ${m['volume']:,.0f} | Time left: {days_left_str}"
                )
                print(f"Tags: {m['tags_str']}")
                print(
                    f"Kelly sizing (p={p_win:.2f}): full={full_kelly * 100:.1f}% | "
                    f"{KELLY_FRACTION:.2f}-Kelly={qk * 100:.1f}% => ${stake:,.0f} (~{shares:,.0f} shares) "
                    f"on bankroll ${BANKROLL_USD:,.0f}"
                )
                print(f"Link: https://polymarket.com/event/{m.get('slug')}")
                any_printed = True
        else:
            print("No watchlist results on this page with current filters.")

        # Append ALL watchlist results to CSV (not just the printed top N),
        # so CSV row counts match the totals under any flag combination.
        if watchlist:
            for m in watchlist:
                p_win = P_WIN_DEFAULT
                full_kelly = _kelly_fraction_for_binary(m["favorite_price"], p_win)
                qk = full_kelly * KELLY_FRACTION
                stake = BANKROLL_USD * qk
                shares = (stake / m["favorite_price"]) if m["favorite_price"] > 0 else 0.0

                page_rows.append(
                    {
                        "run_ts_utc": run_ts,
                        "page": page_idx,
                        "offset": offset,
                        "market_id": m.get("market_id", ""),
                        "slug": m.get("slug", ""),
                        "polymarket_url": (
                            f"https://polymarket.com/event/{m.get('slug')}"
                            if m.get("slug")
                            else ""
                        ),
                        "question": m.get("question", ""),
                        "end_date_iso": m.get("end_date_iso", ""),
                        "hours_left": m.get("hours_left"),
                        "volume_usd": m.get("volume"),
                        "no_price": m.get("no_price"),
                        "yes_price": m.get("yes_price"),
                        "target_side": m.get("favorite_side"),
                        "target_price": m.get("favorite_price"),
                        "one_day_price_change": m.get("one_day_change"),
                        "tags": m.get("tags_str"),
                        "min_volume_usd": MIN_VOLUME_USD,
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
    parser = argparse.ArgumentParser(description="Polymarket strategy screener (Gamma API).")
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
