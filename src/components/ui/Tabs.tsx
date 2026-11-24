export function Tabs<T extends string>({ value, options, onChange, size = 'sm' }: { value: T; options: { value: T; label: string; disabled?: boolean; title?: string }[]; onChange: (v: T) => void; size?: 'sm' | 'xs' }) {
  return (
    <div className="inline-flex rounded-lg border border-line bg-bg p-0.5">
      {options.map((o) => (
        <button
          key={o.value}
          type="button"
          title={o.title}
          disabled={o.disabled}
          onClick={() => onChange(o.value)}
          className={`rounded-md ${size === 'xs' ? 'px-2 py-0.5 text-xs' : 'px-3 py-1 text-sm'} font-medium transition disabled:cursor-not-allowed disabled:opacity-40 ${
            value === o.value ? 'bg-panel2 text-white shadow' : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          {o.label}
        </button>
      ))}
    </div>
  );
}

export function Locked({ level }: { level: number }) {
  return (
    <span className="inline-flex items-center gap-1 rounded bg-panel2 px-1.5 py-0.5 text-[10px] font-medium text-slate-400" title={`Débloqué au niveau ${level}`}>
      🔒 Niv. {level}
    </span>
  );
}
