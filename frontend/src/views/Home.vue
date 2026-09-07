<template>
  <div class="home-container">
    <!-- 头部 -->
    <el-header class="header">
      <h1>保险销售智能陪练系统</h1>
      <p class="subtitle">AI驱动的销售能力提升平台</p>
    </el-header>

    <!-- 主体内容 -->
    <el-main class="main-content">
      <!-- 场景选择卡片 -->
      <el-card class="selection-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <el-icon><User /></el-icon>
            <span>选择客户角色</span>
          </div>
        </template>

        <div class="role-list" v-loading="loading">
          <div
            v-for="role in roles"
            :key="role.id"
            class="role-item"
            :class="{ selected: selectedRole?.id === role.id }"
            @click="selectRole(role)"
          >
            <div class="role-name">{{ role.name }}</div>
            <div class="role-desc">{{ role.description }}</div>
            <el-tag
              :type="getDifficultyType(role.difficulty)"
              size="small"
              class="role-difficulty"
            >
              {{ role.difficulty }}
            </el-tag>
          </div>
        </div>
      </el-card>

      <!-- 产品选择卡片 -->
      <el-card class="selection-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <el-icon><Document /></el-icon>
            <span>选择保险产品</span>
          </div>
        </template>

        <div class="product-list" v-loading="loading">
          <div
            v-for="product in products"
            :key="product.id"
            class="product-item"
            :class="{ selected: selectedProduct?.id === product.id }"
            @click="selectProduct(product)"
          >
            <div class="product-name">{{ product.name }}</div>
            <div class="product-desc">{{ product.description }}</div>
            <div class="product-meta">
              <el-tag size="small">{{ product.product_type }}</el-tag>
              <span class="price">{{ product.premium_range }}</span>
            </div>
          </div>
        </div>
      </el-card>

      <!-- 模型选择卡片 -->
      <el-card class="selection-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <el-icon><Cpu /></el-icon>
            <span>选择对话模型</span>
          </div>
        </template>

        <div class="model-list" v-loading="loadingModels">
          <div
            v-if="activeModels.length === 0 && !loadingModels"
            class="model-empty"
          >
            暂无可用模型，请到
            <router-link to="/admin" class="empty-link">管理后台</router-link>
            配置
          </div>
          <div
            v-for="model in activeModels"
            :key="model.id"
            class="model-item"
            :class="{ selected: selectedModel?.id === model.id }"
            @click="selectModel(model)"
          >
            <div class="model-name">{{ model.model_name }}</div>
            <div class="model-desc">{{ model.provider || '自定义模型' }}</div>
          </div>
        </div>
      </el-card>

      <!-- 开始按钮 -->
      <div class="action-area">
        <el-button
          type="primary"
          size="large"
          :disabled="!canStart"
          @click="startPractice"
          :loading="starting"
        >
          <el-icon><ChatDotRound /></el-icon>
          开始对话练习
        </el-button>
        <p class="tip" v-if="!canStart">
          请先选择客户角色、保险产品和对话模型
        </p>
      </div>

      <!-- 历史记录和管理入口 -->
      <div class="footer-links">
        <router-link to="/history" class="link-item">
          <el-icon><Clock /></el-icon>
          查看练习历史
        </router-link>
        <router-link to="/admin" class="link-item admin-link">
          <el-icon><Setting /></el-icon>
          管理后台
        </router-link>
      </div>
    </el-main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Cpu } from '@element-plus/icons-vue'
import { getRoles, getProducts, getModels, startDialogue } from '@/api/modules'

const router = useRouter()

// 数据
const roles = ref([])
const products = ref([])
const models = ref([])
const selectedRole = ref(null)
const selectedProduct = ref(null)
const selectedModel = ref(null)
const loading = ref(true)
const loadingModels = ref(true)
const starting = ref(false)

// 仅展示启用中的模型
const activeModels = computed(() => models.value.filter(m => m.is_active))

// 计算属性
const canStart = computed(() => {
  return selectedRole.value && selectedProduct.value && selectedModel.value
})

