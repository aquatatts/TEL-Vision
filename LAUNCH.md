# TEL Collection — launch runbook (Thursday 10 September 2026)

Theme to publish: **TEL v6 — LAUNCH CANDIDATE (Thu 10 Sep)**
Admin → Online Store → Themes → the v6 card → Publish.
Preview before publishing: the **Preview** button on the same card (or `https://iw0xvm-v5.myshopify.com/?preview_theme_id=142936834111` while logged into admin).

v6 is already written in the *open* state: no "doors open Thursday" copy anywhere. The password page is the only place that still speaks pre-launch, and it disappears when the password comes off.

The `theme/` folder in this repo is a byte-for-byte snapshot of every file changed in v6, plus `theme/pages/` for the page bodies that were rewritten in admin.

## Wednesday evening (dry run, still gated)

1. Publish v6 while the storefront password is still on. Nobody outside sees anything; you get a real render instead of the editor preview.
2. Walk the site on a phone and a laptop with the password. Checklist below.
3. If anything is wrong, v3 ("TEL v3 — LIVE (2 Sep)") is untouched: Publish it again to roll back in one click.

## Thursday morning

1. Online Store → Preferences → Password protection → untick, Save. That is the launch.
2. Check the homepage loads without the gate on a phone in a private window.
3. Inventory: decided. The site reads live stock, so launch morning shows **450 of 500** and counts down with every order. Leave the variant quantity at 450. Sets sold over the counter at Squires Ink do not touch Shopify stock, so knock those off the variant quantity by hand (Products → The Ritual Duo → Quantity) to keep the count honest. When it reaches zero the homepage flips to "Chapter One is closed" and the product page button changes on its own.

## Walk-through checklist (what to look at, in order)

Homepage
- Hero: sealed set with the monogram card on desktop, sealed box on mobile, "Earned. Not given." and the gold button above the fold on a phone.
- Spec strip: 60 ml × 2 · Sealed as a set · First run of five hundred · Free shipping Australia-wide.
- Product plate: real photo (jars beside the box), price ledger, gold button, "Chapter One · 450 of 500 sets remaining" under it.
- Two stages: the two open jars sit under the intro; the second step keeps its bottom hairline; button goes to the Healing Guide.
- Proof strip scrolls sideways on a phone, five columns on desktop.
- From the chair: Valerio portrait, quote, disclosure line, button to Trusted By.
- Founder: settled-ink chest photo, landscape, quote and ornament rule, button to the founder page.
- Chapter: big 500, "Chapter One is open…", meter reading 450 of 500.
- First access: Chapter One card beside the form. Submit a test email; the success message should appear in place.

Product page (most ad traffic lands here)
- Title in sentence case, price, lead, gold spec line, "Chapter One · N of 500 sets remaining", gold Add to cart, express payment button, assurance line, Healing Guide link.
- Accordions: The Ritual · How to use · What's in it · Heavy work · Built to a standard · From the founder · Shipping and returns.
- Gallery on desktop is a carousel with thumbnails below; the two portrait shots are last so the mobile carousel does not jump.
- Below: Two stages (with image), Proof strip, From the chair, Questions. No empty review box.
- Sticky add-to-cart bar appears on mobile once you scroll past the button.

Other pages
- Contact now shows the email, Instagram, studio address and hours above the form (it was hidden before).
- Our Aim, The Founder, Trusted By, FAQs and The Healing Guide all use the same gold and the theme's serif; Trusted By leads with Valerio and no longer has an empty reviews block.
- Header: no search icon; menu has Healing Guide as the fifth item. Footer has studio address and hours, Terms of Service link, truck and lock icons.
- Newsletter popup is off for launch week.

## Open before Thursday

