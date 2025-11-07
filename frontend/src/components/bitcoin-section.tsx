import { useState, useEffect, useCallback } from "react"
import { useApiFetch } from "@/hooks/useApiFetch"

import { Card } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { TrendingUp, TrendingDown, Bitcoin, ArrowUpRight, ArrowDownRight, Loader2 } from "lucide-react"

interface BitcoinConversionResponse {
  source_currency: string
  target_currency: string
  amount: number
  converted_amount: number
  btc_rate_usd: number
  btc_rate_pyg: number
  usd_rate_pyg: number
  btc_high_24h: number
  btc_low_24h: number
  btc_change_24h: number
  timestamp: string
}



const formatPyg = (value: number) => {
    // 1. Redondear el número para evitar decimales en Guaraníes
    const roundedValue = Math.round(value);
    
    // 2. Usar un locale que asegure el punto como separador de miles.
    // 'es-PY' a veces puede fallar, 'es-ES' suele usar punto para miles.
    // Usamos 'es-PY' con opciones forzadas:
    const formatted = roundedValue.toLocaleString("es-PY", { 
        useGrouping: true, 
        maximumFractionDigits: 0 
    });
    
    // Si el resultado es 7,087, este regex lo convierte a 7.087 si fuera necesario
    // Pero con maximumFractionDigits: 0, deberíamos obtener el formato correcto directamente.
    
    return `₲ ${formatted}`; 
};


