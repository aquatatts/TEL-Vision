# TEL Collection — current state

**Read this file first.** Last verified: **Sun 13 Sep 2026, 08:54 AEST** (morning check).

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

---

## Morning check — Sun 13 Sep 2026, 08:54 AEST

First full day of delivery after the billing fix. Verified by outcome, per the standard.

### Last night's saves — one confirmed NOT applied, one still unverified

| Change | Reading |
|---|---|
| Form `WirxQ2` → live | **NOT DONE.** Still `status: draft`, `updated_at` still **2026-09-04**. Untouched |
| `V9Rbbr` → single opt-in | **STILL UNVERIFIED** — the connector dropped before it could be re-read. Not assumed done |
| `V9Rbbr` → global unsubscribe | **STILL UNVERIFIED**, same reason |
| Instagram bio | Changed, but see `website_clicks` below — it did not resolve the question |

### Consent chain — no movement
Segment `YgyR87` = **23**, unchanged. No backfill occurred, confirming the sync is
forward-only. The CSV import is still required.

### Form capture — still nothing
`query_form_values` over `last_7_days` → `results: []`. Consistent with the form being draft.

### Instagram — spike decaying, still well above baseline

| Date | Profile views | Accounts engaged |
|---|---|---|
| 7 Sep | 91 | 3 |
| 8 Sep | 145 | 5 |
| 9 Sep | 152 | 3 |
| 10 Sep | **2,612** | 51 |
| 11 Sep | **2,718** | 52 |
| 12 Sep | **682** | 8 |

682 is off the peak but still **~4.5× the 91–152 baseline**. Normal decay from a launch moment,
not a collapse.

**`website_clicks` returned `null` on every day, including after the bio change.** That settles
it as an **API limitation of the `IGI` source**, not a pending answer — it cannot be resolved
from here at all. Ben must read link clicks in the Instagram app directly.

### Ad delivery — 12 Sep, full day

| Ad set | Platform | Cost | Impr | Reach | Freq | Clicks | LPV | Cost/LPV |
|---|---|---|---|---|---|---|---|---|
| Warm Entry v2 | facebook | $4.81 | 463 | 444 | 1.04 | 47 | 44 | **$0.109** |
| Broad AU | instagram | $3.43 | 174 | 159 | 1.09 | 2 | 1 | $3.43 |
| Broad AU | facebook | $1.64 | 108 | 100 | 1.08 | 1 | 1 | $1.64 |
| Warm Stack | instagram | $1.36 | 13 | **8** | 1.63 | 0 | 0 | — |
| Warm Stack | facebook | $0 | 2 | 2 | 1.00 | 0 | 0 | — |

**Warm Entry v2 improved to $0.109/LPV**, better than its $0.115 and its historical $0.13.

**Warm Stack confirmed dead again** — reach 8 on $1.36.

**Severe budget underdelivery, flagged for watching.** Combined spend was **$11.24 against a
$60/day budget — 19%.** Ritual Drop used $6.43 of $40; Warm Entry used $4.81 of $20. Likely
Meta ramping after the billing interruption, compounded by Warm Stack being unable to spend its
share of the CBO pool. Expect normalisation over 2–3 days. **If it has not recovered by Tue
15 Sep, treat it as a real fault.**

### Correction — the Instagram placement case is NOT supported by paid data

A previous entry recommended shifting budget to Instagram. The paid numbers appear to
contradict it ($3.43/LPV on Instagram against $0.109 on Facebook), **but this is not a valid
comparison and must not be read as one**:

- Warm Entry v2 is a **TRAFFIC** campaign optimising for landing page views, delivering 100%
  Facebook.
- Broad AU is a **SALES** campaign optimising `OFFSITE_CONVERSIONS` with zero purchase history,
  still in learning, and is the only ad set on Instagram.

A conversion campaign in learning always costs far more per click than a traffic campaign. The
difference measured is **objective, not placement.**

