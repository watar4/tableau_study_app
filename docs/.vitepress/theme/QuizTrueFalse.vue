<template>
  <section class="quiz">
    <header class="quiz-header">
      <h3 class="quiz-title">章末クイズ</h3>
      <p class="quiz-score">正答 {{ correctCount }} / {{ questions.length }} 問</p>
    </header>

    <div v-for="(q, i) in questions" :key="q.id" class="quiz-item">
      <p class="quiz-statement">
        <span class="quiz-num">Q{{ i + 1 }}.</span>
        {{ q.statement }}
      </p>
      <div class="quiz-buttons">
        <button
          type="button"
          class="quiz-btn"
          :class="buttonClass(q, true)"
          @click="answer(q, true)"
        >○ 正しい</button>
        <button
          type="button"
          class="quiz-btn"
          :class="buttonClass(q, false)"
          @click="answer(q, false)"
        >× 誤り</button>
      </div>
      <div
        v-if="answered(q)"
        class="quiz-result"
        :class="{ correct: isCorrect(q), incorrect: !isCorrect(q) }"
      >
        <p class="quiz-judge">
          {{ isCorrect(q) ? '正解です' : '不正解です' }}
          （正解: {{ q.answer ? '○' : '×' }}）
        </p>
        <p class="quiz-explanation">{{ q.explanation }}</p>
      </div>
    </div>

    <p v-if="allAnswered" class="quiz-completion">
      この章のクイズはすべて回答済みです。
      <button type="button" class="quiz-reset" @click="reset">回答をリセット</button>
    </p>
  </section>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'

interface Question {
  id: string
  statement: string
  answer: boolean
  explanation: string
}

interface Result {
  choice: boolean
  correct: boolean
}

const props = defineProps<{
  chapterId: string
  questions: Question[]
}>()

const results = ref<Record<string, Result>>({})

const storageKey = computed(() => `tableau-study-app:quiz:${props.chapterId}`)

onMounted(() => {
  if (typeof window === 'undefined') return
  try {
    const raw = window.localStorage.getItem(storageKey.value)
    if (raw) results.value = JSON.parse(raw)
  } catch (_) {
    // ignore parse / storage errors
  }
})

watch(
  results,
  (v) => {
    if (typeof window === 'undefined') return
    try {
      window.localStorage.setItem(storageKey.value, JSON.stringify(v))
    } catch (_) {
      // ignore storage errors
    }
  },
  { deep: true }
)

const answer = (q: Question, choice: boolean) => {
  results.value = {
    ...results.value,
    [q.id]: { choice, correct: choice === q.answer }
  }
}

const answered = (q: Question) => results.value[q.id] !== undefined
const isCorrect = (q: Question) => results.value[q.id]?.correct === true

const buttonClass = (q: Question, choice: boolean) => {
  if (!answered(q)) return ''
  const chosen = results.value[q.id]?.choice
  if (chosen === choice) {
    return chosen === q.answer ? 'btn-correct' : 'btn-incorrect'
  }
  return 'btn-dim'
}

const correctCount = computed(
  () => props.questions.filter((q) => isCorrect(q)).length
)

const allAnswered = computed(
  () => props.questions.every((q) => answered(q))
)

const reset = () => {
  results.value = {}
}
</script>
