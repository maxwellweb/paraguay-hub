import { useState, useEffect, useCallback } from "react"
import { useApiFetch } from "@/hooks/useApiFetch"
import { ScrollArea, ScrollBar } from "@/components/ui/scroll-area"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { ArrowRightLeft, Loader2, TrendingUp } from "lucide-react"

interface CurrencyState {
  code: string
  name: string
  flag: string
  rate: number
}

interface ConvesionResponse {
  source_currency: string
  target_currency: string
  amount: number
  converted_amount: number
  rate: number
  timestamp: string
}

const AVALIABLE_CURRENCIES: CurrencyState[] = [
  { code: "USD", name: "Dólar Americano", flag: "🇺🇸", rate: 0 },
  { code: "CAD", name: "Dólar Canadense", flag: "🇨🇦", rate: 0 },
  { code: "EUR", name: "Euro", flag: "🇪🇺", rate: 0 },
  { code: "BRL", name: "Real Brasileiro", flag: "🇧🇷", rate: 0 },
  { code: "ARS", name: "Peso Argentino", flag: "🇦🇷", rate: 0 },
  { code: "UYU", name: "Peso Uruguayo", flag: "🇺🇾", rate: 0 },
  { code: "COP", name: "Peso Colombiano", flag: "🇨🇴", rate: 0 },
  { code: "CLP", name: "Peso Chileno", flag: "🇨🇱", rate: 0 },
  { code: "PEN", name: "Peso Peruano", flag: "🇵🇪", rate: 0 },
  { code: "VEF", name: "Peso Venezolano", flag: "🇻🇪", rate: 0 },
  { code: "VND", name: "Dong Vietnamita", flag: "🇻🇳", rate: 0 },
  { code: "KRW", name: "Won Coreano", flag: "🇰🇷", rate: 0 },
  { code: "BOB", name: "Boliviano", flag: "🇧🇴", rate: 0 },
  { code: "GBP", name: "Libra Esterlina", flag: "🇬🇧", rate: 0 },
  { code: "JPY", name: "Yen Japones", flag: "🇯🇵", rate: 0 },
  { code: "MXN", name: "Peso Mexicano", flag: "🇲🇽", rate: 0 },
]

