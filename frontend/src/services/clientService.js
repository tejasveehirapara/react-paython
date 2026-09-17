import api from './api'

export const getClients = async () => api.get('/clients')
export const getClient = async (id) => api.get(`/clients/${id}`)
export const createClient = async (data) => api.post('/clients', data)
export const updateClient = async (id, data) => api.put(`/clients/${id}`, data)
export const deleteClient = async (id) => api.delete(`/clients/${id}`)
