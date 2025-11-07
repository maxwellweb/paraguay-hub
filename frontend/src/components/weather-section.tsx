import type React from "react"

import { useState, useEffect, useCallback } from "react"
import { useApiFetch } from "@/hooks/useApiFetch"
import { Card } from "@/components/ui/card"
import { Cloud, CloudRain, Sun, Moon, CloudSnow, Wind, MapPin, RefreshCw } from "lucide-react"

interface WeatherAPIResponse {
  department: string 
  temp_celsius: number
  description: string // Ej: "cielo claro"
  humidity: number
  wind_speed_kmh: number
}

const PARAGUAY_CITIES = [
  { value: "asuncion", label: "Asunción" },
  { value: "san-lorenzo", label: "San Lorenzo" },
  { value: "ciudad-del-este", label: "Ciudad del Este" },
  { value: "encarnacion", label: "Encarnación" },
  { value: "pedro-juan-caballero", label: "Pedro Juan Caballero" },
  { value: "concepcion", label: "Concepción" },
  { value: "villarrica", label: "Villarrica" },
  { value: "coronel-oviedo", label: "Coronel Oviedo" },
  { value: "caaguazu", label: "Caaguazú" },
]

const CITY_TO_ENDPOINT_KEY: Record<string, string> = {
    "asuncion": "ASUNCION",
    "ciudad-del-este": "ALTO_PARANA",
    "encarnacion": "ITAPUA",
    "san-lorenzo": "CENTRAL", 
    "pedro-juan-caballero": "CENTRAL", 
    "concepcion": "CENTRAL", 
    "villarrica": "CENTRAL", 
    "coronel-oviedo": "CENTRAL", 
    "caaguazu": "CENTRAL", 
};