**There is still no clean Instagram-versus-Facebook read.** The Instagram case rests on
*organic* evidence (5,330 profile views in two days at $0.01 paid), which remains valid and
untested by this data. The experiment that would settle it: run **Warm Entry v2 — same
objective, same creative, proven $0.109 — on Instagram placement** and compare like with like.

### Orders — 54 lifetime, still no new web sales

| Date (AEST) | Orders | Net |
|---|---|---|
| 10 Sep | 2 | $54.50 |
| 11 Sep | 2 | $109 |
| **12 Sep** | **6** | **$327** |
| 13 Sep (to 08:54) | 1 | $54.50 |

#1054 landed **00:14 AEST** — checked directly rather than assumed: `shippingAddress: null`,
fulfilled at "Shop location" two seconds after creation, no tracking. **That is the POS
signature**, a late Saturday studio sale, not a web order.

**Zero new web orders. Zero `ritual_drop_sep26` UTM. Zero `TELTAKEOVER` redemptions.** Every
dollar since launch remains POS.

### Still outstanding
1. Form `WirxQ2` → flip on the sign-up forms **list** row
2. CSV backfill the stranded subscribers (Shopify 50+ vs Klaviyo 23)
3. **Judge.me** → is the review-request email enabled, and what delay
4. End-to-end test — own email through the popup, plus a real counter tick
5. Re-read `V9Rbbr` to confirm last night's two saves actually applied

---

## Form `WirxQ2` — fault CONFIRMED, rebuild rather than debug

**13 Sep, ~11:30 AEST.** Exhaustively tested. Every setting reads correct and the form does not
render on the live site.

### Ruled out by direct verification
| Checked | Result |
|---|---|
| Form status | **Live** — version `28374824`, published 12 Sep. The parent record's `status: "draft"` is misleading metadata; the UI correctly shows Live |
| Forms-on-website (account switch) | **Enabled** |
| Klaviyo app embed on the live theme | `"disabled": false` in `config/settings_data.json` on `TEL v6.2` (role MAIN) |
| `{{ content_for_header }}` | **Present** in `layout/theme.liquid` `<head>` — the hook app embeds inject through |
| URL / page targeting | None. `location: null` |
| Triggers | 8s delay, device `both`, 14-day re-show |
| Conflicting scripts | Mailchimp block correctly `disabled: true` |
| **Live page, phone, never previewed** | **No popup after 15s** |

### Two invalid tests, recorded so they are not repeated
Two earlier negative results were **void** and nearly sent the diagnosis the wrong way:

1. **`Active on Site` = 0 events** does *not* prove the script is absent. That metric only fires
   for **identified** profiles; with 23 subscribers and almost no email clicks, zero is expected
   either way. This is the second time this metric has misled this project.
2. **Desktop tests were run inside a Shopify theme preview.** The browser held a preview session
   pinning `telcollection.com.au` to draft theme `TEL v6.1`, with a clean-looking URL and only a
   small bar at the bottom of the screen to give it away. **Klaviyo does not inject into theme
   previews**, so both the popup test and a "0 matches for klaviyo" page-source search were
   meaningless. Only the phone test was valid.

**Lesson:** verify *which* theme a page is served from before drawing any conclusion from it.
Nine themes exist and one unpublished theme is named "TEL — Earned. Not given. **(live)**".
Theme names lie; `role: MAIN` is the truth.

### Recommendation
**Build a new form from scratch.** The state is unresolvable from the outside, and this form
carries a messy history — created 4 Sep, two versions, a parent/version status split, "(DRAFT)"
in its name. A fresh build is ~10 minutes with far better odds than further forensics. Copy is
ready in `launch/capture-form-fix.md`. Set `record_utm_params_on_submit: true` on the new one.

### But sequence it last
The popup is the **lowest-value** of the three open items, and the only one fighting back:

| Task | Delivers | When |
|---|---|---|
| **CSV backfill** | **27+ subscribers who already bought and already consented** | Today |
| **Judge.me** | Reviews from 40+ customers who have used the product | Today |
| Popup rebuild | Future subscribers, from traffic that must be paid for | After |

