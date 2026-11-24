/**
 * Règles de trading : frais, exécution, PRU, plus/moins-values, ordres en attente.
 * Fonctions pures, sans dépendance à React.
 */

export const STARTING_CASH = 10_000;
export const FEE_RATE = 0.005;
export const FEE_MIN = 1;
/** Garantie exigée sur une vente à découvert (150 % du montant vendu) */
export const SHORT_MARGIN = 1.5;

export const round2 = (x: number) => Math.round((x + Number.EPSILON) * 100) / 100;

/** Frais de courtage : 0,5 % du montant, avec un minimum de 1 €. */
export function computeFees(amount: number, rate = FEE_RATE, min = FEE_MIN): number {
  if (amount <= 0) return 0;
  return round2(Math.max(min, amount * rate));
}

export type Side = 'buy' | 'sell';

export interface Position {
  ticker: string;
  /** Quantité : positive = achat, négative = vente à découvert */
  qty: number;
  /** Prix moyen d'achat (ou de vente pour un short), hors frais */
  avgPrice: number;
  /** Prix de revient unitaire, frais inclus */
  pru: number;
  openedDay: number;
}

export interface Transaction {
  id: string;
  day: number;
  tick: number;
  ticker: string;
  side: Side;
  /** Ouverture / renforcement, ou réduction / clôture de position */
  effect: 'open' | 'close';
  qty: number;
  price: number;
  fees: number;
  /** Montant réglé (achat : débité ; vente : crédité) */
  total: number;
  /** P&L réalisé (uniquement pour les clôtures) */
  realizedPnl?: number;
  /** P&L réalisé en % du coût de revient */
  realizedPct?: number;
  orderType: OrderType;
  note?: string;
  /** Prix de la position au moment de la décision (pour le journal) */
  pruAtClose?: number;
}

export type OrderType = 'market' | 'limit' | 'stop' | 'takeprofit';

export interface PendingOrder {
  id: string;
  ticker: string;
  type: Exclude<OrderType, 'market'>;
  side: Side;
  qty: number;
  triggerPrice: number;
  createdDay: number;
  note?: string;
}

export interface TradeQuote {
  amount: number;
  fees: number;
  /** Total réglé : achat = montant + frais, vente = montant − frais */
  total: number;
}

export function quote(side: Side, qty: number, price: number): TradeQuote {
  const amount = round2(qty * price);
  const fees = computeFees(amount);
  return { amount, fees, total: side === 'buy' ? round2(amount + fees) : round2(amount - fees) };
}

/**
 * Ajoute des titres à une position longue.
 * PRU = (ancienne qté × ancien PRU + qté × prix + frais) / nouvelle qté
 */
export function addToLong(pos: Position | undefined, ticker: string, qty: number, price: number, fees: number, day: number): Position {
  const oldQty = pos && pos.qty > 0 ? pos.qty : 0;
  const newQty = oldQty + qty;
  const avgPrice = (oldQty * (pos?.avgPrice ?? 0) + qty * price) / newQty;
  const pru = (oldQty * (pos?.pru ?? 0) + qty * price + fees) / newQty;
  return { ticker, qty: newQty, avgPrice, pru, openedDay: pos && oldQty > 0 ? pos.openedDay : day };
}

/**
 * Vend des titres d'une position longue. Le PRU ne change pas.
 * P&L réalisé = qté × prix − frais − qté × PRU
 */
export function reduceLong(pos: Position, qty: number, price: number, fees: number): { position?: Position; realizedPnl: number } {
  if (qty > pos.qty) throw new Error('Quantité supérieure à la position');
  const realizedPnl = round2(qty * price - fees - qty * pos.pru);
  const remaining = pos.qty - qty;
  return { position: remaining > 0 ? { ...pos, qty: remaining } : undefined, realizedPnl };
}

/**
 * Vente à découvert : PRU = prix de vente net de frais (moyenne pondérée).
 */
export function addToShort(pos: Position | undefined, ticker: string, qty: number, price: number, fees: number, day: number): Position {
  const oldQty = pos && pos.qty < 0 ? -pos.qty : 0;
  const newQty = oldQty + qty;
  const avgPrice = (oldQty * (pos?.avgPrice ?? 0) + qty * price) / newQty;
  const pru = (oldQty * (pos?.pru ?? 0) + qty * price - fees) / newQty;
  return { ticker, qty: -newQty, avgPrice, pru, openedDay: pos && oldQty > 0 ? pos.openedDay : day };
}

/** Rachat d'une vente à découvert. P&L = qté × PRU − (qté × prix + frais) */
export function reduceShort(pos: Position, qty: number, price: number, fees: number): { position?: Position; realizedPnl: number } {
  if (qty > -pos.qty) throw new Error('Quantité supérieure à la position');
  const realizedPnl = round2(qty * pos.pru - qty * price - fees);
  const remaining = -pos.qty - qty;
  return { position: remaining > 0 ? { ...pos, qty: -remaining } : undefined, realizedPnl };
}

/** Plus/moins-value latente d'une position (frais d'achat inclus via le PRU). */
export function unrealizedPnl(pos: Position, price: number): number {
  return pos.qty >= 0 ? pos.qty * (price - pos.pru) : -pos.qty * (pos.pru - price);
}

export function unrealizedPct(pos: Position, price: number): number {
  if (pos.pru === 0) return 0;
  return pos.qty >= 0 ? price / pos.pru - 1 : 1 - price / pos.pru;
}

/** Valeur de marché signée (négative pour un short) */
export function marketValue(pos: Position, price: number): number {
  return pos.qty * price;
}

