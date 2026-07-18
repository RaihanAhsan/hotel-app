<template>
  <div class="page-booking">
    <div class="container">
      <div class="booking-layout">
        <!-- FORM BOOKING -->
        <div class="booking-form-wrap">
          <h2 class="form-title">Complete Your <span style="color:var(--gold);">Reservation</span></h2>
          <p class="form-sub" v-if="selectedRoom">Room: {{ selectedRoom.name }}</p>
          <p class="form-sub" v-else>Please select a room first.</p>
          
          <form @submit.prevent="openConfirmPopup">
            <div class="form-row">
              <div class="form-group">
                <label><i class="far fa-user" style="margin-right:6px;"></i>Full Name</label>
                <input type="text" v-model="form.fullName" placeholder="Mr. John Doe" required />
              </div>
              <div class="form-group">
                <label><i class="far fa-envelope" style="margin-right:6px;"></i>Email</label>
                <input type="email" v-model="form.email" placeholder="john@example.com" required />
              </div>
            </div>
            <div class="form-row">
              <div class="form-group">
                <label><i class="far fa-calendar-alt" style="margin-right:6px;"></i>Check-in</label>
                <input type="date" v-model="form.checkin" required />
              </div>
              <div class="form-group">
                <label><i class="far fa-calendar-alt" style="margin-right:6px;"></i>Check-out</label>
                <input type="date" v-model="form.checkout" required />
              </div>
            </div>
            <div class="form-row">
              <div class="form-group">
                <label><i class="fas fa-user-friends" style="margin-right:6px;"></i>Guests</label>
                <select v-model="form.guests">
                  <option v-for="n in 5" :key="n" :value="n">{{ n }} Guest{{ n > 1 ? 's' : '' }}</option>
                  <option value="5">5+ Guests</option>
                </select>
              </div>
              <div class="form-group">
                <label><i class="fas fa-bed" style="margin-right:6px;"></i>Room Type</label>
                <select v-model="form.roomId" @change="onRoomChange">
                  <option v-for="r in store.rooms" :key="r.id" :value="r.id">
                    {{ r.name }} – ${{ r.price }}/night
                  </option>
                </select>
              </div>
            </div>
            
            <!-- PAYMENT METHOD - QRIS / VIRTUAL ACCOUNT (DUMMY) -->
            <div style="margin-top:8px;border-top:1px solid #eee;padding-top:20px;">
              <p style="font-weight:600;font-size:0.85rem;color:#555;margin-bottom:16px;">
                <i class="fas fa-credit-card" style="margin-right:8px;color:var(--gold);"></i>Payment Method
              </p>
              <div class="payment-method-grid">
                <div 
                  class="payment-method-card" 
                  :class="{ active: form.paymentMethod === 'qris' }"
                  @click="form.paymentMethod = 'qris'"
                >
                  <i class="fas fa-qrcode"></i>
                  <span>QRIS</span>
                  <small>Scan with any e-wallet</small>
                </div>
                <div 
                  class="payment-method-card" 
                  :class="{ active: form.paymentMethod === 'va' }"
                  @click="form.paymentMethod = 'va'"
                >
                  <i class="fas fa-university"></i>
                  <span>Virtual Account</span>
                  <small>BCA / Mandiri / BNI</small>
                </div>
              </div>
              <div v-if="form.paymentMethod === 'qris'" class="payment-dummy-info">
                <i class="fas fa-check-circle" style="color:#4caf50;"></i>
                <span>QRIS Code akan muncul setelah konfirmasi (Dummy)</span>
              </div>
              <div v-else-if="form.paymentMethod === 'va'" class="payment-dummy-info">
                <i class="fas fa-check-circle" style="color:#4caf50;"></i>
                <span>Virtual Account: 8888-{{ dummyVA }} akan muncul setelah konfirmasi (Dummy)</span>
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
              <i class="fas fa-shield-alt" style="margin-right:6px;"></i>Secure payment · No credit card stored
            </p>
          </form>
        </div>
        
        <!-- SIDEBAR DENGAN TESTIMONIAL RUNNING -->
        <div class="booking-sidebar">
          <!-- Card alasan booking langsung -->
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

          <!-- TESTIMONIAL RUNNING / AUTO SCROLL -->
          <div class="sidebar-card testimonial-running-card">
            <h4>
              <i class="fas fa-comment-dots" style="color:var(--gold);"></i> 
              Guest Stories 
              
            </h4>
            <div class="testimonial-track-wrap">
              <div class="testimonial-track" ref="testimonialTrack">
                <div 
                  v-for="(item, idx) in runningTestimonials" 
                  :key="idx" 
                  class="testimonial-item"
                >
                  <div class="testimonial-avatar">
                    <span>{{ item.avatar }}</span>
                  </div>
                  <div class="testimonial-content">
                    <div class="testimonial-author">
                      <strong>{{ item.name }}</strong>
                      <span>· {{ item.location }}</span>
                      <span class="testimonial-rating">
                        <i v-for="s in item.stars" :key="s" class="fas fa-star" style="color:var(--gold);font-size:0.7rem;"></i>
                      </span>
                    </div>
                    <p class="testimonial-text">“{{ item.comment }}”</p>
                    <span class="testimonial-time">{{ item.time }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 5-Star Signature -->
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
          
          <!-- Need Help -->
          <div class="sidebar-card">
            <h4><i class="fas fa-phone-alt"></i> Need Help?</h4>
            <p style="font-size:0.9rem;color:#666;">Our concierge team is available 24/7.</p>
            <p style="font-size:1.1rem;font-weight:600;color:var(--gold);margin-top:8px;">
              <i class="fas fa-phone" style="margin-right:8px;"></i> +62 21 555 1234
            </p>
            <p style="font-size:0.85rem;color:#888;">
              <i class="fas fa-envelope" style="margin-right:6px;"></i> concierge@thegrandjakarta.com
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- CONFIRMATION POPUP -->
    <div class="confirm-overlay" :class="{ open: showConfirmPopup }" @click.self="showConfirmPopup = false">
      <div class="confirm-box">
        <div class="icon-check"><i class="fas fa-clipboard-check" style="color:var(--gold);"></i></div>
        <h2>Confirm Your Booking</h2>
        <div class="confirm-details">
          <p><strong>Room:</strong> {{ selectedRoom?.name }}</p>
          <p><strong>Guest:</strong> {{ form.fullName }}</p>
          <p><strong>Check-in:</strong> {{ form.checkin }} → {{ form.checkout }}</p>
          <p><strong>Guests:</strong> {{ form.guests }}</p>
          <p><strong>Payment:</strong> {{ form.paymentMethod === 'qris' ? 'QRIS' : 'Virtual Account' }}</p>
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
import { ref, computed, watch, onMounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import { useMainStore } from '../store'

const router = useRouter()
const store = useMainStore()

const showConfirmPopup = ref(false)
const isSubmitting = ref(false)

// --- Data Testimonial untuk Running Comment ---
const testimonialData = [
  { name: 'Mr. Thompson', location: 'London, UK', comment: 'An extraordinary stay — the views from the pool are breathtaking. The butler anticipated our every wish.', stars: 5, time: 'Just now' },
  { name: 'Dr. A. Rahman', location: 'Singapore', comment: 'The penthouse suite is a masterpiece. We felt like royalty. Already planning our return.', stars: 5, time: '2 min ago' },
  { name: 'Sarah & Mike', location: 'Australia', comment: 'Incredible service! The staff made our anniversary unforgettable. Highly recommend the Sky Spa.', stars: 5, time: '4 min ago' },
  { name: 'James K.', location: 'USA', comment: 'Best hotel in Jakarta. The infinity pool at sunset is magical. Will come back again.', stars: 5, time: '7 min ago' },
  { name: 'Lina W.', location: 'Germany', comment: 'The design is stunning and the food is divine. A true 5-star experience.', stars: 5, time: '12 min ago' },
  { name: 'Mr. & Mrs. Chen', location: 'China', comment: 'Our suite was perfect. The butler service was top-notch. Absolutely loved it.', stars: 5, time: '18 min ago' },
  { name: 'Emily R.', location: 'France', comment: 'Everything was perfect, from check-in to check-out. The staff are so welcoming.', stars: 5, time: '25 min ago' },
  { name: 'David P.', location: 'Canada', comment: 'Amazing rooftop pool and bar. The city skyline view is unbeatable.', stars: 5, time: '32 min ago' },
  { name: 'Maria G.', location: 'Spain', comment: 'The Grand Jakarta exceeded all expectations. Luxury at its finest.', stars: 5, time: '45 min ago' },
  { name: 'Tom & Jerry', location: 'Netherlands', comment: 'Great location, amazing facilities, and the breakfast buffet is world-class.', stars: 5, time: '1 hour ago' },
  // tambahkan lebih banyak jika mau
];

// Perbanyak data agar running terlihat ramai (duplikasi)
const runningTestimonials = ref([...testimonialData, ...testimonialData, ...testimonialData]);

// Ref untuk track animasi
const testimonialTrack = ref(null);
let animationId = null;
let scrollPosition = 0;

// Fungsi untuk auto scroll testimonial
const startAutoScroll = () => {
  if (!testimonialTrack.value) return;
  const track = testimonialTrack.value;
  // Hentikan animasi sebelumnya jika ada
  if (animationId) {
    cancelAnimationFrame(animationId);
    animationId = null;
  }

  let lastTimestamp = 0;
  const speed = 0.6; // piksel per frame (kecepatan)

  const step = (timestamp) => {
    if (!lastTimestamp) lastTimestamp = timestamp;
    const delta = timestamp - lastTimestamp;
    lastTimestamp = timestamp;

    // Geser ke atas
    scrollPosition -= speed * (delta / 16); // normalisasi 60fps
    track.style.transform = `translateY(${scrollPosition}px)`;

    // Jika sudah melewati satu set, reset ke posisi awal
    const firstItemHeight = track.firstElementChild?.offsetHeight || 80;
    const totalHeight = track.scrollHeight / 3; // karena kita duplikasi 3x
    if (Math.abs(scrollPosition) >= totalHeight) {
      scrollPosition = 0;
      track.style.transform = `translateY(0px)`;
    }

    animationId = requestAnimationFrame(step);
  };

  animationId = requestAnimationFrame(step);
};

// Hentikan animasi saat komponen unmount
onBeforeUnmount(() => {
  if (animationId) {
    cancelAnimationFrame(animationId);
    animationId = null;
  }
});

// Mulai animasi setelah DOM siap
onMounted(() => {
  startAutoScroll();
  // Jika window di-resize, restart animasi
  window.addEventListener('resize', () => {
    if (animationId) {
      cancelAnimationFrame(animationId);
      animationId = null;
    }
    scrollPosition = 0;
    if (testimonialTrack.value) {
      testimonialTrack.value.style.transform = 'translateY(0px)';
    }
    startAutoScroll();
  });
});

// --- Form Data ---
const form = ref({
  fullName: '',
  email: '',
  checkin: '',
  checkout: '',
  guests: 2,
  roomId: '',
  paymentMethod: 'qris',
});

const selectedRoom = computed(() => {
  return store.rooms.find(r => r.id === form.value.roomId)
});

const totalAmount = computed(() => {
  if (!selectedRoom.value) return 0
  const nights = calcNights(form.value.checkin, form.value.checkout)
  return selectedRoom.value.price * nights
});

const dummyVA = computed(() => {
  return String(Math.floor(10000000 + Math.random() * 90000000))
});

const calcNights = (start, end) => {
  if (!start || !end) return 1
  const d1 = new Date(start)
  const d2 = new Date(end)
  const diff = (d2 - d1) / (1000 * 60 * 60 * 24)
  return Math.max(1, Math.round(diff))
};

const setDefaultDates = () => {
  const today = new Date()
  const tomorrow = new Date(today)
  tomorrow.setDate(tomorrow.getDate() + 1)
  const ymd = d => d.toISOString().split('T')[0]
  if (!form.value.checkin) form.value.checkin = ymd(today)
  if (!form.value.checkout) form.value.checkout = ymd(tomorrow)
};

const onRoomChange = () => {
  // update total
};

const openConfirmPopup = () => {
  if (!selectedRoom.value) {
    alert('Please select a room.')
    return
  }
  if (!form.value.fullName || !form.value.email) {
    alert('Please fill in your name and email.')
    return
  }
  if (!form.value.checkin || !form.value.checkout) {
    alert('Please select check-in and check-out dates.')
    return
  }
  if (!form.value.paymentMethod) {
    alert('Please select a payment method.')
    return
  }
  showConfirmPopup.value = true
};

const submitBooking = async () => {
  if (isSubmitting.value) return
  
  isSubmitting.value = true
  
  const nights = calcNights(form.value.checkin, form.value.checkout)
  const total = selectedRoom.value.price * nights
  const ref = store.generateBookingRef()
  
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
    special: `Payment: ${form.value.paymentMethod === 'qris' ? 'QRIS' : 'Virtual Account'}`,
    card_last4: form.value.paymentMethod === 'qris' ? 'QRIS' : 'VA',
    status: 'Confirmed'
  }
  
  const result = await store.createBooking(bookingData)
  
  isSubmitting.value = false
  showConfirmPopup.value = false
  
  if (result.success) {
    store.openConfirmModal(ref)
    // Reset form
    form.value.fullName = store.user?.name || ''
    form.value.email = store.user?.email || ''
    form.value.paymentMethod = 'qris'
    setDefaultDates()
    if (store.rooms.length) {
      form.value.roomId = store.rooms[0].id
    }
  } else {
    alert(result.message || 'Booking failed. Please try again.')
  }
};

// Watch selectedRoomId dari store
watch(() => store.selectedRoomId, (newId) => {
  if (newId && store.rooms.length) {
    form.value.roomId = newId
  }
}, { immediate: true });

// Set user data dan default dates
onMounted(() => {
  if (store.user) {
    form.value.fullName = store.user.name || ''
    form.value.email = store.user.email || ''
  }
  setDefaultDates()
  if (store.rooms.length && !form.value.roomId) {
    form.value.roomId = store.selectedRoomId || store.rooms[0]?.id
  }
});

if (!store.selectedRoomId && store.rooms.length) {
  store.selectedRoomId = store.rooms[0]?.id
}
</script>

<style scoped>
/* ===== LAYOUT ===== */
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
  grid-template-columns: 1fr 1fr;
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
  background: #e8f5e9;
  padding: 12px 16px;
  border-radius: 10px;
  font-size: 0.85rem;
  color: #2e7d32;
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

/* ===== SIDEBAR ===== */
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

/* ===== TESTIMONIAL RUNNING / AUTO SCROLL ===== */
.testimonial-running-card {
  overflow: hidden;
  padding-bottom: 20px;
}
.live-badge {
  font-size: 0.6rem;
  background: #ff4444;
  color: white;
  padding: 2px 10px;
  border-radius: 20px;
  margin-left: 8px;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  animation: pulse-live 1.5s infinite;
}
@keyframes pulse-live {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}

.testimonial-track-wrap {
  position: relative;
  height: 400px;
  overflow: hidden;
  border-radius: 12px;
  background: var(--cream);
  padding: 8px 4px;
}

.testimonial-track {
  display: flex;
  flex-direction: column;
  gap: 12px;
  will-change: transform;
}

.testimonial-item {
  display: flex;
  gap: 14px;
  background: var(--white);
  padding: 14px 16px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  flex-shrink: 0;
  border-left: 3px solid var(--gold);
}

.testimonial-avatar {
  flex-shrink: 0;
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: var(--gold-light);
  color: var(--gold-dark);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 1.1rem;
  text-transform: uppercase;
}

.testimonial-content {
  flex: 1;
  min-width: 0;
}
.testimonial-author {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 6px;
  font-size: 0.85rem;
}
.testimonial-author strong {
  color: var(--dark);
}
.testimonial-author span {
  color: #888;
  font-size: 0.75rem;
}
.testimonial-rating {
  display: inline-flex;
  gap: 2px;
}
.testimonial-text {
  font-style: italic;
  color: #555;
  font-size: 0.9rem;
  margin: 4px 0 2px;
  line-height: 1.5;
}
.testimonial-time {
  font-size: 0.65rem;
  color: #aaa;
  display: block;
  margin-top: 2px;
}

/* ===== CONFIRM POPUP ===== */
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

/* ===== RESPONSIVE ===== */
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
  .payment-method-grid { grid-template-columns: 1fr; }
  .booking-sidebar { grid-template-columns: 1fr; }
  .testimonial-track-wrap { height: 300px; }
}
@media (max-width:480px) {
  .confirm-box { padding: 32px 20px; }
}
</style>