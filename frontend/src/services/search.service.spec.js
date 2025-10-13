// frontend/src/services/search.service.spec.js

import { describe, it, expect } from 'vitest'
// เราจะ import ฟังก์ชัน normalizeItem มาทดสอบ
import { normalizeItem } from './search.service.js'

describe('search.service.js - normalizeItem', () => {

  it('should normalize a raw project object from API correctly', () => {
    // GIVEN: เตรียมข้อมูลดิบจำลองที่เหมือนกับได้มาจาก API
    const rawProject = {
      projectID: 99,
      project_name: 'My Test Project',
      description: 'This is a description.',
      year: 2025,
      students: [{ firstname: 'สมชาย', lastname: 'ใจดี' }],
      categories: ['Artificial Intelligence'],
      filetypes: ['Senior Project'],
      degrees: ['Bachelor'],
      supervisors: ['อ. วิชาญ'],
      file_path: '/files/test.pdf'
    };

    // WHEN: เรียกใช้ฟังก์ชันที่เราต้องการทดสอบ
    const normalized = normalizeItem(rawProject);

    // THEN: ตรวจสอบว่าผลลัพธ์ที่ได้ตรงตามที่เราคาดหวังหรือไม่
    expect(normalized.id).toBe('99');
    expect(normalized.title).toBe('My Test Project');
    expect(normalized.abstract).toBe('This is a description.');
    expect(normalized.year).toBe('2025');
    expect(normalized.authors).toEqual(['สมชาย ใจดี']);
    expect(normalized.category).toBe('Artificial Intelligence');
    expect(normalized.pdfUrl).toBe('/files/test.pdf'); // ตรวจสอบจาก Logic ที่เราเพิ่งเพิ่มเข้าไป
  });

});