import { Component } from 'react'

export default class ErrorBoundary extends Component {
  state = { error: null }

  static getDerivedStateFromError(error) {
    return { error }
  }

  componentDidCatch(error, info) {
    console.error('ErrorBoundary:', error, info)
  }

  render() {
    if (this.state.error) {
      return (
        <div style={{
          display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center',
          minHeight: '100vh', padding: '24px', textAlign: 'center', gap: '12px', fontFamily: 'sans-serif',
        }}
        >
          <h1 style={{ fontSize: '1.25rem', fontWeight: 600 }}>Nimadir noto'g'ri ketdi</h1>
          <p style={{ color: '#666', maxWidth: '420px' }}>
            Sahifada kutilmagan xatolik yuz berdi. Sahifani qayta yuklab ko'ring - agar muammo
            davom etsa, birozdan so'ng qayta urinib ko'ring.
          </p>
          <button
            type="button"
            onClick={() => window.location.reload()}
            style={{
              padding: '10px 20px', borderRadius: '8px', border: 'none', background: '#4f46e5',
              color: 'white', fontWeight: 600, cursor: 'pointer',
            }}
          >
            Sahifani qayta yuklash
          </button>
        </div>
      )
    }
    return this.props.children
  }
}
