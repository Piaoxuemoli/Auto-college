#!/usr/bin/env node

/**
 * Auto-college skills installer
 *
 * Detects the agent environment (Claude Code / Cursor) and copies skills there.
 * When no known environment marker is found (e.g. plain CLI usage), installs to
 * .agent/skills (created if missing) so the skills stay agent-neutral.
 * Run from your project root:
 *   curl -fsSL https://raw.githubusercontent.com/Piaoxuemoli/Auto-college/master/setup.js | node
 */

const fs = require("fs");
const path = require("path");
const { execFileSync } = require("child_process");

const REPO_URL = "https://github.com/Piaoxuemoli/Auto-college.git";
const SKILLS = ["lab-report", "terminal-screenshot"];

const cwd = process.cwd();

const platforms = [
  { name: "Claude Code", dir: ".claude/skills", marker: ".claude" },
  { name: "Cursor", dir: ".cursor/skills", marker: ".cursor" },
];

function findPlatform() {
  for (const p of platforms) {
    if (fs.existsSync(path.join(cwd, p.marker))) return p;
  }
  // Agent-neutral fallback for CLI installs: .agent/skills, created on demand.
  return { name: "Generic agent (.agent)", dir: ".agent/skills", marker: ".agent" };
}

function main() {
  const platform = findPlatform();
  console.log("Platform: " + platform.name);
  console.log("Install to: " + path.join(cwd, platform.dir));

  const destDir = path.join(cwd, platform.dir);
  fs.mkdirSync(destDir, { recursive: true });

  const tmpDir = path.join(cwd, ".auto-college-tmp");
  try {
    console.log("Cloning " + REPO_URL + " ...");
    execFileSync("git", ["clone", "--depth", "1", REPO_URL, tmpDir], { stdio: "inherit" });

    for (const skill of SKILLS) {
      const src = path.join(tmpDir, "skills", skill);
      const dest = path.join(destDir, skill);
      if (fs.existsSync(src)) {
        fs.cpSync(src, dest, { recursive: true });
        console.log("  " + skill);
      } else {
        console.log("  " + skill + " (not found)");
      }
    }

    console.log("\nDone! Restart your agent to load the skills.");
  } finally {
    try { fs.rmSync(tmpDir, { recursive: true, force: true }); } catch (e) {}
  }
}

main();
