import { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import { GLOSSARY } from '../data/glossary';

const norm = (s: string) => s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '');

export default function Glossary() {
  const [q, setQ] = useState('');
  const { hash } = useLocation();
  const active = hash.replace('#', '');
  useEffect(() => {
    if (!active) return;
    const el = document.getElementById(`g-${active}`);
    el?.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }, [active]);
  const list = [...GLOSSARY].sort((a, b) => a.term.localeCompare(b.term, 'fr')).filter((g) => !q || norm(g.term + g.definition).includes(norm(q)));
  return (
    <div className="space-y-4">
      <div className="card p-4">
        <h1 className="text-lg font-semibold text-white">📖 Glossaire</h1>
        <p className="mt-1 text-sm text-slate-400">Tous les termes de l’application, expliqués simplement avec un exemple. Les « ? » de l’interface renvoient ici.</p>
        <input className="input mt-3 font-sans" placeholder="Rechercher un terme…" value={q} onChange={(e) => setQ(e.target.value)} />
      </div>
      <ul className="grid gap-3 md:grid-cols-2">
        {list.map((g) => (
          <li key={g.id} id={`g-${g.id}`} className={`card p-4 transition ${active === g.id ? 'border-accent ring-1 ring-accent' : ''}`}>
            <h2 className="font-semibold text-white">{g.term}</h2>
            <p className="mt-1 text-sm text-slate-300">{g.definition}</p>
            <p className="mt-2 rounded-lg bg-panel2 p-2 text-sm text-slate-400">
              <span className="text-slate-300">Exemple :</span> {g.example}
            </p>
          </li>
        ))}
      </ul>
    </div>
  );
}
