import fs from 'node:fs';
import path from 'node:path';

const distDir = path.resolve('dist');
if (!fs.existsSync(distDir)) {
  fs.mkdirSync(distDir, { recursive: true });
}

function copyDirRecursive(src, dest) {
  if (!fs.existsSync(src)) return;
  if (!fs.existsSync(dest)) fs.mkdirSync(dest, { recursive: true });
  for (const entry of fs.readdirSync(src, { withFileTypes: true })) {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);
    if (entry.isDirectory()) {
      copyDirRecursive(srcPath, destPath);
    } else {
      fs.copyFileSync(srcPath, destPath);
    }
  }
}

// Ensure dist has css, js, html
copyDirRecursive('frontend', distDir);
if (fs.existsSync('css')) copyDirRecursive('css', path.join(distDir, 'css'));
if (fs.existsSync('js')) copyDirRecursive('js', path.join(distDir, 'js'));

for (const file of ['index.html', 'trends.html', 'trend-detail.html', 'regional.html', 'forecast.html']) {
  if (fs.existsSync(file)) {
    fs.copyFileSync(file, path.join(distDir, file));
  }
}

console.log('[Build] Successfully built static assets in dist/');
