import React, { useState } from 'react';
import { X, Download, Search, CheckCircle2, AlertTriangle, ShieldCheck, Clock, FileText } from 'lucide-react';

export default function AuditTrailDrawer({ isOpen, onClose, auditEvents, onExportJson }) {
  const [searchTerm, setSearchTerm] = useState('');

  if (!isOpen) return null;

  const filteredEvents = auditEvents.filter((ev) => {
    const q = searchTerm.toLowerCase();
    return (
      ev.customer_name?.toLowerCase().includes(q) ||
      ev.pnr?.toLowerCase().includes(q) ||
      ev.user_message?.toLowerCase().includes(q) ||
      ev.detected_intents?.some((i) => i.toLowerCase().includes(q))
    );
  });

  return (
    <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-sm flex justify-end">
      <div className="w-full max-w-2xl bg-slate-900 border-l border-slate-800 h-full flex flex-col shadow-2xl animate-in slide-in-from-right duration-200">
        {/* Header */}
        <div className="p-4 border-b border-slate-800 flex items-center justify-between bg-slate-900/80">
          <div>
            <h2 className="text-sm font-bold text-white flex items-center gap-2">
              <FileText className="w-4 h-4 text-sky-400" />
              Compliance & Audit Trail Record
            </h2>
            <p className="text-xs text-slate-400 mt-0.5">
              Immutable log of every natural language input, deterministic policy rule, simulated action, and escalation.
            </p>
          </div>
          <div className="flex items-center space-x-2">
            <button
              onClick={onExportJson}
              className="px-3 py-1.5 rounded-lg text-xs font-semibold bg-sky-600 hover:bg-sky-500 text-white flex items-center gap-1.5 transition-all"
              title="Download structured JSON audit export"
            >
              <Download className="w-3.5 h-3.5" />
              <span>Export JSON</span>
            </button>
            <button
              onClick={onClose}
              className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-all"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Filter bar */}
        <div className="p-3 border-b border-slate-800/80 bg-slate-950/50">
          <div className="relative">
            <Search className="w-3.5 h-3.5 text-slate-400 absolute left-3 top-2.5" />
            <input
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="Search by customer name, PNR, intent, or message keyword..."
              className="w-full bg-slate-900 border border-slate-700 rounded-lg pl-8 pr-3 py-1.5 text-xs text-slate-100 placeholder-slate-400 focus:outline-none focus:border-sky-500"
            />
          </div>
        </div>

        {/* Event List */}
        <div className="flex-1 overflow-y-auto p-4 space-y-3">
          {filteredEvents.length === 0 ? (
            <div className="text-center py-12 text-slate-400 text-xs">
              No audit records matching your search query.
            </div>
          ) : (
            filteredEvents.map((ev) => (
              <div
                key={ev.audit_id}
                className="bg-slate-950/80 border border-slate-800 rounded-xl p-3.5 text-xs space-y-2 shadow-sm"
              >
                <div className="flex items-center justify-between border-b border-slate-800/80 pb-2">
                  <div className="flex items-center gap-2">
                    <span className="font-bold text-slate-200">{ev.customer_name}</span>
                    <span className="font-mono text-amber-300 bg-amber-500/10 px-1.5 py-0.2 rounded border border-amber-500/20 text-[10px]">
                      {ev.pnr}
                    </span>
                    <span className="text-[10px] text-slate-400 font-mono flex items-center gap-1">
                      <Clock className="w-3 h-3" />
                      {ev.timestamp}
                    </span>
                  </div>
                  <span className={`px-2 py-0.5 text-[9px] font-bold uppercase rounded-full border ${
                    ev.escalated
                      ? 'bg-rose-500/20 text-rose-300 border-rose-500/40'
                      : 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40'
                  }`}>
                    {ev.escalated ? 'Escalated' : 'Resolved'}
                  </span>
                </div>

                {/* User Message */}
                <div>
                  <span className="text-[10px] font-semibold uppercase text-slate-400">User Input:</span>
                  <p className="text-[11px] text-slate-200 mt-0.5 bg-slate-900/60 p-2 rounded border border-slate-800">
                    "{ev.user_message}"
                  </p>
                </div>

                {/* Intents & Decisions */}
                <div className="grid grid-cols-2 gap-2 text-[11px]">
                  <div>
                    <span className="text-[10px] font-semibold uppercase text-slate-400 block">Intents:</span>
                    <div className="flex flex-wrap gap-1 mt-0.5">
                      {ev.detected_intents?.map((int, i) => (
                        <span key={i} className="text-[9px] font-mono bg-slate-800 text-sky-300 px-1.5 py-0.2 rounded">
                          {int}
                        </span>
                      ))}
                    </div>
                  </div>
                  <div>
                    <span className="text-[10px] font-semibold uppercase text-slate-400 block">Actions:</span>
                    <div className="flex flex-wrap gap-1 mt-0.5">
                      {ev.actions_taken?.map((act, i) => (
                        <span key={i} className="text-[9px] font-mono bg-sky-950 text-sky-300 px-1.5 py-0.2 rounded border border-sky-800">
                          {act.action_type}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>

                {/* Citations */}
                {ev.policy_citations && ev.policy_citations.length > 0 && (
                  <div className="pt-1.5 border-t border-slate-800/80 text-[10px] text-slate-400 font-mono">
                    <span className="text-slate-400 font-semibold">Citations: </span>
                    {ev.policy_citations.join(' • ')}
                  </div>
                )}
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
