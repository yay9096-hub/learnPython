const BASE = "/api"

async function req(path, opts = {}) {
  const res = await fetch(BASE + path, {
    headers: { "Content-Type": "application/json" },
    ...opts,
  })
  if (!res.ok) {
    let detail = res.statusText
    try {
      detail = (await res.json()).detail || detail
    } catch {
      /* 后端没返回 json，就用状态文本 */
    }
    throw new Error(detail)
  }
  return res.status === 204 ? null : res.json()
}

const post = (p, body) => req(p, { method: "POST", body: JSON.stringify(body ?? {}) })
const put = (p, body) => req(p, { method: "PUT", body: JSON.stringify(body ?? {}) })

export const api = {
  listDays: () => req("/days"),
  getDay: (day) => req(`/days/${day}`),
  getSolution: (day) => req(`/days/${day}/solution`),
  cheatsheet: () => req("/cheatsheet"),
  myData: () => req("/my-data"),

  saveCode: (day, code) => put(`/progress/${day}/code`, { code }),
  recordRun: (day, kind, payload) => post(`/progress/${day}/run`, { kind, payload }),
  recordHint: (day, level) => post(`/progress/${day}/hint`, { kind: "hint", payload: { level } }),
  recordExercise: (day, exercise_id) => post(`/progress/${day}/exercise`, { exercise_id }),
  recordTime: (day, seconds) => post(`/progress/${day}/time`, { kind: "time", payload: { seconds } }),
  complete: (day, body) => post(`/progress/${day}/complete`, body),

  gallery: () => req("/gallery"),
  saveWork: (day, body) => put(`/gallery/${day}`, body),
}

/** 存后端失败也不该打断她写代码，所以所有埋点都走这个静默包装 */
export function quietly(promise) {
  return Promise.resolve(promise).catch((e) => {
    console.warn("[api] 后端没响应，先忽略：", e.message)
    return null
  })
}
