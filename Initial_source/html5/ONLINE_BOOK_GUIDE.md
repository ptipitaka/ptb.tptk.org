# แนวทางนำหนังสือพระไตรปิฎกฉบับสำหรับประชาชน (PTF 4th Edition) ออนไลน์

คู่มือนี้สรุปแนวทางในการเผยแผ่หนังสือเล่มนี้ในรูปแบบเว็บแบบ GitBook — สวยงาม สะดวก และรองรับการค้นหา (รวมถึง AI search)

---

## ภาพรวมตัวเลือก

| วิธี | ความยาก | ความสวย/ฟีเจอร์ | Search | AI Search | โฮสต์ |
|------|---------|------------------|--------|-----------|--------|
| **1. ใช้โครงเว็บหนังสือ + Pagefind** (แนะนำสำหรับตอนนี้) | ง่าย | ดี | ✅ Full-text | ใช้ DocSearch ภายหลัง | GitHub Pages, Netlify, Vercel |
| **2. GitBook (gitbook.com)** | ปานกลาง | สวย ครบ | มีในตัว | มี (แผนเสียเงิน) | GitBook |
| **3. Docusaurus / VuePress** | ต้องแปลงเป็น MD | สวย ครบ | DocSearch ได้ | Algolia Ask ได้ | GitHub Pages ฯลฯ |
| **4. DocSearch (Algolia)** เพิ่มบนเว็บเดิม | หลังขึ้นเว็บแล้ว | ตามเว็บ | ✅ ฟรีสำหรับ docs | ✅ Algolia Ask AI | ใช้กับเว็บใดก็ได้ |

---

## ตัวเลือกแนว Docusaurus / VuePress — มีอะไรทันสมัยกว่า/ง่ายกว่าบ้าง?

ถ้าสนใจทำเว็บหนังสือด้วย **static site generator แบบ documentation** (เนื้อหาเป็น Markdown/MDX) มีตัวที่ **ทันสมัยกว่า เร็วกว่า หรือตั้งค่าง่ายกว่า** Docusaurus และ VuePress ดังนี้

### สรุปสั้น ๆ

| เครื่องมือ | เทียบกับ Docusaurus/VuePress | เหมาะกับ |
|------------|-----------------------------|----------|
| **VitePress** | ทันสมัยกว่า VuePress (ทีม Vue ทำต่อ), ใช้ Vite เร็วมาก, ตั้งค่าน้อย | หนังสือ/เอกสารหนึ่งชุด, ไม่ต้องมีหลายเวอร์ชัน |
| **Starlight (Astro)** | ใหม่กว่า, โฟกัส performance + accessibility, สวย out of the box, มี local search ในตัว | ต้องการความเร็วและความสวยโดยไม่ยุ่ง config มาก |
| **Nextra** | อยู่ ecosystem Next.js, MDX ครบ | โปรเจกต์ที่ใช้ Next.js อยู่แล้ว |
| **Fumadocs** | ใหม่, React + MDX, ยืดหยุ่น | ชอบ React และ MDX |
| **Mintlify** | เป็น SaaS (ไม่ใช่เปิด source แบบ self-host ฟรีเต็มที่), มี AI ในตัว | ต้องการแพลตฟอร์มจัดการ docs + AI แบบจ่ายเงิน |

---

### 1. VitePress (แนะนำถ้าชอบแนว VuePress แต่ต้องการของใหม่กว่า)

