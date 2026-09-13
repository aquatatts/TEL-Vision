# Fix walkthrough — the two open faults, written app-by-app

**Written 13 Sep 2026.** Earlier instructions moved between three different websites without
ever saying which one, which made them unusable. This version names the exact site and the
exact URL at every step.

**Standing rule: nothing here changes anything until Ben runs it.**

---

## The three places you will be working — learn to tell them apart

| # | What it is | Exact address | How you know you're in it |
|---|---|---|---|
| **1** | **Your shop, as a customer sees it** | `telcollection.com.au` | Black page, the Ritual Duo, an **Add to cart** button |
| **2** | **Shopify admin** — the back office | `admin.shopify.com/store/iw0xvm-v5` | Green bag icon, left menu says Orders / Products / Customers |
| **3** | **Klaviyo** — the email tool | `klaviyo.com` | Left menu says Campaigns / Flows / Lists & Segments |

Shopify store handle: **`iw0xvm-v5`** (`iw0xvm-v5.myshopify.com`).
Klaviyo public API key: **`TbNLXf`**.

**Log into Shopify admin and Klaviyo in two separate browser tabs before starting.**

---

# ① THE ONSITE SCRIPT — why the popup never shows

**In one line:** Klaviyo's tracking code is not running on the website, so it cannot show a
popup and cannot see anyone browsing. **Zero page views recorded in three months.**

## STEP 1 — Prove it. 2 minutes. Phone is fine.

No technical skill needed. This is an outcome test, which is the only kind that counts.

**PLACE 1 — the shop.** On the phone, go to:
`telcollection.com.au/products/tattoo-aftercare-kit`

- Check there is **no grey bar along the bottom** of the screen. If there is, it is a theme
  preview and the test is **void** — close all tabs and retype the address by hand.
- Scroll. Wait ~30 seconds. Close it.

**PLACE 3 — Klaviyo.** Go to `klaviyo.com/analytics/metrics` → open **Viewed Product** → read
**today's** count.

| Reading | Meaning |
|---|---|
| **Still 0** | Confirmed dead. Go to Step 2 |
| **1 or more** | The script works. **Stop** — the whole diagnosis changes |

*Stronger version: before visiting, open any TEL email on that phone and tap through to the
site. That identifies the browser and guarantees the event registers.*

## STEP 2 — Find out WHICH kind of broken. Laptop. 3 minutes.

**PLACE 1 — the shop, in a private window.**

1. **New private / incognito window** (⌘⇧N / Ctrl+Shift+N)
2. `telcollection.com.au/products/tattoo-aftercare-kit`
3. **⌘+Option+U** (Mac) or **Ctrl+U** (Windows) — page source opens
4. **⌘+F / Ctrl+F** → search **`klaviyo`**

Record the match count, and any line reading
`static.klaviyo.com/onsite/js/XXXXXX/klaviyo.js`.

| Result | Meaning | Go to |
|---|---|---|
| Code is **`TbNLXf`** | Right account; blocked at runtime | **Fix B** |
| Code is **anything else** | **Wired to the wrong Klaviyo account** | **Fix A** |
| **0 matches** | App embed not injecting | **Fix C** |

## FIX A — wrong Klaviyo account

*Also answers the open question of which Klaviyo org the upgrade billed to.*

**PLACE 3 — Klaviyo.** `klaviyo.com/integrations`

1. Open the **Shopify** card
2. The store address must read **`iw0xvm-v5.myshopify.com`**
3. Different store, or no Shopify card at all → **you are in the wrong Klaviyo account.** Sign
   out, sign in to the account holding the 58 subscribers, check again
4. Reconnect Shopify **from this Klaviyo page**, not from the Shopify side

> **Do not uninstall the Klaviyo app in Shopify.** The order and customer sync *is* working and
> uninstalling risks losing it.

## FIX B — present but blocked

**PLACE 2 — Shopify admin.** `admin.shopify.com/store/iw0xvm-v5/settings/customer_privacy`

1. Check **Cookie banner**
2. If enabled and set to block tracking until a visitor agrees, that is the cause — most
   visitors never click it, so the script never runs
3. Disabling restores tracking. Check obligations first; a judgement call, not a technical one

## FIX C — embed not injecting

**PLACE 2 — Shopify admin.** `admin.shopify.com/store/iw0xvm-v5/themes`

1. Find **TEL v6.2 — mid-page capture band (11 Sep)**, the one badged **Live**.
   *Ignore theme names — several are misleading. Only the Live badge is true.*
2. **Customize** → bottom-left **jigsaw icon** = **App embeds**
3. **Klaviyo** toggle **OFF** → **Save** → toggle **ON** → **Save**
4. Re-run Step 1

## PROOF ① IS FIXED
Repeat Step 1. **Viewed Product above zero.** It has been zero for three months. Not a setting —
a number.

---

# ② ABANDONED CHECKOUT — not broken, being skipped

**Read before touching anything.** Full config read 13 Sep: flow live, trigger correct
(Checkout Started, no filter), guard correct (Placed Order = 0), all three emails live,
1hr → 23hrs → 2 days. **Nothing is misconfigured.**

`Skipped Send` fired **5 times** in the window carrying 14 checkout starts. The flow **is**
firing; Klaviyo is **refusing to send**, because those people never ticked marketing consent —
and until 01:59 today only **23** profiles in the whole account were emailable.

**So the fix is not in Klaviyo. It is capturing consent at the checkout.**

## STEP 1 — checkout sign-up. 2 minutes.

**PLACE 2 — Shopify admin.** `admin.shopify.com/store/iw0xvm-v5/settings/checkout`

1. Scroll to **Marketing options** (may read "Email marketing")
2. **"Show a sign-up option at checkout"** → **ON**
3. **"Preselect sign-up option"** → **leave OFF**
4. **Save**

> **Why preselect stays off.** Ticking it yields more subscribers, but Australian spam law wants
> consent the customer gave deliberately, and a pre-ticked box is a grey area. For a brand built
> on *Earned. Not given.*, a clean consent record outweighs the extra names. Ben's call.

## STEP 2 — clear one blocker in the flow. 2 minutes.

**PLACE 3 — Klaviyo.** `klaviyo.com/flow/Vg9tuX/edit`

1. Opens **TEL - Abandoned checkout: Still sealed (DRAFT)**. *The name says DRAFT. It is live.*
2. Click the **first email** → **Settings** tab (not Content)
3. **Smart Sending** → **OFF** for this flow

*Why: Smart Sending suppresses anyone emailed recently. 33 people were emailed at 01:59 today,
so it would block the next few days of abandoned-checkout sends.*

## PROOF ② IS FIXED
**PLACE 3 — Klaviyo.** `klaviyo.com/flow/Vg9tuX/edit` → **Analytics** tab.
**"Delivered" above 0.** It has been 0 since the flow was built. Proves itself over days, not
minutes — it needs a *subscribed* person to abandon a checkout.

---

# ORDER OF PLAY

| | Do this | Where | Time |
|---|---|---|---|
| 1 | Visit product page, check Viewed Product | Shop → Klaviyo | 2 min |
| 2 | View page source, record the six characters | Shop, laptop | 3 min |
| 3 | **Stop. Decide which fix from the table.** | — | — |
| 4 | Checkout sign-up ON, preselect OFF | Shopify admin | 2 min |
| 5 | Smart Sending OFF | Klaviyo | 2 min |

**Steps 1–3 before 4–5.** What Step 2 returns decides which fix ① needs — better done once
correctly than three times guessing.
