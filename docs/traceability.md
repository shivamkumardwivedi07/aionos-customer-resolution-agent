# End-to-End Scenario Traceability

This document provides complete traceability from raw user input to final response and audit record for all three evaluation scenarios.

---

## 🛫 Scenario 1: Priya Nair (Cancelled Flight & Upgrade Demand)

* **Raw Customer Input**:  
  `"I am absolutely furious! My flight SK-204 from Delhi to Goa was cancelled. I want a full cash refund immediately and a free business-class upgrade on my return flight for all this trouble!"`
* **Detected Intents**: `["REFUND_REQUEST", "UPGRADE_REQUEST"]`
* **Detected Sentiment**: `Furious`
* **Extracted Entities**:
  * `customer_name`: "Priya Nair"
  * `flight_number`: "SK-204"
  * `wants_cash`: `True`
  * `requests_cabin_upgrade`: `True`
* **Customer Context**:
  * ID: `CUST-001`, Tier: `Gold`, Prior Complaints: `1 (Delayed baggage, resolved with voucher)`
* **Booking Context**:
  * PNR: `SK4821X`, Flight: `SK-204`, Route: `Delhi → Goa`, Date: `Wed 23 Sep 2026`
  * Status: `Cancelled`, Disruption Reason: `Operational reasons`
  * Return Leg: `Goa → Delhi`, Date: `Fri 25 Sep 2026`, Status: `Unaffected`
* **Policy Rules Evaluated**:
  1. `Section 5.1 & 5.3`: Cancellation qualifies for full refund processed within 7 business days strictly to original payment method. Cash payout denied.
  2. `Booking SK4821X`: Return flight confirmed `Unaffected`.
  3. `Section 5.5 & 7.0`: Gold tier does not grant complimentary cabin upgrades. Free upgrade request exceeds policy authority.
* **Decisions Generated**:
  * Refund: `Eligible: True` (Restrictions: `ORIGINAL_PAYMENT_METHOD_ONLY`, `7_BUSINESS_DAYS`).
  * Cabin Upgrade: `Eligible: False` (Escalation: `True`, Reason: `COMPENSATION_EXCEEDS_POLICY`).
* **Simulated Actions Executed**:
  * `REFUND_REQUESTED` (`ID: SIM-REF-XXXXX`, Amount: 100% fare, SLA: 7 business days).
  * `ESCALATED_TO_HUMAN` (`Ticket: ESC-TCK-XXXXX`, Priority: Standard).
* **Escalation Trigger**: `COMPENSATION_EXCEEDS_POLICY`
* **Final Grounded Agent Response**:
  > *"I completely understand your frustration, Priya, and I sincerely apologize for the disruption to your travel plans today.*
  >
  > *I can confirm that your outbound flight SK-204 (Delhi → Goa) has been cancelled due to operational reasons. Please note that your return flight (Goa → Delhi on Friday, 25 September 2026) remains confirmed and unaffected.*
  >
  > *Under Service Rules Section 5.1 and 5.3, I have initiated a full refund request for you. Per airline policy, refunds are processed within 7 business days and issued strictly to your original payment method (cash payouts or alternate accounts are not permitted).*
  >
  > *Your request for an out-of-policy cabin upgrade or additional compensation exceeds automated agent authority (Ticket ID: ESC-TCK-XXXX). I have escalated your request directly to our Senior Customer Relations team for supervisory review."*
* **Policy Citations Displayed**:
  * `Service Rules Section 5.1: Cancellation Rebooking Rule`
  * `Service Rules Section 5.3: Refund Processing Rule`
  * `Service Rules Section 5.5: Loyalty Tier Rule`
  * `Service Rules Section 7.0: Prohibited Actions`

---

## 🛫 Scenario 2: Arvind Kulkarni (4-Hour Delay & Hotel Demand)

* **Raw Customer Input**:  
  `"I am very frustrated. My flight SK-118 to Bengaluru is delayed by 4 hours and I missed my connecting client meeting. Because of this long delay, I need hotel accommodation right now."`
* **Detected Intents**: `["DELAY_COMPENSATION_INQUIRY", "HOTEL_REQUEST"]`
* **Detected Sentiment**: `Frustrated`
* **Extracted Entities**:
  * `customer_name`: "Arvind Kulkarni"
  * `flight_number`: "SK-118"
* **Customer Context**:
  * ID: `CUST-002`, Tier: `Silver`, Prior Complaints: `0`
* **Booking Context**:
  * PNR: `TR1190B`, Flight: `SK-118`, Route: `Mumbai → Bengaluru`, Date: `Wed 23 Sep 2026`
  * Status: `Delayed 4.0 hours` (07:10 $\rightarrow$ 11:10)
* **Policy Rules Evaluated**:
  1. `Section 5.2`: Delays between 3h and 5h qualify for a meal voucher and lounge access.
  2. `Section 5.2 Restriction`: Hotel accommodation requires delay $> 5$ hours. For 4h delay, hotel is strictly denied.
  3. `Meeting Compensation`: Airline disruption policy does not compensate third-party missed meetings.
* **Decisions Generated**:
  * Meal & Lounge: `Eligible: True`.
  * Hotel Assistance: `Eligible: False` (Restriction: `NO_HOTEL_ACCOMMODATION`).
  * Escalation: `False` (Customer frustration alone is not a prohibited escalation trigger).
