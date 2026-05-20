import DefaultTheme from 'vitepress/theme'
import type { Theme } from 'vitepress'
import QuizTrueFalse from './QuizTrueFalse.vue'
import ProgressBadge from './ProgressBadge.vue'
import './style.css'

const theme: Theme = {
  extends: DefaultTheme,
  enhanceApp({ app }) {
    app.component('QuizTrueFalse', QuizTrueFalse)
    app.component('ProgressBadge', ProgressBadge)
  }
}

export default theme
