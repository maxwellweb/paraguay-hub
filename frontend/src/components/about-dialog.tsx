import { Github, Coffee, Info } from "lucide-react"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"

export default function AboutDialog() {
  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button variant="ghost" className="flex items-center gap-2 text-slate-700 hover:text-slate-900">
          <Info className="w-4 h-4" />
          <span className="hidden sm:inline">Acerca de</span>
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2 text-2xl">
            <span>🇵🇾</span>
            Paraguay Hub
          </DialogTitle>
          <DialogDescription className="text-base pt-2">
            Plataforma web interactiva que centraliza información útil para Paraguay
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-6 py-4">
          {/* Descripción del Proyecto */}
          <div className="space-y-2">
            <h3 className="font-semibold text-lg text-slate-900">Sobre el Proyecto</h3>
            <p className="text-slate-600 text-sm leading-relaxed">
              Una landing page moderna y dinámica que integra tres servicios esenciales: información climática de
              Paraguay con efectos visuales día/noche, conversión de monedas internacionales a Guaraníes (PYG), y
              seguimiento en tiempo real del precio de Bitcoin en PYG.
            </p>
          </div>

          {/* Enlaces de GitHub */}
          <div className="space-y-3">
            <h3 className="font-semibold text-lg text-slate-900">Enlaces</h3>
            <div className="space-y-2">
              <a
                href="https://github.com/maxwellweb"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-3 p-3 rounded-lg bg-slate-100 hover:bg-slate-200 transition-colors group"
              >
                <Github className="w-5 h-5 text-slate-700 group-hover:text-slate-900" />
                <div className="flex-1">
                  <p className="text-sm font-medium text-slate-900">Perfil del Creador</p>
                  <p className="text-xs text-slate-600">@maxwellweb</p>
                </div>
              </a>

              <a
                href="https://github.com/maxwellweb/paraguay-hub"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-3 p-3 rounded-lg bg-slate-100 hover:bg-slate-200 transition-colors group"
              >
                <Github className="w-5 h-5 text-slate-700 group-hover:text-slate-900" />
                <div className="flex-1">
                  <p className="text-sm font-medium text-slate-900">Repositorio del Proyecto</p>
                  <p className="text-xs text-slate-600">paraguay-hub</p>
                </div>
              </a>
            </div>
          </div>

          {/* Botón de Donación */}
          <div className="space-y-3">
            <h3 className="font-semibold text-lg text-slate-900">Apóyanos</h3>
            <a href="https://buymeacoffee.com/maxwellweb" target="_blank" rel="noopener noreferrer" className="block">
              <Button className="w-full bg-gradient-to-r from-yellow-400 to-orange-500 hover:from-yellow-500 hover:to-orange-600 text-white font-semibold py-6 rounded-lg shadow-lg hover:shadow-xl transition-all">
                <Coffee className="w-5 h-5 mr-2" />
                Invítame un café
              </Button>
            </a>
            <p className="text-xs text-slate-500 text-center">
              Tu apoyo ayuda a crear estos tipos de proyectos gratuitos y actualizados
            </p>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  )
}