# Launch weekend — what the numbers actually say

Measured Sat 12 Sep 2026, ~23:30 AEST, three days after doors opened (Thu 10 Sep, 7pm AEST).
Every figure below comes from a live API read, not a dashboard screenshot. Where a metric could
not be read, that is stated rather than estimated.

---

## The headline finding: the launch audience was organic, and paid was on the wrong platform

Instagram profile views, TEL account `17841420943769985` (ds_id `IGI`), against paid delivery
split by `publisher_platform` on the ad account `act_2121305908740756` (ds_id `FA`):

| Date | IG profile views | Accounts engaged | IG paid spend | IG paid impressions | FB paid spend |
|---|---|---|---|---|---|
| 6 Sep | 150 | 3 | — | — | — |
| 7 Sep | 91 | 3 | — | — | — |
| 8 Sep | 145 | 5 | — | — | — |
| 9 Sep | 152 | 3 | $0.01 | 2 | $45.60 |
| **10 Sep — doors open** | **2,612** | **51** | **$0.00** | **0** | $39.35 |
| **11 Sep** | **2,718** | **52** | **$0.01** | **3** | $11.83 |
| 12 Sep (partial) | 459 | 5 | $4.73 | 182 | $6.09 |

**5,330 Instagram profile views across 10–11 Sep were bought with $0.01 of Instagram ads.**
17× the 91–152/day baseline, sustained two full days, entirely organic.

Over those same two days, $51.18 of Facebook placement produced ~408 landing page views.
Organic Instagram out-delivered the entire paid budget by roughly 13× on volume, at no cost —
and not one budget dollar was pointed at the platform doing the work.

12 Sep is the first day Instagram has taken real paid delivery ($4.73 / 182 impressions), all
of it from the new `Broad AU — contingency` ad set.

### What this changes
The strategic assumption going into launch was that paid would build the audience and email
would convert it. The data says the opposite is happening: **organic Instagram is the demand
engine.** The paid budget's job is to amplify what is already proven organically, and the
retarget pool worth building is IG engagers — not the gate-era website audiences.

---

## Conversion: the attention is not the constraint

5,330 organic profile views + ~408 paid landing page views over launch weekend produced
**2 web orders**. Zero `TELTAKEOVER` redemptions, ever.

Two candidate leaks, in order of expected value:

1. **The Instagram → store path is unverified.** `website_clicks` returned `null` for all seven
   days queried on `IGI`. This cannot be distinguished from the API: either the metric is
   unavailable on this source, or there were genuinely no profile-link clicks. Needs a manual
   check that the bio link exists and lands on `/products/tattoo-aftercare-kit`.
2. **Nothing is captured, so there is no second attempt.** See below.

---

## Capture is still broken — root cause found

`query_form_values` over `last_7_days` returns `results: []`. Zero views, zero submits, ever.

A direct read of `get_form` on `WirxQ2` shows **two statuses that disagree**:

| Object | Status | Last modified |
|---|---|---|
| Form `WirxQ2` | **`draft`** | **2026-09-04T14:46:47** |
| Version `28374824` | `live` | 12 Sep |

**The version is live; the form is not.** The form record has not been modified since 4 Sep,
which matches the reported symptom exactly — "when I click publish it does nothing". The
publish action updated the version and never committed at the form level. Klaviyo's onsite
script serves forms by **form-level** status, so nothing is ever rendered.

### Correction to an earlier reading in this project
An earlier entry in this file and in the plan stated that the form was live and that the
**display rules** were at fault, having been written for the password-gated store. **That was
wrong.** The targeting carries no page or URL conditions at all:

```
location: null
triggers: delay 8s · device both · after_close_or_submit_timeout 14 days
rule_based_trigger_evaluation: any
```

Targeting is wide open and blocks nothing. The single fault is the form-level status. The fix
is a status toggle on the sign-up forms **list** view, not an edit inside the form builder —
and the builder's own publish control is the thing that has already failed twice on mobile.

### Two further faults in the same read

1. **`record_utm_params_on_submit: false`.** Still off. Without it, a subscriber cannot be
   attributed back to the ad or email that produced them.
2. **One text line renders invisible.** The global body colour was corrected to `#C9A24B`, but
   the block retains an inline `color: rgb(0, 0, 0)`, and inline style overrides global. On the
   `#080808` panel background, "One email a run. Nothing else." is black on black. The same
   block carries two trailing empty paragraphs.
3. The form name still contains "(DRAFT)", which is why the list reads as unpublished at a
   glance even once the status is flipped.

### The consent gap is a SYNC FAULT, not a capture fault

**This supersedes the reading below it.** An earlier entry here concluded that POS customers
were not consenting and therefore could not legally be emailed. That was wrong, and wrong
because only Klaviyo was checked. Shopify tells a different story.

