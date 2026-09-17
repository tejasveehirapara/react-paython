import { createBrowserRouter } from 'react-router-dom'
import { AppLayout } from '../layouts/AppLayout'
import { ClientFormPage } from '../pages/ClientFormPage'
import { ClientsPage } from '../pages/ClientsPage'
import { DashboardPage } from '../pages/DashboardPage'
import { SettingsPage } from '../pages/SettingsPage'

export const router = createBrowserRouter([{ element: <AppLayout />, children: [
  { path: '/', element: <DashboardPage /> },
  { path: '/clients', element: <ClientsPage /> },
  { path: '/clients/new', element: <ClientFormPage /> },
  { path: '/clients/:id/edit', element: <ClientFormPage /> },
  { path: '/settings', element: <SettingsPage /> },
] }])
