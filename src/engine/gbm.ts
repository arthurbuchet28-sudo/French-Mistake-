/**
 * Mouvement brownien géométrique (GBM) avec corrélation marché / secteur.
 *
 *   S(t+dt) = S(t) · exp( (μ − σ²/2)·dt + σ·√dt·Z )
 *
 * μ et σ sont exprimés « par journée de bourse », dt en fraction de journée.
 * Z est un tirage normal centré réduit construit à partir de trois facteurs
 * indépendants (marché, secteur, propre à l'action) pour que les actions
 * d'un même secteur bougent partiellement ensemble.
 */
export const TICKS_PER_DAY = 60;
export const TICK_DT = 1 / TICKS_PER_DAY;

/** Part de variance expliquée par le secteur */
export const SECTOR_VARIANCE_SHARE = 0.25;
/** Part maximale de variance expliquée par le marché (pour beta = 1) */
export const MARKET_VARIANCE_SHARE = 0.45;

export function gbmStep(price: number, mu: number, sigma: number, dt: number, z: number): number {
  return price * Math.exp((mu - 0.5 * sigma * sigma) * dt + sigma * Math.sqrt(dt) * z);
}

/**
 * Combine les facteurs indépendants en un choc de variance 1.
 * corr(A, B) = √wmA·√wmB + √ws² si même secteur.
 */
export function correlatedShock(beta: number, zMarket: number, zSector: number, zIdio: number): number {
  const b = Math.min(1, Math.max(0, beta));
  const wm = MARKET_VARIANCE_SHARE * b;
  const ws = SECTOR_VARIANCE_SHARE;
  const wi = Math.max(0, 1 - wm - ws);
  return Math.sqrt(wm) * zMarket + Math.sqrt(ws) * zSector + Math.sqrt(wi) * zIdio;
}

/** Corrélation théorique entre deux actions */
export function theoreticalCorrelation(betaA: number, betaB: number, sameSector: boolean): number {
  const m = Math.sqrt(MARKET_VARIANCE_SHARE * betaA) * Math.sqrt(MARKET_VARIANCE_SHARE * betaB);
  return m + (sameSector ? SECTOR_VARIANCE_SHARE : 0);
}
