"use client";

import React, { useState } from "react";
import { useUserStore } from "../store/userStore";
import { Sparkles, Key, Mail, User, Shield, AlertCircle } from "lucide-react";

interface AuthModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export default function AuthModal({ isOpen, onClose }: AuthModalProps) {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [username, setUsername] = useState("");
  const [brandName, setBrandName] = useState("RJ Business Solutions");
  const [customAuthor, setCustomAuthor] = useState("Rick Jefferson");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const { setToken, setUser } = useUserStore();

  if (!isOpen) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    const baseUrl = "http://localhost:8000";
    const endpoint = isLogin ? "/api/auth/login" : "/api/auth/register";

    try {
      const body: any = isLogin 
        ? { email, password }
        : { email, password, username, brand_name: brandName, custom_author: customAuthor };

      const response = await fetch(`${baseUrl}${endpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body)
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Authentication failed. Please verify fields.");
      }

      // Success
      setToken(data.access_token);
      setUser(data.user);
      onClose();
    } catch (err: any) {
      setError(err.message || "Connection refused. Ensure backend is running.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-[100] flex items-center justify-center bg-slate-950/80 p-4 backdrop-blur-sm">
      <div className="glass-panel w-full max-w-md rounded-2xl p-8 flex flex-col gap-6 relative overflow-hidden">
        {/* Decorative corner light glow */}
        <div className="absolute -top-12 -right-12 h-24 w-24 rounded-full bg-sky-500/20 blur-xl" />

        <div className="flex flex-col items-center text-center gap-2">
          <div className="h-12 w-12 rounded-xl bg-sky-500/10 border border-sky-500/20 flex items-center justify-center text-sky-400">
            <Shield className="h-6 w-6" />
          </div>
          <h2 className="text-xl font-extrabold text-white uppercase tracking-tight">
            {isLogin ? "Operator Login" : "Operator Sign Up"}
          </h2>
          <p className="text-xs text-slate-400">
            {isLogin 
              ? "Access the Prometheus engine with your secure credentials" 
              : "Register your white-label business system settings"}
          </p>
        </div>

        {error && (
          <div className="bg-red-950/20 border border-red-500/20 rounded-xl p-3.5 text-xs text-red-400 flex items-center gap-2.5">
            <AlertCircle className="h-4 w-4 flex-shrink-0" />
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          {!isLogin && (
            <div className="flex flex-col gap-1.5">
              <label className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Username</label>
              <div className="relative">
                <User className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-500" />
                <input 
                  type="text"
                  required
                  placeholder="rjefferson"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  className="w-full bg-slate-950/80 border border-slate-800 rounded-xl py-2.5 pl-10 pr-4 text-sm text-white focus:outline-none focus:border-sky-500"
                />
              </div>
            </div>
          )}

          <div className="flex flex-col gap-1.5">
            <label className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Email Address</label>
            <div className="relative">
              <Mail className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-500" />
              <input 
                type="email"
                required
                placeholder="rick@rjbusinesssolutions.org"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full bg-slate-950/80 border border-slate-800 rounded-xl py-2.5 pl-10 pr-4 text-sm text-white focus:outline-none focus:border-sky-500"
              />
            </div>
          </div>

          <div className="flex flex-col gap-1.5">
            <label className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Password</label>
            <div className="relative">
              <Key className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-500" />
              <input 
                type="password"
                required
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full bg-slate-950/80 border border-slate-800 rounded-xl py-2.5 pl-10 pr-4 text-sm text-white focus:outline-none focus:border-sky-500"
              />
            </div>
          </div>

          {!isLogin && (
            <div className="grid grid-cols-2 gap-4">
              <div className="flex flex-col gap-1.5">
                <label className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Brand Name</label>
                <input 
                  type="text"
                  required
                  value={brandName}
                  onChange={(e) => setBrandName(e.target.value)}
                  className="w-full bg-slate-950/80 border border-slate-800 rounded-xl py-2.5 px-3 text-xs text-white focus:outline-none"
                />
              </div>
              <div className="flex flex-col gap-1.5">
                <label className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Custom Author</label>
                <input 
                  type="text"
                  required
                  value={customAuthor}
                  onChange={(e) => setCustomAuthor(e.target.value)}
                  className="w-full bg-slate-950/80 border border-slate-800 rounded-xl py-2.5 px-3 text-xs text-white focus:outline-none"
                />
              </div>
            </div>
          )}

          <button 
            type="submit"
            disabled={loading}
            className="w-full bg-sky-600 hover:bg-sky-500 text-white text-xs font-bold rounded-xl py-3 uppercase tracking-wider transition-colors flex items-center justify-center gap-2 mt-2 disabled:opacity-50"
          >
            {loading ? (
              <span className="h-4 w-4 rounded-full border-2 border-white/30 border-t-white animate-spin" />
            ) : (
              <>
                <Sparkles className="h-4 w-4" />
                {isLogin ? "Authenticate Operator" : "Configure White-Label Profile"}
              </>
            )}
          </button>
        </form>

        <div className="flex items-center justify-between text-xs text-slate-400 border-t border-slate-800 pt-4">
          <span>{isLogin ? "New user?" : "Already configured?"}</span>
          <button 
            onClick={() => setIsLogin(!isLogin)}
            className="text-sky-400 font-semibold hover:underline"
          >
            {isLogin ? "Configure profile" : "Access console"}
          </button>
        </div>

        <button 
          onClick={onClose}
          className="absolute top-4 right-4 text-slate-500 hover:text-white text-lg font-bold"
        >
          ×
        </button>
      </div>
    </div>
  );
}
