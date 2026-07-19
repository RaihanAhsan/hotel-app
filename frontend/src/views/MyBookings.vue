<template>
  <div class="page-bookings">
    <div class="container">
      <!-- Header -->
      <div class="bookings-header">
        <h2>My <span>Bookings</span></h2>
        <p style="color:#888;">View all your confirmed reservations.</p>
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
          <div class="status-wrapper">
            <span class="status" :class="b.status.toLowerCase()">
              {{ b.status }}
            </span>
            <!-- Indikator per order (hanya jika booking ini yang sedang menunggu) -->
            <span
              v-if="
                store.isWaitingForPayment &&
                store.pendingBookingId === b.id &&
                b.status.toLowerCase() === 'pending'
              "
              class="waiting-indicator"
            >
              ⏳ Menunggu konfirmasi...
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, onBeforeUnmount, ref, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useMainStore } from '../store'

const router = useRouter()
const route = useRoute()
const store = useMainStore()

// State
const loading = ref(true)
let pollingInterval = null
let pollingAttempts = 0
const MAX_POLLING_ATTEMPTS = 15 // 15 x 2 detik = 30 detik

// Computed
const sortedBookings = computed(() => {
  return [...store.bookings].sort((a, b) => b.id - a.id)
})

// Fungsi fetch data
const loadBookings = async () => {
  loading.value = true
  const data = await store.fetchBookings()
  loading.value = false
  return data
}

// Cek apakah ada booking yang sudah Paid
const hasPaidBooking = (bookings) => {
  return bookings.some(b => b.status && b.status.toLowerCase() === 'paid')
}

// Cek apakah booking dengan ID tertentu sudah Paid
const isBookingPaid = (bookings, bookingId) => {
  const booking = bookings.find(b => b.id === bookingId)
  return booking && booking.status && booking.status.toLowerCase() === 'paid'
}

// Mulai polling
const startPolling = (bookingId) => {
  if (pollingInterval) return

  pollingAttempts = 0
  store.startWaitingForPayment(bookingId)

  const poll = async () => {
    pollingAttempts++
    console.log(`🔄 Polling attempt ${pollingAttempts}/${MAX_POLLING_ATTEMPTS}`)

    const data = await store.fetchBookings()

    // Cek apakah booking yang ditunggu sudah Paid
    if (bookingId && isBookingPaid(data, bookingId)) {
      stopPolling()
      store.stopWaitingForPayment()
      return
    }

    if (pollingAttempts >= MAX_POLLING_ATTEMPTS) {
      console.log('⏰ Polling timeout')
      stopPolling()
      store.stopWaitingForPayment()
    }
  }

  poll()
  pollingInterval = setInterval(poll, 2000)
}

// Hentikan polling
const stopPolling = () => {
  if (pollingInterval) {
    clearInterval(pollingInterval)
    pollingInterval = null
  }
}

// ===== LIFECYCLE =====
onMounted(async () => {
  // 1. Load status waiting dari localStorage (untuk kasus refresh)
  store.loadWaitingState()

  // 2. Cek parameter URL
  const isPaymentSuccess = route.query.payment === 'success'
  const bookingIdFromUrl = route.query.booking_id
    ? Number(route.query.booking_id)
    : null

  // 3. Tentukan apakah perlu polling
  let shouldPoll = false
  let targetBookingId = null

  if (isPaymentSuccess && bookingIdFromUrl) {
    // Kasus: redirect dari Xendit dengan parameter lengkap
    shouldPoll = true
    targetBookingId = bookingIdFromUrl
    store.startWaitingForPayment(targetBookingId)
  } else if (store.isWaitingForPayment && store.pendingBookingId) {
    // Kasus: refresh halaman atau navigasi kembali
    shouldPoll = true
    targetBookingId = store.pendingBookingId
  }

  // 4. Load data awal
  const initialData = await loadBookings()

  // 5. Jika perlu polling dan belum ada booking yang Paid
  if (shouldPoll && targetBookingId) {
    const alreadyPaid = isBookingPaid(initialData, targetBookingId)
    if (alreadyPaid) {
      store.stopWaitingForPayment()
    } else {
      startPolling(targetBookingId)
    }
  } else {
    loading.value = false
  }
})

// Cleanup saat komponen unmount
onBeforeUnmount(() => {
  stopPolling()
})

// Watch: jika user login berubah, refresh data
watch(() => store.isLoggedIn, (newVal) => {
  if (newVal) {
    loadBookings()
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
.bookings-header h2 span {
  color: var(--gold);
}

/* Daftar Booking */
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

/* Status Wrapper */
.status-wrapper {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 4px;
}
.booking-item .status {
  padding: 4px 16px;
  border-radius: 50px;
  font-size: 0.75rem;
  font-weight: 600;
}
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
.waiting-indicator {
  font-size: 0.7rem;
  color: #856404;
  background: #fff3cd;
  padding: 2px 10px;
  border-radius: 12px;
  white-space: nowrap;
  font-weight: 500;
}

/* Empty state */
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
.btn-primary {
  background: var(--gold);
  border: none;
  color: #fff;
  padding: 12px 32px;
  border-radius: 40px;
  font-weight: 600;
  cursor: pointer;
  transition: var(--transition);
}
.btn-primary:hover {
  background: var(--dark-gold);
}

@media (max-width:768px) {
  .booking-item {
    grid-template-columns: 1fr;
    text-align: center;
  }
  .status-wrapper {
    align-items: center;
  }
}
</style>