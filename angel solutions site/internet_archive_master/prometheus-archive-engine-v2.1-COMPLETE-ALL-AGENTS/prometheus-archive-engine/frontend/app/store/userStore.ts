"use client";

import { create } from "zustand";

interface UserProfile {
  id: string;
  username: string;
  email: string;
  role: string;
  brand_name?: string;
  custom_author?: string;
}

interface UserState {
  token: string | null;
  user: UserProfile | null;
  isLoggedIn: boolean;
  searchHistory: any[];
  archivedContent: any[];
  setToken: (token: string | null) => void;
  setUser: (user: UserProfile | null) => void;
  logout: () => void;
  addSearchHistoryItem: (item: any) => void;
  addArchivedContentItem: (item: any) => void;
  setSearchHistory: (items: any[]) => void;
  setArchivedContent: (items: any[]) => void;
}

export const useUserStore = create<UserState>((set) => ({
  token: typeof window !== "undefined" ? localStorage.getItem("token") : null,
  user: null,
  isLoggedIn: typeof window !== "undefined" ? !!localStorage.getItem("token") : false,
  searchHistory: [],
  archivedContent: [],
  
  setToken: (token) => set((state) => {
    if (typeof window !== "undefined") {
      if (token) {
        localStorage.setItem("token", token);
      } else {
        localStorage.removeItem("token");
      }
    }
    return { token, isLoggedIn: !!token };
  }),
  
  setUser: (user) => set({ user }),
  
  logout: () => set((state) => {
    if (typeof window !== "undefined") {
      localStorage.removeItem("token");
    }
    return { token: null, user: null, isLoggedIn: false, searchHistory: [], archivedContent: [] };
  }),

  addSearchHistoryItem: (item) => set((state) => ({
    searchHistory: [item, ...state.searchHistory.filter((i) => i.id !== item.id)].slice(0, 20)
  })),

  addArchivedContentItem: (item) => set((state) => ({
    archivedContent: [item, ...state.archivedContent.filter((i) => i.id !== item.id)]
  })),

  setSearchHistory: (items) => set({ searchHistory: items }),
  setArchivedContent: (items) => set({ archivedContent: items })
}));
