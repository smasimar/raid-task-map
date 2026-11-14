// Headless run of index.html with fixtures shaped like json.tarkov.dev + TarkovTracker /progress
const fs = require("fs");
const { JSDOM } = require("jsdom");
const path = require("path");
const APP = path.resolve(__dirname, "..");
let html = fs.readFileSync(`${APP}/index.html`, "utf8");
const leafletJs = fs.readFileSync(require.resolve("leaflet/dist/leaflet.js"), "utf8");
html = html.replace(/<link rel="stylesheet" href="https:\/\/unpkg[^>]+>/, "").replace(/<script src="https:\/\/unpkg[^>]+><\/script>/, `<script>${leafletJs}</script>`);
const mapsCfg = JSON.parse(fs.readFileSync(`${APP}/maps.json`, "utf8"));

const CUST = "56f40101d2720b2a4d8b45d6", WOODS = "5704e3c2d2720bac5b8b4567", PRAPOR = "54cb50c76803fa8b248b4571", JAEGER = "5c0647fdd443bc2504c2d371";
const task = (id, o) => ({ id, name: `${id} name`, trader: PRAPOR, minPlayerLevel: 1, taskRequirements: [], traderRequirements: [], objectives: [], failConditions: [], finishRewards: { traderUnlock: [] }, factionName: "Any", normalizedName: id, wikiLink: "https://wiki/" + id, ...o });
const tasks = {
  debut: task("debut", { objectives: [{ id: "o1", description: "o1", type: "shoot", count: 5, maps: [CUST] }, { id: "o2", description: "o2", type: "giveItem", count: 2 }] }),
  checking: task("checking", { taskRequirements: [{ task: "debut", status: ["complete"] }], objectives: [{ id: "o3", description: "o3", type: "visit", zones: [{ id: "z", map: CUST, position: { x: 100, y: 1, z: -50 }, outline: [{ x: 95, y: 1, z: -55 }, { x: 105, y: 1, z: -55 }, { x: 105, y: 1, z: -45 }] }], maps: [CUST] }, { id: "o3b", description: "o3b", type: "findQuestItem", possibleLocations: [{ map: CUST, positions: [{ x: 10, y: 2, z: 20 }, { x: 11, y: 2, z: 21 }] }], maps: [CUST] }] }),
  woodsTask: task("woodsTask", { objectives: [{ id: "o4", description: "o4", type: "visit", zones: [{ id: "w", map: WOODS, position: { x: 0, y: 0, z: 0 } }], maps: [WOODS] }] }),
  highLevel: task("highLevel", { minPlayerLevel: 40, objectives: [{ id: "o5", description: "o5", type: "visit", maps: [CUST] }] }),
  jaegerTask: task("jaegerTask", { trader: JAEGER, objectives: [{ id: "o6", description: "o6", type: "visit", maps: [CUST] }] }),
  unlockJaeger: task("unlockJaeger", { finishRewards: { traderUnlock: [JAEGER] }, objectives: [{ id: "o7", description: "o7", type: "visit", maps: [WOODS] }] }),
  needsActive: task("needsActive", { taskRequirements: [{ task: "checking", status: ["active"] }], objectives: [{ id: "o8", description: "o8", type: "visit", maps: [CUST] }] }),
  extraZone: task("extraZone", { objectives: [{ id: "o10", description: "o10", type: "visit", zones: [{ id: "zz", map: CUST, position: { x: 50, y: 1, z: 50 } }], maps: [CUST] }] }),
  nades: task("nades", { objectives: [{ id: "o11", description: "o11", type: "shoot", count: 5 }] }),
  gunsmith: task("gunsmith", { objectives: [{ id: "o12", description: "o12", type: "buildWeapon" }] }),
  arena: task("arena", { objectives: [{ id: "o13", description: "o13", type: "visit" }] }),
  doneTask: task("doneTask", { objectives: [{ id: "o9", description: "o9", type: "visit", maps: [CUST] }] }),
};
const en = { "debut name": "Debut", "checking name": "Checking", "woodsTask name": "Woods Walk", "highLevel name": "Endgame", "jaegerTask name": "Jaeger Job", "unlockJaeger name": "Meet Jaeger", "needsActive name": "Follow Up", "doneTask name": "Old News",
  o1: "Kill 5 Scavs on Customs", o2: "Hand over 2 bolts", o3: "Locate the warehouse", o3b: "Find the folder", o4: "Visit the sawmill", o5: "x", o6: "x", o7: "x", o8: "Do the follow up on Customs", o9: "x", "extraZone name": "Extra Zone", o10: "Visit the extra zone",
  "nades name": "Nade Kills", o11: "Eliminate any target with grenades", "gunsmith name": "Gun Build", o12: "Modify a weapon", "arena name": "Arena Match", o13: "Play a match" };
