# TEL Collection — full overhaul + tuned ad spend

## Context

TEL opened Thu 10 Sep 7pm AEST. Two web orders in 48 hours. Ben is on deck and wants the
whole stack cross-examined, the blockers rectified, and a tuned ad spend ready to run — signed
off within the hour.

**The headline from the audit: far less is broken than the flat launch implies.** The
infrastructure is sound. Three specific failures suppressed the launch, and one of the three
is already fixed.

---

## Cross-examination: what is actually working

Verified by live read this session — do not re-litigate these.

| System | State |
|---|---|
| Checkout | **Healthy.** Shopify Payments SUCCESS on every order (auth + capture) |
| Shipping | **Free domestic shipping live** ($0), Express $15. Not a conversion blocker |
| Product | Ritual Duo ACTIVE, 445 units, `availableForSale: true`, inventory tracked |
| Sales channels | Online Store, **Facebook & Instagram**, POS, Google & YouTube — all published |
| Meta pixel | **Fires.** 1,277 LPVs prove it; LPV optimisation cannot run without it |
| Meta catalog | Wired via the F&I channel — Advantage+ Shopping is available |
| Klaviyo ↔ Shopify | Full commerce event set present: Added to Cart, Checkout Started, Placed Order, Ordered Product, Fulfilled, Refunded, Cancelled |
| Klaviyo flows | 6 live: welcome, 2× post-purchase, reorder, abandoned checkout, browse abandonment |
| Klaviyo sequence | Fired on time, correct `WjZxaE` exclusions throughout |

Telling detail: the `Added to Cart` metric was **created 9 Sep 21:59:51** — the exact minute of
the $0 test order. It had never fired before because the store was locked. Tracking works; it
had nothing to track.

**Supermetrics cannot read the pixel** (`conversion_types` returns empty every call, confirmed
across sessions). That is a Supermetrics scope limit, **not** a TEL problem. Stop treating it
as a red flag.

---

## What is actually broken — the rectification list

| # | Issue | Owner | Effort |
|---|---|---|---|
| 1 | **Capture form never published** (`WirxQ2`, draft since 4 Sep, 0 views ever) | Ben — Klaviyo UI | 5 min |
| 2 | Ritual Drop had zero ads | **DONE** — both built, paused, in review | — |
| 3 | Optimisation event not set per ad set | Ben — Ads Manager | 2 min |
| 4 | **CAPI almost certainly off** — see below | Ben — Shopify F&I channel | 2 min |
| 5 | Custom audiences report size 20, unverified | Ben — Ads Manager | 1 min |
| 6 | `TELTAKEOVER` never redeemed — checkout path unproven | Ben — test purchase | 5 min |
| 7 | #1046 PayPal PENDING, $59.95 unpaid | Ben — PayPal | 2 min |
| 8 | Squires list never emailed about TEL | Ben — Mailchimp send | 10 min |
| 9 | No reviews on the PDP | Later | — |
| 10 | Back-in-stock flow draft; 3 flows mislabelled "(DRAFT)" | Later | 5 min |

### The real "pixel fix" (#4)
The pixel fires, so there is nothing to repair there. The upgrade is **Conversions API**: in
the Shopify **Facebook & Instagram** channel, set data sharing to **Maximum**. That sends
events server-side alongside the browser pixel and typically recovers **20–30% of conversions**
lost to iOS and ad blockers. On a pixel with zero purchase history this matters twice over —
it is also the fastest way out of the learning phase. Two-minute toggle, largest single
technical lever available today.

---

## The strategic miss nobody has named

**Every dollar of real revenue is POS.** Roughly 40 orders at $59.95 through the studio,
against 2 web orders since launch. The studio is the machine; the website is additive. Yet:

- There is no systematic email capture at the studio counter — every Squires client is a
  proven TEL buyer and almost none are on the TEL list.
- The Squires Mailchimp list, the only owned audience with real reach, has never been emailed
  about TEL.
- The TEL list is **20 people**, so no send can move revenue regardless of how good it is.

Fixing capture — at the counter and on the site — is worth more than any budget decision on
this page. A list of 20 cannot be marketed to. A list of 500 changes the business.

Also worth noting: **only one SKU**, no bundle, no upsell, no subscription, on a *consumable*
product. AOV is hard-locked at $59.95. The reorder flow exists but there is nothing to reorder
into. That is the next structural piece after capture.

---

## Tuned ad spend

### Unit economics

