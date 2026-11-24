/**
 * 派森酱（Pyson-chan）—— 紫发双马尾的 AI 搭档。
 * 全 SVG 手绘，没有任何外部图片，换表情只是换几条路径。
 *
 * mood: normal | happy | thinking | worried | excited | wink | sleepy
 */

const MOUTH = {
  normal: "M 46 62 Q 50 66 54 62",
  happy: "M 43 60 Q 50 69 57 60",
  thinking: "M 45 63 L 53 62",
  worried: "M 44 65 Q 50 60 56 65",
  excited: "M 42 59 Q 50 71 58 59",
  wink: "M 44 61 Q 50 68 56 61",
  sleepy: "M 46 64 Q 50 66 54 64",
}

const BROW = {
  normal: null,
  happy: null,
  thinking: [
    "M 36 36 L 44 34",
    "M 56 34 L 64 36",
  ],
  worried: ["M 36 33 L 44 37", "M 56 37 L 64 33"],
  excited: ["M 36 32 L 44 30", "M 56 30 L 64 32"],
  wink: null,
  sleepy: null,
}

function Eye({ cx, closed, mood }) {
  if (closed) {
    return (
      <path
        d={`M ${cx - 5} 47 Q ${cx} 52 ${cx + 5} 47`}
        stroke="#3B2A5C"
        strokeWidth="2.4"
        strokeLinecap="round"
        fill="none"
      />
    )
  }
  const big = mood === "excited"
  return (
    <g>
      <ellipse cx={cx} cy="47" rx={big ? 6.4 : 5.6} ry={big ? 7.4 : 6.6} fill="#3B2A5C" />
      <circle cx={cx + 1.8} cy="44.6" r="2.1" fill="#FFFFFF" />
      <circle cx={cx - 1.9} cy="49.4" r="1.1" fill="#FFFFFF" opacity="0.75" />
      <ellipse cx={cx} cy="50.6" rx="3" ry="1.9" fill="#9B7BE8" opacity="0.55" />
    </g>
  )
}

export default function Mascot({ mood = "normal", size = 84, className = "", float = false }) {
  const brows = BROW[mood]
  const blushOn = ["happy", "excited", "wink"].includes(mood)

  return (
    <svg
      viewBox="0 0 100 100"
      width={size}
      height={size}
      className={`${float ? "animate-floaty" : ""} ${className}`}
      role="img"
      aria-label={`派森酱（${mood}）`}
    >
      {/* 双马尾（后层） */}
      <ellipse cx="19" cy="52" rx="9" ry="19" fill="#8B5CF6" transform="rotate(-14 19 52)" />
      <ellipse cx="81" cy="52" rx="9" ry="19" fill="#8B5CF6" transform="rotate(14 81 52)" />
      <circle cx="24" cy="34" r="4.6" fill="#EC6FA9" />
      <circle cx="76" cy="34" r="4.6" fill="#EC6FA9" />

      {/* 身体 */}
      <path d="M 32 96 Q 32 74 50 74 Q 68 74 68 96 Z" fill="#A78BFA" />
      <path d="M 44 74 L 50 84 L 56 74 Z" fill="#FFFFFF" opacity="0.9" />

      {/* 脸 */}
      <ellipse cx="50" cy="50" rx="27" ry="26" fill="#FFF3F8" />
      <ellipse cx="50" cy="50" rx="27" ry="26" fill="none" stroke="#DDCEFF" strokeWidth="1.6" />

      {/* 刘海 */}
      <path
        d="M 23 46 Q 24 22 50 22 Q 76 22 77 46 Q 70 32 58 30 Q 54 40 47 30 Q 32 32 23 46 Z"
        fill="#8B5CF6"
      />
      <path d="M 50 22 Q 62 23 68 31 Q 58 27 50 28 Z" fill="#A78BFA" />

      {/* 呆毛 */}
      <path
        d="M 50 22 Q 51 12 57 9"
        stroke="#8B5CF6"
        strokeWidth="3"
        strokeLinecap="round"
        fill="none"
      />

      {/* 眉毛 */}
      {brows?.map((d, i) => (
        <path key={i} d={d} stroke="#7C3AED" strokeWidth="2" strokeLinecap="round" fill="none" />
      ))}

      {/* 眼睛 */}
      <Eye cx={40} closed={mood === "sleepy"} mood={mood} />
      <Eye cx={60} closed={mood === "wink" || mood === "sleepy"} mood={mood} />

      {/* 腮红 */}
      {blushOn && (
        <>
          <ellipse cx="31" cy="58" rx="5.2" ry="3.2" fill="#F784B4" opacity="0.5" />
          <ellipse cx="69" cy="58" rx="5.2" ry="3.2" fill="#F784B4" opacity="0.5" />
        </>
      )}

      {/* 嘴 */}
      <path
        d={MOUTH[mood] || MOUTH.normal}
        stroke="#3B2A5C"
        strokeWidth="2.2"
        strokeLinecap="round"
        fill={mood === "excited" || mood === "happy" ? "#EC6FA9" : "none"}
      />

      {/* 心情小挂件 */}
      {mood === "excited" && (
        <g className="animate-sparkle">
          <path d="M 84 20 l 2 5 5 2 -5 2 -2 5 -2 -5 -5 -2 5 -2 z" fill="#F59E0B" />
          <path d="M 14 26 l 1.4 3.5 3.5 1.4 -3.5 1.4 -1.4 3.5 -1.4 -3.5 -3.5 -1.4 3.5 -1.4 z" fill="#F59E0B" />
        </g>
      )}
      {mood === "thinking" && (
        <g fill="#A78BFA">
          <circle cx="82" cy="30" r="2.4" />
          <circle cx="88" cy="24" r="3.4" />
          <circle cx="94" cy="16" r="4.4" />
        </g>
      )}
      {mood === "sleepy" && (
        <text x="78" y="26" fill="#A78BFA" fontSize="13" fontWeight="bold">
          z
        </text>
      )}
    </svg>
  )
}

/** 派森酱说话的气泡，全站统一样式 */
export function MascotSays({ mood = "normal", children, size = 56, tone = "magic" }) {
  const tones = {
    magic: "border-magic-100 bg-magic-50 text-ink",
    sakura: "border-sakura-200 bg-sakura-50 text-ink",
    mint: "border-mint-500/30 bg-mint-100 text-ink",
    amber: "border-amberly-500/30 bg-amberly-100 text-ink",
  }
  return (
    <div className="flex items-start gap-2.5">
      <Mascot mood={mood} size={size} className="shrink-0" />
      <div
        className={`relative mt-1.5 flex-1 rounded-2xl rounded-tl-sm border px-3.5 py-2.5 text-[14px] leading-relaxed ${tones[tone]}`}
      >
        {children}
      </div>
    </div>
  )
}
