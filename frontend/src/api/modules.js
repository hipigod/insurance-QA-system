import api from './index'

export const getRoles = () => api.get('/roles')
export const createRole = (data) => api.post('/roles', data)
export const updateRole = (id, data) => api.put(`/roles/${id}`, data)
export const deleteRole = (id) => api.delete(`/roles/${id}`)

export const getProducts = () => api.get('/products')
export const createProduct = (data) => api.post('/products', data)
export const updateProduct = (id, data) => api.put(`/products/${id}`, data)
export const deleteProduct = (id) => api.delete(`/products/${id}`)

export const getDimensions = () => api.get('/dimensions')
export const createDimension = (data) => api.post('/dimensions', data)
export const updateDimension = (id, data) => api.put(`/dimensions/${id}`, data)
export const deleteDimension = (id) => api.delete(`/dimensions/${id}`)

export const getCases = () => api.get('/cases')
export const createCase = (data) => api.post('/cases', data)
export const updateCase = (id, data) => api.put(`/cases/${id}`, data)
export const deleteCase = (id) => api.delete(`/cases/${id}`)

export const startDialogue = (data) => api.post('/dialogues', data)
export const submitScore = (data) => api.post('/dialogues/score', data)

export const getModels = () => api.get('/models')
export const createModel = (data) => api.post('/models', data)
export const updateModel = (id, data) => api.put(`/models/${id}`, data)
export const deleteModel = (id) => api.delete(`/models/${id}`)
export const activateModel = (id) => api.post(`/models/${id}/activate`)
