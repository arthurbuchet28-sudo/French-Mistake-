import { HashRouter, Navigate, Route, Routes, useLocation } from 'react-router-dom';
import { lazy, Suspense, useEffect } from 'react';
import { Header } from './components/layout/Header';
import { MobileNav, SideNav } from './components/layout/Nav';
import { SimulationBanner } from './components/layout/SimulationBanner';
import { Toasts } from './components/layout/Toasts';
import { TutorialOverlay } from './components/onboarding/TutorialOverlay';
import { GlobalModals } from './components/progression/GlobalModals';
import { useGameLoop } from './store/useGameLoop';
// Chaque page est chargée à la demande pour alléger le premier affichage
const Dashboard = lazy(() => import('./pages/Dashboard'));
const Market = lazy(() => import('./pages/Market'));
const StockDetail = lazy(() => import('./pages/StockDetail'));
const Portfolio = lazy(() => import('./pages/Portfolio'));
const History = lazy(() => import('./pages/History'));
const Journal = lazy(() => import('./pages/Journal'));
const Stats = lazy(() => import('./pages/Stats'));
const Glossary = lazy(() => import('./pages/Glossary'));
const Progression = lazy(() => import('./pages/Progression'));
const Settings = lazy(() => import('./pages/Settings'));

function Loading() {
  return <div className="py-16 text-center text-sm text-slate-500">Chargement…</div>;
}

function ScrollTop() {
  const { pathname } = useLocation();
  useEffect(() => {
    window.scrollTo(0, 0);
  }, [pathname]);
  return null;
}

function Shell() {
  useGameLoop();
  return (
    <div className="min-h-screen pb-12">
      <Header />
      <ScrollTop />
      <div className="mx-auto flex max-w-7xl gap-6 px-3 pt-0 sm:px-4 md:pt-4">
        <SideNav />
        <main className="min-w-0 flex-1">
          <MobileNav />
          <Suspense fallback={<Loading />}>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/marche" element={<Market />} />
            <Route path="/action/:ticker" element={<StockDetail />} />
            <Route path="/portefeuille" element={<Portfolio />} />
            <Route path="/historique" element={<History />} />
            <Route path="/journal" element={<Journal />} />
            <Route path="/statistiques" element={<Stats />} />
            <Route path="/glossaire" element={<Glossary />} />
            <Route path="/progression" element={<Progression />} />
            <Route path="/reglages" element={<Settings />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
          </Suspense>
        </main>
      </div>
      <GlobalModals />
      <TutorialOverlay />
      <Toasts />
      <SimulationBanner />
    </div>
  );
}

export default function App() {
  return (
    <HashRouter future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
      <Shell />
    </HashRouter>
  );
}
