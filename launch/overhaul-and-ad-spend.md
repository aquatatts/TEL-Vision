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
| Form `WirxQ2` | `status: live` but `query_form_values` → `results: []`. **Still not rendering** |
| Emailable segment | 20 → **23** (+3) |
| New profiles since 11 Sep | 9, of which 8 read `NEVER_SUBSCRIBED` in Klaviyo — but **subscribed in Shopify**. Sync fault, see 1c |
| CAPI | Already Maximum on the Shopify F&I channel |
| Checkout / shipping / channels / pixel | All healthy, confirmed by live read |

---

## Priority 1 — stop the leak (before another ad dollar scales)

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
it. Feed the ad account the material that is already performing organically: 14 high-res
editorial photographs in the repo, the CHAPTER 1 frame, the founder portrait. Target 4 statics
+ 1 reel per ad set. The two iPhone screen recordings carry UI chrome and need recapture.

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

## Standing rule

Nothing spends, sends or goes live without Ben's word.
