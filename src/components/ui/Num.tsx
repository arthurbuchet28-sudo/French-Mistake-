import { colorFor, fmtEur, fmtEurSigned, fmtPct } from '../../utils/format';

export function Money({ value, signed = false, color = false, className = '' }: { value: number; signed?: boolean; color?: boolean; className?: string }) {
  return <span className={`num ${color ? colorFor(value) : ''} ${className}`}>{signed ? fmtEurSigned(value) : fmtEur(value)}</span>;
}

export function Pct({ value, className = '', digits = 2 }: { value: number; className?: string; digits?: number }) {
  return <span className={`num ${colorFor(value)} ${className}`}>{fmtPct(value, digits)}</span>;
}

export function Arrow({ value }: { value: number }) {
  return <span className={colorFor(value)}>{value > 0 ? '▲' : value < 0 ? '▼' : '•'}</span>;
}
