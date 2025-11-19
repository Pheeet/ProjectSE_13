# ProjectSE_13

## Team: (ProjectSE_13)
### Project: การพัฒนาระบบสืบค้นผลงานวิจัยและผลงานนักศึกษา
**Client:** นายถนอม กองใจ

### Tech Stack:
- **Frontend:** Vue.js
- **Backend:** Flask, python
- **Database:** Postgre sql
- **DevOps:** Docker
### Members:

#### 1. ติณห์ อุปติ
- **Student ID:** 660510650  
- **GitHub ID:** [tin-auppati](https://github.com/tin-auppati)  
- **Role:** Database Engineer, Testing Manager
- **Actual Duty** Database, Testing, Backend, frontend(ระบบแนะนำงานวิจัยที่เกี่ยวข้อง)
#### 2. วุฒิภัทร ถิ่นหลวง
- **Student ID:** 660510677  
- **GitHub ID:** [pheeet](https://github.com/pheeet)  
- **Role:** Scrum Master, Requirements Manager
- **Actual Duty** Scrum Master, Requirements Manage, Full-stack

#### 3. นิติวัชร์ จริยวนิชชากร
- **Student ID:**  660510706 
- **GitHub ID:** [Mhacha174](https://github.com/Mhacha174)  
- **Role:** DevOps Manager, UI/UX Designer
- **Actual Duty** DevOps Manager, UI/UX Designer, Frontend

#### 4. พงศ์ภัศ เลาวกุล
- **Student ID:** 660510710
- **GitHub ID:** [pxsklii](https://github.com/pxsklii)  
- **Role:** UI/UX Designer (Main)
- **Actual Duty** UI/UX Designer, Frontend


#### 5. ภัทรพงศ์ ติยะธะ
- **Student ID:** 660510717
- **GitHub ID:** [Bananakluay](https://github.com/Bananakluay)
- **Role:** Tech Leader, Database Engineer
- **Actual Duty** Backend

  
---
### Screenshots
หน้า Dashboard
<img width="1507" height="717" alt="image" src="https://github.com/user-attachments/assets/613b65ca-62c4-4a5f-a099-2510bb729b94" />

หน้า Search
<img width="1528" height="752" alt="image" src="https://github.com/user-attachments/assets/e694eaef-1652-4124-8ef0-97cb1fa2c5e6" />

### Get Started
To run this project locally, you need **Docker** and **Docker Compose** installed on your machine.

#### Installation

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/Pheeet/ProjectSE_13.git](https://github.com/Pheeet/ProjectSE_13.git)
    cd ProjectSE_13
    ```

2.  **Execute permision**
    ```bash
    chmod +x ./run_docker_compoe.sh
    ```

3.  **Build and Run with Docker**
    ```bash
    ./run_docker_compose.sh
    ```

4.  **Access the Application**
    * Frontend: `http://localhost:5173`
    * Backend API: `http://localhost:56732`

### Project Structure
└── ProjectSE_13
    ├── .env.dev
    ├── .gitignore
    ├── backend
    │   ├── .coverage
    │   ├── .pytest_cache
    │   │   ├── .gitignore
    │   │   ├── CACHEDIR.TAG
    │   │   ├── README.md
    │   │   └── v
    │   │       └── cache
    │   │           ├── lastfailed
    │   │           └── nodeids
    │   ├── Dockerfile
    │   ├── Pipfile
    │   ├── Pipfile.lock
    │   ├── app
    │   │   ├── __init__.py
    │   │   ├── models
    │   │   │   └── project.py
    │   │   ├── schemas.py
    │   │   └── views.py
    │   ├── gunicorn.config.py
    │   ├── gunicorn_starter.sh
    │   ├── htmlcov
    │   │   ├── .gitignore
    │   │   ├── class_index.html
    │   │   ├── coverage_html_cb_6fb7b396.js
    │   │   ├── favicon_32_cb_58284776.png
    │   │   ├── function_index.html
    │   │   ├── index.html
    │   │   ├── keybd_closed_cb_ce680311.png
    │   │   ├── status.json
    │   │   ├── style_cb_6b508a39.css
    │   │   ├── z_5f5a17c013354698___init___py.html
    │   │   ├── z_5f5a17c013354698_schemas_py.html
    │   │   ├── z_5f5a17c013354698_views_py.html
    │   │   └── z_6c0e4b930745278b_project_py.html
    │   ├── main.py
    │   ├── manage.py
    │   ├── requirements.txt
    │   ├── tests
    │   │   ├── __init__.py
    │   │   ├── conftest.py
    │   │   ├── test_models.py
    │   │   └── test_views.py
    │   └── uploads
    │       ├── mock1.pdf
    │       ├── mock2.pdf
    │       ├── mock3.pdf
    │       ├── project1.pdf
    │       ├── project2.zip
    │       ├── project3.docx
    │       ├── project4.pdf
    │       └── project5.zip
    ├── build_docker.sh
    ├── docker-compose.yml
    ├── flask-app1_db_1.session.sql
    ├── frontend
    │   ├── .github
    │   │   └── copilot-instructions.md
    │   ├── Dockerfile
    │   ├── README.md
    │   ├── index.html
    │   ├── package-lock.json
    │   ├── package.json
    │   ├── public
    │   │   └── vite.svg
    │   ├── src
    │   │   ├── App.vue
    │   │   ├── assets
    │   │   │   └── vue.svg
    │   │   ├── features
    │   │   │   └── research
    │   │   │       ├── components
    │   │   │       │   ├── ResultCard.vue
    │   │   │       │   ├── ResultList.vue
    │   │   │       │   ├── SearchBar.vue
    │   │   │       │   ├── TopGroupsBarChart.vue
    │   │   │       │   ├── TypePieChart.vue
    │   │   │       │   └── YearTrendChart.vue
    │   │   │       └── pages
    │   │   │           ├── ReportDashboard.vue
    │   │   │           └── ReportSearch.vue
    │   │   ├── main.js
    │   │   ├── router
    │   │   │   └── index.js
    │   │   ├── services
    │   │   │   ├── search.service.js
    │   │   │   └── search.service.spec.js
    │   │   └── styles
    │   │       └── research.css
    │   └── vite.config.js
    └── run_docker_compose.sh