const apiMaps = {
  [CUST]: { id: CUST, name: `${CUST} Name`, normalizedName: "customs", nameId: "bigmap", scenePath: "maps/customs_preset.bundle", raidDuration: 35, extracts: [
    { id: "e1", name: "ex_pmc_a", faction: "pmc", position: { x: 300, y: 0, z: -100 }, outline: [{ x: 1, y: 0, z: 1 }, { x: 2, y: 0, z: 2 }, { x: 3, y: 0, z: 1 }], switches: [] },
    { id: "e2", name: "ex_scav_b", faction: "scav", position: { x: 0, y: 0, z: 0 }, switches: [] },
    { id: "e3", name: "ex_shared_c", faction: "shared", position: { x: -200, y: 0, z: 50 }, switches: ["s"] },
    { id: "e4", name: "ex_null_d", faction: null, position: { x: -100, y: 0, z: 60 }, switches: [] }] },
  [WOODS]: { id: WOODS, name: `${WOODS} Name`, normalizedName: "woods", nameId: "Woods", scenePath: "maps/woods_preset.bundle", raidDuration: 35, extracts: [] },
};
const mapsEn = { [`${CUST} Name`]: "Customs", [`${WOODS} Name`]: "Woods", ex_pmc_a: "Crossroads", ex_shared_c: "Boat", ex_null_d: "Coop thing" };
const progress = { data: { tasksProgress: [{ id: "doneTask", complete: true }], taskObjectivesProgress: [{ id: "o1", complete: false, count: 3 }, { id: "o2", complete: true }], tradersProgress: [{ id: PRAPOR, level: 2, reputation: 0.2 }], displayName: "Tester", playerLevel: 12, pmcFaction: "USEC" }, meta: {} };

const routes = {
  "/maps.json": mapsCfg,
  "/api/config": { hasToken: true, tokenHint: "PVP_…abcd", gameMode: "regular", screenshotsDir: "C:/s", screenshotsDirExists: true, deleteScreenshots: false, logsDir: "", logsDirActive: "C:/g/Logs", logsDirExists: true, autoTick: true },
  "/api/state": { position: null, game: null },
  "/api/progress": progress,
  "https://json.tarkov.dev/regular/tasks": { data: { tasks } },
  "https://json.tarkov.dev/regular/tasks_en": { data: en },
  "https://json.tarkov.dev/regular/maps": { data: { maps: apiMaps } },
  "https://json.tarkov.dev/regular/maps_en": { data: mapsEn },
  "https://json.tarkov.dev/regular/traders": { data: { [PRAPOR]: { id: PRAPOR, name: "p", normalizedName: "prapor" }, [JAEGER]: { id: JAEGER, name: "j", normalizedName: "jaeger" } } },
  "https://json.tarkov.dev/regular/traders_en": { data: { p: "Prapor", j: "Jaeger" } },
};
// a small copy of the helper's quest list (state.json): it applies the changes and sends the "quests" event
const quests = { modes: {}, migrated: [] };
let pastLogsApplied = 0;
function questPost(w, body) {
  const m = quests.modes[body.mode] ??= { selected: [], custom: [] };
  const gone = new Set(body.remove || []);
  m.selected = [...m.selected.filter((x) => !gone.has(x)), ...(body.add || []).filter((x) => !m.selected.includes(x) && !gone.has(x))];
  const low = new Set((body.removeCustom || []).map((n) => n.toLowerCase()));
  m.custom = [...m.custom.filter((n) => !low.has(n.toLowerCase())), ...(body.addCustom || []).filter((n) => !m.custom.some((c) => c.toLowerCase() === n.toLowerCase()))];
  if (body.migrated && !quests.migrated.includes(body.mode)) quests.migrated.push(body.mode);
  const ev = { type: "quests", mode: body.mode, selected: [...m.selected], custom: [...m.custom] };
  setTimeout(() => w.__es?.onmessage({ data: JSON.stringify(ev) }), 5);
  return ev;
}
const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 50"><g id="Ground_Level"><rect width="100" height="50"/></g><g id="First_Floor"/><g id="Second_Floor"/></svg>`;