// 方法
const getDifficultyType = (difficulty) => {
  const map = {
    '简单': 'success',
    '普通': 'info',
    '困难': 'danger',
    '专家': 'warning'
  }
  return map[difficulty] || 'info'
}

const selectRole = (role) => {
  selectedRole.value = role
}

const selectProduct = (product) => {
  selectedProduct.value = product
}

const selectModel = (model) => {
  selectedModel.value = model
}

const startPractice = async () => {
  if (!canStart.value) return

  starting.value = true

  try {
    const response = await startDialogue({
      role_id: selectedRole.value.id,
      product_id: selectedProduct.value.id,
      model_name: selectedModel.value.model_name
    })

    // 保存会话信息到 sessionStorage
    sessionStorage.setItem('session_id', response.session_id)
    sessionStorage.setItem('role_name', response.role_name)
    sessionStorage.setItem('product_name', response.product_name)
    sessionStorage.setItem('greeting', response.greeting)

    // 跳转到对话页面
    router.push('/dialogue')

  } catch (error) {
    ElMessage.error('启动对话失败: ' + (error.message || '未知错误'))
  } finally {
    starting.value = false
  }
}

// 生命周期
onMounted(async () => {
  try {
    // 并行加载角色、产品和模型列表
    const [rolesData, productsData, modelsData] = await Promise.all([
      getRoles(),
      getProducts(),
      getModels().catch(() => [])
    ])

    roles.value = rolesData
    products.value = productsData
    models.value = modelsData

  } catch (error) {
    ElMessage.error('加载数据失败')
  } finally {
    loading.value = false
    loadingModels.value = false
  }
})
</script>

<style scoped>
.home-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.header {
  text-align: center;
  padding: 40px 20px;
  color: white;
}

.header h1 {
  font-size: 32px;
  margin-bottom: 10px;
}

.subtitle {
  font-size: 16px;
  opacity: 0.9;
}

.main-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.selection-card {
  margin-bottom: 20px;
  border-radius: 12px;
  overflow: hidden;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: bold;
  font-size: 18px;
}

.role-list,
.product-list,
.model-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
}

.model-empty {
  grid-column: 1 / -1;
  text-align: center;
  color: #909399;
  padding: 24px 0;
  font-size: 14px;
}

.empty-link {
  color: #667eea;
}

.role-item,
.product-item,
.model-item {
  padding: 16px;
  border: 2px solid #e4e7ed;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
}

.role-item:hover,
.product-item:hover,
.model-item:hover {
  border-color: #667eea;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
}

.role-item.selected,
.product-item.selected,
.model-item.selected {
  border-color: #667eea;
  background-color: #f0f2ff;
}

.role-name,
.product-name,
.model-name {
  font-weight: bold;
  font-size: 16px;
  margin-bottom: 8px;
}

.role-desc,
.product-desc,
.model-desc {
  color: #606266;
  font-size: 14px;
  margin-bottom: 12px;
  line-height: 1.5;
}

.role-difficulty {
  margin-top: 8px;
}

.product-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 12px;
}

.price {
  color: #f56c6c;
  font-weight: bold;
  font-size: 14px;
}

.action-area {
  text-align: center;
  margin: 40px 0;
}

.action-area .el-button {
  padding: 16px 48px;
  font-size: 18px;
}

.tip {
  margin-top: 16px;
  color: white;
  font-size: 14px;
}

.footer-links {
  text-align: center;
  margin-top: 20px;
  display: flex;
  justify-content: center;
  gap: 40px;
}

.link-item {
  color: white;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  transition: all 0.3s;
}

.link-item:hover {
  opacity: 0.8;
}

.admin-link {
  padding: 8px 16px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 20px;
}

/* 移动端适配 */
@media (max-width: 768px) {
  .header h1 {
    font-size: 24px;
  }

  .role-list,
  .product-list,
  .model-list {
    grid-template-columns: 1fr;
  }

  .action-area .el-button {
    width: 100%;
  }
}
</style>
