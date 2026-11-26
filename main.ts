// News-image entry for 25 November 2026: the program copies the rendered
// infographic that sits beside it into the grader's output directory.
// No network and no randomness, so every run writes the same bytes.
import { copyFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
copyFileSync(
  new URL('./entry.png', import.meta.url),
  join(outDir, 'entry.png'),
);
