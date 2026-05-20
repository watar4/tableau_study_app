<template>
  <section class="progress-badge">
    <h3 class="progress-title">学習進捗</h3>
    <p v-if="total === 0" class="progress-empty">
      まだクイズに回答していません。各章末のクイズに回答すると、この画面に進捗が表示されます。
    </p>
    <template v-else>
      <p class="progress-summary">
        全 {{ total }} 問中 {{ correct }} 問正答（{{ percentage }}%）
      </p>
      <div class="progress-bar">
        <div class="progress-fill" :style="{ width: percentage + '%' }"></div>
      </div>
      <button type="button" class="progress-reset" @click="clearAll">
        すべての進捗をリセット
      </button>
    </template>
  </section>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'

const STORAGE_PREFIX = 'tableau-study-app:quiz:'

const correct = ref(0)
const total = ref(0)

const refresh = () => {
  if (typeof window === 'undefined') return
  let c = 0
  let t = 0
  try {
    for (let i = 0; i < window.localStorage.length; i++) {
      const key = window.localStorage.key(i)
      if (!key || !key.startsWith(STORAGE_PREFIX)) continue
      const raw = window.localStorage.getItem(key)
      if (!raw) continue
      const parsed = JSON.parse(raw) as Record<string, { choice: boolean; correct: boolean }>
      for (const v of Object.values(parsed)) {
        t += 1
        if (v && v.correct) c += 1
      }
    }
  } catch (_) {
    // ignore
  }
  correct.value = c
  total.value = t
}

const clearAll = () => {
  if (typeof window === 'undefined') return
  if (!window.confirm('全章のクイズ回答をリセットします。よろしいですか?')) return
  const keys: string[] = []
  for (let i = 0; i < window.localStorage.length; i++) {
    const key = window.localStorage.key(i)
    if (key && key.startsWith(STORAGE_PREFIX)) keys.push(key)
  }
  keys.forEach((k) => window.localStorage.removeItem(k))
  refresh()
}

onMounted(refresh)

const percentage = computed(() =>
  total.value === 0 ? 0 : Math.round((correct.value / total.value) * 100)
)
</script>
