<template>
  <div class="auth-overlay" :class="{ open: store.isAuthModalOpen }" @click.self="store.closeAuthModal()">
    <div class="auth-box">
      <button class="close-auth" @click="store.closeAuthModal()">&times;</button>
      <h2>{{ authTitle }}</h2>
      <p class="auth-sub">{{ authSub }}</p>
      <div class="auth-error" v-if="errorMessage">{{ errorMessage }}</div>
      <form @submit.prevent="handleSubmit">
        <div v-if="authMode === 'register'" class="form-group">
          <label><i class="far fa-user" style="margin-right:6px;"></i>Full Name</label>
          <input type="text" v-model="form.name" placeholder="John Doe" required />
        </div>
        <div class="form-group">
          <label><i class="far fa-envelope" style="margin-right:6px;"></i>Email</label>
          <input type="email" v-model="form.email" placeholder="john@example.com" required />
        </div>
        <div class="form-group">
          <label><i class="fas fa-lock" style="margin-right:6px;"></i>Password</label>
          <input type="password" v-model="form.password" placeholder="••••••••" required minlength="4" />
        </div>
        <button type="submit" class="btn btn-primary" style="width:100%;padding:16px;font-size:1rem;">
          {{ submitLabel }}
        </button>
      </form>
      <div class="auth-switch">
        <span>{{ switchText }}</span>
        <a @click="toggleMode">{{ switchLink }}</a>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useMainStore } from '../store'
import { useRouter } from 'vue-router'

const store = useMainStore()
const router = useRouter()

const form = ref({ name: '', email: '', password: '' })
const errorMessage = ref('')

const authMode = computed(() => store.authMode)

const authTitle = computed(() => 
  authMode.value === 'login' ? 'Welcome Back' : 'Create Account'
)
const authSub = computed(() => 
  authMode.value === 'login' 
    ? 'Sign in to access your exclusive booking.' 
    : 'Join The Grand Jakarta and enjoy exclusive benefits.'
)
const submitLabel = computed(() => 
  authMode.value === 'login' ? 'Sign In' : 'Register'
)
const switchText = computed(() => 
  authMode.value === 'login' ? "Don't have an account?" : "Already have an account?"
)
const switchLink = computed(() => 
  authMode.value === 'login' ? 'Register' : 'Sign In'
)

const toggleMode = () => {
  store.authMode = authMode.value === 'login' ? 'register' : 'login'
  errorMessage.value = ''
  form.value = { name: '', email: '', password: '' }
}

const handleSubmit = async () => {
  errorMessage.value = ''
  const { name, email, password } = form.value
  
  let result
  if (authMode.value === 'login') {
    result = await store.login(email, password)
  } else {
    if (!name) {
      errorMessage.value = 'Please enter your full name.'
      return
    }
    result = await store.register(name, email, password)
  }
  
  if (result.success) {
    store.closeAuthModal()
    form.value = { name: '', email: '', password: '' }
    
    const pending = store.pendingRoomId
    if (pending) {
      store.pendingRoomId = null
      store.selectedRoomId = pending
      router.push('/booking')
    } else if (router.currentRoute.value.path === '/') {
      // stay on home
    } else {
      router.push('/rooms')
    }
  } else {
    errorMessage.value = result.message
  }
}

watch(() => store.isAuthModalOpen, (open) => {
  if (open) {
    form.value = { name: '', email: '', password: '' }
    errorMessage.value = ''
  }
})
</script>

<style scoped>
.auth-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(12px);
  z-index: 2000;
  display: none;
  align-items: center;
  justify-content: center;
  padding: 20px;
}
.auth-overlay.open { display: flex; }
.auth-box {
  background: var(--white);
  border-radius: var(--radius);
  padding: 48px 44px;
  max-width: 460px;
  width: 100%;
  box-shadow: var(--shadow-dark);
  position: relative;
  animation: slideUp 0.4s ease;
}
.auth-box .close-auth {
  position: absolute;
  top: 16px;
  right: 20px;
  background: none;
  border: none;
  font-size: 1.8rem;
  cursor: pointer;
  color: #aaa;
  transition: var(--transition);
}
.auth-box .close-auth:hover {
  color: var(--dark);
  transform: rotate(90deg);
}
.auth-box h2 {
  font-family: 'Cormorant Garamond', serif;
  font-size: 2.2rem;
  font-weight: 700;
  color: var(--dark);
  margin-bottom: 4px;
}
.auth-box .auth-sub {
  color: #888;
  font-size: 0.95rem;
  margin-bottom: 28px;
}
.auth-box .form-group {
  margin-bottom: 18px;
}
.auth-box .form-group label {
  display: block;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #555;
  margin-bottom: 6px;
}
.auth-box .form-group input {
  width: 100%;
  padding: 14px 18px;
  border: 1px solid #e0ddd8;
  border-radius: 12px;
  font-family: 'Inter', sans-serif;
  font-size: 0.95rem;
  background: var(--cream);
  transition: var(--transition);
  outline: none;
  color: var(--dark);
}
.auth-box .form-group input:focus {
  border-color: var(--gold);
  box-shadow: 0 0 0 4px rgba(200, 161, 101, 0.12);
  background: var(--white);
}
.auth-box .auth-error {
  background: #fee;
  color: #c0392b;
  padding: 12px 16px;
  border-radius: 10px;
  font-size: 0.85rem;
  margin-bottom: 16px;
}
.auth-box .auth-switch {
  text-align: center;
  margin-top: 18px;
  font-size: 0.9rem;
  color: #888;
}
.auth-box .auth-switch a {
  color: var(--gold);
  font-weight: 600;
  cursor: pointer;
  transition: var(--transition);
}
.auth-box .auth-switch a:hover { color: var(--gold-dark); }
@keyframes slideUp {
  0% { opacity: 0; transform: translateY(30px) scale(0.96); }
  100% { opacity: 1; transform: translateY(0) scale(1); }
}
@media (max-width:480px) {
  .auth-box { padding: 32px 24px; }
}
</style>