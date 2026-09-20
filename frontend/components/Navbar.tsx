"use client";

import React, { useEffect, useState } from "react";
import { useAuth } from "@/lib/auth-context";
import { LogOut, Sun, Moon, PlusCircle, Compass } from "lucide-react";

interface NavbarProps {
  onOpenAuth: (mode?: "login" | "register") => void;
  onOpenNewSession: () => void;
  onGoHome: () => void;
}

export function Navbar({ onOpenAuth, onOpenNewSession, onGoHome }: NavbarProps) {
  const { user, logout } = useAuth();
  const [isDark, setIsDark] = useState<boolean>(true);

  useEffect(() => {
    // Default to dark mode for modern high-craft devtool aesthetic
    const isLight = localStorage.getItem("theme") === "light";
    const root = document.documentElement;
    if (isLight) {
      root.classList.remove("dark");
    } else {
      root.classList.add("dark");
    }
    requestAnimationFrame(() => {
      setIsDark(!isLight);
    });
  }, []);

  const toggleTheme = () => {
    const root = document.documentElement;
    if (isDark) {
      root.classList.remove("dark");
      localStorage.setItem("theme", "light");
      setIsDark(false);
    } else {
      root.classList.add("dark");
      localStorage.setItem("theme", "dark");
      setIsDark(true);
    }
  };

  return (
    <header className="sticky top-0 z-40 w-full border-b border-zinc-200/80 bg-white/80 backdrop-blur-md dark:border-zinc-800/80 dark:bg-zinc-950/80">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
        {/* Brand */}
        <div className="flex items-center gap-6">
          <button
            onClick={onGoHome}
            className="flex items-center gap-2.5 text-left focus:outline-none group"
          >
            <div className="flex size-9 items-center justify-center rounded-xl bg-zinc-900 text-white shadow-sm ring-1 ring-zinc-800 dark:bg-zinc-100 dark:text-zinc-900">
              <Compass className="size-5 transition-transform duration-300 group-hover:rotate-45" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="font-semibold tracking-tight text-zinc-900 text-lg dark:text-zinc-50">
                  Bespoke
                </span>
                <span className="rounded-full bg-emerald-500/10 px-2 py-0.5 text-[10px] font-medium tracking-wide text-emerald-600 dark:bg-emerald-500/20 dark:text-emerald-400 border border-emerald-500/20">
                  PREP
                </span>
              </div>
              <p className="text-[11px] text-zinc-500 dark:text-zinc-400 font-normal">
                Adaptive Company-Specific AI Interviews
              </p>
            </div>
          </button>
        </div>

        {/* Right Actions */}
        <div className="flex items-center gap-3">
          {user ? (
            <>
              <button
                onClick={onOpenNewSession}
                className="hidden sm:inline-flex items-center gap-2 rounded-lg bg-zinc-900 px-3.5 py-2 text-xs font-semibold text-white transition-all hover:bg-zinc-800 shadow-sm active:scale-[0.98] dark:bg-zinc-100 dark:text-zinc-900 dark:hover:bg-zinc-200"
              >
                <PlusCircle className="size-4" />
                <span>Start Preparation</span>
              </button>

              <div className="flex items-center gap-2.5 pl-2 border-l border-zinc-200 dark:border-zinc-800">
                <div className="hidden sm:flex flex-col items-end text-right">
                  <span className="text-xs font-medium text-zinc-900 dark:text-zinc-100">
                    {user.full_name || user.email.split("@")[0]}
                  </span>
                  <span className="text-[10px] text-zinc-400 capitalize">
                    {user.role}
                  </span>
                </div>

                <div className="flex size-8 items-center justify-center rounded-full bg-zinc-100 text-zinc-700 font-medium text-xs dark:bg-zinc-800 dark:text-zinc-200">
                  {user.full_name ? user.full_name[0].toUpperCase() : "C"}
                </div>

                <button
                  onClick={logout}
                  title="Sign out"
                  className="rounded-lg p-2 text-zinc-500 hover:bg-zinc-100 hover:text-zinc-900 dark:text-zinc-400 dark:hover:bg-zinc-800 dark:hover:text-zinc-100 transition-colors"
                >
                  <LogOut className="size-4" />
                </button>
              </div>
            </>
          ) : (
            <div className="flex items-center gap-2">
              <button
                onClick={() => onOpenAuth("login")}
                className="rounded-lg px-3.5 py-2 text-xs font-medium text-zinc-700 hover:bg-zinc-100 dark:text-zinc-300 dark:hover:bg-zinc-800 transition-colors"
              >
                Sign In
              </button>
              <button
                onClick={() => onOpenAuth("register")}
                className="rounded-lg bg-zinc-900 px-3.5 py-2 text-xs font-semibold text-white shadow-sm hover:bg-zinc-800 dark:bg-zinc-100 dark:text-zinc-900 dark:hover:bg-zinc-200 transition-all"
              >
                Create Free Account
              </button>
            </div>
          )}

          {/* Theme Toggle */}
          <button
            onClick={toggleTheme}
            title={isDark ? "Switch to light mode" : "Switch to dark mode"}
            className="rounded-lg p-2 text-zinc-500 hover:bg-zinc-100 hover:text-zinc-900 dark:text-zinc-400 dark:hover:bg-zinc-800 dark:hover:text-zinc-100 transition-colors"
          >
            {isDark ? <Sun className="size-4" /> : <Moon className="size-4" />}
          </button>
        </div>
      </div>
    </header>
  );
}
