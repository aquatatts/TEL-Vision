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

## Capture is still broken

Form `WirxQ2` reads `status: "live"` — it was published on 12 Sep — but
`query_form_values` over `last_7_days` returns `results: []`. Zero views, zero submits, ever.

**Publication is therefore not the problem; the display rules are.** They were authored while
the store was password-gated, so the trigger and targeting conditions no longer match any page
on the open store. This is the top remaining fix.

### The consent gap
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
