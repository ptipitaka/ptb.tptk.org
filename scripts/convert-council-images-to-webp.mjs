#!/usr/bin/env node
/**
 * Convert images in docs/public/images/03-buddhist-council-illustration
 * from jpg/png to webp (quality 85). Keeps originals; output is .webp.
 */
import sharp from 'sharp'
import fs from 'fs'
import path from 'path'
import { fileURLToPath } from 'url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const imageDir = path.join(__dirname, '..', 'docs', 'public', 'images', '03-buddhist-council-illustration')

const names = ['00.jpg', '01.png', '02.jpg', '03.png', '04.png', '05.jpg', '06.png']

for (const name of names) {
  const src = path.join(imageDir, name)
  const base = path.basename(name, path.extname(name))
  const dest = path.join(imageDir, `${base}.webp`)
  if (!fs.existsSync(src)) {
    console.warn('Skip (not found):', src)
    continue
  }
  await sharp(src)
    .webp({ quality: 85 })
    .toFile(dest)
  const statIn = fs.statSync(src)
  const statOut = fs.statSync(dest)
  console.log(`${name} → ${base}.webp  (${(statIn.size / 1024).toFixed(0)} KB → ${(statOut.size / 1024).toFixed(0)} KB)`)
}

console.log('Done.')
