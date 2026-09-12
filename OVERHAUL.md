# TEL — rectification and ad plan
### For sign-off, Saturday 12 September 2026. Every status below verified live, not assumed.

---

# PART 1 — THE FOUR FIXES

## A. META PIXEL — status: ✅ **FIXED, Saturday 12 September**

**Resolved.** The Facebook & Instagram channel was installed 28 July and **never configured** —
Shopify was sending nothing to Meta. Confirmed by four independent signals: hollow status badge
in Customer events, "—" in the Data column, an empty Datasets list in Events Manager, and a
greyed-out Test button.

**The empty Datasets list had a different cause than expected.** Ben was viewing Events Manager
through `act=3364467513587954` — his *personal* ad account. Dataset `1917775705566990` existed
the whole time, already bound to the **TEL Collection Ads** account (`2121305908740756`). Meta's
side was correct; the Shopify→Meta pipe was the missing piece.

Fixed by completing the channel setup: existing `telcollection` portfolio, existing page and
Instagram profile, **Data sharing = Maximum** (Meta Pixel + advanced matching + Conversions API),
bound to the existing dataset rather than a new one. Result: **"Run ads on Facebook and
Instagram — Active."**

Shop commerce review (up to 4 weeks) and catalog sync (48h) are pending and block nothing.

**Note for next time:** two ad accounts exist. Decide which one TEL actually spends from —
`2121305908740756` (TEL Collection Ads) keeps business spend off personal billing and is easier
to hand over.

### The original diagnosis, kept for the record

**What I know for certain:**

- Domain verification survived the theme swap. `layout/theme.liquid:7` carries
  `<meta name="facebook-domain-verification" content="c0hf8rfbls1qzmzth1yy0etwchwo1j">`
- Facebook & Instagram is a **published sales channel**, so catalog sync is possible
- Ben checked Settings → Customer events and reported pixels **Connected, data access granted**
- Pixel `1917775705566990` was hardcoded in `theme/sections/main-password.liquid`, firing
  PageView and a Lead event on gate signup

**What broke:** that inline pixel lived **only on the password page**. `theme.liquid` renders
that section for `request.page_type == 'password'` alone. Dropping the password at 18:39
Thursday deleted it — along with the Lead event, which was the only conversion signal the
account had.

**What I still cannot confirm, after three attempts:**

```
webPixel          → Access denied. Required access: `read_pixels` access scope
appInstallations  → access denied
```

**This is the honest limit of what I can do from here.** Everything about the pixel below is
Ben's ten minutes at a laptop, and it must be done before a dollar of ad spend.

### The three checks, in order

1. **Events Manager → Data sources.** How many pixels are listed? **If there is more than one,
   that is the problem** — the gate pixel `1917775705566990` collected for three weeks, and if
   the Facebook & Instagram channel is wired to a *different* ID, your audience is split across
   two datasets and neither has enough to work with.
2. **Open the pixel that is receiving storefront traffic → Overview.** Are PageView,
   ViewContent, AddToCart, InitiateCheckout and **Purchase** all arriving? Purchase is the one
   that matters — without it Meta optimises for clicks, not sales.
3. **Aggregated Event Measurement** (Events Manager → the pixel → Aggregated Event
   Measurement). Domain is verified, so configure the 8 event priorities with **Purchase at
   number one**. Most accounts never do this and lose iOS conversions silently.

### Then — Conversions API

Shopify's Facebook & Instagram channel has a built-in Conversions API toggle. Turn it on.
It sends events server-side as well as browser-side, which recovers the 20–40% of conversions
that ad blockers and iOS tracking prompts eat. **Free, ten minutes, and it is the single
biggest lift to match quality you can get.**

---

## B. MAILCHIMP — status: ✅ **ROOT CAUSE FOUND, Saturday 12 September. Fix is one field.**

### The campaign was sent from `squiresink@gmail.com`

