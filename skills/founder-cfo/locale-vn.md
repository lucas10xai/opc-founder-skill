# Vietnam notes: CFO and numbers

Vietnam notes for this skill. Prompts for you to check, not rules. Rules change (several tax and invoicing
rules changed in 2025 and 2026), so confirm anything specific with the authority or a professional.

## Currency (VND)
- Set `"currency": "VND"` in `founder/numbers.json`. Use whole numbers, no decimals, no thousand separators
  in the file. Prices are often in thousands: write 45000 for a 45,000₫ item, not 45.
- Show amounts in documents like `45,000₫`. Say "million" or "triệu" in prose only when clear (for example
  12 triệu = 12,000,000₫).
- If the user thinks in "k" (45k), convert and confirm the full number before using it.

## Costs to remember
- Rent paid several months up front plus a deposit (đặt cọc). Put this in startup, not monthly cost.
- Accounting (kế toán) fee and e-invoice provider fee, monthly or per invoice.
- Platform commissions: Shopee, TikTok Shop, Lazada, Grab, ShopeeFood and other delivery apps charge a
  percentage and fees that change. Treat it as a per-unit variable cost for each channel and read the current
  fee from the platform's own seller page.
- Payment fees: card, QR, e-wallet. Check each provider's published rate.
- COD refusals and return shipping as a cost per order.
- Staff: salary plus employer social insurance (BHXH), health insurance and Tết bonus (thưởng Tết).
- Taxes: VAT treatment and personal income tax for household businesses changed in 2025 and 2026. Check the
  current rule at https://gdt.gov.vn and with an accountant. Never enter a rate from memory.
- Licences and permits: see `founder/compliance.md`; add costs only after the user confirms them.

## Cash flow
- Tết month: lower sales for some businesses, bonuses and supplier prepayment for others. Model a buffer.
- Platform payouts arrive after a delay; keep working cash for it.

## Honest limits
- These are projections. Confirm every number with a local accountant (kế toán). Nothing here is tax advice.
