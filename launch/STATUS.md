# TEL Collection — current state

**Read this file first.** Last verified: **Sun 13 Sep 2026, 13:40 AEST** (deep audit).

The dated sections below are appended in order and **later entries supersede earlier ones** — where
they disagree, the later one was the verified read. The tables immediately below are kept current.

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
| 1 | **The Klaviyo onsite script has never run** | **ROOT CAUSE, found 13 Sep.** `Viewed Product` and `Active on Site` = **0 events in three months**. Every server-side Shopify event fires; every onsite-JS event is zero. This is why form `WirxQ2` does not render — **and why rebuilding it would not have helped.** First check: does the theme's app embed carry public key `TbNLXf`? |
| 2 | ~~**Consent stranded**~~ | **FIXED AND SIGNED OFF 13 Sep.** Two-sided check passes: Shopify **57** subscribed vs Klaviyo **56** emailable — a gap of 1, against 27+. *Still open:* the auto-sync is inconsistent, not proven — see UNTESTED |
| 3 | **No reviews integration in Klaviyo** | All 37 Klaviyo metrics are Shopify / Klaviyo-internal / onsite-API. No Judge.me connector, no review metric, no flow that asks. **This does not mean no reviews** — Judge.me collects and displays them independently: 6 reviews at 5.0, live on the product page. Correction logged below |
| 4 | **Warm Stack audiences empty** | Reach **9** on $1.33. Targeting re-read 13 Sep: **still pointed at `TEL - gate visitors 30d` and `tel gate visitors 180d`.** Never swapped |
| 5 | `record_utm_params_on_submit: false` | Subscribers cannot be attributed to the ad or email that produced them. *(Ad-side UTM tagging is correct — this is the form only)* |
| 6 | One form text line invisible | Inline `color: rgb(0,0,0)` overrides the corrected global gold, on a `#080808` panel |
| 7 | Order #1046 | PayPal `SALE` stuck PENDING, $59.95. PayPal-side hold, not a gateway fault |
| 8 | `WjZxaE` Squires exclusion list | **0 members** — the price-split guard was empty. Harmless (separate platforms) but not to be relied on |
| 9 | **Ritual Drop is not delivering** | $40 of the $60/day budget. **$6.43 spent in eight days.** Reads ENABLED with ACTIVE, APPROVED ads — nothing in config explains it. Needs one look at the Delivery column in Ads Manager |
| 10 | **No web order has ever come from the open store** | Both web orders first landed on `/password` — gate-era traffic. Not "2 web orders since launch"; **zero** |
| 11 | **Browse abandonment `YgAs6b` can never fire** | Live, triggers on `Viewed Product`, which has never once occurred. Dead until the onsite script runs |
| 12 | **Abandoned checkout `Vg9tuX` is skipped, not broken** | Flow, trigger, guard and all 3 emails read correct. **5 `Skipped Send` events** prove it triggers and Klaviyo declines — recipients were not subscribed. Fix is checkout consent capture, not the flow |
| 13 | **The import sent 39 unauthorised emails** | The 01:59 backfill triggered `Added to List` on the live welcome flow. 33 welcome + 6 healing guide. **Checked: no discount code, no offer — commercial cost nil.** Process rule now recorded: pause Added-to-List flows before any import |
| 15 | Flow emails carry no UTM tags | The welcome email's button is a bare product URL. Email-driven purchases are unattributable |
| 14 | Sending domain DNS unverified | All 5 records `verified: false`. **Not currently harmful** — 100% delivery, 1 bounce in 132, 0 spam. Finish it for durability, do not blame it for anything |

## UNVERIFIED — reported saved, never re-read

- `V9Rbbr` → single opt-in — **CLEARED.** Re-read by API 13 Sep: `opt_in_process: single_opt_in`
- `V9Rbbr` → global unsubscribe ticked — **CLEARED**, confirmed in the list settings
- Instagram bio updated — changed, but `website_clicks` returns `null` on every day and that is
  an **API limitation of the `IGI` source**, not a pending answer. Link clicks must be read in
  the Instagram app directly

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
| **Auto consent sync on a new sale** | The backfill used `method: LIST_IMPORT`. On the next POS sale, read the new profile: `method: SHOPIFY` = the sync is fixed; `NEVER_SUBSCRIBED` = still broken and every future counter sale strands again |
| `TEL — IG engagers 365d` | Built 13 Sep, reads **Below 1000**. Unusable for targeting until it grows. Re-check ~13 Oct |

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

