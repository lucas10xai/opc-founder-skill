# Vietnam notes: pricing

Vietnam notes for this skill. Prompts for you to check, not rules. Rules change (several tax and invoicing
rules changed in 2025 and 2026), so confirm anything specific with the authority or a professional.

## VND price points
- Round to 1,000 or 5,000. Common endings are 39,000, 45,000, 49,000, 59,000, 99,000. Test two neighbouring points
  rather than one.
- Buyers read "k" notation (45k = 45,000₫). In the panel, keep prices as whole VND in the profile.
- Use whole VND numbers in `founder/numbers.json` (45000, not 45 and not 45.0).
- For higher tickets (millions of VND) round to 100,000 or 500,000 and consider whether instalments change what
  the buyer compares (monthly amount vs total).

## Anchors
- Delivery apps (Grab, ShopeeFood, Be) show prices with platform markup. Compare your in-shop price with your
  delivery price and the app price, and decide whether you want the same price on every channel.
- Marketplace comparison: a large share of buyers compare with Shopee or TikTok Shop for any product that can
  be shipped. Check three listings and note price, shipping and shop rating. Do not guess them.
- Bundles and freeship thresholds change the effective price; include them when reading the answers.

## Reading panel answers in VND
- Answers like "too expensive" cluster around a few round numbers. Look at the median and the share at
  each price point, not one extreme answer.
- Simulated buyers are not customers: run the real-world test (`/founder-launch`) with a real price in VND.
- Check price vs unit cost with `/founder-cfo` in VND, including platform commissions per channel.

## Cautions
- Do not copy Western price ladders such as 9.99 into VND by conversion. Pick local price points.
- Promotion days (11/11, 12/12, Tết, 8/3, 20/10) distort comparison; note whether competitors show campaign prices.