1. **Re-paste the meta description** (see below). The saved one still says "the years after".
2. **New back-tattoo studio image.** Upload it to Content → Files at 4000 px on the long edge (Shopify rejects anything over 25 MP, and the camera originals are 42 MP). Tell me the filename and I'll place it — the natural home is the "From the chair" band or the Trusted By page, and it can go into the product gallery if it reads as product context rather than portfolio.
3. **Release video, Sunday.** Not on the site yet. Decide whether it lands as the hero, a band below the two-stage section, or Instagram-only for launch week.

## Things only you can do in admin

- **Homepage meta description and social sharing image (optional now).** Plain English: the *meta description* is the sentence Google shows under "TEL Collection" in search results; the *social sharing image* is the picture that appears when someone pastes telcollection.com.au into Instagram, WhatsApp, Messenger or Facebook. Both were empty. v6 now ships defaults for the homepage (the sentence below, and the sealed-set hero as the picture), so launch is covered. If you want to set them officially so every page and every app reads the same thing: Online Store → Preferences → "Title and meta description" (paste the sentence) and "Social sharing image" (upload the sealed-set frame, DSC02912 or the 4000 px copy from Content → Files). Whatever you set there takes over from the theme defaults automatically.
  Sentence: "Sealed two-step tattoo aftercare from a Surfers Paradise studio. Restore Balm for fresh ink, Recovery Cream for the months after. Free shipping Australia-wide."
  **Re-paste this.** The sentence currently saved in Preferences says "the years after". That claim now belongs to the everyday moisturiser (Chapter Two), not to Recovery Cream — see "Product ladder" below. Online Store → Preferences → Meta description → replace → Save.
- ~~**Hide the five empty collections.**~~ Handled in the theme instead. `layout/theme.liquid` emits `<meta name="robots" content="noindex,follow">` on any collection with zero products, and on Shopify's default `frontpage` collection. Movement, Threads, Vision and Collective stay reachable but stay out of Google. It is self-correcting — the noindex lifts the moment a chapter has stock, with no edit needed. If you'd rather they were gone entirely, Products → Collections → open one → **Publishing** card → **Manage** → untick **Online Store** → **Done** → **Save**. Optional.
- ~~**Social sharing image.**~~ Handled in the theme. The Preferences field only accepts a device upload (you can't pick a file already in Content → Files, and there's no API for it), so `layout/theme.liquid` now serves the retouched sealed-set hero as `og:image` directly from the CDN, with `twitter:card=summary_large_image` so it renders as a wide card. Anything you later set in Preferences still overrides it.
- **Checkout branding.** Settings → Checkout → Customize: square TEL mark as logo, gold `#C9A24B` accent, dark background if the plan allows.
- ~~**Full ingredient lists (INCI).**~~ Done. Both lists are now published verbatim from the jars on the product page ("What's in it"), the FAQs page and the Shopify product description. The Healing Guide carries a "Why the balm is petrolatum" section explaining the first ingredient.
- **"FDA GMP" claim.** The proof strip says "ISO 22716 · GMP"; the accordion says "ISO 22716 and FDA GMP". Confirm the manufacturer's certificate wording before launch; if it is only ISO 22716, drop "FDA" from the accordion.
- **Password page on the live v3 theme.** It still shows "5.0 · 10 verified reviews", which cannot be backed up yet. In v6 that line reads "Built in a working studio · Surfers Paradise". If the gate stays up past Sunday, change the line in the v3 editor too (Theme editor → password page → Proof line).
- **Two leftover files** in v6 that the API is not allowed to delete: `sections/tel-spec-strip-probe.liquid` (now emptied, no preset) and `templates/product.pre-order.json`. Both are harmless; delete them in Edit code if you want a clean list.
- **Klaviyo.** Both signup forms tag the Shopify customer `newsletter`. Check Klaviyo's Shopify integration is syncing subscribers and that a welcome email exists; the on-site success copy no longer promises one.
- **Judge.me.** The app embed is still installed but the badge and widget are removed from the product page and Trusted By. Re-add them once the first five or so reviews are in.

## Brand architecture — keeping the fragrance pivot cheap