1. ~~CSV backfill the stranded subscribers~~ — **DONE 13 Sep.** 24 → 58
2. ~~Judge.me review display~~ — **DONE.** Star rating now sits under the price; reviews were
   already on the page via a custom section
3. **The end-to-end test above** — a real order, real email, through every entry point. The one
   remaining thing that has never been done, and the one that would catch the next fault
4. Rebuild form `WirxQ2` from scratch (lowest value of the open items — sequence it last)
5. Star colour → brand gold `#C9A24B` (cosmetic)

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

---

## CORRECTION — the reviews were already displaying. 13 Sep, 12:38 AEST

**The preceding Judge.me entry is wrong and is superseded by this one.** It claimed six reviews
existed that "nobody can see". They were visible the whole time.

### What is actually on the product page
A custom-built `TEL - Reviews` section, and it is **better than the Judge.me default widget**:

- **"FROM THE FIRST FIVE HUNDRED — Every review so far. Five stars."**
- *"Collected by Judge.me after purchase and from our Google Business Profile. Published as
  written."*
- A **★★★★★ 5.0 OF 5 · 6 REVIEWS** badge
- Featured reviews with attribution and **VERIFIED BUYER** tags
- Google Business reviews merged alongside Judge.me ones
- **"EVERY REVIEW — Newest first. Nothing edited."** followed by all six, one with a customer
  photo of healed work

### How the error happened
Judge.me's setup guide listed "Enable Reviews Widget" as incomplete. That checklist measures
**whether Judge.me's own widget is installed** — not whether reviews appear on the site. The
site displays them through custom section code instead, so the checklist is permanently
unticked and permanently misleading.

