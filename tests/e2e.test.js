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
  checking: task("checking", { neededKeys: [{ map: CUST, keys: ["k206"] }], taskRequirements: [{ task: "debut", status: ["complete"] }], objectives: [{ id: "o3", description: "o3", type: "visit", requiredKeys: [["k206", "k207"]], zones: [{ id: "z", map: CUST, position: { x: 100, y: 1, z: -50 }, outline: [{ x: 95, y: 1, z: -55 }, { x: 105, y: 1, z: -55 }, { x: 105, y: 1, z: -45 }] }], maps: [CUST] }, { id: "o3b", description: "o3b", type: "findQuestItem", possibleLocations: [{ map: CUST, positions: [{ x: 10, y: 2, z: 20 }, { x: 11, y: 2, z: 21 }] }], maps: [CUST] }] }),
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
    { id: "e1", name: "ex_pmc_a", faction: "pmc", position: { x: 300, y: 0, z: -100 }, outline: [{ x: 1, y: 0, z: 1 }, { x: 2, y: 0, z: 2 }, { x: 3, y: 0, z: 1 }], switches: [], transferItem: { item: "rub", count: 20000 } },
    { id: "e2", name: "ex_scav_b", faction: "scav", position: { x: 0, y: 0, z: 0 }, switches: [] },
    { id: "e3", name: "ex_shared_c", faction: "shared", position: { x: -200, y: 0, z: 50 }, switches: ["s"] },
    { id: "e4", name: "ex_null_d", faction: null, position: { x: -100, y: 0, z: 60 }, switches: [] }] },
  [WOODS]: { id: WOODS, name: `${WOODS} Name`, normalizedName: "woods", nameId: "Woods", scenePath: "maps/woods_preset.bundle", raidDuration: 35, extracts: [] },
};
const mapsEn = { [`${CUST} Name`]: "Customs", [`${WOODS} Name`]: "Woods", ex_pmc_a: "Crossroads", ex_shared_c: "Boat", ex_null_d: "Coop thing" };
const progress = { data: { tasksProgress: [{ id: "doneTask", complete: true }], taskObjectivesProgress: [{ id: "o1", complete: false, count: 3 }, { id: "o2", complete: true }], tradersProgress: [{ id: PRAPOR, level: 2, reputation: 0.2 }], displayName: "Tester", playerLevel: 12, pmcFaction: "USEC" }, meta: {} };