Filtering Shopify customers on `email_marketing_state:subscribed` returns the same people
Klaviyo reports as `NEVER_SUBSCRIBED`, matched by creation timestamp to within three seconds:

| Created (UTC) | Shopify consent | Klaviyo consent |
|---|---|---|
| 12 Sep 08:55:59 | **subscribed** | `NEVER_SUBSCRIBED` |
| 12 Sep 09:21:52 | subscribed | `SUBSCRIBED` — the one that synced |
| 12 Sep 11:31:46 | **subscribed** | `NEVER_SUBSCRIBED` |
| 12 Sep 12:23:21 | **subscribed** | `NEVER_SUBSCRIBED` |
| 12 Sep 12:30:59 | **subscribed** | `NEVER_SUBSCRIBED` |
| 12 Sep 12:51:30 | **subscribed** | `NEVER_SUBSCRIBED` |
| 12 Sep 13:02:07 | **subscribed** | `NEVER_SUBSCRIBED` |

**The customers consented. Shopify recorded it. Klaviyo did not receive it.** There is no legal
problem — the consent exists and is documented. The problem is that it is stranded in the
wrong system.

**Scale of the gap:** `email_marketing_state:subscribed` returned **50 rows and hit the API
page limit**, so 50 is a floor, not a total. Klaviyo's emailable segment `YgyR87` reads **23**.
At least 27 consented subscribers are unreachable from the sending tool, likely many more. The
exact figure is visible in Shopify → Customers filtered on email subscription = subscribed.

**Fix:** Klaviyo → Integrations → Shopify → the subscriber/consent sync setting, and the list
it syncs into. Profiles are being created within seconds of each order, so the integration
itself is healthy; it is specifically the marketing-consent field that is not being mapped.

This now ranks **above** the popup fix. The popup earns future subscribers; this releases
customers who have already bought and already opted in.

### Second gate behind the sync: the target list is double opt-in

The subscriber sync was enabled on 13 Sep and correctly targets list `V9Rbbr` ("Email List").
But that list reads:

```
opt_in_process: "double_opt_in"
```

Every profile Shopify pushes into it therefore receives a confirmation email and is **not**
`SUBSCRIBED` until it is clicked. A customer who ticked a box at the counter and left will
almost never click an unexpected confirmation, so the sync hands people over and the list holds
them pending. The plumbing is fixed and a valve two feet further along is still shut.

Counts consistent with this: list `V9Rbbr` **24**, emailable segment `YgyR87` **23** — one
member on the list who cannot be emailed.

**Fix: switch `V9Rbbr` to single opt-in.** Double opt-in exists for sources where it is unclear
whether the address owner asked. Every source feeding this list is an explicit tick — the onsite
popup and Shopify checkout — and Shopify retains the consent record with timestamps regardless,
so the confirmation step buys nothing and costs most of the list.

### Backfill is not automatic

Immediately after enabling the sync the segment still read **23** — the existing 50+ Shopify
subscribers had not moved. Klaviyo's own wording in the setting is forward-looking ("site
visitors that subscribe ... **will be** subscribed"), so this setting should be assumed to catch
new subscribers only.

If the count has not moved after propagation time, backfill explicitly: Shopify → Customers →
filter email subscription = subscribed → export CSV → import to `V9Rbbr` in Klaviyo with
consent. This relocates consent that Shopify already documents with timestamps; it does not
manufacture it.

### Klaviyo-side consent as read (for reference)
Profiles created since 11 Sep, with `subscriptions.email.marketing.consent`:

| Created (UTC) | Consent | Method |
|---|---|---|
| 11 Sep 05:44 | NEVER_SUBSCRIBED | — |
| 11 Sep 13:10 | NEVER_SUBSCRIBED | — |
| 12 Sep 08:56 | NEVER_SUBSCRIBED | — |
| **12 Sep 09:21** | **SUBSCRIBED** | **SHOPIFY / Customer Webhook** |
| 12 Sep 11:31 | NEVER_SUBSCRIBED | — |
| 12 Sep 12:23 | NEVER_SUBSCRIBED | — |
| 12 Sep 12:31 | NEVER_SUBSCRIBED | — |
| 12 Sep 12:51 | NEVER_SUBSCRIBED | — |
| 12 Sep 13:02 | NEVER_SUBSCRIBED | — |

**8 of 9 are `NEVER_SUBSCRIBED`.** These are paying customers whose email address sits in
Klaviyo and who cannot legally be marketed to. The single opt-in came through the Shopify POS
customer webhook, not the popup.

Segment `YgyR87` (TEL — Emailable): **20 → 23**. Three net new in three days.

