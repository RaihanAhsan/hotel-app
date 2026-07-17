<template>
  <header :class="headerClass">
    <div class="container nav-wrap">
      <router-link class="logo" to="/">The Grand<span>Jakarta</span></router-link>
      
      <ul class="nav-links" :class="{ 'mobile-open': mobileOpen }">
        <li><router-link to="/" @click="mobileOpen=false">Home</router-link></li>
        <li><a href="#" @click.prevent="scrollToSection('rooms')">Suites</a></li>
        <li><a href="#" @click.prevent="scrollToSection('amenities')">Amenities</a></li>
        <li><a href="#" @click.prevent="scrollToSection('footer')">Contact</a></li>
      </ul>
      
      <div class="nav-actions">
        <div v-if="store.isLoggedIn" class="nav-user">
          <div class="user-avatar" @click="toggleDropdown">{{ userInitial }}</div>
          <span class="user-name">{{ store.user?.name }}</span>
          <div class="dropdown" :class="{ open: dropdownOpen }">
            <div class="user-info">
              {{ store.user?.name }}
              <small>{{ store.user?.email }}</small>
            </div>
            <div class="divider"></div>
            <a @click="goToBookings"><i class="fas fa-history" style="margin-right:10px;"></i>My Bookings</a>
            <a @click="handleLogout"><i class="fas fa-sign-out-alt" style="margin-right:10px;"></i>Logout</a>
          </div>
        </div>
        
        <button v-else class="btn btn-primary btn-sm" @click="store.openAuthModal('login')">
          <i class="fas fa-sign-in-alt" style="margin-right:8px;"></i>Sign In
        </button>
        
        <button class="hamburger" @click="mobileOpen = !mobileOpen" aria-label="Menu">
          <span></span><span></span><span></span>
        </button>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useMainStore } from '../store'

const store = useMainStore()
const router = useRouter()
const route = useRoute()
const mobileOpen = ref(false)
const dropdownOpen = ref(false)

const userInitial = computed(() => {
  if (!store.user) return ''
  return store.user.name.charAt(0).toUpperCase()
})

const isDarkHeader = computed(() => {
  return route.path === '/booking' || route.path === '/my-bookings'
})

const isScrolled = ref(false)

const headerClass = computed(() => {
  const classes = []
  if (isDarkHeader.value) classes.push('dark-header')
  if (isScrolled.value && !isDarkHeader.value) classes.push('scrolled')
  return classes.join(' ')
})

const handleScroll = () => {
  isScrolled.value = window.scrollY > 60
}

const toggleDropdown = (e) => {
  e.stopPropagation()
  dropdownOpen.value = !dropdownOpen.value
}

const closeDropdown = () => {
  dropdownOpen.value = false
}

const handleLogout = () => {
  dropdownOpen.value = false
  store.logout()
  router.push('/')
}

const goToBookings = () => {
  dropdownOpen.value = false
  router.push('/my-bookings')
}

const scrollToSection = (id) => {
  mobileOpen.value = false
  if (route.path !== '/') {
    router.push('/')
    setTimeout(() => {
      const el = document.getElementById(id)
      if (el) el.scrollIntoView({ behavior: 'smooth' })
    }, 300)
  } else {
    const el = document.getElementById(id)
    if (el) el.scrollIntoView({ behavior: 'smooth' })
  }
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
  document.addEventListener('click', closeDropdown)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
  document.removeEventListener('click', closeDropdown)
})
</script>

<style scoped>
header {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 1000;
  padding: 20px 0;
  transition: var(--transition);
  background: transparent;
}
header.scrolled {
  background: rgba(17, 17, 17, 0.92);
  backdrop-filter: blur(16px);
  padding: 12px 0;
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.2);
}
header.dark-header {
  background: rgba(17, 17, 17, 0.95) !important;
  backdrop-filter: blur(16px);
  padding: 12px 0;
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.2);
}
.nav-wrap {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.logo {
  font-family: 'Cormorant Garamond', serif;
  font-size: 2rem;
  font-weight: 700;
  color: var(--white);
  letter-spacing: 1px;
  cursor: pointer;
}
.logo span { color: var(--gold); }
.nav-links {
  display: flex;
  gap: 40px;
  align-items: center;
}
.nav-links a {
  font-size: 0.85rem;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.8);
  letter-spacing: 0.5px;
  transition: var(--transition);
  position: relative;
  cursor: pointer;
}
.nav-links a::after {
  content: '';
  position: absolute;
  bottom: -4px;
  left: 0;
  width: 0;
  height: 2px;
  background: var(--gold);
  transition: var(--transition);
}
.nav-links a:hover { color: var(--white); }
.nav-links a:hover::after { width: 100%; }
.nav-links a.router-link-active { color: var(--white); }
.nav-links a.router-link-active::after { width: 100%; }

.nav-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}
.nav-user {
  display: flex;
  align-items: center;
  gap: 12px;
  color: rgba(255, 255, 255, 0.8);
  font-size: 0.85rem;
  position: relative;
}
.nav-user .user-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: var(--gold);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--white);
  font-weight: 700;
  font-size: 0.9rem;
  cursor: pointer;
  transition: var(--transition);
}
.nav-user .user-avatar:hover { transform: scale(1.05); }
.nav-user .dropdown {
  display: none;
  position: absolute;
  top: 50px;
  right: 0;
  background: var(--white);
  border-radius: var(--radius);
  padding: 16px 0;
  min-width: 200px;
  box-shadow: var(--shadow-dark);
  z-index: 100;
  border: 1px solid rgba(0, 0, 0, 0.04);
}
.nav-user .dropdown.open { 
  display: block;
  animation: fadeIn 0.25s ease;
}
.nav-user .dropdown a {
  display: block;
  padding: 10px 24px;
  color: var(--text-body);
  font-size: 0.85rem;
  transition: var(--transition);
  cursor: pointer;
}
.nav-user .dropdown a:hover {
  background: var(--cream);
  color: var(--gold);
}
.nav-user .dropdown .divider {
  height: 1px;
  background: #eee;
  margin: 8px 16px;
}
.nav-user .dropdown .user-info {
  padding: 0 24px 8px;
  font-weight: 600;
  color: var(--dark);
  font-size: 0.9rem;
}
.nav-user .dropdown .user-info small {
  display: block;
  font-weight: 400;
  color: #888;
  font-size: 0.75rem;
}
.hamburger {
  display: none;
  flex-direction: column;
  gap: 5px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px;
}
.hamburger span {
  width: 30px;
  height: 2.5px;
  background: var(--white);
  border-radius: 4px;
  transition: var(--transition);
}
@media (max-width:768px) {
  .nav-links {
    display: none;
    flex-direction: column;
    position: absolute;
    top: 72px;
    left: 0;
    width: 100%;
    background: rgba(17, 17, 17, 0.98);
    backdrop-filter: blur(16px);
    padding: 32px 28px;
    gap: 20px;
    border-radius: 0 0 20px 20px;
  }
  .nav-links.mobile-open { display: flex; }
  .hamburger { display: flex; }
  .nav-user .user-name { display: none; }
}
</style>