export interface PortfolioLike {
  cash: number;
  positions: Record<string, Position>;
}

/** Valeur totale = liquidités + valeur des positions (les shorts sont des dettes). */
export function portfolioValue(p: PortfolioLike, prices: Record<string, number>): number {
  let v = p.cash;
  for (const t in p.positions) v += marketValue(p.positions[t], prices[t] ?? 0);
  return v;
}

/** Montant immobilisé en garantie des ventes à découvert (au-delà du produit de la vente). */
export function shortCollateral(p: PortfolioLike, prices: Record<string, number>): number {
  let c = 0;
  for (const t in p.positions) {
    const pos = p.positions[t];
    if (pos.qty < 0) c += -pos.qty * (prices[t] ?? 0) * SHORT_MARGIN;
  }
  return c;
}

/** Liquidités réellement disponibles pour acheter */
export function buyingPower(p: PortfolioLike, prices: Record<string, number>): number {
  return Math.max(0, p.cash - shortCollateral(p, prices));
}

export interface ExecutionResult {
  ok: boolean;
  error?: string;
  cash: number;
  positions: Record<string, Position>;
  transaction?: Transaction;
}

/**
 * Exécute un ordre au prix donné. Gère achat, vente, vente à découvert et rachat.
 * Une position ne peut pas passer directement de longue à courte en un seul ordre.
 */
export function executeTrade(
  p: PortfolioLike,
  args: {
    id: string;
    ticker: string;
    side: Side;
    qty: number;
    price: number;
    day: number;
    tick: number;
    orderType: OrderType;
    allowShort: boolean;
    prices: Record<string, number>;
    note?: string;
  },
): ExecutionResult {
  const { ticker, side, qty, day } = args;
  const price = round2(args.price);
  const fail = (error: string): ExecutionResult => ({ ok: false, error, cash: p.cash, positions: p.positions });
  if (!Number.isInteger(qty) || qty <= 0) return fail('La quantité doit être un nombre entier positif.');

  const pos = p.positions[ticker];
  const q = quote(side, qty, price);
  const positions = { ...p.positions };
  let cash = p.cash;
  let effect: 'open' | 'close' = 'open';
  let realizedPnl: number | undefined;
  let realizedPct: number | undefined;
  let pruAtClose: number | undefined;

  if (side === 'buy') {
    if (pos && pos.qty < 0) {
      // Rachat d'un short
      if (qty > -pos.qty) return fail(`Tu ne peux racheter que ${-pos.qty} titre(s) vendus à découvert.`);
      if (q.total > p.cash) return fail('Liquidités insuffisantes.');
      const r = reduceShort(pos, qty, price, q.fees);
      effect = 'close';
      realizedPnl = r.realizedPnl;
      pruAtClose = pos.pru;
      realizedPct = r.realizedPnl / (qty * pos.pru);
      if (r.position) positions[ticker] = r.position;
      else delete positions[ticker];
    } else {
      if (q.total > buyingPower(p, args.prices) + 1e-9) return fail('Liquidités insuffisantes pour cet achat (frais compris).');
      positions[ticker] = addToLong(pos, ticker, qty, price, q.fees, day);
    }
    cash = round2(cash - q.total);
  } else {
    if (pos && pos.qty > 0) {
      if (qty > pos.qty) return fail(`Tu ne possèdes que ${pos.qty} titre(s).`);
      const r = reduceLong(pos, qty, price, q.fees);
      effect = 'close';
      realizedPnl = r.realizedPnl;
      pruAtClose = pos.pru;
      realizedPct = r.realizedPnl / (qty * pos.pru);
      if (r.position) positions[ticker] = r.position;
      else delete positions[ticker];
    } else {
      if (!args.allowShort) return fail('Tu ne possèdes pas cette action. (La vente à découvert se débloque au niveau 5.)');
      // Vente à découvert : il faut pouvoir bloquer la garantie
      const need = qty * price * SHORT_MARGIN;
      if (need > buyingPower(p, args.prices) + q.amount) return fail('Garantie insuffisante pour cette vente à découvert.');
      positions[ticker] = addToShort(pos, ticker, qty, price, q.fees, day);
    }
    cash = round2(cash + q.total);
  }

  return {
    ok: true,
    cash,
    positions,
    transaction: {
      id: args.id,
      day,
      tick: args.tick,
      ticker,
      side,
      effect,
      qty,
      price,
      fees: q.fees,
      total: q.total,
      realizedPnl,
      realizedPct,
      orderType: args.orderType,
      note: args.note?.trim() || undefined,
      pruAtClose,
    },
  };
}

/** Sens de déclenchement d'un ordre en attente */
export function triggerDirection(o: Pick<PendingOrder, 'type' | 'side'>): 'below' | 'above' {
  switch (o.type) {
    case 'limit':
      return o.side === 'buy' ? 'below' : 'above';
    case 'stop':
      return o.side === 'sell' ? 'below' : 'above';
    case 'takeprofit':
      return o.side === 'sell' ? 'above' : 'below';
  }
}

export function isTriggered(o: PendingOrder, price: number): boolean {
  return triggerDirection(o) === 'below' ? price <= o.triggerPrice : price >= o.triggerPrice;
}

/** Ordres déclenchés par les prix courants */
export function findTriggeredOrders(orders: PendingOrder[], prices: Record<string, number>): PendingOrder[] {
  return orders.filter((o) => prices[o.ticker] !== undefined && isTriggered(o, prices[o.ticker]));
}

/** Part d'une position dans le portefeuille (0..1) */
export function positionWeight(posValue: number, total: number): number {
  return total <= 0 ? 0 : Math.abs(posValue) / total;
}
