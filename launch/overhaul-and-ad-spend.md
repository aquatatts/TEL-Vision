# TEL Collection — post-launch: convert the attention you already have

## Context

TEL opened Thu 10 Sep 7pm AEST. The launch looked flat, and the original diagnosis found three
stacked failures: the capture form never published, the Ritual Drop sales campaign was an empty
shell, and the Meta ad account's billing failed ~24h after opening and switched the campaigns
off. **All three are now rectified** — ads built and enabled, billing paid with the card set
primary, form published, CAPI confirmed already on Maximum.

Tonight's measurement changed the strategic picture, and that is why this plan is being
rewritten rather than continued.

**The finding:** Instagram profile views went from a 91–152/day baseline to **2,612 (10 Sep)
and 2,718 (11 Sep)** — 17× — while paid Instagram delivery on those days was **$0.00 and
$0.01**. The entire ad budget went to Facebook placement. The launch-weekend attention was
**100% organic**, and it beat the paid budget by roughly 13× on volume at zero cost.

Those 5,330 profile views produced **2 web orders**. The problem was never attention. It is
that attention is arriving and leaking — no capture, and an unverified path from Instagram to
the product page. Fixing the leak is worth more than any budget decision here.

### Verified tonight — do not re-litigate

| Thing | State |
|---|---|
| Orders 12 Sep | 5 × $59.95 = **$299.75**, all `sourceName: "pos"` (#1048–#1052) |
| Web orders since launch | **2**. Zero `TELTAKEOVER` redemptions, ever |
| Ad account | Billing rectified, card primary, all 3 ad sets delivering |
| Warm Entry v2 | **$0.115/LPV** — beating its historical $0.13 |
| Warm Stack | **Dead.** Reach 9 on $1.33. Audiences built against the gated store |
| Form `WirxQ2` | **still `status: draft`** at form level, `updated_at` 4 Sep. `query_form_values` → `results: []` |
| Emailable segment | **23**. No backfill after the sync was enabled |
| Subscriber sync | **Enabled** 13 Sep, targeting `V9Rbbr` |
| `V9Rbbr` opt-in | double → **single** (reported saved, verify by API) |
| `V9Rbbr` opt-out | global unsubscribe **ticked** |
| Instagram bio | **Updated** — `website_clicks` should stop returning `null` |
| `WjZxaE` Squires exclusion list | **0 members** — the price-split guard was empty. No harm (different platforms), but do not rely on it |
| New profiles since 11 Sep | 9, of which 8 read `NEVER_SUBSCRIBED` in Klaviyo — but **subscribed in Shopify**. Sync fault, see 1c |
| CAPI | Already Maximum on the Shopify F&I channel |
| Checkout / shipping / channels / pixel | All healthy, confirmed by live read |

---

## Priority 1 — stop the leak (before another ad dollar scales)

### Doable from a phone, at the counter

**Job 1 — publish the form (~30s).** Klaviyo → **Sign-up forms list** → the row
`TEL · First access popup (DRAFT)` → switch its status to Live **on the row**. Do **not** open
the form builder: its publish control is the thing that has failed twice, updating the version
and leaving the form on `draft`. The list is a different control.

**Job 2 — the audience (~90s).** Meta Ads app → Audiences → Create → Custom Audience →
**Instagram account** → the TEL account → **365 days** → name `TEL — IG engagers 365d`.

Everything else in Priority 1 is a laptop job.


**1a. The Instagram → store path.** `website_clicks` returned `null` for all 7 days; I cannot
distinguish "metric unavailable on IGI" from "genuinely zero". Ben to confirm on his phone that
the bio link exists and lands on `/products/tattoo-aftercare-kit`. If 5,330 profile views had no
clear route to the store, that is the single largest loss in the whole account. **10-second
check, highest expected value on this page.**

**1b. The form still does not render — and the cause is smaller than first diagnosed.**
`get_form` on `WirxQ2` returns **form-level `status: "draft"`** (unmodified since 4 Sep) while
version `28374824` reads `live`. The version was published; the form never was. Klaviyo's
onsite script serves by form-level status, so nothing renders.

Targeting is **not** at fault — an earlier reading in this plan said it was, and that was
wrong. There are no page or URL conditions at all (`location: null`; triggers are only an
8s delay, device `both`, and a 14-day re-show).

Fix: flip the status on the sign-up forms **list** view. The builder's own publish control is
what has already failed twice on mobile, so do not go back through it. Then also:
`record_utm_params_on_submit` is still `false`, and one text block carries an inline
`color: rgb(0, 0, 0)` that overrides the corrected global gold — black on the `#080808` panel,
so that line is invisible. Confirm the fix with `query_form_values` returning non-empty.

**1c. The POS consent sync is broken — and this is now the top item.** An earlier version of
this plan said POS customers were not consenting. Wrong: only Klaviyo had been checked.
Shopify's `email_marketing_state:subscribed` returns the same customers Klaviyo reports as
`NEVER_SUBSCRIBED`, matched on creation timestamp to within three seconds. **They consented.
Shopify recorded it. Klaviyo is not receiving it.**

Shopify returned **50 subscribed customers and hit the API page limit** (so 50 is a floor)
against Klaviyo's emailable segment of **23**. At least 27 consented subscribers cannot be
reached from the sending tool.

Fix: Klaviyo → Integrations → Shopify → the subscriber/consent sync setting and its target
list. Profiles sync within seconds of each order, so the connection is healthy — it is the
marketing-consent field that is unmapped. Laptop job.

This ranks above the popup: the popup earns future subscribers, this releases customers who
have already bought and already said yes. The counter ask is still worth building as a habit,
but it is evidently already happening — the consent just has nowhere to land.

**1d. The sync's target list is double opt-in — fix this or 1c achieves nothing.** The
subscriber sync now targets `V9Rbbr` ("Email List"), which reads
`opt_in_process: "double_opt_in"`. Profiles pushed in receive a confirmation email and are not
`SUBSCRIBED` until it is clicked, which a counter customer will almost never do. Switch
`V9Rbbr` to **single opt-in**: every source feeding it is an explicit tick (onsite popup,
Shopify checkout) and Shopify retains the timestamped consent record either way.

**Backfill is not automatic.** The segment still read 23 immediately after the sync was
enabled, and Klaviyo's wording is forward-looking. If it has not moved after propagation time,
backfill explicitly — Shopify → Customers → filter email subscription = subscribed → export
CSV → import to `V9Rbbr` with consent. That relocates documented consent rather than
manufacturing it.

---

## Priority 2 — put the budget where the audience already is

Paid delivery is on the wrong platform. Organic Instagram is carrying the brand; paid is buying
Facebook.

| Action | Detail |
|---|---|
| **Reallocate to Instagram placement** | Warm Entry v2 delivered 100% Facebook. Split placement or duplicate to an IG-weighted ad set and compare cost/LPV directly |
| **Kill Warm Stack** | Reach 9 confirms the audiences are empty. Fold its budget into Broad AU |
| **Build an Instagram engagement audience first** | Not a website rebuild. `120247577486770688` / `120247577506740688` are gate-era and near-empty, but a website audience would only ever capture the site trickle. Organic Instagram put **5,330 profile views** through in two days — that is the real warm pool. An IG-account engagement audience (365 days) needs no URL rules and no pixel history, so it is buildable on a phone in ~90 seconds. Rebuild the website audiences later, on a laptop, as a secondary layer |
| **Hold total at $60/day** | Do not scale until Priority 1 is closed. Scaling into a leaking funnel is exactly what produced this week |
| **Leave Broad AU alone for now** | $2.30/LPV looks bad but it is n=2 clicks, conversion-optimised, zero purchase history, in learning. Judge on 7-day |

**Creative is the real constraint.** One image asset exists in the entire ad account
(`594e7f8e9e2eac3e1bc4340eacade4b6`). The organic content is clearly working — 17× lift proves
it. Target 4 statics + 1 video per ad set.

### The creative pool, ranked

**1. The scab/dry-skin application reel — build the next ad set around this.**
Cream applied to dry healing skin, which visibly settles. A *demonstration*, and demonstration
outperforms product photography in aftercare because it answers the only cold-audience question
— does this work — in three seconds with no copy. Highest expected performer in the pool.

> **Policy risk, flagged before anyone builds on it.** Meta restricts skin-condition and
> before/after content in ads (health and beauty policy), and close-up skin detail can also
> trip the shocking/sensational content rule. Mitigations: frame as product-in-use, never
> before/after (no split screens, no "day 1 / day 14"); do not lead on the most visceral
> frame; run it as **one ad among three or four** so a rejection costs an ad and not a
> campaign; appeal once if rejected, but have the alternative already live. None of this
> applies to the organic feed — only the paid cut needs the softer edit.

**2. The gate video that went viral organically — re-run it, do not retire it.**
The "it will look washed" concern is not supported by the delivery data:

| Day | Facebook | Instagram | Frequency |
|---|---|---|---|
| 9 Sep | $45.60 · 4,050 impr | **$0.01 · 2 impr** | 1.09 |
| 10 Sep | $39.35 · 3,528 impr | **$0.00 · 0 impr** | 1.10 |
| 11 Sep | $11.83 · 1,139 impr | **$0.01 · 3 impr** | 1.05 |

Frequency **1.05–1.10** means the average viewer saw it once; fatigue is a frequency-3+
problem. And as a *paid* ad it has never meaningfully run on Instagram — 5 impressions in
three days — so an IG run is a first run, not a repeat. A creative validated by organic virality
is the most valuable paid asset available: most advertisers pay to discover what works, this one
is already known. Retire on measured signals (frequency > 2.0 with rising cost per result),
never on a feeling.

**3. Product stills.** Seven public Shopify CDN images, six unused — see
`launch-weekend-measurement.md` for the frame-to-ad-set pairing.

**4. Callum's edits, when he returns.** They must land in **Shopify → Content → Files** to get
public CDN URLs, because Meta ingests creative by URL and the repo is not publicly served.
Request **4:5 and 9:16** crops: paid Instagram delivery only began 12 Sep and those are its
placements. The repo's 19 editorial stills (`DSC*.jpg`), the CHAPTER 1 frame and the founder
portrait need the same treatment. The two iPhone screen recordings carry UI chrome and need
recapture.

**Parked:** the TEL video drop release. Hold until the funnel captures and there is a warm pool
to hit twice — a launch asset deserves a working funnel under it.

### The one gate on scaling
Spend appetite is not the constraint and cost per click is strong. The single trigger is
**`query_form_values` returning submits**. Until then the funnel does not hold water, and last
week already demonstrated the cost of that: $96.80 into a page that could not capture an email.
Once it does, the guardrails below take over (+20% per 48h while CPA ≤ $25).

### Known platform limit
Conversion event / pixel / optimisation **cannot be edited on a published ad set** (Meta error
100, subcode 3260011). Both Ritual Drop ad sets published 9 Aug, so both are locked. Changing
the optimisation event requires **creating new ad sets**, not editing these. Supermetrics also
cannot read per-ad-set conversion events (`conversion_types` returns empty) — this must be read
in Ads Manager.

---

## Priority 3 — the structural gap

**One SKU, no bundle, no upsell, no subscription, on a consumable.** AOV is hard-locked at
$59.95. The reorder flow exists with nothing to reorder into. After capture is fixed, this is
the next piece worth real thought — it is the difference between a $60 AOV and a $120 one on
the same traffic.

---

## Remaining tasks

| # | Task | Owner |
|---|---|---|
| 1 | Judge.me — approve pending queue; auto-publish 4–5★, hold 1–3★ | Ben |
| 2 | Review requests — 40+ POS customers exist, only 14 on `WtAMQQ` | Ben |
| 3 | Confirm which Klaviyo account the upgrade billed to (possibly the wrong "King…" org) | Ben |
| 4 | #1046 — PayPal `SALE` stuck PENDING, $59.95. PayPal-side hold, not a gateway fault | Ben |
| 5 | **Confirm COGS per Ritual Duo** — the whole CPA model assumes ~$15 | Ben |
| 6 | Rename form (still "(DRAFT)" in title) and 3 mislabelled "(DRAFT)" flows | Either |
| 7 | Activate back-in-stock flow `SuavPL` | Either |

---

## Unit economics (unchanged, pending COGS confirmation)

| Metric | Value |
|---|---|
| AOV | $59.95 (free domestic shipping, so AOV = revenue) |
| Est. contribution margin | ~$45 at ~$15 COGS — **to confirm** |
| Break-even CPA | ~$45 |
| Target CPA to scale | ≤$20 |
| Kill threshold | >$35 CPA sustained 3 days |
| Break-even conversion rate | ~0.57% |

Measured: **$0.115/LPV**, 9.2% CTR, frequency 1.03–1.14. Exceptional buying, nowhere near
saturation. At 1% LPV→purchase that is a $11.50 CPA; at 0.5%, $23. The economics work — the
conversion rate is the unknown, and it is unknown because nothing has converted yet.

## Scaling guardrails (when Priority 1 is closed)

- Never move a budget **>20% in 48h** — larger jumps re-enter learning
- **7-day click** attribution; judge on the 7-day, never a single day
- Frequency ceiling **2.0** → refresh creative before touching budget
- Weekly: kill the bottom creative, add one new
- Switch Broad AU to PURCHASE only after ~30–50 add-to-carts accumulate
- Advantage+ Shopping only at ~50 purchases/7 days — under-fed ASC burns budget

---

## Verification

1. **`get_form` on `WirxQ2` returns form-level `status: "live"`**, not just a live version —
   then **`query_form_values` over `last_7_days` returns non-empty**, with rising views and
   submits. This is the one that matters most.
2. Instagram bio link resolves to `/products/tattoo-aftercare-kit`; `website_clicks` starts
   returning a number.
3. Klaviyo's emailable segment count converges on Shopify's subscribed-customer count, and
   new POS customers land in Klaviyo as `SUBSCRIBED` rather than `NEVER_SUBSCRIBED`.
4. A real order carrying `utm_campaign=ritual_drop_sep26` proves ads→checkout attribution.
5. Rebuilt custom audiences report a workable size and Warm Stack's replacement actually
   delivers (reach >> 9).
6. Placement split by `publisher_platform` shows Instagram taking meaningful spend, with
   cost/LPV compared against Facebook's $0.115.
7. T+48h: `data_query` by ad set for spend, ATCs and purchases.

## Account security

A Meta-impersonation phishing DM arrived on 25 Aug and was verified as a scam the same
night. The rule and the account-hardening checklist live in `README.md` under
**Account security — Meta impersonation**.

## Morning fire — armed

Routine `trig_01VLuY5aCWg5xHrNfgLRTD5a`, firing **08:54 AEST Sun 13 Sep** into this session.
Written to **verify rather than assume**, because three separate settings tonight read as saved
while the API showed them unchanged.

It checks, in order:
1. Whether last night's saves actually applied — `get_list` on `V9Rbbr` for
   `opt_in_process: single_opt_in` (reported saved, never re-read), and `get_form` on `WirxQ2`
   for form-level status.
2. Whether the consent chain moved — segment `YgyR87` (was 23) and list `V9Rbbr` (was 24)
   against Shopify's subscribed count (50+, page-limited), plus whether any overnight POS
   customer landed `SUBSCRIBED`.
3. `query_form_values` on `WirxQ2` — empty still means not rendering.
4. Whether `website_clicks` has stopped returning `null` now the bio is updated, and whether
   the organic profile-view lift is holding or decaying.
5. Ad delivery split by `publisher_platform` — Instagram cost/LPV against Facebook's $0.115.
6. Overnight orders: any web order at all, any `ritual_drop_sep26` UTM, any `TELTAKEOVER`
   redemption. Inventory was 439.

It is instructed to flag any save that did not apply, and it carries the standing rule below.

---

## Standing rule

Nothing spends, sends or goes live without Ben's word.
