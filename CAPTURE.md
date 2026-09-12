# The capture engine — what to build after Chapter One opens

Written on launch night, 10 September 2026, while the doors were open. Nothing here was
done tonight on purpose: every item touches a live marketing system or the live theme, and
launch night is the wrong time for both. This is the build sheet for the morning after.

## Why this exists

Ben's own framing, the afternoon of launch day:

> *"re targetting pool and klavyio very important as i dont think my intention is to stess
> about how many sell its more about the vision and people engaging."*

That is the right instinct and it has a hard consequence: **448 units is a ceiling you hit
once. The list has no ceiling.** Tonight is the largest traffic spike this brand will ever
get for the first time, and most of the people arriving will not buy on the first visit.
Whatever does not capture them is gone — Instagram traffic is anonymous, and the Meta pool
decays through tracking prompts, in-app browsers and expiring attribution windows.

So the question that matters is not how many sold. It is: **what caught the ones who
didn't?**

## What already works — do not rebuild these

Three things are better than they look, and it is worth knowing before touching anything.

**The homepage product plate handles sellout correctly.**
`theme/sections/tel-product.liquid` branches on `variant.available`. When it goes false the
button becomes *"Chapter One is closed"* and links to `#tel-newsletter` — straight into the
First access band. Sellout already feeds the list on the homepage. That was well built.

**Four Klaviyo flows are live despite "(DRAFT)" in their names.** The suffix is in the flow
*name*; the API `status` says `live`. Welcome (`TEZ6PM`), Abandoned checkout (`Vg9tuX`),
Browse abandonment (`YgAs6b`) and all three post-purchase flows are running. Rename them so
the labels stop contradicting reality.

**Meta is properly set up.** Domain verified (the `facebook-domain-verification` tag carried
into v6.1 at `theme/layout/theme.liquid:7`), pixel connected with data access granted, and
Facebook & Instagram is a published sales channel so the catalog can sync.

## The four gaps, in priority order

### 1. The product page has no sellout capture — the biggest hole

`theme/templates/product.json` renders `main-product`, which is Shopify's stock Prestige
section. It is **not in this repo and has never been customised**. At sellout it shows a grey
"Sold out" button and nothing else.

That matters because the product page is where the traffic lands. The founding-price link
redirects there:

```
telcollection.com.au/discount/TELTAKEOVER?redirect=/products/tattoo-aftercare-kit
```

So every person arriving from the email after the last set goes — at 11pm tonight, tomorrow,
next week — hits a dead end and leaves no trace. **These are the warmest people this brand
will ever have.** They wanted in and could not get in. That is a better list than the buyers.

**Fix:** enable **Klaviyo Back in Stock**, which installs a "Notify me when available"
button on sold-out product pages and writes subscribers straight into Klaviyo. The account
already supports it — the `create_back_in_stock_subscription` endpoint is available.

Then take flow **`SuavPL` — "TEL - Back in stock: Doors open again"** out of draft. It is the
only genuinely-draft flow in the account and it is the exact flow this needs.

### 2. No popup — nothing catches a visitor who scrolls past

| Where | File / ID | State |
|---|---|---|
| Homepage "First access" band | `theme/sections/tel-newsletter.liquid` | **live**, but **last** in `templates/index.json`'s section order |
| Theme newsletter popup | `theme/sections/overlay-group.json` | `"disabled": true` |
| Klaviyo popup "TEL · First access popup" | `WirxQ2` | **draft**, and `updated_at` equals `created_at` (4 Sep 14:46:47) — created and never edited |

The band works but sits at the bottom of a long page, so most visitors never reach it. The
Klaviyo popup was left off on launch night deliberately: a form whose updated time equals its
created time is an untouched shell, and an off-brand popup costs more on a store selling "no
half measures" than the addresses it collects.

**Fix:** build `WirxQ2` properly in TEL's dark/gold, target homepage and product page, ~15s
delay or 40% scroll, and point it at a named list so the live Welcome flow (`TEZ6PM`) fires
on join. Then **move `tel_newsletter` up** the order in `templates/index.json` — above
`tel_chapter`, or add a second instance mid-page.

Note the band posts through Shopify's `{% form 'customer' %}` with `contact[tags] =
newsletter`, so joins arrive as Shopify customers and reach Klaviyo through the store
integration rather than as a direct list add. **Confirm that path actually triggers `TEZ6PM`**
before relying on it — if it does not, the welcome never fires for anyone who joins via the
band.

### 3. The Squires Ink list only exists inside Mailchimp

Roughly 7,000 past clients, reachable tonight only because Mailchimp holds them. The Klaviyo
import never landed — the exclusion list "Squires Ink — Imported Sep 2026 (NO founding
price)" has **0 profiles**, which is why the founding-price exclusion guarded nobody and why
the Klaviyo Doors Open email reached 21 inboxes.

Rebuild it properly, with consent, into Klaviyo. Not a panic import — a real one with a
lawful basis, because this list is the single largest owned asset either business has.

### 4. Sending domain is not authenticated

Mailchimp is sending from the shared `mailchimpapp.com` rather than an authenticated
`telcollection.com.au`. That caps deliverability and puts the brand's reputation on somebody
else's domain. A next-week job, not a tonight job — but it should not wait past Chapter Two.

## Copy, ready to paste

Written in the same voice as the site so tomorrow is a paste, not a drafting session.

**Popup — First access**

> FIRST ACCESS
>
> **Named when it's earned.**
>
> Chapter One is aftercare. What follows gets named when it's ready, and this list hears
> first.
>
> [ Your email address ] [ Join ]
>
> One email when it opens. Nothing else.

**Back in stock — subject lines**

> The doors open again
> Chapter Two has a date
> You were on the list

**Back in stock — body**

> You went looking for a set after the last one was gone.
>
> That's the whole reason this email exists. Chapter One was five hundred, it closed the way
> it said it would, and everyone who missed it is on this list.
>
> **[ CHAPTER TWO IS OPEN ]**
>
> Same set. Same standard. Same promise that when they're gone, they're gone.
>
> Look after the art.
>
> — Benny

**Sold-out button on the product page**

> Notify me when the doors reopen

## Verification

Each item is checkable, so nothing goes in on faith:

1. **Back in stock** — set the variant to 0 in a preview or on a test product, load the
   product page, confirm the notify button renders. Subscribe with a `+test` address and
   confirm the profile appears in Klaviyo. Restock and confirm `SuavPL` sends.
2. **Popup** — load the site in a private window, confirm it fires on the right delay, join
   with a `+test` address, confirm the profile lands in the named list **and** that `TEZ6PM`
   sends the welcome.
3. **Band → Welcome path** — join through the homepage band with a different `+test`
   address, then check whether a Klaviyo profile appears and whether `TEZ6PM` fires. If it
   does not, the band is capturing into Shopify only and the welcome is silently missing.
4. **Section order** — after moving `tel_newsletter`, read `templates/index.json` back from
   the live theme and confirm the checksum matches the repo, the way every other theme change
   this week was verified.
5. **Sending domain** — send a test after authentication and confirm the headers show
   `telcollection.com.au`, not `mailchimpapp.com`.

## The one rule

Everything here is a marketing-system change, not a store change. **None of it justifies
touching a verified-clean live theme while traffic is on it.** Do it in the morning, verify
each piece, and keep the repo and the live theme byte-identical the way they have been all
week.
