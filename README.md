# พระไตรปิฎกฉบับสำหรับประชาชน (PTF 4th Edition) — เว็บ VitePress

เว็บหนังสือพระไตรปิฎกฉบับสำหรับประชาชน สร้างด้วย [VitePress](https://vitepress.dev/)

## โครงสร้างโปรเจกต์

- **docs/** — เนื้อหา Markdown และ config VitePress
  - **docs/.vitepress/** — config, theme, custom CSS
  - **docs/index.md** — หน้าหลัก
  - **docs/00-speech-of-appreciation/** … **docs/06-part-1-knowledge-of-the-tipitaka/** — เนื้อหาหลัก (มี `rewrites` ใน config ให้ URL เป็น `/speech-of-appreciation/` ฯลฯ)
- **Initial_source/** — แหล่งเนื้อหาเริ่มต้น (HTML, PDF) — **อย่าลบหรือเขียนทับ**
- **.github/workflows/deploy.yml** — Deploy ไป GitHub Pages

## การพัฒนาท้องถิ่น

```bash
npm install
npm run docs:dev
```

เปิด http://localhost:5173 (หรือพอร์ตที่แสดง)

## Build

```bash
npm run docs:build
```

ผลลัพธ์อยู่ที่ `docs/.vitepress/dist`. การค้นหาภาษาไทย (Pagefind) จะถูกสร้างในขั้นตอน build โดยอัตโนมัติผ่าน vitepress-plugin-pagefind

## Deploy บน GitHub Pages

1. **ตั้งค่า repo:** Settings → Pages → Build and deployment → Source: **GitHub Actions**
2. **base URL:** ในโปรเจกต์ใช้ `base: '/ptb.tptk.org/'` ใน `docs/.vitepress/config.ts`  
   - ถ้า repo ชื่อ `ptb.tptk.org` อยู่ภายใต้ organization (เช่น `tptk-org/ptb.tptk.org`) URL จะเป็น `https://tptk-org.github.io/ptb.tptk.org/`
   - ถ้าเป็น User/Organization site แยกต่างหาก ให้ปรับ `base` ใน config ให้ตรงกับ path ของ repo (เช่น `'/ptb.tptk.org/'` หรือ `'/'` ตามที่ใช้)
3. เมื่อ push ขึ้นสาขา **main** หรือ **master** workflow จะรัน: ติดตั้ง dependencies → build → อัปโหลด artifact → deploy ไป GitHub Pages

รายละเอียดความต้องการเต็มอยู่ใน **PTF_VITEPRESS_REQUIREMENTS.md**
