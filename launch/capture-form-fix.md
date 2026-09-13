# Capture fix — publish the signup form

**The finding:** Klaviyo holds exactly one form, `TEL · First access popup` (`WirxQ2`,
version `28243577`), **status: draft since 4 Sep, never updated.** `query_form_values`
returns an **empty result set** over 30 days — zero views, zero submits, never rendered.

~1,300 paid landing page views at $0.13 each reached a page with no way to leave an email
address. That is why the launch sequence went to 20 people.

**Why this is a UI job, not an API one:** the Klaviyo API can only *create* forms with
`status: "draft"` — the field is a fixed constant, and there is no publish endpoint. Going
live has to happen in the Klaviyo form editor. Below is everything needed so it is a
five-minute job.

---

## Replace the copy first

The existing form was written for a password-gated store — "first access" to something that
has already opened. Publishing it as-is would read as stale to anyone who visits.

### Phase 1 — now until Mon 14 Sep 23:59 (real deadline, real urgency)

> **The founding price closes Monday.**
>
> The Ritual Duo at **$49.99** instead of $59.95 — the balm and cream we use on fresh ink
> at Squires, sealed as one set.
>
> Drop your email and we'll send the code.
>
> `[ SEND ME THE CODE ]`
>
> *Chapter One. First release.*

Delivers `TELTAKEOVER` through the welcome flow (`TEZ6PM`) rather than printing it on the
popup, so the code is not scraped straight off the page by non-subscribers.

### Phase 2 — from Tue 15 Sep, when the founding window has closed

> **Look after the art.**
>
> Aftercare built in a working tattoo studio, on real healing ink. Join the list for
> Chapter Two before it drops.
>
> `[ JOIN THE LIST ]`

No discount in phase 2. It protects margin on a $59.95 premium product and keeps the brand
from training buyers to wait for a code. The next drop is the incentive.

---

## Settings that matter

| Setting | Value | Why |
|---|---|---|
| Form type | Popup | Already correct on the draft |
| Devices | Desktop + mobile | Meta traffic is overwhelmingly mobile |
| Trigger | 5s delay **or** 30% scroll | Fires before the bounce, after the hero lands |
| Exit intent | On, desktop only | Second chance at no extra cost |
| Targeting | All pages, **including** `/products/tattoo-aftercare-kit` | The PDP is where the paid traffic lands |
| Don't show to | Already-identified / subscribed profiles | Stops it nagging existing subscribers |
| **Record UTM params on submit** | **On** | The one to not skip — attributes each signup to the ad that produced it |
| Adds to | `Email List` (`V9Rbbr`) | Feeds the welcome flow `TEZ6PM`, already live |

`record_utm_params_on_submit` is worth calling out: with it on, every signup carries the
campaign that produced it, so cost-per-subscriber by ad becomes readable instead of guessed.

---

## Prove it worked

Run `query_form_values` over `last_7_days` grouped by `form_id`. Today it returns `[]`.
Once live it must return rising `viewed_form` and `submits`. A still-empty result means the
form did not actually publish — check it is enabled on the live theme, not just saved.

Benchmark: a popup like this should convert **5–15%** of unique views. At the ~100–350
landing page views a day the traffic campaign was producing, that is roughly 10–35 subscribers
a day, against a current list of 20.
