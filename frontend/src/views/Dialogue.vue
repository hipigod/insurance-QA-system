<template>
  <div class="dialogue-container">
    <div class="dialogue-header">
      <el-button circle size="small" @click="goBack">
        <el-icon><ArrowLeft /></el-icon>
      </el-button>
      <div class="header-info">
        <h3>{{ roleName }} - {{ productName }}</h3>
        <el-tag size="small" type="success">实时对话中</el-tag>
      </div>
      <el-button type="danger" size="small" @click="endDialogue">
        结束对话
      </el-button>
    </div>

    <div class="messages-container" ref="messagesRef">
      <div
        v-for="(msg, index) in messages"
        :key="index"
        class="message-item"
        :class="msg.role"
      >
        <div class="message-avatar">
          <el-icon v-if="msg.role === 'user'"><User /></el-icon>
          <el-icon v-else><Avatar /></el-icon>
        </div>
        <div class="message-content">
          <div class="message-text">{{ msg.content }}</div>
          <div class="message-time">{{ msg.time }}</div>
        </div>
      </div>

      <div v-if="thinking" class="message-item assistant thinking">
        <div class="message-avatar">
          <el-icon><Avatar /></el-icon>
        </div>
        <div class="message-content">
          <div class="typing-indicator">
            <span></span>
            <span></span>
            <span></span>
          </div>
          <div class="message-time">AI正在输入...</div>
        </div>
      </div>
    </div>

    <div class="input-container">
      <el-input
        v-model="userInput"
        type="textarea"
        :rows="3"
        placeholder="输入您的回复..."
        @keydown.enter.prevent="sendMessage"
        :disabled="thinking"
      />
      <el-button
        type="primary"
        @click="sendMessage"
        :loading="thinking"
        :disabled="!userInput.trim()"
      >
        发送
      </el-button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'

const router = useRouter()

const sessionId = ref('')
const roleName = ref('')
const productName = ref('')
const greeting = ref('')
const messages = ref([])
const userInput = ref('')
const thinking = ref(false)
const messagesRef = ref(null)

let websocket = null

const goBack = () => {
  ElMessageBox.confirm(
    '确定要退出当前对话吗？对话进度将不会保存。',
    '提示',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(() => {
    if (websocket) {
      websocket.close()
    }
    router.push('/')
  }).catch(() => {})
}

const scrollToBottom = () => {
  nextTick(() => {
    if (messagesRef.value) {
      messagesRef.value.scrollTop = messagesRef.value.scrollHeight
    }
  })
}

const addMessage = (role, content) => {
  const now = new Date()
  const time = `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}`

  messages.value.push({
    role,
    content,
    time
  })

  scrollToBottom()
}

const sendMessage = () => {
  const message = userInput.value.trim()
  if (!message || thinking.value) return

  addMessage('user', message)
  userInput.value = ''

  if (websocket && websocket.readyState === WebSocket.OPEN) {
    websocket.send(JSON.stringify({
      type: 'chat',
      session_id: sessionId.value,
      message
    }))
  }
}

const endDialogue = () => {
  ElMessageBox.confirm(
    '确定要结束对话并进行评分吗？',
    '提示',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'info'
    }
  ).then(() => {
    thinking.value = true

    if (websocket && websocket.readyState === WebSocket.OPEN) {
      websocket.send(JSON.stringify({
        type: 'end',
        session_id: sessionId.value
      }))
    }
  }).catch(() => {})
}

const connectWebSocket = () => {
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
  const host = window.location.host
  const wsUrl = `${protocol}//${host}/ws/dialogue`

  console.log('正在连接WebSocket:', wsUrl)
  websocket = new WebSocket(wsUrl)

  websocket.onopen = () => {
    console.log('WebSocket connected')
    websocket.send(JSON.stringify({
      type: 'subscribe',
      session_id: sessionId.value
    }))
  }

  websocket.onmessage = (event) => {
    const data = JSON.parse(event.data)

    if (data.type === 'message') {
      thinking.value = false
      addMessage(data.role, data.content)
    } else if (data.type === 'status') {
      if (data.status === 'thinking') {
        thinking.value = true
      } else if (data.status === 'scoring') {
        thinking.value = true
      }
    } else if (data.type === 'score') {
      sessionStorage.setItem('score_result', JSON.stringify(data.data))
      sessionStorage.setItem('dialogue_history', JSON.stringify(messages.value))

      setTimeout(() => {
        router.push('/result')
      }, 1000)
    } else if (data.type === 'error') {
      thinking.value = false
      ElMessage.error(data.message)
    }
  }

  websocket.onerror = (error) => {
    console.error('WebSocket错误:', error)
    ElMessage.error('连接失败，请刷新页面重试')
  }

  websocket.onclose = () => {
    console.log('WebSocket连接关闭')
  }
}

onMounted(() => {
  sessionId.value = sessionStorage.getItem('session_id')
  roleName.value = sessionStorage.getItem('role_name')
  productName.value = sessionStorage.getItem('product_name')
  greeting.value = sessionStorage.getItem('greeting')

  if (!sessionId.value) {
    ElMessage.error('会话信息丢失，请重新开始')
    router.push('/')
    return
  }

  if (greeting.value) {
    addMessage('assistant', greeting.value)
  }

  connectWebSocket()
})

onUnmounted(() => {
  if (websocket) {
    websocket.close()
  }
})
</script>

<style scoped>
.dialogue-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: #f5f7fa;
}

.dialogue-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px;
  background: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  z-index: 10;
}

.header-info h3 {
  margin: 0;
  font-size: 16px;
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  scroll-behavior: smooth;
}

.message-item {
  display: flex;
  margin-bottom: 20px;
  align-items: flex-start;
}

.message-item.user {
  flex-direction: row-reverse;
}

.message-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 20px;
  flex-shrink: 0;
}

.message-item.user .message-avatar {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.message-content {
  max-width: 70%;
  margin: 0 12px;
}

.message-text {
  background: white;
  padding: 12px 16px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  line-height: 1.6;
  word-wrap: break-word;
}

.message-item.user .message-text {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.message-time {
  font-size: 12px;
  color: #909399;
  margin-top: 6px;
  padding: 0 4px;
}

.message-item.thinking .typing-indicator {
  display: flex;
  gap: 6px;
  padding: 12px 16px;
}

.typing-indicator span {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #c0c4cc;
  animation: typing 1.4s infinite;
}

.typing-indicator span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-indicator span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typing {
  0%, 60%, 100% {
    transform: translateY(0);
    opacity: 0.7;
  }
  30% {
    transform: translateY(-10px);
    opacity: 1;
  }
}

.input-container {
  display: flex;
  gap: 12px;
  padding: 16px;
  background: white;
  box-shadow: 0 -2px 4px rgba(0, 0, 0, 0.1);
}

.input-container .el-textarea {
  flex: 1;
}

.input-container .el-button {
  align-self: flex-end;
}

@media (max-width: 768px) {
  .message-content {
    max-width: 85%;
  }

  .dialogue-header h3 {
    font-size: 14px;
  }
}
</style>