| Metric | Value |
|---|---|
| AOV | $59.95 (free shipping, so AOV = revenue) |
| Est. contribution margin | ~$45/set at ~$15 COGS — **Ben to confirm COGS** |
| Break-even CPA | ~$45 |
| Target CPA to scale | **≤$20** (≈3× MER) |
| Kill threshold | >$35 CPA sustained over 3 days |

Measured performance to date: **$0.13 per landing page view, 9.2% CTR, frequency 1.03–1.11.**
That is exceptional buying — but it was to a *gate*, and click intent to a shop is different.
Assume LPV cost rises to **$0.20** against a PDP. At a 1% LPV→purchase rate that is a **$20
CPA**; at 1.5%, **$13**. The economics work with real headroom, and frequency near 1.0 means
the audience is nowhere near saturated.

### Phase 0 — before another dollar (today)
Nothing below runs until the form is live and CAPI is on. Spending into a site that cannot
capture an email is exactly what produced this week.

### Phase 1 — Days 1–3: buy signal. Hold $60/day
The pixel has **zero purchase history**, so optimising everything for Purchase stalls in
learning. Buy cheaper events first.

| Ad set | Budget | Optimise for |
|---|---|---|
| Broad AU — contingency | **$30/day** | **ADD_TO_CART** |
| Warm Stack | **$15/day** | **PURCHASE** |
| Warm Entry v2 (traffic) | **$15/day** | LPV — now feeding the live form |

If the custom audiences read <1,000, Warm Stack cannot deliver: fold its $15 into Broad AU and
rebuild the audiences against the open store's URLs.

**Gate to Phase 2:** ≥20 add-to-carts/day at ≤$4 each, and first purchases landing.

### Phase 2 — Days 4–10: switch to purchase. $60 → $100/day
- Broad AU → **PURCHASE** once ~30–50 ATCs have accumulated
- Scale **+20% every 48h**, and only while trailing-3-day CPA ≤$25
- Kill any ad set >$35 CPA over 3 days
- Run **3–4 creatives per ad set** — creative variety is the single biggest performance driver
  and there is currently **one image** in the whole ad account

### Phase 3 — Day 10+: Advantage+ Shopping. $100–150/day
The catalog is already live through the F&I channel. ASC needs roughly **50 purchases in 7
days** to outperform; for a single-SKU DTC brand it usually then beats manual structures
comfortably. Do not start it early — under-fed ASC burns budget.

### Guardrails
- Never move a budget **>20% in 48h** — larger jumps re-enter learning and reset delivery
- **7-day click** attribution; judge on the 7-day, never a single day
- Frequency ceiling **2.0** → refresh creative before touching budget
- Weekly: kill the bottom creative, add one new

### Creative pipeline — the current bottleneck
One image exists in the ad account (asset `594e7f8e9e2eac3e1bc4340eacade4b6`). The repo holds
far better material that has never been used: **14 high-res editorial tattoo photographs**
(the "look after the art" proof), the **CHAPTER 1** story frame, and the founder portrait.
Target 4 statics + 1 reel per ad set. Note the two iPhone screen recordings carry UI chrome and
need recapture before any paid placement.

---

## Ben's hour, in order

1. **Klaviyo** — rewrite the popup copy (open-store, not "first access") and **publish**. Turn
   on `record_utm_params_on_submit`. Spec: `launch/capture-form-fix.md`
2. **Shopify → Facebook & Instagram channel** — data sharing to **Maximum** (CAPI on)
3. **Ads Manager** — check the two audience sizes; set Warm Stack → Purchase, Broad AU →
   Add to cart; confirm both new ads passed review
4. **Mailchimp** — send the Squires email. Copy: `launch/squires-mailchimp-founding-window.md`
5. **Test purchase** with `TELTAKEOVER`, then refund it — proves the discount path end to end
6. **PayPal** — chase #1046
7. **Then, and only then**, enable Ritual Drop at the Phase 1 split

---

## Verification

1. `query_form_values` over `last_7_days` returns **non-empty** with rising views and submits.
   Empty = still not live. This is the one that matters.
2. Meta Events Manager shows Purchase arriving via **both** Browser and Server (CAPI on).
3. Re-read the campaign at `campaign_detail_level: full` — both ad sets show a non-empty `ads`
   array and the correct `promoted_object` event before any enable.
4. A real order carrying `utm_campaign=ritual_drop_sep26` proves ads→checkout attribution;
   `utm_campaign=squires_chapter_one` proves the Mailchimp send.
5. T+48h: `data_query` by ad set for spend, ATCs and purchases against the Phase 1 gate.

## Standing rule

Nothing spends, sends or goes live without Ben's word. Both new ads, both ad sets and the
campaign are all currently PAUSED.
