import { useMemo, useState } from 'react';
import { FEATURE_LEVEL } from '../../data/levels';
import { quote, type OrderType, type Side } from '../../engine/trading';
import { useGame } from '../../store/gameStore';
import { usePortfolioSummary, usePrices, useUnlocked } from '../../store/selectors';
import { fmtEur } from '../../utils/format';
import { Label } from '../ui/Help';
import { Locked } from '../ui/Tabs';
import { OrderConfirmModal, type OrderDraft } from './OrderConfirmModal';

const TYPES: { v: OrderType; label: string; term: string }[] = [
  { v: 'market', label: 'Marché', term: 'ordre-marche' },
  { v: 'limit', label: 'Limite', term: 'ordre-limite' },
  { v: 'stop', label: 'Stop-loss', term: 'stop-loss' },
  { v: 'takeprofit', label: 'Take-profit', term: 'take-profit' },
];

export function OrderPanel({ ticker }: { ticker: string }) {
  const prices = usePrices();
  const sum = usePortfolioSummary();
  const pos = useGame((s) => s.positions[ticker]);
  const limitOk = useUnlocked('limit');
  const stopOk = useUnlocked('stopTakeProfit');
  const shortOk = useUnlocked('short');
  const [side, setSide] = useState<Side>('buy');
  const [type, setType] = useState<OrderType>('market');
  const [qtyStr, setQtyStr] = useState('');
  const [trigStr, setTrigStr] = useState('');
  const [draft, setDraft] = useState<OrderDraft | null>(null);
  const [msg, setMsg] = useState<string | null>(null);

  const price = prices[ticker];
  const qty = Number(qtyStr);
  const trig = Number(trigStr.replace(',', '.'));
  const isProtective = type === 'stop' || type === 'takeprofit';
  const effSide: Side = isProtective ? (pos && pos.qty < 0 ? 'buy' : 'sell') : side;
  const refPrice = type === 'market' ? price : trig > 0 ? trig : price;
  const q = useMemo(() => quote(effSide, qty > 0 ? qty : 0, refPrice), [effSide, qty, refPrice]);
  const held = pos ? Math.abs(pos.qty) : 0;
  const unlocked: Record<OrderType, boolean> = { market: true, limit: limitOk, stop: stopOk, takeprofit: stopOk };

  const maxQty = () => {
    if (effSide === 'buy' && (!pos || pos.qty >= 0)) {
      let n = Math.floor(sum.buyingPower / refPrice);
      while (n > 0 && quote('buy', n, refPrice).total > sum.buyingPower) n--;
      return n;
    }
    return held;
  };

  let problem: string | null = null;
  if (!Number.isInteger(qty) || qty <= 0) problem = 'Indique une quantité (nombre entier).';
  else if (type !== 'market' && !(trig > 0)) problem = 'Indique un prix de déclenchement.';
  else if (isProtective && held === 0) problem = 'Un stop-loss ou un take-profit protège une position que tu possèdes déjà.';
  else if (effSide === 'buy' && (!pos || pos.qty >= 0) && q.total > sum.buyingPower) problem = 'Liquidités insuffisantes (frais compris).';
  else if (effSide === 'sell' && !isProtective && (!pos || pos.qty <= 0) && !shortOk) problem = `Tu ne possèdes pas cette action. La vente à découvert se débloque au niveau ${FEATURE_LEVEL.short}.`;
  else if (effSide === 'sell' && pos && pos.qty > 0 && qty > pos.qty) problem = `Tu ne possèdes que ${pos.qty} titre(s).`;

  return (
    <div className="card p-4" data-tour="order-panel">
      <div className="mb-3 grid grid-cols-2 gap-1 rounded-lg bg-bg p-1">
        {(['buy', 'sell'] as Side[]).map((s) => (
          <button
            key={s}
            disabled={isProtective}
            onClick={() => setSide(s)}
            className={`rounded-md py-1.5 text-sm font-semibold transition ${effSide === s ? (s === 'buy' ? 'bg-up text-black' : 'bg-down text-white') : 'text-slate-400 hover:text-white'}`}
          >
            {s === 'buy' ? 'Acheter' : 'Vendre'}
          </button>
        ))}
      </div>

      <div className="mb-3 flex flex-wrap gap-1">
        {TYPES.map((t) => (
          <button
            key={t.v}
            disabled={!unlocked[t.v]}
            onClick={() => {
              setType(t.v);
              if (t.v !== 'market' && !trigStr) setTrigStr(price.toFixed(2).replace('.', ','));
            }}
            className={`chip flex items-center gap-1 ${type === t.v ? 'border-accent bg-accent/15 text-white' : 'text-slate-400'} disabled:cursor-not-allowed disabled:opacity-60`}
          >
            {t.label}
            {!unlocked[t.v] && <Locked level={FEATURE_LEVEL[t.v === 'limit' ? 'limit' : 'stopTakeProfit']} />}
          </button>
        ))}
      </div>

      <div className="space-y-3">
        <label className="block">
          <span className="flex items-center justify-between text-xs text-slate-400">
            Quantité
            <button className="text-accent hover:underline" onClick={() => setQtyStr(String(maxQty()))} type="button">
              Max
            </button>
          </span>
          <input className="input mt-1" inputMode="numeric" placeholder="0" value={qtyStr} onChange={(e) => setQtyStr(e.target.value.replace(/[^0-9]/g, ''))} data-tour="order-qty" />
        </label>
        {type !== 'market' && (
          <label className="block">
            <span className="text-xs text-slate-400">
              <Label term={TYPES.find((t) => t.v === type)!.term}>
                {type === 'limit' ? (side === 'buy' ? 'Prix maximum d’achat' : 'Prix minimum de vente') : type === 'stop' ? 'Vendre si le cours descend à' : 'Vendre si le cours monte à'}
              </Label>
            </span>
            <input className="input mt-1" inputMode="decimal" value={trigStr} onChange={(e) => setTrigStr(e.target.value.replace(/[^0-9,.]/g, ''))} />
          </label>
        )}

        <dl className="space-y-1 rounded-lg bg-bg p-3 text-sm">
          <div className="flex justify-between">
            <dt className="text-slate-400">{type === 'market' ? 'Prix actuel' : 'Prix visé'}</dt>
            <dd className="num">{fmtEur(refPrice)}</dd>
          </div>
          <div className="flex justify-between">
            <dt className="text-slate-400">Montant</dt>
            <dd className="num">{fmtEur(q.amount)}</dd>
          </div>
          <div className="flex justify-between">
            <dt className="text-slate-400">
              <Label term="frais">Frais estimés</Label>
            </dt>
            <dd className="num text-gold">{fmtEur(q.fees)}</dd>
          </div>
          <div className="flex justify-between border-t border-line pt-1 font-medium">
            <dt className="text-slate-300">Total</dt>
            <dd className="num text-white">{fmtEur(q.total)}</dd>
          </div>
        </dl>

        <div className="flex justify-between text-xs text-slate-500">
          <span>
            Disponible : <span className="num text-slate-300">{fmtEur(sum.buyingPower)}</span>
          </span>
          <span>
            Détenu : <span className="num text-slate-300">{pos ? pos.qty : 0}</span>
          </span>
        </div>

        {qtyStr && problem && <p className="text-xs text-amber-300">{problem}</p>}
        {msg && <p className="text-xs text-up">{msg}</p>}

        <button
          className={`${effSide === 'buy' ? 'btn-buy' : 'btn-sell'} w-full py-2.5`}
          disabled={!!problem}
          data-tour="order-submit"
          onClick={() => {
            setMsg(null);
            setDraft({ ticker, side: effSide, type, qty, triggerPrice: type === 'market' ? undefined : trig });
          }}
        >
          {effSide === 'buy' ? 'Acheter' : 'Vendre'} {qty > 0 ? qty : ''} {ticker}
        </button>
      </div>

      <OrderConfirmModal
        draft={draft}
        onClose={() => setDraft(null)}
        onDone={() => {
          setDraft(null);
          setQtyStr('');
          setMsg(type === 'market' ? 'Ordre exécuté ✔' : 'Ordre enregistré ✔');
        }}
      />
    </div>
  );
}