export default function WeatherSection() {
  const [selectedCity, setSelectedCity] = useState(PARAGUAY_CITIES[0].value)
  const [isDay, setIsDay] = useState(true)

  const { data, loading, error, executeRequest } = useApiFetch<WeatherAPIResponse>();

  const fetchWeather = useCallback((cityValue: string) => {
    const departmentKey = CITY_TO_ENDPOINT_KEY[cityValue] || "ASUNCION";
    const endpoint = `/weather/${departmentKey}`;
    
    // 💡 Ejecutamos la solicitud GET
    executeRequest('GET', endpoint);
  }, [executeRequest]); // Solo depende de executeRequest


  useEffect(() => {
    const hour = new Date().getHours()
    setIsDay(hour >= 6 && hour < 20)
    fetchWeather(selectedCity)
  }, [fetchWeather, selectedCity])



  const currentDescription = data?.description?.toLowerCase() || 'cielo claro';

  const handleCityChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const newCity = e.target.value;
    setSelectedCity(newCity);
    // 💡 Llamamos inmediatamente a fetchWeather para cargar los datos de la nueva ciudad
    fetchWeather(newCity); 
  }

  // Define los datos finales usados en el renderizado
  const weatherData = {
    temp_celsius: data?.temp_celsius ? Math.round(data.temp_celsius) : 'N/D',
    description: currentDescription,
    // Usamos el nombre formal del departamento de la API, o el label de la ciudad como fallback
    department: data?.department || PARAGUAY_CITIES.find(c => c.value === selectedCity)?.label || 'Cargando',
    humidity: data?.humidity || 'N/D',
    wind_speed_kmh: data?.wind_speed_kmh ? Math.round(data.wind_speed_kmh) : 'N/D',
    isDay: isDay,
  };

  const getWeatherIcon = () => {
    const iconClass = `w-24 h-24 md:w-32 md:h-32 transition-transform duration-500 ${loading ? 'animate-spin-slow opacity-50' : 'animate-float'}`

    if (loading) return <Cloud className={iconClass} />;

    if (!weatherData.isDay) {
      return <Moon className={iconClass} />
    }
    switch (weatherData.description) {
      case "cielo claro":
        return <Sun className={iconClass} />
      case "nubes dispersas":
        return <Cloud className={iconClass} />
      case "nubes":
        return <Cloud className={iconClass} />
      case "nubes altas":
        return <Cloud className={iconClass} />
      case "muy nuboso":
        return <Cloud className={iconClass} />
      case "lluvia":
        return <CloudRain className={iconClass} />
      case "nieve":
        return <CloudSnow className={iconClass} />
      case "ventoso":
        return <Wind className={iconClass} />
      default:
        return <Sun className={iconClass} />
    }
  }

  const getBackgroundClass = () => {
    if (loading) return "bg-gradient-to-br from-slate-100 via-slate-200 to-slate-300"

    if (!weatherData.isDay) {
      return "bg-gradient-to-br from-indigo-900 via-purple-900 to-slate-900"
    }
    
    if (currentDescription === "cielo claro") {
      return "bg-gradient-to-br from-amber-300 via-orange-300 to-yellow-400"
    }
    
    if (currentDescription === "nublado" || currentDescription === "nubes dispersas" || currentDescription === "nubes" || currentDescription === "nubes altas" || currentDescription === "muy nuboso") {
      return "bg-gradient-to-br from-slate-300 via-gray-300 to-slate-400"
    }
    
    if (currentDescription === "lluvia" || currentDescription === "lluvias") {
      return "bg-gradient-to-br from-slate-500 via-blue-400 to-slate-600"
    }
    
    if (currentDescription === "nieve" || currentDescription === "nieves") {
      return "bg-gradient-to-br from-blue-200 via-slate-200 to-blue-300"
    }
    
    if (currentDescription === "ventoso" || currentDescription === "ventos") {
      return "bg-gradient-to-br from-teal-300 via-cyan-300 to-sky-400"
    }
    
    return "bg-gradient-to-br from-amber-300 via-orange-300 to-sky-400"
  }

  const getTextColor = () => {
    return weatherData.isDay ? "text-slate-900" : "text-white"
  }

  return (
    <section
      className={`min-h-screen flex items-center justify-center p-4 md:p-8 transition-all duration-1000 ${getBackgroundClass()}`}
    >
      <div className="container max-w-6xl">
        <div className="text-center mb-8">
          <h1 className={`text-4xl md:text-6xl font-bold mb-4 ${getTextColor()}`}>Clima en Paraguay</h1>
          <p className={`text-lg md:text-xl ${getTextColor()} opacity-90`}>Información meteorológica en tiempo real</p>
        </div>

        <Card
          className={`p-8 md:p-12 backdrop-blur-sm ${weatherData.isDay ? "bg-white/80" : "bg-slate-800/80"} border-none shadow-2xl`}
        >
          <div className="grid md:grid-cols-2 gap-8 items-center">
            <div className="flex justify-center">
              <div className={weatherData.isDay ? "text-amber-500" : "text-blue-300"}>{getWeatherIcon()}</div>
            </div>

            <div className="space-y-6">

              {loading && <p className={`text-2xl animate-pulse ${getTextColor()}`}>Consultando el cielo...</p>}
              {error && <p className="text-red-400 font-semibold">Error de conexión: {error}</p>}             

              <div>
                <h2
                  className={`text-5xl md:text-7xl font-bold mb-2 ${weatherData.isDay ? "text-slate-900" : "text-white"}`}
                >
                  {weatherData.temp_celsius}°C
                </h2>
                <p className={`text-xl md:text-2xl ${weatherData.isDay ? "text-slate-700" : "text-slate-300"} capitalize`}>
                  {weatherData.description}
                </p>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className={`p-4 rounded-lg ${weatherData.isDay ? "bg-slate-100" : "bg-slate-700"}`}>
                  <p className={`text-sm ${weatherData.isDay ? "text-slate-600" : "text-slate-400"} mb-1`}>Humedad</p>
                  <p className={`text-2xl font-bold ${weatherData.isDay ? "text-slate-900" : "text-white"}`}>
                    {weatherData.humidity}%
                  </p>
                </div>
                <div className={`p-4 rounded-lg ${weatherData.isDay ? "bg-slate-100" : "bg-slate-700"}`}>
                  <p className={`text-sm ${weatherData.isDay ? "text-slate-600" : "text-slate-400"} mb-1`}>Viento</p>
                  <p className={`text-2xl font-bold ${weatherData.isDay ? "text-slate-900" : "text-white"}`}>
                    {weatherData.wind_speed_kmh} km/h
                  </p>
                </div>
              </div>

              <div className={`p-4 rounded-lg ${weatherData.isDay ? "bg-primary/20" : "bg-secondary/20"} relative`}>
                <div className="flex items-center gap-2">
                  <MapPin className={`w-5 h-5 ${weatherData.isDay ? "text-slate-900" : "text-white"}`} />
                  <select
                    value={selectedCity}
                    onChange={handleCityChange}
                    className={`flex-1 bg-transparent text-lg font-semibold ${weatherData.isDay ? "text-slate-900" : "text-white"} border-none outline-none cursor-pointer appearance-none pr-8`}
                    style={{
                      backgroundImage: `url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='${weatherData.isDay ? "%23000" : "%23fff"}' d='M6 9L1 4h10z'/%3E%3C/svg%3E")`,
                      backgroundRepeat: "no-repeat",
                      backgroundPosition: "right 0.5rem center",
                    }}
                    disabled={loading}
                  >
                    {PARAGUAY_CITIES.map((city) => (
                      <option key={city.value} value={city.value} className="bg-slate-800 text-white">
                        {city.label}, Paraguay
                      </option>
                    ))}
                  </select>
                </div>
              </div>
              
              <div className='text-center'>
                  <button 
                      onClick={() => fetchWeather(selectedCity)} 
                      disabled={loading}
                      className={`w-full px-6 py-3 rounded-lg font-bold transition flex items-center justify-center gap-2 
                                ${weatherData.isDay ? 'bg-slate-900 text-white hover:bg-slate-700' : 'bg-white text-slate-900 hover:bg-slate-200'} disabled:opacity-50`}
                  >
                      <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`}/>
                      {loading ? 'Actualizando...' : 'Recargar Datos'}
                  </button>
              </div>
            </div>
          </div>
        </Card>
      </div>
    </section>
  )
}
