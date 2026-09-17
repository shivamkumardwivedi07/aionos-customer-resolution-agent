import React from 'react';
import { Plane, ShieldCheck, RotateCcw, AlertTriangle, FileText } from 'lucide-react';

export default function Header({ onReset, onToggleAudit, isAuditOpen, agentStatus = 'Online' }) {
  return (
    <header className="h-16 bg-slate-900/90 backdrop-blur-md border-b border-slate-800 px-6 flex items-center justify-between shrink-0 z-20">
      <div className="flex items-center space-x-3">
        <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-sky-500 to-blue-700 flex items-center justify-center shadow-lg shadow-sky-500/20">
          <Plane className="w-6 h-6 text-white transform -rotate-45" />
        </div>
        <div>
          <div className="flex items-center space-x-2">
            <h1 className="text-base font-bold text-white tracking-tight">
              AIONOS Airline Customer Resolution Agent
            </h1>
            <span className="px-2 py-0.5 text-xs font-semibold rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 flex items-center gap-1">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
              {agentStatus}
            </span>
          </div>
          <p className="text-xs text-slate-400">
            Operations Console • Disruption Date: <span className="text-slate-300 font-medium">Wed, 23 Sep 2026</span> • Grounded in Authoritative Policy Pack
          </p>
        </div>
      </div>

      <div className="flex items-center space-x-3">
        <div className="hidden lg:flex items-center space-x-2 px-3 py-1.5 rounded-lg bg-slate-800/80 border border-slate-700/60 text-xs text-slate-300">
          <ShieldCheck className="w-4 h-4 text-sky-400" />
          <span>LLM for Language • Deterministic Rules for Decisions</span>
        </div>

        <button
          onClick={onToggleAudit}
          className={`px-3 py-1.5 rounded-lg text-xs font-medium border transition-all flex items-center gap-1.5 ${
            isAuditOpen
              ? 'bg-sky-500/20 text-sky-300 border-sky-500/40 shadow-sm shadow-sky-500/20'
              : 'bg-slate-800 text-slate-300 border-slate-700 hover:bg-slate-700/80 hover:text-white'
          }`}
          title="Open Audit Trail & Event Logs"
        >
          <FileText className="w-3.5 h-3.5" />
          <span>Audit Trail</span>
        </button>

        <button
          onClick={onReset}
          className="px-3 py-1.5 rounded-lg text-xs font-medium bg-slate-800 text-slate-300 border border-slate-700 hover:bg-rose-950/40 hover:text-rose-300 hover:border-rose-800/50 transition-all flex items-center gap-1.5"
          title="Reset conversation state and simulated transactions"
        >
          <RotateCcw className="w-3.5 h-3.5" />
          <span>Reset State</span>
        </button>
      </div>
    </header>
  );
}
