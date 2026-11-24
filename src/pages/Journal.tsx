import { useState } from 'react';
import { Card } from '../components/ui/Card';
import { Help } from '../components/ui/Help';
import { Money, Pct } from '../components/ui/Num';
import type { Transaction } from '../engine/trading';
import { useGame } from '../store/gameStore';
import { usePrices } from '../store/selectors';
import { fmtDate, fmtNum } from '../utils/format';

function Outcome({ t, price }: { t: Transaction; price: number }) {
  if (t.realizedPnl !== undefined) {
    const after = t.side === 'sell' ? price / t.price - 1 : 1 - price / t.price;
    return (
      <div className="text-xs">
        Résultat réalisé : <Money value={t.realizedPnl} signed color /> (<Pct value={t.realizedPct ?? 0} />)
        <div className="text-slate-500">
          Depuis, le cours a évolué de <Pct value={price / t.price - 1} />
          {after < -0.03 ? ' — tu as peut-être vendu trop tôt.' : after > 0.03 ? ' — bien vu d’être sorti !' : '.'}
        </div>
      </div>
    );
  }
  const dir = t.side === 'buy' ? 1 : -1;
  const r = dir * (price / t.price - 1);
  return (
    <div className="text-xs">
      Depuis cette décision : <Pct value={r} /> (<Money value={dir * t.qty * (price - t.price) - t.fees} signed color /> frais d’achat inclus)
    </div>
  );
}

function Entry({ t, price }: { t: Transaction; price: number }) {
  const setNote = useGame((s) => s.setNote);
  const [edit, setEdit] = useState(false);
  const [text, setText] = useState(t.note ?? '');
  return (
    <li className="card p-4">
      <div className="flex flex-wrap items-center gap-2 text-sm">
        <span className="num text-xs text-slate-500">{fmtDate(t.day)}</span>
        <span className={t.side === 'buy' ? 'text-up' : 'text-down'}>{t.side === 'buy' ? (t.effect === 'close' ? 'Rachat' : 'Achat') : t.effect === 'close' ? 'Vente' : 'Vente à découvert'}</span>
        <span className="font-mono font-semibold text-white">{t.ticker}</span>
        <span className="num text-slate-400">
          {t.qty} × {fmtNum(t.price)} €
        </span>
      </div>
      <div className="mt-3 grid gap-3 md:grid-cols-2">
        <div className="rounded-lg bg-panel2 p-3">
          <div className="mb-1 text-[11px] uppercase tracking-wide text-slate-500">Pourquoi je prends cette décision ?</div>
          {edit ? (
            <div>
              <textarea className="input h-20 resize-none font-sans" value={text} onChange={(e) => setText(e.target.value)} autoFocus />
              <div className="mt-2 flex gap-2">
                <button className="btn-primary px-2 py-1 text-xs" onClick={() => { setNote(t.id, text); setEdit(false); }}>Enregistrer</button>
                <button className="btn-ghost px-2 py-1 text-xs" onClick={() => { setText(t.note ?? ''); setEdit(false); }}>Annuler</button>
              </div>
            </div>
          ) : t.note ? (
            <p className="whitespace-pre-wrap text-sm text-slate-200">
              « {t.note} » <button className="ml-1 text-xs text-accent hover:underline" onClick={() => setEdit(true)}>modifier</button>
            </p>
          ) : (
            <button className="text-sm text-accent hover:underline" onClick={() => setEdit(true)}>+ Ajouter ma raison</button>
          )}
        </div>
        <div className="rounded-lg bg-panel2 p-3">
          <div className="mb-1 text-[11px] uppercase tracking-wide text-slate-500">Résultat réel</div>
          <Outcome t={t} price={price} />
        </div>
      </div>
    </li>
  );
}

export default function Journal() {
  const tx = useGame((s) => s.transactions);
  const prices = usePrices();
  const [onlyNotes, setOnlyNotes] = useState(false);
  const list = [...tx].reverse().filter((t) => !onlyNotes || t.note);
  const withNote = tx.filter((t) => t.note).length;
  return (
    <div className="space-y-4">
      <Card title={<span className="inline-flex items-center gap-1">📓 Journal de trading <Help term="journal" /></span>}>
        <p className="text-sm text-slate-300">
          Relis tes raisons à côté du résultat réel. Repères-tu des erreurs qui reviennent ? Achats sur des rumeurs, ventes trop rapides, positions trop grosses… ?
        </p>
        <div className="mt-3 flex items-center justify-between text-xs text-slate-400">
          <span>
            {withNote} note(s) sur {tx.length} ordre(s)
          </span>
          <label className="flex items-center gap-1.5">
            <input type="checkbox" checked={onlyNotes} onChange={(e) => setOnlyNotes(e.target.checked)} /> Seulement les ordres commentés
          </label>
        </div>
      </Card>
      {list.length === 0 ? (
        <p className="card p-8 text-center text-sm text-slate-500">Ton journal est vide. Il se remplit à chaque ordre.</p>
      ) : (
        <ul className="space-y-3">
          {list.map((t) => (
            <Entry key={t.id} t={t} price={prices[t.ticker]} />
          ))}
        </ul>
      )}
    </div>
  );
}