const dom = new JSDOM(html, {
  runScripts: "dangerously", pretendToBeVisual: true, url: "http://localhost:3000/",
  beforeParse(w) {
    w.localStorage.setItem("tqm.selected.regular", JSON.stringify(["extraZone"])); // ticks kept by an earlier version
    w.fetch = async (url, opts) => {
      const u = String(url).replace("?force=1", "");
      const reply = (obj) => ({ ok: true, status: 200, json: async () => JSON.parse(JSON.stringify(obj)) });
      if (u === "/api/quests") return reply(opts?.method === "POST" ? questPost(w, JSON.parse(opts.body)) : quests);
      if (u === "/api/past-logs") {
        const changes = { regular: { started: ["woodsTask", "doneTask"], ended: ["nades"] } };
        if (JSON.parse(opts.body).apply) { pastLogsApplied++; questPost(w, { mode: "regular", add: changes.regular.started, remove: changes.regular.ended }); }
        return reply({ changes, messages: 3, applied: JSON.parse(opts.body).apply });
      }
      if (u.endsWith(".svg")) return { ok: true, status: 200, text: async () => svg };
      if (!(u in routes)) { console.log("UNROUTED", u); return { ok: false, status: 404, statusText: "nf", json: async () => ({}) }; }
      return { ok: true, status: 200, json: async () => JSON.parse(JSON.stringify(routes[u])) };
    };
    w.EventSource = function () { w.__es = this; };
    w.HTMLDialogElement.prototype.showModal = function () { this.open = true; };
    w.SVGElement.prototype.getBBox = () => ({ x: 0, y: 0, width: 0, height: 0 });
    w.SVGSVGElement.prototype.createSVGRect = () => ({}); // Leaflet needs this to draw zone outlines as SVG
  },
});
const w = dom.window, d = w.document;
const errors = [];
w.addEventListener("error", (e) => errors.push(e.message));
w.console.warn = (...a) => errors.push("warn " + a.join(" "));
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const text = (sel) => [...d.querySelectorAll(sel)].map((e) => e.textContent.replace(/\s+/g, " ").trim());
const assert = (c, m) => { console.log((c ? "PASS " : "FAIL ") + m); if (!c) process.exitCode = 1; };

