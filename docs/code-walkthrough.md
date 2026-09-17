# Code Walkthrough & Engineering Guide

This guide explains the key modules of the codebase in plain English, focusing on what you may be asked about during your technical interview.

---

## 1. `backend/app/agent/policy_engine.py` (The Heart of the System)

* **Purpose**: Evaluates customer disruption eligibility using pure, deterministic Python functions. It is completely decoupled from the LLM to eliminate hallucinations.
* **Key Functions**:
  * `evaluate_cancellation(booking, chosen_action)`:
    * *Inputs*: `Booking` model, optional `chosen_action` (`"REFUND"` or `"REBOOK"`).
    * *Outputs*: `PolicyDecision` specifying whether a full refund or 24h rebooking is permitted, along with restrictions (`ORIGINAL_PAYMENT_METHOD_ONLY`, `7_BUSINESS_DAYS`).
    * *Why it matters*: Guarantees that refunds cannot be diverted to cash or unapproved accounts, and ensures the agent never invents fake replacement flights.
  * `evaluate_delay_compensation(booking)`:
    * *Inputs*: `Booking` model with `delay_hours`.
    * *Outputs*: `PolicyDecision` with exact entitlements:
      * $<3$h: ₹500 meal voucher.
      * $3$h to $5$h (Arvind 4h): Meal voucher + Lounge pass (`NO_HOTEL_ACCOMMODATION`).
      * $>5$h (Meher 6h): Meal voucher + Lounge pass + Transit day-room hotel (`NO_FULL_NIGHT_STAY`).
    * *Interview talking point*: Point out that boundary conditions (4 hours vs 6 hours) are hardcoded here and unit tested, preventing the model from giving Arvind an unauthorized hotel room.
  * `evaluate_fare_difference(fare_diff_inr)`:
    * *Inputs*: Float amount in INR.
    * *Outputs*: `PolicyDecision` with `escalation_required = True` if the amount exceeds `AGENT_WAIVER_LIMIT_INR` (₹1,500).
    * *Why it matters*: Defends the boundary in Meher Kaur's scenario (₹2,000 $> ₹1,500$).
  * `evaluate_loyalty(tier, request_upgrade_or_extra)`:
    * *Inputs*: Customer loyalty tier (`Gold`, `Platinum`, `Silver`), boolean flag.
    * *Outputs*: Grants priority rebooking but enforces Section 5.5: strictly no complimentary cabin upgrades or extra monetary compensation.

---

## 2. `backend/app/agent/escalation.py` (The Safety Governor)

* **Purpose**: Enforces Section 7.0 Prohibited Actions and mandatory escalation rules.
* **Inputs**: Customer message, detected intents, extracted entities, and policy decisions.
* **Outputs**: `EscalationDecision` with boolean `escalate`, trigger codes, and recommended routing action.
* **Key Logic**:
  * Uses regex pattern matching and semantic trigger checks to identify:
    1. Legal action threats (`LEGAL_ACTION_THREAT`).
    2. Formal regulatory complaints (`FORMAL_COMPLAINT_THREAT`).
    3. Requests for alternate payment methods or cash payouts (`DIFFERENT_PAYMENT_METHOD_REQUEST`).
    4. Fare difference waiver requests exceeding ₹1,500 (`FARE_DIFF_WAIVER_EXCEEDS_1500`).
    5. Demands for compensation beyond policy (`COMPENSATION_EXCEEDS_POLICY`).
* **Interview talking point**: If asked *"How do you handle a customer who says they'll sue in consumer court?"*, explain how `EscalationEngine` intercepts this before any standard reply and tags the ticket with `HIGH` priority for the Executive Grievance Desk.

---

## 3. `backend/app/agent/action_engine.py` (Simulated Operations)

* **Purpose**: Simulates the execution of permitted operational tools and produces immutable action records.
* **Key Functions**:
  * `initiate_refund(customer, booking)` $\rightarrow$ Emits `REFUND_REQUESTED` with SLA of 7 business days and refund method `ORIGINAL_PAYMENT_METHOD_ONLY`.
  * `issue_meal_voucher(customer, booking)` $\rightarrow$ Emits `MEAL_VOUCHER_ISSUED` with a unique voucher code and valid airport.
  * `issue_lounge_access(customer, booking)` $\rightarrow$ Emits `LOUNGE_ACCESS_ISSUED` with lounge pass code.
  * `arrange_hotel(customer, booking)` $\rightarrow$ Emits `HOTEL_REQUESTED_FOR_DELAYED_HOURS` with explicit restriction: *Transit room only; full night's stay is not eligible*.
  * `request_rebooking(customer, booking)` $\rightarrow$ Emits `REBOOKING_REQUESTED` noting priority standby for Gold/Platinum and ground operations assignment.
  * `create_escalation_ticket(customer, booking, triggers, reason)` $\rightarrow$ Emits `ESCALATED_TO_HUMAN` with ticket reference `ESC-TCK-XXXXXX`.
* **Interview talking point**: Emphasize that every action is stamped with `is_simulated = True` and a clear disclaimer to maintain operational transparency.

---

## 4. `backend/app/agent/orchestrator.py` (Pipeline Coordinator)

* **Purpose**: Glues together session retrieval, intent extraction, privacy checks, policy evaluation, action execution, response synthesis, and audit logging.
* **Execution Flow**:
  1. Retrieves or creates session state via `SessionManager`.
  2. Runs `IntentExtractor.extract(user_message)` to parse intents, entities, and customer tone (`Furious`, `Frustrated`, `Neutral`).
  3. Validates customer identity: checks if the customer is querying another passenger's PNR. If a mismatch is detected, triggers a privacy refusal.
  4. Runs appropriate deterministic policy evaluators based on booking disruption type (cancellation vs delay).
  5. Evaluates escalation triggers.
  6. Executes simulated actions for permitted entitlements.
  7. Invokes `ResponseGenerator.generate()` to compose a policy-grounded, empathetic response.
  8. Commits a complete `AuditEvent` to `AuditService`.
  9. Returns a structured `ResolutionResponse` to the UI.

---

## 5. `backend/app/agent/session.py` (Multi-Turn State Store)

* **Purpose**: Enables natural multi-turn conversations without forcing passengers to repeat known information.
* **State Tracked**:
  * `customer_id`, `pnr`, `flight_number`
  * `pending_choice` (e.g. `AWAITING_CANCELLATION_SELECTION`)
  * `executed_actions` (prevents issuing duplicate vouchers or refunds in the same session)
  * `escalated` flag and `escalation_ticket_id`
  * Conversation history turns

---

## 6. `backend/app/services/audit_service.py` (Compliance & Traceability)

* **Purpose**: In-memory immutable ledger of every customer interaction.
* **Capabilities**:
  * Appends structured `AuditEvent` objects with millisecond timestamps.
  * Filters audit history by session ID or PNR.
  * Generates formatted JSON dumps for regulatory export via `GET /api/audit/export`.
