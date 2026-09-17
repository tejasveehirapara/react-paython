import { Menu } from 'lucide-react'
import { useState } from 'react'
import { Outlet } from 'react-router-dom'
import { AppSidebar } from '../components/AppSidebar'

export function AppLayout() { const [menuOpen, setMenuOpen] = useState(false); return <div className="min-h-screen lg:flex"><AppSidebar open={menuOpen} onClose={() => setMenuOpen(false)} /><div className="min-w-0 flex-1"><header className="flex h-16 items-center border-b border-[var(--border)] px-4 sm:px-7"><button className="rounded p-2 lg:hidden" aria-label="Open navigation" onClick={() => setMenuOpen(true)}><Menu size={20} /></button><p className="ml-auto text-sm text-zinc-500">Operations workspace</p><div className="ml-3 grid h-8 w-8 place-items-center rounded-full bg-black text-xs font-semibold text-white">MB</div></header><main className="mx-auto w-full max-w-7xl p-4 sm:p-7"><Outlet /></main></div></div> }
