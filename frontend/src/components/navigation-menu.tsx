
import { useState, useEffect } from "react"
import { Menu, X, Cloud, DollarSign, Bitcoin } from "lucide-react"
import { Button } from "@/components/ui/button"
import AboutDialog from "./about-dialog"

export default function NavigationMenu() {
  const [isOpen, setIsOpen] = useState(false)
  const [activeSection, setActiveSection] = useState("clima")

  useEffect(() => {
    const handleScroll = () => {
      const sections = ["clima", "monedas", "bitcoin"]
      const scrollPosition = window.scrollY + 100

      for (const section of sections) {
        const element = document.getElementById(section)
        if (element) {
          const { offsetTop, offsetHeight } = element
          if (scrollPosition >= offsetTop && scrollPosition < offsetTop + offsetHeight) {
            setActiveSection(section)
            break
          }
        }
      }
    }

    window.addEventListener("scroll", handleScroll)
    return () => window.removeEventListener("scroll", handleScroll)
  }, [])

  const scrollToSection = (sectionId: string) => {
    const element = document.getElementById(sectionId)
    if (element) {
      element.scrollIntoView({ behavior: "smooth" })
      setIsOpen(false)
    }
  }

  const menuItems = [
    { id: "clima", label: "Clima", icon: Cloud },
    { id: "monedas", label: "Monedas", icon: DollarSign },
    { id: "bitcoin", label: "Bitcoin", icon: Bitcoin },
  ]

  return (
    <>
      {/* Desktop Navigation */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-white/80 backdrop-blur-md shadow-lg">
        <div className="container mx-auto px-4">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center gap-2">
              <span className="text-2xl">🇵🇾</span>
              <h1 className="text-xl font-bold text-slate-900">Paraguay Hub</h1>
            </div>

            {/* Desktop Menu */}
            <div className="hidden md:flex items-center gap-2">
              {menuItems.map((item) => {
                const Icon = item.icon
                return (
                  <Button
                    key={item.id}
                    onClick={() => scrollToSection(item.id)}
                    variant={activeSection === item.id ? "default" : "ghost"}
                    className={`flex items-center gap-2 transition-all ${
                      activeSection === item.id ? "bg-primary text-white" : "text-slate-700 hover:text-slate-900"
                    }`}
                  >
                    <Icon className="w-4 h-4" />
                    {item.label}
                  </Button>
                )
              })}
              <AboutDialog />
            </div>

            {/* Mobile Menu Button */}
            <Button variant="ghost" size="icon" className="md:hidden" onClick={() => setIsOpen(!isOpen)}>
              {isOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </Button>
          </div>
        </div>
      </nav>

      {/* Mobile Menu */}
      <div
        className={`fixed inset-0 z-40 bg-white transform transition-transform duration-300 md:hidden ${
          isOpen ? "translate-x-0" : "translate-x-full"
        }`}
        style={{ top: "64px" }}
      >
        <div className="p-6 space-y-4">
          {menuItems.map((item) => {
            const Icon = item.icon
            return (
              <button
                key={item.id}
                onClick={() => scrollToSection(item.id)}
                className={`w-full flex items-center gap-4 p-4 rounded-lg transition-all ${
                  activeSection === item.id
                    ? "bg-primary text-white shadow-lg scale-105"
                    : "bg-slate-100 text-slate-700 hover:bg-slate-200"
                }`}
              >
                <Icon className="w-6 h-6" />
                <span className="text-lg font-semibold">{item.label}</span>
              </button>
            )
          })}
          <AboutDialog />
        </div>
      </div>

      {/* Overlay */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-30 md:hidden"
          onClick={() => setIsOpen(false)}
          style={{ top: "64px" }}
        />
      )}
    </>
  )
}
