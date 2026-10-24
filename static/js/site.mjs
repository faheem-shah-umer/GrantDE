export const STATE_KEY = "grantde.directory.v1";
export const DISCOVERY_KEY = "grantde.discovery.v1";

const themeButton = document.querySelector("#theme-toggle");

function updateThemeButton() {
  const dark = document.documentElement.dataset.theme === "dark";
  const action = dark ? "Switch to light mode" : "Switch to dark mode";
  themeButton.setAttribute("aria-label", action);
  themeButton.setAttribute("title", action);
  themeButton.setAttribute("aria-pressed", String(dark));
  document.querySelector('meta[name="theme-color"]').content = dark ? "#101014" : "#f7f7f3";
}

if (themeButton) {
  updateThemeButton();
  themeButton.hidden = false;
  themeButton.addEventListener("click", () => {
    const theme = document.documentElement.dataset.theme === "dark" ? "light" : "dark";
    document.documentElement.dataset.theme = theme;
    try { localStorage.setItem("grantde.theme", theme); } catch { /* The toggle still works without storage. */ }
    updateThemeButton();
  });
}

export function readSession(key) {
  try { return JSON.parse(sessionStorage.getItem(key)); } catch { return null; }
}

export function writeSession(key, value) {
  try { sessionStorage.setItem(key, JSON.stringify(value)); } catch { /* Browsing still works without storage. */ }
}

export function countryName(code) {
  try { return new Intl.DisplayNames(["en"], { type: "region" }).of(code); } catch { return code; }
}

export function dateLabel(value) {
  if (!value) return "Not announced";
  return new Intl.DateTimeFormat("en-GB", { day: "numeric", month: "short", year: "numeric", timeZone: "UTC" })
    .format(new Date(`${value}T12:00:00Z`));
}

export function berlinDate() {
  const parts = new Intl.DateTimeFormat("en", { timeZone: "Europe/Berlin", year: "numeric", month: "2-digit", day: "2-digit" })
    .formatToParts(new Date());
  const value = type => parts.find(part => part.type === type).value;
  return `${value("year")}-${value("month")}-${value("day")}`;
}

document.querySelectorAll("[data-degree]").forEach(link => {
  link.addEventListener("click", () => writeSession(DISCOVERY_KEY, { degrees: [link.dataset.degree] }));
});
document.querySelectorAll("[data-country]").forEach(node => { node.textContent = countryName(node.dataset.country); });
