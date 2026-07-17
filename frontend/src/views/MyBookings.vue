<template>
  <div class="page-bookings">
    <div class="container">
      <div class="bookings-header">
        <h2>My <span>Bookings</span></h2>
        <p style="color:#888;">View all your confirmed reservations.</p>
      </div>
      <div v-if="!store.isLoggedIn" class="booking-empty">
        <i class="fas fa-lock"></i>
        <h3>Please Sign In</h3>
        <p>Sign in to view your booking history.</p>
        <button class="btn btn-primary" style="margin-top:16px;" @click="store.openAuthModal('login')">
          Sign In Now
        </button>
      </div>
      <div v-else-if="store.bookings.length === 0" class="booking-empty">
        <i class="fas fa-calendar-plus"></i>
        <h3>No Bookings Yet</h3>
        <p>You haven't made any reservations. Start planning your luxury stay today.</p>
        <button class="btn btn-primary" style="margin-top:16px;" @click="router.push('/rooms')">
          Book Now
        </button>
      </div>
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
          <span class="status">{{ b.status }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useMainStore } from '../store'

const router = useRouter()
const store = useMainStore()

const sortedBookings = computed(() => {
  return [...store.bookings].sort((a, b) => b.id - a.id)
})

onMounted(async () => {
  if (store.isLoggedIn) {
    await store.fetchBookings()
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
  background: #e8f5e9;
  color: #2e7d32;
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