Confirmed on the campaign record itself (Mailchimp campaign id 1377):

```
Campaign:   The Thing I've Been Building   [sent]
Delivered:  Thu, Sep 10, 2026 4:45 am      (US Eastern — see below)
From name:  Squires Ink
From email: squiresink@gmail.com           ← THE FAULT
Subject:    The thing I've been building
Recipients: Sent to audience: Squires Ink  (~7,000)
```

**Why that destroys a bulk send.** Google publishes a DMARC policy on `gmail.com` instructing
every receiving mail server to quarantine any message claiming to come from `@gmail.com` that
was not sent by Google's own servers. Mailchimp's servers are not Google's. All ~7,000 messages
failed DMARC on arrival and were filed as spam — at Gmail, Yahoo, Outlook and iCloud alike.
Enforced policy since February 2024, not a reputation score. No content quality, list hygiene
or warming can beat it.

### The evidence, and how it fits

| Metric | Result | Verdict |
|---|---|---|
| Delivered | **~6,990 of 7,000** | The list is excellent |
| Bounced | **10 — 0.14%** | Accepted, then filed. Not rejected |
| Unsubscribed | **14 — 0.20%** | Nobody annoyed — almost nobody read it |
| **Opened** | **4.2% ≈ 294** | Only the minority whose provider let it through |
| Clicked | 1.2% ≈ 84 | |
| **Click-to-open** | **28.6%** | **Excellent. Industry average is 10–15%** |
| Shopify sessions attributed to email | **1** | Confirms the traffic never arrived |

**Counterfactual at a normal 22% open:** ~1,540 opens → ~440 clicks → roughly **11 orders from
one send**. The From-address field cost about **5× the entire launch**.

### The original diagnosis, kept for the record — it was wrong

I called this as *"sending from Mailchimp's shared, unauthenticated `mailchimpapp.com`"* and
wrote a DNS walkthrough for it. That was wrong, and Ben was right to push back with *"it says
tel collection is already authenticated in domains."* The domain was authenticated the whole
time. The campaign simply never used it.

### Everything else was checked and is clean

Verified on screen, one at a time:

| Check | Result |
|---|---|
| Mailchimp domain auth (`telcollection.com.au`) | ✅ **Authenticated** |
| DKIM `k2._domainkey` → `dkim2.mcsv.net` | ✅ present, **DNS only** |
| DKIM `k3._domainkey` → `dkim3.mcsv.net` | ✅ present, **DNS only** |
| DMARC `_dmarc` | ✅ `v=DMARC1; p=none; rua=mailto:info@telcollection.com.au` |
| SPF | ✅ exactly one: `v=spf1 include:_spf.google.com ~all` |
| Google Workspace DKIM + MX | ✅ `google._domainkey`, `MX → smtp.google.com` |
| Klaviyo sending subdomain | ✅ `send.` delegated to ns1–4.klaviyo.com |
| Proxy status, all 14 Cloudflare records | ✅ DNS only — no orange clouds |
| Google bulk-sender requirements | ✅ **met by the domain** |

Two further corrections to earlier calls of mine: **`_dmarc` was never missing** — it has been
published all along. And **`k1._domainkey` is not missing** — Mailchimp's current setup issues
k2 and k3 only; k1 is the legacy record.

DNS lives at **Cloudflare** (zone added 8 July 2026), not Shopify. Shopify's Domains page only
shows the two records that point the website at Shopify.

### Second finding — the Mailchimp account timezone is US Eastern, not Brisbane

Mailchimp records delivery as **4:45am Thu 10 Sep**. Brisbane 6:45pm = 08:45 UTC = 04:45 EDT.
The account runs on US Eastern, and the send fired at **6:45pm Brisbane — ten minutes earlier
than the intended 6:55pm.** Harmless this time. Fix the account timezone before the next
scheduled send.

### The fix

