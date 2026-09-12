# TEL Collection — current state

**Read this file first.** Last verified: **Sun 13 Sep 2026, ~01:30 AEST**.

Every line below carries one of three labels, per the verification standard in `README.md`:
**WORKING** (an outcome was observed), **BROKEN** (a fault was observed), **UNTESTED** (state
cannot be known yet — not the same as working).

---

## WORKING — observed producing an outcome

| Thing | Evidence |
|---|---|
| Checkout | Shopify Payments SUCCESS on every order, auth + capture |
| Shipping | Free domestic ($0), Express $15 |
| Product | Ritual Duo ACTIVE, **439 units**, published to Online Store / Facebook & Instagram / POS / Google & YouTube |
| Meta pixel | Fires — 1,277 landing page views on 1,390 clicks. LPV optimisation cannot run without it |
| CAPI | **Maximum** on the Shopify Facebook & Instagram channel, with advanced matching |
| Meta ads | Campaign `120247236202470688` ENABLED; both ads `ACTIVE` + `review.status: APPROVED` |
| Ad efficiency | Warm Entry v2 at **$0.115 per landing page view**, frequency 1.05–1.10 |
| Meta page standing | `1184411344764247` returns as a valid promotable page. A restricted page cannot get ads approved |
| Healing guide flow `WnAETh` | **14 delivered, 7 opens (50%)** |
| Welcome flow `TEZ6PM` | 5 delivered, 2 clicks, **1 conversion $59.95** |
| Klaviyo ↔ Shopify | Full commerce event set present and firing |
| Subscriber sync | **Enabled** 13 Sep, targeting list `V9Rbbr` |
| POS revenue | 38 units in 30 days. 12 Sep: **6 orders, $327 net** — best day in a fortnight |
| Organic Instagram | 2,612 (10 Sep) and 2,718 (11 Sep) profile views against a 91–152/day baseline. **17×, on $0.01 of paid IG** |

## BROKEN — a fault was observed

| # | Fault | Detail |
|---|---|---|
| 1 | **Form `WirxQ2` does not render** | Form-level `status: draft`, `updated_at` 4 Sep. The *version* is live; the form is not. Zero views, ever. Fix on the sign-up forms **list** row, not in the builder |
| 2 | **Consent stranded** | Segment `YgyR87` = **23** against Shopify's **50+** subscribed. Sync is on but does not backfill. Needs a CSV import |
| 3 | **No reviews integration anywhere** | All 37 Klaviyo metrics are Shopify / Klaviyo-internal / onsite-API. No Judge.me, no review metric. None of the 7 flows asks for a review |
| 4 | **Warm Stack audiences empty** | Reach **9** on $1.33 across a full evening. Built against gate-era URLs |
| 5 | `record_utm_params_on_submit: false` | Subscribers cannot be attributed to the ad or email that produced them |
| 6 | One form text line invisible | Inline `color: rgb(0,0,0)` overrides the corrected global gold, on a `#080808` panel |
| 7 | Order #1046 | PayPal `SALE` stuck PENDING, $59.95. PayPal-side hold, not a gateway fault |
| 8 | `WjZxaE` Squires exclusion list | **0 members** — the price-split guard was empty. Harmless (separate platforms) but not to be relied on |

## UNVERIFIED — reported saved, never re-read

These were changed late and the session closed before confirming. **Treat as unknown.**

- `V9Rbbr` → single opt-in (was `double_opt_in`)
- `V9Rbbr` → global unsubscribe ticked
- Instagram bio updated

## UNTESTED — cannot be known yet

| Thing | Why |
|---|---|
| `TPwqqq` online healing guide | Triggers on fulfilment; only 2 web orders ever, one a stuck PayPal |
| `Vg9tuX` abandoned checkout | No abandoned carts of consequence yet |
| `YgAs6b` browse abandonment | Onsite tracking only just enabled |
| `UpBgzj` reorder | **Correct** — 50-day delay, first sends due **~8–11 Oct** |
| `SuavPL` back-in-stock | Still `draft`. 439 units, so no urgency |
| Conversion event per ad set | Unreadable via Supermetrics; uneditable on published ad sets. Ads Manager only |
| COGS per Ritual Duo | Assumed ~$15. **The entire CPA model rests on this** |
| Which Klaviyo org the upgrade billed to | Possibly the wrong "King…" account |

---

## Ben's own five-minute check

Run this weekly, and after any change to the email or ads stack. It catches the whole class of
fault that suppressed the launch, without needing anyone else.

1. **Klaviyo → Sign-up forms.** Does the row say **Live**? Then open its analytics — are
   **views above zero**? Live with zero views means it is not rendering.
2. **Klaviyo → Lists → Email List.** Is the member count **higher than last week**? Flat means
   capture has stopped.
3. **The two-sided check.** Shopify → Customers → filter *email subscription = subscribed*, and
   note the count. Compare to Klaviyo's emailable segment. **They should roughly match.** A gap
   means consent is stranded — this is the check that would have caught the biggest fault here.
4. **Meta Ads Manager → Ads.** Does every ad read **Active** *and* **Approved**? And is
   yesterday's spend non-zero? Zero spend on an active campaign means billing.
5. **Judge.me.** Is the review count rising?
6. **Monthly, and before any launch:** put a real order through with a real email, and confirm
   the welcome and post-purchase emails actually arrive. Then refund it. **Four minutes.** This
   single test would have caught all three launch faults.

Rule of thumb behind all six: **a setting that says the right thing is a hypothesis. A number
that moved is a fact.**

---

## Next four actions

1. Form `WirxQ2` → flip on the forms **list** row
2. CSV backfill the stranded subscribers
3. **Judge.me** → is the review-request email enabled, and what delay. *Check this before
   building any Klaviyo review flow, or the two will double-ask the same customer*
4. The end-to-end test above

Nothing is currently losing money while these wait. The ads are delivering, the studio is
selling, and the funnel's remaining faults are settings rather than damage.