const routes = {
  "/maps.json": mapsCfg,
  "/api/config": { hasToken: true, tokenHint: "PVP_…abcd", gameMode: "regular", screenshotsDir: "C:/s", screenshotsDirExists: true, deleteScreenshots: false, logsDir: "", logsDirActive: "C:/g/Logs", logsDirExists: true, autoTick: true, tokens: { regular: "PVP_…abcd" }, writeTT: false, canWrite: null },
  "/api/writes": { type: "writes", pending: 0, error: null },
  "/api/status": { logLines: 4812, logSeen: Date.now() / 1000 - 30, logFiles: 3, session: "log_2026.11.15_6-56-39", logsFound: true, shotsFound: true, shotTime: null,
    trackerTime: Date.now() / 1000 - 5, trackerOk: true, trackerError: null, now: Date.now() / 1000, mode: "regular", hasToken: true, writeTT: true, canWrite: true,
    writes: { type: "writes", pending: 2, error: null, remaining: "93" }, game: { mode: "regular", raid: { phase: "idle" } }, logsDir: "C:/g/Logs",
    activity: [{ time: 1, kind: "raid", text: "loading Woods", err: false, raid: { phase: "loading", scenePath: "maps/woods_preset.bundle" } },
               { time: 2, kind: "task", text: "finished in the game", err: false, taskId: "debut", status: "finished" },
               { time: 3, kind: "tracker", text: "TarkovTracker not reachable", err: true }] },
  "/api/state": { position: null, game: null },
  "/api/progress": progress,
  "https://json.tarkov.dev/regular/tasks": { data: { tasks } },
  "https://json.tarkov.dev/regular/tasks_en": { data: en },
  "https://json.tarkov.dev/regular/maps": { data: { maps: apiMaps } },
  "https://json.tarkov.dev/regular/maps_en": { data: mapsEn },
  "https://json.tarkov.dev/regular/traders": { data: { [PRAPOR]: { id: PRAPOR, name: "p", normalizedName: "prapor" }, [JAEGER]: { id: JAEGER, name: "j", normalizedName: "jaeger" } } },
  "https://json.tarkov.dev/regular/items_en": { data: { "k206 Name": "Dorm room 206 key", "k207 Name": "Spare key", "rub Name": "Roubles" } },
  "https://json.tarkov.dev/regular/traders_en": { data: { p: "Prapor", j: "Jaeger" } },
};
// a small copy of the helper's quest list (state.json): it applies the changes and sends the "quests" event
const quests = { modes: {}, migrated: [] };
let pastLogsApplied = 0;
const progressPosts = [];
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
      if (u.startsWith("/api/progress/")) { progressPosts.push([u, JSON.parse(opts.body)]); return reply({ type: "writes", pending: 1, error: null }); }
      if (u === "/api/config" && opts?.method === "POST") { Object.assign(routes["/api/config"], JSON.parse(opts.body), { canWrite: true }); return reply(routes["/api/config"]); }
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
// Tasks view helpers: select an entry on the left, read the task rows on the right
const pick = (name) => [...d.querySelectorAll("#traderList .tbtn")].find((b) => b.firstChild.textContent === name).click();
const rows = (cls = "") => [...d.querySelectorAll("#taskLines .trow" + cls)].map((r) => r.querySelector(".tname").textContent);
const rowOf = (name) => [...d.querySelectorAll("#taskLines .trow")].find((r) => r.querySelector(".tname").textContent === name);
const assert = (c, m) => { console.log((c ? "PASS " : "FAIL ") + m); if (!c) process.exitCode = 1; };

