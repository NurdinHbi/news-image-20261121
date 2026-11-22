// Entry point: copies the generated poster to the output directory.
// Node stdlib only. Does NOT delete the output directory itself.
import { copyFileSync, existsSync, mkdirSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = resolve(process.env.MAKEFUN_OUTPUT_DIR ?? "output");
mkdirSync(outDir, { recursive: true });
const src = join(here, "entry.png");
if (!existsSync(src)) {
  throw new Error(`entry.png not found at ${src} — run generate_poster.py first`);
}
copyFileSync(src, join(outDir, "entry.png"));
console.log(`wrote ${join(outDir, "entry.png")}`);
