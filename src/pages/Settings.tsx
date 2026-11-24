import { useState } from 'react';
import { Card } from '../components/ui/Card';
import { Help } from '../components/ui/Help';
import { Modal } from '../components/ui/Modal';
import { Locked } from '../components/ui/Tabs';
import { FEATURE_LEVEL } from '../data/levels';
import { FEE_MIN, FEE_RATE, STARTING_CASH } from '../engine/trading';
import { useGame } from '../store/gameStore';
import { useUnlocked } from '../store/selectors';
import { fmtEur } from '../utils/format';

function Toggle({ checked, onChange, disabled }: { checked: boolean; onChange: (v: boolean) => void; disabled?: boolean }) {
  return (
    <button
      role="switch"
      aria-checked={checked}
      disabled={disabled}
      onClick={() => onChange(!checked)}
      className={`relative h-6 w-11 shrink-0 rounded-full transition disabled:opacity-40 ${checked ? 'bg-accent' : 'bg-line'}`}
    >
      <span className={`absolute top-0.5 h-5 w-5 rounded-full bg-white transition ${checked ? 'left-[22px]' : 'left-0.5'}`} />
    </button>
  );
}

export default function Settings() {
  const settings = useGame((s) => s.settings);
  const setSandbox = useGame((s) => s.setSandbox);
  const setVolatile = useGame((s) => s.setVolatile);
  const startTutorial = useGame((s) => s.startTutorial);
  const resetGame = useGame((s) => s.resetGame);
  const challenge = useGame((s) => s.challenge);
  const volatileOk = useUnlocked('volatile');
  const [confirm, setConfirm] = useState(false);

  return (
    <div className="space-y-4">
      <Card title="⚙️ Réglages">
        <ul className="divide-y divide-line">
          <li className="flex items-center gap-4 py-3">
            <div className="flex-1">
              <div className="flex items-center gap-2 font-medium text-white">
                🌪️ Mode « marché volatil » <Help term="volatil-mode" /> {!volatileOk && <Locked level={FEATURE_LEVEL.volatile} />}
              </div>
              <p className="text-sm text-slate-400">Les cours bougent 1,8 fois plus fort, comme en période de crise.</p>
            </div>
            <Toggle checked={settings.volatileMode} disabled={!volatileOk} onChange={setVolatile} />
          </li>
          <li className="flex items-center gap-4 py-3">
            <div className="flex-1">
              <div className="font-medium text-white">🧪 Mode bac à sable</div>
              <p className="text-sm text-slate-400">Débloque immédiatement tous les outils (stop-loss, ordres limites, indicateurs, statistiques avancées, vente à découvert) pour explorer librement. Les niveaux et missions continuent de fonctionner.</p>
            </div>
            <Toggle checked={settings.sandbox} onChange={setSandbox} />
          </li>
          <li className="flex items-center gap-4 py-3">
            <div className="flex-1">
              <div className="font-medium text-white">❔ Tutoriel</div>
              <p className="text-sm text-slate-400">Revoir la visite guidée de l’application.</p>
            </div>
            <button className="btn-ghost" onClick={startTutorial}>Relancer</button>
          </li>
          <li className="flex items-center gap-4 py-3">
            <div className="flex-1">
              <div className="font-medium text-white">🔄 Réinitialiser la partie</div>
              <p className="text-sm text-slate-400">Nouveau marché, {fmtEur(STARTING_CASH)} de capital, niveau 1. Toute la progression est effacée.</p>
            </div>
            <button className="btn-sell" onClick={() => setConfirm(true)}>Réinitialiser</button>
          </li>
        </ul>
      </Card>

      <Card title="ℹ️ À propos de la simulation">
        <ul className="list-disc space-y-1.5 pl-5 text-sm text-slate-300">
          <li>Toutes les entreprises, actualités, cours et montants sont <strong>fictifs</strong>. Aucune donnée réelle, aucun courtier, aucun appel réseau.</li>
          <li>Les prix suivent un mouvement brownien géométrique, avec une corrélation par secteur et par rapport au marché.</li>
          <li>1 tick = 1 seconde à vitesse x1 ; 1 journée de bourse = 60 ticks ; 1 semaine = 5 journées ; 1 mois = 21 journées.</li>
          <li>Frais de courtage : {(FEE_RATE * 100).toString().replace('.', ',')} % du montant, minimum {fmtEur(FEE_MIN)} par ordre.</li>
          <li>Dividendes trimestriels (tous les 63 jours de bourse) pour les entreprises qui en versent.</li>
          <li>La partie est sauvegardée automatiquement dans ton navigateur (localStorage).</li>
        </ul>
      </Card>

      <Modal open={confirm} onClose={() => setConfirm(false)} title="Réinitialiser la partie ?">
        <p className="text-sm text-slate-300">
          Ton portefeuille, ton historique, ton journal, tes niveaux et tes badges seront effacés. {challenge && 'Le défi en cours sera aussi abandonné. '}Cette action est irréversible.
        </p>
        <div className="mt-4 flex gap-2">
          <button className="btn-ghost flex-1" onClick={() => setConfirm(false)}>Annuler</button>
          <button
            className="btn-sell flex-1"
            onClick={() => {
              resetGame();
              setConfirm(false);
            }}
          >
            Oui, tout effacer
          </button>
        </div>
      </Modal>
    </div>
  );
}
