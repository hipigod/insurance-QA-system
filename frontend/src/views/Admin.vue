<template>
  <div class="admin-container">
    <!-- 头部 -->
    <div class="admin-header">
      <el-button circle @click="goBack">
        <el-icon><ArrowLeft /></el-icon>
      </el-button>
      <h2>管理后台</h2>
      <div></div>
    </div>

    <!-- 主体内容 -->
    <el-main class="main-content">
      <el-tabs v-model="activeTab" type="border-card">
        <!-- 角色管理 -->
        <el-tab-pane label="客户角色管理" name="roles">
          <div class="tab-header">
            <el-button type="primary" @click="showRoleDialog()">
              <el-icon><Plus /></el-icon>
              新增角色
            </el-button>
          </div>

          <el-table :data="roles" style="width: 100%" v-loading="loading">
            <el-table-column prop="id" label="ID" width="60" />
            <el-table-column prop="name" label="角色名称" width="150" />
            <el-table-column prop="description" label="简介" />
            <el-table-column prop="difficulty" label="难度" width="100">
              <template #default="{ row }">
                <el-tag :type="getDifficultyType(row.difficulty)">
                  {{ row.difficulty }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="180" fixed="right">
              <template #default="{ row }">
                <el-button size="small" @click="showRoleDialog(row)">编辑</el-button>
                <el-button size="small" type="danger" @click="deleteRole(row.id)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>

        <!-- 产品管理 -->
        <el-tab-pane label="保险产品管理" name="products">
          <div class="tab-header">
            <el-button type="primary" @click="showProductDialog()">
              <el-icon><Plus /></el-icon>
              新增产品
            </el-button>
          </div>

          <el-table :data="products" style="width: 100%" v-loading="loading">
            <el-table-column prop="id" label="ID" width="60" />
            <el-table-column prop="name" label="产品名称" width="180" />
            <el-table-column prop="product_type" label="类型" width="120" />
            <el-table-column prop="description" label="简介" />
            <el-table-column prop="premium_range" label="保费范围" width="120" />
            <el-table-column label="操作" width="180" fixed="right">
              <template #default="{ row }">
                <el-button size="small" @click="showProductDialog(row)">编辑</el-button>
                <el-button size="small" type="danger" @click="deleteProduct(row.id)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>

        <!-- 评分维度管理 -->
        <el-tab-pane label="评分维度管理" name="dimensions">
          <div class="tab-header">
            <el-alert
              title="提示：各维度权重之和必须等于100%"
              type="info"
              :closable="false"
              style="margin-bottom: 16px"
            />
            <el-button type="primary" @click="showDimensionDialog()">
              <el-icon><Plus /></el-icon>
              新增维度
            </el-button>
          </div>

          <el-table :data="dimensions" style="width: 100%" v-loading="loading">
            <el-table-column prop="id" label="ID" width="60" />
            <el-table-column prop="name" label="维度名称" width="150" />
            <el-table-column prop="description" label="描述" />
            <el-table-column prop="weight" label="权重(%)" width="100">
              <template #default="{ row }">
                <el-input-number
                  v-model="row.weight"
                  :min="0"
                  :max="100"
                  size="small"
                  @change="updateDimensionWeight(row)"
                />
              </template>
            </el-table-column>
            <el-table-column label="操作" width="180" fixed="right">
              <template #default="{ row }">
                <el-button size="small" @click="showDimensionDialog(row)">编辑</el-button>
                <el-button size="small" type="danger" @click="deleteDimension(row.id)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>

          <div class="weight-summary">
            <el-tag :type="totalWeight === 100 ? 'success' : 'danger'">
              当前总权重: {{ totalWeight }}%
            </el-tag>
          </div>
        </el-tab-pane>

        <!-- 优秀案例管理 -->
        <el-tab-pane label="优秀案例库" name="cases">
          <div class="tab-header">
            <el-alert
              title="案例将在评分报告中针对用户薄弱环节自动推送"
              type="info"
              :closable="false"
              style="margin-bottom: 16px"
            />
            <el-button type="primary" @click="showCaseDialog()">
              <el-icon><Plus /></el-icon>
              新增案例
            </el-button>
          </div>

          <el-table :data="cases" style="width: 100%" v-loading="loading">
            <el-table-column prop="id" label="ID" width="60" />
            <el-table-column prop="weakness_type" label="薄弱环节" width="150" />
            <el-table-column prop="case_content" label="案例内容" show-overflow-tooltip />
            <el-table-column label="操作" width="180" fixed="right">
              <template #default="{ row }">
                <el-button size="small" @click="showCaseDialog(row)">编辑</el-button>
                <el-button size="small" type="danger" @click="deleteCase(row.id)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>

        <!-- 数据导出 -->
        <el-tab-pane label="数据导出" name="export">
          <el-card shadow="never">
            <h3>导出练习记录</h3>
            <p class="tip">将LocalStorage中的练习记录导出为文件</p>

            <el-space direction="vertical" style="width: 100%">
              <el-button type="primary" @click="exportData('json')" :icon="Download">
                导出为JSON
              </el-button>
              <el-button type="success" @click="exportData('excel')" :icon="Download">
                导出为Excel（CSV）
              </el-button>
            </el-space>

            <el-divider />

            <h3>导入练习记录</h3>
            <p class="tip">从之前导出的JSON文件恢复数据</p>

            <el-upload
              :auto-upload="false"
              :on-change="importData"
              :show-file-list="false"
              accept=".json"
            >
              <el-button type="warning" :icon="Upload">
                选择JSON文件导入
              </el-button>
            </el-upload>
          </el-card>
        </el-tab-pane>
      </el-tabs>
    </el-main>

    <!-- 角色编辑对话框 -->
    <el-dialog
      v-model="roleDialogVisible"
      :title="roleForm.id ? '编辑角色' : '新增角色'"
      width="600px"
    >
      <el-form :model="roleForm" label-width="100px">
        <el-form-item label="角色名称">
          <el-input v-model="roleForm.name" placeholder="请输入角色名称" />
        </el-form-item>
        <el-form-item label="角色简介">
          <el-input v-model="roleForm.description" type="textarea" :rows="2" />
        </el-form-item>
        <el-form-item label="难度等级">
          <el-select v-model="roleForm.difficulty">
            <el-option label="简单" value="简单" />
            <el-option label="普通" value="普通" />
            <el-option label="困难" value="困难" />
            <el-option label="专家" value="专家" />
          </el-select>
        </el-form-item>
        <el-form-item label="角色提示词">
          <el-input
            v-model="roleForm.system_prompt"
            type="textarea"
            :rows="10"
            placeholder="详细描述角色的性格特征、沟通风格、对保险的态度等"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="roleDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveRole" :loading="saving">保存</el-button>
      </template>
    </el-dialog>

    <!-- 产品编辑对话框 -->
    <el-dialog
      v-model="productDialogVisible"
      :title="productForm.id ? '编辑产品' : '新增产品'"
      width="600px"
    >
      <el-form :model="productForm" label-width="120px">
        <el-form-item label="产品名称">
          <el-input v-model="productForm.name" />
        </el-form-item>
        <el-form-item label="产品类型">
          <el-input v-model="productForm.product_type" />
        </el-form-item>
        <el-form-item label="产品简介">
          <el-input v-model="productForm.description" type="textarea" :rows="2" />
        </el-form-item>
        <el-form-item label="保障范围">
          <el-input v-model="productForm.coverage" type="textarea" :rows="3" />
        </el-form-item>
        <el-form-item label="保费范围">
          <el-input v-model="productForm.premium_range" />
        </el-form-item>
        <el-form-item label="适用人群">
          <el-input v-model="productForm.target_audience" />
        </el-form-item>
        <el-form-item label="详细信息">
          <el-input v-model="productForm.detailed_info" type="textarea" :rows="5" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="productDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveProduct" :loading="saving">保存</el-button>
      </template>
    </el-dialog>

    <!-- 维度编辑对话框 -->
    <el-dialog
      v-model="dimensionDialogVisible"
      :title="dimensionForm.id ? '编辑维度' : '新增维度'"
      width="600px"
    >
      <el-form :model="dimensionForm" label-width="120px">
        <el-form-item label="维度名称">
          <el-input v-model="dimensionForm.name" />
        </el-form-item>
        <el-form-item label="维度描述">
          <el-input v-model="dimensionForm.description" type="textarea" :rows="2" />
        </el-form-item>
        <el-form-item label="权重(%)">
          <el-input-number v-model="dimensionForm.weight" :min="0" :max="100" />
        </el-form-item>
        <el-form-item label="评分依据">
          <el-input v-model="dimensionForm.evaluation_prompt" type="textarea" :rows="5" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dimensionDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveDimension" :loading="saving">保存</el-button>
      </template>
    </el-dialog>

    <!-- 案例编辑对话框 -->
    <el-dialog
      v-model="caseDialogVisible"
      :title="caseForm.id ? '编辑案例' : '新增案例'"
      width="600px"
    >
      <el-form :model="caseForm" label-width="120px">
        <el-form-item label="薄弱环节">
          <el-select v-model="caseForm.weakness_type" placeholder="请选择">
            <el-option label="需求挖掘" value="需求挖掘" />
            <el-option label="沟通表达" value="沟通表达" />
            <el-option label="异议处理" value="异议处理" />
            <el-option label="促成技巧" value="促成技巧" />
            <el-option label="产品介绍" value="产品介绍" />
          </el-select>
        </el-form-item>
        <el-form-item label="对话节点">
          <el-select v-model="caseForm.dialogue_node" placeholder="请选择">
            <el-option label="开场白" value="开场白" />
            <el-option label="需求挖掘" value="需求挖掘" />
            <el-option label="产品介绍" value="产品介绍" />
            <el-option label="异议处理" value="异议处理" />
            <el-option label="促成尝试" value="促成尝试" />
          </el-select>
        </el-form-item>
        <el-form-item label="案例内容">
          <el-input
            v-model="caseForm.case_content"
            type="textarea"
            :rows="8"
            placeholder="优秀对话片段或标准话术"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="caseDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveCase" :loading="saving">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Download, Upload } from '@element-plus/icons-vue'