**This is the third time today a vendor UI reported a state that was not real** (Klaviyo's
"Enable forms on website", the browser's theme preview, and now this). The difference is that
the first two were verified before acting and this one was not: the product page itself was
never opened before the claim was written down. **Rule 1 of the verification standard exists
for precisely this and was skipped.**

### The one genuine gap, now closed
No star rating appeared **near the price**, above the fold — a cold visitor saw the price with
no rating before deciding whether to scroll. Fixed by adding the Judge.me **Star Ratings** block
directly beneath `Price` in the `Product page` section on `TEL v6.2`.

**Verified rendering:** the live preview now reads
`The Ritual Duo` → `$59.95` → **★★★★★ 6 reviews**.

### Outstanding, cosmetic
The stars render in Judge.me's default **teal**, against a page otherwise built entirely on the
brand gold `#C9A24B`. Set the star colour in the block settings, or in Judge.me → widget
appearance.

### Do NOT add the Judge.me Review Widget
It would duplicate the custom section and present the same six reviews less well.

---

## IG engagement audience built — and it is UNDER 1,000

**13 Sep, ~13:00 AEST.** `TEL — IG engagers 365d` created on `act_2121305908740756` from the
Instagram profile source, 365-day retention, broadest engagement setting.

**Meta reports the size as "Below 1000".**

### Correction — this was predicted to clear 1,000 comfortably
It did not. The prediction was flagged as a prediction rather than a fact, which was right, but
the reasoning behind it was wrong and the error is worth keeping:

**Profile views are not unique people.** 5,330 views across 10–11 Sep represents far fewer
individuals viewing repeatedly. Meta counts *people*, and only those with engagement actions it
can attribute. The organic lift is genuine; it simply converts to a much thinner retargetable
pool than raw view counts suggest. **Do not size a Meta audience from a view metric again.**

### Consequences
- **Warm Stack stays parked.** Swapping this audience in would hit the same wall as the
  gate-era audiences (`TEL - gate visitors 30d` now reads **"Size not available"** in Ads
  Manager — Meta will not even report a size for it).
- **Do not build a lookalike from it yet.** Meta's floor for a lookalike source is ~100 people,
  so it would technically be allowed, but the recommended seed is 1,000–50,000. A lookalike off
  a thin seed generally underperforms broad targeting with good creative — and broad targeting
  with good creative is already delivering **$0.109–0.115/LPV** on Warm Entry v2. Building it
  now would feel like progress and probably would not be.

### The honest strategic position
**There is no warm audience available, and nothing buildable today creates one.** Customer list
44, gate audiences dead, IG pool under 1,000, site traffic thin. The play for the next stretch
is **broad prospecting plus better creative** — which is what Warm Entry has quietly been
winning at the whole time.

### What was actually gained
The audience now **exists and accumulates daily**. Before today it did not exist at all. With
organic Instagram running at ~4.5× baseline, it should clear 1,000 within weeks. **Re-check in
a month**; at that point the lookalike becomes worth building and Warm Stack has something real
to target.

Its immediate uses, valid at any size: **exclusion** (stop paying to show discovery ads to
existing engagers) and **accumulation**.

---

## CROSS-CHECK — Sun 13 Sep 2026, 13:07 AEST

Full live read across Klaviyo, Shopify and Meta, run to establish what can be **signed off** as
working. Every line below is an observed outcome or a direct API read, per rule 1.

### SIGNED OFF — verified by outcome

**1. The email consent chain. The two-sided check now passes.**

| Side | Reading |
|---|---|
| Shopify — subscribed | **57** |
| Shopify — not subscribed | 18 |
| Shopify — total customers | 75 (57 + 18 = 75, both pages exhaustive) |
| Klaviyo — emailable segment `YgyR87` | **56** |
| Klaviyo — list `V9Rbbr` | 58 |

**Gap of 1, against a gap of 27+ last night.** This is the fault that suppressed the launch and
it is closed. The 2-profile difference between the list (58) and the emailable segment (56) is
the customers who declined — consent relocated, never manufactured, still visible in the data.

**2. The segment recalculated on its own: 23 → 56.** At 12:00 it still read 23 and that was
called lag rather than a failed import. The call was right; it was lag.

**3. `V9Rbbr` is single opt-in** — `opt_in_process: single_opt_in`, re-read, third confirmation.

**4. Flows — 6 of 7 live.** `TEZ6PM`, `TPwqqq`, `UpBgzj`, `Vg9tuX`, `WnAETh`, `YgAs6b` all read
`status: live`. Only `SuavPL` (back-in-stock) is genuinely `draft`. **Three live flows still
carry "(DRAFT)" in their names** — the names lie, the status is the truth.

**5. Ad account standing.** Both campaigns `ENABLED`. Both Ritual Drop ad sets `ENABLED`, both
ads `ACTIVE` with `review.status: APPROVED`.

**6. UTM tagging is correct on both ads** — `utm_source=meta&utm_medium=paid_social&
utm_campaign=ritual_drop_sep26`, with `utm_content` split `broad_au` / `warm_stack`. The
attribution plumbing is sound even though nothing has flowed through it yet.

**7. Warm Entry v2 is holding.** 13 Sep to 13:07: $5.78, 570 impressions, 65 clicks, 53 LPV =
**$0.109/LPV**, frequency 1.04.

### A near-miss, recorded because it is the same trap as always
`customersCount(query: "email_marketing_state:subscribed")` returned **75** — and so did
`customersCount` with **no filter**, and so did a deliberately invalid filter. **The
`customersCount` field silently ignores its query argument.** Reporting 75 subscribed would have
invented 18 consenting customers who do not exist. The `customers` connection does filter
correctly, and that is what the numbers above come from. **Control query first; a number that
cannot be wrong has not been tested.**

### STILL BROKEN — re-confirmed, not assumed

| Thing | Reading |
|---|---|
| Form `WirxQ2` | `query_form_values` over `last_7_days` → **`results: []`** again. No views, no submits |
| Warm Stack targeting | Read directly off the ad set: still `TEL - gate visitors 30d` and `tel gate visitors 180d`. **The dead audiences were never swapped out** |

### NEW FINDING — Ritual Drop has delivered on one day in eight

| Date | Warm Entry v2 | Ritual Drop (both ad sets) |
|---|---|---|
| 6 Sep | $15.67 | — |
| 7 Sep | $9.24 | — |
| 8 Sep | $27.55 | — |
| 9 Sep | $45.61 | — |
| 10 Sep | $39.35 | — |
| 11 Sep | $11.84 | — |
| 12 Sep | $4.81 | **$6.43** |
| 13 Sep → 13:07 | $5.78 | **$0** |

**Ritual Drop holds $40 of the $60/day budget — two thirds — and has spent $6.43 in eight
days.** It reads ENABLED with approved, active ads, so nothing in the configuration explains it.

Two further things this table shows:
- **Total spend has collapsed** from ~$40/day (9–10 Sep) to ~$5/day. The 12 Sep underdelivery
  was not a one-off ramp after the billing fix.
- **Warm Entry spent $45.61 on 9 Sep against a campaign budget that now reads $20/day.** The
  budget has been changed at some point since. Not resolvable from here.

**What this cannot tell us:** whether the ad sets read "Learning limited", "Not delivering" or
carry a payment flag. Supermetrics does not return delivery status. **This needs one look in
Ads Manager at the Delivery column** — it is the highest-value 30 seconds available right now,
because two thirds of the budget is inert.

Candidate causes, none verified: a conversion campaign with zero purchase history cannot exit
learning and gets throttled; Warm Stack cannot spend its share of the CBO pool because its
audiences are empty; or a second billing-side limit.

### WEB ORDERS — sharper than previously recorded

Both web orders read `landingPage: "https://telcollection.com.au/password"` — **both buyers
first arrived during the gate period.** Neither came from the open store.

The accurate statement is therefore not "2 web orders since launch". It is: **no visitor who
first arrived at the open store has ever purchased.** #1045 (paid) and #1046 (PayPal, still
PENDING) were both gate-era traffic converting later.