export default function CurrencySection() {
  const [selectedCurrency, setSelectedCurrency] = useState<CurrencyState>(AVALIABLE_CURRENCIES[0])
  const [amount, setAmount] = useState<string>("1")
  const [result, setResult] = useState<number>(0)
  const [isAnimating, setIsAnimating] = useState(false)

  const [currentRates, setCurrentRates] = useState<number>(AVALIABLE_CURRENCIES[0].rate)


  const { 
    data: conversionData, 
    loading: loadingConversion, 
    error: errorConversion, 
    executeRequest: executeConversion 
  } = useApiFetch<ConvesionResponse>();

  useEffect(() => {
    if (conversionData && !loadingConversion) {
        setResult(conversionData.converted_amount); 
        setCurrentRates(conversionData.rate)
        setIsAnimating(true);
        setTimeout(() => setIsAnimating(false), 600);
    }
  }, [conversionData, loadingConversion]);

  const handleConvert = useCallback(async (currentAmount: string, currencyCode: string) => {
    const numAmount = Number.parseFloat(currentAmount) || 0;
    
    if (numAmount <= 0 || !currencyCode) {
        setResult(0);
        return;
    }

    // Payload de POST: { "from_currency": "str", "amount": 1 }
    const payload = {
        from_currency: currencyCode, 
        amount: numAmount,
    };

    // 💡 Ejecutamos la solicitud POST a tu backend
    await executeConversion('POST', '/currency/convert', payload);

  }, [executeConversion]);

  useEffect(() => {
    handleConvert(amount, selectedCurrency.code);
    // Nota: handleConvert se auto-memoiza con useCallback, pero dependemos de los estados
  }, [amount, selectedCurrency, handleConvert]);

  const handleCurrencySelect = (currency: CurrencyState) => {
    setSelectedCurrency(currency);
    setCurrentRates(currency.rate)
    // El useEffect anterior se encarga de disparar la conversión
  }

  return (
    <section className="min-h-screen flex items-center justify-center p-4 md:p-8 bg-gradient-to-br from-emerald-50 via-teal-50 to-cyan-100">
      <div className="container max-w-6xl">
        <div className="text-center mb-8">
          <h1 className="text-4xl md:text-6xl font-bold mb-4 text-slate-900">Conversor de Monedas</h1>
          <p className="text-lg md:text-xl text-slate-700">Convierte cualquier moneda a Guaraníes (PYG)</p>
        </div>

        <div className="grid lg:grid-cols-2 gap-6">
          <Card className="p-6 md:p-8 bg-white shadow-xl border-none">
            <h3 className="text-xl font-bold mb-6 text-slate-900 flex items-center gap-2">
              <TrendingUp className="w-6 h-6 text-emerald-600" />
              Selecciona una moneda
            </h3>
            <ScrollArea className="h-[400px] rounded-md border-none whitespace-nowrap">
              <div className="grid grid-cols-2 gap-4 p-4">
              {AVALIABLE_CURRENCIES.map((currency) => (
                <Button
                  key={currency.code}
                  onClick={() => handleCurrencySelect(currency)}
                  variant={selectedCurrency.code === currency.code ? "default" : "outline"}
                  className={`h-auto p-4 flex flex-col items-start gap-2 transition-all duration-300 ${
                    selectedCurrency.code === currency.code
                      ? "bg-emerald-600 text-white scale-105 shadow-lg"
                      : "hover:bg-emerald-50 hover:scale-105"
                  }`}
                >
                  <span className="text-3xl">{currency.flag}</span>
                  <div className="text-left">
                    <p className="font-bold text-sm">{currency.code}</p>
                    <p className="text-xs opacity-80 line-clamp-1">{currency.name}</p>
                  </div>
                </Button>
              ))}
            </div>
            <ScrollBar orientation="vertical" />
            </ScrollArea>
          </Card>

          <Card className="p-6 md:p-8 bg-gradient-to-br from-emerald-600 to-teal-600 text-white shadow-xl border-none">
            <h3 className="text-xl font-bold mb-6 flex items-center gap-2">
              <ArrowRightLeft className="w-6 h-6" />
              Conversión
            </h3>

            <div className="space-y-6">
              <div className="bg-white/20 backdrop-blur-sm rounded-lg p-6">
                <label className="text-sm font-semibold mb-2 block">Cantidad en {selectedCurrency.code}</label>
                <div className="flex items-center gap-3">
                  <span className="text-4xl">{selectedCurrency.flag}</span>
                  <Input
                    type="number"
                    value={amount}
                    onChange={(e) => setAmount(e.target.value)}
                    className="text-2xl font-bold bg-white text-slate-900 border-none h-14"
                    placeholder="0.00"
                  />
                </div>
              </div>

              <div className="flex justify-center">
                <div className="bg-white/30 rounded-full p-3 animate-pulse-glow">
                  <ArrowRightLeft className="w-8 h-8" />
                </div>
              </div>

              <div
                className={`bg-white/20 backdrop-blur-sm rounded-lg p-6 transition-all duration-500 ${
                  isAnimating ? "scale-105 bg-white/30" : ""
                }`}
              >
                <label className="text-sm font-semibold mb-2 block">Resultado en PYG</label>
                <div className="flex items-center gap-3">
                  <span className="text-4xl">🇵🇾</span>
                  <div className="flex-1">
                    <p className="text-3xl md:text-4xl font-bold">
                      {loadingConversion ? (
                        <Loader2 className="w-8 h-8 animate-spin inline-block mr-2" />
                      ) : (
                        `₲ ${result.toLocaleString("es-PY", { maximumFractionDigits: 0 })}`
                      )}
                    </p>
                  </div>
                </div>
              </div>

              <div className="bg-white/10 rounded-lg p-4 text-sm">
                <p className="opacity-90">
                  {errorConversion ? (
                    <p className="text-red-300 font-medium">Error al convertir: {errorConversion}</p>
                  ) : (
                    <p className="opacity-90">
                        Tasa de Referencia: 1 {selectedCurrency.code} = ₲ {currentRates.toLocaleString("es-PY", { maximumFractionDigits: 0 })}
                    </p>
                  )}
                </p>
              </div>
            </div>
          </Card>
        </div>
      </div>
    </section>
  )
}
