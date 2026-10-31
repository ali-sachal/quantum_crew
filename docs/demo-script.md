# FoodMatch — 3-Minute Demo Walkthrough Script

## 0:00 - 0:30: Problem & Urban Food Desert Context
- **Speaker:** "Hi everyone! Low-income urban food deserts have dozens of corner stores and bodegas that want to stock fresh produce, but commercial wholesalers bypass them due to small ticket sizes. At the exact same time, local community gardens and urban rooftop farms compost 30% of their fresh surplus because they lack distribution."
- **Visual:** Open FoodMatch on `http://localhost:5173`. Show the navigation bar and explain the three core technology pillars: **Google Gemma 4 (Gemini API)**, **Snowflake with CoCo**, and **Solana Devnet Agent Registry**.

## 0:30 - 1:15: Farmer Upload & Gemma 4 Multimodal Inspection
- **Action:** Click **Farmer Upload** (`/`).
- **Speaker:** "A farmer at South Bronx Green Workers Co-op snaps a photo of freshly harvested Roma tomatoes and drags it into FoodMatch."
- **Action:** Drag and drop a produce photo, set quantity to 40 kg, floor price to $2.10/kg, and click **Inspect with Gemma 4 & Publish Listing**.
- **Speaker:** "Google Gemma 4 processes the image via the Gemini API, evaluates color tautness and surface blemishes, assigns a USDA-aligned Quality Grade (Grade A), writes a market description for corner store shoppers, and recommends a suggested price of $2.85/kg."
- **Visual:** Point out the generated AI result card with the grade badge, freshness notes, and verified Solana badge.

## 1:15 - 1:55: Snowflake CoCo Demand Prediction & Store Dashboard
- **Action:** Click **Store Dashboard** (`/dashboard`).
- **Speaker:** "Now let's switch to the corner store owner's view in ZIP 10451. How does a corner store know what day to buy produce?"
- **Visual:** Highlight the **Neighborhood Fresh Produce Deficit Chart**.
- **Speaker:** "Using a Snowflake consumer spending and census dataset developed with CoCo, FoodMatch predicts unmet demand across every day of the week. Friday shows a peak deficit score of 9.4/10 because paychecks arrive and corner store produce coolers are bare. The store owner sees our newly listed Roma tomatoes ranked at the top based on haversine distance and deficit urgency."

## 1:55 - 2:40: Autonomous Negotiation with Floor Guardrails
- **Action:** Click **Bargain** on the tomato listing to open the **Negotiation Chat** (`/negotiate/1`).
- **Speaker:** "The store owner wants to negotiate a discount for their Friday rush."
- **Action:** Type: *"Can you sell this batch for $1.80/kg?"* and click Send.
- **Speaker:** "Watch the autonomous Gemma 4 seller agent respond in real-time. Notice the programmed guardrail: the farm's floor cost is $2.10/kg. Gemma 4 refuses the lowball offer, explains the farm cooperative's sustainability cost, and counters at $2.45/kg!"
- **Action:** Type: *"Let's do $2.45/kg."* Send, and then click **Accept Deal & Settle Onchain**.

## 2:40 - 3:00: Verifiable Solana Onchain Trust & Closing
- **Visual:** Show the green **Deal Verified Onchain** banner and click **View on Solana Explorer**.
- **Speaker:** "Upon acceptance, the deal receipt and a 5-star reputation score are cryptographically committed to the Solana Devnet Agent Registry via our isolated adapter module. Anyone can verify this transaction on Solana Explorer. FoodMatch eliminates food waste, turns bodegas into fresh produce hubs, and builds verifiable trust onchain. Thank you!"

