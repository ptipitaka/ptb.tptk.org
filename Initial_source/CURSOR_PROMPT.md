# Prompt สำหรับ Cursor: สร้างเว็บหนังสือ PTF บน VitePress

**คัดลอกข้อความในบล็อก "ข้อความสำหรับ Cursor" ด้านล่างไปวางใน Cursor แล้วให้ดำเนินการตามลำดับ**

---

## ข้อความสำหรับ Cursor (copy ทั้งหมดในกล่องนี้)

```
โปรเจกต์: เว็บหนังสือ "พระไตรปิฎกฉบับสำหรับประชาชน (PTF 4th Edition)" ด้วย VitePress

**ที่ตั้งโปรเจกต์:** โฟลเดอร์รากของโปรเจกต์นี้ คือ C:\Dev\ptb.tptk.org\

**แหล่งเนื้อหาเริ่มต้น (อย่าลบ):**
- C:\Dev\ptb.tptk.org\Initial_source\html5\ — มี index.html (เล่มรวม), 00.html ถึง 11.html (แยกบท), และ book.html (โครง sidebar)
- C:\Dev\ptb.tptk.org\Initial_source\ptb_fullbook.pdf — หนังสือรวมฉบับ PDF

**ความต้องการ (ให้ทำตามลำดับที่ทำได้):**

1. **สร้างโปรเจกต์ VitePress** ใน C:\Dev\ptb.tptk.org\ (หรือในโฟลเดอร์ย่อยที่เหมาะสม เช่น docs หรือ site) โดยใช้ `npx vitepress init` ตั้งชื่อ/title เป็น "พระไตรปิฎกฉบับสำหรับประชาชน" ภาษาไทย (lang: 'th').

2. **ตั้งค่า VitePress config (.vitepress/config.ts):**
   - กำหนด `base` สำหรับ GitHub Pages: ถ้า repo จะชื่อ ptb.tptk.org หรือคล้ายกัน ให้ใช้ `base: '/ptb.tptk.org/'` (หรือตามชื่อ repo จริง)
   - กำหนด `lang: 'th'`
   - กำหนด `themeConfig.outline: 'deep'` (หรือ `[2, 6]`) เพื่อแสดงสารบัญขวาจากหัวข้อหลายระดับ (h2–h6)
   - กำหนด `themeConfig.sidebar` เป็นโครงสร้างหลายชั้น (nested items สูงสุด 6 ระดับ) ตามลำดับบทในหนังสือ: ใช้ชื่อและลำดับจากโครงใน Initial_source\html5\book.html หรือจาก 00–11 (หน้าปก/ส่วนนำ, Front Matter, คำนำ, สารบัญสรุป, สารบัญละเอียด, ภาค 1–5, ดรรชนี ฯลฯ) — ถ้ายังไม่มีไฟล์ Markdown ให้สร้าง placeholder ตามโครง sidebar ก่อน

3. **เนื้อหาและโครงสร้าง:**
   - สร้างโฟลเดอร์ docs (หรือตามที่ VitePress ใช้เป็น source) สำหรับไฟล์ Markdown
   - จาก Initial_source\html5\ ให้ใช้ 00.html–11.html เป็นอ้างอิง: ให้สร้างไฟล์ .md ตัวอย่าง 1–2 หน้าพร้อมโครง frontmatter และคำอธิบาย
   - แต่ละไฟล์ .md ควรมี frontmatter ที่มี title (และ outline ถ้าต้องการจำกัดระดับ TOC ต่อหน้า)

4. **การค้นหาภาษาไทย:**
   - ติดตั้งและตั้งค่า **vitepress-plugin-pagefind** (หรือทางเลือกที่รองรับภาษาไทย) เพื่อให้ค้นหาภาษาไทยในเว็บได้
   - ใน config เปิดใช้ search ตามวิธีที่ plugin กำหนด (และตรวจว่า build มีขั้นตอนรัน pagefind ถ้าจำเป็น)

5. **ธีมและฟอนต์ไทย:**
   - ใช้ default theme ของ VitePress หรือติดตั้ง theme จาก community (เช่น Catppuccin หรือ Theme You) ตามที่ระบุใน PTF_VITEPRESS_REQUIREMENTS.md
   - ปรับให้รองรับฟอนต์ไทย (เช่น Sarabun, TH Sarabun New) ผ่าน .vitepress/theme/custom.css หรือ theme-without-fonts ตามเอกสาร VitePress

6. **Deploy บน GitHub Pages:**
   - สร้างไฟล์ workflow สำหรับ GitHub Actions (.github/workflows/deploy.yml) ที่:
     - trigger บน push (เช่น main หรือ master)
     - ติดตั้ง dependencies (npm ci หรือ pnpm)
     - รัน build (npm run docs:build หรือคำสั่งที่ใช้)
     - ถ้าใช้ Pagefind ให้รัน pagefind หลัง build ตามที่ plugin กำหนด
     - อัปโหลดผลลัพธ์จาก .vitepress/dist ไปยัง branch gh-pages (หรือตามที่ GitHub Pages ของ repo ตั้งไว้)
   - ใส่คำอธิบายสั้นใน README ว่าวิธี deploy และค่า base ที่ใช้

7. **เอกสารอ้างอิงในโปรเจกต์:**
   - คัดลอกหรืออ้างอิงไฟล์ PTF_VITEPRESS_REQUIREMENTS.md (จาก Initial_source หรือจากที่เก็บสรุปความต้องการ) ไว้ในโปรเจกต์เพื่อให้ทีมหรือ Cursor รอบถัดไปอ่านความต้องการเต็มได้

**ข้อจำกัด:** อย่าลบหรือเขียนทับโฟลเดอร์ Initial_source\ — ใช้เป็น read-only แหล่งอ้างอิงและเนื้อหาเริ่มต้นเท่านั้น
```



---

## วิธีใช้

1. เปิด Cursor แล้วเปิดโฟลเดอร์ **C:\Dev\ptb.tptk.org** เป็น workspace
2. เปิดแชทกับ Cursor (Composer หรือ Chat) แล้ววางข้อความทั้งหมดที่อยู่ในบล็อก ``` ด้านบน
3. หรือใช้คำสั่ง @ และแนบไฟล์ CURSOR_PROMPT.md พร้อมบอกว่า "ดำเนินการตาม prompt ในไฟล์นี้"

---

## ไฟล์อ้างอิงความต้องการเต็ม

- **PTF_VITEPRESS_REQUIREMENTS.md** — สรุปความต้องการและแนวทางทำต่อ (ควรมีใน Initial_source หรือคัดลอกมาไว้ใน C:\Dev\ptb.tptk.org

