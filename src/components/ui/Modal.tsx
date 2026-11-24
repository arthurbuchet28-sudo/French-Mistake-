import { useEffect, type ReactNode } from 'react';

export function Modal({ open, onClose, title, children, wide = false, z = 'z-50' }: { open: boolean; onClose?: () => void; title?: ReactNode; children: ReactNode; wide?: boolean; z?: string }) {
  useEffect(() => {
    if (!open || !onClose) return;
    const h = (e: KeyboardEvent) => e.key === 'Escape' && onClose();
    window.addEventListener('keydown', h);
    return () => window.removeEventListener('keydown', h);
  }, [open, onClose]);
  if (!open) return null;
  return (
    <div className={`fixed inset-0 ${z} flex items-end justify-center bg-black/70 p-0 sm:items-center sm:p-4`} onClick={onClose}>
      <div
        role="dialog"
        aria-modal="true"
        className={`card max-h-[92vh] w-full overflow-y-auto rounded-b-none sm:rounded-xl ${wide ? 'sm:max-w-2xl' : 'sm:max-w-md'}`}
        onClick={(e) => e.stopPropagation()}
      >
        {title && (
          <div className="flex items-center justify-between border-b border-line px-5 py-3">
            <h2 className="font-semibold text-slate-100">{title}</h2>
            {onClose && (
              <button className="text-slate-400 hover:text-white" onClick={onClose} aria-label="Fermer">
                ✕
              </button>
            )}
          </div>
        )}
        <div className="p-5">{children}</div>
      </div>
    </div>
  );
}