**1 · Change the From address.** From name and From address are separate fields in Mailchimp.
The inbox shows the name in bold; the domain sits in small grey text. So the studio
relationship survives intact while the authenticated domain carries deliverability:

```
From name:     Benny — Squires Ink
From address:  info@telcollection.com.au
```

`telcollection.com.au` is the only authenticated domain in the account and is fully configured.
Nothing else needs to change for this to work today.

**2 · Audit Automations for the same fault.** Any automation in the Squires Ink audience may
carry `squiresink@gmail.com` as its sender — each one currently sends straight to spam, every
day, silently.

**3 · Remove `gmail.com` from Public email domains.** Only after 1 and 2, so nothing live
breaks mid-change. Once removed it cannot be selected again.

**Optional, not a blocker:** if a Squires-owned domain exists with DNS access, authenticating
it in Mailchimp would be a better long-term brand fit for studio sends.

### Then the resend — three waves, not a blast

`telcollection.com.au` has **no Mailchimp sending history at all** — the 7,000 send never used
it. So the corrected sender starts from zero reputation, and a 7,000 burst is still wrong even
with perfect authentication. Every wave also stays under 5,000/day, keeping the domain clear of
Google's bulk-sender threshold while it builds.

| Wave | Audience | Approx | Content | Gap |
|---|---|---|---|---|
| **1** | Opened or clicked the original | **~300** | **New follow-up** — `emails/squires-wave-1-healing-guide.html` | — |
| **2** | Non-openers with prior Squires engagement | ~500–1,000 | Resend of the original — they never saw it | 2 days |
| **3** | Remaining non-openers, split across days | ~5,000 | Resend of the original | 2 days |

Check each wave's open rate before firing the next. **Wave 1 should return 25–35%.** Single
digits means stop and find out why before burning 6,700.

**Wave 1 leads with the Healing Guide, not the product.** They already read the pitch. Its job
is warming the sender with opens and clicks from the most engaged segment there is, while
placing the set at the trigger — the counter, and the next booking — rather than pushing a
second sell at people who just declined the first.

**No discount extension needed.** `TELTAKEOVER` expires Monday, but the Squires email
deliberately carried no founding price — scarcity and story only. The 7,000 were never offered
it, so waves 2 and 3 deliver exactly the message written for them.

### Optional DNS hardening — NOT today

`v=spf1 include:_spf.google.com ~all` covers Google but not Mailchimp. **Not the cause and not
urgent**: Mailchimp uses its own Return-Path, so SPF is evaluated against Mailchimp's own
record, and DMARC passes on aligned DKIM regardless. Adding `include:servers.mcsv.net` is
belt-and-braces. **Edit the existing record, never add a second** — two SPF records invalidate
each other and break all outbound mail. Once the domain is warm, move DMARC from `p=none` to
`p=quarantine`.

### Also fix: link tracking

Only **1 session** was attributed to email in Shopify though ~84 people clicked. Mailchimp's
UTM tagging is likely off, so email traffic lands in "direct" and cannot be measured. Turn on
link tracking in the campaign settings before wave 1.

### Verification

1. **Before wave 1** — test send to a Gmail address, open it, tap the sender to expand.
   Confirm `mailed-by` / `signed-by` read `telcollection.com.au` and there is **no "via"**.
2. **Jess** — she never received it. Have her search **spam** for "The thing I've been
   building". Finding it there is human confirmation of the whole diagnosis. If it is not
   there, check whether she is in the audience at all — that changes the 4.2% denominator.
3. **DMARC reports** — `rua` delivers daily aggregate reports to `info@telcollection.com.au`.
   After wave 1 they should list Mailchimp IPs with **pass**. Reports covering 10–11 Sep should
   show no Mailchimp activity, since the campaign never claimed the domain.
4. **Wave 1 open rate at 24h** — the number that gates waves 2 and 3.
5. **Shopify sessions by referrer** — email should move off 1 session.

---

## C. SHOPIFY — status: **the store works; four things need decisions**

