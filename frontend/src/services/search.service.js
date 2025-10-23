import { reactive } from 'vue'

const API_BASE = 'http://localhost:56732/api'


async function fetchApi(url, options = {}) {
    try {
        // 2.1) ตั้งค่า Default ที่จำเป็นสำหรับทุก Request
        const defaultOptions = {
            method: options.method || 'GET',
            headers: {
                'Content-Type': 'application/json',
                ...options.headers,
            },
            // ⚠️ 2.2) สำคัญมาก: สั่งให้ส่ง Cookie (jwt_token) ไปด้วย
            credentials: 'include',
        }

        if (options.body) {
            defaultOptions.body = options.body
        }

        // 2.3) ยิง Request
        const res = await fetch(`${API_BASE}${url}`, defaultOptions)

        // ⚠️ 2.4) ดักจับ 401 (Unauthorized) ที่นี่!
        if (res.status === 401) {
            console.warn('Fetch 401: ไม่ได้ล็อกอิน หรือ Token หมดอายุ')
            const data = await res.json()

            if (data.login_url) {
                console.log('Backend สั่งให้ไปที่:', data.login_url);
                window.location.href = data.login_url
            }

            // ⚠️ "หยุด" การทำงานทั้งหมด (ห้าม Throw Error)
            // ต้องเป็นบรรทัดนี้เท่านั้น
            return new Promise(() => { }); // 👈 เช็กว่าแก้เป็นอันนี้หรือยัง
        }

        // ถ้าไม่ใช่ 401 แต่ Error อื่น
        if (!res.ok) {
            throw new Error(`HTTP ${res.status} ${res.statusText}`)
        }

        // ถ้าทุกอย่าง OK
        return res.json()

    } catch (error) {
        console.error(`fetchApi failed for: ${url}`, error)
        // ส่ง Error ต่อไปให้ฟังก์ชันที่เรียกใช้
        throw error
    }
}

// -------------------- normalize --------------------
function normalizeItem(p = {}) {
    const categories = Array.isArray(p.categories) ? p.categories : []
    const filetypes = Array.isArray(p.filetypes) ? p.filetypes : []
    const degrees = Array.isArray(p.degrees) ? p.degrees : []
    const supervisors = Array.isArray(p.supervisors) ? p.supervisors : []

    return {
        id: String(p.projectID || p.id || ''),
        title: p.project_name || p.title || '',
        abstract: p.description || p.abstract || '',
        year: Number(p.year || ''),

        // arrays
        categories,
        filetypes,
        degrees,
        supervisors,
        authors: Array.isArray(p.students) ?
            p.students.map(s => `${s.firstname ?? ''} ${s.lastname ?? ''}`.trim()) : [],

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
        yearStart = '',
        yearEnd = '',
        type = '',
        degree = ''
    } = params

    const body = {}

    if (query && query.trim()) body.query = query.trim()
    if (advisor) body.supervisors = [advisor]
    if (category) body.categories = [category]
    if (type) body.filetypes = [type]
    if (degree) body.degrees = [degree]
    const start = yearStart ? parseInt(String(yearStart), 10) : null;
    const end = yearEnd ? parseInt(String(yearEnd), 10) : null;

    if (start && end && start === end && !Number.isNaN(start)) {
        body.year = start; // ส่งเป็น year เดียว ถ้าปีเริ่มต้นและสิ้นสุดเหมือนกัน
    } else { }

    try {
        // ⚠️ ลบ fetch(...) 4 บรรทัดบนทิ้งไป
        const arr = await fetchApi('/projects', { // 👈 1. เหลือไว้แค่อันนี้
            method: 'POST',
            body: JSON.stringify(body),
        })
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
    keywords: [],
    minYear: new Date().getFullYear() - 5,
    maxYear: new Date().getFullYear()
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

    facetsStore.minYear = Number(data.minYear) || facetsStore.minYear
    facetsStore.maxYear = Number(data.maxYear) || facetsStore.maxYear
}

async function initFacets() {
    // 1️⃣ พยายามโหลดจาก /api/facets ก่อน
    try {
        const data = await fetchApi('/facets') // (GET request)
        setFacets(data)
        return
    } catch (e) {
        console.warn('getFacets API failed, fallback to local derive', e)
    }

    // 2️⃣ fallback: ดึงทั้งหมดจาก projects แล้ว derive facets เอง
    try {
        const { items } = await searchPublications({})

        // 👇 [FIX 2] เพิ่มการคำนวณ min/max ในส่วน fallback
        const allYears = uniq(items.map(r => Number(r.year))).filter(y => y > 1900) // กรองปีที่ถูกต้อง

        const minYearFallback = allYears.length
            ? Math.min(...allYears)
            : facetsStore.minYear // ใช้ default ถ้าไม่มีข้อมูล

        const maxYearFallback = allYears.length
            ? Math.max(...allYears)
            : facetsStore.maxYear // ใช้ default ถ้าไม่มีข้อมูล

        setFacets({
            advisors: uniq(items.map(r => r.advisor)),
            categories: uniq(items.map(r => r.category)),
            types: uniq(items.map(r => r.type)),
            degrees: uniq(items.map(r => r.degree)),
            years: allYears.sort((a, b) => b - a), // ใช้ปีที่คำนวณแล้ว
            keywords: uniq(items.map(r => r.title)).slice(0, 30),
            minYear: minYearFallback, // 👈 ส่ง min ที่คำนวณได้
            maxYear: maxYearFallback  // 👈 ส่ง max ที่คำนวณได้
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