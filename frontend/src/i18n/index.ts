import { createI18n } from 'vue-i18n'
import en from './en.json'
import sv from './sv.json'

export const i18n = createI18n({
  legacy: false,
  locale: navigator.language.split('-')[0] || 'en',
  fallbackLocale: 'en',
  messages: {
    en,
    sv
  }
})

export const availableLocales = [
  { code: 'en', name: 'English' },
  { code: 'sv', name: 'Svenska' }
]
