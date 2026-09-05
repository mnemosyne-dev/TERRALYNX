import React, { useState, useEffect, useRef } from 'react';
import { Search, MapPin, X, Loader2, Navigation, Compass, Globe, Crosshair, GraduationCap, Building2, Hospital, Landmark } from 'lucide-react';
import { apiService } from '../../services/api';

export interface LocationSearchResult {
  title: string;
  subtitle: string;
  category: 'university' | 'hospital' | 'city' | 'suburb' | 'locality' | string;
  category_label: string;
  lat: number;
  lng: number;
}

interface LocationSearchBarProps {
  onSelectLocation: (lat: number, lng: number, locationName: string) => void;
  isLoading?: boolean;
}

const PRESET_LOCATIONS = [
  { name: 'Bhubaneswar', lat: 20.2961, lng: 85.8245, state: 'Khordha' },
  { name: 'Cuttack', lat: 20.4625, lng: 85.8828, state: 'Millennium City' },
  { name: 'Puri Coast', lat: 19.8135, lng: 85.8312, state: 'Puri' },
  { name: 'Ganjam (Berhampur)', lat: 19.3552, lng: 85.0187, state: 'Ganjam' },
  { name: 'Balasore', lat: 21.4934, lng: 86.9135, state: 'Balasore' },
  { name: 'Kendrapara', lat: 20.5015, lng: 86.4225, state: 'Kendrapara' },
  { name: 'Mayurbhanj', lat: 21.9322, lng: 86.7389, state: 'Baripada' },
  { name: 'Sambalpur', lat: 21.4669, lng: 83.9812, state: 'Hirakud' },
  { name: 'C. V. Raman Univ', lat: 20.2198, lng: 85.7358, state: 'CVRGU' },
  { name: 'SCB Medical', lat: 20.4682, lng: 85.8895, state: 'Cuttack' },
  { name: 'CDA Sector 9', lat: 20.47937, lng: 85.82872, state: 'Cuttack' },
];