TEL is a lifestyle brand that started in aftercare, not a tattoo-aftercare brand. Chapter Two may be a signature scent. The site is already built so that pivot is a content edit, not a rebuild — keep it that way:

- **The category word never goes in brand-level furniture.** Logo lockup, homepage H1, tagline, email footer, Instagram bio, packaging outer. Right now the homepage H1 is "Earned. Not given." — category-free, and it works for a fragrance unchanged. The word "tattoo" lives only in product-level copy: the product page, the Healing Guide, the Ritual collection. Those are chapters; they are *meant* to be specific.
- **The organising idea sits one level above tattoos, and it is already written.** "Built on discipline. Driven by purpose. Proven under the gun." · "TEL isn't a brand you buy once. It's a standard you choose." · "People who hold themselves to a higher standard shouldn't have to drop it at the studio door." That last line is the pivot, already on the Our Aim page.
- **The studio is origin, not category.** Hermès was a saddlery; nobody thinks it is about horses. The studio stays forever as *where the standard was proven*, which is exactly how Our Aim frames it. Never let it become *what the brand is about*.
- **The bridge to fragrance is permanence.** A tattoo is the most permanent thing you put on your body; a signature scent is the most permanent thing about how you are remembered. Both are marks you choose to wear. "Earned. Not given." carries across unchanged.
- **Every homepage string is a theme setting.** The `tel-*` sections (hero, spec strip, product, steps, proof, band, chapter, newsletter) are generic. A fragrance homepage is a copy-and-image swap in the theme editor.
- **The list is the asset that crosses categories.** "One email when Chapter Two opens" is the only thing that carries a Ritual buyer into a fragrance launch.
- **One thing that will look odd later and should not be changed now:** the product handle `/products/tattoo-aftercare-kit`. It is earning search traffic; leave it. New chapters get category-free handles.

## Product ladder — read this before writing any new copy

Chapter Two is a premium everyday moisturiser for tattooed skin. To leave it room, the site no longer says Recovery Cream is the jar you use forever. The ladder is:

| | Job | Horizon |
|---|---|---|
| Restore Balm | Seals the fresh wound | Days 1–14 |
| Recovery Cream | Carries the piece through settling | The months after, and as long as you want it looking sharp |
| **Chapter Two — the moisturiser** | Maintenance, daily, on healed work | **For as long as you own the piece** |

Recovery vs maintenance is a real distinction, not a marketing split — the name *Recovery* Cream already argues it. Do not let "for as long as you own the tattoo", "for life" or "forever" reattach to Recovery Cream anywhere; that phrase is reserved.

The Healing Guide's ∞ panel now belongs to **the daily habit**, not to the jar, so it still answers the "lost in year three" argument without over-claiming.

Our Aim → "Where it's heading" now names the moisturiser first in the pipeline. It is not mentioned anywhere in the buying flow (product page, homepage), so nobody holds off buying the Duo waiting for it.

## What changed, in one screen

Homepage: hero now uses the shoot (was a portrait placeholder); real photo on the product plate (was a CGI render); two-stage section gets the texture image and a fixed hairline; studio and founder bands merged around the settled-ink photo; new "From the chair" band; sets-remaining count next to the price; launch-state copy; newsletter copy no longer assumes a purchase.
Product page: story sections and a five-question FAQ added below the gallery; "What's in it" accordion; sets-remaining and assurance lines; Healing Guide link; Judge.me removed; payment-terms block (renders nothing in AU) removed; carousel gallery with portraits last.
Theme-wide: gold `#C9A24B` everywhere (pages were still copper); favicon set; theme fonts on every page (the pages named a font family that was never loaded, so headings fell back to Georgia); mono micro-type raised to 10.5–11 px; placeholder and mute contrast raised; Google font no longer render-blocking; empty alt text fixed; proof strip made a real list; search icon off; popup off; footer studio details.
Store data: five 4000 px frames added to Files; two added to the product gallery and the gallery reordered; Healing Guide in the main menu; Terms of Service in the footer; Ritual collection given an image and description.
