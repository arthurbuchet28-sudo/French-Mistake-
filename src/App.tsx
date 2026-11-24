import { HashRouter, Navigate, Route, Routes, useLocation } from 'react-router-dom';
import { useEffect } from 'react';
import { Header } from './components/layout/Header';
import { MobileNav, SideNav } from './components/layout/Nav';
import { SimulationBanner } from './components/layout/SimulationBanner';
import { Toasts } from './components/layout/Toasts';
import { TutorialOverlay } from './components/onboarding/TutorialOverlay';
import { GlobalModals } from './components/progression/GlobalModals';
import { useGameLoop } from './store/useGameLoop';
import Dashboard from './pages/Dashboard';
import Market from './pages/Market';
import StockDetail from './pages/StockDetail';
import Portfolio from './pages/Portfolio';
import History from './pages/History';
import Journal from './pages/Journal';
import Stats from './pages/Stats';
import Glossary from './pages/Glossary';
import Progression from './pages/Progression';
import Settings from './pages/Settings';

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