**Verified working:** v6.2 is MAIN, all files byte-identical to the repo, store public,
445 in stock on DENY (will not oversell), $59.95, checkout proven by three real orders,
free shipping correct at both price points, `shop.description` fixed.

### C1 — The three-year shelf-life claim ⚠️ **the one with legal exposure**

The FAQs page states publicly: *"Every batch is tested … with a three-year shelf life."*

VOG confirmed in writing: *"The preservative system we use can maintain a 3-year shelf life.
However, we have not conducted a preservative efficacy test."* No stability study either. The
COA's −10°C/+40°C range is a **process measurement**, not stability data.

**That is an unsubstantiated claim on a live storefront under Australian Consumer Law.**

Two ways out, pick one today:
- **Substantiate it** — send jars to an Australian lab for PET (ISO 11930) and accelerated
  stability. Both run on **finished product**, so VOG's formula is not needed. Their "do it
  yourself" answer is not a blocker.
- **Change the sentence** until the data exists. "Batch tested for heavy metals" is defensible
  today; the shelf-life half is not.

### C2 — TELTAKEOVER expires **Monday 14 September, 23:59** — decision needed today

Status ACTIVE, one use (the cancelled test). **Nobody has used it.** All three real orders
paid full price with no code.

That means the founding price did nothing except sit there. And Monday's scheduled Klaviyo
email — "Founding Price Closes" — lands on an offer no customer took. **Either let it expire
quietly and pull that email, or extend it and actually promote it.** Sending a "last chance"
for something nobody wanted reads badly.

### C3 — HEALED15 is still live with **no end date**

15% off, active since 4 August, zero uses. Harmless now — it cannot stack with TELTAKEOVER and
is worse value. **It matters the moment TELTAKEOVER expires**, because it quietly contradicts
"the price never comes down again." Give it an end date or consciously keep it as a loyalty
code that sits outside the no-sales promise.

### C4 — Two orders sitting

- **#1045 Jessica Holland** — PAID Thursday 19:14, **still UNFULFILLED**. Two days.
- **#1046 Gai Chase** — **PENDING** since Friday 13:42, 44 hours. Money not captured. If it
  has not cleared by Monday, cancel and restock so the count stays honest.

---

## D. CAPTURE / KLAVIYO — status: **the mechanism works, the placement was removed**

### The finding that explains the week

Every signup this brand has came from the **password gate**. `main-password.liquid` carries a
`{% form 'customer' %}` with "Get first access" — every visitor during the gated period hit a
page whose only call to action was handing over an email.

**23 people tagged `newsletter` in Shopify. The most recent is 9 September, 09:28 — the morning
before the doors opened. Zero since.** 931 sessions, not one capture.

Dropping the gate deleted the only capture point that was converting. After 18:39, visitors
landed on a homepage where the capture band sat 12th of 12.

