# Assumptions, Boundary Limits & Ground Truth Specifications

## 1. Prototype & Simulation Nature
* **Simulated Operational Actions**: No physical external airline reservation system (GDS such as Amadeus, Sabre, or Navitaire) or banking payment gateway is connected. All actions (e.g. `REFUND_REQUESTED`, `MEAL_VOUCHER_ISSUED`, `LOUNGE_ACCESS_ISSUED`, `HOTEL_REQUESTED_FOR_DELAYED_HOURS`, `ESCALATED_TO_HUMAN`) are simulated state transitions and are explicitly tagged with `[SIMULATED DEMO ACTION]`.
* **Simulated Escalation Queue**: Escalation tickets (e.g., `ESC-TCK-XXXXXX`) simulate hand-offs to human supervisory teams and legal grievance desks.

## 2. Authoritative Ground Truth & Data Isolation
* **Closed World Dataset**: The supplied data pack is the exclusive source of customer facts, booking facts, transaction history, and airline policies.
* **Zero Inventory Fabrication**: The authoritative data does not supply alternative flight schedules, connecting flight numbers, or live seat availability. The agent states its entitlement to free 24-hour rebooking under Section 5.1 but never fabricates a flight number, seat number, or schedule.
* **Temporal Grounding**: The exercise date is strictly **Wednesday, 23 September 2026**.
* **Known Customers**: Only three passengers exist in the system:
  1. **Priya Nair** (Gold, PNR: `SK4821X`, Outbound `SK-204` Cancelled, Return Goa→Delhi Unaffected).
  2. **Arvind Kulkarni** (Silver, PNR: `TR1190B`, Flight `SK-118` Delayed 4h).
  3. **Meher Kaur** (Platinum, PNR: `WL7742`, Flight `SK-305` Delayed 6h).

## 3. Strict Service Rule Boundaries
* **Cancellation Choice**: The customer must be allowed to choose between (A) Free rebooking within 24 hours or (B) Full refund.
* **Refund SLA & Method**: Refunds for airline-caused cancellations are processed within 7 business days strictly to the original payment method. Demands for "cash payouts" or alternate cards/accounts are rejected.
* **Delay Compensation Steps**:
  * $< 3$ hours: ₹500 meal voucher.
  * $3$ to $5$ hours (Arvind 4h): Meal voucher + lounge access. Hotel accommodation is strictly prohibited.
  * $> 5$ hours (Meher 6h): Meal voucher + lounge access + transit day-room hotel covering only the delayed-hours window. Full-night hotel accommodation is strictly prohibited.
* **Fare Difference Waiver Threshold**: Agents have authority to waive fare differences up to ₹1,500. Any waiver exceeding ₹1,500 (e.g. Meher's ₹2,000 difference) strictly mandates supervisor escalation.
* **Loyalty Entitlements**: Gold and Platinum tiers receive priority rebooking and first access to next-available seats, but strictly no complimentary cabin upgrades or extra monetary compensation beyond standard disruption policy.

## 4. Architectural & Safety Boundaries
* **LLM Subservience**: The Large Language Model is strictly confined to natural language comprehension, intent/entity extraction, and empathetic response phrasing. Under no circumstances can the LLM override the deterministic Python policy engine.
* **Data Privacy Protection**: The demo customer selector is provided for evaluation convenience. However, the system enforces passenger data isolation: cross-passenger PNR inquiries are rejected at the gateway.
* **Deterministic Offline Fallback**: The application does not require any paid external LLM API key to operate at 100% capacity; it features an embedded deterministic baseline parser.
