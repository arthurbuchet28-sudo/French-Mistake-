import { NavLink } from 'react-router-dom';

export const NAV = [
  { to: '/', label: 'Tableau de bord', short: 'Accueil', icon: '🏠' },
  { to: '/marche', label: 'Marché', short: 'Marché', icon: '📈' },
  { to: '/portefeuille', label: 'Portefeuille', short: 'Portef.', icon: '💼' },
  { to: '/historique', label: 'Historique', short: 'Histo.', icon: '🧾' },
  { to: '/journal', label: 'Journal', short: 'Journal', icon: '📓' },
  { to: '/statistiques', label: 'Statistiques', short: 'Stats', icon: '📊' },
  { to: '/progression', label: 'Progression', short: 'Missions', icon: '🎯' },
  { to: '/glossaire', label: 'Glossaire', short: 'Glossaire', icon: '📖' },
  { to: '/reglages', label: 'Réglages', short: 'Réglages', icon: '⚙️' },
];

export function SideNav() {
  return (
    <nav className="sticky top-16 hidden h-fit w-52 shrink-0 flex-col gap-0.5 md:flex">
      {NAV.map((n) => (
        <NavLink
          key={n.to}
          to={n.to}
          end={n.to === '/'}
          className={({ isActive }) =>
            `flex items-center gap-2.5 rounded-lg px-3 py-2 text-sm transition ${isActive ? 'bg-panel2 text-white' : 'text-slate-400 hover:bg-panel hover:text-slate-200'}`
          }
        >
          <span>{n.icon}</span>
          {n.label}
        </NavLink>
      ))}
    </nav>
  );
}

export function MobileNav() {
  return (
    <nav className="-mx-3 mb-3 flex gap-1 overflow-x-auto border-b border-line bg-bg/95 px-3 py-2 backdrop-blur md:hidden">
      {NAV.map((n) => (
        <NavLink
          key={n.to}
          to={n.to}
          end={n.to === '/'}
          className={({ isActive }) => `chip shrink-0 whitespace-nowrap ${isActive ? 'border-accent bg-accent/15 text-white' : 'text-slate-400'}`}
        >
          {n.icon} {n.short}
        </NavLink>
      ))}
    </nav>
  );
}
