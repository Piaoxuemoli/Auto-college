#!/usr/bin/env node

/**
 * Auto-college skills installer
 *
 * Detects Claude Code / Cursor and copies skills to the current project.
 * Run from your project root:
 *   curl -fsSL https://raw.githubusercontent.com/Piaoxuemoli/Auto-college/master/setup.mjs | node
 */

const fs = require("fs");
const path = require("path");
const { execSync } = require("child_process");

const REPO_URL = "https://github.com/Piaoxuemoli/Auto-college.git";
const SKILLS = ["coursework-helper", "lab-report", "terminal-screenshot", "study-index", "paper-writer"];

const cwd = process.cwd();

const platforms = [
  { name: "Claude Code", dir: ".claude/skills", marker: ".claude" },
  { name: "Cursor", dir: ".cursor/skills", marker: ".cursor" },
];

function findPlatform() {
  for (const p of platforms) {
    if (fs.existsSync(path.join(cwd, p.marker))) return p;
  }
  return platforms[0]; // default to Claude Code
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
    execSync('git clone --depth 1 "' + REPO_URL + '" "' + tmpDir + '"', { stdio: "inherit" });

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
