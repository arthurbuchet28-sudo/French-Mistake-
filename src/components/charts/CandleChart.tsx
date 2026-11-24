import { useEffect, useMemo, useRef } from 'react';
import {
  ColorType,
  createChart,
  CrosshairMode,
  type IChartApi,
  type ISeriesApi,
  type UTCTimestamp,
} from 'lightweight-charts';
import { dayToUnix, SESSION_MINUTES } from '../../engine/calendar';
import { TICKS_PER_DAY } from '../../engine/gbm';
import { aggregateTicks, sma } from '../../engine/indicators';
import type { Candle, StockState } from '../../engine/types';
import { fmtNum } from '../../utils/format';

export type Timeframe = '1J' | '1S' | '1M' | '6M';
const TF_DAYS: Record<Exclude<Timeframe, '1J'>, number> = { '1S': 5, '1M': 21, '6M': 126 };
const UP = '#22c55e';
const DOWN = '#ef4444';

interface Props {
  stock: Pick<StockState, 'candles' | 'intraday' | 'dayOpen' | 'dayHigh' | 'dayLow' | 'price' | 'dayVolume'>;
  day: number;
  timeframe: Timeframe;
  showMA: boolean;
  showVolume: boolean;
  height?: number;
}

interface Bar {
  time: UTCTimestamp;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
}

function buildBars(p: Props): { bars: Bar[]; ma20: (number | null)[]; ma50: (number | null)[] } {
  const { stock, day, timeframe } = p;
  if (timeframe === '1J') {
    const size = 3;
    const candles: Candle[] = aggregateTicks(stock.intraday, size);
    const perTickVol = stock.intraday.length > 1 ? stock.dayVolume / (stock.intraday.length - 1) : 0;
    const bars = candles.map((c) => ({
      time: dayToUnix(day, ((c.t - 1) / TICKS_PER_DAY) * SESSION_MINUTES) as UTCTimestamp,
      open: c.o,
      high: c.h,
      low: c.l,
      close: c.c,
      volume: perTickVol * size,
    }));
    const closes = bars.map((b) => b.close);
    return { bars, ma20: sma(closes, 20), ma50: sma(closes, 50) };
  }
  // Journalier : historique + bougie du jour en cours
  const all: Candle[] = [...stock.candles];
  if (stock.intraday.length > 1) all.push({ t: day, o: stock.dayOpen, h: stock.dayHigh, l: stock.dayLow, c: stock.price, v: stock.dayVolume });
  const closes = all.map((c) => c.c);
  const ma20 = sma(closes, 20);
  const ma50 = sma(closes, 50);
  const n = TF_DAYS[timeframe];
  const from = Math.max(0, all.length - n);
  return {
    bars: all.slice(from).map((c) => ({ time: dayToUnix(c.t) as UTCTimestamp, open: c.o, high: c.h, low: c.l, close: c.c, volume: c.v })),
    ma20: ma20.slice(from),
    ma50: ma50.slice(from),
  };
}

export function CandleChart(props: Props) {
  const { timeframe, showMA, showVolume, height = 360 } = props;
  const el = useRef<HTMLDivElement>(null);
  const chart = useRef<IChartApi | null>(null);
  const series = useRef<{
    candle: ISeriesApi<'Candlestick'>;
    vol: ISeriesApi<'Histogram'>;
    ma20: ISeriesApi<'Line'>;
    ma50: ISeriesApi<'Line'>;
  } | null>(null);

  // Création du graphique
  useEffect(() => {
    if (!el.current) return;
    const c = createChart(el.current, {
      height,
      autoSize: true,
      layout: { background: { type: ColorType.Solid, color: 'transparent' }, textColor: '#94a3b8', fontFamily: 'JetBrains Mono, monospace' },
      grid: { vertLines: { color: '#1a2336' }, horzLines: { color: '#1a2336' } },
      rightPriceScale: { borderColor: '#243049' },
      timeScale: { borderColor: '#243049', rightOffset: 2 },
      crosshair: { mode: CrosshairMode.Normal },
      localization: {
        locale: 'fr-FR',
        priceFormatter: (p: number) => fmtNum(p),
      },
    });
    const candle = c.addCandlestickSeries({ upColor: UP, downColor: DOWN, borderUpColor: UP, borderDownColor: DOWN, wickUpColor: UP, wickDownColor: DOWN });
    const vol = c.addHistogramSeries({ priceScaleId: 'vol', priceFormat: { type: 'volume' }, lastValueVisible: false, priceLineVisible: false });
    c.priceScale('vol').applyOptions({ scaleMargins: { top: 0.8, bottom: 0 } });
    const ma20 = c.addLineSeries({ color: '#f59e0b', lineWidth: 2, lastValueVisible: false, priceLineVisible: false, crosshairMarkerVisible: false });
    const ma50 = c.addLineSeries({ color: '#a78bfa', lineWidth: 2, lastValueVisible: false, priceLineVisible: false, crosshairMarkerVisible: false });
    chart.current = c;
    series.current = { candle, vol, ma20, ma50 };
    return () => {
      c.remove();
      chart.current = null;
      series.current = null;
    };
  }, [height]);

  const data = useMemo(() => buildBars(props), [props.stock, props.day, props.timeframe]); // eslint-disable-line react-hooks/exhaustive-deps

  // Mise à jour des données
  useEffect(() => {
    const s = series.current;
    const c = chart.current;
    if (!s || !c) return;
    s.candle.setData(data.bars.map(({ time, open, high, low, close }) => ({ time, open, high, low, close })));
    s.vol.setData(showVolume ? data.bars.map((b) => ({ time: b.time, value: b.volume, color: b.close >= b.open ? 'rgba(34,197,94,0.35)' : 'rgba(239,68,68,0.35)' })) : []);
    const line = (arr: (number | null)[]) =>
      showMA ? data.bars.map((b, i) => (arr[i] === null ? { time: b.time } : { time: b.time, value: arr[i] as number })) : [];
    s.ma20.setData(line(data.ma20));
    s.ma50.setData(line(data.ma50));
    c.applyOptions({
      timeScale: { timeVisible: timeframe === '1J', secondsVisible: false },
      localization: {
        locale: 'fr-FR',
        priceFormatter: (p: number) => fmtNum(p),
        timeFormatter: (t: number) => {
          const d = new Date(t * 1000);
          const date = `${String(d.getUTCDate()).padStart(2, '0')}/${String(d.getUTCMonth() + 1).padStart(2, '0')}/${d.getUTCFullYear()}`;
          return timeframe === '1J' ? `${date} ${String(d.getUTCHours()).padStart(2, '0')}h${String(d.getUTCMinutes()).padStart(2, '0')}` : date;
        },
      },
    });
  }, [data, showMA, showVolume, timeframe]);

  // Recadrer quand on change de période
  useEffect(() => {
    chart.current?.timeScale().fitContent();
  }, [timeframe, data.bars.length]);

  return (
    <div className="relative" data-tour="candle-chart">
      <div ref={el} style={{ height }} />
      {data.bars.length === 0 && (
        <div className="absolute inset-0 flex items-center justify-center text-sm text-slate-500">Ouverture de la séance… les premières bougies arrivent.</div>
      )}
      {showMA && (
        <div className="pointer-events-none absolute left-2 top-1 flex gap-3 text-[11px]">
          <span className="text-amber-500">— MM20</span>
          <span className="text-violet-400">— MM50</span>
        </div>
      )}
    </div>
  );
}

