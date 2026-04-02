วิธี Export Book เป็น HTML5 รวมเล่ม
====================================

ขั้นตอนที่ 1 – Export จาก InDesign
----------------------------------
1. เปิด Adobe InDesign
2. เปิดไฟล์ Book: File > Open > เลือก FullBook.indb
3. รันสคริปต์: File > Scripts > User > ExportBookToHTML.jsx
   (ถ้าไม่มีใน User ให้ไปที่ File > Scripts > Browse... แล้วเลือกไฟล์ ExportBookToHTML.jsx ที่อยู่โฟลเดอร์ PTF 4th Edition)
4. รอจนสคริปต์ export ครบทุกบท จะได้ไฟล์ 00.html, 01.html, ... ในโฟลเดอร์ html5

หมายเหตุ: InDesign จะ export เป็นรูปแบบ HTML/XHTML ตามที่โปรแกรมรองรับ ลำดับตามลำดับใน Book panel

ขั้นตอนที่ 2 – รวมเป็นเล่มเดียว
--------------------------------
1. เปิด PowerShell
2. รันคำสั่ง:
   cd "C:\Users\conta\Desktop\PTF 4th Edition"
   .\CombineHTML.ps1
3. จะได้ไฟล์ index.html ในโฟลเดอร์ html5 เป็นหนังสือรวมเล่มเรียงตามลำดับ

ถ้า PowerShell บล็อกการรันสคริปต์ ให้รันคำสั่งนี้ครั้งเดียว (Run as Administrator ไม่จำเป็น):
   Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