* **Simulated Actions Executed**:
  * `MEAL_VOUCHER_ISSUED` (`ID: SIM-VOUCH-XXXXX`, Airport dining allowance).
  * `LOUNGE_ACCESS_ISSUED` (`ID: SIM-LNG-XXXXX`, Valid at Mumbai Airport until 11:10).
* **Final Grounded Agent Response**:
  > *"I completely understand your frustration, Arvind, and I sincerely apologize for the disruption to your travel plans today.*
  >
  > *Your flight SK-118 (Mumbai → Bengaluru) is currently delayed by 4.0 hours, with an updated departure time of 11:10.*
  >
  > *I have issued a complimentary Full Airport Meal Allowance for airport dining.*
  >
  > *I have activated complimentary airport lounge access for you while you wait.*
  >
  > *Regarding hotel accommodation: Under Service Rules Section 5.2, hotel assistance is only provided for delays exceeding 5 hours. Because your delay is 4.0 hours, hotel accommodation cannot be authorized."*
* **Policy Citations Displayed**:
  * `Service Rules Section 5.2: Delay Compensation Rule`
  * `Service Rules Section 5.5: Loyalty Tier Rule`

---

## 🛫 Scenario 3: Meher Kaur (6-Hour Delay & ₹2,000 Fare Difference)

* **Raw Customer Input**:  
  `"My flight SK-305 is delayed by 6 hours. As a Platinum member, I demand a full night's hotel stay and want to rebook onto a different flight with a ₹2,000 higher fare with the fare difference waived."`
* **Detected Intents**: `["DELAY_COMPENSATION_INQUIRY", "HOTEL_REQUEST", "FARE_DIFFERENCE_REQUEST", "REBOOKING_REQUEST"]`
* **Detected Sentiment**: `Neutral`
* **Extracted Entities**:
  * `customer_name`: "Meher Kaur"
  * `flight_number`: "SK-305"
  * `fare_difference_inr`: `2000.0`
  * `wants_full_night_hotel`: `True`
* **Customer Context**:
  * ID: `CUST-003`, Tier: `Platinum`, Prior Complaints: `1 (Overbooking, resolved with tier upgrade)`
* **Booking Context**:
  * PNR: `WL7742`, Flight: `SK-305`, Route: `Delhi → Hyderabad`, Date: `Wed 23 Sep 2026`
  * Status: `Delayed 6.0 hours` (14:00 $\rightarrow$ 20:00)
* **Policy Rules Evaluated**:
  1. `Section 5.2`: Delays $> 5$ hours qualify for meal voucher, lounge access, and transit hotel covering delayed hours only.
  2. `Section 5.2 Restriction`: Full-night hotel stay is strictly not permitted.
  3. `Section 5.4`: Higher-fare rebooking requires paying fare difference. Agents can waive up to ₹1,500. Requested waiver of ₹2,000 exceeds threshold; supervisor approval required.
  4. `Section 5.5`: Platinum tier provides priority rebooking only, not fee waivers or extra payouts.
* **Decisions Generated**:
  * Delay Assistance: `Eligible: True` (Meal, Lounge, Transit Hotel for Delayed Hours).
  * Full-Night Stay: `Eligible: False` (Restricted to delayed-hours portion).
  * Fare Difference Waiver: `Eligible: False` (Escalation: `True`, Reason: `FARE_DIFFERENCE_EXCEEDS_AGENT_LIMIT_1500`).
* **Simulated Actions Executed**:
  * `MEAL_VOUCHER_ISSUED` (`ID: SIM-VOUCH-XXXXX`).
  * `LOUNGE_ACCESS_ISSUED` (`ID: SIM-LNG-XXXXX`).
  * `HOTEL_REQUESTED_FOR_DELAYED_HOURS` (`ID: SIM-HTL-XXXXX`, Day-room transit accommodation).
  * `ESCALATED_TO_HUMAN` (`Ticket: ESC-TCK-XXXXX`, Supervisor Fare Waiver Queue).
* **Final Grounded Agent Response**:
  > *"Hello Meher, thank you for contacting us regarding your flight.*
  >
  > *Your flight SK-305 (Delhi → Hyderabad) is currently delayed by 6.0 hours, with an updated departure time of 20:00.*
  >
  > *I have issued a complimentary Full Airport Meal Allowance for airport dining.*
  >
  > *I have activated complimentary airport lounge access for you while you wait.*
  >
  > *I have arranged transit day-room hotel accommodation. Per Section 5.2, this accommodation covers only the qualifying delayed-hours portion up to departure; full-night stays are not eligible under standard policy.*
  >
  > *Regarding your request for a higher-fare flight: The fare difference is ₹2,000. Under Service Rules Section 5.4, any fare difference waiver exceeding ₹1,500 requires supervisor approval.*
  >
  > *I have escalated the ₹2,000 fare-difference waiver request to a human supervisor (Ticket ID: ESC-TCK-XXXX) for formal review."*
* **Policy Citations Displayed**:
  * `Service Rules Section 5.2: Delay Compensation Rule`
  * `Service Rules Section 5.4: Fare Difference Rule`
  * `Service Rules Section 5.5: Loyalty Tier Rule`
  * `Service Rules Section 7.0: Prohibited Actions`