**And it demonstrably worked:** Gai Chase (#1046) and Bradley Oulton (#1042) both signed up via
the gate on 9 September, then bought. Capture → nurture → sale, already proven twice.

### Current state, verified

| | Status |
|---|---|
| Homepage capture band | Live, now **7th of 12** (v6.2) |
| Product page capture band | Live, **5th of 7** (v6.2) |
| Theme popup (`overlay-group.json`) | **`"disabled": true`** |
| Klaviyo popup `WirxQ2` | **draft** — `updated_at` still 4 Sep 14:46:47, never edited |
| Welcome flow `TEZ6PM` | **live** |
| Abandoned checkout `Vg9tuX` | **live** |
| Browse abandonment `YgAs6b` | **live** |
| 3× post-purchase flows | **live** |
| Back-in-stock `SuavPL` | **draft** — the only genuine draft |

**A band you scroll to is not a wall you cannot pass.** The popup is what replaces the gate,
and it is the prerequisite for ad spend — otherwise paid traffic leaks exactly like the organic
did.

### Also worth ten minutes

Klaviyo's Doors Open campaign went to **20 recipients**. Shopify holds **23 newsletter-tagged
customers** plus more subscribed buyers. **The Shopify→Klaviyo sync may be dropping people** —
meaning the list is bigger than Klaviyo thinks.

---

# PART 2 — EVERYTHING ELSE THAT NEEDS MOVING

## Compliance — now gating revenue, not tidying up

**Products liability insurance — the urgent one.** VOG confirmed: *"We don't have product
liability insurance covering export markets. We are merely a manufacturer engaged in
production, not an exporter."*

Two consequences:
- **Aqua747 carries 100% of the risk.** No upstream insurer, on a product applied to open
  wounds.
- **"Not an exporter" means TEL is the importer** — which settles the AICIS question. **TEL is
  the introducer and must register.**

Find a broker who handles **cosmetics specifically**. Brief: aftercare applied to freshly
tattooed skin, manufactured offshore by a third party to TEL's specification, imported by TEL,
sold direct and intended for wholesale. **This gates the artist channel** — the first serious
stockist asks for the certificate.

**AICIS registration.** TEL is the introducer. Register, categorise introductions, keep records.

**PET + stability.** Needed for C1 above, and before the 1,000-set run.

## Suppliers

**VOG — four gaps confirmed:** ISO 22716 scope for the anhydrous balm (they answered about the
Chinese production licence instead — different document), no stability study, no PET, no
liability insurance. The 11 documents sent 8 September are still unread; opening them closes
most of the file.

**Moisturiser is stalled** — freight ask declined, the black airless pump doesn't exist in
their range, and pump specs/pricing/MOQ, the ISO 11930 build request and pH figures all went
unanswered.

**JAJI — waiting since 3 September.** Reply drafted and ready in `SUPPLIERS.md`. Formula IP is
retained (standard, but a single point of failure), 5L MOQ ≈ 500 bottles at 50ml, and **no
pricing has been given across two emails.**

---

# PART 3 — THE AD PLAN

## Do not spend a dollar until these four are true

1. Pixel verified, single ID, Purchase event firing
2. Conversions API on
3. **Popup live** — or paid traffic leaks exactly like the organic did
4. Link in bio → `/products/tattoo-aftercare-kit`

**Spending before capture exists means paying full price for cold clicks that leave no trace.
That is the same leak, now metered.**

## The one number I need from you

**What does a Ritual Duo cost you landed — product, freight, duty, packaging?**

At $59.95 retail, if landed cost is ~$15 you have ~$45 gross per unit, which supports a **$20–25
target CPA** and still makes money. Every budget below assumes roughly that. **If your landed
cost is materially different, the whole plan re-scales** — so give me the real figure before
this goes live.

## The audience ladder — warmest first, cheapest first

### Tier 1 · Site retargeting — 931 visitors, 180-day window
Warmest and cheapest, but **931 is below Meta's comfortable minimum (~1,000)**. It will deliver
but inefficiently. It grows on its own as traffic continues.
**Budget: $10/day.** First place ROAS shows up.

### Tier 2 · Meta engagers — your biggest free asset ⭐
Everyone who watched the launch video, engaged with the collab post, or visited the profile
across **TEL, Squires Ink, Valerio and CW Media**. That collab reached far more than 931 people
— this audience is likely **5–10× your site pool**, and it costs nothing to build.
**Budget: $15/day.** Best near-term value in the whole plan.

### Tier 3 · Customer list upload + Lookalike — the real unlock ⭐⭐
Upload the **7,000 Squires list** plus your 65 Shopify customers as a Custom Audience. Typical
match rate 50–70% → **~4,000 matched people**. Then build a **1% Lookalike from that seed.**

This is the single most valuable cold audience available to you, because it is modelled on
people who have actually sat in your chair.

⚠️ **Check the consent position first.** These are Squires clients whose emails were collected
for studio purposes. Uploading them to Meta for advertising is a different use, and the
Australian Privacy Act cares about that. Confirm your privacy policy covers it before you
upload — a ten-minute question that avoids a real problem.

**Budget: $20/day** once the Lookalike is built.

### Tier 4 · Cold interest targeting — last, and only if 1–3 work
Tattoo interests, AU-wide, 18–45. Consider **geo-radius around tattoo studios** — aftercare is
a trigger purchase, and proximity to studios is the closest thing to targeting the trigger.
**Budget: hold until Tiers 1–3 have data.**

### Skip: Lookalike from purchasers
You have 3–5 online purchasers. Far too small a seed. The 7,000 list is the seed.

## Structure and budget

| Campaign | Objective | Audience | Daily | 14 days |
|---|---|---|---|---|
| **1 · Retarget** | Sales | Tier 1 + Tier 2, excluding purchasers | **$25** | $350 |
| **2 · Acquire** | Sales | Tier 3 Lookalike 1% | **$20** | $280 |
| | | | **$45/day** | **$630** |

**Roughly $1,350/month.** At a $25 CPA that is ~54 sales/month. At $40 CPA, ~34. Both clear
the bar if landed cost is near $15.

**Run 14 days before judging anything.** Meta's learning phase needs ~50 conversions per ad set
to optimise; you will not get there immediately, which is exactly why Tier 3's volume matters.

## Creative — you already have it

1. **The launch video** (CW Media) — hero asset, cut to 15s and 6s
2. **The retouched product frames** — the sealed set, the plate
3. **The founder cut** — seventeen years, the back piece, the chest. Nobody else in this
   category has this and it is your strongest differentiator
4. **The chemistry angle** — *"We live and breathe tattoos — we know chemistry"* plus the
   petrolatum myth. High-intent, genuinely differentiated, and it doubles as search content

**Run 3–4 creatives per ad set and let Meta find the winner.** Refresh every 2–3 weeks before
fatigue sets in.

## Landing page

**Always `/products/tattoo-aftercare-kit`.** Never the homepage. It carries the buy button, the
500-set counter, the proof strip, seven accordions and now the capture band. It is the only
page that does all four jobs.

## What to measure

| Metric | Target |
|---|---|
| CPA | **under $25** |
| ROAS | **above 2.4×** at $59.95 |
| Click-through rate | above 1% |
| Cost per click | under $1.00 AU |
| **Capture rate** | **above 2% of sessions** ← the leading indicator |

**Capture rate is the one to watch first.** If paid traffic arrives and still captures nobody,
stop spending and fix the popup before continuing. Everything else is downstream of that.

---

# THE ORDER OF OPERATIONS

| # | Action | Who | Time | Blocks |
|---|---|---|---|---|
| 1 | Pack **#1045** | Ben | 10 min | A customer is waiting |
| 2 | **Mailchimp From address** → `info@telcollection.com.au`, then wave 1 | Ben | 10 min | The 5× email fix |
| 3 | **Pixel audit** — count pixels, confirm Purchase, set AEM | Ben | 15 min | All ad spend |
| 4 | **Conversions API** on in the FB & IG channel | Ben | 10 min | Match quality |
| 5 | **Popup live** — I build it, you approve | Claude → Ben | 45 min | All ad spend |
| 6 | **Shelf-life claim** — amend or commission testing | Ben | 15 min | Legal exposure |
| 7 | **TELTAKEOVER decision** before Monday 23:59 | Ben | 5 min | Monday's email |
| 8 | **Insurance broker** booked | Ben | 20 min | The artist channel |
| 9 | **JAJI reply** sent | Ben | 5 min | Nine days waiting |
| 10 | Ads live — Tiers 1–3 | Claude + Ben | — | Needs 2–5 done |

**Items 2, 3, 4 and 5 are the whole "machine running" question. Nothing else in this document
matters until those four are done.**
