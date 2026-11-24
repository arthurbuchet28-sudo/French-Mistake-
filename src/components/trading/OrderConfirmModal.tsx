import { useEffect, useState } from 'react';
import { COMPANY_BY_TICKER } from '../../data/companies';
import { FEATURE_LEVEL } from '../../data/levels';
import { quote, round2, type OrderType, type Side } from '../../engine/trading';
import { useGame } from '../../store/gameStore';
import { usePortfolioSummary, usePrices, useUnlocked } from '../../store/selectors';
import { fmtEur, fmtNum, fmtPctPlain } from '../../utils/format';
import { Label } from '../ui/Help';
import { Modal } from '../ui/Modal';

export interface OrderDraft {
  ticker: string;
  side: Side;
  type: OrderType;
  qty: number;
  triggerPrice?: number;
}

const TYPE_LABEL: Record<OrderType, string> = { market: 'Au marché', limit: 'Ordre limite', stop: 'Stop-loss', takeprofit: 'Take-profit' };

export function OrderConfirmModal({ draft, onClose, onDone }: { draft: OrderDraft | null; onClose: () => void; onDone: () => void }) {
  const prices = usePrices();
  const sum = usePortfolioSummary();
  const positions = useGame((s) => s.positions);
  const orders = useGame((s) => s.orders);
  const placeOrder = useGame((s) => s.placeOrder);
  const stopUnlocked = useUnlocked('stopTakeProfit');
  const [note, setNote] = useState('');
  const [addStop, setAddStop] = useState(false);
  const [stopPrice, setStopPrice] = useState('');
  const [addTp, setAddTp] = useState(false);
  const [tpPrice, setTpPrice] = useState('');
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!draft) return;
    const p = prices[draft.ticker];
    setNote('');
    setError(null);
    setAddStop(false);
    setAddTp(false);
    const dir = draft.side === 'buy' ? 1 : -1;
    setStopPrice(fmtNum(round2(p * (1 - 0.08 * dir))).replace(/\s/g, ''));
    setTpPrice(fmtNum(round2(p * (1 + 0.15 * dir))).replace(/\s/g, ''));
  }, [draft]); // eslint-disable-line react-hooks/exhaustive-deps

  if (!draft) return null;
  const c = COMPANY_BY_TICKER[draft.ticker];
  const price = draft.type === 'market' ? prices[draft.ticker] : (draft.triggerPrice ?? prices[draft.ticker]);
  const q = quote(draft.side, draft.qty, price);
  const pos = positions[draft.ticker];
  const opensOrAdds =
    (draft.side === 'buy' && (!pos || pos.qty >= 0)) || (draft.side === 'sell' && (!pos || pos.qty <= 0));
  const newPosValue = Math.abs((pos?.qty ?? 0) * prices[draft.ticker]) + (opensOrAdds ? q.amount : -q.amount);
  const weight = sum.total > 0 ? newPosValue / sum.total : 0;
  const parseP = (s: string) => Number(s.replace(/\s/g, '').replace(',', '.'));
  const hasStop = orders.some((o) => o.ticker === draft.ticker && o.type === 'stop');
  const isEntry = opensOrAdds && (draft.type === 'market' || draft.type === 'limit');
  const warnNoStop = stopUnlocked && isEntry && draft.type === 'market' && !addStop && !hasStop;

  const confirm = () => {
    const r = placeOrder({
      ticker: draft.ticker,
      side: draft.side,
      qty: draft.qty,
      type: draft.type,
      triggerPrice: draft.triggerPrice,
      note,
      stopLoss: draft.type === 'market' && opensOrAdds && addStop ? parseP(stopPrice) : undefined,
      takeProfit: draft.type === 'market' && opensOrAdds && addTp ? parseP(tpPrice) : undefined,
    });
    if (r.ok) onDone();
    else setError(r.error ?? 'Ordre refusé.');
  };

  const sideLabel = draft.side === 'buy' ? (pos && pos.qty < 0 ? 'Rachat' : 'Achat') : pos && pos.qty > 0 ? 'Vente' : 'Vente à découvert';

  return (
    <Modal open onClose={onClose} title={`Confirmer : ${sideLabel} ${c.ticker}`}>
      <dl className="grid grid-cols-2 gap-x-4 gap-y-2 text-sm">
        <dt className="text-slate-400">Entreprise</dt>
        <dd className="text-right text-slate-100">{c.name}</dd>
        <dt className="text-slate-400">Type d’ordre</dt>
        <dd className="text-right text-slate-100">{TYPE_LABEL[draft.type]}</dd>
        <dt className="text-slate-400">Quantité</dt>
        <dd className="num text-right text-slate-100">{draft.qty}</dd>
        <dt className="text-slate-400">{draft.type === 'market' ? 'Prix estimé' : 'Prix de déclenchement'}</dt>
        <dd className="num text-right text-slate-100">{fmtEur(price)}</dd>
        <dt className="text-slate-400">Montant</dt>
        <dd className="num text-right text-slate-100">{fmtEur(q.amount)}</dd>
        <dt className="text-slate-400">
          <Label term="frais">Frais (0,5 %, min. 1 €)</Label>
        </dt>
        <dd className="num text-right text-gold">{fmtEur(q.fees)}</dd>
        <dt className="font-medium text-slate-200">{draft.side === 'buy' ? 'Total débité' : 'Total crédité'}</dt>
        <dd className="num text-right text-base font-semibold text-white">{fmtEur(q.total)}</dd>
        <dt className="text-slate-400">
          <Label term="portefeuille">Part du portefeuille</Label>
        </dt>
        <dd className={`num text-right ${weight > 0.25 ? 'text-down' : 'text-slate-100'}`}>{fmtPctPlain(weight)}</dd>
      </dl>
      {draft.type !== 'market' && (
        <p className="mt-3 rounded-lg bg-panel2 p-2 text-xs text-slate-400">
          Cet ordre attendra que le cours atteigne {fmtEur(price)}. Il sera alors exécuté au cours du moment (qui peut être légèrement différent).
        </p>
      )}

      {/* Garde-fous pédagogiques (non bloquants) */}
      <div className="mt-4 space-y-2">
        {opensOrAdds && weight > 0.25 && (
          <div className="rounded-lg border border-down/40 bg-down/10 p-2 text-xs text-red-200">
            ⚠️ Après cet ordre, {c.ticker} représenterait {fmtPctPlain(weight)} de ton portefeuille. Au-delà de 25 % sur une seule action, une mauvaise nouvelle peut te coûter très cher.
          </div>
        )}
        {q.amount > 0 && q.fees / q.amount > 0.01 && (
          <div className="rounded-lg border border-gold/40 bg-gold/10 p-2 text-xs text-amber-200">
            💸 Les frais représentent {fmtPctPlain(q.fees / q.amount)} du montant : le minimum de 1 € pèse lourd sur les petits ordres.
          </div>
        )}
        {warnNoStop && (
          <div className="rounded-lg border border-gold/40 bg-gold/10 p-2 text-xs text-amber-200">
            🚪 Tu achètes sans stop-loss. Sais-tu à quel prix tu sortiras si le cours baisse ?
          </div>
        )}
      </div>

      {stopUnlocked && draft.type === 'market' && opensOrAdds && (
        <div className="mt-3 space-y-2 rounded-lg border border-line p-3">
          <label className="flex items-center gap-2 text-sm">
            <input type="checkbox" checked={addStop} onChange={(e) => setAddStop(e.target.checked)} />
            <Label term="stop-loss">Ajouter un stop-loss à</Label>
            <input className="input ml-auto w-28 py-1 text-right" value={stopPrice} onChange={(e) => setStopPrice(e.target.value)} inputMode="decimal" />
            <span className="text-slate-400">€</span>
          </label>
          <label className="flex items-center gap-2 text-sm">
            <input type="checkbox" checked={addTp} onChange={(e) => setAddTp(e.target.checked)} />
            <Label term="take-profit">Ajouter un take-profit à</Label>
            <input className="input ml-auto w-28 py-1 text-right" value={tpPrice} onChange={(e) => setTpPrice(e.target.value)} inputMode="decimal" />
            <span className="text-slate-400">€</span>
          </label>
        </div>
      )}
      {!stopUnlocked && draft.type === 'market' && opensOrAdds && (
        <p className="mt-3 text-xs text-slate-500">🔒 Le stop-loss et le take-profit se débloquent au niveau {FEATURE_LEVEL.stopTakeProfit}.</p>
      )}

      <label className="mt-4 block">
        <span className="text-sm text-slate-300">
          <Label term="journal">📓 Pourquoi je prends cette décision ?</Label> <span className="text-slate-500">(facultatif)</span>
        </span>
        <textarea
          className="input mt-1 h-20 resize-none font-sans"
          placeholder="Ex. : bons résultats publiés, je vise +10 % et je sors à −8 %."
          value={note}
          onChange={(e) => setNote(e.target.value)}
        />
      </label>

      {error && <p className="mt-3 rounded-lg bg-down/15 p-2 text-sm text-red-300">{error}</p>}

      <div className="mt-4 flex gap-2">
        <button className="btn-ghost flex-1" onClick={onClose}>
          Annuler
        </button>
        <button className={`${draft.side === 'buy' ? 'btn-buy' : 'btn-sell'} flex-1`} onClick={confirm} data-tour="order-confirm">
          Confirmer
        </button>
      </div>
    </Modal>
  );
}
