<template>
  <Header />
  <router-view />
  <Footer />
  <AuthModal />
  <ConfirmModal />
</template>

<script setup>
import Header from './components/Header.vue'
import Footer from './components/Footer.vue'
import AuthModal from './components/AuthModal.vue'
import ConfirmModal from './components/ConfirmModal.vue'
import { useMainStore } from './store'
import { onMounted } from 'vue'

const store = useMainStore()

onMounted(async () => {
  await store.loadUserFromToken()
  await store.fetchRooms()  // ← penting
})
</script>