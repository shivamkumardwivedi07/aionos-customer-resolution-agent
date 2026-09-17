import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import CustomerCard from './components/CustomerCard';
import QuickScenarios from './components/QuickScenarios';
import ChatWindow from './components/ChatWindow';
import ResolutionInspector from './components/ResolutionInspector';
import AuditTrailDrawer from './components/AuditTrailDrawer';

const API_BASE = '/api';

export default function App() {
  const [customers, setCustomers] = useState([]);
  const [selectedCustomer, setSelectedCustomer] = useState(null);
  const [scenarios, setScenarios] = useState([]);
  const [activeScenarioId, setActiveScenarioId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [resolution, setResolution] = useState(null);
  const [auditEvents, setAuditEvents] = useState([]);
  const [isAuditOpen, setIsAuditOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);

  // Load initial data
  useEffect(() => {
    fetchInitialData();
  }, []);

  const fetchInitialData = async () => {
    try {
      const [custRes, scenRes, auditRes] = await Promise.all([
        fetch(`${API_BASE}/customers`),
        fetch(`${API_BASE}/scenarios`),
        fetch(`${API_BASE}/audit`)
      ]);

      if (custRes.ok) {
        const custList = await custRes.json();
        setCustomers(custList);
        if (custList.length > 0) {
          setSelectedCustomer(custList[0]);
        }
      }

      if (scenRes.ok) {
        const scenList = await scenRes.json();
        setScenarios(scenList);
      }

      if (auditRes.ok) {
        const auditList = await auditRes.json();
        setAuditEvents(auditList);
      }
    } catch (err) {
      console.error('Failed to load initial data:', err);
    }
  };

  const handleSelectCustomer = (customerData) => {
    setSelectedCustomer(customerData);
    setActiveScenarioId(null);
  };

  const handleSendMessage = async (text, overrideCustomerId = null) => {
    const custId = overrideCustomerId || selectedCustomer?.customer?.customer_id;
    const custName = selectedCustomer?.customer?.name || 'Customer';

    // Append user message immediately
    const userMsg = {
      role: 'user',
      content: text,
      customer_name: custName,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' })
    };

    setMessages((prev) => [...prev, userMsg]);
    setIsLoading(true);

    try {
      const res = await fetch(`${API_BASE}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: text,
          session_id: sessionId,
          customer_id: custId
        })
      });

      if (!res.ok) {
        throw new Error(`Server returned status ${res.status}`);
      }

      const data = await res.json();
      setSessionId(data.session_id);
      setResolution(data);

      // Append agent response
      const agentMsg = {
        role: 'agent',
        content: data.agent_message,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' }),
        actions: data.actions_taken,
        escalated: data.escalated,
        escalation_reason: data.escalation_reason,
        citations: data.policy_citations
      };

      setMessages((prev) => [...prev, agentMsg]);

      // Refresh audit logs
      const auditRes = await fetch(`${API_BASE}/audit`);
      if (auditRes.ok) {
        const freshAudits = await auditRes.json();
        setAuditEvents(freshAudits);
      }
    } catch (err) {
      console.error('Chat error:', err);
      const errMsg = {
        role: 'agent',
        content: `Error processing request: ${err.message}. Please check backend service status.`,
        timestamp: new Date().toLocaleTimeString()
      };
      setMessages((prev) => [...prev, errMsg]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSelectScenario = (sc) => {
    setActiveScenarioId(sc.id);
    const targetCust = customers.find((c) => c.customer.customer_id === sc.customer_id);
    if (targetCust) {
      setSelectedCustomer(targetCust);
    }
    handleSendMessage(sc.prompt, sc.customer_id);
  };

  const handleReset = async () => {
    try {
      await fetch(`${API_BASE}/reset`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ reset_audit: true })
      });
      setMessages([]);
      setResolution(null);
      setAuditEvents([]);
      setActiveScenarioId(null);
      setSessionId(null);
      if (customers.length > 0) {
        setSelectedCustomer(customers[0]);
      }
    } catch (err) {
      console.error('Failed to reset state:', err);
    }
  };

  const handleExportJson = () => {
    window.open(`${API_BASE}/audit/export`, '_blank');
  };

  return (
    <div className="h-screen w-full flex flex-col bg-slate-950 text-slate-100 overflow-hidden font-sans">
      {/* Top Header */}
      <Header
        onReset={handleReset}
        onToggleAudit={() => setIsAuditOpen(!isAuditOpen)}
        isAuditOpen={isAuditOpen}
      />

      {/* Main 3-Pane Body */}
      <main className="flex-1 flex min-h-0 overflow-hidden p-3 gap-3">
        {/* Left Pane: Customer Context & Quick Scenarios */}
        <aside className="w-80 flex flex-col gap-3 min-h-0 overflow-y-auto shrink-0">
          <CustomerCard
            customers={customers}
            selectedCustomer={selectedCustomer}
            onSelectCustomer={handleSelectCustomer}
          />
          <QuickScenarios
            scenarios={scenarios}
            onSelectScenario={handleSelectScenario}
            activeScenarioId={activeScenarioId}
          />
        </aside>

        {/* Center Pane: Interactive Chat & Operations Console */}
        <section className="flex-1 flex flex-col min-w-0 min-h-0 h-full">
          <ChatWindow
            messages={messages}
            onSendMessage={handleSendMessage}
            isLoading={isLoading}
            activeCustomer={selectedCustomer}
            lastResolution={resolution}
          />
        </section>

        {/* Right Pane: Policy Resolution Inspector & Citations */}
        <aside className="w-80 flex flex-col min-h-0 overflow-hidden shrink-0">
          <ResolutionInspector
            resolution={resolution}
          />
        </aside>
      </main>

      {/* Slide-out Audit Trail Drawer */}
      <AuditTrailDrawer
        isOpen={isAuditOpen}
        onClose={() => setIsAuditOpen(false)}
        auditEvents={auditEvents}
        onExportJson={handleExportJson}
      />
    </div>
  );
}
