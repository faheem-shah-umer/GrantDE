const DEGREE_LABELS = {
  bachelor: "Bachelor’s", master: "Master’s", doctorate: "Doctorate", state_exam: "State examination",
  diploma: "Diploma", preparatory: "Preparatory study", short_course: "Short course", exchange: "Exchange", other: "Other",
};
export const STATUS_LABELS = {
  open: "Open", upcoming: "Upcoming", closed: "Closed", rolling: "Rolling applications", dates_unconfirmed: "Dates unconfirmed",
};
export const degreeLabel = value => DEGREE_LABELS[value] || value;

export function currentStatus(round, today) {
  if (round.deadline && round.deadline < today) return "closed";
  if (round.opens_on && round.opens_on > today) return "upcoming";
  const recorded = round.recorded_status;
  if (["open", "upcoming"].includes(recorded) && round.as_of < today) {
    return recorded === "open" && round.deadline && round.deadline >= today ? "open" : "dates_unconfirmed";
  }
  return recorded;
}

export function relevantRounds(record, today) {
  return record.rounds.map(round => ({ ...round, status: currentStatus(round, today) }));
}

export function displayRound(record, today) {
  const priority = ["open", "upcoming", "rolling", "dates_unconfirmed", "closed"];
  return relevantRounds(record, today).sort((left, right) =>
    priority.indexOf(left.status) - priority.indexOf(right.status)
    || (left.deadline || "9999").localeCompare(right.deadline || "9999") || left.id.localeCompare(right.id)
  )[0] || { status: "dates_unconfirmed", deadline: null, applicable_country_codes: null };
}

function criterionMatch(criterion, selected) {
  if (!selected.length || criterion.status === "unrestricted") return "pass";
  if (criterion.status === "unknown" || !criterion.values?.length) return "unknown";
  return selected.some(value => criterion.values.includes(value)) ? "pass" : "fail";
}

export function evaluateRecord(record, filters) {
  const checks = [];
  if (filters.degrees.length) checks.push(["Degree level", criterionMatch(record.degrees, filters.degrees)]);
  if (filters.subjects.length) checks.push(["Subject area", criterionMatch(record.subjects, filters.subjects)]);
  if (filters.residence) checks.push(["Residence conditions", criterionMatch(record.residence, [filters.residence])]);
  if (filters.institution) checks.push(["University restriction", criterionMatch(record.institutions, [filters.institution])]);
  if (filters.purposes.length) checks.push(["Funding coverage", !record.purposes.length ? "unknown"
    : filters.purposes.some(value => record.purposes.includes(value)) ? "pass" : "fail"]);
  const reasons = [];
  let failed = false;
  for (const [name, result] of checks) {
    if (result === "fail" && record.has_exceptions) reasons.push(`${name}: check the listed exceptions.`);
    else if (result === "fail") { failed = true; reasons.push(`${name} does not meet a listed condition.`); }
    else if (result === "unknown") reasons.push(`${name} needs checking.`);
  }
  return { status: failed ? "excluded" : reasons.length ? "checking" : checks.length ? "potential" : "unselected", reasons };
}

const normalise = value => value.normalize("NFKD").replace(/[\u0300-\u036f]/g, "").toLowerCase()
  .replace(/[’']/g, "").replace(/[_-]/g, " ");

export function filterRecords(records, filters, sort, today) {
  const words = normalise(filters.query.trim()).split(/\s+/).filter(Boolean);
  const matches = [];
  for (const record of records) {
    const text = normalise([record.title, record.provider, record.summary,
      ...(record.degrees.values || []).map(degreeLabel), ...(record.subjects.values || [])].join(" "));
    if (!words.every(word => text.includes(word))) continue;
    const match = evaluateRecord(record, filters);
    if (match.status === "excluded") continue;
    const rounds = relevantRounds(record, today);
    if (filters.availability && !rounds.some(round => round.status === filters.availability)
      && !(filters.availability === "dates_unconfirmed" && !rounds.length)) continue;
    const nearestKnown = sort === "deadline" ? rounds.filter(round => round.deadline && round.deadline >= today)
      .sort((a, b) => a.deadline.localeCompare(b.deadline) || a.id.localeCompare(b.id))[0] : null;
    matches.push({ record, match, round: nearestKnown || displayRound(record, today) });
  }
  const byName = (a, b) => a.record.title.localeCompare(b.record.title, "en") || a.record.id.localeCompare(b.record.id);
  const deadline = entry => entry.round.deadline && entry.round.deadline >= today ? entry.round.deadline : "9999";
  const tiers = ["potential", "checking", "unselected"];
  matches.sort((a, b) => {
    if (sort === "deadline") return deadline(a).localeCompare(deadline(b)) || byName(a, b);
    if (sort === "relevance") return tiers.indexOf(a.match.status) - tiers.indexOf(b.match.status) || byName(a, b);
    return byName(a, b);
  });
  return matches;
}