Latest order is still **#1054, 13 Sep 00:14 AEST, POS.** No orders at all since.

### STILL UNTESTED — and honestly so

**The POS consent sync.** No order has been placed since the backfill completed at 01:59, so the
test has not been possible. But the profile read produced a genuine refinement:

- A profile created **12 Sep 09:21** reads `method: SHOPIFY`, consent timestamped 40 minutes later
- A profile created **9 Sep 09:28** reads `method: SHOPIFY`, consent timestamped 25 seconds later
- Profiles created **11 Sep** read `NEVER_SUBSCRIBED`, never rescued until the manual import
- Every 12 Sep POS profile reads `method: LIST_IMPORT` — **they were rescued by the backfill, not
  by the sync**

**So the sync is inconsistent, not dead.** It has carried consent at least twice. Because the
backfill overwrote the POS profiles, the only clean test left is the next counter sale:
`method: SHOPIFY` = working, `NEVER_SUBSCRIBED` = still faulty.

---

## DEEP AUDIT — Sun 13 Sep 2026, ~13:40 AEST

Run against the untested surface rather than the known-fault list, because every fault in this
project has been a thing nobody had ever measured. Four findings, two of them material.

### 1. ROOT CAUSE FOUND — the Klaviyo onsite script has NEVER run

| Metric | Integration | Events, 15 Jun → 13 Sep |
|---|---|---|
| **Viewed Product** | API (onsite JS) | **0** |
| **Active on Site** | API (onsite JS) | **0** |
| Added to Cart | Shopify (server) | firing |
| Checkout Started | Shopify (server) | firing, 69 events |
| Placed Order | Shopify (server) | firing |

**Every server-side Shopify event fires. Every onsite-JavaScript event is zero, across three
months.** Not low — zero, in every month, including the launch weekend with thousands of
sessions.

`Active on Site` alone proves nothing (it only fires for identified profiles — that reasoning
was correct and is unchanged). **`Viewed Product` fires for anonymous visitors.** Three months
at zero with live traffic is conclusive: **the Klaviyo onsite script is not executing on
telcollection.com.au.**

#### This explains the form, and it changes the fix
The app embed reads `"disabled": false` in `settings_data.json` on the live theme and
`{{ content_for_header }}` is present — and the script still is not running. Same class of
fault as everything else here: **configuration correct, outcome absent.**

**Therefore: rebuilding the form would NOT have fixed it.** The previous recommendation — build
a new form from scratch — would have produced a second form that also never rendered, because
there is no script on the page to serve either of them. **That recommendation is withdrawn.**

**Leading hypothesis, unverified:** this account's public API key is **`TbNLXf`**. If the
theme's Klaviyo app embed carries a *different* key, the script would load and report to
another Klaviyo account — producing exactly this signature: zero onsite events here, while the
page looks correctly configured. This connects to the open question of which Klaviyo org the
upgrade billed to. **Check the key in the app embed against `TbNLXf` before anything else.**