POS is where 100% of real revenue happens, and it is capturing consent on roughly one customer
in nine. A deliberate opt-in ask at the counter is worth more than the whole paid budget —
every Squires client is already a proven TEL buyer.

---

## Orders, Sat 12 Sep

| Order | Time (UTC) | Value | Source |
|---|---|---|---|
| #1048 | 08:56 | $59.95 | pos |
| #1049 | 11:32 | $59.95 | pos |
| #1050 | 12:32 | $59.95 | pos |
| #1051 | 12:52 | $59.95 | pos |
| #1052 | 13:03 | $59.95 | pos (AUTHORIZED) |

**$299.75, all POS.** Three of five landed inside 31 minutes (22:32–23:03 AEST) — a late
Saturday studio cluster. No web orders, no `ritual_drop_sep26` UTM, no discount redemptions.

---

## Paid delivery after the billing fix

The ad account entered a billing grace period and Meta switched the campaigns **off** — they do
not self-resume. Spend history: 9 Sep $45.61 → 10 Sep $39.35 → 11 Sep $11.84 → 12 Sep zero
until the card was rectified and made primary on the evening of 12 Sep.

First evening of restored delivery:

| Ad set | Spend | Impressions | Reach | Clicks | LPV | Freq | Cost/LPV |
|---|---|---|---|---|---|---|---|
| Warm Entry v2 — AU | $4.58 | 432 | 402 | 44 | 40 | 1.07 | **$0.115** |
| Broad AU — contingency | $4.60 | 259 | 228 | 3 | 2 | 1.14 | $2.30 |
| Warm Stack — all custom audiences | $1.33 | 13 | 9 | 0 | 0 | 1.44 | — |

**Warm Entry v2 at $0.115/LPV beats its own historical $0.13.** The buying is genuinely good.

**Warm Stack is confirmed dead.** Reach 9 on $1.33 across a full evening with budget available
settles the earlier open question: the custom audiences `120247577486770688` (30d) and
`120247577506740688` (180d) really are near-empty, not a Supermetrics placeholder. They were
built against the password-gated store's URLs. Rebuild against the open store plus IG engagers.

**Broad AU's $2.30/LPV is not yet a verdict** — n=2 clicks, conversion-optimised, zero purchase
history in the pixel, still in learning. Judge it on the 7-day.

Placement split for the same evening shows why: Warm Entry v2 delivered **100% Facebook**
(444 impressions, 0 on Instagram), while Broad AU split 169 Instagram / 99 Facebook.

---

## Corrections to earlier readings in this project

Recorded so they are not repeated.

| Earlier claim | Reality |
|---|---|
| "Zero pixels on the ad account" | Supermetrics `conversion_types` returns empty on every call — a connector scope limit. 1,277 LPVs on 1,390 clicks proves the pixel fires |
| "Onsite tracking is live" | The metrics existed but had fired 0 events in 5 weeks. Existence ≠ events |
| "CAPI is almost certainly off" | Already set to **Maximum** on the Shopify F&I channel |
| "Meta resumes delivery once billing clears" | Meta switches campaigns **off** and they stay off |
| "Warm Stack should carry the launch" | Reach 3 in two hours. Retracted |
| "The audiences reading size 20 is an artefact" | It was real |
| "The Squires list has never been emailed about TEL" | Already sent 10 Sep 04:45 |
| "I can set the per-ad-set conversion event" | Meta error 100 / subcode 3260011 — locked on published ad sets |

---

## Known API limits in this stack

- **`conversion_types` (FA)** returns `{"conversions": [], "pixels": []}` always. Pixel and
  per-ad-set conversion events must be read in Ads Manager.
- **Conversion event / pixel / optimisation cannot be edited on a published ad set** (error 100,
  subcode 3260011). Both Ritual Drop ad sets published 9 Aug, so both are locked. Changing the
  optimisation event requires **creating new ad sets**.
- **`website_clicks` (IGI)** returns `null`. Cannot confirm profile-link clicks from the API.
- **`create_form` (Klaviyo)** pins `status` to `"draft"`; there is no publish endpoint. Publish
  and display rules are UI-only.
- **Mailchimp connector** exposes no send or schedule tool. Sends are manual.
- **Egress** to `telcollection.com.au` is blocked by the proxy; storefront state must be
  verified through the Shopify Admin API.

---

## Creative: the bottleneck is solvable immediately

The ad account contains **one** image asset (`594e7f8e9e2eac3e1bc4340eacade4b6`, the product
hero). Creative variety is the single biggest performance driver in a Meta account, and every
ad in TEL has been running the same frame.

The Ritual Duo product already carries **seven public Shopify CDN images**, all with written
alt text. Meta can ingest any of these by `asset_url` — that is exactly how the existing asset
was created, so the path is proven. Six are unused:

