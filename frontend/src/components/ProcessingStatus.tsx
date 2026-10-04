import React from 'react';
import { Check, Loader2, Circle } from 'lucide-react';
import type { ProcessingStep } from '../types/document';

interface ProcessingStatusProps {
  steps: ProcessingStep[];
  currentStepIndex: number;
}

export const ProcessingStatus: React.FC<ProcessingStatusProps> = ({ steps, currentStepIndex }) => {
  const percentage = Math.min(100, Math.round(((currentStepIndex + 1) / steps.length) * 100));

  return (
    <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-6 shadow-xl">
      <div className="flex items-center justify-between mb-4">
        <h4 className="text-sm font-semibold text-white">Pipeline Execution</h4>
        <span className="text-xs font-mono font-medium text-blue-400 bg-blue-500/10 px-2 py-0.5 rounded-full border border-blue-500/20">
          {percentage}%
        </span>
      </div>

      {/* Progress Bar */}
      <div className="w-full bg-slate-800 rounded-full h-1.5 mb-6 overflow-hidden">
        <div
          className="bg-gradient-to-r from-blue-500 to-sky-400 h-1.5 rounded-full transition-all duration-300"
          style={{ width: `${percentage}%` }}
        />
      </div>

      {/* Step Indicators */}
      <div className="space-y-3">
        {steps.map((step, idx) => {
          const isDone = idx < currentStepIndex;
          const isCurrent = idx === currentStepIndex;

          return (
            <div
              key={step.id}
              className={`flex items-center gap-3 text-xs transition-colors ${
                isDone
                  ? 'text-emerald-400'
                  : isCurrent
                  ? 'text-blue-400 font-medium'
                  : 'text-slate-500'
              }`}
            >
              {isDone ? (
                <div className="w-5 h-5 rounded-full bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center shrink-0">
                  <Check className="w-3 h-3 text-emerald-400" />
                </div>
              ) : isCurrent ? (
                <div className="w-5 h-5 rounded-full bg-blue-500/10 border border-blue-500/20 flex items-center justify-center shrink-0">
                  <Loader2 className="w-3 h-3 text-blue-400 animate-spin" />
                </div>
              ) : (
                <div className="w-5 h-5 rounded-full bg-slate-800 flex items-center justify-center shrink-0">
                  <Circle className="w-2.5 h-2.5 text-slate-600" />
                </div>
              )}
              <span>{step.label}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
};
