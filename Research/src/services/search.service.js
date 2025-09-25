const MOCK = [{
        id: '1',
        title: 'Deep Learning for Thai NLP',
        authors: ['A. Student', 'B. Advisor'],
        abstract: 'ศึกษาวิธีการประมวลผลภาษาไทยด้วยโมเดลสมัยใหม่',
        year: '2024',
        category: 'Machine Learning',
        type: '204499',
        degree: 'Bachelor',
        advisor: 'Assistant Professor Dr. Prakarn Unachak'
    },
    {
        id: '2',
        title: 'Computer Vision in Agriculture',
        authors: ['C. Student'],
        abstract: 'ประยุกต์ใช้ CV เพื่อตรวจโรคพืชจากภาพถ่าย',
        year: '2023',
        category: 'Image Processing',
        type: 'Co-operative',
        degree: 'Bachelor',
        advisor: 'Associate Professor Dr. Ekkarat Boonchieng'
    },
    {
        id: '3',
        title: 'Anomaly Detection on Campus Network',
        authors: ['D. Student'],
        abstract: 'วิเคราะห์ทราฟฟิกเครือข่ายเพื่อหาพฤติกรรมผิดปกติ',
        year: '2025',
        category: 'Network',
        type: 'Other Type',
        degree: 'Master',
        advisor: 'Associate Professor Dr. Rattasit Sukhahuta'
    }
]

export function getFacets() {
    return {
        advisors: [
            'Assistant Professor Dr. Ratsameetip Wita',
            'Associate Professor Dr. Jakramate Bootkrajang',
            'Assistant Professor Dr. Prakarn Unachak',
            'Dr. Sutasinee Thovuttikul',
            'Dr. Thapanapong Rukkanchanunt',
            'Associate Professor Dr. Rattasit Sukhahuta',
            'Associate Professor Dr. Ekkarat Boonchieng',
            'Assistant Professor Dr. Dussadee Praserttitipong',
            'Assistant Professor Dr. Suphakit Awiphan',
            'Assistant Professor Dr. Wijak Srisujjalertwaja',
            'Dr. Worawut Srisukkham',
            'Assistant Professor Dr. Papangkorn Inkeaw',
            'Assistant Professor Dr. Kornprom Pikulkaew',
            'Associate Professor Dr. Jeerayut Chaijaruwanich',
            'Associate Professor Dr. Chumphol Bunkhumpornpat',
            'Associate Professor Dr. Varin Chouvatut',
            'Associate Professor Dr. Wattana Jindaluang',
            'Assistant Professor Dr. Samerkae Somhom',
            'Assistant Professor Dr. Areerat Trongratsameethong',
            'Assistant Professor Dr. Matinee Kiewkanya',
            'Assistant Professor Dr. Jakarin Chawachat',
            'Assistant Professor Dr. Prapaporn Techa-Angkoon',
            'Assistant Professor Wassana Naiyapo',
            'Assistant Professor Benjamas Panyangam',
            'Noparut Vanitchanant',
            'Dr. Kamonphop Srisopha',
            'Dr. Khukrit Osathanunkul',
            'Kittipitch Kuptavanich',
            'Sitthichoke Subpaiboonkit'
        ],
        categories: [
            'Web App', 'Machine Learning', 'Image Processing', 'Games', 'Data Classification',
            'Data Analysis', 'Database', 'IoT', 'Network', 'Windows App', 'Security',
            'Simulation', 'Data Warehouse', 'Virtual Reality', 'Other Categories'
        ],
        types: ['204499', 'Co-operative', 'Other Type'],
        degrees: ['Bachelor', 'Master', 'PhD'],
        years: ['2025', '2024', '2023', '2022', '2021']
    }
}

// --- Search (ยัง filter จาก MOCK) ---
export async function searchPublications(params = {}) {
    const { query = '', advisor = '', category = '', year = '', type = '', degree = '' } = params
    const q = query.trim().toLowerCase()

    const filtered = MOCK.filter((r) => {
        const okQ = !q || r.title.toLowerCase().includes(q) || (r.abstract || '').toLowerCase().includes(q)
        const okA = !advisor || r.advisor === advisor
        const okC = !category || r.category === category
        const okY = !year || r.year === String(year)
        const okT = !type || r.type === type
        const okD = !degree || r.degree === degree
        return okQ && okA && okC && okY && okT && okD
    })

    await new Promise((res) => setTimeout(res, 200))
    return { items: filtered }
}