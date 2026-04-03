import { useState } from "react";
import { motion } from "framer-motion";
import { Sun, Moon, Thermometer, Music, BellOff, ConciergeBell, Power } from "lucide-react";

interface RoomState {
  lights: boolean;
  temperature: number;
  music: boolean;
  dnd: boolean;
}

const SmartRoom = () => {
  const [room, setRoom] = useState<RoomState>({
    lights: true,
    temperature: 23,
    music: false,
    dnd: false,
  });
  const [serviceRequested, setServiceRequested] = useState(false);

  const toggle = (key: keyof Omit<RoomState, "temperature">) =>
    setRoom((prev) => ({ ...prev, [key]: !prev[key] }));

  const setTemp = (val: number) => setRoom((prev) => ({ ...prev, temperature: val }));

  const requestService = () => {
    setServiceRequested(true);
    setTimeout(() => setServiceRequested(false), 3000);
  };

  return (
    <div className="min-h-screen bg-background">
      <div className="gradient-earth px-4 py-10 sm:px-6">
        <div className="container-resort">
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
            <p className="text-gold-light font-body text-sm uppercase tracking-[0.2em] mb-2">Smart Room</p>
            <h1 className="font-display text-3xl sm:text-4xl font-bold text-primary-foreground">Room Control Dashboard</h1>
            <p className="text-primary-foreground/60 text-sm mt-2">Villa 12 — Cultural Experience Suite</p>
          </motion.div>
        </div>
      </div>

      <div className="container-resort section-padding">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 max-w-4xl mx-auto">
          {/* Lights */}
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.05 }} className="glass-card p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-3">
                {room.lights ? <Sun className="w-6 h-6 text-accent" /> : <Moon className="w-6 h-6 text-muted-foreground" />}
                <h3 className="font-display text-lg font-semibold text-foreground">Lights</h3>
              </div>
              <span className={`text-xs font-body px-2 py-1 rounded-full ${room.lights ? "bg-accent/10 text-accent" : "bg-muted text-muted-foreground"}`}>
                {room.lights ? "ON" : "OFF"}
              </span>
            </div>
            <button
              onClick={() => toggle("lights")}
              className={`w-full py-3 rounded-xl font-semibold text-sm transition-all ${
                room.lights ? "gradient-gold text-primary-foreground shadow-md" : "bg-secondary text-secondary-foreground"
              }`}
            >
              <Power className="w-4 h-4 inline mr-2" />
              {room.lights ? "Turn Off" : "Turn On"}
            </button>
          </motion.div>

          {/* Temperature */}
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }} className="glass-card p-6">
            <div className="flex items-center gap-3 mb-4">
              <Thermometer className="w-6 h-6 text-terracotta" />
              <h3 className="font-display text-lg font-semibold text-foreground">Temperature</h3>
            </div>
            <div className="text-center mb-4">
              <span className="font-display text-4xl font-bold text-foreground">{room.temperature}°</span>
              <span className="text-muted-foreground text-sm ml-1">C</span>
            </div>
            <input
              type="range"
              min={16}
              max={30}
              value={room.temperature}
              onChange={(e) => setTemp(Number(e.target.value))}
              className="w-full accent-accent h-2 rounded-lg appearance-none bg-secondary cursor-pointer"
            />
            <div className="flex justify-between text-xs text-muted-foreground mt-1">
              <span>16°C</span>
              <span>30°C</span>
            </div>
          </motion.div>

          {/* Music */}
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.15 }} className="glass-card p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-3">
                <Music className={`w-6 h-6 ${room.music ? "text-accent" : "text-muted-foreground"}`} />
                <h3 className="font-display text-lg font-semibold text-foreground">Music</h3>
              </div>
              <span className={`text-xs font-body px-2 py-1 rounded-full ${room.music ? "bg-accent/10 text-accent" : "bg-muted text-muted-foreground"}`}>
                {room.music ? "Playing" : "OFF"}
              </span>
            </div>
            {room.music && <p className="text-sm text-muted-foreground mb-3">♪ Ethiopian Jazz — Mulatu Astatke</p>}
            <button
              onClick={() => toggle("music")}
              className={`w-full py-3 rounded-xl font-semibold text-sm transition-all ${
                room.music ? "gradient-gold text-primary-foreground shadow-md" : "bg-secondary text-secondary-foreground"
              }`}
            >
              {room.music ? "Pause Music" : "Play Music"}
            </button>
          </motion.div>

          {/* DND */}
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }} className="glass-card p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-3">
                <BellOff className={`w-6 h-6 ${room.dnd ? "text-destructive" : "text-muted-foreground"}`} />
                <h3 className="font-display text-lg font-semibold text-foreground">Do Not Disturb</h3>
              </div>
            </div>
            <button
              onClick={() => toggle("dnd")}
              className={`w-full py-3 rounded-xl font-semibold text-sm transition-all ${
                room.dnd ? "bg-destructive text-destructive-foreground shadow-md" : "bg-secondary text-secondary-foreground"
              }`}
            >
              {room.dnd ? "Disable DND" : "Enable DND"}
            </button>
          </motion.div>

          {/* Room Service */}
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.25 }} className="glass-card p-6 sm:col-span-2 lg:col-span-2">
            <div className="flex items-center gap-3 mb-4">
              <ConciergeBell className="w-6 h-6 text-accent" />
              <h3 className="font-display text-lg font-semibold text-foreground">Room Service</h3>
            </div>
            <p className="text-muted-foreground text-sm mb-4">Request in-room dining, housekeeping, or any special assistance.</p>
            <button
              onClick={requestService}
              disabled={serviceRequested}
              className={`w-full py-3 rounded-xl font-semibold text-sm transition-all ${
                serviceRequested ? "bg-forest text-primary-foreground" : "gradient-gold text-primary-foreground shadow-md hover:shadow-lg"
              }`}
            >
              {serviceRequested ? "✓ Request Sent — Staff Notified" : "Request Room Service"}
            </button>
          </motion.div>
        </div>

        {/* Room Status */}
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }} className="max-w-4xl mx-auto mt-8">
          <div className="glass-card p-6">
            <h3 className="font-display text-lg font-semibold text-foreground mb-4">Current Room Status</h3>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 text-center">
              <div><div className="text-xs text-muted-foreground mb-1">Lights</div><div className={`font-semibold ${room.lights ? "text-accent" : "text-muted-foreground"}`}>{room.lights ? "On" : "Off"}</div></div>
              <div><div className="text-xs text-muted-foreground mb-1">Temperature</div><div className="font-semibold text-foreground">{room.temperature}°C</div></div>
              <div><div className="text-xs text-muted-foreground mb-1">Music</div><div className={`font-semibold ${room.music ? "text-accent" : "text-muted-foreground"}`}>{room.music ? "Playing" : "Off"}</div></div>
              <div><div className="text-xs text-muted-foreground mb-1">DND</div><div className={`font-semibold ${room.dnd ? "text-destructive" : "text-muted-foreground"}`}>{room.dnd ? "Active" : "Off"}</div></div>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default SmartRoom;
