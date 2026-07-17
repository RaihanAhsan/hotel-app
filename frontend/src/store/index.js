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
        const res = await api.get('/rooms/')
        this.rooms = res.data
        console.log('✅ Rooms fetched from API:', this.rooms)
        return this.rooms
      } catch (error) {
        console.error('❌ Failed to fetch rooms, using fallback data:', error)
        // Fallback data jika API gagal (CORS, network, dll)
        this.rooms = [
          {
            id: 'deluxe',
            name: 'Deluxe Skyline',
            price: 220,
            image: 'https://images.pexels.com/photos/258154/pexels-photo-258154.jpeg?auto=compress&cs=tinysrgb&w=600',
            description: 'Floor-to-ceiling windows, king bed, marble bathroom, and a private balcony.',
            features: ['King Bed', 'City View', 'Marble Bath', 'Balcony']
          },
          {
            id: 'executive',
            name: 'Executive Suite',
            price: 380,
            image: 'https://images.pexels.com/photos/271618/pexels-photo-271618.jpeg?auto=compress&cs=tinysrgb&w=600',
            description: 'Spacious living area, separate bedroom, and a private terrace with skyline views.',
            features: ['King Bed', 'Living Area', 'Terrace', 'Skyline View']
          },
          {
            id: 'penthouse',
            name: 'Penthouse Collection',
            price: 590,
            image: 'https://images.pexels.com/photos/279746/pexels-photo-279746.jpeg?auto=compress&cs=tinysrgb&w=600',
            description: 'Top-floor luxury with panoramic views, private terrace, and dedicated butler service.',
            features: ['Panoramic View', 'Private Terrace', 'Butler Service', 'King Bed']
          }
        ]
        return this.rooms
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
        const data = {
        ...bookingData,
        card_last4: bookingData.card_last4 || 'DUMMY'
        }
        // Pastikan panggil dengan trailing slash '/bookings/'
        const res = await api.post('/bookings/', data)
        await this.fetchBookings()
        return { success: true, data: res.data }
    } catch (error) {
        console.error('Booking error:', error)
        return {
        success: false,
        message: error.response?.data?.detail || 'Booking failed'
        }
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
    const timestamp = now.getFullYear() + 
        String(now.getMonth() + 1).padStart(2, '0') + 
        String(now.getDate()).padStart(2, '0') + 
        String(now.getHours()).padStart(2, '0') + 
        String(now.getMinutes()).padStart(2, '0') + 
        String(now.getSeconds()).padStart(2, '0')
    const random = String(Math.floor(Math.random() * 1000)).padStart(3, '0')
    return `GRAND-${timestamp}-${random}`
    }
  }
})