/** Calendrier fictif : uniquement des jours ouvrés, à partir du lundi 3 janvier 2033. */
const BASE = Date.UTC(2033, 0, 3);
const DAY_MS = 86_400_000;

export const DAYS_PER_WEEK = 5;
export const DAYS_PER_MONTH = 21;
export const DAYS_PER_QUARTER = 63;

export function dayToDate(day: number): Date {
  const weeks = Math.floor(day / 5);
  const rem = ((day % 5) + 5) % 5;
  return new Date(BASE + (weeks * 7 + rem) * DAY_MS);
}

/** Horodatage UNIX (secondes) pour les graphiques ; heure d'ouverture 9h00 + minutes */
export function dayToUnix(day: number, minutes = 0): number {
  return Math.floor(dayToDate(day).getTime() / 1000) + 9 * 3600 + Math.round(minutes * 60);
}

/** Le marché simulé « ouvre » à 9h00 et « ferme » à 17h30 : 510 minutes. */
export const SESSION_MINUTES = 510;