- **ทำโดย**: ทีม Vue.js (ถือเป็นตัวต่อของ VuePress)
- **เทคโนโลยี**: Vue 3 + Vite
- **ความง่าย**: ตั้งค่าน้อย (zero-config พื้นฐาน), เร็วมาก
- **จุดเด่น**: ค้นหาได้ทั้ง local และ Algolia, รองรับ i18n (รวมภาษาไทย), ใช้กับ Vue/Vite ecosystem
- **ข้อจำกัด**: ไม่มี versioned docs แบบ Docusaurus (หลายเวอร์ชันของเอกสาร)
- **เหมาะกับหนังสือเล่มนี้**: เนื้อหาเป็น Markdown แยกบท, ต้องการ sidebar + search, โฮสต์ GitHub Pages / Netlify ได้
- **ลิงก์**: [vitepress.dev](https://vitepress.dev/)

---

### 2. Starlight (Astro) — สวย เร็ว ง่าย

- **ทำโดย**: ทีม Astro
- **เทคโนโลยี**: Astro (สร้าง HTML static ได้มาก, JavaScript น้อย)
- **ความง่าย**: สร้างโปรเจกต์ด้วย template ได้ทันที (`npm create astro@latest -- --template starlight`)
- **จุดเด่น**: คะแนน Lighthouse สูง, accessibility ดี, มี **local search (Pagefind)** ในตัว, รองรับหลายภาษา (i18n), โครงสร้างโฟลเดอร์ชัด
- **ข้อจำกัด**: ไม่มี versioned docs / blog แบบ Docusaurus
- **เหมาะกับหนังสือเล่มนี้**: ต้องการเว็บหนังสือสวย เร็ว อ่านสบาย โดยไม่ต้องผูกกับ React/Vue
- **ลิงก์**: [starlight.astro.build](https://starlight.astro.build/)

---

### 3. Docusaurus (ตัวเดิม — ครบที่สุด)

- **จุดเด่น**: versioned docs, i18n หลายภาษา, blog, หลายชุด docs ใน site เดียว, plugin เยอะ
- **ข้อเสีย**: ใช้ Webpack, ตั้งค่าหนักกว่า VitePress/Starlight
- **เหมาะกับ**: โปรเจกต์ใหญ่ มีหลายเวอร์ชัน/หลายภาษาชัดเจน

---

### 4. VuePress (ตัวเดิม)

- **สถานะ**: ยังใช้ได้ แต่ทีม Vue เลื่อนไปพัฒนา **VitePress** เป็นหลัก
- **แนะนำ**: ถ้าจะเริ่มใหม่ ใช้ **VitePress** แทนจะได้ของใหม่กว่า เร็วกว่า

---

### 5. ตัวอื่น ๆ สั้น ๆ

- **Nextra**: ใช้กับ Next.js, MDX — เหมาะถ้าโปรเจกต์เป็น Next.js อยู่แล้ว
- **Fumadocs**: React + MDX + Vite — เหมาะถ้าชอบ React และต้องการความยืดหยุ่น
- **Mintlify**: แพลตฟอร์ม docs แบบ SaaS มี AI — ใช้เมื่อต้องการบริการจัดการ docs แบบจ่ายเงิน

---

### สรุปสำหรับหนังสือ PTF 4th Edition

- **อยากได้ทันสมัย + ง่าย**: เลือก **VitePress** หรือ **Starlight**
- **อยากได้สวย เร็ว โดยไม่ยุ่งกับ React/Vue มาก**: **Starlight** เหมาะมาก (มี local search ในตัว)
- **อยากได้ครบ versioned docs / blog / i18n แบบหนัก ๆ**: ยังใช้ **Docusaurus** ได้

ทั้ง VitePress และ Starlight รองรับการโฮสต์แบบ static (GitHub Pages, Netlify, Vercel) และต่อยอดใส่ **DocSearch (Algolia)** สำหรับ full-text + AI search ได้เหมือนกัน

---

## VitePress vs Docusaurus vs Starlight — อันไหน implement ง่ายที่สุด + ต่อยอด “แชทกับ AI” ได้?

### ความง่ายในการ implement (เรียงจากง่ายไปยาก)

| ลำดับ | เครื่องมือ | ความง่าย | หมายเหตุ |
|-------|------------|----------|----------|
| **1** | **VitePress** | ง่ายที่สุด | `npx vitepress init` แล้วตอบคำถามไม่กี่ข้อ ได้โครงโปรเจกต์ + config เดียว (`config.ts`), มี local search เปิดใช้หนึ่งบรรทัด |
| **2** | **Starlight** | ง่าย | `npm create astro@latest -- --template starlight` ได้เลย, มี **Pagefind (ค้นหาในตัว)** ไม่ต้องตั้งค่า, โครงโฟลเดอร์ชัด |
| **3** | **Docusaurus** | ปานกลาง | ต้องตั้งค่า config หลายจุด, มี preset, plugin เยอะ — เหมาะเมื่อต้องการ versioning / blog / i18n แบบเต็ม |

สรุป: **implement ง่ายที่สุด = VitePress** ตามด้วย Starlight แล้วค่อย Docusaurus

---

### ต่อยอด “แชทกับ AI” (ค้นหาจากเนื้อหาในเว็บ)

ทั้งสามตัว **ต่อยอดให้มี AI chat ที่ตอบจากเนื้อหาใน docs ได้** โดยใช้บริการหรือ plugin ด้านล่าง (ส่วนใหญ่ใช้ RAG/embedding + LLM)

| เครื่องมือ | ทางเลือกสำหรับ AI Chat / ค้นหาด้วย AI |
|------------|----------------------------------------|
| **VitePress** | **Biel.ai** (widget ใน navbar), **VectraDocs** (plugin open source + backend), **Documate** (open source + AirCode + OpenAI), **Inkeep** (chat button) |
| **Starlight** | **Biel.ai** (มี integration สำหรับ Starlight โดยตรง — ใส่ component ใน footer + script ใน config), **Algolia DocSearch** (ค้นหา + Algolia Ask AI ถ้าสมัคร) |
| **Docusaurus** | **docusaurus-plugin-chat-page** (open source, ใช้ embedding + streaming), **@upstash/docusaurus-theme-ai-search**, **Inkeep**, **DocuScout** (Metered) |

- **Biel.ai**: ใช้ได้ทั้ง VitePress และ Starlight, เป็น SaaS (สมัครแล้วใส่ script/component), AI ตอบจากเนื้อหาใน docs
- **VectraDocs / Documate (VitePress)**: แนว open source แต่ต้องมี backend (หรือ AirCode) และ API key (เช่น OpenAI)
- **Docusaurus**: มี plugin chat แบบ open source (เช่น chat-page) ที่สร้าง embedding จากเนื้อหาแล้วให้ผู้ใช้แชทกับ AI ได้

---

### สรุปตอบคำถาม

- **Implement ง่ายที่สุด**: **VitePress** (จากนั้นคือ Starlight แล้วค่อย Docusaurus)
- **ต่อยอดแชทกับ AI ได้ทั้งสามตัว** — เลือกได้ตามสไตล์:
  - **VitePress**: ง่ายสุด + ตัวเลือก AI หลายแบบ (Biel.ai, VectraDocs, Documate, Inkeep)
  - **Starlight**: ง่าย มี search ในตัว + ใส่ Biel.ai หรือ DocSearch (Algolia Ask) ได้ตรง
  - **Docusaurus**: หนักกว่าแต่มี plugin chat แบบ open source (embedding + streaming) และ ecosystem ใหญ่

ถ้าต้องการ **ง่ายและต่อยอดแชทกับ AI ได้เร็ว**: แนะนำ **VitePress** หรือ **Starlight** แล้วเพิ่ม **Biel.ai** หรือ (ถ้าไม่ต้องการบริการจ่าย) ใช้ **VectraDocs/Documate** บน VitePress หรือ **docusaurus-plugin-chat-page** บน Docusaurus

---

## VitePress vs Starlight — ความเร็ว (เร็วกว่ากันอย่างไร)

ความเร็วแบ่งได้สองมุม: **ความเร็วตอนผู้ใช้เปิดเว็บ (runtime)** กับ **ความเร็วตอนพัฒนา/build**

### 1. ความเร็วที่ผู้ใช้รู้สึก (Runtime — เปิดเว็บแล้วโหลด/เลื่อนหน้า)

| ด้าน | VitePress | Starlight |
|------|-----------|-----------|
| **JavaScript ที่ส่งไปเบราว์เซอร์** | ส่ง Vue runtime + chunk ของหน้า (ประมาณหลักหมื่น bytes ถึง ~21kB gzipped ในหลายเคส) | **Astro ส่งน้อยมาก (zero/ship less JS)** — หน้าเป็น HTML เป็นหลัก, มี JS เฉพาะส่วนที่ต้อง interactive (เช่น search, theme) |
| **ผลต่อความเร็ว** | เร็วมาก โหลดเร็ว | **มักเบากว่า** — โหลดเร็วและมักได้ Lighthouse/PageSpeed ดี เพราะส่ง JS น้อยกว่า |
| **การเลื่อนหน้า (navigation)** | ใช้ Vue เป็น SPA-like เลื่อนหน้าเร็ว | ใช้ HTML + เล็กน้อย JS, มีการ optimize ให้ defer JS ที่ไม่จำเป็น (เช่น TOC, code block) ออกไปรันตอน main thread ว่าง |

**สรุป runtime:** **Starlight มักจะ “เร็ว” กว่าในสายตาผู้ใช้** เพราะส่ง JavaScript น้อยกว่า (Astro zero-JS by default) ทำให้หน้าโหลดและทำงานบนมือถือ/อุปกรณ์ช้าได้ดีกว่า

---

### 2. ความเร็วตอนพัฒนาและ build

| ด้าน | VitePress | Starlight |
|------|-----------|-----------|
| **Dev server / HMR** | ใช้ Vite — เปิด server เร็ว, แก้ไฟล์แล้วอัปเดต &lt;100ms | ใช้ Vite เช่นกัน — เร็วระดับเดียวกัน |
| **Build time (โปรเจกต์เล็ก–กลาง)** | โครงสร้างเรียบง่าย → build มักเร็ว | มี layer ของ Astro + Starlight → อาจใช้เวลามากกว่าเล็กน้อย |
| **Build time (โปรเจกต์ใหญ่)** | ยังเร็ว | **ถูก optimize ชัด** — มีการ cache sidebar และลดงานซ้ำ (เช่น โปรเจกต์ขนาดระดับ Cloudflare Docs build เร็วขึ้นราว 36%) |

**สรุป build:** **VitePress มัก build เร็วกว่าเล็กน้อยในโปรเจกต์ขนาดเล็ก–กลาง** เพราะโครงสร้างเบา; **Starlight โดดเด่นในโปรเจกต์ใหญ่** หลังมีการ optimize build แล้ว

---

### สรุปเปรียบเทียบความเร็ว

| ประเภทความเร็ว | ใครมักจะเร็วกว่า | หมายเหตุ |
|----------------|-------------------|----------|
| **ผู้ใช้เปิดเว็บ (โหลดหน้า, ใช้งาน)** | **Starlight** | ส่ง JS น้อยกว่า (Astro), หน้าเป็น HTML หลัก → มักได้คะแนน Lighthouse/ประสบการณ์ใช้งานที่ดีกว่า |
| **ตอนพัฒนา (dev server, HMR)** | **ใกล้เคียงกัน** | ทั้งคู่ใช้ Vite |
| **Build (โปรเจกต์เล็ก–กลาง)** | **VitePress** | โครงสร้างเบากว่า → build มักเร็วกว่าเล็กน้อย |
| **Build (โปรเจกต์ใหญ่มาก)** | **Starlight** | มีการ optimize build และ cache สำหรับ docs ขนาดใหญ่ |

ถ้าพิจารณาเฉพาะ **“ความเร็วในการใช้งาน” แบบที่ผู้ใช้สัมผัสได้ (เปิดเว็บ อ่าน เลื่อนหน้า)** → **Starlight มักจะเร็วกว่า** เพราะส่ง JavaScript น้อยกว่าและเน้น HTML เป็นหลัก

---

## VitePress — มี Template / Theme ที่สวยไหม?

มีครับ VitePress มีทั้ง **default theme ที่ปรับแต่งได้** และ **theme / template จาก community** หลายแบบ สรุปดังนี้

### 1. Default theme + ปรับแต่งเอง

- **Theme มาตรฐาน** ของ VitePress สะอาด อ่านง่าย
- ปรับสี/ฟอนต์ได้ผ่าน **CSS variables** ใน `.vitepress/theme/custom.css`
- ใช้ **theme-without-fonts** ได้ถ้าต้องการใส่ฟอนต์เอง (เช่น ฟอนต์ไทย)
- ดูวิธีขยาย/ปรับ: [Extending the Default Theme](https://vitepress.dev/guide/extending-default-theme)

### 2. Theme จาก community (สวย / พร้อมใช้)

| Theme | ลักษณะ | Demo / Repo |
|-------|--------|-------------|
| **Catppuccin** | โทน pastel, 4 variants (Latte, Frappé, Macchiato, Mocha), light/dark, สี accent ปรับได้ | [vitepress.catppuccin.com](https://vitepress.catppuccin.com/) · [github.com/catppuccin/vitepress](https://github.com/catppuccin/vitepress) |
| **Trito** | ปรับปรุง default theme ให้ดูดีขึ้น, drop-in replacement | [github.com/hesprs/vitepress-theme-trito](https://github.com/hesprs/vitepress-theme-trito) |
| **Theme + (Default Plus)** | default theme + ฟีเจอร์เพิ่ม (multi-column nav, tabs, cards) | [vitepress-theme-default-plus.lando.dev](https://vitepress-theme-default-plus.lando.dev/) · [github.com/lando/vitepress-theme-default-plus](https://github.com/lando/vitepress-theme-default-plus) |
| **VitePress Theme You** | มินิมอล สะอาด เหมาะ docs, มี cover page | [you.yunyoujun.cn](https://you.yunyoujun.cn/) · [github.com/YunYouJun/vitepress-theme-you](https://github.com/YunYouJun/vitepress-theme-you) |
| **VitePress Blog Pure** | บล็อก มินิมอล ตัวอักษรสวย | [ti.bi](https://ti.bi/) · [github.com/airene/vitepress-blog-pure](https://github.com/airene/vitepress-blog-pure) |
| **VitePress Blog Starter** | บล็อก มี categories, reading time, author, local search, dark mode | [sfxcode.github.io/vitepress-blog-starter](https://sfxcode.github.io/vitepress-blog-starter/) · [github.com/sfxcode/vitepress-blog-starter](https://github.com/sfxcode/vitepress-blog-starter) |
| **Aplós** | หลาย layout (blog, features), components เยอะ, ดูสวย น้ำหนักเบา | [aplos.gxbs.dev](https://aplos.gxbs.dev/) · [github.com/aplosdev/aplos](https://github.com/aplosdev/aplos) |
| **Theme Curve** | บล็อก/docs มี TOC แบบ animate, tags, comments | [blog.imsyy.top](https://blog.imsyy.top/) · [github.com/imsyy/vitepress-theme-curve](https://github.com/imsyy/vitepress-theme-curve) |
| **Lumen** | มีสถิติ site, announcements, link cards, social share, comments (Twikoo) | [lumen.theojs.cn](https://lumen.theojs.cn/) · [github.com/Theo-Messi/lumen](https://github.com/Theo-Messi/lumen) |
| **VitePress OpenAPI** | สำหรับ API docs มี code snippet + live demo ต่อ endpoint | [vitepress-openapi.vercel.app](https://vitepress-openapi.vercel.app/) · [github.com/enzonotario/vitepress-openapi](https://github.com/enzonotario/vitepress-openapi) |

### 3. สำหรับหนังสือ / documentation แบบ PTF

- **ใช้เป็น docs ธรรมดา**: **Catppuccin** หรือ **Theme You** หรือ **Trito** — ดูสวย อ่านสบาย
- **อยากได้โทน pastel / สลับ light–dark**: **Catppuccin** (ติดตั้ง `@catppuccin/vitepress` แล้วเลือก flavor)
- **อยากได้แบบ default แต่สวยขึ้น**: **Trito** หรือ **Default Plus**
- **ต้องการฟอนต์ไทย**: ใช้ default theme แล้วใส่ `theme-without-fonts` + กำหนดฟอนต์ไทยใน CSS

สรุป: **มี template/theme สวยหลายตัว** — ถ้าต้องการ "สวยพร้อมใช้" แนะนำลอง **Catppuccin** หรือ **Theme You** ก่อน

---

## VitePress vs Starlight — การค้นหา (Pagefind ในตัวไหม, ภาษาไทยดีกว่ากัน)

### มี Pagefind ในตัวไหม?

| เครื่องมือ | Search ในตัว | ใช้ Pagefind หรือไม่ |
|------------|--------------|----------------------|
| **Starlight** | **มีในตัว** | **ใช่ — ใช้ Pagefind เป็น default** ไม่ต้องตั้งค่า build แล้วมี search bar ใน header เลย |
| **VitePress** | **มีในตัว** | **ไม่ — ใช้ MiniSearch** (local, fuzzy search ในเบราว์เซอร์) ไม่ได้ใช้ Pagefind โดยตรง ถ้าอยากได้ Pagefind ต้องติดตั้ง plugin **vitepress-plugin-pagefind** เอง |

### ประสิทธิภาพการค้นหาในตัว (โดยไม่ติดตั้งอะไรเพิ่ม)

| ด้าน | VitePress (MiniSearch) | Starlight (Pagefind) |
|------|------------------------|----------------------|
| **เปิดใช้** | ตั้ง `search.provider: 'local'` ใน config | ไม่ต้องทำอะไร — ใช้ได้เลยหลัง build |
| **การ index** | สร้าง index ตอน build, โหลดในเบราว์เซอร์ | Pagefind สร้าง index แยก (รันหลัง build), โหลดตาม language |
| **ขนาด/แบนด์วิธ** | Index อยู่ใน bundle ของไซต์ | Pagefind แยก chunk ตามภาษา, มักใช้แบนด์วิธน้อยในไซต์ใหญ่ |
| **ภาษาไทย** | **ใช้ได้** — ถ้าติดตั้ง **vitepress-plugin-pagefind** จะได้พฤติกรรมใกล้ Starlight; หรือใช้ MiniSearch ในตัว + **custom tokenizer สำหรับไทย** (เช่น thai-tokenizer) | **ใช้ได้** — Pagefind ในตัว: UI แปลไทย, index ตาม `lang="th"` ค้นคำไทยได้ (ไม่มี Word Stemming สำหรับไทย) |

### ภาษาไทย: ดีกว่ากันอย่างไร

- **Starlight (Pagefind ในตัว)**  
  - ภาษาไทย **ใช้ได้ดีกว่าโดยไม่ต้อง config เพิ่ม**: ตั้ง `lang="th"` ในหน้า/ไซต์ แล้ว UI เป็นไทย และค้นคำไทยได้  
  - ข้อจำกัด: ไทยไม่มี stemming จึงต้องตรงคำ (หรือส่วนของคำ) ที่อยู่ในเนื้อหา  

- **VitePress (MiniSearch ในตัว)**  
  - ภาษาไทย **โดยค่าเริ่มต้นไม่เหมาะ**: tokenizer มาตรฐานไม่เข้าใจการตัดคำไทย  
  - ถ้าต้องการให้ดี: ต้องเพิ่ม **custom tokenizer สำหรับไทย** (เช่น ผูกกับ thai-tokenizer) ใน `search.options.miniSearch.options.tokenize`  

**สรุปสำหรับภาษาไทย:**  
- **คำนึงถึงการค้นหาภาษาไทย ทั้งสองอย่างนี้ใช้ได้ทั้งคู่**  
  - **Starlight:** ใช้ได้เลยโดยไม่ต้อง config เพิ่ม (Pagefind ในตัว, UI ไทย, index ตาม `lang="th"`)  
  - **VitePress:** ใช้ได้เช่นกัน — ถ้าใช้ **vitepress-plugin-pagefind** จะได้ engine แบบ Pagefind (รองรับไทยเหมือน Starlight) หรือถ้าใช้ search ในตัว (MiniSearch) ก็ปรับ **custom tokenizer สำหรับไทย** (เช่น thai-tokenizer) ได้  
- ข้อจำกัดร่วม: ภาษาไทยไม่มี word stemming ใน Pagefind/MiniSearch จึงค้นด้วยคำที่ตรงหรือส่วนของคำ ไม่มีการลดรูปคำอัตโนมัติ

### อ้างอิง

- Starlight search: [starlight.astro.build/guides/site-search](https://starlight.astro.build/guides/site-search)  
- VitePress search: [vitepress.dev/reference/default-theme-search](https://vitepress.dev/reference/default-theme-search)  
- Pagefind ภาษาไทย: [pagefind.app/docs/multilingual](https://pagefind.app/docs/multilingual/) (Thai: UI ✅, Stemming ❌)

---

## Docusaurus — Plugin ที่น่าสนใจ

ถ้าเลือกใช้ Docusaurus มี plugin ทั้งแบบ **official** (จากทีม Docusaurus) และ **community** (จาก docusaurus.community/plugindirectory) ที่น่าสนใจสำหรับเว็บหนังสือ/เอกสาร ดังนี้

### ค้นหา (Search)

| Plugin | ประเภท | คำอธิบาย |
|--------|--------|----------|
| **Theme Search Algolia** | Official | ค้นหาด้วย Algolia — ใช้กับ DocSearch ได้, รองรับ AI (Algolia Ask) |
| **Search Local** (หลายตัว) | Community | ค้นหาแบบ offline/local ไม่ต้องมี API — เช่น `docusaurus-plugin-search-local` รองรับหลายภาษา (รวมไทยผ่าน lunr-languages) |
| **Lunr / Lunr Search** | Community | สร้างดัชนี Lunr.js สำหรับค้นหาในไซต์ |
| **Search Typesense** | Community | ค้นหาด้วย Typesense (self-host หรือ cloud) |

### เนื้อหา & Markdown

| Plugin | คำอธิบาย |
|--------|----------|
| **Backlinks** | แสดง backlinks ระหว่างหน้า — เหมาะกับหนังสือที่อ้างอิงข้ามบท |
| **Draw.io** | แทรกไดอะแกรม draw.io ใน Markdown |
| **Mindmap** | แทรก mind map ในเอกสาร |
| **Includes** | include เนื้อหาจากไฟล์ Markdown อื่น (ลดการซ้ำ) |
| **Image Zoom** | ซูมรูปเมื่อคลิก (medium-zoom) |
| **Content Gists** | แทรก GitHub Gists |
| **Code Preview** | ตัวอย่างโค้ดแบบ live ในหน้า |
| **Tab Blocks** | แปลง code block เป็นแท็บ (เช่น npm / yarn / pnpm) |

### PDF / Export

| Plugin | คำอธิบาย |
|--------|----------|
| **Mr PDF** | ปุ่ม export หน้า/ทั้งเล่มเป็น PDF จาก Docusaurus |
| **docusaurus-plugin-papersaurus** | สร้าง PDF อัตโนมัติจาก sidebar (ใช้ Puppeteer), มี TOC และหน้าปก |
| **WKHTMLToPDF** | สร้าง PDF ด้วย wkhtmltopdf |
| **playwright-docusaurus-pdf** | สร้าง PDF ด้วย Playwright (crawl ตาม URL) |

### วิเคราะห์ & SEO

| Plugin | คำอธิบาย |
|--------|----------|
| **Google Analytics / Gtag / Tag Manager** | Official — วิเคราะห์การเข้าชม |
| **Plausible, Umami, GoatCounter, Simple Analytics** | Community — analytics แบบเน้นความเป็นส่วนตัว |
| **Sitemap** | Official — สร้าง sitemap สำหรับ SEO |
| **Structured Data** | เพิ่ม JSON-LD สำหรับ SEO (แบบ Yoast) |
| **PWA** | Official — ทำให้ไซต์ใช้แบบ PWA (ติดตั้งบนมือถือ/เดสก์ท็อปได้) |

### อื่น ๆ ที่น่าสนใจ

| Plugin | คำอธิบาย |
|--------|----------|
| **Docs Editor** | ให้ผู้ใช้เสนอแก้ไข Markdown ผ่านตัวแก้ข้อความในเบราว์เซอร์ (ไม่ต้องรู้ Git) |
| **Ideal Image** | Official — ปรับขนาดและ lazy load รูปอัตโนมัติ |
| **Remote Content** | ดึงเนื้อหาจาก URL ภายนอกมาเป็นหน้าใน Docusaurus |
| **RSS Feeds** | แสดง RSS feed ในไซต์ |
| **Chatwoot / Papercups** | แชทสนับสนุนผู้ใช้ในไซต์ |
| **Tailwind CSS / SASS / Less** | ใช้ Tailwind หรือ SASS/Less ในการออกแบบ theme |

### สำหรับหนังสือ PTF (พระไตรปิฎกฉบับสำหรับประชาชน)

- **Search**: ใช้ **Search Local** (รองรับหลายภาษา) หรือ **Algolia** ถ้าต้องการ AI search
- **PDF**: ใช้ **Mr PDF** หรือ **papersaurus** ถ้าต้องการให้ผู้อ่านดาวน์โหลดเป็น PDF
- **Backlinks**: มีประโยชน์ถ้ามีการอ้างอิงข้ามบท (เช่น “ดูเพิ่มที่…”)
- **Image Zoom**: ถ้ามีภาพประกอบในเล่ม
- **PWA**: ให้ผู้อ่าน “ติดตั้ง” หนังสือบนมือถือ/แท็บเล็ตเพื่ออ่านแบบ offline ได้

รายการ plugin เต็ม: [docusaurus.community/plugindirectory](https://docusaurus.community/plugindirectory/)

---

## ฐานข้อมูลเนื้อหา: แสดงบนเว็บ + นำไปทำหนังสือได้

ถ้าต้องการให้ **เนื้อหาเป็นแหล่งเดียว** (single source) ใช้ทั้ง **แสดงบนเว็บ** และ **ผลิตเป็นหนังสือ/PDF สำหรับพิมพ์** แนะนำให้เก็บเนื้อหาในรูปแบบข้อความที่มีโครงสร้างชัด แล้วค่อยแปลงออกเป็นหลายรูปแบบ

### แนวทางหลัก: เนื้อหาแหล่งเดียว (Single-Source)

| รูปแบบต้นทาง | ใช้ทำเว็บ | ใช้ทำหนังสือ/พิมพ์ |
|--------------|-----------|---------------------|
| **Markdown (.md)** | Docusaurus, VitePress, Starlight อ่านโฟลเดอร์ docs แล้ว build เป็น HTML | Pandoc แปลงเป็น PDF, EPUB, DOCX หรือใช้ plugin export PDF จากไซต์ที่ build แล้ว |
| **AsciiDoc (.adoc)** | Asciidoctor → HTML แล้วใช้กับ static host หรือ Antora (docs site) | Asciidoctor PDF หรือ AsciiDoc → DocBook → PDF |

สำหรับโปรเจกต์นี้ **Markdown** เหมาะที่สุด เพราะ Docusaurus/VitePress/Starlight ใช้ MD อยู่แล้ว และมีเครื่องมือแปลงไปพิมพ์ได้มาก

---

### โครงสร้างที่แนะนำ

```
ptf-4th/
├── content/                 # ฐานข้อมูลเนื้อหา (แหล่งเดียว)
│   ├── 00-คำปรารภ.md
│   ├── 01-front-matter.md
│   ├── 02-คำนำ.md
│   ├── ...
│   └── 12-ดรรชนี.md
├── docs/                    # ถ้าใช้ Docusaurus/VitePress: ลิงก์หรือ copy มาจาก content/
│   └── (หรือชี้ path ไปที่ content/)
├── docusaurus.config.js     # หรือ vitepress config
└── scripts/
    └── build-pdf.sh         # สคริปต์รัน Pandoc ฯลฯ
```

- **เว็บ**: ตั้งค่า Docusaurus/VitePress/Starlight ให้อ่านจาก `content/` (หรือ `docs/` ที่ชี้ไปที่เนื้อหาเดียวกัน) → build เป็น static site
- **หนังสือ**: จากโฟลเดอร์ `content/` เดียวกัน ใช้ Pandoc (หรือ plugin) สร้าง PDF/EPUB/DOCX

---

### จากเนื้อหาแหล่งเดียว → ทำหนังสือ/พิมพ์

#### วิธีที่ 1: Pandoc (Markdown → PDF / EPUB / DOCX)

- **PDF (สำหรับพิมพ์หรือแจก)**  
  - ใช้ engine เช่น XeLaTeX เพื่อรองรับฟอนต์ไทย:  
    `pandoc content/*.md -o book.pdf --pdf-engine=xelatex -V mainfont="TH Sarabun New"`  
  - กำหนดหน้าปก สารบัญ ขนาดหน้ากระดาษ ผ่าน template LaTeX หรือตัวแปร
- **EPUB**  
  - สำหรับ ebook:  
    `pandoc content/*.md -o book.epub`
- **DOCX**  
  - ส่งต่อให้ InDesign หรือ Word เพื่อจัดหน้าการพิมพ์:  
    `pandoc content/*.md -o book.docx`

ข้อดี: เนื้อหาอยู่ใน `.md` แก้ที่เดียว ได้ทั้งเว็บและหนังสือ

#### วิธีที่ 2: Export PDF จากเว็บที่ build แล้ว

- **Docusaurus**: ใช้ plugin เช่น **papersaurus** หรือ **Mr PDF** ให้ build ไซต์จาก Markdown ก่อน แล้วค่อย export หน้าที่ต้องการเป็น PDF (หรือทั้งเล่ม)
- **VitePress**: ใช้ **vitepress-export-pdf** (Puppeteer) export หน้าที่ build แล้วเป็น PDF

ข้อดี: หน้าที่ได้ตรงกับที่แสดงบนเว็บ (รวม style, สารบัญที่สร้างจาก sidebar)  
ข้อควรระวัง: ต้องดูแล print CSS (หน้าขึ้นใหม่, หัวกระดาษ-ท้ายกระดาษ) ถ้าต้องการคุณภาพระดับพิมพ์

#### วิธีที่ 3: AsciiDoc เป็นแหล่งเดียว

- เก็บต้นฉบับเป็น **.adoc**
- **เว็บ**: Asciidoctor → HTML แล้ว deploy; หรือใช้ **Antora** ถ้าต้องการโครงแบบ documentation site
- **หนังสือ**: **Asciidoctor PDF** หรือ AsciiDoc → DocBook → PDF ผ่าน DocBook toolchain

เหมาะถ้าต้องการฟีเจอร์ระดับหนังสือ (footnote, cross-reference ซับซ้อน) ในตัวรูปแบบ AsciiDoc

---

### สรุปสำหรับ PTF 4th Edition

1. **เก็บเนื้อหาเป็น Markdown** ในโฟลเดอร์เดียว (เช่น `content/` หรือ `docs/`)
2. **เว็บ**: ใช้ Docusaurus / VitePress / Starlight อ่านจากโฟลเดอร์นั้น → build เป็นเว็บหนังสือ
3. **หนังสือ/พิมพ์**:  
   - **ทางรวด**: Pandoc จาก `content/*.md` → `book.pdf` (XeLaTeX + ฟอนต์ไทย) หรือ `book.docx` เพื่อส่งต่อ InDesign  
   - **ทางเลือก**: build เว็บแล้วใช้ plugin (papersaurus, vitepress-export-pdf) export เป็น PDF

ผลลัพธ์: **ฐานข้อมูลเนื้อหา** อยู่ที่ไฟล์ Markdown ชุดหนึ่ง แก้ที่เดียว แล้วได้ทั้ง **เว็บ** และ **หนังสือ/PDF** สำหรับเผยแผ่หรือพิมพ์

---

## แนวทางที่แนะนำ (ทำได้ทันที)

### ขั้นที่ 1: ใช้โครงเว็บหนังสือในโฟลเดอร์นี้

ในโฟลเดอร์ `html5` มีไฟล์ **`book.html`** เป็นหน้าแรกแบบหนังสือออนไลน์:

- **Sidebar ซ้าย**: สารบัญบท (00–11) ลิงก์ไปยัง `00.html` … `11.html`
- **พื้นที่อ่าน**: แสดงบทที่เลือก
- **ลิงก์ "อ่านทั้งเล่ม"**: ไปที่ `index.html` (รวมทุกบทในหน้าเดียว)

เปิดทดสอบโดยเปิดไฟล์ `book.html` ในเบราว์เซอร์ (หรือรัน local server เช่น `npx serve .` ในโฟลเดอร์ html5)

**ถ้าต้องการให้หน้า “หนังสือมีสารบัญ” เป็นหน้าแรกเมื่อเข้า site:** เปลี่ยนชื่อ `book.html` เป็น `index.html` และเปลี่ยนชื่อ `index.html` เดิม (เล่มรวม) เป็น `full.html` แล้วอัปเดตลิงก์ "อ่านทั้งเล่ม" ในหนังสือให้ชี้ไปที่ `full.html`

### ขั้นที่ 2: เพิ่มการค้นหา (Full-Text Search) ด้วย Pagefind

Pagefind เป็นการค้นหาแบบ static ไม่ต้องมี server รองรับภาษาไทยได้ดี

1. ติดตั้งและรัน index (รันครั้งเดียวหรือทุกครั้งที่อัปเดตเนื้อหา):

```bash
cd "PTF 4th Edition/html5"
npx -y pagefind --site . --output-path pagefind
```

2. ใน `book.html` มีส่วนสำหรับใส่ Pagefind UI อยู่แล้ว (ดูคอมเมนต์ในไฟล์)  
   หลังรันคำสั่งด้านบนแล้ว เปิด `book.html` ผ่าน **เว็บเซิร์ฟเวอร์** (เช่น `npx serve .` หรือ `python -m http.server`) เพื่อให้ Pagefind ทำงาน

3. ทางเลือกโฮสต์: อัปโหลดทั้งโฟลเดอร์ `html5` ขึ้น **GitHub Pages**, **Netlify** หรือ **Vercel** แล้วรัน Pagefind เป็นขั้นตอนหลัง build (ถ้าใช้ Netlify/Vercel กำหนด build command เป็น `npx pagefind --site . --output-path pagefind` และ publish folder เป็น `html5` หรือตามที่ตั้งค่า)

### ขั้นที่ 3: AI Search (ถ้าต้องการ)

- **DocSearch by Algolia (ฟรีสำหรับ documentation)**  
  - สมัครที่ [docsearch.algolia.com](https://docsearch.algolia.com/)  
  - ใส่ URL เว็บหนังสือที่โฮสต์แล้ว (เช่น `https://your-username.github.io/ptf-4th/`)  
  - Algolia จะ crawl และให้ script มาใส่ในเว็บ คุณจะได้ทั้ง full-text และ **Algolia Ask AI** (ตอบคำถามจากเนื้อหา)  
  - ต้องแสดงโลโก้ "Search by Algolia" ตามเงื่อนไขฟรี

- **ทางเลือกอื่น**: ใช้ API ของ AI (เช่น OpenAI) สร้างปุ่ม "ถาม AI จากบริบทหน้านี้" โดยส่งข้อความที่เลือกหรือทั้งหน้ามาให้ API — ทำได้แต่ต้องมี backend หรือ serverless function

---

## โฮสต์ฟรีที่เหมาะกับหนังสือออนไลน์

1. **GitHub Pages**  
   - สร้าง repo ใส่ไฟล์จากโฟลเดอร์ `html5` (รวม `pagefind` หลังรัน Pagefind)  
   - เปิด GitHub Pages ของ repo จะได้ URL แบบ `https://username.github.io/repo-name/`  
   - ใช้ `book.html` เป็นหน้าแรกได้โดยตั้งค่าเป็น index หรือเปลี่ยนชื่อเป็น `index.html` แล้วเก็บของเดิมไว้ชื่ออื่น

2. **Netlify**  
   - ลากโฟลเดอร์ `html5` ไปที่ netlify.com/drop  
   - หรือเชื่อมกับ Git แล้วตั้ง build command รัน Pagefind ตามขั้นที่ 2  
   - ได้ URL เช่น `https://random-name.netlify.app`

3. **Vercel**  
   - อัปโหลดโปรเจกต์หรือเชื่อม Git  
   - ตั้ง root directory เป็น `html5` (หรือที่เก็บเว็บหนังสือ) และเพิ่ม build step สำหรับ Pagefind ถ้าต้องการ

### โฮสต์ VitePress บน GitHub Pages

**VitePress โฮสต์บน GitHub ได้** โดยใช้ GitHub Pages (static site)

1. **ตั้ง `base` ใน config**  
   ถ้า URL จะเป็น `https://username.github.io/repo-name/` ให้ใน `.vitepress/config.ts` ใส่:
   ```ts
   base: '/repo-name/',   // ขึ้นต้นและลงท้ายด้วย /
   ```
   ถ้าใช้ User/Org site (`https://username.github.io/`) ให้ใช้ `base: '/'`

2. **Build**  
   `npm run docs:build` (หรือ `pnpm docs:build`) — ผลลัพธ์อยู่ที่ `.vitepress/dist`

3. **Deploy**  
   - ไปที่ repo → **Settings → Pages** → Source เลือก **GitHub Actions**  
   - สร้าง workflow ใน `.github/workflows/deploy.yml` ให้รัน `npm run docs:build` แล้วอัปโหลดโฟลเดอร์ `.vitepress/dist` ไปที่ branch ที่ใช้กับ GitHub Pages (เช่น `gh-pages`)  
   - คู่มืออย่างเป็นทางการ: [vitepress.dev/guide/deploy](https://vitepress.dev/guide/deploy)

---

## สรุปลำดับการทำ

1. เปิด `book.html` ในโฟลเดอร์ `html5` ทดสอบการเลื่อนบทและลิงก์
2. รัน Pagefind ในโฟลเดอร์ `html5` แล้วเปิดเว็บผ่าน local server เพื่อทดสอบ search
3. เลือกโฮสต์ (GitHub Pages / Netlify / Vercel) แล้วอัปโหลดโฟลเดอร์ `html5` (รวมโฟลเดอร์ `pagefind`)
4. เมื่อเว็บขึ้นแล้ว ถ้าต้องการ AI search สมัคร DocSearch (Algolia) แล้วใส่ script ที่ได้ลงใน `book.html`

ถ้าต้องการเปลี่ยนโครง (เช่น แยกบทเป็น Markdown สำหรับ Docusaurus/VuePress) หรือออกแบบหน้าใหม่เพิ่ม บอกได้ครับว่าจะเดินทางแบบไหนต่อ