export default function BitcoinSection() {
  const [btcAmount, setBtcAmount] = useState<string>("1")
  const [pygAmount, setPygAmount] = useState<number>(0)

  const [btcRatePyg, setBtcRatePyg] = useState<number>(0)
  const [high24hPyg, setHigh24hPyg] = useState<number>(0)
  const [low24hPyg, setLow24hPyg] = useState<number>(0)
  const [change24hPercent, setChange24hPercent] = useState<number>(0)
   

  const {
    data: conversionData,
    loading: loadingConversion,
    error: errorConversion,
    executeRequest: executeConversion,
  } = useApiFetch<BitcoinConversionResponse>();

const handleConvert = useCallback(async (currentAmount: string) => {
    const numAmount = Number.parseFloat(currentAmount) || 0;
    
    if (numAmount <= 0) {
        setPygAmount(0);
        return;
    }

    // Payload de POST para convertir una cantidad de BTC
    const payload = {
        from_currency: "BTC", // Asumiendo que la API sabe que es BTC
        amount: numAmount,
    };

    // 💡 Llamada POST: Asumimos el endpoint /bitcoin/convert
    await executeConversion('POST', '/bitcoin/convert', payload);

  }, [executeConversion]);

  useEffect(() => {
    handleConvert(btcAmount)
  }, [btcAmount, handleConvert])

  useEffect(() => {
    if(conversionData && !loadingConversion){
      setPygAmount(conversionData.converted_amount)
      setBtcRatePyg(conversionData.btc_rate_pyg)
      setHigh24hPyg(conversionData.btc_high_24h)
      setLow24hPyg(conversionData.btc_low_24h)
      setChange24hPercent(conversionData.btc_change_24h)
    }
  }, [conversionData, loadingConversion]);

  const bitcoinStats = {
    price: btcRatePyg,
    change24h: change24hPercent,
    high24h: high24hPyg,
    low24h: low24hPyg,
    trend: change24hPercent > 0 ? "up" : "down",
  }

  const isUp = bitcoinStats.trend === "up"

  const getTrendColor = () => {
    if(isUp) return "from-emerald-600 to-green-500";
    if(bitcoinStats.trend === "down") return "from-red-600 to-red-500";
    return "from-slate-500 to-gray-500"
  }

  const getTrendBg = () => {
    if (isUp) return "bg-gradient-to-br from-emerald-900 via-teal-900 to-green-900";
    if (bitcoinStats.trend === "down") return "bg-gradient-to-br from-red-900 via-rose-900 to-pink-900";
    return "bg-gradient-to-br from-slate-900 via-gray-900 to-zinc-900";
  }

  if(loadingConversion && pygAmount === 0) {
    return (
      <section className={`min-h-screen flex items-center justify-center ${getTrendBg()}`}>
        <Loader2 className="w-10 h-10 animate-spin text-white" />
        <p className="ml-4 text-white">Consultando precio de Bitcoin...</p>
      </section>
    );
  }

  if(errorConversion) {
    return (
        <section className={`min-h-screen flex items-center justify-center ${getTrendBg()}`}>
            <p className="text-red-400 font-bold text-xl">
                Error al convertir BTC: {errorConversion}
            </p>
        </section>
    );
  }

    return (
    <section
      className={`min-h-screen flex items-center justify-center p-4 md:p-8 transition-all duration-1000 ${getTrendBg()}`}
    >
      <div className="container max-w-6xl">
        <div className="text-center mb-8">
          <h1 className="text-4xl md:text-6xl font-bold mb-4 text-white">Bitcoin a Guaraníes</h1>
          <p className="text-lg md:text-xl text-white/90">Precio en tiempo real de BTC a PYG</p>
        </div>

        <div className="grid lg:grid-cols-3 gap-6 mb-6">
          <Card className="p-6 bg-white/10 backdrop-blur-md border-white/20 text-white">
            <div className="flex items-center justify-between mb-2">
              <p className="text-sm font-semibold opacity-80">Precio Actual</p>
              <Bitcoin className="w-5 h-5" />
            </div>
            <p className="text-2xl md:text-3xl font-bold">
              {loadingConversion && btcRatePyg === 0 ? (
                  <Loader2 className="w-6 h-6 animate-spin text-white" />
              ) : (
                  <p className="text-2xl md:text-3xl font-bold">
                      {formatPyg(bitcoinStats.price)}
                  </p>
              )}
            </p>
          </Card>

          <Card className={`p-6 bg-gradient-to-br ${getTrendColor()} border-none text-white`}>
            <div className="flex items-center justify-between mb-2">
              <p className="text-sm font-semibold">Cambio 24h</p>
              {isUp ? <TrendingUp className="w-5 h-5" /> : <TrendingDown className="w-5 h-5" />}
            </div>
            <p className="text-2xl md:text-3xl font-bold flex items-center gap-2">
              {bitcoinStats.change24h.toFixed(2)}%
              {isUp ? <ArrowUpRight className="w-6 h-6" /> : <ArrowDownRight className="w-6 h-6" />}
            </p>
          </Card>

          <Card className="p-6 bg-white/10 backdrop-blur-md border-white/20 text-white">
            <div className="flex items-center justify-between mb-2">
              <p className="text-sm font-semibold opacity-80">Rango 24h</p>
            </div>
            <div className="space-y-1">
              <p className="text-sm">
                <span className="opacity-70">Alto:</span>{" "}
                <span className="font-bold">
                  {formatPyg(bitcoinStats.high24h)}
                </span>
              </p>
              <p className="text-sm">
                <span className="opacity-70">Bajo:</span>{" "}
                <span className="font-bold">
                  {formatPyg(bitcoinStats.low24h)}
                </span>
              </p>
            </div>
          </Card>
        </div>

        <Card className="p-8 md:p-12 bg-white/95 backdrop-blur-sm border-none shadow-2xl">
          <div className="grid md:grid-cols-2 gap-8">
            <div className="space-y-4">
              <div className="flex items-center gap-3 mb-6">
                <div className={`p-3 rounded-full bg-gradient-to-br ${getTrendColor()}`}>
                  <Bitcoin className="w-8 h-8 text-white" />
                </div>
                <div>
                  <h3 className="text-2xl font-bold text-slate-900">Calculadora BTC</h3>
                  <p className="text-sm text-slate-600">Convierte Bitcoin a Guaraníes</p>
                </div>
              </div>

              <div className="bg-slate-50 rounded-lg p-6">
                <label className="text-sm font-semibold text-slate-700 mb-2 block">Cantidad de Bitcoin (BTC)</label>
                <Input
                  type="number"
                  value={btcAmount}
                  onChange={(e) => setBtcAmount(e.target.value)}
                  className="text-2xl font-bold h-14 bg-white border-slate-200"
                  placeholder="0.00"
                  step="0.00000001"
                />
              </div>

              <div className={`bg-gradient-to-br ${getTrendColor()} rounded-lg p-6 text-white`}>
                <label className="text-sm font-semibold mb-2 block opacity-90">Equivalente en PYG</label>
                <p className="text-3xl md:text-4xl font-bold">
                  {loadingConversion && pygAmount === 0 ? (
                      <Loader2 className="w-8 h-8 animate-spin inline-block mr-2" />
                  ) : (
                      formatPyg(pygAmount)
                  )}
                </p>
              </div>
            </div>

            <div className="flex items-center justify-center">
              <div className="relative">
                <div
                  className={`absolute inset-0 bg-gradient-to-br ${getTrendColor()} rounded-full blur-3xl opacity-30 animate-pulse-glow`}
                ></div>
                <div className={`relative bg-gradient-to-br ${getTrendColor()} rounded-full p-12 md:p-16`}>
                  <Bitcoin className="w-32 h-32 md:w-40 md:h-40 text-white animate-float" />
                </div>
              </div>
            </div>
          </div>

          <div className="mt-8 grid grid-cols-2 md:grid-cols-4 gap-4">
            {[0.001, 0.01, 0.1, 1].map((value) => (
              <button
                key={value}
                onClick={() => setBtcAmount(value.toString())}
                className="p-4 bg-slate-100 hover:bg-slate-200 rounded-lg transition-all hover:scale-105 active:scale-95"
              >
                <p className="text-sm text-slate-600 mb-1">Convertir</p>
                <p className="text-lg font-bold text-slate-900">{value} BTC</p>
              </button>
            ))}
          </div>
        </Card>
      </div>
    </section>
  )
}
