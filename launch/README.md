# TEL Collection — Chapter One launch runbook

Drop: **Thu 10 Sep 2026, 7:00pm AEST.** Founding window closes **Mon 14 Sep 23:59 AEST.**
Written post-launch, from live reads. Every number here came from an API pull, not memory.

## What happened

The Klaviyo sequence fired exactly on schedule. The problem was the size of the room.

| Campaign | Recipients | Opens | Clicks | Revenue |
|---|---|---|---|---|
| T-1 "This time tomorrow" | 21 | 5 (25%) | 0 | $59.95 |
| Doors Open — Founding Price (7:00pm) | 20 | 5 (25%) | 0 | $0 |
| Chapter One Review Ask | 14 | 1 | 0 | $0 |

`TEL — Emailable (subscribed)` is the entire owned list: **20 people.**

## Root cause: no email capture, ever

Klaviyo holds exactly one signup form — `TEL · First access popup` (`WirxQ2`,
version `28243577`) — **status: draft**, created 4 Sep, never updated.
`query_form_values` returns an **empty result set** for the last 30 days: zero views,
zero submits, never shown to anyone.

~1,300 paid landing page views at $0.13 each arrived at a page with no way to leave an
email address. That is the leak. It is not a conversion-rate problem; there was no form.

Note the form was written as a **"First access" popup for a password-gated store**. The
store is now open, so its copy must change before it is published.

## Meta: the sales campaign never ran

`TEL | SLS | Ritual Drop` is still `PAUSED` with **zero ads in both ad sets**. Meanwhile the
traffic campaign kept spending through launch:

| Date | Spend | Landing page views |
|---|---|---|
| Wed 9 Sep | $45.61 | 349 |
| Thu 10 Sep (launch) | $39.35 | 309 |
| Fri 11 Sep | $11.84 | 99 |

$96.80 over three days. Neither web order carries a Meta UTM, so zero attributable orders.

## Sales since doors opened

Two web orders, both full $59.95 — one direct, one from Google. One POS at $59.95.
**`TELTAKEOVER` has zero redemptions.** Order **#1046 is PENDING and unpaid.**

## The email/price split

Squires clients are emailed from **Mailchimp** at $59.95, where their consent and the
sending reputation live. Klaviyo sends only to TEL opt-ins at the $49.99 founding price.
Every Klaviyo campaign already excludes list `WjZxaE`, which enforces the split.

`TELTAKEOVER` is a **single shared code** — if it appears anywhere in the Squires email,
including image alt text, the split collapses.

## Connector limits worth knowing

- **Mailchimp cannot send from the API.** No send or schedule tool, and `campaign_planner`
  refuses single-campaign requests. A human presses send.
- **Supermetrics drops its tools on reconnect.** Meta reads/writes go dark without warning
  mid-session; re-load via ToolSearch before trusting a "not available" conclusion.
- Supermetrics `conversion_types` reports zero pixels on this account. That is a reporting
  gap — LPV optimisation proves the pixel fires. Do not re-flag it.

## ID inventory

| Thing | ID |
|---|---|
| Shopify store | telcollection.com.au · AUD · AEST · Basic |
| Ritual Duo | `gid://shopify/Product/8235149754431` · variant `43455141969983` · SKU `TEL-RD-60` · $59.95 · 448 units |
| Product handle | `/products/tattoo-aftercare-kit` |
| Founding discount | `TELTAKEOVER` · `gid://shopify/DiscountCodeNode/1370178715711` · $9.96 off → $49.99 · ends 2026-09-14T13:59Z |
| Meta ad account | `act_2121305908740756` |
| Meta page | `1184411344764247` (TEL Collection) |
| Ritual Drop (SALES, paused, $20/day) | `120247236202470688` |
| — Broad AU — contingency | `120247236203480688` |
| — Warm Stack — all custom audiences | `120247236203130688` |
| Warm Entry v2 (TRAFFIC) | `120247501786430688` · ad set `120247501786710688` |
| Custom audience — gate visitors 30d | `120247577486770688` (reports size 20) |
| Custom audience — gate visitors 180d | `120247577506740688` (reports size 20) |
| Klaviyo account | `TbNLXf` · sender info@telcollection.com.au |
| Conversion metric | `Y5U9sG` |
| Segment — TEL Emailable | `YgyR87` (20 profiles) |
| List — Email List (double opt-in) | `V9Rbbr` |
| List — Squires Ink import (NO founding price) | `WjZxaE` |
| List — Chapter One Review Ask | `WtAMQQ` |
| Form — First access popup | `WirxQ2` / version `28243577` — **DRAFT** |
| Flow — Back in stock | `SuavPL` — **draft** |
| Flows live but named "(DRAFT)" | `Vg9tuX`, `YgAs6b`, `TEZ6PM` |

