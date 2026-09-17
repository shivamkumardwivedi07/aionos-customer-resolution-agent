# 10-Minute Live Demo & Defense Script

**Total Demo Duration:** 10 Minutes (Leaving 5 minutes for Reviewer Q&A in a 15-minute slot)

---

## 🕒 0:00 – 0:45 | The Problem
> **Action:** Share screen showing the application header and customer selector.

"Hello everyone. Today I'm demonstrating our Customer-Facing Resolution Agent for Airline Disruption. 

When flights are cancelled or delayed, passengers are anxious, emotional, and demand immediate resolution. The biggest pitfall in deploying AI agents in this space is hallucination—chatbots promising free business class upgrades, non-existent connecting flights, or unauthorized cash refunds. 

Our goal was to build a production-style agent that absorbs high-emotion customer input, understands compound requests, and delivers grounded, zero-hallucination decisions strictly backed by airline policy."

---

## 🕒 0:45 – 1:30 | Solution Overview
> **Action:** Point out the 3-pane layout on screen: Customer Profile (left), Live Operations Chat (center), Resolution Inspector & Citations (right).

"Here is our system. We chose a 3-pane airline operations console built with React, Vite, and a high-performance Python FastAPI backend.

The architectural north star is simple: **LLM for natural language processing, but deterministic Python rules for business decisions.** 

The agent can parse emotional customer messages, extract multiple intents, check booking state, execute simulated operational actions like refunds or vouchers, and escalate when authority is exceeded—all while writing an immutable audit log."

---

## 🕒 1:30 – 2:30 | System Architecture
> **Action:** Click on the 'Deterministic Policy Engine Active' badge and reference Slide 4.

"Architecturally, we deliberately avoided bloated agent frameworks. Instead, we built an air-gapped pipeline:
1. Intake & Context Manager: Resolves passenger profile and active PNR.
2. Privacy Gateway: Blocks any cross-customer inquiries.
3. Multi-Intent Decomposer: Breaks down compound requests into individual evaluation units.
4. Pure Deterministic Policy Engine: Enforces Sections 5.1 through 5.5 in pure Python without LLM hallucination risk.
5. Simulated Action State Machine: Emits tracked actions with explicit demo disclaimer tags.
6. Grounded Response Synthesizer: Crafts concise, empathetic responses citing exact policy clauses."

---

## 🕒 2:30 – 4:00 | Scenario 1 — Priya Nair (Cancelled Flight)
> **Action:** Click the button **'Scenario 1: Priya Nair — Cancelled Flight (Gold)'**.

"Let's test Scenario 1. Priya Nair is a Gold member whose flight SK-204 from Delhi to Goa was cancelled. She is furious, demands an immediate cash refund, and asks for a free business-class upgrade on her return flight.

Notice the agent's behavior:
1. **Empathy**: It acknowledges her frustration calmly without defensiveness.
2. **Refund Policy**: It recognizes the airline-caused cancellation and initiates a full refund. But notice: it explicitly states that per Section 5.3, refunds must go to the original payment method within 7 business days—it does NOT invent a cash payout.
3. **Return Flight Check**: It explicitly verifies that her return flight from Goa to Delhi on Sept 25 is unaffected.
4. **Out-of-Policy Escalation**: It explains that Gold tier gives priority rebooking but does not grant complimentary cabin upgrades under Section 5.5. It immediately logs an escalation ticket for supervisory review.
5. **Inspector View**: On the right, you can see Section 5.1, 5.3, and 5.5 evaluated with exact citations."

---

## 🕒 4:00 – 5:15 | Scenario 2 — Arvind Kulkarni (4-Hour Delay)
> **Action:** Click the button **'Scenario 2: Arvind Kulkarni — 4h Delay (Silver)'**.

"Now let's switch to Arvind Kulkarni. He is a Silver member on flight SK-118, which is delayed 4 hours. He is frustrated because he missed a client meeting, and demands hotel accommodation.