(async () => {
  await sleep(800);
  console.log("status:", d.getElementById("status").textContent);
  assert(d.getElementById("mapSelect").value === "customs", "starts on customs");
  assert(d.getElementById("app").dataset.tab === "tasks" && d.getElementById("tabTasks").classList.contains("on"), "starts on the Tasks tab");
  assert(text("#traderList .tbtn span:first-child").join() === "My tasks,All traders,Jaeger,Prapor", "left list: My tasks, All traders, then the traders");
  pick("Prapor");
  console.log("Prapor lines:", rows());
  assert(rows(".st-available").includes("Debut"), "Debut available");
  assert(rows(".st-locked").includes("Checking"), "Checking locked (needs Debut complete)");
  assert(rowOf("Checking").textContent.includes("after: Debut"), "a locked task names the task it waits for");
  assert(rows(".st-locked").includes("Endgame"), "level gate");
  assert(!rows().includes("Old News"), "completed task hidden");
  const line = rows();
  assert(line.indexOf("Checking") === line.indexOf("Debut") + 1 && line.indexOf("Follow Up") === line.indexOf("Checking") + 1, "a task line shows the tasks in the order you get them");
  assert(rowOf("Debut").style.marginLeft === rowOf("Follow Up").style.marginLeft, "a line with no split stays in one column");
  d.getElementById("hideDone").click();
  assert(rows(".st-done").includes("Old News"), "completed tasks show when Hide completed is off");
  d.getElementById("hideDone").click();
  pick("Jaeger");
  assert(rows(".st-locked").includes("Jaeger Job"), "trader unlock gate");
  d.getElementById("taskSearch").value = "walk";
  d.getElementById("taskSearch").dispatchEvent(new w.Event("input"));
  assert(rows().join() === "Woods Walk", "search finds tasks of all traders");
  d.getElementById("taskSearch").value = "";
  d.getElementById("taskSearch").dispatchEvent(new w.Event("input"));
  // the ticks of an earlier version move from browser storage to the helper, one time
  assert(quests.migrated.includes("regular") && quests.modes.regular.selected.includes("extraZone"), "old ticks moved to the helper");
  pick("My tasks");
  assert(rows(".st-active").join() === "Extra Zone", "moved tick shows under My tasks");
  assert(d.querySelectorAll(".leaflet-marker-pane .q-icon").length === 1 && d.querySelectorAll(".leaflet-marker-pane .q-item").length === 0, "only the moved tick has a marker before ticking");
  const ex = text(".ex-icon span");
  console.log("extracts:", ex);
  assert(ex.length === 3 && ex.includes("Crossroads") && ex.includes("Boat") && !ex.some((x) => x.includes("scav")), "PMC + shared extracts only");
  // extracts with a special requirement are dimmed and say what they need
  const exIcon = (name) => [...d.querySelectorAll(".ex-icon")].find((x) => x.textContent === name);
  assert(exIcon("Crossroads").classList.contains("ex-need") && exIcon("Coop thing").classList.contains("ex-need") && !exIcon("Boat").classList.contains("ex-need"), "extracts that need an item or a partner are dimmed");
  assert(w.eval('extractNeeds({ name: "ex_pmc_a", transferItem: { item: "rub", count: 20000 } }, "Crossroads").join()') === "20,000 Roubles", "an extract shows the payment");
  assert(w.eval('extractNeeds({ name: "Alpinist" }, "Cliff Descent").join()') === "Red Rebel ice pick,Paracord,no body armor", "a climb extract shows the Red Rebel rule");
  assert(w.eval('extractNeeds({ name: "EXFIL_vent" }, "Sewer Manhole").join()') === "no backpack" && w.eval('extractNeeds({ name: "x" }, "Old Road").length') === 0, "no backpack rule; no note for a usual extract");
  // keys that a task needs
  assert(w.eval('keyText([["k206", "k207"]])') === "Dorm room 206 key or Spare key" && w.eval('keyText([{ map: "m", keys: ["k206"] }])') === "Dorm room 206 key", "key names for a step and for a task");
  pick("Prapor");
  assert([...d.querySelectorAll(".trow")].find((r) => r.querySelector(".tname").textContent === "Checking").querySelector(".tmeta").textContent.includes("🔑 Dorm room 206 key"), "the task line shows the key that the task needs");
  pick("My tasks");

  // tick Debut in the Prapor line
  pick("Prapor");
  const debutBox = rowOf("Debut").querySelector("input[type=checkbox]");
  debutBox.checked = true; debutBox.dispatchEvent(new w.Event("change"));
  await sleep(50);
  assert(rowOf("Debut").classList.contains("st-active"), "ticked task shows as in progress");
  assert(text("#traderList .tbtn").some((x) => x.startsWith("Prapor") && x.includes("2 ·")), "the trader entry counts the tasks in progress");
  assert(quests.modes.regular.selected.includes("debut"), "tick saved by the helper");
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
  pick("My tasks");
  assert(rows().includes("Woods Walk"), "other-map quest is under My tasks");

  // a name that tarkov.dev does not know becomes a text-only quest
  d.getElementById("addTask").value = "Brand New Quest";
  d.getElementById("addTaskBtn").click();
  await sleep(50);
  assert(text("#questList .qname").includes("Brand New Quest"), "unknown quest added as text only");
  rowOf("Brand New Quest").querySelector("button").click();
  await sleep(50);
  assert(!text("#questList .qname").includes("Brand New Quest"), "text-only quest removed");

  // any-location quests: only those with an open in-raid step are in the mission list
  for (const n of ["Nade Kills", "Gun Build", "Arena Match"]) { d.getElementById("addTask").value = n; d.getElementById("addTaskBtn").click(); }
  await sleep(50);
  assert(text("#questList .qname").includes("Nade Kills"), "any-location quest with a raid step is in the mission list");
  assert(!text("#questList .qname").includes("Gun Build") && !text("#questList .qname").includes("Arena Match"), "out-of-raid quests are not in the mission list");
  assert(["Nade Kills", "Gun Build", "Arena Match"].every((n) => rows().includes(n)), "all of them are under My tasks");

  // the view button cycles setup -> mission across -> mission down -> setup
  const app = d.getElementById("app"), vb = d.getElementById("viewBtn");
  // top bar: the map controls are one group, the timer and the status line are a second group
  assert(d.querySelector("#maptools #mapSelect") && d.querySelector("#maptools #layersBtn") && d.querySelector("#maptools #viewBtn"), "the map controls are one group in the top bar");
  assert(d.querySelector("#info #raidTimer") && d.querySelector("#info #status") && d.querySelector("#brand #tabs"), "the timer and the status line are a group at the right");
  assert(!d.getElementById("status").textContent.includes("tasks available"), "the status line does not count the available tasks");
  // two tabs; on the Map tab the view button moves the mission list
  d.getElementById("tabMap").click();
  assert(app.classList.contains("tab-map") && !app.classList.contains("tab-tasks") && d.getElementById("tabMap").classList.contains("on"), "the Map tab shows the map");
  assert(app.classList.contains("view-mission-h") && vb.textContent === "List ↔", "mission list across the top");
  vb.click(); assert(app.classList.contains("view-mission-v") && !app.classList.contains("view-mission-h"), "mission list down the side");
  vb.click(); assert(app.classList.contains("view-mission-off") && !app.classList.contains("view-mission-v") && vb.textContent === "List ✕", "third choice: no mission list");
  assert(w.getComputedStyle(d.getElementById("mission")).display === "none", "the hidden list takes no room on the map");
  vb.click(); assert(app.classList.contains("view-mission-h"), "and across the top again");
  vb.click();
  d.getElementById("tabTasks").click();
  assert(app.dataset.tab === "tasks" && app.dataset.view === "mission-v", "the Tasks tab keeps the place of the mission list");
  const css = d.querySelector("style").textContent;
  assert(/#mission \{ grid-column:1;/.test(css) && /#map \{ grid-column:1;/.test(css), "the mission list lies over the map, in the same grid cell");

  // show-all mode draws markers for everything possible
  d.getElementById("showAll").click();
  await sleep(50);
  assert(d.getElementById("showAll").checked, "show-all mode on");
  assert(d.querySelectorAll(".leaflet-marker-pane .q-icon").length === 2, "show-all mode keeps the ticked markers");
  d.getElementById("showAll").click();
  await sleep(50);
  assert(d.querySelectorAll(".leaflet-marker-pane .q-icon").length === 2, "ticked-only mode shows the two ticked zones");

  // Status tab: counters, connections and the activity lines
  d.getElementById("tabStatus").click();
  await sleep(50);
  assert(d.getElementById("app").classList.contains("tab-status") && d.getElementById("tabStatus").classList.contains("on"), "Status is a tab");
  assert(text("#statCards .v").join("|") === "PvP|4,812|2|93", "status cards: mode, log lines, changes waiting, writes left");
  const conn = (name) => [...d.querySelectorAll("#connRows .conn")].find((c) => c.querySelector(".name").textContent === name);
  assert(conn("TarkovTracker").classList.contains("good") && conn("TarkovTracker").textContent.includes("read and write"), "TarkovTracker row shows the token rights");
  assert(conn("Game data").textContent.includes("tasks") && conn("Game logs").textContent.includes("3 files"), "game data and game logs rows");
  assert(conn("Screenshots").classList.contains("wait") && conn("Game").querySelector(".pill").textContent === "Running", "screenshots wait for a position; the game runs");
  const act = text("#activity div");
  assert(act[0].endsWith("raid loading Woods") && act[1].endsWith("task finished: Debut"), "activity lines name the map and the task");
  assert(d.querySelector("#activity div.err").textContent.includes("not reachable"), "a fault line is marked");
  w.__es.onmessage({ data: JSON.stringify({ type: "activity", time: 4, kind: "position", text: "280.9, -274.3 from a screenshot", err: false }) });
  assert(text("#activity div").length === 4, "a new activity line shows at once");
  routes["/api/status"].trackerOk = false; routes["/api/status"].trackerError = "not reachable: timed out";
  await w.eval("loadStatus()");
  assert(conn("TarkovTracker").classList.contains("fail") && conn("TarkovTracker").querySelector(".pill").textContent === "Not reachable", "a failed read shows as not reachable");
  d.getElementById("tabTasks").click();

  // filters and sort order on the Tasks tab
  const set = (id, value) => { const el = d.getElementById(id); if (el.type === "checkbox") el.checked = value; else el.value = value; el.dispatchEvent(new w.Event("change")); };
  const groups = () => text("#taskLines .tgroup");
  pick("All traders");
  assert(groups().join() === "Jaeger,Prapor" && rows().includes("Jaeger Job") && rows().includes("Debut"), "All traders: the lines of each trader under its name");
  set("onlyActive", true);
  assert(rows().length > 0 && rows().length === rows(".st-active").length && !rows().includes("Endgame"), "Only accepted shows only the tasks in progress");
  set("onlyActive", false);
  set("mapFilter", "woods");
  assert(rows().join() === "Meet Jaeger,Woods Walk", "the map filter shows only the tasks of that map");
  set("mapFilter", "none");
  assert(rows().includes("Nade Kills") && !rows().includes("Debut"), "Any location shows the tasks with no map");
  set("mapFilter", "");
  set("taskSort", "status");
  assert(groups().join() === "In progress,Available,Locked", "sort by status: a heading for each status, in progress first");
  const order = rows();
  assert(order.indexOf("Debut") < order.indexOf("Meet Jaeger") && order.indexOf("Meet Jaeger") < order.indexOf("Endgame"), "sort by status: in progress, then available, then locked");
  set("taskSort", "map");
  assert(groups().join() === "Customs,Woods,Any location", "sort by map: a heading for each map, tasks with no map last");
  set("taskSort", "name");
  assert(rows().join() === [...rows()].sort((a, b) => a.localeCompare(b)).join() && groups().length === 0, "sort by name");
  set("taskSort", "lines");
  pick("My tasks");

  // progress controls are only on the Tasks tab; with sending off, a click changes nothing and says why
  assert(d.querySelectorAll("#questList .pbtn, #questList input").length === 0, "the mission list on the map has no progress controls");
  pick("My tasks");
  const step = () => [...rowOf("Debut").querySelectorAll(".tobj")].find((x) => x.textContent.includes("Kill 5 Scavs"));
  const sbtn = (label) => [...step().querySelectorAll(".pbtn")].find((b) => b.textContent === label);
  sbtn("✓").click();
  assert(progressPosts.length === 0 && d.getElementById("status").textContent.includes("Send task progress to TarkovTracker"), "with sending off, a click explains the setting");
  assert(text("#questList .step").some((x) => x.includes("Kill 5 Scavs") && x.includes("3/5")), "and the count stays");
  d.getElementById("tabSettings").click();
  assert(d.getElementById("app").classList.contains("tab-settings") && d.getElementById("tabSettings").classList.contains("on"), "Settings is a tab");
  d.getElementById("writeTT").checked = true;
  d.getElementById("settingsForm").dispatchEvent(new w.Event("submit", { cancelable: true }));
  await sleep(100);
  assert(d.getElementById("savedNote").textContent === "Saved." && routes["/api/config"].writeTT === true, "Save on the Settings tab saves");
  d.getElementById("tabTasks").click();
  sbtn("✓").click();
  await sleep(30);
  assert(text("#questList .step").every((x) => !x.includes("Kill 5 Scavs")), "a done step leaves the mission list");
  assert(JSON.stringify(progressPosts) === JSON.stringify([["/api/progress/objective", { id: "o1", state: "completed", count: 5 }]]), "the click goes to the helper");
  // undo the done step, then type a count
  const undo = [...step().querySelectorAll(".pbtn")].find((b) => b.textContent === "↺");
  assert(undo && step().classList.contains("done"), "a done step in the Tasks view has an undo button");
  undo.click();
  await sleep(30);
  assert(progressPosts.at(-1)[1].state === "uncompleted" && text("#questList .step").some((x) => x.includes("Kill 5 Scavs")), "undo puts the step back");
  const box = step().querySelector("input.cnt");
  assert(box && box.max === "5", "a counted step has a box for the count");
  box.value = "3"; box.dispatchEvent(new w.Event("change"));
  await sleep(30);
  assert(JSON.stringify(progressPosts.at(-1)) === JSON.stringify(["/api/progress/objective", { id: "o1", count: 3, state: "uncompleted" }]), "a typed count goes to the helper as one change");
  assert(step().querySelector("input.cnt").value === "3" && text("#questList .step").some((x) => x.includes("3/5")), "the typed count shows in both views");
  w.confirm = () => true;
  [...rowOf("Debut").querySelectorAll(".thead .pbtn")].find((b) => b.textContent === "✓ task").click();
  assert(JSON.stringify(progressPosts.at(-1)) === JSON.stringify(["/api/progress/task", { id: "debut", state: "completed" }]), "✓ task marks the quest as completed");
  w.__es.onmessage({ data: JSON.stringify({ type: "writes", pending: 2, error: null }) });
  assert(d.getElementById("writesNote").textContent === "2 changes to send…" && d.getElementById("writesNote").classList.contains("on"), "waiting changes show in the top bar");
  w.__es.onmessage({ data: JSON.stringify({ type: "writes", pending: 2, error: "TarkovTracker daily write limit reached." }) });
  assert(d.getElementById("writesNote").classList.contains("err"), "a send fault shows as an error");
  w.__es.onmessage({ data: JSON.stringify({ type: "writes", pending: 0, error: null }) });

  // untick Debut
  const tb = rowOf("Debut").querySelector("input[type=checkbox]");
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
  assert(text("#questList .qname").includes("Follow Up"), "task started in the game is ticked");
  assert(d.getElementById("status").textContent.includes("Task started in the game: Follow Up"), "status names the started quest");
  questPost(w, { mode: "regular", remove: ["needsActive"] });
  await sleep(50);
  assert(!text("#questList .qname").includes("Follow Up"), "task finished in the game is unticked");
  send({ type: "quests", mode: "pve", selected: ["highLevel"], custom: [] });
  await sleep(20);
  assert(!rows().includes("Endgame"), "the list of a different game mode is ignored");

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
  assert(pastLogsApplied === 1 && !rows().includes("Nade Kills"), "past logs: applied after a yes");
  assert(!list().selected.includes("doneTask"), "a completed quest from the old logs is removed again");

  // raid events from the game logs: map, view and timer
  const raid = (o) => send({ type: "game", mode: "regular", session: "s", raid: { phase: "idle", scenePath: null, location: null, online: null, raidId: null, since: 0, started: null, side: null, ...o } });
  const timer = d.getElementById("raidTimer");
  d.getElementById("tabTasks").click();
  raid({ phase: "loading", scenePath: "maps/woods_preset.bundle" });
  await sleep(300);
  assert(d.getElementById("mapSelect").value === "woods", "raid loading selects the raid map");
  assert(app.dataset.tab === "map" && app.dataset.view === "mission-v", "raid loading opens the Map tab");
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
  // extracts follow the side of the raid
  const exNames = () => text(".ex-icon span");
  d.getElementById("mapSelect").value = "customs";
  d.getElementById("mapSelect").dispatchEvent(new w.Event("change"));
  await sleep(300);
  raid({ phase: "raid", scenePath: "maps/customs_preset.bundle", location: "bigmap", online: true, raidId: "SCAV01", side: "scav", started: Date.now() / 1000 - 60 });
  await sleep(50);
  assert(exNames().includes("ex_scav_b") && exNames().includes("Boat") && !exNames().includes("Crossroads"), "a Scav raid shows the Scav and shared extracts");
  assert(timer.textContent.startsWith("Customs · Scav · "), "the timer names the side");
  const mode = d.getElementById("extractMode");
  mode.value = "both"; mode.dispatchEvent(new w.Event("change"));
  assert(exNames().includes("ex_scav_b") && exNames().includes("Crossroads"), "PMC and Scav shows both");
  mode.value = "off"; mode.dispatchEvent(new w.Event("change"));
  assert(exNames().length === 0, "None shows no extracts");
  mode.value = "auto"; mode.dispatchEvent(new w.Event("change"));
  raid({});
  await sleep(50);
  assert(exNames().includes("Crossroads") && !exNames().includes("ex_scav_b"), "after the raid the PMC extracts are back");
  assert(d.querySelector("#layersPanel #extractMode") && d.querySelector("#layersPanel #showAll") && !d.querySelector("#settings #showQuests"), "the map options are in the Layers panel of the Map tab");
  d.getElementById("layersBtn").click();
  assert(d.getElementById("layersPanel").classList.contains("open") && d.getElementById("layersBtn").classList.contains("on"), "the Layers button opens the panel");
  d.getElementById("layersBtn").click();
  assert(!d.getElementById("layersPanel").classList.contains("open"), "and closes it");
  // mini view: a button and the M key; only the map and the icons stay
  const shown = (sel) => w.getComputedStyle(d.querySelector(sel)).display !== "none";
  const key = (k, target = d.body) => target.dispatchEvent(new w.KeyboardEvent("keydown", { key: k, bubbles: true }));
  const tabBefore = app.dataset.tab;
  d.getElementById("tabMap").click();
  d.getElementById("miniBtn").click();
  assert(app.classList.contains("mini") && !shown("header") && !shown("#mission") && !shown(".ex-icon span") && !shown(".map-label") && shown("#map") && shown(".ex-icon .box"), "mini view: no top bar, no list, no names; the map and the icons stay");
  assert(w.localStorage.getItem("tqm.mini") === "true" && shown("#miniExit"), "the mini view is kept and has a button to leave it");
  key("m"); assert(!app.classList.contains("mini") && shown("header"), "the M key leaves the mini view");
  key("m", d.getElementById("mapSelect")); assert(!app.classList.contains("mini"), "the M key does nothing in a list or a text box");
  key("M"); assert(app.classList.contains("mini"), "the M key opens the mini view");
  key("Escape"); assert(!app.classList.contains("mini"), "Esc leaves the mini view");
  key("M"); d.getElementById("tabTasks").click();
  assert(shown("header"), "the other tabs keep the top bar in the mini view");
  d.getElementById("tabMap").click(); key("Escape");
  if (tabBefore !== "map") d.getElementById("tab" + tabBefore[0].toUpperCase() + tabBefore.slice(1)).click();
  // landmark names: one option in the Layers panel
  const marks = () => d.querySelectorAll(".leaflet-marker-pane .map-label").length, lm = d.getElementById("showLandmarks");
  const allMarks = marks();
  assert(d.querySelector("#layersPanel #showLandmarks") && allMarks > 0, "landmark names show by default");
  lm.checked = false; lm.dispatchEvent(new w.Event("change"));
  assert(marks() === 0 && w.localStorage.getItem("tqm.showLandmarks") === "false", "the option hides the landmark names and is kept");
  lm.checked = true; lm.dispatchEvent(new w.Event("change"));
  assert(marks() === allMarks, "and shows them again");
  assert(text("#settings h2").join("|") === "TarkovTracker|Folders|Automatic actions|About, credits and licenses", "the Settings tab has a heading for each group");
  assert(app.dataset.tab === "tasks" && !timer.classList.contains("on"), "raid end goes back to the Tasks tab and hides the timer");
  send({ type: "game", mode: "pve", session: "s", raid: { phase: "idle" } });
  await sleep(20);
  assert(d.getElementById("status").textContent.includes("no TarkovTracker token"), "warns when the game mode has no token");

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