#### Second casualty
Flow `YgAs6b` (browse abandonment) triggers on **Viewed Product**. That event has never
occurred. **The flow is live and can never fire.** It is not "untested" — it is dead until the
script runs.

### 2. The import sent 39 emails this morning that nobody authorised

Flow report, **today only**:

| Flow | Delivered today |
|---|---|
| `TEZ6PM` Welcome: The standard | **33** |
| `WnAETh` Post-purchase: The Healing Guide | **6** |

The CSV backfill added 44 profiles to `V9Rbbr` at **01:59**. `TEZ6PM` triggers on **Added to
List**. The import therefore fired the welcome sequence at existing paying customers, and
released healing-guide messages that had been held back for want of consent.

**This was a foreseeable consequence of the import and it was not flagged before it ran.** It
breaches the standing rule that nothing sends without Ben's word — not by intent, but the
emails went out either way.

- The **6 healing-guide sends are correct and welcome** — those customers bought on 12 Sep and
  should receive it. The flow had been holding them because they were not subscribed.
- The **33 welcome sends are the problem**: they greet people who have already bought.

**RESOLVED — ALL CLEAR, checked 13 Sep ~13:55.** Template `SqWZAx` (`TEL · Welcome 1 · The
standard`) read in full. **There is no discount code and no offer.** The email explicitly states:
*"What the list gets: first look at every run, healing notes from a working studio, and priority
when a run sells out. **No codes. Nothing else.**"* Subject *"You're in. Here's the standard."*,
from *Benny at TEL Collection*, single button to the product page, correct unsubscribe and
physical address.

**Commercial cost of the 33 unplanned sends: nil.** It is a well-built brand email. The only
awkwardness is greeting existing customers with "You're in", which is cosmetic.

**One small real fault found while reading it:** the button links to
`https://telcollection.com.au/products/tattoo-aftercare-kit` with **no UTM parameters**, so any
purchase these 33 emails produce will not be attributable to the email. Worth adding tracking
params to every flow message.

**Rule to carry forward: before any import into a list, check what flows trigger on
`Added to List` and pause them for the duration.**

### 3. Abandoned checkout is real, and nothing chases it

`Checkout Started` has fired **69 times** — 2 in June, 30 in July, 22 in August, 15 in
September (9–13). Over 9–13 Sep: **15 checkouts started against 10 orders placed.**

Flow `Vg9tuX` (abandoned checkout) is **live** and has **delivered 0 messages, ever**.

*Caveat, stated rather than assumed:* these counts include POS, since the studio was selling
through the gated period when the web store had no visitors. The gap is therefore roughly
**five abandoned checkouts in five days**, not fifteen. Modest money — but it is money already
at the till, the flow is already built, and it recovers nothing.

**Also note: `Added to Cart` fired twice while `Checkout Started` fired 15 times.** Buyers are
using the dynamic "Buy it now" button and skipping the cart entirely. Any logic anywhere that
depends on Added to Cart is close to useless on this store.

### 4. Deliverability — a red flag raised, then cleared by outcome

`get_sending_domains` returns `send.telcollection.com.au` with `status: "active"` but **all five
DNS records reading `verified: false`** (4 × NS to `ns1–4.klaviyo.com`, 1 × TXT site
verification). Created 22 Aug, untouched since 26 Aug.

That looked like a serious deliverability fault. **The outcome data says it is not hurting
anything today:**

| Send | Delivered | Delivery rate | Bounced | Spam complaints | Open rate |
|---|---|---|---|---|---|
| Welcome flow (all-time) | 38 | **100%** | 0 | 0 | 10.5% |
| Healing guide (all-time) | 20 | **100%** | 0 | 0 | **35%** |
| Doors Open campaign | 20 | 100% | 0 | 0 | 25% |
| T-1 campaign | 20 | 95.2% | 1 | 0 | 25% |
| T+3 campaign | 20 | 100% | 0 | 0 | 20% |
| Review Ask campaign | 14 | 100% | 0 | 0 | 14% |

**100% delivery, one bounce in 132 sends, zero spam complaints, open rates 14–35%.** Mail is
arriving and being read.

**Verdict: worth finishing, not a current fault.** Klaviyo falls back to its shared sending
domain, which works fine at this volume. Finish the DNS delegation before the list is large
enough for inbox providers to care — it is durability, not an emergency. Recorded so it is
never re-diagnosed as the cause of something else.

### Campaign history — four sends, and what they actually did

