<template>
  <div class="page-bookings">
    <div class="container">
      <!-- Header -->
      <div class="bookings-header">
        <h2>My <span>Bookings</span></h2>
        <p style="color:#888;">View all your confirmed reservations.</p>
      </div>

      <!-- Indikator Polling (tampil saat menunggu pembayaran) -->
      <div v-if="isPolling" class="polling-indicator">
        <i class="fas fa-spinner fa-spin" style="margin-right:10px;"></i>
        Menunggu konfirmasi pembayaran...
      </div>

      <!-- Belum Login -->
      <div v-if="!store.isLoggedIn" class="booking-empty">
        <i class="fas fa-lock"></i>
        <h3>Please Sign In</h3>
        <p>Sign in to view your booking history.</p>
        <button class="btn btn-primary" style="margin-top:16px;" @click="store.openAuthModal('login')">
          Sign In Now
        </button>
      </div>

      <!-- Sudah Login tapi belum ada booking -->
      <div v-else-if="store.bookings.length === 0 && !loading" class="booking-empty">
        <i class="fas fa-calendar-plus"></i>
        <h3>No Bookings Yet</h3>
        <p>You haven't made any reservations. Start planning your luxury stay today.</p>
        <button class="btn btn-primary" style="margin-top:16px;" @click="router.push('/rooms')">
          Book Now
        </button>
      </div>

      <!-- Loading -->
      <div v-else-if="loading" class="booking-empty">
        <i class="fas fa-spinner fa-spin" style="font-size:2rem;color:var(--gold);"></i>
        <p style="margin-top:16px;">Loading your bookings...</p>
      </div>

      <!-- Daftar Booking -->
      <div v-else class="booking-list">
        <div v-for="b in sortedBookings" :key="b.id" class="booking-item">
          <div class="info">
            <div class="booking-id">#{{ b.ref }}</div>
            <h4>{{ b.room }}</h4>
            <p>
              <i class="far fa-calendar-alt" style="margin-right:6px;"></i>
              {{ b.checkin }} — {{ b.checkout }} &nbsp;·&nbsp;
              <i class="fas fa-user" style="margin-right:4px;"></i> {{ b.guests }} guest(s)
              &nbsp;·&nbsp;
              <strong>${{ b.total.toLocaleString() }}</strong>
            </p>
            <p style="font-size:0.8rem;color:#999;margin-top:2px;">
              <i class="fas fa-credit-card" style="margin-right:4px;"></i>
              Paid with card ending in {{ b.card_last4 || '••••' }}
            </p>
          </div>
          <span class="status" :class="b.status.toLowerCase()">
            {{ b.status }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useMainStore } from '../store'

const router = useRouter()
const route = useRoute()
const store = useMainStore()

// State untuk polling & loading
const loading = ref(true)
const isPolling = ref(false)

// Urutkan booking berdasarkan ID (terbaru di atas)
const sortedBookings = computed(() => {
  return [...store.bookings].sort((a, b) => b.id - a.id)
})

// Fungsi untuk fetch data dari store
const loadBookings = async () => {
  loading.value = true
  const data = await store.fetchBookings()
  loading.value = false
  return data
}

// Cek apakah booking sudah ada yang berstatus 'Paid'
const hasPaidBooking = (bookings) => {
  return bookings.some(b => b.status && b.status.toLowerCase() === 'paid')
}

// Polling: cek data setiap 2 detik
const startPolling = () => {
  isPolling.value = true
  let attempts = 0
  const maxAttempts = 12 // total 24 detik (12 x 2 detik)

  const poll = async () => {
    attempts++
    console.log(`🔄 Polling attempt ${attempts}/${maxAttempts}`)
    
    const data = await store.fetchBookings()
    
    // Jika ada booking yang sudah Paid, hentikan polling
    if (hasPaidBooking(data) || attempts >= maxAttempts) {
      isPolling.value = false
      loading.value = false
      console.log('✅ Polling selesai')
      return
    }
    
    // Lanjutkan polling jika belum mencapai batas
    if (attempts < maxAttempts) {
      setTimeout(poll, 2000)
    } else {
      isPolling.value = false
      loading.value = false
      console.log('⏰ Polling timeout')
    }
  }

  // Mulai polling
  poll()
}

// Lifecycle: saat halaman dimuat
onMounted(async () => {
  // Cek apakah ada parameter ?payment=success di URL
  const isPaymentSuccess = route.query.payment === 'success'

  if (isPaymentSuccess) {
    console.log('🎯 Detected payment success redirect, starting polling...')
    
    // Load data awal
    const initialData = await loadBookings()
    
    // Jika belum ada yang Paid, mulai polling
    if (!hasPaidBooking(initialData)) {
      startPolling()
    } else {
      loading.value = false
    }
  } else {
    // Load normal (tanpa polling)
    await loadBookings()
    loading.value = false
  }
})
</script>

<style scoped>
.page-bookings {
  padding: 140px 0 80px;
  background: var(--cream);
  min-height: 100vh;
}
.bookings-header {
  margin-bottom: 40px;
}
.bookings-header h2 {
  font-family: 'Cormorant Garamond', serif;
  font-size: 2.6rem;
  font-weight: 700;
  color: var(--dark);
}
.bookings-header h2 span { color: var(--gold); }

/* Polling Indicator */
.polling-indicator {
  background: #fff3cd;
  color: #856404;
  padding: 12px 24px;
  border-radius: 8px;
  margin-bottom: 24px;
  text-align: center;
  font-weight: 500;
  border: 1px solid #ffc107;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

.booking-list {
  display: flex;
  flex-direction: column;
  gap: 24px;
}
.booking-item {
  background: var(--white);
  border-radius: var(--radius);
  padding: 28px 32px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 20px;
  align-items: center;
  border-left: 4px solid var(--gold);
  transition: var(--transition);
}
.booking-item:hover {
  box-shadow: var(--shadow-dark);
}
.booking-item .info h4 {
  font-family: 'Cormorant Garamond', serif;
  font-size: 1.2rem;
  font-weight: 700;
  color: var(--dark);
}
.booking-item .info p {
  color: #666;
  font-size: 0.9rem;
  margin-top: 4px;
}
.booking-item .info .booking-id {
  font-size: 0.75rem;
  color: #999;
  font-weight: 500;
}
.booking-item .status {
  padding: 4px 16px;
  border-radius: 50px;
  font-size: 0.75rem;
  font-weight: 600;
}

/* Status colors */
.booking-item .status.paid {
  background: #e8f5e9;
  color: #2e7d32;
}
.booking-item .status.pending {
  background: #fff3e0;
  color: #e65100;
}
.booking-item .status.cancelled {
  background: #ffebee;
  color: #c62828;
}

.booking-empty {
  text-align: center;
  padding: 80px 20px;
  color: #888;
}
.booking-empty i {
  font-size: 4rem;
  color: #ddd;
  margin-bottom: 16px;
}
.booking-empty h3 {
  font-family: 'Cormorant Garamond', serif;
  font-size: 1.8rem;
  color: var(--dark);
}

@media (max-width:768px) {
  .booking-item {
    grid-template-columns: 1fr;
    text-align: center;
  }
  .booking-item .status { justify-self: center; }
}
</style>