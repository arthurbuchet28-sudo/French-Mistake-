import type { ReactNode } from 'react';

export function Card({ title, right, children, className = '', tour }: { title?: ReactNode; right?: ReactNode; children: ReactNode; className?: string; tour?: string }) {
  return (
    <section className={`card ${className}`} data-tour={tour}>
      {(title || right) && (
        <header className="flex items-center justify-between gap-2 border-b border-line px-4 py-3">
          <h2 className="text-sm font-semibold text-slate-200">{title}</h2>
          {right}
        </header>
      )}
      <div className="p-4">{children}</div>
    </section>
  );
}

export function Stat({ label, value, sub, className = '' }: { label: ReactNode; value: ReactNode; sub?: ReactNode; className?: string }) {
  return (
    <div className={`card p-4 ${className}`}>
      <div className="flex items-center gap-1 text-xs text-slate-400">{label}</div>
      <div className="num mt-1 text-xl font-semibold text-slate-50">{value}</div>
      {sub && <div className="num mt-0.5 text-xs">{sub}</div>}
    </div>
  );
}