Watch how the deterministic policy engine handles this exact boundary:
1. Under Section 5.2, delays over 3 hours qualify for a meal voucher and lounge access. The agent issues both.
2. But what about the hotel? The policy strictly requires a delay of **more than 5 hours** for hotel assistance. 
3. The agent does NOT grant a hotel room. It politely and clearly explains the 5-hour threshold.
4. It does not invent compensation for his missed meeting, and notice: it does NOT trigger an unnecessary escalation just because Arvind is frustrated. Escalation is reserved strictly for prohibited triggers."

---

## 🕒 5:15 – 6:45 | Scenario 3 — Meher Kaur (6-Hour Delay & ₹2,000 Fare Difference)
> **Action:** Click the button **'Scenario 3: Meher Kaur — 6h Delay & Higher Fare (Platinum)'**.

"Now let's test our most complex scenario: Meher Kaur, a Platinum member on flight SK-305, delayed 6 hours. She demands a full night's hotel stay and wants to rebook onto a higher-fare flight with a ₹2,000 fare difference waived.

Observe the multi-boundary evaluation:
1. **6-Hour Delay**: Because 6 hours > 5 hours, she qualifies for a hotel room. But Section 5.2 explicitly restricts hotel accommodation to the **delayed-hours window only**—NOT a full night's stay. The agent issues transit accommodation and explicitly declines the full-night stay.
2. **Fare Difference Boundary**: Section 5.4 establishes that agents can waive fare differences up to ₹1,500. Meher's requested waiver is ₹2,000. 
3. Because ₹2,000 > ₹1,500, automated waiver is prohibited. The agent informs Meher of the supervisor requirement and immediately logs an escalation ticket.
4. Notice the Authority Gauge in the right-hand panel: it visibly flags that the request exceeded the agent's ₹1,500 authority limit."

---

## 🕒 6:45 – 7:30 | Audit Trail & Policy Traceability
> **Action:** Click the **'Audit Trail'** button in the header to open the slide-out drawer.

"Enterprise compliance requires complete replayability. Clicking 'Audit Trail' opens our real-time audit ledger. 

For every turn, we record:
- Timestamp and customer PNR
- The exact customer prompt
- Parsed intents and sentiment
- Evaluated policy rules and allowed actions
- Simulated action IDs
- Escalation reasons and authoritative citations

Reviewers or compliance officers can click 'Export JSON' to download the entire structured audit trail for offline verification."

---

## 🕒 7:30 – 8:30 | Adversarial Robustness
> **Action:** Click the adversarial test buttons: 'Legal Threat', 'Privacy', and 'Cash/UPI'.

"Let's look at how the agent defends against adversarial edge cases:
1. **Legal Threat**: When a customer says 'I will sue in consumer court', the Escalation Engine intercepts it under Section 7.0 and creates an expedited priority grievance ticket.
2. **Data Privacy**: If Priya asks for Arvind's booking TR1190B, the identity gateway immediately refuses to discuss third-party passenger data.
3. **Cash/Payment Hijack**: If someone demands a refund to a friend's UPI account, Section 5.3 blocks it and enforces the original payment method."

---

## 🕒 8:30 – 9:30 | Automated Testing Suite
> **Action:** Show the terminal output of `pytest backend/tests -v` (27 passing tests).

"Quality assurance is mathematically verified. We have an automated test suite containing 27 `pytest` test cases covering:
- Unit tests for every policy clause (5.1 through 5.5).
- Boundary tests (4h vs 6h delay, ₹1,500 waiver limit).
- Full end-to-end multi-turn journeys for Priya, Arvind, and Meher.
- Adversarial attacks and FastAPI endpoint contracts.
All 27 tests pass in under 0.5 seconds."

---

## 🕒 9:30 – 10:00 | Conclusion & Q&A
"To conclude: this agent demonstrates that high-stakes enterprise AI doesn't need to be an unpredictable black box. By decoupling natural language understanding from deterministic rule execution, we achieve empathy, zero hallucinations, complete auditability, and rock-solid policy compliance.

Thank you. I am ready for your questions."
