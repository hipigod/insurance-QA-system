import api from './index'

// ============ 角色管理 ============
// 获取角色列表
export const getRoles = () => {
  return api.get('/roles/')
}

// 创建角色
export const createRole = (data) => {
  return api.post('/roles/', data)
}

// 更新角色
export const updateRole = (id, data) => {
  return api.put(`/roles/${id}`, data)
}

// 删除角色
export const deleteRole = (id) => {
  return api.delete(`/roles/${id}`)
}

// ============ 产品管理 ============
// 获取产品列表
export const getProducts = () => {
  return api.get('/products/')
}

// 创建产品
export const createProduct = (data) => {
  return api.post('/products/', data)
}

// 更新产品
export const updateProduct = (id, data) => {
  return api.put(`/products/${id}`, data)
}

// 删除产品
export const deleteProduct = (id) => {
  return api.delete(`/products/${id}`)
}

// ============ 评分维度管理 ============
// 获取评分维度列表
export const getDimensions = () => {
  return api.get('/dimensions/')
}

// 创建评分维度
export const createDimension = (data) => {
  return api.post('/dimensions/', data)
}

// 更新评分维度
export const updateDimension = (id, data) => {
  return api.put(`/dimensions/${id}`, data)
}

// 删除评分维度
export const deleteDimension = (id) => {
  return api.delete(`/dimensions/${id}`)
}

// ============ 优秀案例管理 ============
// 获取案例列表
export const getCases = () => {
  return api.get('/cases/')
}

// 创建案例
export const createCase = (data) => {
  return api.post('/cases/', data)
}

// 更新案例
export const updateCase = (id, data) => {
  return api.put(`/cases/${id}`, data)
}

// 删除案例
export const deleteCase = (id) => {
  return api.delete(`/cases/${id}`)
}

// ============ 对话相关 ============
// 开始对话
export const startDialogue = (data) => {
  return api.post('/dialogue/start', data)
}

// 提交评分
export const submitScore = (data) => {
  return api.post('/dialogue/score', data)
}

// ============ 模型配置管理 ============
// 获取所有模型配置
export const getModels = () => {
  return api.get('/models/')
}

// 创建模型配置
export const createModel = (data) => {
  return api.post('/models/', data)
}

// 更新模型配置
export const updateModel = (id, data) => {
  return api.put(`/models/${id}`, data)
}

// 删除模型配置
export const deleteModel = (id) => {
  return api.delete(`/models/${id}`)
}

// 激活模型
export const activateModel = (id) => {
  return api.post(`/models/${id}/activate`)
}