| Campaign | Sent | Recipients | Opens | Clicks | Conversions |
|---|---|---|---|---|---|
| CH1 · T-1 | 9 Sep | 21 | 25% | 0 | **1 · $59.95** |
| Doors Open — Founding Price | 10 Sep | 20 | 25% | **0** | 0 |
| Chapter One Review Ask | 11 Sep | 14 | 14% | **0** | 0 |
| CH1 · T+3 · Sets remaining | 12 Sep | 20 | 20% | **0** | 0 |

Three consecutive sends with **zero clicks on 54 delivered emails**. Link tracking is **not**
broken — the welcome flow records a 50% click-to-open — so this is audience size and content,
not a technical fault. On 20 recipients, 4–5 opens and 0 clicks is unremarkable in isolation;
across three sends it is a reminder that **a 20-person list cannot produce commercial signal**,
whatever the copy says. The backfill to 56 is the fix, and it has now happened.

**A review-ask campaign did go out on 11 Sep to 14 people** — separate from Judge.me's own 21
requests. Two systems are asking the same customers for reviews. Worth reconciling before
adding a third.

### Flow send counts — which zeros are faults and which are expected

| Flow | Delivered, all time | Reading |
|---|---|---|
| `TEZ6PM` Welcome | 38 | Working |
| `WnAETh` Healing Guide | 20 | Working, 35% opens |
| `TPwqqq` Online healing guide | **0** | **Expected** — needs a fulfilled *web* order; there have been none |
| `UpBgzj` Reorder | **0** | **Expected** — 50-day delay, first sends due ~8–11 Oct |
| `YgAs6b` Browse abandonment | **0** | **FAULT** — triggers on Viewed Product, which has never fired |
| `Vg9tuX` Abandoned checkout | **0** | **FAULT** — 69 checkout-start events and not one message |
| `SuavPL` Back in stock | **0** | Expected — still draft, 439 units in stock |


---

## FIX PREP — the two open faults, diagnosed to the step. 13 Sep ~14:15 AEST

### Correction — the onsite key is NOT stored in the theme
An earlier note said to check the app embed's key against `TbNLXf`. **The theme stores no key.**
Read directly from `settings_data.json` on `TEL v6.2` (role MAIN):

```json
"855628211100114053": {
  "type": "shopify://apps/klaviyo-email-marketing-sms/blocks/klaviyo-onsite-embed/2632fe16-...",
  "disabled": false,
  "settings": {}
}
```

`settings` is **empty**. The account the script reports to is decided by **which Klaviyo account
the Shopify app is connected to**, not by anything in the theme. So the check is the page source
or the app connection — not the theme editor.

**This session cannot fetch the live site** — the network egress proxy blocks
`telcollection.com.au`. The page-source read must be done by Ben. Recorded so nobody assumes it
was checked from here.

### Abandoned checkout `Vg9tuX` — the flow is built correctly. It is being SKIPPED.

Full config read 13 Sep:

| Element | Reading |
|---|---|
| Flow status | **live** |
| Trigger | metric `Tf2hcu` (Checkout Started), **no trigger filter** |
| Guard | Placed Order count **= 0** since flow start — correct |
| Sequence | 1h delay → email → 23h delay → email → 2d delay → email |
| All three emails | `status: live` |

**Nothing is misconfigured.** The build is right.

**`Skipped Send` fired 5 times, 9–11 Sep** — the window with 14 checkout starts. So the flow
**is** triggering and Klaviyo is **declining to send**. The remaining ~9 never entered at all,
consistent with checkouts that carry no usable email profile.

**Cause: the recipients were not subscribed to email marketing.** Klaviyo will not send a
marketing email to an unsubscribed profile. Until 01:59 today **only 23 profiles in the entire
account were emailable** — the same consent fault that suppressed everything else.

**So this is not a third fault. It is the consent fault wearing a third costume.** The fix is
not in the flow — it is capturing marketing consent at checkout, where the abandoners are.

**Verification after fixing:** `Skipped Send` should fall and the flow report should show
`delivered > 0`. Watch both.

### The step-by-step lives in its own file
**`launch/fix-walkthrough.md`** — both fixes written app-by-app with exact URLs, because earlier
instructions moved between three websites without naming which. Store handle `iw0xvm-v5`,
Klaviyo key `TbNLXf`.
