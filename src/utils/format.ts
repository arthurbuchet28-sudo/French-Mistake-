import { dayToDate, SESSION_MINUTES } from '../engine/calendar';
import { TICKS_PER_DAY } from '../engine/gbm';

const eur = new Intl.NumberFormat('fr-FR', { style: 'currency', currency: 'EUR', minimumFractionDigits: 2, maximumFractionDigits: 2 });
const num2 = new Intl.NumberFormat('fr-FR', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
const int = new Intl.NumberFormat('fr-FR', { maximumFractionDigits: 0 });

/** 1 234,56 € */
export const fmtEur = (x: number) => eur.format(x).replace(/ /g, ' ');
/** +1 234,56 € / −12,30 € */
export const fmtEurSigned = (x: number) => (x > 0 ? '+' : x < 0 ? '−' : '') + fmtEur(Math.abs(x));
export const fmtNum = (x: number) => num2.format(x).replace(/ /g, ' ');
export const fmtInt = (x: number) => int.format(x).replace(/ /g, ' ');
/** +1,23 % */
export const fmtPct = (x: number, digits = 2) =>
  (x > 0 ? '+' : x < 0 ? '−' : '') + Math.abs(x * 100).toFixed(digits).replace('.', ',') + ' %';
export const fmtPctPlain = (x: number, digits = 1) => (x * 100).toFixed(digits).replace('.', ',') + ' %';

/** JJ/MM/AAAA */
export function fmtDate(day: number): string {
  const d = dayToDate(day);
  const dd = String(d.getUTCDate()).padStart(2, '0');
  const mm = String(d.getUTCMonth() + 1).padStart(2, '0');
  return `${dd}/${mm}/${d.getUTCFullYear()}`;
}

const WEEKDAYS = ['dim.', 'lun.', 'mar.', 'mer.', 'jeu.', 'ven.', 'sam.'];
export function fmtWeekday(day: number): string {
  return WEEKDAYS[dayToDate(day).getUTCDay()];
}

/** Heure simulée à partir du tick (séance 9h00–17h30) */
export function fmtTime(tick: number): string {
  const minutes = 9 * 60 + Math.round((tick / TICKS_PER_DAY) * SESSION_MINUTES);
  return `${String(Math.floor(minutes / 60)).padStart(2, '0')}h${String(minutes % 60).padStart(2, '0')}`;
}

export const colorFor = (x: number) => (x > 0 ? 'text-up' : x < 0 ? 'text-down' : 'text-slate-400');
