# Process Flow & Sequence Diagrams

## 1. End-to-End Resolution Process Flow

The following flowchart illustrates the step-by-step processing of each customer interaction through the system.

```mermaid
flowchart TD
    Start([User Submits Message]) --> ResolveContext[Resolve Session & Customer Context]
    ResolveContext --> PrivacyCheck{Cross-Customer PNR Inquiry?}
    
    PrivacyCheck -- Yes --> PrivacyRefusal[Return Privacy Refusal Notice<br><i>Customer Privacy Standard</i>]
    PrivacyRefusal --> RecordAudit
    
    PrivacyCheck -- No --> ParseInput[Intent & Entity Extraction<br><i>Detect Sentiment & Multiple Intents</i>]
    ParseInput --> EvalPolicy[Deterministic Policy Engine]
    
    subgraph Deterministic Rule Evaluation
        EvalPolicy --> CheckCanc{Flight Status?}
        CheckCanc -- Cancelled --> Rule51[Apply Section 5.1 & 5.3<br>Rebook 24h OR Full Refund in 7 Days]
        CheckCanc -- Delayed --> Rule52[Apply Section 5.2<br>Check Delay Threshold]
        
        Rule52 --> ThreshCheck{Delay Hours}
        ThreshCheck -- "< 3h" --> D1[₹500 Meal Voucher]
        ThreshCheck -- "3h to 5h" --> D2[Meal Voucher + Lounge Access<br>NO Hotel]
        ThreshCheck -- "> 5h" --> D3[Meal + Lounge + Hotel<br>Delayed Hours ONLY, NO Full Night]
        
        EvalPolicy --> FareCheck{Fare Diff > ₹1,500?}
        FareCheck -- Yes --> FareEsc[Section 5.4: Require Supervisor Waiver]
        FareCheck -- No --> FareOK[Section 5.4: Within Agent Authority]
        
        EvalPolicy --> TierCheck{Gold / Platinum?}
        TierCheck -- "Extra Compensation / Upgrade Demanded" --> TierEsc[Section 5.5: Deny & Escalate Upgrade]
        TierCheck -- "Standard Request" --> TierOK[Grant Priority Rebooking]
    end
    
    Rule51 --> CheckEscalation
    D1 --> CheckEscalation
    D2 --> CheckEscalation
    D3 --> CheckEscalation
    FareEsc --> CheckEscalation
    FareOK --> CheckEscalation
    TierEsc --> CheckEscalation
    TierOK --> CheckEscalation
    
    subgraph Escalation & Action
        CheckEscalation{Prohibited Trigger Active?<br><i>Legal, Complaint, Payment, Limit</i>}
        CheckEscalation -- Yes --> TriggerEscTicket[Emit ESCALATED_TO_HUMAN Action Ticket]
        CheckEscalation -- No --> ExecActions[Emit Permitted Simulated Action Records]
        TriggerEscTicket --> SynthResponse[Grounded Response Generator]
        ExecActions --> SynthResponse
    end
    
    SynthResponse --> RecordAudit[Append Event to Audit Trail]
    RecordAudit --> End([Render Response, Actions & Citations in UI])
```

---

## 2. Sequence Diagram: Scenario 1 (Priya Nair — Cancellation & Out-of-Policy Upgrade)

```mermaid
sequenceDiagram
    autonumber
    actor Priya as Priya Nair (Gold)
    participant UI as React UI Console
    participant Orch as Orchestrator
    participant Intent as Intent Extractor
    participant Policy as Policy Engine
    participant Esc as Escalation Engine
    participant Action as Action Engine
    participant Audit as Audit Service

    Priya->>UI: "Flight SK-204 cancelled. Want full cash refund & free business class return!"
    UI->>Orch: POST /api/chat { message, customer_id: "CUST-001" }
    Orch->>Intent: extract(message)
    Intent-->>Orch: intents: [REFUND_REQUEST, UPGRADE_REQUEST], sentiment: "Furious"
    
    Orch->>Policy: evaluate_cancellation(SK-204, chosen="REFUND")
    Policy-->>Orch: Eligible: True (Full refund to original payment method in 7 days)
    
    Orch->>Policy: evaluate_return_flight(SK-204)
    Policy-->>Orch: Return leg Goa→Delhi is confirmed Unaffected
    
    Orch->>Policy: evaluate_loyalty("Gold", upgrade_requested=True)
    Policy-->>Orch: Eligible: False (No complimentary cabin upgrade under Sec 5.5)
    
    Orch->>Esc: evaluate(intents, entities, policies)
    Esc-->>Orch: Escalate: True (Triggers: [COMPENSATION_EXCEEDS_POLICY])
    
    Orch->>Action: initiate_refund(Priya, SK-204)
    Action-->>Orch: ActionRecord: REFUND_REQUESTED (Ref: SIM-REF-XXXX)
    
    Orch->>Action: create_escalation_ticket(Priya, SK-204, triggers)
    Action-->>Orch: ActionRecord: ESCALATED_TO_HUMAN (Ticket: ESC-TCK-XXXX)
    
    Orch->>Audit: record_event(audit_record)
    Orch-->>UI: ResolutionResponse (Message, Actions, Decisions, Citations)
    UI-->>Priya: Empathetic response with refund confirmation, return status, and escalation
```

