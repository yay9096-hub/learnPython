/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        ink: { DEFAULT: '#2E2545', soft: '#6B5F86', faint: '#9B8FB4' },
        paper: { DEFAULT: '#FDF9FF', card: '#FFFFFF', sunken: '#F4EDFB' },
        sakura: { 50: '#FFF1F7', 200: '#FBCFE3', 400: '#F784B4', 500: '#EC6FA9' },
        magic: { 50: '#F5F0FF', 100: '#EDE4FF', 200: '#DDCEFF', 400: '#A78BFA', 500: '#8B5CF6', 600: '#7C3AED' },
        mint: { 100: '#DCFCE7', 500: '#34D399', 600: '#10B981' },
        amberly: { 100: '#FEF3C7', 500: '#F59E0B' },
      },
      fontFamily: {
        round: ['"Segoe UI"', '"PingFang SC"', '"Microsoft YaHei"', 'system-ui', 'sans-serif'],
        mono: ['"Cascadia Code"', '"JetBrains Mono"', 'Consolas', '"Courier New"', 'monospace'],
      },
      boxShadow: {
        card: '0 2px 0 0 rgba(124,58,237,0.10), 0 8px 24px -12px rgba(124,58,237,0.30)',
        pop: '0 4px 0 0 rgba(124,58,237,0.20)',
      },
      keyframes: {
        pop: { '0%': { transform: 'scale(.6)', opacity: 0 }, '70%': { transform: 'scale(1.08)' }, '100%': { transform: 'scale(1)', opacity: 1 } },
        floaty: { '0%,100%': { transform: 'translateY(0)' }, '50%': { transform: 'translateY(-5px)' } },
        sparkle: { '0%,100%': { opacity: .3, transform: 'scale(.8)' }, '50%': { opacity: 1, transform: 'scale(1.15)' } },
      },
      animation: {
        pop: 'pop .28s cubic-bezier(.34,1.56,.64,1)',
        floaty: 'floaty 3.5s ease-in-out infinite',
        sparkle: 'sparkle 1.6s ease-in-out infinite',
      },
    },
  },
  plugins: [],
}
