import { defineStore } from 'pinia'
import api from '../api/client'

export const useMainStore = defineStore('main', {
  state: () => ({
    user: null,
    rooms: [],
    bookings: [],
    selectedRoomId: null,
    pendingRoomId: null,
    isAuthModalOpen: false,
    authMode: 'login',
    isConfirmModalOpen: false,
    confirmBookingRef: '',
  }),
  
  getters: {
    isLoggedIn: (state) => !!state.user,
    getRoomById: (state) => (id) => state.rooms.find(r => r.id === id),
  },
  
  actions: {
    async fetchRooms() {
      try {
        const res = await api.get('/rooms')
        this.rooms = res.data
        return res.data
      } catch (error) {
        console.error('Failed to fetch rooms:', error)
        return []
      }
    },
    
    async login(email, password) {
      try {
        const res = await api.post('/auth/login', { email, password })
        localStorage.setItem('access_token', res.data.access_token)
        this.user = res.data.user
        return { success: true, user: res.data.user }
      } catch (error) {
        return { success: false, message: error.response?.data?.detail || 'Login failed' }
      }
    },
    
    async register(name, email, password) {
      try {
        const res = await api.post('/auth/register', { name, email, password })
        localStorage.setItem('access_token', res.data.access_token)
        this.user = res.data.user
        return { success: true, user: res.data.user }
      } catch (error) {
        return { success: false, message: error.response?.data?.detail || 'Registration failed' }
      }
    },
    
    logout() {
      localStorage.removeItem('access_token')
      this.user = null
      this.selectedRoomId = null
      this.pendingRoomId = null
    },
    
    async fetchBookings() {
      if (!this.user) return []
      try {
        const res = await api.get(`/bookings?email=${this.user.email}`)
        this.bookings = res.data
        return res.data
      } catch (error) {
        console.error('Failed to fetch bookings:', error)
        return []
      }
    },
    
    async createBooking(bookingData) {
      try {
        const res = await api.post('/bookings', bookingData)
        await this.fetchBookings()
        return { success: true, data: res.data }
      } catch (error) {
        return { success: false, message: error.response?.data?.detail || 'Booking failed' }
      }
    },
    
    openAuthModal(mode = 'login') {
      this.authMode = mode
      this.isAuthModalOpen = true
    },
    
    closeAuthModal() {
      this.isAuthModalOpen = false
    },
    
    openConfirmModal(ref) {
      this.confirmBookingRef = ref
      this.isConfirmModalOpen = true
    },
    
    closeConfirmModal() {
      this.isConfirmModalOpen = false
    },
    
    async loadUserFromToken() {
      const token = localStorage.getItem('access_token')
      if (!token) return null
      try {
        const res = await api.get('/auth/me')
        this.user = res.data
        return res.data
      } catch (error) {
        localStorage.removeItem('access_token')
        this.user = null
        return null
      }
    },
    
    generateBookingRef() {
      const now = new Date()
      const year = now.getFullYear()
      const seq = String(this.bookings.length + 1).padStart(4, '0')
      return `GRAND-${year}-${seq}`
    }
  }
})