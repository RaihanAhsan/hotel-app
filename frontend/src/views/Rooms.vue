<template>
  <div class="page-select-room">
    <div class="container">
      <div class="select-room-header">
        <h2>Choose Your <span>Suite</span></h2>
        <p>Select the room that best fits your stay. Each offers a unique experience.</p>
      </div>
      <div class="select-room-grid">
        <div v-for="room in store.rooms" :key="room.id" class="select-room-card" @click="selectRoom(room.id)">
          <div class="img-wrap"><img :src="room.image" :alt="room.name" loading="lazy" /></div>
          <div class="body">
            <h3>{{ room.name }}</h3>
            <div class="price">${{ room.price }} <small>/ night</small></div>
            <p>{{ room.description }}</p>
            <div class="features">
              <span v-for="(f, idx) in room.features" :key="idx">{{ f }}</span>
            </div>
            <button class="btn btn-primary" @click.stop="selectRoom(room.id)">Select This Room</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useMainStore } from '../store'

const router = useRouter()
const store = useMainStore()

const selectRoom = (roomId) => {
  if (!store.isLoggedIn) {
    store.pendingRoomId = roomId
    store.openAuthModal('login')
    return
  }
  store.selectedRoomId = roomId
  router.push('/booking')
}
</script>

<style scoped>
.page-select-room {
  padding: 140px 0 80px;
  background: var(--cream);
  min-height: 100vh;
}
.select-room-header {
  text-align: center;
  margin-bottom: 48px;
}
.select-room-header h2 {
  font-family: 'Cormorant Garamond', serif;
  font-size: 2.8rem;
  font-weight: 700;
  color: var(--dark);
}
.select-room-header h2 span { color: var(--gold); }
.select-room-header p {
  color: #888;
  font-size: 1rem;
  margin-top: 8px;
}
.select-room-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 40px;
}
.select-room-card {
  background: var(--white);
  border-radius: var(--radius);
  overflow: hidden;
  transition: var(--transition);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
  border: 2px solid transparent;
  cursor: pointer;
}
.select-room-card:hover {
  transform: translateY(-8px);
  box-shadow: var(--shadow-dark);
}
.select-room-card .img-wrap {
  height: 240px;
  overflow: hidden;
}
.select-room-card .img-wrap img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: var(--transition);
}
.select-room-card:hover .img-wrap img { transform: scale(1.03); }
.select-room-card .body { padding: 28px 28px 32px; }
.select-room-card .body h3 {
  font-family: 'Cormorant Garamond', serif;
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--dark);
}
.select-room-card .body .price {
  font-size: 1.6rem;
  font-weight: 700;
  color: var(--gold);
  margin: 4px 0 8px;
}
.select-room-card .body .price small {
  font-size: 0.85rem;
  font-weight: 400;
  color: #888;
}
.select-room-card .body p {
  color: #666;
  font-size: 0.95rem;
  margin: 8px 0 16px;
}
.select-room-card .body .features {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 16px;
}
.select-room-card .body .features span {
  background: var(--cream);
  padding: 4px 14px;
  border-radius: 50px;
  font-size: 0.75rem;
  color: #555;
}
.select-room-card .body .btn { width: 100%; padding: 14px; }
@media (max-width:768px) {
  .select-room-grid { grid-template-columns: 1fr; }
}
</style>