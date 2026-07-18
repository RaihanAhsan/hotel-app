<template>
  <div class="page-booking">
    <div class="container">
      <div class="booking-layout">
        <div class="booking-form-wrap">
          <h2 class="form-title">Complete Your <span style="color:var(--gold);">Reservation</span></h2>
          <p class="form-sub" v-if="selectedRoom">Room: {{ selectedRoom.name }}</p>
          <p class="form-sub" v-else>Please select a room first.</p>

          <form @submit.prevent="openConfirmPopup">
            <div class="form-row">
              <div class="form-group">
                <label><i class="far fa-user"></i> Full Name</label>
                <input type="text" v-model="form.fullName" placeholder="Mr. John Doe" required />
              </div>
              <div class="form-group">
                <label><i class="far fa-envelope"></i> Email</label>
                <input type="email" v-model="form.email" placeholder="john@example.com" required />
              </div>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label><i class="far fa-calendar-alt"></i> Check-in</label>
                <input type="date" v-model="form.checkin" required />
              </div>
              <div class="form-group">
                <label><i class="far fa-calendar-alt"></i> Check-out</label>
                <input type="date" v-model="form.checkout" required />
              </div>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label><i class="fas fa-user-friends"></i> Guests</label>
                <select v-model="form.guests">
                  <option v-for="n in 5" :key="n" :value="n">{{ n }} Guest{{ n > 1 ? 's' : '' }}</option>
                  <option value="5">5+ Guests</option>
                </select>
              </div>
              <div class="form-group">
                <label><i class="fas fa-bed"></i> Room Type</label>
                <select v-model="form.roomId" @change="onRoomChange">
                  <option v-for="r in store.rooms" :key="r.id" :value="r.id">
                    {{ r.name }} – ${{ r.price }}/night
                  </option>
                </select>
              </div>
            </div>

            <!-- Payment Method -->
            <div style="margin-top:8px;border-top:1px solid #eee;padding-top:20px;">
              <p style="font-weight:600;font-size:0.85rem;color:#555;margin-bottom:16px;">
                <i class="fas fa-credit-card" style="margin-right:8px;color:var(--gold);"></i>Payment Method
              </p>
              <div class="payment-method-grid">
                <div 
                  class="payment-method-card" 
                  :class="{ active: form.paymentMethod === 'xendit' }"
                  @click="form.paymentMethod = 'xendit'"
                >
                  <i class="fas fa-credit-card"></i>
                  <span>Pay with Xendit</span>
                  <small>Credit Card, VA, QRIS, E-Wallet</small>
                </div>
              </div>
              <div class="payment-dummy-info" style="background:#e3f2fd;color:#0d47a1;">
                <i class="fas fa-check-circle"></i>
                <span>You will be redirected to Xendit secure payment page</span>
              </div>
            </div>

            <div class="payment-summary-box">
              <span><strong>Total Payment</strong></span>
              <span class="total">${{ totalAmount }}</span>
            </div>

            <button type="submit" class="btn btn-primary" style="width:100%;padding:18px;font-size:1rem;">
              <i class="fas fa-lock" style="margin-right:12px;"></i>Review &amp; Confirm Booking
            </button>
            <p style="margin-top:16px;font-size:0.75rem;color:#999;text-align:center;">
              <i class="fas fa-shield-alt" style="margin-right:6px;"></i>Secure payment · Powered by Xendit
            </p>
          </form>
        </div>

        <!-- Sidebar -->
        <div class="booking-sidebar">
          <div class="sidebar-card">
            <h4><i class="fas fa-info-circle"></i> Why Book Direct?</h4>
            <ul>
              <li><i class="fas fa-check-circle"></i> Best rate guaranteed</li>
              <li><i class="fas fa-check-circle"></i> Free breakfast for two</li>
              <li><i class="fas fa-check-circle"></i> Complimentary airport transfer</li>
              <li><i class="fas fa-check-circle"></i> Late checkout (subject to availability)</li>
              <li><i class="fas fa-check-circle"></i> Access to Sky Spa &amp; pool</li>
            </ul>
          </div>
          <div class="sidebar-card">
            <h4><i class="fas fa-star" style="color:var(--gold);"></i> Guest Stories</h4>
            <div class="testimonial-card">
              <p>"An extraordinary stay — the views from the pool are simply breathtaking."</p>
              <div class="author">— Mr. &amp; Mrs. Thompson <span> · London</span></div>
            </div>
            <div class="testimonial-card" style="margin-top:12px;">
              <p>"The penthouse suite is a masterpiece. We felt like royalty."</p>
              <div class="author">— Dr. A. Rahman <span> · Singapore</span></div>
            </div>
          </div>
          <div class="sidebar-card">
            <h4><i class="fas fa-crown"></i> 5-Star Signature</h4>
            <ul>
              <li><i class="fas fa-check"></i> 24/7 Personal Butler</li>
              <li><i class="fas fa-check"></i> Michelin-starred Dining</li>
              <li><i class="fas fa-check"></i> Rooftop Infinity Pool</li>
              <li><i class="fas fa-check"></i> Award-winning Spa</li>
              <li><i class="fas fa-check"></i> Private City Tours</li>
            </ul>
          </div>
          <div class="sidebar-card">
            <h4><i class="fas fa-phone-alt"></i> Need Help?</h4>
            <p style="font-size:0.9rem;color:#666;">Our concierge team is available 24/7.</p>
            <p style="font-size:1.1rem;font-weight:600;color:var(--gold);margin-top:8px;">
              <i class="fas fa-phone" style="margin-right:8px;"></i> +62 21 555 1234
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Confirmation Popup -->
    <div class="confirm-overlay" :class="{ open: showConfirmPopup }" @click.self="showConfirmPopup = false">
      <div class="confirm-box">
        <div class="icon-check"><i class="fas fa-clipboard-check" style="color:var(--gold);"></i></div>
        <h2>Confirm Your Booking</h2>
        <div class="confirm-details">
          <p><strong>Room:</strong> {{ selectedRoom?.name }}</p>
          <p><strong>Guest:</strong> {{ form.fullName }}</p>
          <p><strong>Check-in:</strong> {{ form.checkin }} → {{ form.checkout }}</p>
          <p><strong>Guests:</strong> {{ form.guests }}</p>
          <p><strong>Payment:</strong> Xendit</p>
          <p style="font-size:1.4rem;color:var(--gold);font-weight:700;">Total: ${{ totalAmount }}</p>
        </div>
        <div style="display:flex;gap:16px;justify-content:center;flex-wrap:wrap;margin-top:20px;">
          <button class="btn btn-primary" @click="submitBooking" :disabled="isSubmitting">
            <i v-if="isSubmitting" class="fas fa-spinner fa-spin" style="margin-right:8px;"></i>
            {{ isSubmitting ? 'Processing...' : 'Confirm Booking' }}
          </button>
          <button class="btn btn-outline-dark" @click="showConfirmPopup = false">Cancel</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useMainStore } from '../store'
