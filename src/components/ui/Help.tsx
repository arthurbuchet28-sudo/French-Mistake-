import { useState } from 'react';
import { Link } from 'react-router-dom';
import { GLOSSARY_BY_ID } from '../../data/glossary';

/** Infobulle « ? » qui renvoie vers le glossaire */
export function Help({ term }: { term: string }) {
  const g = GLOSSARY_BY_ID[term];
  const [open, setOpen] = useState(false);
  if (!g) return null;
  return (
    <span className="relative inline-flex" onMouseEnter={() => setOpen(true)} onMouseLeave={() => setOpen(false)}>
      <button
        type="button"
        aria-label={`Définition : ${g.term}`}
        className="inline-flex h-4 w-4 items-center justify-center rounded-full border border-slate-600 text-[10px] font-bold leading-none text-slate-400 hover:border-accent hover:text-accent"
        onClick={(e) => {
          e.preventDefault();
          e.stopPropagation();
          setOpen((o) => !o);
        }}
      >
        ?
      </button>
      {open && (
        <span className="absolute left-1/2 top-5 z-[70] w-60 -translate-x-1/2 rounded-lg border border-line bg-panel2 p-3 text-left text-xs font-normal normal-case tracking-normal text-slate-300 shadow-xl">
          <span className="block font-semibold text-slate-100">{g.term}</span>
          <span className="mt-1 block">{g.short}</span>
          <Link to={`/glossaire#${g.id}`} className="mt-2 block text-accent hover:underline" onClick={() => setOpen(false)}>
            Voir dans le glossaire →
          </Link>
        </span>
      )}
    </span>
  );
}

export function Label({ children, term }: { children: React.ReactNode; term?: string }) {
  return (
    <span className="inline-flex items-center gap-1">
      {children}
      {term && <Help term={term} />}
    </span>
  );
}
