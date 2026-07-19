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
    // ===== TAMBAHKAN INI =====
    isWaitingForPayment: false,     // status polling aktif
    pendingBookingId: null,         // ID booking yang sedang ditunggu
    // ===== END =====
    toast: {
      message: '',
      type: 'success',
      visible: false
    }
  }),

  getters: {
    isLoggedIn: (state) => !!state.user,
    getRoomById: (state) => (id) => state.rooms.find(r => r.id === id),
  },

  actions: {
  // ===== TAMBAHKAN INI =====
  startWaitingForPayment(bookingId) {
    this.isWaitingForPayment = true
    this.pendingBookingId = bookingId
    // Simpan ke localStorage agar persist saat refresh
    localStorage.setItem('waiting_for_payment', 'true')
    localStorage.setItem('pending_booking_id', String(bookingId))
  },
  stopWaitingForPayment() {
    this.isWaitingForPayment = false
    this.pendingBookingId = null
    localStorage.removeItem('waiting_for_payment')
    localStorage.removeItem('pending_booking_id')
  },
  loadWaitingState() {
    const waiting = localStorage.getItem('waiting_for_payment') === 'true'
    const id = localStorage.getItem('pending_booking_id')
    if (waiting && id) {
      this.isWaitingForPayment = true
      this.pendingBookingId = Number(id)
    }
  },

    // ===== ROOMS =====
    async fetchRooms() {
      try {
        const res = await api.get('/rooms/')
        this.rooms = res.data
        console.log('✅ Rooms fetched from API:', this.rooms)
        return this.rooms
      } catch (error) {
        console.error('❌ Failed to fetch rooms, using fallback data:', error)
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

    // ===== AUTH =====
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

    // ===== BOOKINGS =====
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
    console.log('📤 Sending booking to backend:', data) // Tambahkan log
    const res = await api.post('/bookings/', data)
    console.log('📥 Booking response:', res.data) // Tambahkan log
    await this.fetchBookings()
    return { success: true, data: res.data }
  } catch (error) {
    console.error('❌ Booking error:', error)
    return {
      success: false,
      message: error.response?.data?.detail || 'Booking failed'
    }
  }
},

    // ===== MODALS =====
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

    // ===== SESSION =====
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