import api from '../api/client'

const router = useRouter()
const store = useMainStore()

const showConfirmPopup = ref(false)
const isSubmitting = ref(false)

const form = ref({
  fullName: '',
  email: '',
  checkin: '',
  checkout: '',
  guests: 2,
  roomId: '',
  paymentMethod: 'xendit',
})

const selectedRoom = computed(() => {
  return store.rooms.find(r => r.id === form.value.roomId)
})

const totalAmount = computed(() => {
  if (!selectedRoom.value) return 0
  const nights = calcNights(form.value.checkin, form.value.checkout)
  return selectedRoom.value.price * nights
})

const calcNights = (start, end) => {
  if (!start || !end) return 1
  const d1 = new Date(start)
  const d2 = new Date(end)
  const diff = (d2 - d1) / (1000 * 60 * 60 * 24)
  return Math.max(1, Math.round(diff))
}

const setDefaultDates = () => {
  const today = new Date()
  const tomorrow = new Date(today)
  tomorrow.setDate(tomorrow.getDate() + 1)
  const ymd = d => d.toISOString().split('T')[0]
  if (!form.value.checkin) form.value.checkin = ymd(today)
  if (!form.value.checkout) form.value.checkout = ymd(tomorrow)
}

const onRoomChange = () => {}

const openConfirmPopup = () => {
  if (!selectedRoom.value) {
    store.showToast('Please select a room.', 'error')
    return
  }
  if (!form.value.fullName || !form.value.email) {
    store.showToast('Please fill in your name and email.', 'error')
    return
  }
  if (!form.value.checkin || !form.value.checkout) {
    store.showToast('Please select check-in and check-out dates.', 'error')
    return
  }
  showConfirmPopup.value = true
}

