import path from "path"
import { FilePath } from "./path"
import { globby } from "globby"

export function toPosixPath(fp: string): string {
  return fp.split(path.sep).join("/")
}

export async function glob(
  pattern: string,
  cwd: string,
  ignorePatterns: string[],
): Promise<FilePath[]> {
  const fps = (
    await globby(pattern, {
      cwd,
      ignore: ignorePatterns,
      // Content is generated and intentionally ignored by Git in this vault.
      // Publishing selection is made by prepare_site.py and ignorePatterns.
      gitignore: false,
    })
  ).map(toPosixPath)
  return fps as FilePath[]
}
