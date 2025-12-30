import api from './index'

// 获取角色列表
export const getRoles = () => {
  return api.get('/roles/')
}

// 获取角色详情
export const getRole = (id) => {
  return api.get(`/roles/${id}`)
}

// 获取产品列表
export const getProducts = () => {
  return api.get('/products/')
}

// 获取产品详情
export const getProduct = (id) => {
  return api.get(`/products/${id}`)
}

// 开始对话
export const startDialogue = (data) => {
  return api.post('/dialogue/start', data)
}

// 提交评分
export const submitScore = (data) => {
  return api.post('/dialogue/score', data)
}
