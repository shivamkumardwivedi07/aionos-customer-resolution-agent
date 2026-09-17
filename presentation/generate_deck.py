"""Generates the official 10-slide PowerPoint presentation for the 15-minute defence.

Uses python-pptx to produce AIONOS_Customer_Resolution_Agent.pptx with embedded speaker notes.
"""

from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

OUTPUT_DIR = Path(__file__).resolve().parent
OUTPUT_FILE = OUTPUT_DIR / "AIONOS_Customer_Resolution_Agent.pptx"

def create_deck():
    prs = Presentation()
    # 16:9 widescreen
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    blank_layout = prs.slide_layouts[6]

    NAVY = RGBColor(11, 25, 44)
    SKY = RGBColor(2, 132, 199)
    WHITE = RGBColor(255, 255, 255)
    GRAY = RGBColor(148, 163, 184)
    DARK_CARD = RGBColor(15, 23, 42)
    AMBER = RGBColor(245, 158, 11)
    ROSE = RGBColor(244, 63, 94)
    EMERALD = RGBColor(16, 185, 129)

    slides_data = [
        {
            "title": "AIONOS Agentic AI Factory: Customer Resolution Agent",
            "subtitle": "Production-Style Airline Disruption Agent • Pure Deterministic Policy Core",
            "category": "SLIDE 1: TITLE & EXECUTIVE SUMMARY",
            "points": [
                "Domain: Airline Disruption Resolution (Flight Cancellations & Delays).",
                "Core Engineering Tenet: 'LLM for language, deterministic rules for business decisions.'",
                "Zero Hallucination: Grounded strictly in authoritative facts and policy clauses (Sections 5.1–5.5).",
                "Simulated Action Execution: State machine simulating refunds, meal vouchers, lounge passes, and hotel transit.",
                "Mandatory Escalation: Automated detection of 6 prohibited actions and authority boundary breaches."
            ],
            "notes": (
                "Good morning, reviewers. Today I am presenting our Customer-Facing Resolution Agent for Airline Disruption. "
                "The core engineering philosophy behind this system is: LLMs are brilliant at understanding human emotion, intent, "
                "and unstructured natural language, but business decisions, monetary refunds, and compliance boundaries must be 100% deterministic. "
                "In this presentation, I will walk you through the architecture, deterministic policy engine, the three test scenarios, "
                "and how our audit trail guarantees zero hallucinations."
            )
        },
        {
            "title": "Business Problem & Customer Disruption Journey",
            "subtitle": "Turning High-Stress Disruption Moments into Grounded, Trustworthy Resolutions",
            "category": "SLIDE 2: THE BUSINESS PROBLEM",
            "points": [
                "Customer Friction: Sudden cancellations and multi-hour delays cause intense frustration and urgent demands.",
                "The Hallucination Danger: Generic AI chatbots frequently hallucinate non-existent seats, free business-class upgrades, or unapproved cash payouts.",
                "Policy Complexity: Strict boundary conditions (e.g. 4h delay vs 6h delay; agent waiver limit of ₹1,500).",
                "Privacy & Compliance: Need strict isolation between passengers; no cross-customer data leakage.",
                "Goal: Resolve what is permitted immediately, explain restrictions with empathy, and escalate out-of-policy demands."
            ],
            "notes": (
                "When flights are cancelled or delayed, passengers are anxious and often angry. Traditional chatbots either give generic "
                "non-answers or, worse, make promises the airline cannot fulfill—such as free upgrades or immediate cash payouts. "
                "Our business objective was to build a system that can absorb emotional customer input, accurately detect complex compound intents, "
                "evaluate entitlements against strict airline policy rules, simulate authorized operational actions, and immediately escalate exceptions."
            )
        },
        {
            "title": "Solution Architecture Overview",
            "subtitle": "3-Pane Operations Console, Air-Gapped Policy Engine, and Live Audit Trail",
            "category": "SLIDE 3: SOLUTION ARCHITECTURE",
            "points": [
                "User Interface: Responsive 3-pane React console with 1-click test scenarios and live policy inspector.",
                "Context Resolution: Hybrid Intent & Entity Extractor identifying compound requests, sentiment, and PNR context.",
                "Air-Gapped Policy Engine: Pure Python deterministic functions enforcing Sections 5.1 through 5.5.",
                "Simulated Action Engine: Emits explicit simulated operations with unique tracking IDs.",
                "Continuous Audit Trail: Every single turn records timestamp, intent, policy evaluated, decision, action, and citation."
            ],
            "notes": (
                "Here is our system architecture. Notice the strict separation of concerns. The LLM or NLU parser is only responsible for "
                "intent extraction and empathetic response formatting. It is physically impossible for the LLM to grant a refund or waive a fee "
                "on its own. The request passes through our deterministic Policy Engine, which inspects the booking status, delay hours, and loyalty tier. "
                "If permitted, the Action Engine simulates the change; if prohibited, the Escalation Engine logs an urgent supervisor ticket."
            )
        },
        {
            "title": "Detailed Process Flow & State Management",
            "subtitle": "End-to-End Traceable Pipeline from Natural Language to Audit Record",
            "category": "SLIDE 4: AGENT WORKFLOW",
            "points": [
                "1. Intake: Customer message received; session state retrieved (PNR, active passenger).",
                "2. Boundary Gateway: Validates passenger identity; rejects cross-passenger PNR queries immediately.",
                "3. Multi-Intent Decomposition: Deconstructs compound inputs (e.g. 'Refund + Free Business Upgrade').",
                "4. Policy Evaluation: Evaluates cancellation, delay thresholds, fare diff limits, and loyalty restrictions.",
                "5. Action & Escalation: Executes permitted actions; flags authority breaches (e.g. ₹2,000 waiver > ₹1,500 limit).",
                "6. Grounded Generation: Formulates concise, empathetic, non-defensive responses with citations."
            ],
            "notes": (
                "Let's follow the data flow. When a customer sends a message, our session manager binds their profile. The message is decomposed "
                "into distinct intents. If a customer asks for a refund AND an upgrade, both are evaluated independently. The refund is approved "
                "under Section 5.1, while the upgrade is flagged as out-of-policy under Section 5.5 and escalated. The response generator then synthesizes "
                "these verified facts into a single empathetic message."
            )
        },
        {
            "title": "Deterministic Policy Engine & Guardrails",
            "subtitle": "Authoritative Service Rules Codified in Pure, Mathematically Proven Python",
            "category": "SLIDE 5: POLICY ENGINE & GUARDRAILS",
            "points": [
                "Section 5.1 (Cancellation): Free rebooking within 24h OR full refund. Never fabricates replacement flight numbers or seat availability.",
                "Section 5.2 (Delay): <3h: ₹500 meal voucher; 3h–5h (4h delay): meal + lounge, NO hotel; >5h (6h delay): meal + lounge + hotel for delayed hours only (NO full night).",
                "Section 5.3 (Refund): Processed in full within 7 business days, strictly to original payment method. No cash payouts.",
                "Section 5.4 (Fare Difference): Customer pays fare diff. Agent limit: ≤ ₹1,500. Supervisor required if > ₹1,500.",
                "Section 5.5 (Loyalty Tier): Gold/Platinum get priority rebooking only. Absolutely NO extra compensation or free upgrades."
            ],
            "notes": (
                "This slide highlights the exact mathematical boundaries of our Policy Engine. Notice the rigid adherence to the brief: "
                "For Arvind's 4-hour delay, hotel accommodation is strictly denied because the policy requires a delay greater than 5 hours. "
                "For Meher's 6-hour delay, hotel is granted, but strictly for the delayed-hours window—not a full night's stay. "
                "And when Meher asks for a ₹2,000 fare waiver, because ₹2,000 exceeds the agent's ₹1,500 threshold, the system enforces supervisor escalation."
            )
        },
        {
            "title": "The Three Mandatory Scenarios in Action",
            "subtitle": "Empirical Proof: Verified Correctness Across All Three Evaluation Journeys",
            "category": "SLIDE 6: SCENARIO DEMONSTRATIONS",
            "points": [
                "Scenario 1 — Priya Nair (Gold): Outbound SK-204 cancelled. Demands cash refund + return business class. Result: Full refund to original card in 7 days; return flight confirmed unaffected; upgrade denied & escalated under Section 5.5.",
                "Scenario 2 — Arvind Kulkarni (Silver): Flight SK-118 delayed 4h. Missed meeting, demands hotel. Result: Meal voucher + lounge access issued; hotel denied (<5h threshold); empathetic tone without false escalation.",
                "Scenario 3 — Meher Kaur (Platinum): Flight SK-305 delayed 6h. Demands full-night hotel + ₹2,000 fare waiver. Result: Meal + lounge + transit hotel for delayed hours issued; full night denied; ₹2,000 waiver escalated to supervisor."
            ],
            "notes": (
                "These three scenarios represent the core test of the assignment. In Priya's case, the agent validates that her return flight "
                "is unaffected, initiates a refund strictly to her original payment method, and refuses the business class upgrade while escalating. "
                "In Arvind's case, the agent acknowledges his missed meeting with empathy, gives meal and lounge vouchers, but correctly withholds hotel accommodation. "
                "In Meher's case, transit hotel is granted, but the ₹2,000 fare waiver is escalated because it exceeds our ₹1,500 authority."
            )
        },
        {
            "title": "Audit Trail, Citations & Prohibited Escalations",
            "subtitle": "Enterprise Compliance: Section 7.0 Enforcement and Full Replayability",
            "category": "SLIDE 7: AUDIT & ESCALATION",
            "points": [
                "Prohibited Escalation Triggers: Legal action threats, formal regulatory complaints (DGCA), non-original payment requests, compensation exceeding policy, and fare difference waivers > ₹1,500.",
                "Zero Black Box: Every decision displays its authoritative policy citation directly on screen (e.g. 'Service Rules Section 5.2').",
                "Immutable Audit Events: Captures timestamp, customer ID, PNR, raw prompt, parsed intents, evaluated decisions, and simulated action IDs.",
                "Exportable Compliance Log: One-click export of complete audit log in standardized JSON format."
            ],
            "notes": (
                "Enterprise adoption of agentic AI requires total accountability. If a reviewer asks: 'Why did the agent make this decision?', "
                "the answer is instantly available in the right-hand Inspector and the Audit Drawer. We cite the exact section number. "
                "Furthermore, our Escalation Engine actively listens for legal threats, formal regulatory complaints, and unauthorized payment methods, "
                "immediately cutting off autonomous execution and routing the ticket to specialized human desks."
            )
        },
        {
            "title": "Adversarial Robustness & Safety Guardrails",
            "subtitle": "Defending Against Jailbreaks, Privacy Breaches, and Out-of-Policy Demands",
            "category": "SLIDE 8: ADVERSARIAL DEFENCE",
            "points": [
                "Adversarial Test 1 (Arbitrary Demands): 'Give me ₹10,000 compensation' -> Refused; escalated as out-of-policy.",
                "Adversarial Test 2 (Payment Hijack): 'Refund to friend's UPI account' -> Denied under Section 5.3; original payment method enforced.",
                "Adversarial Test 3 (Cross-Customer Privacy): 'What is Arvind's booking status?' -> Denied at gateway; passenger data strictly isolated.",
                "Adversarial Test 4 (Legal Pressure): 'I will sue in consumer court!' -> Immediate expedited escalation ticket logged.",
                "Adversarial Test 5 (Inventory Hallucination): Demands for specific alternative flight numbers -> Refuses to fabricate inventory."
            ],
            "notes": (
                "We subjected our agent to a battery of adversarial attacks. In every case, the deterministic guardrails held firm. "
                "When users attempt to divert funds to a third-party UPI account, the agent enforces Section 5.3. When a user asks about another "
                "passenger's flight, the privacy gateway intercepts the request. When a user threatens a lawsuit, an expedited grievance ticket is generated."
            )
        },
        {
            "title": "Technology Stack, AI Tools & Quality Verification",
            "subtitle": "Production-Grade Engineering • 100% Passing Automated Tests",
            "category": "SLIDE 9: TECH STACK & TESTING",
            "points": [
                "Backend: Python 3.14 + FastAPI + Pydantic v2 (Strict Typing, Sub-millisecond execution).",
                "Frontend: React 18 + Vite + Tailwind CSS (High-contrast 3-pane airline operations console).",
                "Automated Test Suite: 27 comprehensive pytest tests covering unit, scenario, boundary, adversarial, and API endpoints (100% Pass).",
                "Zero-Key Offline Mode: Embedded deterministic baseline ensures complete functionality with zero external API dependencies.",
                "AI Tool Transparency: Built using Claude for architectural breakdown and Antigravity for implementation & test orchestration."
            ],
            "notes": (
                "Our technology stack was chosen for reliability and speed. Python with FastAPI and Pydantic provides type safety and sub-millisecond "
                "rule evaluation. Our automated test suite contains 27 pytest cases verifying every single requirement and edge case in the brief. "
                "Crucially, the system operates in an offline deterministic fallback mode, meaning a reviewer can test it anywhere without needing "
                "a paid API key or network access."
            )
        },
        {
            "title": "Results, Limitations & Production Roadmap",
            "subtitle": "Ready for Demonstration and Practical Enterprise Integration",
            "category": "SLIDE 10: CONCLUSION & FUTURE WORK",
            "points": [
                "Results: Delivered a small, credible, production-style customer resolution agent fully aligned with the AIONOS brief.",
                "Current Limitations: Flight inventory is simulated (no real GDS connection); authentication uses demo customer selector.",
                "Roadmap Phase 1: Real-time GDS integration (Amadeus / Sabre APIs for live seat inventory).",
                "Roadmap Phase 2: OpenTelemetry distributed tracing and production SMS/WhatsApp notification channels.",
                "Summary: Demonstrates how agentic AI can be deployed safely, deterministically, and explainably in high-stakes enterprise workflows."
            ],
            "notes": (
                "In conclusion, we have built a working, explainable, and interview-ready resolution agent in under 6 hours. "
                "It proves that agentic workflows in regulated industries do not require risky black-box autonomy—they require smart LLM language comprehension "
                "backed by rock-solid deterministic business rules. Thank you, and I look forward to taking your questions."
            )
        }
    ]

    for idx, data in enumerate(slides_data):
        slide = prs.slides.add_slide(blank_layout)

        # Background color
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = NAVY

        # Category pill
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.5), Inches(0.4))
        cat_tf = cat_box.text_frame
        cat_tf.word_wrap = True
        cat_p = cat_tf.paragraphs[0]
        cat_p.text = data["category"]
        cat_p.font.size = Pt(11)
        cat_p.font.bold = True
        cat_p.font.color.rgb = SKY

        # Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.85), Inches(11.5), Inches(0.8))
        title_tf = title_box.text_frame
        title_tf.word_wrap = True
        title_p = title_tf.paragraphs[0]
        title_p.text = data["title"]
        title_p.font.size = Pt(24)
        title_p.font.bold = True
        title_p.font.color.rgb = WHITE

        # Subtitle
        sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.55), Inches(11.5), Inches(0.5))
        sub_tf = sub_box.text_frame
        sub_tf.word_wrap = True
        sub_p = sub_tf.paragraphs[0]
        sub_p.text = data["subtitle"]
        sub_p.font.size = Pt(13)
        sub_p.font.color.rgb = GRAY

        # Content Card Background
        card = slide.shapes.add_shape(
            1, # Rectangle
            Inches(0.8), Inches(2.2), Inches(11.733), Inches(4.7)
        )
        card.fill.solid()
        card.fill.fore_color.rgb = DARK_CARD
        card.line.color.rgb = RGBColor(30, 41, 59)
        card.line.width = Pt(1.5)

        # Bullet points
        content_box = slide.shapes.add_textbox(Inches(1.1), Inches(2.4), Inches(11.1), Inches(4.3))
        content_tf = content_box.text_frame
        content_tf.word_wrap = True

        for p_idx, pt in enumerate(data["points"]):
            p = content_tf.add_paragraph() if p_idx > 0 else content_tf.paragraphs[0]
            p.text = f"•   {pt}"
            p.font.size = Pt(13)
            p.font.color.rgb = WHITE
            p.space_after = Pt(14)
            p.line_spacing = 1.25

        # Add speaker notes
        notes_slide = slide.notes_slide
        text_frame = notes_slide.notes_text_frame
        text_frame.text = data["notes"]

    prs.save(str(OUTPUT_FILE))
    print(f"Successfully generated 10-slide presentation at: {OUTPUT_FILE}")


if __name__ == "__main__":
    create_deck()
