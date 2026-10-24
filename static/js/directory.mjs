import { STATE_KEY, DISCOVERY_KEY, readSession, writeSession, dateLabel, berlinDate } from "./site.mjs";
import { degreeLabel, STATUS_LABELS, filterRecords } from "./matching.mjs";

const root = document.querySelector("[data-directory]");
const form = document.querySelector("#filter-form");
const search = document.querySelector("#search");
const sort = document.querySelector("#sort");
const results = document.querySelector("#results");
const pagination = document.querySelector("#pagination");
const activeFilters = document.querySelector("#active-filters");
const dialog = document.querySelector("#filter-dialog");
const pageSize = Number(root.dataset.pageSize);
const preview = document.body.dataset.preview === "true";
const today = berlinDate();
const defaults = () => ({ query: "", degrees: [], subjects: [], residence: "", purposes: [], availability: "", institution: "" });
const mobile = matchMedia("(max-width: 850px)");
let state = { filters: defaults(), sort: "relevance", page: Number(root.dataset.page), scroll: 0 };
let records = [];
let draftFilters = null;
let searchTimer;
let announcementTimer;

function element(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

function arrow() {
  const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  svg.setAttribute("class", "icon");
  svg.setAttribute("viewBox", "0 0 24 24");
  svg.setAttribute("fill", "none");
  svg.setAttribute("stroke", "currentColor");
  svg.setAttribute("stroke-width", "1.5");
  svg.setAttribute("aria-hidden", "true");
  const path = document.createElementNS(svg.namespaceURI, "path");
  path.setAttribute("d", "M4 12h16m-6-6 6 6-6 6");
  svg.append(path);
  return svg;
}

function readForm() {
  const values = new FormData(form);
  return {
    ...(dialog.open && draftFilters ? draftFilters : state.filters),
    degrees: values.getAll("degrees"), subjects: values.getAll("subjects"), purposes: values.getAll("purposes"),
    residence: values.get("residence") || "",
    availability: values.get("availability") || "", institution: values.get("institution") || "",
  };
}

function populateForm(filters) {
  for (const input of form.querySelectorAll("input[type=checkbox]")) input.checked = filters[input.name]?.includes(input.value) || false;
  for (const select of form.querySelectorAll("select")) select.value = filters[select.name] || "";
}

function sanitiseFilters(value) {
  const filters = defaults();
  if (!value || typeof value !== "object") return filters;
  filters.query = typeof value.query === "string" ? value.query.slice(0, 300) : "";
  for (const name of ["degrees", "subjects", "purposes"]) {
    const known = [...form.querySelectorAll(`input[name="${name}"]`)].map(input => input.value);
    filters[name] = Array.isArray(value[name]) ? [...new Set(value[name].filter(v => known.includes(v)))] : [];
  }
  for (const name of ["residence", "availability", "institution"]) {
    const select = form.elements.namedItem(name);
    filters[name] = [...select.options].some(option => option.value === value[name]) ? value[name] : "";
  }
  return filters;
}

function saveState() {
  state.scroll = scrollY;
  writeSession(STATE_KEY, { ...state, fingerprint: root.dataset.fingerprint });
}

function makeCard(entry) {
  const { record, match, round } = entry;
  const article = element("article", "scholarship-card");
  const top = element("div", "card-top");
  top.append(element("span", "provider", record.provider), element("span", `status status-${round.status}`, STATUS_LABELS[round.status]));
  const title = element("h3");
  const link = element("a", "card-link", record.title);
  link.href = record.url;
  title.append(link);
  const tags = element("div", "card-tags");
  const degrees = record.degrees.values || [];
  if (record.degrees.status === "unrestricted") tags.append(element("span", "", "All degree levels"));
  else if (degrees.length) degrees.slice(0, 3).forEach(value => tags.append(element("span", "", degreeLabel(value))));
  else tags.append(element("span", "", "Study level needs checking"));
  if (preview && record.is_draft) tags.append(element("span", "draft-tag", "Draft"));
  const bottom = element("div", "card-bottom");
  const funding = element("div");
  funding.append(element("span", "meta-label", "Funding"), element("strong", "", record.funding));
  const deadline = element("div");
  deadline.append(element("span", "meta-label", round.applicable_country_codes ? "Country-specific deadline" : "Deadline"),
    element("strong", "", round.deadline ? dateLabel(round.deadline) : round.status === "rolling" ? "Rolling applications" : "Not announced"));
  const icon = element("span", "card-arrow");
  icon.setAttribute("aria-hidden", "true");
  icon.append(arrow());
  bottom.append(funding, deadline, icon);
  article.append(top, title, element("p", "card-summary", record.summary), tags, bottom);
  if (match.status !== "unselected") {
    const note = element("p", `match-note${match.status === "checking" ? " needs-checking" : ""}`);
    note.append(element("strong", "", match.status === "checking" ? "Needs checking. " : "Potential match. "));
    note.append(document.createTextNode(match.reasons.length ? match.reasons.join(" ") : "Read the full additional requirements."));
    article.append(note);
  }
  const item = element("li");
  item.append(article);
  return item;
}

function filterLabel(name, value) {
  if (name === "query") return `Search: ${value}`;
  if (["degrees", "subjects", "purposes"].includes(name)) {
    const input = [...form.querySelectorAll(`input[name="${name}"]`)].find(node => node.value === value);
    return input?.closest("label").textContent.trim() || value;
  }
  const select = form.elements.namedItem(name);
  return [...select.options].find(option => option.value === value)?.textContent || value;
}

function renderChips() {
  const fragment = document.createDocumentFragment();
  let count = 0;
  for (const [name, selected] of Object.entries(state.filters)) {
    for (const value of Array.isArray(selected) ? selected : selected ? [selected] : []) {
      count++;
      const chip = element("button", "filter-chip", filterLabel(name, value));
      chip.type = "button";
      chip.setAttribute("aria-label", `Remove ${filterLabel(name, value)} filter`);
      const close = element("span", "", "×");
      close.setAttribute("aria-hidden", "true");
      chip.append(close);
      chip.addEventListener("click", () => {
        state.filters[name] = Array.isArray(selected) ? selected.filter(item => item !== value) : "";
        search.value = state.filters.query;
        draftFilters = null;
        populateForm(state.filters);
        state.page = 1;
        render();
      });
      fragment.append(chip);
    }
  }
  activeFilters.replaceChildren(fragment);
  activeFilters.hidden = count === 0;
  document.querySelector("#filter-count").textContent = count ? `(${count})` : "";
}

function pageLink(page, text, label, current) {
  const link = element("a", "page-button", text);
  link.href = page === 1 ? "/scholarships/" : `/scholarships/page/${page}/`;
  link.dataset.page = String(page);
  link.setAttribute("aria-label", label);
  if (current) link.setAttribute("aria-current", "page");
  return link;
}

function renderPagination(total, pages) {
  const links = element("div");
  if (state.page > 1) links.append(pageLink(state.page - 1, "←", "Previous page"));
  let previous = 0;
  for (let page = 1; page <= pages; page++) {
    if (![1, pages].includes(page) && Math.abs(page - state.page) > 1) continue;
    if (previous && page - previous > 1) links.append(element("span", "page-ellipsis", "…"));
    links.append(pageLink(page, String(page), `Page ${page}`, page === state.page));
    previous = page;
  }
  if (state.page < pages) links.append(pageLink(state.page + 1, "→", "Next page"));
  pagination.replaceChildren(element("span", "", `Page ${state.page}`), links);
  pagination.hidden = total === 0;
}

function render(announce = true) {
  const matches = filterRecords(records, state.filters, state.sort, today);
  const filtered = Object.values(state.filters).some(value => Array.isArray(value) ? value.length > 0 : value.trim() !== "");
  const resultHeading = filtered ? `${matches.length} scholarship${matches.length === 1 ? "" : "s"} found` : "Scholarships";
  document.querySelector("#result-heading").textContent = resultHeading;
  const pages = Math.max(1, Math.ceil(matches.length / pageSize));
  state.page = Math.min(Math.max(1, state.page), pages);
  const fragment = document.createDocumentFragment();
  matches.slice((state.page - 1) * pageSize, state.page * pageSize).forEach(entry => fragment.append(makeCard(entry)));
  results.replaceChildren(fragment);
  document.querySelector("#empty-state").hidden = matches.length !== 0;
  const checking = matches.some(entry => entry.match.status === "checking");
  document.querySelector("#result-context").textContent = checking
    ? "Some criteria need checking. Read the full conditions."
    : preview ? "Draft catalogue · Explore, compare, check the details." : "Explore, compare, check the details.";
  renderChips();
  renderPagination(matches.length, pages);
  if (announce) {
    clearTimeout(announcementTimer);
    announcementTimer = setTimeout(() => {
      document.querySelector("#result-announcement").textContent = matches.length
        ? `${filtered ? resultHeading : "Scholarship results updated"}. Page ${state.page}.`
        : "No scholarships match your search or filters.";
    }, 220);
  }
  saveState();
}

function reset() {
  clearTimeout(searchTimer);
  state.filters = defaults();
  state.page = 1;
  draftFilters = null;
  search.value = "";
  populateForm(state.filters);
  render();
}

function closePanel(action) {
  if (action === "apply") {
    state.filters = readForm();
    search.value = state.filters.query;
    state.page = 1;
    draftFilters = null;
  } else if (action === "cancel") draftFilters = null;
  else draftFilters = readForm();
  dialog.close();
  document.querySelector("#filter-home").append(form);
  populateForm(state.filters);
  if (action === "apply") render();
  document.querySelector("#open-filters").focus({ preventScroll: true });
}

function connectControls() {
  form.addEventListener("submit", event => event.preventDefault());
  form.addEventListener("change", () => {
    if (dialog.open) { draftFilters = readForm(); return; }
    state.filters = readForm();
    state.page = 1;
    draftFilters = null;
    render();
  });
  search.addEventListener("input", () => {
    state.filters.query = search.value;
    state.page = 1;
    clearTimeout(searchTimer);
    searchTimer = setTimeout(render, 125);
  });
  sort.addEventListener("change", () => { state.sort = sort.value; state.page = 1; render(); });
  pagination.addEventListener("click", event => {
    const link = event.target.closest("a[data-page]");
    if (!link || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    event.preventDefault();
    state.page = Number(link.dataset.page);
    render();
    document.querySelector("#result-heading").focus({ preventScroll: true });
    document.querySelector(".results-section").scrollIntoView({ block: "start" });
  });
  document.querySelectorAll("[data-reset]").forEach(button => button.addEventListener("click", () => {
    if (dialog.open) { draftFilters = defaults(); populateForm(draftFilters); }
    else reset();
  }));
  document.querySelector("#open-filters").addEventListener("click", () => {
    populateForm(draftFilters || state.filters);
    document.querySelector("#dialog-form-host").append(form);
    dialog.showModal();
  });
  document.querySelector("#apply-filters").addEventListener("click", () => closePanel("apply"));
  document.querySelector("#cancel-filters").addEventListener("click", () => closePanel("cancel"));
  document.querySelector("#close-filters").addEventListener("click", () => closePanel("close"));
  dialog.addEventListener("cancel", event => { event.preventDefault(); closePanel("close"); });
  mobile.addEventListener("change", () => { if (dialog.open) closePanel("cancel"); });
  addEventListener("pagehide", saveState);
  results.addEventListener("click", saveState);
  addEventListener("pageshow", event => {
    if (event.persisted) requestAnimationFrame(() => scrollTo(0, readSession(STATE_KEY)?.scroll || 0));
  });
}

async function initialise() {
  try {
    const response = await fetch(root.dataset.index, { credentials: "same-origin" });
    if (!response.ok) throw new Error("Catalogue unavailable");
    records = await response.json();
    const institutions = [...new Set(records.flatMap(record => record.institutions.values || []))].sort();
    institutions.forEach(value => form.elements.namedItem("institution").add(new Option(value, value)));
    const stored = readSession(STATE_KEY);
    if (stored?.filters && typeof stored.filters === "object") {
      state.filters = sanitiseFilters(stored.filters);
      state.sort = ["relevance", "deadline", "name"].includes(stored.sort) ? stored.sort : "relevance";
      state.page = Number.isInteger(stored.page) ? stored.page : 1;
      state.scroll = Number.isFinite(stored.scroll) ? Math.max(0, stored.scroll) : 0;
    }
    const discovery = readSession(DISCOVERY_KEY);
    if (discovery) {
      state.filters = sanitiseFilters(discovery);
      state.page = 1;
      state.scroll = 0;
      writeSession(DISCOVERY_KEY, null);
    } else if (root.dataset.page !== "1") state.page = Number(root.dataset.page);
    const restoreScroll = state.scroll;
    search.value = state.filters.query;
    sort.value = state.sort;
    populateForm(state.filters);
    connectControls();
    root.classList.add("is-enhanced");
    history.scrollRestoration = "manual";
    render(false);
    requestAnimationFrame(() => scrollTo(0, restoreScroll));
  } catch {
    document.documentElement.classList.remove("js");
    const message = document.querySelector("#directory-error");
    message.textContent = "Search and filters couldn’t load. You can still browse the directory and open every listing below.";
    message.hidden = false;
  }
}

initialise();