(async () => {
  await sleep(800);
  console.log("status:", d.getElementById("status").textContent);
  assert(d.getElementById("mapSelect").value === "customs", "starts on customs");
  const avail = text("#otherList .task-name");
  console.log("possible on customs:", avail);
  assert(avail.some((x) => x.startsWith("Debut")), "Debut available");
  assert(!avail.some((x) => x.startsWith("Checking")), "Checking locked (needs Debut complete)");
  assert(!avail.some((x) => x.startsWith("Endgame")), "level gate");
  assert(!avail.some((x) => x.startsWith("Jaeger Job")), "trader unlock gate");
  assert(!avail.some((x) => x.startsWith("Old News")), "completed task hidden");
  assert(!avail.some((x) => x.startsWith("Woods Walk")), "other-map task not listed on customs");
  // the ticks of an earlier version move from browser storage to the helper, one time
  assert(quests.migrated.includes("regular") && quests.modes.regular.selected.includes("extraZone"), "old ticks moved to the helper");
  assert(text("#taskList .task-name").some((x) => x.startsWith("Extra Zone")), "moved tick shows as ticked");
  assert(d.querySelectorAll(".leaflet-marker-pane .q-icon").length === 1 && d.querySelectorAll(".leaflet-marker-pane .q-item").length === 0, "only the moved tick has a marker before ticking");
  const ex = text(".ex-icon span");
  console.log("extracts:", ex);
  assert(ex.length === 3 && ex.includes("Crossroads") && ex.includes("Boat") && !ex.some((x) => x.includes("scav")), "PMC + shared extracts only");

  // tick Debut
  const debutBox = [...d.querySelectorAll("#otherList .task")].find((x) => x.textContent.includes("Debut")).querySelector("input");
  debutBox.checked = true; debutBox.dispatchEvent(new w.Event("change"));
  await sleep(50);
  assert(text("#taskList .task-name").some((x) => x.startsWith("Debut")), "Debut moved to ticked list");
  assert(quests.modes.regular.selected.includes("debut"), "tick saved by the helper");
  console.log("left objs:", text("#taskList .obj"));
  console.log("mission list:", text("#questList .qname"), text("#questList .step"));
  assert(text("#questList .step").some((x) => x.includes("Kill 5 Scavs") && x.includes("3/5")), "mission list shows steps with counts");
  assert(!text("#questList .step").some((x) => x.includes("Hand over 2 bolts")), "completed objective left out of the mission list");

  // add a task by name that the computed list says is locked (Checking) -> markers appear
  d.getElementById("addTask").value = "Checking (Prapor)";
  d.getElementById("addTaskBtn").click();
  await sleep(50);
  const qm = d.querySelectorAll(".leaflet-marker-pane .q-icon").length, qi = d.querySelectorAll(".leaflet-marker-pane .q-item").length;
  console.log("markers zone/item:", qm, qi);
  assert(qm === 2 && qi === 2, "manually added task shows its zone + 2 item locations");
  assert(text("#questList .qname").includes("Checking"), "added task is in the mission list");
  // add woods task -> not in the mission list for customs, listed under "My other quests"
  d.getElementById("addTask").value = "Woods Walk";
  d.getElementById("addTaskBtn").click();
  await sleep(50);
  assert(!text("#questList .qname").includes("Woods Walk"), "other-map quest is not in the mission list");
  assert(text("#elseList .ename").includes("Woods Walk"), "other-map quest listed under My other quests");

  // a name that tarkov.dev does not know becomes a text-only quest
  d.getElementById("addTask").value = "Brand New Quest";
  d.getElementById("addTaskBtn").click();
  await sleep(50);
  assert(text("#questList .qname").includes("Brand New Quest"), "unknown quest added as text only");
  [...d.querySelectorAll("#elseList .row")].find((x) => x.textContent.includes("Brand New Quest")).querySelector("button").click();
  await sleep(50);
  assert(!text("#questList .qname").includes("Brand New Quest"), "text-only quest removed");

  // any-location quests: only those with an open in-raid step are in the mission list
  for (const n of ["Nade Kills", "Gun Build", "Arena Match"]) { d.getElementById("addTask").value = n; d.getElementById("addTaskBtn").click(); }
  await sleep(50);
  assert(text("#questList .qname").includes("Nade Kills"), "any-location quest with a raid step is in the mission list");
  assert(!text("#questList .qname").includes("Gun Build") && !text("#questList .qname").includes("Arena Match"), "out-of-raid quests are not in the mission list");
  assert(["Nade Kills", "Gun Build", "Arena Match"].every((n) => text("#elseList .ename").includes(n)), "they stay under My other quests");

  // the view button cycles setup -> mission across -> mission down -> setup
  const app = d.getElementById("app"), vb = d.getElementById("viewBtn");
  assert(app.dataset.view === "setup", "starts in the setup view");
  vb.click(); assert(app.classList.contains("view-mission-h"), "second view: mission list across the top");
  vb.click(); assert(app.classList.contains("view-mission-v"), "third view: mission list down the side");
  vb.click(); assert(app.dataset.view === "setup" && !app.classList.contains("view-mission-v"), "back to the setup view");

  // show-all mode draws markers for everything possible
  d.querySelector('input[name="showMode"][value="all"]').click();
  await sleep(50);
  assert(d.querySelector('input[name="showMode"][value="all"]').checked, "show-all mode on");
  assert(d.querySelectorAll(".leaflet-marker-pane .q-icon").length === 2, "show-all mode keeps the ticked markers");
  d.querySelector('input[name="showMode"][value="selected"]').click();
  await sleep(50);
  assert(d.querySelectorAll(".leaflet-marker-pane .q-icon").length === 2, "ticked-only mode shows the two ticked zones");

  // untick Debut
  const tb = [...d.querySelectorAll("#taskList .task")].find((x) => x.textContent.includes("Debut")).querySelector("input");
  tb.checked = false; tb.dispatchEvent(new w.Event("change"));
  await sleep(50);
  assert(!text("#questList .qname").includes("Debut"), "untick removes from the mission list");

  // screenshot position event
  w.__es.onmessage({ data: JSON.stringify({ type: "position", x: 120, y: 1, z: -60, rotation: 45, filename: "shot.png" }) });
  await sleep(50);
  assert(d.querySelectorAll(".leaflet-marker-pane .player").length === 1, "player marker drawn");
  console.log("player transform:", d.querySelector(".player").style.transform);

  // switch map to woods: player stays on customs, woods task markers shown
  d.getElementById("mapSelect").value = "woods";
  d.getElementById("mapSelect").dispatchEvent(new w.Event("change"));
  await sleep(300);
  assert(d.querySelectorAll(".leaflet-marker-pane .player").length === 0, "player marker not on other map");
  assert(d.querySelectorAll(".leaflet-marker-pane .q-icon").length === 1, "woods quest marker shown");
  assert(text("#questList .qname").includes("Woods Walk"), "mission list follows the selected map");

  // floor select on customs
  d.getElementById("mapSelect").value = "customs";
  d.getElementById("mapSelect").dispatchEvent(new w.Event("change"));
  await sleep(300);
  console.log("floors:", text("#floorSelect option"), "styles:", text("#styleSelect option"));

  // quest messages from the game logs arrive as "quests" events with a note
  const send = (ev) => w.__es.onmessage({ data: JSON.stringify(ev) });
  const list = () => quests.modes.regular;
  send(questPost(w, { mode: "regular", add: ["needsActive"] }));
  send({ type: "quests", mode: "regular", selected: list().selected, custom: list().custom, note: { status: "started", id: "needsActive" } });
  await sleep(50);
  assert(text("#questList .qname").includes("Follow Up"), "quest started in the game is ticked");
  assert(d.getElementById("status").textContent.includes("Quest started in the game: Follow Up"), "status names the started quest");
  questPost(w, { mode: "regular", remove: ["needsActive"] });
  await sleep(50);
  assert(!text("#questList .qname").includes("Follow Up"), "quest finished in the game is unticked");
  send({ type: "quests", mode: "pve", selected: ["highLevel"], custom: [] });
  await sleep(20);
  assert(!text("#taskList .task-name").some((x) => x.startsWith("Endgame")), "the list of a different game mode is ignored");

  // Read past logs: asks first, leaves out quests that TarkovTracker shows as completed
  let asked = "";
  w.confirm = (m) => { asked = m; return false; };
  d.getElementById("pastLogsBtn").click();
  await sleep(50);
  assert(asked.includes("tick 0, untick 1") && asked.includes("Nade Kills") && !asked.includes("Old News"), "past logs: proposal lists only real changes");
  assert(pastLogsApplied === 0 && list().selected.includes("nades"), "past logs: nothing changes without a yes");
  w.confirm = () => true;
  d.getElementById("pastLogsBtn").click();
  await sleep(80);
  assert(pastLogsApplied === 1 && !text("#elseList .ename").includes("Nade Kills"), "past logs: applied after a yes");
  assert(!list().selected.includes("doneTask"), "a completed quest from the old logs is removed again");

  // raid events from the game logs: map, view and timer
  const raid = (o) => send({ type: "game", mode: "regular", session: "s", raid: { phase: "idle", scenePath: null, location: null, online: null, raidId: null, since: 0, started: null, ...o } });
  const timer = d.getElementById("raidTimer");
  raid({ phase: "loading", scenePath: "maps/woods_preset.bundle" });
  await sleep(300);
  assert(d.getElementById("mapSelect").value === "woods", "raid loading selects the raid map");
  assert(app.dataset.view === "mission-v", "raid loading shows the last mission view");
  assert(timer.classList.contains("on") && timer.textContent === "Loading Woods…", "timer shows the loading map");
  raid({ phase: "raid", scenePath: "maps/woods_preset.bundle", location: "Woods", started: Date.now() / 1000 - 600 });
  await sleep(50);
  assert(/^Woods · 10:0\d · (25:00|24:5\d) left$/.test(timer.textContent), "timer shows raid time and time left: " + timer.textContent);
  d.getElementById("mapSelect").value = "customs";
  d.getElementById("mapSelect").dispatchEvent(new w.Event("change"));
  await sleep(300);
  raid({ phase: "raid", scenePath: "maps/woods_preset.bundle", location: "Woods", raidId: "ABC123", started: Date.now() / 1000 - 600 });
  await sleep(50);
  assert(d.getElementById("mapSelect").value === "customs", "a map you select during the raid stays");
  raid({});
  await sleep(50);
  assert(app.dataset.view === "setup" && !timer.classList.contains("on"), "raid end goes back to setup and hides the timer");
  send({ type: "game", mode: "pve", session: "s", raid: { phase: "idle" } });
  await sleep(20);
  assert(d.getElementById("status").textContent.includes("pve mode"), "warns when the game mode differs from the token");

  // completing Checking in TarkovTracker drops it automatically
  routes["/api/progress"].data.tasksProgress.push({ id: "checking", complete: true });
  d.getElementById("refreshBtn").click();
  await sleep(100);
  assert(!text("#questList .qname").includes("Checking"), "completed ticked task drops off");
  console.log("ticked on the helper:", JSON.stringify(quests.modes.regular));
  console.log("errors:", errors);
  assert(!errors.filter((e) => !e.startsWith("warn")).length, "no page errors");
  process.exit();
})();