---

## 3. Sequence Diagram: Scenario 2 (Arvind Kulkarni — 4h Delay Boundary Handling)

```mermaid
sequenceDiagram
    autonumber
    actor Arvind as Arvind Kulkarni (Silver)
    participant UI as React UI Console
    participant Orch as Orchestrator
    participant Policy as Policy Engine
    participant Action as Action Engine

    Arvind->>UI: "SK-118 delayed 4h. Missed client meeting. Need hotel room now."
    UI->>Orch: POST /api/chat { message, customer_id: "CUST-002" }
    
    Orch->>Policy: evaluate_delay_compensation(delay=4.0h)
    Note over Policy: Delay > 3h and <= 5h.<br/>Eligible: Meal voucher + Lounge.<br/>Prohibited: Hotel (<5h threshold).
    Policy-->>Orch: PolicyDecision (Meal + Lounge Eligible; Hotel Ineligible)
    
    Orch->>Action: issue_meal_voucher(Arvind, SK-118)
    Action-->>Orch: ActionRecord: MEAL_VOUCHER_ISSUED
    Orch->>Action: issue_lounge_access(Arvind, SK-118)
    Action-->>Orch: ActionRecord: LOUNGE_ACCESS_ISSUED
    
    Note over Orch: No escalation triggered.<br/>Frustration handled with calm empathy.
    Orch-->>UI: Response explaining 4h entitlement and denying hotel under Section 5.2
    UI-->>Arvind: Displays meal voucher code, lounge pass, and hotel explanation
```

---

## 4. Sequence Diagram: Scenario 3 (Meher Kaur — 6h Delay & ₹2,000 Fare Difference)

```mermaid
sequenceDiagram
    autonumber
    actor Meher as Meher Kaur (Platinum)
    participant UI as React UI Console
    participant Orch as Orchestrator
    participant Policy as Policy Engine
    participant Esc as Escalation Engine
    participant Action as Action Engine

    Meher->>UI: "SK-305 delayed 6h. Want full-night hotel & waive ₹2,000 fare diff on new flight."
    UI->>Orch: POST /api/chat { message, customer_id: "CUST-003" }
    
    Orch->>Policy: evaluate_delay_compensation(delay=6.0h)
    Note over Policy: Delay > 5h.<br/>Hotel allowed for DELAYED HOURS ONLY.<br/>Full-night stay strictly prohibited.
    Policy-->>Orch: PolicyDecision (Meal + Lounge + Transit Hotel for Delayed Hours)
    
    Orch->>Policy: evaluate_fare_difference(fare_diff=2000.0)
    Note over Policy: ₹2,000 > ₹1,500 agent threshold.<br/>Requires supervisor approval.
    Policy-->>Orch: PolicyDecision (Eligible: False, Escalation: Required)
    
    Orch->>Esc: evaluate(intents, entities, policies)
    Esc-->>Orch: Escalate: True (Trigger: FARE_DIFF_WAIVER_EXCEEDS_1500)
    
    Orch->>Action: arrange_hotel(Meher, SK-305)
    Action-->>Orch: ActionRecord: HOTEL_REQUESTED_FOR_DELAYED_HOURS
    Orch->>Action: create_escalation_ticket(Meher, SK-305, triggers)
    Action-->>Orch: ActionRecord: ESCALATED_TO_HUMAN
    
    Orch-->>UI: Response with transit hotel confirmation & supervisor waiver escalation
    UI-->>Meher: Explains transit hotel window & formal waiver escalation ticket
```
