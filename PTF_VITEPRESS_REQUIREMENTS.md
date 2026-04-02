# ความต้องการโปรเจกต์ VitePress — พระไตรปิฎกฉบับสำหรับประชาชน (PTF 4th Edition)

เอกสารนี้อ้างอิงความต้องการสำหรับเว็บหนังสือพระไตรปิฎกฉบับสำหรับประชาชน ด้วย VitePress

## แหล่งเนื้อหา (อย่าลบ)

- **Initial_source/html5/** — มี index.html (เล่มรวม), 00.html ถึง 11.html (แยกบท), และ book.html (โครง sidebar)
- **Initial_source/ptb_fullbook.pdf** — หนังสือรวมฉบับ PDF

## ความต้องการที่ดำเนินการแล้ว

### 1. โปรเจกต์ VitePress
- ตั้งอยู่ที่โฟลเดอร์ราก โครงสร้าง: `docs/` เป็น source ของ Markdown, `docs/.vitepress/` เป็น config และ theme
- Title: "พระไตรปิฎกฉบับสำหรับประชาชน", `lang: 'th'`

### 2. การตั้งค่า config (.vitepress/config.ts)
- **base:** `/ptb.tptk.org/` สำหรับ GitHub Pages (ปรับตามชื่อ repo จริง)
- **lang:** `'th'`
- **themeConfig.outline:** `'deep'` (หรือ `[2, 6]`) — สารบัญขวาหลายระดับ (h2–h6)
- **themeConfig.sidebar:** ลำดับอ่านหลัก — หน้าหลัก, พระคติธรรม, คำปรารภ, คำนำ, ภาพสังคายนา, แผนภูมิ, อักษรย่อ, ภาค ๑ (ไม่มีหน้า placeholder แยกตามเลข 00–11 ที่ราก `docs/`)

### 3. เนื้อหาและโครงสร้าง
- โฟลเดอร์ `docs/` สำหรับไฟล์ .md
- เนื้อหาหลักอยู่ในโฟลเดอร์ `00-speech-of-appreciation/` … `06-part-1-knowledge-of-the-tipitaka/` (จัดลำดับด้วย prefix เลข)
- แหล่ง HTML ต้นฉบับยังอยู่ที่ `Initial_source/html5/00.html` … `11.html` สำหรับอ้างอิง/แปลงต่อ

### 4. การค้นหาภาษาไทย
- **vitepress-plugin-pagefind** ติดตั้งและเปิดใช้ใน config
- ตั้ง `forceLanguage: 'th'` และข้อความ UI เป็นภาษาไทย (btnPlaceholder, placeholder, emptyText, heading)
- Pagefind รันหลัง build อัตโนมัติโดย plugin

### 5. ธีมและฟอนต์ไทย
- ใช้ default theme ของ VitePress
- ฟอนต์: Sarabun (Google Fonts), fallback TH Sarabun New ผ่าน `.vitepress/theme/custom.css`

### 6. Deploy บน GitHub Pages
- Workflow: `.github/workflows/deploy.yml`
  - Trigger: push สาขา main หรือ master
  - ขั้นตอน: checkout → setup Node → npm ci → npm run docs:build → upload artifact จาก `docs/.vitepress/dist` → deploy-pages
- ตั้งค่า repo: Settings → Pages → Source: GitHub Actions

### 7. เอกสารอ้างอิง
- ไฟล์นี้ (PTF_VITEPRESS_REQUIREMENTS.md) เก็บไว้ที่รากโปรเจกต์เพื่อให้ทีมหรือ Cursor อ่านความต้องการเต็ม

## ข้อจำกัด

**อย่าลบหรือเขียนทับโฟลเดอร์ Initial_source/** — ใช้เป็น read-only แหล่งอ้างอิงและเนื้อหาเริ่มต้นเท่านั้น
