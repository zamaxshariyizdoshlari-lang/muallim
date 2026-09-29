import { beforeEach, describe, expect, it, vi } from 'vitest'
import { isSpeechSupported, speak } from './speech'

describe('speech', () => {
  beforeEach(() => {
    delete window.speechSynthesis
    window.SpeechSynthesisUtterance = vi.fn(function SpeechSynthesisUtterance(text) {
      this.text = text
    })
  })

  it('isSpeechSupported is false without window.speechSynthesis', () => {
    expect(isSpeechSupported()).toBe(false)
  })

  it('speak does nothing (no throw) when unsupported', () => {
    expect(() => speak('merhaba')).not.toThrow()
  })

  it('speak does nothing for empty text even when supported', () => {
    window.speechSynthesis = { cancel: vi.fn(), speak: vi.fn(), getVoices: () => [] }
    speak('')
    expect(window.speechSynthesis.speak).not.toHaveBeenCalled()
  })

  it('speak calls speechSynthesis.speak when supported', () => {
    window.speechSynthesis = { cancel: vi.fn(), speak: vi.fn(), getVoices: () => [] }
    speak('merhaba', 'tr-TR')
    expect(window.speechSynthesis.speak).toHaveBeenCalledTimes(1)
  })
})
