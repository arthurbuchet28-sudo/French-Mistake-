import { useEffect } from 'react';
import { useGame } from '../../store/gameStore';
import type { Toast } from '../../store/types';

const STYLE: Record<Toast['kind'], string> = {
  success: 'border-up/40',
  error: 'border-down/50',
  info: 'border-accent/40',
  mission: 'border-gold/60',
  badge: 'border-fuchsia-500/60',
  news: 'border-slate-500/50',
};
const ICON: Record<Toast['kind'], string> = { success: '✅', error: '⚠️', info: 'ℹ️', mission: '🎯', badge: '🏅', news: '📰' };

function ToastItem({ t }: { t: Toast }) {
  const dismiss = useGame((s) => s.dismissToast);
  useEffect(() => {
    const id = setTimeout(() => dismiss(t.id), t.kind === 'mission' || t.kind === 'badge' ? 7000 : 5000);
    return () => clearTimeout(id);
  }, [t.id, t.kind, dismiss]);
  return (
    <div className={`pointer-events-auto card flex items-start gap-2 border-l-4 p-3 shadow-2xl ${STYLE[t.kind]}`} role="status">
      <span>{ICON[t.kind]}</span>
      <div className="min-w-0 flex-1">
        <div className="text-sm font-medium text-slate-100">{t.title}</div>
        {t.body && <div className="mt-0.5 text-xs text-slate-400">{t.body}</div>}
      </div>
      <button className="text-xs text-slate-500 hover:text-white" onClick={() => dismiss(t.id)} aria-label="Fermer">
        ✕
      </button>
    </div>
  );
}

export function Toasts() {
  const toasts = useGame((s) => s.toasts);
  return (
    <div className="pointer-events-none fixed bottom-10 right-3 z-[80] flex w-[min(360px,calc(100vw-24px))] flex-col gap-2">
      {toasts.map((t) => (
        <ToastItem key={t.id} t={t} />
      ))}
    </div>
  );
}
