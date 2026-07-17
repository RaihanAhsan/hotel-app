<template>
  <div class="confirm-overlay" :class="{ open: store.isConfirmModalOpen }" @click.self="store.closeConfirmModal()">
    <div class="confirm-box">
      <div class="icon-check"><i class="fas fa-check-circle"></i></div>
      <h2>Booking Confirmed!</h2>
      <p>Your reservation has been successfully processed.</p>
      <div class="booking-ref">#{{ store.confirmBookingRef }}</div>
      <p style="font-size:0.9rem;color:#666;">A confirmation email has been sent to your inbox.</p>
      <div style="display:flex;gap:16px;justify-content:center;flex-wrap:wrap;margin-top:24px;">
        <button class="btn btn-primary" @click="viewBookings">View My Bookings</button>
        <button class="btn btn-outline-dark" @click="continueExploring">Continue Exploring</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useMainStore } from '../store'
import { useRouter } from 'vue-router'

const store = useMainStore()
const router = useRouter()

const viewBookings = () => {
  store.closeConfirmModal()
  router.push('/my-bookings')
}

const continueExploring = () => {
  store.closeConfirmModal()
  router.push('/')
}
</script>

<style scoped>
.confirm-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(8px);
  z-index: 3000;
  display: none;
  align-items: center;
  justify-content: center;
  padding: 20px;
}
.confirm-overlay.open { display: flex; }
.confirm-box {
  background: var(--white);
  border-radius: var(--radius);
  padding: 48px 44px;
  max-width: 520px;
  width: 100%;
  text-align: center;
  animation: slideUp 0.4s ease;
}
.confirm-box .icon-check {
  font-size: 4rem;
  color: #4caf50;
  margin-bottom: 12px;
}
.confirm-box h2 {
  font-family: 'Cormorant Garamond', serif;
  font-size: 2rem;
  font-weight: 700;
  color: var(--dark);
}
.confirm-box p {
  color: #666;
  margin: 8px 0 20px;
}
.confirm-box .booking-ref {
  background: var(--cream);
  padding: 12px;
  border-radius: 10px;
  font-weight: 600;
  font-size: 1.1rem;
  color: var(--gold);
  margin-bottom: 20px;
}
@keyframes slideUp {
  0% { opacity: 0; transform: translateY(30px) scale(0.96); }
  100% { opacity: 1; transform: translateY(0) scale(1); }
}
@media (max-width:480px) {
  .confirm-box { padding: 32px 20px; }
}
</style>