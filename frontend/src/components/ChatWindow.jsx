import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, AlertTriangle, CheckCircle2, ShieldAlert, Zap, Clock, Sparkles, HelpCircle } from 'lucide-react';

export default function ChatWindow({
  messages,
  onSendMessage,
  isLoading,
  activeCustomer,
  lastResolution
}) {
  const [inputText, setInputText] = useState('');
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!inputText.trim() || isLoading) return;
    onSendMessage(inputText.trim());
    setInputText('');
  };

  const handlePromptClick = (promptText) => {
    if (isLoading) return;
    onSendMessage(promptText);
  };

  const getSentimentBadge = (sentiment) => {
    switch (sentiment?.toLowerCase()) {
      case 'furious':
        return 'bg-rose-500/20 text-rose-300 border-rose-500/30';
      case 'frustrated':
        return 'bg-amber-500/20 text-amber-300 border-amber-500/30';
      default:
        return 'bg-slate-700/50 text-slate-300 border-slate-600';
    }
  };

  // Dynamic suggested prompts based on the currently selected customer & flight situation
  const getSuggestedQuestions = () => {
    const custId = activeCustomer?.customer?.customer_id;
    if (custId === 'CUST-001') {
      // Priya Nair (Cancelled flight)
      return [
        "I want a full refund to my original payment method.",
        "What are my free rebooking options within 24 hours?",
        "Is my return flight from Goa to Delhi affected?",
        "Can I get a complimentary business-class upgrade?"
      ];
    } else if (custId === 'CUST-002') {
      // Arvind Kulkarni (4h delay)
      return [
        "Am I entitled to a meal voucher for my 4-hour delay?",
        "Can I access the airport lounge while I wait?",
        "Can you arrange a hotel room for my 4-hour delay?",
        "Can the airline compensate me for my missed meeting?"
      ];
    } else if (custId === 'CUST-003') {
      // Meher Kaur (6h delay)
      return [
        "Am I eligible for a hotel room for my 6-hour delay?",
        "Can I get a full night's hotel stay instead of transit hours?",
        "Can you waive the ₹2,000 fare difference for a higher flight?",
        "What benefits do I get as a Platinum tier member?"
      ];
    }
    return [
      "What compensation am I entitled to?",
      "Can I get a full refund?",
      "Can I get free rebooking on the next flight?",
      "Can you provide a meal voucher?"
    ];
  };

  const suggestedQuestions = getSuggestedQuestions();

  return (
    <div className="flex-1 flex flex-col h-full min-h-0 bg-slate-900/50 rounded-xl border border-slate-800 overflow-hidden shadow-xl">
      {/* Chat Messages Stream */}
      <div className="flex-1 min-h-0 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-center p-6 text-slate-400">
            <div className="w-14 h-14 rounded-2xl bg-sky-500/10 border border-sky-500/20 flex items-center justify-center text-sky-400 mb-3 shadow-lg shadow-sky-500/10">
              <Bot className="w-7 h-7" />
            </div>
            <h3 className="text-sm font-bold text-slate-100">
              Disruption Resolution Assistant Ready
            </h3>
            <p className="text-xs text-slate-400 max-w-md mt-1 mb-4">
              Ask any question below, click a suggested inquiry chip, or select a scenario from the sidebar.
            </p>

            <div className="max-w-md w-full bg-slate-950/70 border border-slate-800/80 rounded-xl p-3.5 text-left space-y-2">
              <span className="text-[11px] font-semibold text-slate-300 flex items-center gap-1.5">
                <HelpCircle className="w-3.5 h-3.5 text-sky-400" />
                Suggested Questions to Ask Now:
              </span>
              <div className="space-y-1.5">
                {suggestedQuestions.map((q, idx) => (
                  <button
                    key={idx}
                    onClick={() => handlePromptClick(q)}
                    disabled={isLoading}
                    className="w-full text-left text-xs bg-slate-900 hover:bg-sky-950/70 text-slate-300 hover:text-sky-300 border border-slate-800 hover:border-sky-500/40 rounded-lg px-3 py-2 transition-all flex items-center justify-between group"
                  >
                    <span>"{q}"</span>
                    <span className="text-[10px] text-sky-400 opacity-0 group-hover:opacity-100 transition-opacity">
                      Ask →
                    </span>
                  </button>
                ))}
              </div>
            </div>
          </div>
        ) : (
          messages.map((msg, index) => {
            const isUser = msg.role === 'user';
            return (
              <div
                key={index}
                className={`flex items-start gap-3 ${isUser ? 'flex-row-reverse' : 'flex-row'}`}
              >
                {/* Avatar */}
                <div
                  className={`w-8 h-8 rounded-lg flex items-center justify-center shrink-0 shadow-sm ${
                    isUser
                      ? 'bg-amber-600 text-white'
                      : 'bg-sky-600 text-white'
                  }`}
                >
                  {isUser ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
                </div>

                {/* Message Bubble Container */}
                <div className={`max-w-[85%] space-y-2 ${isUser ? 'items-end' : 'items-start'}`}>
                  <div className="flex items-center gap-2 px-1">
                    <span className="text-[11px] font-semibold text-slate-400">
                      {isUser ? (msg.customer_name || 'Customer') : 'Resolution Agent'}
                    </span>
                    <span className="text-[10px] text-slate-400 font-mono flex items-center gap-0.5">
                      <Clock className="w-3 h-3" />
                      {msg.timestamp || 'Just now'}
                    </span>
                    {isUser && msg.sentiment && (
                      <span className={`text-[10px] font-semibold px-1.5 py-0.2 rounded-full border ${getSentimentBadge(msg.sentiment)}`}>
                        Tone: {msg.sentiment}
                      </span>
                    )}
                  </div>

                  {/* Bubble Content */}
                  <div
                    className={`p-3.5 rounded-2xl text-xs leading-relaxed shadow-md ${
                      isUser
                        ? 'bg-slate-800 text-slate-100 border border-slate-700/80 rounded-tr-none'
                        : 'bg-slate-950 text-slate-100 border border-slate-800 rounded-tl-none'
                    }`}
                  >
                    <div className="whitespace-pre-line">{msg.content}</div>
                  </div>

                  {/* Embedded Action Execution Cards (Agent Only) */}
                  {!isUser && msg.actions && msg.actions.length > 0 && (
                    <div className="space-y-1.5 pt-1">
                      {msg.actions.map((act) => (
                        <div
                          key={act.action_id}
                          className="bg-sky-950/40 border border-sky-500/30 rounded-lg p-2.5 text-xs text-sky-200 shadow-sm"
                        >
                          <div className="flex items-center justify-between">
                            <span className="font-semibold flex items-center gap-1.5 text-sky-300">
                              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                              {act.action_type.replace(/_/g, ' ')}
                            </span>
                            <span className="font-mono text-[10px] bg-sky-900/60 px-1.5 py-0.5 rounded text-sky-300">
                              {act.action_id}
                            </span>
                          </div>
                          <p className="text-[11px] text-slate-300 mt-1">{act.reason}</p>
                          <div className="mt-1.5 text-[10px] text-sky-400/80 font-mono">
                            {act.disclaimer}
                          </div>
                        </div>
                      ))}
                    </div>
                  )}

                  {/* Embedded Escalation Notice (Agent Only) */}
                  {!isUser && msg.escalated && (
                    <div className="bg-rose-950/40 border border-rose-500/40 rounded-lg p-2.5 text-xs text-rose-200 shadow-sm">
                      <div className="flex items-center gap-1.5 font-bold text-rose-300">
                        <ShieldAlert className="w-4 h-4 text-rose-400" />
                        <span>MANDATORY SUPERVISOR ESCALATION TRIGGERED</span>
                      </div>
                      <p className="text-[11px] text-rose-200 mt-1">
                        Reason: {msg.escalation_reason || 'Prohibited action or out-of-policy request.'}
                      </p>
                      <span className="inline-block mt-1 text-[10px] font-mono bg-rose-900/60 px-1.5 py-0.5 rounded text-rose-300">
                        Service Rules Section 7.0 Enforcement
                      </span>
                    </div>
                  )}
                </div>
              </div>
            );
          })
        )}

        {/* Loading Indicator */}
        {isLoading && (
          <div className="flex items-start gap-3">
            <div className="w-8 h-8 rounded-lg bg-sky-600 text-white flex items-center justify-center shrink-0">
              <Bot className="w-4 h-4 animate-spin" />
            </div>
            <div className="bg-slate-950 border border-slate-800 p-3 rounded-2xl rounded-tl-none text-xs text-slate-400 flex items-center gap-2">
              <span className="inline-flex gap-1">
                <span className="w-1.5 h-1.5 rounded-full bg-sky-400 animate-bounce" style={{ animationDelay: '0ms' }} />
                <span className="w-1.5 h-1.5 rounded-full bg-sky-400 animate-bounce" style={{ animationDelay: '150ms' }} />
                <span className="w-1.5 h-1.5 rounded-full bg-sky-400 animate-bounce" style={{ animationDelay: '300ms' }} />
              </span>
              <span>Evaluating deterministic policy rules and simulating operations...</span>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Suggested Quick Questions Bar */}
      <div className="px-3 py-2 bg-slate-950/90 border-t border-slate-800/80 shrink-0">
        <div className="text-[10px] uppercase font-semibold text-slate-400 mb-1.5 flex items-center gap-1">
          <Sparkles className="w-3 h-3 text-amber-400" />
          <span>Quick Suggestions (Click to send directly):</span>
        </div>
        <div className="flex flex-wrap gap-1.5">
          {suggestedQuestions.map((q, idx) => (
            <button
              key={idx}
              type="button"
              onClick={() => handlePromptClick(q)}
              disabled={isLoading}
              className="text-[11px] bg-slate-900 hover:bg-sky-950 text-slate-300 hover:text-sky-200 border border-slate-800 hover:border-sky-500/50 rounded-md px-2.5 py-1 transition-all text-left"
            >
              {q}
            </button>
          ))}
        </div>
      </div>

      {/* Message Input Form */}
      <div className="p-3 bg-slate-950 border-t border-slate-800 shrink-0">
        <form onSubmit={handleSubmit} className="flex items-center gap-2">
          <input
            ref={inputRef}
            type="text"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder={`Type a message as ${activeCustomer?.customer?.name || 'Customer'} (Press Enter to send)...`}
            disabled={isLoading}
            autoFocus
            className="flex-1 bg-slate-900 border border-slate-700/80 rounded-lg px-3.5 py-2.5 text-xs text-slate-100 placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-1 focus:ring-sky-500 transition-all shadow-inner"
          />
          <button
            type="submit"
            disabled={isLoading || !inputText.trim()}
            className="px-4 py-2.5 bg-sky-600 hover:bg-sky-500 disabled:opacity-40 disabled:cursor-not-allowed text-white rounded-lg text-xs font-semibold shadow-md shadow-sky-600/20 transition-all flex items-center gap-1.5 shrink-0"
          >
            <Send className="w-3.5 h-3.5" />
            <span>Send</span>
          </button>
        </form>
      </div>
    </div>
  );
}