const submitBooking = async () => {
  if (isSubmitting.value) return

  isSubmitting.value = true

  const nights = calcNights(form.value.checkin, form.value.checkout)
  const total = selectedRoom.value.price * nights
  const ref = store.generateBookingRef()

  // 1. Simpan booking ke database
  const bookingData = {
    ref,
    guest: form.value.fullName,
    email: form.value.email,
    room: selectedRoom.value.name,
    room_id: form.value.roomId,
    checkin: form.value.checkin,
    checkout: form.value.checkout,
    guests: form.value.guests,
    nights,
    total,
    special: 'Payment via Xendit',
    card_last4: 'XENDIT',
    status: 'Pending'
  }

  const result = await store.createBooking(bookingData)

  if (!result.success) {
    isSubmitting.value = false
    showConfirmPopup.value = false
    store.showToast(result.message || 'Booking failed', 'error')
    return
  }

  // 2. Buat invoice di Xendit
  try {
    const invoiceData = {
      booking_id: result.data.id,
      amount: total,
      payer_email: form.value.email,
      payer_name: form.value.fullName,
      room_name: selectedRoom.value.name,
      checkin: form.value.checkin,
      checkout: form.value.checkout,
      guests: form.value.guests
    }

    const invoiceResponse = await api.post('/payment/create-invoice', invoiceData)

    if (invoiceResponse.data.success) {
      // Redirect ke halaman pembayaran Xendit
      window.location.href = invoiceResponse.data.invoice_url
    } else {
      store.showToast('Failed to create payment invoice', 'error')
      isSubmitting.value = false
      showConfirmPopup.value = false
    }
  } catch (error) {
    console.error('Payment error:', error)
    store.showToast('Payment processing failed', 'error')
    isSubmitting.value = false
    showConfirmPopup.value = false
  }
}

watch(() => store.selectedRoomId, (newId) => {
  if (newId && store.rooms.length) {
    form.value.roomId = newId
  }
}, { immediate: true })

onMounted(() => {
  if (store.user) {
    form.value.fullName = store.user.name || ''
    form.value.email = store.user.email || ''
  }
  setDefaultDates()
  if (store.rooms.length && !form.value.roomId) {
    form.value.roomId = store.selectedRoomId || store.rooms[0]?.id
  }
})

if (!store.selectedRoomId && store.rooms.length) {
  store.selectedRoomId = store.rooms[0]?.id
}
</script>