export const LocationSearchBar: React.FC<LocationSearchBarProps> = ({
  onSelectLocation,
  isLoading = false,
}) => {
  const [query, setQuery] = useState<string>('');
  const [results, setResults] = useState<LocationSearchResult[]>([]);
  const [isSearching, setIsSearching] = useState<boolean>(false);
  const [isLocating, setIsLocating] = useState<boolean>(false);
  const [isOpen, setIsOpen] = useState<boolean>(false);
  const [selectedIndex, setSelectedIndex] = useState<number>(-1);
  const dropdownRef = useRef<HTMLDivElement>(null);

  // Debounced smart search via backend unified search endpoint
  useEffect(() => {
    if (!query || query.trim().length < 2) {
      setResults([]);
      setSelectedIndex(-1);
      return;
    }

    const handler = setTimeout(async () => {
      setIsSearching(true);
      try {
        const searchResults = await apiService.searchLocations(query.trim());
        setResults(searchResults as LocationSearchResult[]);
        setIsOpen(true);
        setSelectedIndex(-1);
      } catch (e) {
        console.error('Failed to search location:', e);
      } finally {
        setIsSearching(false);
      }
    }, 150);

    return () => clearTimeout(handler);
  }, [query]);

  // Click outside to close dropdown
  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target as Node)) {
        setIsOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleSelect = (item: LocationSearchResult) => {
    setQuery(item.title);
    setIsOpen(false);
    onSelectLocation(item.lat, item.lng, `${item.title} (${item.subtitle})`);
  };

  const handleSelectPreset = (preset: typeof PRESET_LOCATIONS[0]) => {
    setQuery(preset.name);
    setIsOpen(false);
    onSelectLocation(preset.lat, preset.lng, `${preset.name}, ${preset.state}`);
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (!isOpen || results.length === 0) {
      if (e.key === 'Enter' && query.trim().length >= 2) {
        setIsSearching(true);
        apiService.searchLocations(query.trim()).then((res) => {
          setIsSearching(false);
          if (res && res.length > 0) {
            handleSelect(res[0] as LocationSearchResult);
          }
        });
      }
      return;
    }

    if (e.key === 'ArrowDown') {
      e.preventDefault();
      setSelectedIndex((prev) => (prev < results.length - 1 ? prev + 1 : 0));
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      setSelectedIndex((prev) => (prev > 0 ? prev - 1 : results.length - 1));
    } else if (e.key === 'Enter') {
      e.preventDefault();
      if (selectedIndex >= 0 && selectedIndex < results.length) {
        handleSelect(results[selectedIndex]);
      } else if (results.length > 0) {
        handleSelect(results[0]);
      }
    } else if (e.key === 'Escape') {
      setIsOpen(false);
    }
  };

  const handleDetectGPS = () => {
    if (!navigator.geolocation) {
      alert('Geolocation is not supported by your browser.');
      return;
    }
    setIsLocating(true);
    navigator.geolocation.getCurrentPosition(
      async (pos) => {
        const lat = pos.coords.latitude;
        const lng = pos.coords.longitude;
        let locName = `GPS Location (${lat.toFixed(3)}°N, ${lng.toFixed(3)}°E)`;
        try {
          const revUrl = `https://nominatim.openstreetmap.org/reverse?lat=${lat}&lon=${lng}&format=json&zoom=14`;
          const res = await fetch(revUrl, {
            headers: { 'User-Agent': 'TerraLynx-DisasterOps/2.0' },
          });
          if (res.ok) {
            const data = await res.json();
            const addr = data.address || {};
            const city = addr.suburb || addr.city || addr.town || addr.state_district || addr.county || '';
            const st = addr.state || '';
            if (city) locName = st ? `${city}, ${st}` : city;
          }
        } catch (_) {}
        setQuery(locName);
        setIsLocating(false);
        setIsOpen(false);
        onSelectLocation(lat, lng, locName);
      },
      (err) => {
        setIsLocating(false);
        alert(`Could not detect current location: ${err.message}`);
      },
      { timeout: 10000, enableHighAccuracy: true }
    );
  };

  const getCategoryIcon = (category: string) => {
    switch (category) {
      case 'district':
        return <Landmark className="w-3.5 h-3.5 text-indigo-400" />;
      case 'university':
        return <GraduationCap className="w-3.5 h-3.5 text-amber-400" />;
      case 'hospital':
        return <Hospital className="w-3.5 h-3.5 text-rose-400" />;
      case 'city':
        return <Building2 className="w-3.5 h-3.5 text-cyan-400" />;
      default:
        return <Navigation className="w-3.5 h-3.5 text-emerald-400" />;
    }
  };

  return (
    <div ref={dropdownRef} className="relative w-full max-w-lg z-30 font-sans">
      {/* Search Input Box */}
      <div className="relative flex items-center bg-[#0d1322]/95 border border-[#263553] focus-within:border-cyan-400 focus-within:ring-1 focus-within:ring-cyan-500/50 rounded-xl shadow-2xl backdrop-blur-md transition-all">
        <div className="pl-3.5 pr-2 text-cyan-400">
          {isSearching || isLoading || isLocating ? (
            <Loader2 className="w-4 h-4 animate-spin text-cyan-400" />
          ) : (
            <Search className="w-4 h-4" />
          )}
        </div>
        <input
          type="text"
          value={query}
          onChange={(e) => {
            setQuery(e.target.value);
            setIsOpen(true);
          }}
          onKeyDown={handleKeyDown}
          onFocus={() => {
            if (query.trim().length >= 2 || results.length > 0) setIsOpen(true);
          }}
          placeholder="Search University, Hospital, Sector or City (e.g. C.V. Raman, Bhubaneswar)..."
          className="w-full py-2.5 pr-16 bg-transparent text-slate-100 placeholder-slate-400 text-xs font-mono focus:outline-none"
        />

        {/* GPS Current Location Quick Button */}
        <button
          onClick={handleDetectGPS}
          disabled={isLocating}
          title="Detect my current location via GPS"
          className="p-1.5 mr-1 text-cyan-400 hover:text-cyan-300 hover:bg-cyan-950/60 rounded-lg transition-all"
        >
          <Crosshair className={`w-4 h-4 ${isLocating ? 'animate-spin' : ''}`} />
        </button>

        {query && (
          <button
            onClick={() => {
              setQuery('');
              setResults([]);
            }}
            className="pr-3 text-slate-400 hover:text-white transition-colors"
          >
            <X className="w-3.5 h-3.5" />
          </button>
        )}
      </div>

      {/* Autocomplete Dropdown */}
      {isOpen && (
        <div className="absolute top-full left-0 right-0 mt-1.5 bg-[#0b101c]/98 border border-[#263553] rounded-xl shadow-2xl overflow-hidden backdrop-blur-lg animate-in fade-in zoom-in-95 duration-100 text-xs font-mono">
          {/* Quick GPS Location Bar */}
          <button
            onClick={handleDetectGPS}
            disabled={isLocating}
            className="w-full px-3 py-2 bg-[#121c2e] hover:bg-cyan-950/90 text-cyan-300 border-b border-[#1b253b] text-left flex items-center space-x-2 transition-colors font-bold"
          >
            <Crosshair className={`w-3.5 h-3.5 text-cyan-400 ${isLocating ? 'animate-spin' : 'animate-pulse'}`} />
            <span>{isLocating ? 'Detecting GPS coordinates...' : '📍 Use My Exact Current Location'}</span>
          </button>

          {/* Quick Preset Chips */}
          <div className="p-2 border-b border-[#1b253b] bg-[#070b14]/90">
            <div className="text-[10px] text-slate-400 mb-1.5 px-1 flex items-center justify-between">
              <span>Quick Regional Presets:</span>
              <span className="text-cyan-400 flex items-center space-x-1">
                <Globe className="w-2.5 h-2.5" />
                <span>Global Coverage</span>
              </span>
            </div>
            <div className="flex flex-wrap gap-1.5">
              {PRESET_LOCATIONS.map((p) => (
                <button
                  key={p.name}
                  onClick={() => handleSelectPreset(p)}
                  className="px-2 py-0.5 rounded-md bg-[#131b2d] hover:bg-cyan-950/80 hover:text-cyan-300 text-slate-300 border border-[#212c44] text-[11px] transition-colors flex items-center space-x-1"
                >
                  <MapPin className="w-2.5 h-2.5 text-cyan-400" />
                  <span>{p.name}</span>
                </button>
              ))}
            </div>
          </div>

          {/* Search Results List */}
          {results.length > 0 ? (
            <div className="max-h-64 overflow-y-auto py-1 divide-y divide-[#151e30]">
              {results.map((item, idx) => (
                <button
                  key={idx}
                  onClick={() => handleSelect(item)}
                  className={`w-full px-3 py-2 text-left transition-colors flex items-start space-x-2.5 group ${
                    selectedIndex === idx ? 'bg-[#1a263d] border-l-2 border-cyan-400' : 'hover:bg-[#151f33]'
                  }`}
                >
                  <div className="mt-0.5 p-1 rounded bg-[#101726] border border-[#22304d] shrink-0 group-hover:border-cyan-500/50 transition-colors">
                    {getCategoryIcon(item.category)}
                  </div>
                  <div className="truncate flex-1">
                    <div className="flex items-center justify-between">
                      <div className="font-semibold text-slate-200 group-hover:text-cyan-300 transition-colors truncate text-[12px]">
                        {item.title}
                      </div>
                      <span className="text-[9px] text-slate-400 px-1.5 py-0.2 rounded bg-slate-800/80 border border-slate-700/60 ml-2 shrink-0">
                        {item.category_label || item.category}
                      </span>
                    </div>
                    <div className="text-[10px] text-slate-400 truncate mt-0.5">
                      {item.subtitle}
                    </div>
                  </div>
                </button>
              ))}
            </div>
          ) : query.trim().length >= 2 && !isSearching ? (
            <div className="p-4 text-center text-slate-400 text-xs">
              No matching locations found for "{query}".
            </div>
          ) : null}
        </div>
      )}
    </div>
  );
};
