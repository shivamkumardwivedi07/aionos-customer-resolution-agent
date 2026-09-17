import React from 'react';
import { PlayCircle, ShieldAlert, Sparkles, Scale, Lock, CreditCard } from 'lucide-react';

export default function QuickScenarios({ scenarios, onSelectScenario, activeScenarioId }) {
  const mandatoryScenarios = scenarios.filter((s) => !s.id.startsWith('scenario-adversarial'));
  const adversarialScenarios = scenarios.filter((s) => s.id.startsWith('scenario-adversarial'));

  return (
    <div className="bg-slate-900/60 rounded-xl border border-slate-800 p-3.5 space-y-3">
      <div>
        <div className="flex items-center justify-between mb-2">
          <label className="text-[11px] font-semibold uppercase tracking-wider text-slate-400 flex items-center gap-1.5">
            <Sparkles className="w-3.5 h-3.5 text-amber-400" />
            Mandatory Test Scenarios
          </label>
          <span className="text-[10px] text-slate-400 font-mono">1-Click Test</span>
        </div>
        <div className="space-y-1.5">
          {mandatoryScenarios.map((sc) => {
            const isActive = activeScenarioId === sc.id;
            return (
              <button
                key={sc.id}
                onClick={() => onSelectScenario(sc)}
                className={`w-full text-left p-2.5 rounded-lg border transition-all flex items-start space-x-2.5 group ${
                  isActive
                    ? 'bg-sky-950/70 border-sky-500/80 shadow-md shadow-sky-500/10'
                    : 'bg-slate-950/60 border-slate-800/80 hover:bg-slate-800/60 hover:border-slate-700'
                }`}
              >
                <PlayCircle className={`w-4 h-4 mt-0.5 shrink-0 transition-transform group-hover:scale-110 ${
                  isActive ? 'text-sky-400' : 'text-slate-400'
                }`} />
                <div className="min-w-0 flex-1">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-bold text-slate-200 truncate">
                      {sc.title.split('—')[1]?.trim() || sc.title}
                    </span>
                    <span className="text-[10px] font-semibold px-1.5 py-0.2 rounded bg-slate-800 text-slate-300 font-mono">
                      {sc.customer_name.split(' ')[0]}
                    </span>
                  </div>
                  <p className="text-[11px] text-slate-400 truncate mt-0.5">
                    {sc.subtitle}
                  </p>
                </div>
              </button>
            );
          })}
        </div>
      </div>

      {/* Adversarial & Boundary Tests */}
      <div className="pt-2 border-t border-slate-800">
        <label className="text-[11px] font-semibold uppercase tracking-wider text-rose-400/90 flex items-center gap-1.5 mb-2">
          <ShieldAlert className="w-3.5 h-3.5 text-rose-400" />
          Adversarial & Boundary Tests
        </label>
        <div className="grid grid-cols-3 gap-1.5">
          {adversarialScenarios.map((sc) => {
            const isLegal = sc.id.includes('legal');
            const isPrivacy = sc.id.includes('privacy');
            const isPayment = sc.id.includes('payment');

            return (
              <button
                key={sc.id}
                onClick={() => onSelectScenario(sc)}
                className="p-2 rounded-lg bg-slate-950/80 border border-slate-800 hover:border-rose-500/50 hover:bg-rose-950/20 text-left transition-all group"
                title={sc.subtitle}
              >
                <div className="flex items-center gap-1 text-[11px] font-semibold text-slate-300 group-hover:text-rose-300">
                  {isLegal && <Scale className="w-3.5 h-3.5 text-amber-400" />}
                  {isPrivacy && <Lock className="w-3.5 h-3.5 text-sky-400" />}
                  {isPayment && <CreditCard className="w-3.5 h-3.5 text-emerald-400" />}
                  <span className="truncate">
                    {isLegal ? 'Legal Threat' : isPrivacy ? 'Privacy' : 'Cash/UPI'}
                  </span>
                </div>
              </button>
            );
          })}
        </div>
      </div>
    </div>
  );
}
