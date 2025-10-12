import { reactive } from 'vue'

const API_BASE = '/api'

// -------------------- normalize --------------------
function normalizeItem(p = {}) {
    const categories = Array.isArray(p.categories) ? p.categories : []
    const filetypes = Array.isArray(p.filetypes) ? p.filetypes : []
    const degrees = Array.isArray(p.degrees) ? p.degrees : []
    const supervisors = Array.isArray(p.supervisors) ? p.supervisors : []

    return {
        id: String(p.projectID ?? p.id ?? ''),
        title: p.project_name ?? p.title ?? '',
        abstract: p.description ?? p.abstract ?? '',
        year: String(p.year ?? ''),

        // arrays
        categories,
        filetypes,
        degrees,
        supervisors,
        authors: Array.isArray(p.students)
            ? p.students.map(s => `${s.firstname ?? ''} ${s.lastname ?? ''}`.trim())
            : [],

        // singles (สำหรับ UI เดิม)
        category: categories[0] || '',
        type: filetypes[0] || '',
        degree: degrees[0] || '',
        advisor: supervisors[0] || '',

        // เก็บ path ดั้งเดิมไว้ เผื่อต้องใช้
        filePath: p.file_path || '',
        // สร้าง URL ที่ template ต้องการ โดยอิงจากนามสกุลไฟล์
        // ถ้าเป็น .pdf ให้สร้าง pdfUrl, ถ้าเป็นรูปภาพ ให้สร้าง posterUrl
        pdfUrl: (p.file_path && p.file_path.endsWith('.pdf')) ? p.file_path : null,
        posterUrl: (p.file_path && (p.file_path.endsWith('.png') || p.file_path.endsWith('.jpg') || p.file_path.endsWith('.zip') || p.file_path.endsWith('.docx'))) ? p.file_path : null,
    }
}

// -------------------- search (POST /api/projects) --------------------
export async function searchPublications(params = {}) {
    const {
        query = '',
        advisor = '',
        category = '',
        year = '',
        type = '',
        degree = ''
    } = params

    const body = {}

    if (query && query.trim()) body.query = query.trim()
    if (advisor) body.supervisors = [advisor]
    if (category) body.categories = [category]
    if (type) body.filetypes = [type]
    if (degree) body.degrees = [degree]
    if (year) {
        const y = parseInt(String(year), 10)
        if (!Number.isNaN(y)) body.year = y
    }

    try {
        const res = await fetch(`${API_BASE}/projects`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body),
        })
        if (!res.ok) throw new Error(`HTTP ${res.status}`)
        const arr = await res.json()
        const items = Array.isArray(arr) ? arr.map(normalizeItem) : []
        return { items }
    } catch (e) {
        console.error('searchPublications failed:', e)
        return { items: [] }
    }
}

// -------------------- facets store (Reactive Global Cache) --------------------
const facetsStore = reactive({
    advisors: [],
    categories: [],
    types: [],
    degrees: [],
    years: [],
    keywords: []
})

let facetsInitStarted = false

const sortAlpha = (a, b) => a.localeCompare(b)
const uniq = (arr) => Array.from(new Set(arr.filter(Boolean)))

function setFacets(data = {}) {
    const clean = (arr) => Array.isArray(arr) ? arr.filter(Boolean) : []
    facetsStore.advisors = clean(data.advisors).sort(sortAlpha)
    facetsStore.categories = clean(data.categories).sort(sortAlpha)
    facetsStore.types = clean(data.types).sort(sortAlpha)
    facetsStore.degrees = clean(data.degrees).sort(sortAlpha)
    facetsStore.years = clean(data.years).sort((a, b) => Number(b) - Number(a)) // new → old
    facetsStore.keywords = clean(data.keywords)
}

async function initFacets() {
    // 1️⃣ พยายามโหลดจาก /api/facets ก่อน
    try {
        const res = await fetch(`${API_BASE}/facets`)
        if (res.ok) {
            const data = await res.json()
            setFacets(data)
            return
        }
    } catch (e) {
        console.warn('getFacets API failed, fallback to local derive', e)
    }

    // 2️⃣ fallback: ดึงทั้งหมดจาก projects แล้ว derive facets เอง
    try {
        const { items } = await searchPublications({})
        setFacets({
            advisors: uniq(items.map(r => r.advisor)),
            categories: uniq(items.map(r => r.category)),
            types: uniq(items.map(r => r.type)),
            degrees: uniq(items.map(r => r.degree)),
            years: uniq(items.map(r => String(r.year))),
            keywords: uniq(items.map(r => r.title)).slice(0, 30),
        })
    } catch (e) {
        console.error('initFacets fallback failed:', e)
    }
}

/**
 * ใช้ใน Vue component ได้ทันที:
 * const facets = getFacets()
 * facets จะ reactive และถูกโหลดข้อมูลเบื้องหลังอัตโนมัติ
 */
export function getFacets() {
    if (!facetsInitStarted) {
        facetsInitStarted = true
        initFacets()
    }
    return facetsStore
}
