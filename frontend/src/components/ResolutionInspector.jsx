import React from 'react';
import { ShieldCheck, BookOpen, AlertOctagon, CheckCircle, XCircle, FileText, Sliders, ExternalLink } from 'lucide-react';

export default function ResolutionInspector({ resolution, policies }) {
  if (!resolution) {
    return (
      <div className="w-full h-full min-h-0 bg-slate-900/60 rounded-xl border border-slate-800 p-4 shadow-md flex flex-col items-center justify-center text-center text-slate-400">
        <Sliders className="w-8 h-8 text-slate-400 mb-2" />
        <h3 className="text-xs font-bold text-slate-300">Policy Resolution Inspector</h3>
        <p className="text-[11px] text-slate-400 mt-1 max-w-xs">
          Send a customer message or trigger a demo scenario to view live policy evaluations, authority checks, and citations.
        </p>
      </div>
    );
  }

  const {
    detected_intents = [],
    detected_sentiment = 'Neutral',
    policy_decisions = [],
    actions_taken = [],
    escalated = false,
    escalation_reason = null,
    policy_citations = []
  } = resolution;

  return (
    <div className="w-full h-full min-h-0 bg-slate-900/60 rounded-xl border border-slate-800 p-4 shadow-md flex flex-col space-y-4 overflow-y-auto">
      {/* Header */}
      <div className="border-b border-slate-800 pb-2.5 flex items-center justify-between">
        <div>
          <h2 className="text-xs font-bold uppercase tracking-wider text-slate-200 flex items-center gap-1.5">
            <ShieldCheck className="w-4 h-4 text-sky-400" />
            Resolution Inspector
          </h2>
          <span className="text-[10px] text-slate-400 font-mono">Deterministic Grounding Engine</span>
        </div>
        <span className={`px-2 py-0.5 text-[10px] font-bold rounded-full border uppercase ${
          escalated
            ? 'bg-rose-500/20 text-rose-300 border-rose-500/40'
            : 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40'
        }`}>
          {escalated ? 'Escalated' : 'Resolved'}
        </span>
      </div>

      {/* Detected Intents */}
      <div>
        <label className="text-[11px] font-semibold uppercase tracking-wider text-slate-400 block mb-1.5">
          Parsed Intents ({detected_intents.length})
        </label>
        <div className="flex flex-wrap gap-1">
          {detected_intents.map((intent, idx) => (
            <span
              key={idx}
              className="px-2 py-0.5 rounded bg-slate-800 text-sky-300 text-[10px] font-mono border border-slate-700 font-medium"
            >
              {intent}
            </span>
          ))}
        </div>
      </div>

      {/* Authority Boundary Gauge */}
      <div className="bg-slate-950/80 rounded-lg border border-slate-800 p-3 space-y-2">
        <div className="flex justify-between items-center text-[11px] font-semibold text-slate-300">
          <span>Agent Authority Limit</span>
          <span className="font-mono text-emerald-400">Max ₹1,500</span>
        </div>
        <div className="w-full bg-slate-800 rounded-full h-2 overflow-hidden">
          <div
            className={`h-full transition-all ${
              escalated && escalation_reason?.includes('1500')
                ? 'w-full bg-rose-500'
                : 'w-2/3 bg-emerald-500'
            }`}
          />
        </div>
        <div className="flex justify-between text-[10px] text-slate-400">
          <span>Standard Waiver: ≤ ₹1,500</span>
          <span>Supervisor: &gt; ₹1,500</span>
        </div>
      </div>

      {/* Policy Decisions List */}
      <div className="space-y-2">
        <label className="text-[11px] font-semibold uppercase tracking-wider text-slate-400 block">
          Evaluated Policy Rules ({policy_decisions.length})
        </label>
        <div className="space-y-2">
          {policy_decisions.map((dec, i) => (
            <div
              key={i}
              className="bg-slate-950/70 border border-slate-800/90 rounded-lg p-2.5 text-xs space-y-1.5"
            >
              <div className="flex items-center justify-between">
                <span className="font-bold text-slate-200 text-[11px] truncate flex items-center gap-1">
                  {dec.eligible ? (
                    <CheckCircle className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
                  ) : (
                    <XCircle className="w-3.5 h-3.5 text-rose-400 shrink-0" />
                  )}
                  {dec.policy_name}
                </span>
                <span className="font-mono text-[9px] bg-slate-800 px-1 py-0.2 rounded text-slate-300">
                  {dec.policy_id}
                </span>
              </div>

              <p className="text-[11px] text-slate-400 leading-normal">
                {dec.explanation}
              </p>

              {/* Restrictions */}
              {dec.restrictions && dec.restrictions.length > 0 && (
                <div className="pt-1 border-t border-slate-800/80 flex flex-wrap gap-1">
                  {dec.restrictions.map((r, rIdx) => (
                    <span
                      key={rIdx}
                      className="text-[9px] font-mono text-amber-300 bg-amber-500/10 px-1.5 py-0.2 rounded border border-amber-500/20"
                    >
                      {r}
                    </span>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Policy Citations */}
      <div className="pt-2 border-t border-slate-800 space-y-1.5">
        <label className="text-[11px] font-semibold uppercase tracking-wider text-slate-400 flex items-center gap-1">
          <BookOpen className="w-3.5 h-3.5 text-sky-400" />
          Authoritative Citations
        </label>
        <div className="space-y-1">
          {policy_citations.map((cite, idx) => (
            <div
              key={idx}
              className="text-[10px] text-slate-300 bg-slate-950/50 px-2 py-1 rounded border border-slate-800/80 font-mono flex items-center gap-1.5"
            >
              <FileText className="w-3 h-3 text-slate-400 shrink-0" />
              <span className="truncate">{cite}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