The first two hand over value already earned. Do those first.

---

## Backfill COMPLETE — 13 Sep, 12:00 AEST

**The consent chain is now working end to end for existing customers.** Verified at profile
level, not by the success screen.

### What was done
Shopify → Customers → filtered `email_subscription_status = SUBSCRIBED` → exported 44 → imported
to list `V9Rbbr` with **"Update subscription status for all imported contacts to subscribed"**,
Email → Marketing messages only (no SMS, no WhatsApp).

### Verified by API

| Measure | Before | After |
|---|---|---|
| List `V9Rbbr` | 24 | **58** |
| Import job | — | **44/44 rows, completed** |
| Sampled profiles | 8 of 9 `NEVER_SUBSCRIBED` | **9 of 11 `SUBSCRIBED`** |

Profiles that read `NEVER_SUBSCRIBED` last night now read:
```
consent:                     SUBSCRIBED
method:                      LIST_IMPORT
consent_timestamp:           2026-09-13T01:59:53Z
can_receive_email_marketing: true
```

**The two customers who did NOT consent in Shopify remain `NEVER_SUBSCRIBED`.** They were
manually unticked before export (49 → 44). This is the important detail: consent was
*relocated*, never manufactured, and the people who declined stayed out. Verifiable in the data.

### Also resolved
`opt_in_process` now reads **`single_opt_in`** by API — clearing one of the three items recorded
as UNVERIFIED last night. It had saved; it simply was never re-read.

### Known lag, not a fault
Segment `YgyR87` still reads **23**. Klaviyo segments recalculate asynchronously and the
underlying profile consent is already correct. Expect convergence toward ~58 without action.
**Do not treat the stale segment count as a failed import** — the profile-level read is the
truth here.

### Why this matters commercially
A list of 23 cannot move revenue regardless of copy quality — which is exactly why the Doors
Open campaign reached 20 people and produced $0. **58 paying customers is a list that can be
sold to**, and every one of them has used the product.

---

## Judge.me — six 5-star reviews exist and none of them display

**13 Sep, ~12:10 AEST. This supersedes the earlier reading that "no reviews have landed".**
That claim was extrapolated from Klaviyo having no reviews integration — true, but it said
nothing about Judge.me, and it should never have been stated as fact about reviews generally.

### What the Judge.me dashboard actually shows

| Metric (30d) | Value |
|---|---|
| **Reviews** | **6** |
| **Average rating** | **5.0** |
| Requests sent | 21 (↑425%) |
| Revenue attributed | $0 |

**Collection is working.** Review requests are going out and customers are responding, all five
stars. What has never worked is **display** — the reviews are not on the product page.

### The actual fault
Judge.me's setup guide lists two incomplete steps: *"Enable Judge.me on your store"* and
*"Enable Reviews Widget"*. The first is **a false alarm** — `judgeme_core` reads
`"disabled": false` in `settings_data.json` on the live theme, and the theme editor's App
embeds toggle is already ON. Another case of a UI claiming a state that is not real.

The real gap is the second one. The core snippet only **loads the script**; it renders nothing.
The theme editor states this plainly: *"The Judge.me Core Snippet contains code used by
Judge.me widgets. Enable this before you add more widgets."* **No display widget has ever been
placed on the product page template.**

### Fix — two widgets on `TEL v6.2` (role MAIN), template "Default product"
1. **Judge.me Preview Badge** (star rating + review count) — add as a **block inside the main
   product section**, positioned **directly under the Price**. This is the higher-value of the
   two: visible without scrolling, and it is what a cold visitor reads in the first second.
2. **Judge.me Review Widget** (full review list) — add as a **section** below the product
   description.

### Why this ranks above the Meta audience
The store converts at **0.04%** on 4,580 sessions. A cold visitor meets a $59.95 product from an
unknown brand with **no social proof of any kind**. Six reviews at a perfect 5.0 is the
strongest possible answer to that, it is already earned, and it costs nothing to switch on.

Same pattern as the email backfill: **the value was already there and simply not connected.**
