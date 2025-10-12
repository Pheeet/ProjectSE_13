// src/services/search.service.spec.js

import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { searchPublications, getFacets, normalizeItem } from './search.service.js'

// ---- Mocking global fetch ----
// เราจะจำลองการทำงานของ fetch เพื่อไม่ต้องยิง API จริง
const mockFetch = vi.fn()
vi.stubGlobal('fetch', mockFetch)

// ---- Mocking console ----
// เพื่อตรวจสอบว่ามีการ log error ออกมาหรือไม่ โดยไม่แสดงผลใน Terminal ตอนรันเทส
vi.spyOn(console, 'error').mockImplementation(() => { })
vi.spyOn(console, 'warn').mockImplementation(() => { })


describe('search.service.js', () => {

    // beforeEach จะถูกรันก่อนทุกๆ `it` block ใน describe นี้
    // เราใช้เพื่อเคลียร์ mock history เพื่อให้แต่ละเทสไม่เกี่ยวข้องกัน
    beforeEach(() => {
        mockFetch.mockClear()
        vi.clearAllMocks()
    })

    // =================================================================
    // 1. เทสฟังก์ชัน normalizeItem()
    // =================================================================
    describe('normalizeItem', () => {
        it('ควรแปลงข้อมูลจาก API ที่มีข้อมูลครบถ้วนได้ถูกต้อง', () => {
            // Arrange: เตรียมข้อมูลดิบจาก API
            const rawItem = {
                projectID: 123,
                project_name: 'Test Project',
                description: 'An abstract.',
                year: 2025,
                categories: ['AI'],
                filetypes: ['PDF'],
                degrees: ['Master'],
                supervisors: ['Dr. A'],
                students: [{ firstname: 'John', lastname: 'Doe' }]
            }

            // Act: เรียกใช้ฟังก์ชันที่ต้องการทดสอบ
            const result = normalizeItem(rawItem)

            // Assert: ตรวจสอบผลลัพธ์
            expect(result.id).toBe('123')
            expect(result.title).toBe('Test Project')
            expect(result.abstract).toBe('An abstract.')
            expect(result.year).toBe('2025')
            expect(result.authors).toEqual(['John Doe'])
            expect(result.category).toBe('AI') // ค่าเดี่ยวตัวแรก
        })

        it('ควรจัดการกับข้อมูลที่ไม่มีค่า (null/undefined) หรือเป็น Array ว่างได้', () => {
            // Arrange: ข้อมูลดิบที่บาง field ไม่มีค่า
            const rawItem = {
                id: 456,
                title: 'Empty Project',
            }

            // Act: เรียกใช้ฟังก์ชัน
            const result = normalizeItem(rawItem)

            // Assert: ตรวจสอบว่าได้ค่า default ที่ถูกต้อง (string ว่าง, array ว่าง)
            expect(result.id).toBe('456')
            expect(result.title).toBe('Empty Project')
            expect(result.abstract).toBe('')
            expect(result.year).toBe('')
            expect(result.authors).toEqual([])
            expect(result.categories).toEqual([])
        })
    })

    // =================================================================
    // 2. เทสฟังก์ชัน searchPublications()
    // =================================================================
    describe('searchPublications', () => {
        it('ควรเรียก API POST /api/projects พร้อม body ที่ถูกต้องเมื่อมีพารามิเตอร์', async () => {
            // Arrange: จำลองว่า fetch สำเร็จและคืนค่าเป็น Array ว่าง
            mockFetch.mockResolvedValue({
                ok: true,
                json: () => Promise.resolve([]),
            })

            const params = {
                query: ' machine learning ', // ทดสอบการ trim()
                year: '2024',
                advisor: 'Dr. B'
            }

            // Act: เรียกใช้ฟังก์ชัน
            await searchPublications(params)

            // Assert: ตรวจสอบว่า fetch ถูกเรียกด้วยค่าที่ถูกต้อง
            expect(mockFetch).toHaveBeenCalledWith('/api/projects', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    query: 'machine learning',
                    year: 2024,
                    supervisors: ['Dr. B'],
                }),
            })
        })

        it('ควรคืนค่า items ที่ผ่านการ normalize แล้วเมื่อ API ตอบกลับสำเร็จ', async () => {
            // Arrange: จำลองว่า API คืนข้อมูลดิบมา 1 รายการ
            const rawData = [{ projectID: 789, project_name: 'Normalized Test' }]
            mockFetch.mockResolvedValue({
                ok: true,
                json: () => Promise.resolve(rawData),
            })

            // Act: เรียกฟังก์ชัน
            const result = await searchPublications({})

            // Assert: ตรวจสอบว่าผลลัพธ์ที่ได้เป็นข้อมูลที่ผ่าน normalizeItem แล้ว
            expect(result.items.length).toBe(1)
            expect(result.items[0].id).toBe('789')
            expect(result.items[0].title).toBe('Normalized Test')
        })

        it('ควรคืนค่าเป็น { items: [] } เมื่อ API ตอบกลับมาโดยมีปัญหา (res.ok = false)', async () => {
            // Arrange: จำลองว่า API คืนค่า error
            mockFetch.mockResolvedValue({
                ok: false,
                status: 500,
            })

            // Act: เรียกฟังก์ชัน
            const result = await searchPublications({ query: 'test' })

            // Assert: ตรวจสอบว่าได้ค่า fallback และมีการ log error
            expect(result).toEqual({ items: [] })
            expect(console.error).toHaveBeenCalled()
        })

        it('ควรคืนค่าเป็น { items: [] } เมื่อ fetch เกิด network error', async () => {
            // Arrange: จำลองว่า fetch ล้มเหลว (เช่น network error)
            mockFetch.mockRejectedValue(new Error('Network Failed'))

            // Act: เรียกฟังก์ชัน
            const result = await searchPublications({ query: 'test' })

            // Assert: ตรวจสอบว่าได้ค่า fallback และมีการ log error
            expect(result).toEqual({ items: [] })
            expect(console.error).toHaveBeenCalled()
        })
    })

    // =================================================================
    // 3. เทสฟังก์ชัน getFacets()
    // =================================================================
    describe('getFacets', () => {
        it('ควรเรียก API /api/facets ก่อนเป็นอันดับแรกและเก็บข้อมูลลง store', async () => {
            // Arrange: จำลองว่า API /facets ตอบกลับสำเร็จ
            const facetsData = { degrees: ['Master', 'Bachelor'], years: ['2025', '2024'] }
            mockFetch.mockResolvedValue({
                ok: true,
                json: () => Promise.resolve(facetsData),
            })

            // Act: เรียก getFacets() (ซึ่งจะ trigger initFacets)
            const facets = getFacets()

            // Assert: ต้องรอให้ promise ใน initFacets ทำงานเสร็จ
            await vi.waitFor(() => {
                expect(facets.degrees).toEqual(['Bachelor', 'Master']) // ตรวจสอบการ sort
            })

            // ตรวจสอบว่าเรียก API ถูกต้องและไม่ได้เรียก fallback
            expect(mockFetch).toHaveBeenCalledWith('/api/facets')
            expect(mockFetch).not.toHaveBeenCalledWith('/api/projects')
        })

        it('ควรใช้ fallback โดยการเรียก /api/projects หาก /api/facets ล้มเหลว', async () => {
            // Arrange: จำลองให้ /api/facets ล้มเหลว และ /api/projects สำเร็จ
            const projectsData = [
                { projectID: 1, year: '2025', degree: 'Ph.D.' },
                { projectID: 2, year: '2025', degree: 'Master' },
            ]

            mockFetch
                .mockResolvedValueOnce({ ok: false }) // ครั้งแรกที่เรียก (facets) ให้ fail
                .mockResolvedValueOnce({ // ครั้งที่สอง (projects) ให้ success
                    ok: true,
                    json: () => Promise.resolve(projectsData)
                })

            // Act: เรียก getFacets() (ต้อง reset state ก่อน)
            const facets = getFacets()
            // Reset state for this test since it's a global singleton
            facets.degrees = []
            facets.years = []
            await initFacets() // Manually trigger for test isolation

            // Assert
            await vi.waitFor(() => {
                expect(facets.degrees).toEqual(['Master', 'Ph.D.']) // Derived and sorted
                expect(facets.years).toEqual(['2025']) // Derived and unique
            })

            expect(mockFetch).toHaveBeenCalledWith('/api/facets')
            expect(mockFetch).toHaveBeenCalledWith('/api/projects', expect.anything())
        })
    })
})