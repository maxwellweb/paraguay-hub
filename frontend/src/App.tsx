import NavigationMenu from "@/components/navigation-menu"
import WeatherSection from "@/components/weather-section"
import CurrencySection from "@/components/currency-section"
import BitcoinSection from "@/components/bitcoin-section"
function App() {

  return (
    <>
    <NavigationMenu />
    <main className="min-h-screen pt-16">
      <div id="clima">
        <WeatherSection />
      </div>
      <div id="monedas">
        <CurrencySection />
      </div>
      <div id="bitcoin">
        <BitcoinSection />
      </div>
    </main>
    </>
  )
}

export default App