import api from '@/api/modules'

const router = useRouter()

// 数据
const activeTab = ref('roles')
const loading = ref(false)
const saving = ref(false)
const roles = ref([])
const products = ref([])
const dimensions = ref([])
const cases = ref([])

// 对话框状态
const roleDialogVisible = ref(false)
const productDialogVisible = ref(false)
const dimensionDialogVisible = ref(false)
const caseDialogVisible = ref(false)

// 表单数据
const roleForm = ref({})
const productForm = ref({})
const dimensionForm = ref({})
const caseForm = ref({})

// 计算总权重
const totalWeight = computed(() => {
  return dimensions.value.reduce((sum, d) => sum + (d.weight || 0), 0)
})

// 方法
const goBack = () => {
  router.push('/')
}

const getDifficultyType = (difficulty) => {
  const map = {
    '简单': 'success',
    '普通': 'info',
    '困难': 'danger',
    '专家': 'warning'
  }
  return map[difficulty] || 'info'
}

// 加载数据
const loadRoles = async () => {
  try {
    loading.value = true
    roles.value = await api.getRoles()
  } catch (error) {
    ElMessage.error('加载角色失败')
  } finally {
    loading.value = false
  }
}

const loadProducts = async () => {
  try {
    loading.value = true
    products.value = await api.getProducts()
  } catch (error) {
    ElMessage.error('加载产品失败')
  } finally {
    loading.value = false
  }
}

