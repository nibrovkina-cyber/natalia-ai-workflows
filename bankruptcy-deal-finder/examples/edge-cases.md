# Edge Cases

How the Bankruptcy Deal Finder handles unusual situations.

---

### Case: No lots match criteria today
**Input:** All lots in your region are above MAX_PRICE or wrong asset type.
**Agent output:** "No deals above 25% discount today. 47 lots scanned across 2 regions. Closest match: apartment in Mytishchi, 12% discount (below threshold)."
**Why:** Don't send an empty alert. Show that the scan ran and what the closest result was.

### Case: Lot has no clear description
**Input:** Title says "Lot #4492" with no asset type, no area, no address beyond city name.
**Agent output:** Logs as "unclassified, manual review needed." Includes raw data in alert but does NOT estimate market price.
**Why:** Estimating price without area or asset type is worse than no estimate. False positives destroy trust.

### Case: Same lot appears on torgi.gov.ru AND bankrot.fedresurs.ru
**Input:** Identical apartment listed on both platforms with slightly different prices.
**Agent output:** Deduplicates by address + price range (within 5%). Shows as one lot with note: "Listed on 2 platforms. torgi.gov.ru price: 3.2M, fedresurs price: 3.15M."
**Why:** Duplicate alerts waste attention. But the price difference itself is useful information.

### Case: Auction cancelled or postponed
**Input:** Yesterday this lot was active, today status changed to "cancelled" or "postponed."
**Agent output:** If the lot was in your tracked list: "Lot #112233 (apartment Mytishchi): CANCELLED. Reason: debtor settled debt."
**Why:** Tracking status changes prevents you from preparing for an auction that won't happen.

### Case: Market price impossible to estimate (rare asset type)
**Input:** "Industrial crane, 2014, located in Chelyabinsk port." No comparable listings on Avito.
**Agent output:** "MANUAL REVIEW: Industrial crane in Chelyabinsk. Starting price: 1.8M rub. Market estimate: unavailable (no comparables found). Raw data attached."
**Why:** Better to say "I don't know" than to guess wildly on heavy equipment.

### Case: API rate limit on torgi.gov.ru
**Input:** Too many requests in a short period, server returns 429.
**Agent output:** Waits 60 seconds, retries up to 3 times with exponential backoff. If still failing: "Scan incomplete. torgi.gov.ru returned rate limit error. 23 of 47 lots scanned. Will retry next run."
**Why:** Partial data is better than crashing silently. But clearly mark it as incomplete.

### Case: Lot price is suspiciously low (possible data error)
**Input:** Apartment in central Moscow, 80 sqm, starting price 150,000 rub.
**Agent output:** Flags as "VERIFY: price may be data entry error or per-sqm price instead of total. Starting price 150,000 rub for 80 sqm in Moscow center is 99.7% below market."
**Why:** Sometimes platforms list price per sqm instead of total, or there's a decimal error. Don't let the user bid on a data glitch.
