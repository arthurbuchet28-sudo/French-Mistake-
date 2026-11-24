import { Card, Stat } from '../components/ui/Card';
import { Label } from '../components/ui/Help';
import { Money } from '../components/ui/Num';
import { useGame } from '../store/gameStore';
import { labelOrderType } from '../store/logic';
import { fmtDate, fmtNum, fmtTime } from '../utils/format';

export default function History() {
  const tx = useGame((s) => s.transactions);
  const dividends = useGame((s) => s.dividends);
  const fees = tx.reduce((a, t) => a + t.fees, 0);
  const realized = tx.reduce((a, t) => a + (t.realizedPnl ?? 0), 0);
  const divTotal = dividends.reduce((a, d) => a + d.amount, 0);
  return (
    <div className="space-y-4">
      <div className="grid grid-cols-2 gap-3 lg:grid-cols-4">
        <Stat label="Ordres exécutés" value={tx.length} />
        <Stat label={<Label term="realise">P&L réalisé</Label>} value={<Money value={realized} signed color />} />
        <Stat label={<Label term="frais">Frais payés</Label>} value={<Money value={fees} />} />
        <Stat label={<Label term="dividende">Dividendes</Label>} value={<Money value={divTotal} signed color />} />
      </div>
      <Card title="Toutes les transactions" className="[&>div]:p-0">
        {tx.length === 0 ? (
          <p className="p-8 text-center text-sm text-slate-500">Aucune transaction pour l’instant.</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full min-w-[760px]">
              <thead className="border-b border-line">
                <tr>
                  <th className="th">Date</th>
                  <th className="th">Opération</th>
                  <th className="th">Type</th>
                  <th className="th text-right">Qté</th>
                  <th className="th text-right">Prix</th>
                  <th className="th text-right">Frais</th>
                  <th className="th text-right">Total</th>
                  <th className="th text-right"><Label term="realise">P&L réalisé</Label></th>
                </tr>
              </thead>
              <tbody>
                {[...tx].reverse().map((t) => (
                  <tr key={t.id} className="border-b border-line/50 last:border-0">
                    <td className="td num text-xs text-slate-400">{fmtDate(t.day)} {fmtTime(t.tick)}</td>
                    <td className="td">
                      <span className={t.side === 'buy' ? 'text-up' : 'text-down'}>
                        {t.side === 'buy' ? (t.effect === 'close' ? 'Rachat' : 'Achat') : t.effect === 'close' ? 'Vente' : 'Vente à découvert'}
                      </span>{' '}
                      <span className="font-mono font-semibold">{t.ticker}</span>
                    </td>
                    <td className="td text-xs text-slate-400">{labelOrderType(t.orderType)}</td>
                    <td className="td num text-right">{t.qty}</td>
                    <td className="td num text-right">{fmtNum(t.price)} €</td>
                    <td className="td num text-right text-gold">{fmtNum(t.fees)} €</td>
                    <td className="td text-right"><Money value={t.side === 'buy' ? -t.total : t.total} signed /></td>
                    <td className="td text-right">{t.realizedPnl !== undefined ? <Money value={t.realizedPnl} signed color /> : <span className="text-slate-600">—</span>}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </Card>
      {dividends.length > 0 && (
        <Card title="Dividendes">
          <ul className="divide-y divide-line text-sm">
            {[...dividends].reverse().map((d, i) => (
              <li key={i} className="flex justify-between py-1.5">
                <span><span className="num text-xs text-slate-400">{fmtDate(d.day)}</span> · <span className="font-mono">{d.ticker}</span> · {Math.abs(d.qty)} × {fmtNum(d.perShare)} €</span>
                <Money value={d.amount} signed color />
              </li>
            ))}
          </ul>
        </Card>
      )}
    </div>
  );
}
