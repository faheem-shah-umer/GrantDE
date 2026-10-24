(() => {
  document.documentElement.classList.add("js");
  let saved;
  try { saved = localStorage.getItem("grantde.theme"); } catch { /* Storage is optional. */ }
  const theme = saved === "light" || saved === "dark" ? saved
    : matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  document.documentElement.dataset.theme = theme;
  document.querySelector('meta[name="theme-color"]').content = theme === "dark" ? "#101014" : "#f7f7f3";
})();