<style scoped>
/* ===== Gaya sama seperti sebelumnya, tidak diubah ===== */
.page-booking {
  background: var(--cream);
  padding-top: 140px;
  padding-bottom: 80px;
  min-height: 100vh;
}
.booking-layout {
  display: grid;
  grid-template-columns: 1fr 380px;
  gap: 48px;
  align-items: start;
}
.booking-form-wrap {
  background: var(--white);
  border-radius: var(--radius);
  padding: 48px;
  box-shadow: var(--shadow-dark);
}
.booking-form-wrap .form-title {
  font-family: 'Cormorant Garamond', serif;
  font-size: 2.4rem;
  font-weight: 700;
  color: var(--dark);
  margin-bottom: 4px;
}
.booking-form-wrap .form-sub {
  color: #888;
  margin-bottom: 32px;
  font-size: 0.95rem;
}
.form-group {
  margin-bottom: 22px;
}
.form-group label {
  display: block;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #555;
  margin-bottom: 6px;
}
.form-group input,
.form-group select {
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
.form-group input:focus,
.form-group select:focus {
  border-color: var(--gold);
  box-shadow: 0 0 0 4px rgba(200, 161, 101, 0.12);
  background: var(--white);
}
.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}
.payment-method-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 16px;
  margin-bottom: 12px;
}
.payment-method-card {
  border: 2px solid #e0ddd8;
  border-radius: 12px;
  padding: 16px;
  text-align: center;
  cursor: pointer;
  transition: var(--transition);
  background: var(--cream);
}
.payment-method-card:hover {
  border-color: var(--gold-light);
}
.payment-method-card.active {
  border-color: var(--gold);
  background: rgba(200, 161, 101, 0.08);
  box-shadow: 0 0 0 4px rgba(200, 161, 101, 0.12);
}
.payment-method-card i {
  font-size: 2rem;
  color: var(--gold);
  display: block;
  margin-bottom: 4px;
}
.payment-method-card span {
  font-weight: 600;
  color: var(--dark);
  display: block;
}
.payment-method-card small {
  font-size: 0.7rem;
  color: #999;
}
.payment-dummy-info {
  padding: 12px 16px;
  border-radius: 10px;
  font-size: 0.85rem;
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 8px;
}
.payment-summary-box {
  background: var(--cream);
  border-radius: 12px;
  padding: 20px 24px;
  margin: 24px 0 32px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  border: 1px solid #e0ddd8;
}
.payment-summary-box .total {
  font-family: 'Cormorant Garamond', serif;
  font-size: 2.2rem;
  font-weight: 700;
  color: var(--gold);
}
.booking-sidebar {
  display: flex;
  flex-direction: column;
  gap: 32px;
}
.sidebar-card {
  background: var(--white);
  border-radius: var(--radius);
  padding: 32px 28px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
  border: 1px solid rgba(0, 0, 0, 0.04);
}
.sidebar-card h4 {
  font-family: 'Cormorant Garamond', serif;
  font-size: 1.3rem;
  font-weight: 700;
  color: var(--dark);
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  gap: 10px;
}
.sidebar-card h4 i { color: var(--gold); }
.sidebar-card ul li {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 10px 0;
  border-bottom: 1px solid rgba(0, 0, 0, 0.04);
  font-size: 0.9rem;
}
.sidebar-card ul li:last-child { border-bottom: none; }
.sidebar-card ul li i {
  color: var(--gold);
  width: 20px;
  text-align: center;
}
.testimonial-card {
  background: var(--cream);
  border-radius: 12px;
  padding: 24px;
  margin-top: 12px;
  border-left: 4px solid var(--gold);
}
.testimonial-card p {
  font-style: italic;
  color: #555;
  font-size: 0.95rem;
}
.testimonial-card .author {
  font-weight: 600;
  color: var(--dark);
  margin-top: 8px;
  font-style: normal;
}
.testimonial-card .author span {
  font-weight: 400;
  color: #888;
  font-size: 0.85rem;
}
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
  max-height: 90vh;
  overflow-y: auto;
}
.confirm-box .icon-check {
  font-size: 4rem;
  color: var(--gold);
  margin-bottom: 12px;
}
.confirm-box h2 {
  font-family: 'Cormorant Garamond', serif;
  font-size: 2rem;
  font-weight: 700;
  color: var(--dark);
  margin-bottom: 16px;
}
.confirm-details {
  text-align: left;
  background: var(--cream);
  padding: 20px;
  border-radius: 12px;
  margin: 12px 0;
}
.confirm-details p {
  margin: 6px 0;
  color: #555;
  font-size: 0.95rem;
}
.confirm-details p strong {
  color: var(--dark);
}
@keyframes slideUp {
  0% { opacity: 0; transform: translateY(30px) scale(0.96); }
  100% { opacity: 1; transform: translateY(0) scale(1); }
}
@media (max-width:1024px) {
  .booking-layout { grid-template-columns: 1fr; }
  .booking-sidebar {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 32px;
  }
}
@media (max-width:768px) {
  .booking-form-wrap { padding: 28px 20px; }
  .form-row { grid-template-columns: 1fr; }
  .booking-sidebar { grid-template-columns: 1fr; }
}
@media (max-width:480px) {
  .confirm-box { padding: 32px 20px; }
}
</style>