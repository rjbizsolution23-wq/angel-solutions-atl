"use client";

import React, { useState, useEffect, useRef } from "react";
import { Gamepad2, Play, Pause, RotateCcw, Monitor } from "lucide-react";

interface RetroArcadeProps {
  selectedPlatform: string;
  selectedGame: string;
  onPackageGame: () => void;
  romPackStatus: string;
  activeGameId: string;
  activeGameFile: string;
}

export default function RetroArcade({
  selectedPlatform,
  selectedGame,
  onPackageGame,
  romPackStatus,
  activeGameId,
  activeGameFile
}: RetroArcadeProps) {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [score, setScore] = useState(0);
  const [highScore, setHighScore] = useState(12800);
  const [isGameOver, setIsGameOver] = useState(false);

  // Edge-caching mirror proxy URL construction for EmulatorJS
  const romUrl = `https://prometheus-cloudflare-backend.rickjefferson.workers.dev/api/games/proxy?id=${encodeURIComponent(activeGameId || "smb_nes")}&file=${encodeURIComponent(activeGameFile || "Super Mario Bros.nes")}`;

  // Platform mapping NES -> nes, SNES -> snes, Sega Genesis -> genesis, Game Boy Advance -> gba
  let platform = (selectedPlatform || "nes").toLowerCase();
  if (platform === "sega" || platform === "genesis" || platform === "megadrive") {
    platform = "genesis";
  }

  // Game Engine State Variables
  const ballX = useRef(150);
  const ballY = useRef(150);
  const ballSpeedX = useRef(2.5);
  const ballSpeedY = useRef(-2.5);
  const paddleX = useRef(120);
  const paddleWidth = 60;
  const paddleHeight = 8;
  const brickRowCount = 4;
  const brickColumnCount = 6;
  const brickWidth = 40;
  const brickHeight = 12;
  const brickPadding = 6;
  const brickOffsetTop = 30;
  const brickOffsetLeft = 20;

  const bricks = useRef<any[][]>([]);

  // Initialize Bricks
  const initBricks = () => {
    const tempBricks: any[][] = [];
    for (let c = 0; c < brickColumnCount; c++) {
      tempBricks[c] = [];
      for (let r = 0; r < brickRowCount; r++) {
        tempBricks[c][r] = { x: 0, y: 0, status: 1 };
      }
    }
    bricks.current = tempBricks;
  };

  useEffect(() => {
    initBricks();
  }, [selectedPlatform]);

  // Adjust game parameters based on selected core/platform
  useEffect(() => {
    let speed = 2.5;
    if (selectedPlatform === "nes") speed = 2.5;
    if (selectedPlatform === "snes") speed = 3.5;
    if (selectedPlatform === "genesis") speed = 4.5;
    if (selectedPlatform === "dos") speed = 5.5;

    ballSpeedX.current = speed * (ballSpeedX.current > 0 ? 1 : -1);
    ballSpeedY.current = -speed;
    resetGame();
  }, [selectedPlatform, selectedGame]);

  const resetGame = () => {
    setIsGameOver(false);
    setScore(0);
    ballX.current = 150;
    ballY.current = 200;
    paddleX.current = 120;
    initBricks();
  };

  // Keyboard controls
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (!isPlaying || isGameOver) return;
      if (e.key === "ArrowLeft" || e.key === "a") {
        paddleX.current = Math.max(0, paddleX.current - 15);
      } else if (e.key === "ArrowRight" || e.key === "d") {
        const canvas = canvasRef.current;
        if (canvas) {
          paddleX.current = Math.min(canvas.width - paddleWidth, paddleX.current + 15);
        }
      }
    };

    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [isPlaying, isGameOver]);

  // Game Loop
  useEffect(() => {
    if (!isPlaying || isGameOver) return;

    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    let animationFrameId: number;

    const draw = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      // Draw Background grid (retro matrix feel)
      ctx.strokeStyle = "rgba(14, 165, 233, 0.04)";
      ctx.lineWidth = 1;
      for (let i = 0; i < canvas.width; i += 20) {
        ctx.beginPath();
        ctx.moveTo(i, 0);
        ctx.lineTo(i, canvas.height);
        ctx.stroke();
      }
      for (let i = 0; i < canvas.height; i += 20) {
        ctx.beginPath();
        ctx.moveTo(0, i);
        ctx.lineTo(canvas.width, i);
        ctx.stroke();
      }

      // Draw Bricks
      for (let c = 0; c < brickColumnCount; c++) {
        for (let r = 0; r < brickRowCount; r++) {
          if (bricks.current[c]?.[r]?.status === 1) {
            const brickX = c * (brickWidth + brickPadding) + brickOffsetLeft;
            const brickY = r * (brickHeight + brickPadding) + brickOffsetTop;
            bricks.current[c][r].x = brickX;
            bricks.current[c][r].y = brickY;
            
            // Retro multi-color rows
            let fillStyle = "#0ea5e9"; // Sky Blue
            if (r === 1) fillStyle = "#3b82f6"; // Royal Blue
            if (r === 2) fillStyle = "#8b5cf6"; // Violet
            if (r === 3) fillStyle = "#10b981"; // Emerald

            ctx.fillStyle = fillStyle;
            ctx.fillRect(brickX, brickY, brickWidth, brickHeight);
            ctx.strokeStyle = "#020617";
            ctx.strokeRect(brickX, brickY, brickWidth, brickHeight);
          }
        }
      }

      // Draw Ball
      ctx.beginPath();
      ctx.arc(ballX.current, ballY.current, 5, 0, Math.PI * 2);
      ctx.fillStyle = "#ffffff";
      ctx.shadowBlur = 10;
      ctx.shadowColor = "#ffffff";
      ctx.fill();
      ctx.shadowBlur = 0; // reset shadow

      // Draw Paddle
      ctx.fillStyle = "#a855f7";
      ctx.fillRect(paddleX.current, canvas.height - paddleHeight - 5, paddleWidth, paddleHeight);

      // Ball Wall Collisions
      if (ballX.current + ballSpeedX.current > canvas.width - 5 || ballX.current + ballSpeedX.current < 5) {
        ballSpeedX.current = -ballSpeedX.current;
      }
      if (ballY.current + ballSpeedY.current < 5) {
        ballSpeedY.current = -ballSpeedY.current;
      } else if (ballY.current + ballSpeedY.current > canvas.height - paddleHeight - 10) {
        // Paddle hit collision
        if (ballX.current > paddleX.current && ballX.current < paddleX.current + paddleWidth) {
          ballSpeedY.current = -ballSpeedY.current;
        } else if (ballY.current + ballSpeedY.current > canvas.height - 5) {
          // Game Over
          setIsGameOver(true);
          setIsPlaying(false);
        }
      }

      // Ball Brick Collision
      for (let c = 0; c < brickColumnCount; c++) {
        for (let r = 0; r < brickRowCount; r++) {
          const b = bricks.current[c]?.[r];
          if (b && b.status === 1) {
            if (
              ballX.current > b.x &&
              ballX.current < b.x + brickWidth &&
              ballY.current > b.y &&
              ballY.current < b.y + brickHeight
            ) {
              ballSpeedY.current = -ballSpeedY.current;
              b.status = 0;
              setScore((s) => {
                const newScore = s + 100;
                if (newScore > highScore) setHighScore(newScore);
                return newScore;
              });
            }
          }
        }
      }

      ballX.current += ballSpeedX.current;
      ballY.current += ballSpeedY.current;

      animationFrameId = requestAnimationFrame(draw);
    };

    animationFrameId = requestAnimationFrame(draw);
    return () => cancelAnimationFrame(animationFrameId);
  }, [isPlaying, isGameOver]);

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
      {/* Game controls menu */}
      <div className="flex flex-col gap-6 justify-between bg-slate-950/20 border border-slate-800/60 rounded-2xl p-6">
        <div className="flex flex-col gap-4">
          <div className="flex flex-col gap-1.5">
            <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Active Core Module</span>
            <div className="text-sm font-black text-sky-400 uppercase">{selectedPlatform.toUpperCase()} EMU CORE v1.0</div>
          </div>

          <div className="flex flex-col gap-1.5">
            <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">ROM Header</span>
            <div className="text-xs font-semibold text-white truncate">{selectedGame || "No Game Loaded"}</div>
          </div>

          <div className="border-t border-slate-800 my-2 pt-4 flex flex-col gap-3">
            <div className="flex justify-between text-xs font-mono text-slate-400">
              <span>SCORE:</span>
              <span className="text-white font-bold">{score}</span>
            </div>
            <div className="flex justify-between text-xs font-mono text-slate-400">
              <span>HI-SCORE:</span>
              <span className="text-violet-400 font-bold">{highScore}</span>
            </div>
          </div>
        </div>

        <div className="flex flex-col gap-3">
          {isPlaying && (
            <button 
              onClick={() => setIsPlaying(false)}
              className="w-full bg-rose-600 hover:bg-rose-500 text-white text-xs font-bold rounded-xl py-3 uppercase tracking-wider transition-all shadow-lg"
            >
              Power Off Console
            </button>
          )}
          <button 
            onClick={onPackageGame}
            className="w-full bg-violet-600 hover:bg-violet-500 text-white text-xs font-bold rounded-xl py-3 uppercase tracking-wider transition-all"
          >
            Rebuild Emulator Bundle
          </button>
          
          {romPackStatus && (
            <p className="text-[10px] text-center text-violet-400 leading-relaxed font-semibold">{romPackStatus}</p>
          )}
        </div>
      </div>

      {/* Screen Monitor Cabinet viewport */}
      <div className="lg:col-span-2 arcade-monitor relative flex flex-col justify-between p-6 h-80 overflow-hidden">
        {/* CRT Scanline matrix effects */}
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(14,165,233,0.06),transparent_80%)] pointer-events-none" />

        {/* Top Header */}
        <div className="flex items-center justify-between z-10 font-mono text-[9px] text-emerald-400 uppercase tracking-widest">
          <div className="flex items-center gap-2">
            <span className="h-2 w-2 rounded-full bg-emerald-500 animate-pulse" />
            <span>Core Active</span>
          </div>
          <span>FPS: {isPlaying ? "60.0" : "0.0"}</span>
        </div>

        {/* Canvas play center replaced with EmulatorJS iframe */}
        <div className="flex-1 flex items-center justify-center z-10 relative h-full w-full min-h-0 bg-slate-950/80 border border-slate-800 rounded shadow-inner overflow-hidden mt-2">
          {isPlaying ? (
            <iframe 
              src={`https://cdn.emulatorjs.org/stable/loader.html?game=${encodeURIComponent(romUrl)}&system=${platform}`}
              className="w-full h-full border-0 bg-black absolute inset-0"
              scrolling="no"
              allowFullScreen
            />
          ) : (
            <div className="absolute inset-0 flex flex-col items-center justify-center bg-slate-950/90 gap-3 rounded">
              <Gamepad2 className="h-10 w-10 text-slate-700 animate-bounce" />
              <button 
                onClick={() => setIsPlaying(true)}
                className="bg-sky-600 hover:bg-sky-500 text-white font-black text-[10px] uppercase tracking-wider px-4 py-2 rounded-lg flex items-center gap-1.5 transition-all shadow-lg"
              >
                <Play className="h-3 w-3 fill-white" />
                Play Console ROM
              </button>
            </div>
          )}
        </div>

        {/* Bottom controls explanation bar */}
        <div className="flex justify-between items-center z-10 text-[9px] text-slate-500 font-mono mt-3 truncate">
          <span>CONTROLS: ARROWS (D-PAD) | Z (A) | X (B) | SHIFT (SELECT) | ENTER (START)</span>
          <span>RJ SYSTEMS ARCADE v3.1</span>
        </div>
      </div>
    </div>
  );
}