| # | Shot | Status |
|---|---|---|
| 01 | Sealed set hero — both jars, monogram card behind | **in use** |
| 02 | Both jars front-on | unused |
| 08 | Restore Balm front, Recovery Cream angled to show ingredient panel | unused |
| 09 | Sealed retail box, front-on | unused |
| 12 | Open jar, top-down — cream texture macro | unused |
| 13 | Restore Balm single jar under studio light | unused |
| 15 | Both jars on the retail box with the metal card | unused |

Base path: `https://cdn.shopify.com/s/files/1/0669/8870/3807/files/tel-ritual-duo-*`

Recommended pairing, matching each frame to the job it does:

- **Broad AU (cold)** → 09 sealed box and 02 both jars. Cold traffic needs to understand what
  arrives in the parcel before it needs atmosphere.
- **Warm/retarget** → 12 texture macro and 08 ingredient panel. A warm viewer already knows the
  product; these answer "is it any good", which is the objection that actually blocks the sale.
- **Organic-style** → 13 single jar and 15 jars on box read least like an ad, which matters
  given that organic Instagram is the channel actually working.

Also available and stronger, but not yet Shopify-hosted: **19 high-res editorial tattoo
photographs** in the repo root (`DSC*.jpg`), the **CHAPTER 1 — LOOK AFTER THE ART** frame
(`IMG_9030(1).png`), and the founder portrait. These carry the "look after the art" proof that
product-only shots cannot. They need uploading to Shopify Files (or any public host) first,
because Meta pulls by URL and the repo is not publicly served. The two iPhone screen recordings
carry UI chrome and need recapture before any paid placement.

**Deliberately not built tonight.** Adding ads means writing to campaigns that are now live and
delivering at $0.115/LPV. A malformed `manage_campaign` payload at midnight risks stopping
delivery overnight for no gain, since nothing can be judged before morning anyway. The URLs
above make this a five-minute job in daylight.

---

## Inventory

Ritual Duo variant `43455141969983`: **439 units** (was 445). Six units moved, consistent with
the five POS orders on 12 Sep plus one earlier. No sellout risk — which is why the launch copy
deliberately carries no scarcity claim.

---

## Automation audit — verified by delivery data, 13 Sep

Seven flows in the account. Status checked at **both** flow and message level, then confirmed
against `get_flow_report` over 90 days — because a `status: live` flow can still hold draft
messages, and three settings this night read as done while the API said otherwise.

| Flow | Status | Delivered (90d) | Verdict |
|---|---|---|---|
| `WnAETh` Post-purchase: The Healing Guide | live / msg live | **14** · 7 opens (**50%**) · 0 clicks | **Working** |
| `UpBgzj` Post-purchase: The Long Stage (reorder) | live / msg live | 0 | **Correct** — 50-day delay, first sends due ~8–11 Oct |
| `TEZ6PM` Welcome: The standard | live | 5 · 3 opens · 2 clicks · **1 conversion $59.95** | Working |
| `TPwqqq` Post-purchase (ONLINE): The Healing Guide | live / msg live | 0 | **Untested** — triggers on fulfilment; only 2 web orders ever, one a stuck PayPal |
| `Vg9tuX` Abandoned checkout | live | 0 | Untested — no abandoned carts of consequence yet |
| `YgAs6b` Browse abandonment | live | 0 | Untested — onsite tracking only just enabled |
| `SuavPL` Back in stock | **draft** | — | Not activated. 439 units, so no urgency |

### The real gap: there is no review-request flow
**None of the seven flows asks for a review.** The list `WtAMQQ`
("Chapter One - Review Ask (Aug backfill)", 16 members) exists with nothing driving it.

Judge.me is installed and may be sending review requests independently of Klaviyo — **check
Judge.me before building a Klaviyo flow**, or the two will double up on the same customer.

This is the automation worth building next. Reviews on the PDP are what convert the cold
traffic the ads are buying, and there are 40+ POS customers who have already used the product.

### Correction recorded
An earlier reading of `WnAETh`'s trigger JSON concluded the two `Source Name` equals conditions
sat in one AND group and could therefore never both be true, i.e. that the flow could never
fire. **That was wrong** — delivery data shows 14 recipients. The API's representation of
same-field metric-property conditions does not map to AND the way the raw JSON suggested.
**Lesson: read flow behaviour from `get_flow_report`, not from trigger JSON.**

### Worth watching
- `WnAETh`: **0 clicks on 14 delivered** at a 50% open rate. Read and not clicked, so the guide
  generates no return traffic and no path to reorder. Consider a single clear link.
- Once web orders start flowing, check whether `TPwqqq` and `WnAETh` both fire for the same
  online buyer — their source filters are written as mirror images and may overlap. Not a
  present problem at 0 sends.
