import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import RichText from './RichText'

describe('RichText', () => {
  it('renders plain text unchanged', () => {
    render(<RichText text="oddiy matn" />)
    expect(screen.getByText('oddiy matn')).toBeInTheDocument()
  })

  it('renders **bold** as <strong>', () => {
    render(<RichText text="bu **muhim** so'z" />)
    const strong = screen.getByText('muhim')
    expect(strong.tagName).toBe('STRONG')
  })

  it('renders ==highlight== as <mark>', () => {
    render(<RichText text="bu ==testda chiqadi== deb yozilgan" />)
    const mark = screen.getByText('testda chiqadi')
    expect(mark.tagName).toBe('MARK')
  })

  it('handles multiple markers in one string', () => {
    render(<RichText text="**birinchi** va ==ikkinchi==" />)
    expect(screen.getByText('birinchi').tagName).toBe('STRONG')
    expect(screen.getByText('ikkinchi').tagName).toBe('MARK')
  })

  it('returns null for empty text', () => {
    const { container } = render(<RichText text="" />)
    expect(container).toBeEmptyDOMElement()
  })
})