const loadDimensions = async () => {
  try {
    loading.value = true
    dimensions.value = await api.getDimensions()
  } catch (error) {
    ElMessage.error('加载评分维度失败')
  } finally {
    loading.value = false
  }
}

const loadCases = async () => {
  try {
    loading.value = true
    cases.value = await api.getCases()
  } catch (error) {
    ElMessage.error('加载案例失败')
  } finally {
    loading.value = false
  }
}

// 角色管理
const showRoleDialog = (role = null) => {
  roleForm.value = role ? { ...role } : {
    name: '',
    description: '',
    difficulty: '普通',
    system_prompt: ''
  }
  roleDialogVisible.value = true
}

const saveRole = async () => {
  if (!roleForm.value.name) {
    ElMessage.warning('请输入角色名称')
    return
  }

  try {
    saving.value = true
    if (roleForm.value.id) {
      await api.updateRole(roleForm.value.id, roleForm.value)
      ElMessage.success('更新成功')
    } else {
      await api.createRole(roleForm.value)
      ElMessage.success('创建成功')
    }
    roleDialogVisible.value = false
    loadRoles()
  } catch (error) {
    ElMessage.error('保存失败')
  } finally {
    saving.value = false
  }
}

const deleteRole = async (id) => {
  try {
    await ElMessageBox.confirm('确定删除该角色吗？', '提示', {
      type: 'warning'
    })
    await api.deleteRole(id)
    ElMessage.success('删除成功')
    loadRoles()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

// 产品管理
const showProductDialog = (product = null) => {
  productForm.value = product ? { ...product } : {
    name: '',
    product_type: '',
    description: '',
    coverage: '',
    premium_range: '',
    target_audience: '',
    detailed_info: ''
  }
  productDialogVisible.value = true
}

const saveProduct = async () => {
  if (!productForm.value.name) {
    ElMessage.warning('请输入产品名称')
    return
  }

  try {
    saving.value = true
    if (productForm.value.id) {
      await api.updateProduct(productForm.value.id, productForm.value)
      ElMessage.success('更新成功')
    } else {
      await api.createProduct(productForm.value)
      ElMessage.success('创建成功')
    }
    productDialogVisible.value = false
    loadProducts()
  } catch (error) {
    ElMessage.error('保存失败')
  } finally {
    saving.value = false
  }
}

const deleteProduct = async (id) => {
  try {
    await ElMessageBox.confirm('确定删除该产品吗？', '提示', {
      type: 'warning'
    })
    await api.deleteProduct(id)
    ElMessage.success('删除成功')
    loadProducts()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

// 维度管理
const showDimensionDialog = (dimension = null) => {
  dimensionForm.value = dimension ? { ...dimension } : {
    name: '',
    description: '',
    weight: 25,
    evaluation_prompt: ''
  }
  dimensionDialogVisible.value = true
}

const saveDimension = async () => {
  if (!dimensionForm.value.name) {
    ElMessage.warning('请输入维度名称')
    return
  }

  try {
    saving.value = true
    if (dimensionForm.value.id) {
      await api.updateDimension(dimensionForm.value.id, dimensionForm.value)
      ElMessage.success('更新成功')
    } else {
      await api.createDimension(dimensionForm.value)
      ElMessage.success('创建成功')
    }
    dimensionDialogVisible.value = false
    loadDimensions()
  } catch (error) {
    ElMessage.error('保存失败')
  } finally {
    saving.value = false
  }
}

const updateDimensionWeight = async (dimension) => {
  try {
    await api.updateDimension(dimension.id, { weight: dimension.weight })
    ElMessage.success('权重已更新')
  } catch (error) {
    ElMessage.error('更新失败')
  }
}

const deleteDimension = async (id) => {
  try {
    await ElMessageBox.confirm('确定删除该维度吗？', '提示', {
      type: 'warning'
    })
    await api.deleteDimension(id)
    ElMessage.success('删除成功')
    loadDimensions()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

// 案例管理
const showCaseDialog = (caseItem = null) => {
  caseForm.value = caseItem ? { ...caseItem } : {
    weakness_type: '',
    case_content: '',
    dialogue_node: ''
  }
  caseDialogVisible.value = true
}

const saveCase = async () => {
  if (!caseForm.value.weakness_type || !caseForm.value.case_content) {
    ElMessage.warning('请填写完整信息')
    return
  }

  try {
    saving.value = true
    if (caseForm.value.id) {
      await api.updateCase(caseForm.value.id, caseForm.value)
      ElMessage.success('更新成功')
    } else {
      await api.createCase(caseForm.value)
      ElMessage.success('创建成功')
    }
    caseDialogVisible.value = false
    loadCases()
  } catch (error) {
    ElMessage.error('保存失败')
  } finally {
    saving.value = false
  }
}

const deleteCase = async (id) => {
  try {
    await ElMessageBox.confirm('确定删除该案例吗？', '提示', {
      type: 'warning'
    })
    await api.deleteCase(id)
    ElMessage.success('删除成功')
    loadCases()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

// 数据导出
const exportData = (format) => {
  const history = localStorage.getItem('practice_history')

  if (!history) {
    ElMessage.warning('暂无练习记录')
    return
  }

  const data = JSON.parse(history)

  if (format === 'json') {
    // 导出为JSON
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `练习记录_${new Date().toISOString().slice(0, 10)}.json`
    a.click()
    URL.revokeObjectURL(url)
    ElMessage.success('导出成功')
  } else if (format === 'excel') {
    // 导出为CSV
    let csv = '\ufeff'  // UTF-8 BOM
    csv += '时间,角色,产品,总分,对话轮次\n'

    data.forEach(record => {
      const time = new Date(record.created_at).toLocaleString()
      const rounds = record.dialogue_data ? record.dialogue_data.length : 0
      csv += `"${time}","${record.role_name}","${record.product_name}",${record.total_score},${rounds}\n`
    })

    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `练习记录_${new Date().toISOString().slice(0, 10)}.csv`
    a.click()
    URL.revokeObjectURL(url)
    ElMessage.success('导出成功')
  }
}

const importData = (file) => {
  const reader = new FileReader()

  reader.onload = (e) => {
    try {
      const data = JSON.parse(e.target.result)

      if (!Array.isArray(data)) {
        throw new Error('格式错误')
      }

      localStorage.setItem('practice_history', JSON.stringify(data))
      ElMessage.success(`成功导入${data.length}条记录`)

      // 刷新当前页面（如果需要）
    } catch (error) {
      ElMessage.error('文件格式错误，请选择正确的JSON文件')
    }
  }

  reader.readAsText(file.raw)
}

// 生命周期
onMounted(() => {
  loadRoles()
  loadProducts()
  loadDimensions()
  loadCases()
})
</script>

<style scoped>
.admin-container {
  min-height: 100vh;
  background-color: #f5f7fa;
}

.admin-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  background: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.admin-header h2 {
  margin: 0;
  font-size: 20px;
}

.main-content {
  max-width: 1400px;
  margin: 20px auto;
  padding: 0 20px 40px;
}

.tab-header {
  margin-bottom: 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.tip {
  color: #909399;
  font-size: 14px;
  margin-top: 8px;
}

.weight-summary {
  margin-top: 20px;
  padding: 16px;
  background: #f9fafc;
  border-radius: 8px;
  text-align: center;
}
</style>
