export default function CoffeeCup() {
  return (
    <svg
      className="coffee-cup"
      viewBox="0 0 120 120"
      width="96"
      height="96"
      role="img"
      aria-label="Cup of coffee"
    >
      <g className="steam" fill="none" stroke="#8aa596" strokeWidth="4" strokeLinecap="round">
        <path d="M42 30 C34 22 50 16 42 8" />
        <path d="M60 30 C52 22 68 16 60 8" />
        <path d="M78 30 C70 22 86 16 78 8" />
      </g>

      <ellipse cx="60" cy="108" rx="46" ry="7" fill="#c9dccf" />

      <path
        d="M96 54 h8 a12 12 0 0 1 0 24 h-12"
        fill="none"
        stroke="#ffffff"
        strokeWidth="7"
        strokeLinecap="round"
      />
      <path
        d="M96 54 h8 a12 12 0 0 1 0 24 h-12"
        fill="none"
        stroke="#d9e6dd"
        strokeWidth="1.5"
        strokeLinecap="round"
      />

      <path d="M18 42 h84 v32 a30 30 0 0 1 -30 30 h-24 a30 30 0 0 1 -30 -30 z" fill="#ffffff" />
      <path
        d="M18 42 h84 v32 a30 30 0 0 1 -30 30 h-24 a30 30 0 0 1 -30 -30 z"
        fill="none"
        stroke="#d9e6dd"
        strokeWidth="1.5"
      />

      <ellipse cx="60" cy="42" rx="42" ry="8" fill="#fbfdfb" stroke="#d9e6dd" strokeWidth="1.5" />
      <ellipse cx="60" cy="43" rx="36" ry="5.5" fill="#6f4a33" />
      <ellipse cx="50" cy="42" rx="10" ry="1.8" fill="#8a6044" />
    </svg>
  )
}
