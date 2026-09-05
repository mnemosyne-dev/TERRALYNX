import React, { useState, useEffect } from 'react';
import { Shield, AlertTriangle, RefreshCw, Radio, Compass, CloudRain, Wind, Navigation as NavigationIcon, MapPin, Crosshair } from 'lucide-react';
import { DistrictState } from '../../types';

interface HeaderProps {
  state: DistrictState | null;
  onResetSimulation: () => void;
  onFetchLiveWeather: () => void;
  onDetectCurrentLocation?: () => void;
  isSimulating: boolean;
  isLiveFeed: boolean;
}

export const Header: React.FC<HeaderProps> = ({
  state,
  onResetSimulation,
  onFetchLiveWeather,
  onDetectCurrentLocation,
  isSimulating,
  isLiveFeed,
}) => {
  const [time, setTime] = useState<string>('');

useEffect(() => {
    const updateTime = () => {
      const now = new Date();
      setTime(
        now.toLocaleTimeString('en-IN', {
          timeZone: 'Asia/Kolkata',
          hour12: false,
          hour: '2-digit',
          minute: '2-digit',
          second: '2-digit'
        }) + ' IST'
      );
    };
    updateTime();
    const interval = setInterval(updateTime, 1000);
    return () => clearInterval(interval);
  }, []);

  const isSimulationActive = state?.simulation_diff?.is_simulation_active;
  const isCyclone = (state?.hazard?.category || 0) >= 1;
  const activeDistrictName = state?.hazard?.name
    ? state.hazard.name.replace('Live Weather (', '').replace(')', '')
    : 'Purva Coastal District';

  const windDirDeg = state?.hazard?.wind_direction_deg || 135;

  return (
    <header className="bg-[#0e131f] border-b border-[#1f293d] px-4 py-2.5 flex items-center justify-between sticky top-0 z-50">
      {/* Brand & Platform Identity */}
      <div className="flex items-center space-x-3">
        <div className="relative flex items-center justify-center w-10 h-10 rounded-lg bg-cyan-950 border border-cyan-500/40 text-cyan-400 shadow-inner">
          <Shield className="w-5 h-5" />
          <span className="absolute -top-1 -right-1 flex h-2.5 w-2.5">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-red-500"></span>
          </span>
        </div>
        <div>
          <div className="flex items-center space-x-2">
            <h1 className="text-lg font-bold tracking-wider text-slate-100 font-mono">
              TERRA<span className="text-cyan-400">LYNX</span>
            </h1>
            <span className="px-1.5 py-0.5 text-[10px] font-semibold tracking-wider uppercase rounded bg-cyan-950/80 text-cyan-300 border border-cyan-800/60">
              Ops Command
            </span>
          </div>
          <p className="text-[11px] text-slate-400 font-sans tracking-wide">
            Predict. Prepare. Protect. — Decision Intelligence
          </p>
        </div>
      </div>

      {/* Dynamic Active Threat Center Pill with Wind Compass */}
      {state && (
        <div className="hidden lg:flex items-center space-x-3 bg-[#141b2a] border border-[#232f48] rounded-full px-4 py-1.5 text-xs shadow-lg">
          <div
            className={`flex items-center space-x-1.5 font-semibold font-mono ${
              isCyclone ? 'text-red-400' : 'text-cyan-300'
            }`}
          >
            <Radio
              className={`w-3.5 h-3.5 animate-pulse ${
                isCyclone ? 'text-red-500' : 'text-cyan-400'
              }`}
            />
            <span className="truncate max-w-[240px]">
              {isCyclone
                ? `${state.hazard.name.toUpperCase()} (CAT-${state.hazard.category})`
                : `${state.hazard.name.toUpperCase()}`}
            </span>
          </div>

          <span className="text-slate-600">|</span>

          {/* Real Wind Vector & Compass Arrow */}
          <div className="text-slate-200 flex items-center space-x-1.5">
            <Wind className="w-3.5 h-3.5 text-cyan-400" />
            <span className="text-slate-400 font-mono">Wind:</span>
            <span className="font-mono text-cyan-300 font-bold">
              {state.hazard.wind_speed_kmh} km/h
            </span>
            <div className="flex items-center space-x-1 pl-1 border-l border-slate-700">
              <NavigationIcon
                className="w-3 h-3 text-amber-400 transition-transform duration-500"
                style={{ transform: `rotate(${windDirDeg}deg)` }}
              />
              <span className="font-mono text-amber-300 font-semibold text-[11px]">
                {windDirDeg}° ({state.hazard.movement_direction})
              </span>
            </div>
            <span className="text-slate-400 font-mono text-[10px] pl-1">
              (Gusts: <span className="text-amber-400 font-semibold">{state.hazard.wind_gusts_kmh}</span>)
            </span>
          </div>

          <span className="text-slate-600">|</span>

          <div className="text-slate-300 flex items-center space-x-1">
            <CloudRain className="w-3.5 h-3.5 text-cyan-400" />
            <span className="text-slate-400 font-mono">Rain 24h:</span>
            <span className="font-mono text-cyan-400 font-bold">
              {state.hazard.total_24h_rainfall_mm}mm
            </span>
          </div>
        </div>
      )}

      {/* Right Controls & Simulation State */}
      <div className="flex items-center space-x-2.5">
        {/* Detect Current Location GPS Button */}
        {onDetectCurrentLocation && (
          <button
            onClick={onDetectCurrentLocation}
            disabled={isSimulating}
            className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg font-mono text-xs bg-[#141b2a] hover:bg-cyan-950/80 text-cyan-300 hover:text-cyan-200 border border-cyan-700/60 hover:border-cyan-400 shadow-md transition-all active:scale-95"
            title="Auto-detect current GPS location and fetch live weather & risk sectors"
          >
            <Crosshair className="w-3.5 h-3.5 text-cyan-400 animate-pulse" />
            <span className="font-bold hidden sm:inline">MY LOCATION</span>
          </button>
        )}

        {/* Live Open-Meteo Feed Trigger */}
        <button
          onClick={onFetchLiveWeather}
          disabled={isSimulating}
          className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-lg font-mono text-xs transition-all shadow-md active:scale-95 ${
            isLiveFeed
              ? 'bg-emerald-950 text-emerald-300 border border-emerald-500 ring-1 ring-emerald-500/40'
              : 'bg-[#141b2a] hover:bg-emerald-950/80 text-slate-200 hover:text-emerald-300 border border-emerald-700/60 hover:border-emerald-500'
          }`}
          title="Fetch live atmospheric, precipitation and wind data from Open-Meteo API"
        >
          {isSimulating ? (
            <RefreshCw className="w-3 h-3 text-emerald-400 animate-spin" />
          ) : (
            <span
              className={`h-2 w-2 rounded-full ${
                isLiveFeed ? 'bg-emerald-400 animate-ping' : 'bg-emerald-400'
              }`}
            ></span>
          )}
          <span className="font-bold">
            {isSimulating
              ? 'FETCHING...'
              : isLiveFeed
              ? 'LIVE FEED'
              : '⚡ LIVE FEED'}
          </span>
        </button>

        {isSimulationActive && (
          <div className="flex items-center space-x-2 bg-amber-950/60 border border-amber-600/50 rounded-lg px-2.5 py-1">
            <AlertTriangle className="w-3.5 h-3.5 text-amber-400 animate-bounce" />
            <span className="text-xs font-mono font-medium text-amber-300">
              WHAT-IF
            </span>
            <button
              onClick={onResetSimulation}
              disabled={isSimulating}
              className="text-[11px] bg-amber-500/20 hover:bg-amber-500/30 text-amber-200 px-2 py-0.5 rounded border border-amber-500/40 flex items-center space-x-1 transition-colors"
              title="Reset simulation parameters to baseline"
            >
              <RefreshCw className="w-3 h-3" />
              <span>Reset</span>
            </button>
          </div>
        )}

        {/* Operational Clock & Dynamic District Name */}
        <div className="hidden sm:flex flex-col items-end text-right">
          <span className="font-mono text-xs text-cyan-400 font-semibold tracking-wider">
            {time}
          </span>
          <span className="text-[10px] text-slate-400 flex items-center space-x-1 truncate max-w-[160px]">
            <Compass className="w-3 h-3 text-slate-400 shrink-0" />
            <span className="truncate">{activeDistrictName}</span>
          </span>
        </div>
      </div>
    </header>
  );
};