## Order of operations for the next drop

1. **Publish the capture form before spending a dollar on traffic.** Verify with
   `query_form_values` returning non-empty. This is the step that was missed.
2. Build ads into the sales campaign before launch night, and confirm a non-empty `ads`
   array by re-reading with `campaign_detail_level: full`.
3. Verify custom audiences clear ~1,000 before relying on a warm ad set.
4. Put UTMs on every link, email and ad, or attribution lands in "direct".
5. Prove the money path with one real end-to-end purchase using the discount code.

---

## Build log — Sat 12 Sep 2026, ~11:10 AEST

Ads built into `TEL | SLS | Ritual Drop` (`120247236202470688`). `write_status: applied`.
Campaign, both ad sets and both ads all remain **PAUSED** — nothing is spending.

| Ad | ID | Ad set | Review |
|---|---|---|---|
| Ritual Duo — Doors Open (warm) | `120247952594970688` | Warm Stack `120247236203130688` | IN_REVIEW |
| Ritual Duo — Look After The Art (broad) | `120247952595560688` | Broad AU `120247236203480688` | IN_REVIEW |

Both carry CTA `SHOP_NOW`, land on `/products/tattoo-aftercare-kit`, and are tagged
`utm_source=meta&utm_medium=paid_social&utm_campaign=ritual_drop_sep26` with
`utm_content=warm_stack` / `broad_au`. Review started now rather than at enable time, so the
ads should be approved and ready when the budget decision is made.

Creative: the ad account's asset library returns empty via the API, so the image was supplied
as a public `asset_url` — the Shopify product hero. Meta downloaded and stored it as
asset `594e7f8e9e2eac3e1bc4340eacade4b6`, now reusable by ID for future ads.

### Still needs Ads Manager

**The pixel cannot be reached from the API.** `conversion_types` returns
`{"conversions": [], "pixels": []}` on every call, confirmed across separate connector
sessions. Setting an ad set's `promoted_object` requires a `pixel_id`, so the per-event
optimisation split cannot be written from here:

- Warm Stack → **Purchase**
- Broad AU → **Add to cart** for the first 48–72h, then Purchase at ~30–50 purchases

Both ad sets currently sit at `OFFSITE_CONVERSIONS` with whatever event was already bound.
Check and set the event in Ads Manager at the same time as the audience-size check.

---

## Build log — Sat 12 Sep 2026, ~23:30 AEST

**The ads above are no longer paused.** Both ads passed review (`review.status: APPROVED`) and
the campaigns were enabled on Ben's word after the ad account's billing was rectified:

| Campaign | ID | Status | Budget |
|---|---|---|---|
| TEL \| SLS \| Ritual Drop | `120247236202470688` | **ENABLED** | $40/day CBO |
| TEL \| TRF \| Warm Entry v2 | `120247501786430688` | **ENABLED** | $20/day CBO |

Three things were fixed between the entry above and this one:

1. **Capture form published.** `WirxQ2` moved draft → `status: "live"`. It still renders
   nothing (`query_form_values` → `results: []`), so the remaining fault is the **display
   rules**, authored while the store was password-gated.
2. **Ad account billing.** The account had entered a grace period and Meta had switched both
   campaigns **off** — they do not self-resume. Card paid and set primary.
3. **CAPI.** Already at **Maximum** on the Shopify Facebook & Instagram channel, with advanced
   matching and Conversions API active. No change needed; the earlier assumption was wrong.

### The measurement that changed the plan

Launch-weekend Instagram attention was **100% organic** — 2,612 and 2,718 profile views on
10–11 Sep against a 91–152/day baseline, while paid Instagram delivery those days was $0.00
and $0.01. The whole budget was on Facebook placement.

Full numbers, the consent gap, and the corrections log: **`launch-weekend-measurement.md`**.

### Open at time of writing

| Item | Where |
|---|---|
| Form display rules — the top fix | Klaviyo UI · `capture-form-fix.md` |
| Verify IG bio link → `/products/tattoo-aftercare-kit` | Instagram app |
| POS consent capture — 8 of 9 customers `NEVER_SUBSCRIBED` | Studio counter |
| Rebuild custom audiences against the open store + IG engagers | Ads Manager |
| Per-ad-set conversion event — needs **new** ad sets, cannot be edited | Ads Manager |
| Confirm COGS per Ritual Duo (CPA model assumes ~$15) | Ben |
| #1046 PayPal `SALE` stuck PENDING, $59.95 | PayPal |
| Which Klaviyo org the upgrade billed to (possibly the wrong "King…" account) | Klaviyo billing |
