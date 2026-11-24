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
  [CUST]: { id: CUST, name: `${CUST} Name`, normalizedName: "customs", nameId: "bigmap", scenePath: "maps/customs_preset.bundle", raidDuration: 35,
    locks: [{ id: "lk1", lockType: "door", key: "k208", position: { x: 20, y: 0, z: 20 } }, { id: "lk2", lockType: "trunk", key: "k209", position: { x: 40, y: 0, z: 20 } }, { id: "lk3", key: "k209" }],
    extracts: [
    { id: "e1", name: "ex_pmc_a", faction: "pmc", position: { x: 300, y: 0, z: -100 }, outline: [{ x: 1, y: 0, z: 1 }, { x: 2, y: 0, z: 2 }, { x: 3, y: 0, z: 1 }], switches: [], transferItem: { item: "rub", count: 20000 } },
    { id: "e2", name: "ex_scav_b", faction: "scav", position: { x: 0, y: 0, z: 0 }, switches: [] },
    { id: "e3", name: "ex_shared_c", faction: "shared", position: { x: -200, y: 0, z: 50 }, switches: ["s"] },
    { id: "e4", name: "EXFIL_Bunker", faction: null, position: { x: -100, y: 0, z: 60 }, switches: [] }],
    switches: [{ id: "sw1", name: "switch_autoId_00632_EXFIL_reserve_electric_switcher_lever", position: { x: -90, y: 0, z: 70 } }, { id: "sw2", name: "other_switch", position: { x: 0, y: 0, z: 9 } }],
    transits: [{ id: "9", description: "CUS_TRANSIT_9_DESC", map: WOODS, position: { x: 50, y: 0, z: 50 }, outline: [] },
      { id: "10", description: "CUS_TRANSIT_10_DESC", map: "unknownMap", conditions: "CUS_TRANSIT_10_COND", position: { x: 60, y: 0, z: 50 } }] },
  [WOODS]: { id: WOODS, name: `${WOODS} Name`, normalizedName: "woods", nameId: "Woods", scenePath: "maps/woods_preset.bundle", raidDuration: 35, extracts: [], locks: [{ id: "l1", key: "k206" }] },
};
const mapsEn = { [`${CUST} Name`]: "Customs", [`${WOODS} Name`]: "Woods", ex_pmc_a: "Crossroads", ex_shared_c: "Boat", EXFIL_Bunker: "Coop thing", "switch_autoId_00632_EXFIL_reserve_electric_switcher_lever": "Bunker Power Switch" };
const progress = { data: { tasksProgress: [{ id: "doneTask", complete: true }], taskObjectivesProgress: [{ id: "o1", complete: false, count: 3 }, { id: "o2", complete: true }], tradersProgress: [{ id: PRAPOR, level: 2, reputation: 0.2 }], displayName: "Tester", playerLevel: 12, pmcFaction: "USEC" }, meta: {} };

const W = "https://wiki.test/wiki/";
// ending routes for the "skies" chapter, in the form that story.routes() gives
const storyRoutes = { chapter: "skies", source: { title: "Endings chart", author: "Someone", version: "1.0", url: W + "Endings" }, sections: {
  start: { title: "The case", steps: [
    { kind: "note", text: "Decision: keep the case or not." },
    { ref: "f3", mark: "f3", text: "Route text for the last step" },
    { id: "r-keep", mark: "r-keep", text: "Keep the case", choice: "A" },
    { id: "r-give", mark: "r-give", text: "Give the case", choice: "B" },
    { id: "r-extra", mark: "r-extra", text: "Pay more", if: "You kept the case", when: "A" } ] },
  one: { title: "Route one", steps: [
    { id: "r-one", mark: "r-one", text: "Do route one", achievement: "Fast", mandatory: true },
    { id: "r-opt", mark: "r-opt", text: "Optional thing", optional: true } ] },
  two: { title: "Route two", steps: [{ id: "r-two", mark: "r-two", text: "Do route two" }] } },
  routes: [{ id: "one", name: "One", ending: "e1", sections: ["start", "one"] }, { id: "two", name: "Two", ending: "e2", sections: ["start", "two"] }] };
const storyDone = { regular: [] }, storyFailed = { regular: [] }, storyPosts = [];
const routes = {
  "/api/story?mode=regular": { mode: "regular", fetched: 1700000000, chapters: [
    { id: "tour", name: "Tour", order: 1, wiki: W + "Tour", autoStart: true, description: "The first chapter", activation: "", notes: "", rewards: "An achievement",
      requires: [], unlocks: [], exclusive: [], endings: [], steps: [
        { id: "s1", text: "Escape Ground Zero", optional: false, stage: "q1", parent: null, ending: null, tutorial: true, unlocks: [{ type: "trader", id: "t", name: "Therapist", note: null }], wiki: W + "Tour#Escape" },
        { id: "s2", text: "Hand over cash to Therapist", optional: false, stage: "q2", parent: null, ending: null, tutorial: false, unlocks: [], wiki: W + "Tour#Cash" },
        { id: "s3", text: "Collect the cash", optional: true, stage: "q2", parent: "s2", ending: null, tutorial: false, unlocks: [], wiki: W + "Tour#Cash" },
        { id: "s4", text: "Talk to Ragman", optional: false, stage: "q3", parent: null, ending: null, tutorial: false, unlocks: [], wiki: W + "Tour" },
      ] },
    { id: "skies", name: "Falling Skies", order: 2, wiki: W + "Falling_Skies", autoStart: false, description: "", activation: "Ask Mechanic", notes: "", rewards: "",
      requires: [{ id: "tour", name: "Tour" }], unlocks: [], exclusive: [["qa", "qb"]], endings: [], steps: [
        { id: "f1", text: "Path A step", optional: false, stage: "qa", parent: null, ending: null, tutorial: false, unlocks: [], wiki: W + "Falling_Skies#A" },
        { id: "f2", text: "Path B step", optional: false, stage: "qb", parent: null, ending: null, tutorial: false, unlocks: [], wiki: W + "Falling_Skies#B" },
        { id: "f3", text: "Last step", optional: false, stage: "qc", parent: null, ending: null, tutorial: false, unlocks: [], wiki: W + "Falling_Skies" },
      ] },
  ] },
  "/maps.json": mapsCfg,
  "/api/config": { hasToken: true, tokenHint: "PVP_…abcd", gameMode: "regular", screenshotsDir: "C:/s", screenshotsDirExists: true, deleteScreenshots: false, logsDir: "", logsDirActive: "C:/g/Logs", logsDirExists: true, autoTick: true, tokens: { regular: "PVP_…abcd" }, writeTT: false, canWrite: null },
  "/api/writes": { type: "writes", pending: 0, error: null },
  "/api/status": { logLines: 4812, logSeen: Date.now() / 1000 - 30, logFiles: 3, session: "log_2026.11.15_6-56-39", logsFound: true, shotsFound: true, shotTime: null,
    trackerTime: Date.now() / 1000 - 5, trackerOk: true, trackerError: null, now: Date.now() / 1000, mode: "regular", hasToken: true, writeTT: true, canWrite: true,
    writes: { type: "writes", pending: 2, error: null, remaining: "93" }, flea: { busy: false, maxAge: 28800, error: null, errorTime: null, fetched: Date.now() / 1000 - 600, items: 360, crafts: 214 },
    story: { busy: false, maxAge: 86400, error: null, errorTime: null, fetched: Date.now() / 1000 - 600, chapters: 10, steps: 437 }, game: { mode: "regular", raid: { phase: "idle" } }, logsDir: "C:/g/Logs",
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
  "https://json.tarkov.dev/regular/items_en": { data: { "k206 Name": "Dorm room 206 key", "k206 ShortName": "Dorm 206", "k207 Name": "Spare key", "k208 Name": "Customs office key", "k208 ShortName": "Office", "rub Name": "Roubles", "a1 Name": "Bolts", "t1 Name": "Toolset", "p1 Name": "Weapon parts", "p2 Name": "Gunpowder" } },
  "https://json.tarkov.dev/regular/traders_en": { data: { p: "Prapor", j: "Jaeger" } },
  "/api/crafts?mode=regular": { mode: "regular", fetched: 1700000000, crafts: [
    { id: "c1", station: "st1", level: 1, duration: 7200, gameEditions: [], requiredQuestItems: [],
      requiredItems: [{ item: "a1", count: 2, attributes: {} }, { item: "t1", count: 1, attributes: { tool: true } }], productItem: { item: "p1", count: 1, attributes: {} } },
    { id: "c2", station: "st1", level: 2, duration: 3600, gameEditions: [], requiredQuestItems: [],
      requiredItems: [{ item: "a1", count: 1, attributes: {} }], productItem: { item: "p2", count: 3, attributes: {} } },
    { id: "c3", station: "st2", level: 1, duration: 60, gameEditions: [], requiredQuestItems: [],
      requiredItems: [{ item: "zz", count: 1, attributes: {} }], productItem: { item: "p1", count: 1, attributes: {} } },
  ],
  stations: { st1: { id: "st1", name: "area_10", normalizedName: "workbench", levels: [] }, st2: { id: "st2", name: "area_7", normalizedName: "medstation", levels: [] }, st3: { id: "st3", name: "area_3", normalizedName: "stash", levels: [] } },
  stationsEn: { area_10: "Workbench", area_7: "Medstation" },
  flea: { sellOfferFeeRate: 0.05, sellRequirementFeeRate: 0.05 }, prices: {
    a1: { avg: 1000, low: 900, base: 500, noFlea: false, buy: { trader: PRAPOR, priceRUB: 800, minTraderLevel: 2 }, sell: null },
    t1: { avg: 50000, low: 0, base: 10000, noFlea: false, buy: null, sell: null },
    p1: { avg: 10000, low: 9000, base: 5000, noFlea: false, buy: null, sell: { trader: PRAPOR, priceRUB: 3000 }, icon: "p1.webp" },
    p2: { avg: 0, low: 0, base: 400, noFlea: true, buy: null, sell: { trader: JAEGER, priceRUB: 400 } },
  } },
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
      if (u === "/api/story" && opts?.method === "POST") {
        const b = JSON.parse(opts.body);
        storyPosts.push(b);
        const change = (list, add, remove) => [...list.filter((x) => !remove.includes(x)), ...add.filter((x) => !list.includes(x) && !remove.includes(x))];
        storyDone[b.mode] = change(storyDone[b.mode], b.done, [...b.undone, ...b.failed]);
        storyFailed[b.mode] = change(storyFailed[b.mode], b.failed, [...b.unfailed, ...b.done]);
        return reply({ type: "story", mode: b.mode, done: storyDone[b.mode], failed: storyFailed[b.mode] });
      }
      if (u === "/api/story?mode=regular") return reply({ ...routes[u], done: storyDone.regular, failed: storyFailed.regular, routes: storyRoutes });
      if (u.startsWith("/api/progress/")) { progressPosts.push([u, JSON.parse(opts.body)]); return reply({ type: "writes", pending: 1, error: null }); }
      if (u === "/api/config" && opts?.method === "POST") { Object.assign(routes["/api/config"], JSON.parse(opts.body), { canWrite: true }); return reply(routes["/api/config"]); }
      if (u === "/api/past-logs") {
        const changes = { regular: { started: ["woodsTask", "doneTask", ...logOnlyTasks], ended: ["nades"] } };
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
const logOnlyTasks = [];   // ids that the old game logs have and the task data does not
const pick = (name) => [...d.querySelectorAll("#traderList .tbtn")].find((b) => b.firstChild.textContent === name).click();
const rows = (cls = "") => [...d.querySelectorAll("#taskLines .trow" + cls)].map((r) => r.querySelector(".tname").textContent);
const rowOf = (name) => [...d.querySelectorAll("#taskLines .trow")].find((r) => r.querySelector(".tname").textContent === name);
const assert = (c, m) => { console.log((c ? "PASS " : "FAIL ") + m); if (!c) process.exitCode = 1; };

(async () => {
  await sleep(800);
  console.log("status:", d.getElementById("status").textContent);
  assert(d.getElementById("mapSelect").value === "customs", "starts on customs");
  assert(d.getElementById("app").dataset.tab === "tasks" && d.getElementById("tabTasks").classList.contains("on"), "starts on the Tasks tab");
  assert(text("#traderList .tbtn span:first-child").join() === "My tasks,All traders,Prapor,Jaeger", "left list: My tasks, All traders, then the traders in the order of the game");
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
  const ex = text(".ex-icon:not(.ex-transit):not(.ex-lever) span");
  assert(d.querySelectorAll(".ex-icon").length > 0 && [...d.querySelectorAll(".ex-icon:not(.ex-lever)")].every((x) => x.querySelector("svg.box path")), "extracts and transits are arrows");
  // the power lever of an extract shows with it; other switches do not show
  const levers = [...d.querySelectorAll(".ex-lever")];
  assert(levers.map((x) => x.textContent).join() === "⚡Bunker Power Switch", "the lever of an extract shows, with its name");
  assert(w.eval('extractNeeds({ name: "EXFIL_Bunker" }, "Bunker Hermetic Door").join()') === "power lever on", "the extract needs the lever");
  console.log("extracts:", ex);
  assert([...d.querySelectorAll(".ex-shared")].length > 0 && [...d.querySelectorAll(".ex-shared")].every((x) => x.classList.contains("ex-pmc")), "with no raid, a shared extract has the PMC color");
  assert(ex.length === 3 && ex.includes("Crossroads") && ex.includes("Boat") && !ex.some((x) => x.includes("scav")), "PMC + shared extracts only");
  // transits: the name from the game text, else from the map they go to; a condition dims them
  const trs = [...d.querySelectorAll(".ex-transit")];
  assert(trs.map((x) => x.textContent).join() === "Transit to Woods,Transit to another map", "transits show with their names");
  assert(trs[1].classList.contains("ex-need") && !trs[0].classList.contains("ex-need"), "a transit with a condition is dimmed");
  d.getElementById("showTransits").checked = false; d.getElementById("showTransits").dispatchEvent(new w.Event("change"));
  assert(d.querySelectorAll(".ex-transit").length === 0 && text(".ex-icon:not(.ex-lever) span").length === 3 && d.querySelectorAll(".ex-lever").length === 1, "the Layers option hides the transits only");
  d.getElementById("showTransits").checked = true; d.getElementById("showTransits").dispatchEvent(new w.Event("change"));
  // extracts with a special requirement are dimmed and say what they need
  const exIcon = (name) => [...d.querySelectorAll(".ex-icon")].find((x) => x.textContent === name);
  assert(exIcon("Crossroads").classList.contains("ex-need") && exIcon("Coop thing").classList.contains("ex-need") && !exIcon("Boat").classList.contains("ex-need"), "extracts that need an item or a partner are dimmed");
  assert(w.eval('extractNeeds({ name: "ex_pmc_a", transferItem: { item: "rub", count: 20000 } }, "Crossroads").join()') === "20,000 Roubles", "an extract shows the payment");
  assert(w.eval('extractNeeds({ name: "Alpinist" }, "Cliff Descent").join()') === "Red Rebel ice pick,Paracord,no body armor", "a climb extract shows the Red Rebel rule");
  assert(w.eval('extractNeeds({ name: "EXFIL_vent" }, "Sewer Manhole").join()') === "no backpack" && w.eval('extractNeeds({ name: "x" }, "Old Road").length') === 0, "no backpack rule; no note for a usual extract");
  // a fix for old tarkov.dev data applies only while tarkov.dev has the old text of the step
  const fixed = w.eval(`(() => {
    const keep = [S.tasksById, S.tasksEn], f = TASK_FIXES[0], run = (text) => {
      const obj = { id: f.step, description: "d", maps: ["old"] };
      S.tasksById = new Map([[f.task, { id: f.task, objectives: [obj] }]]); S.tasksEn = { d: text };
      applyTaskFixes(); return [S.tasksEn.d === f.text, obj.maps.join() === f.maps.join()];
    };
    const out = [run(f.was), run("New text from tarkov.dev")];
    [S.tasksById, S.tasksEn] = keep; return JSON.stringify(out);
  })()`);
  assert(fixed === "[[true,true],[false,false]]", "a task fix changes the old step, and stops when tarkov.dev has new text");
  // a step that places, marks with or uses a special-slot item has a blue diamond
  assert(w.eval('isToolStep({ type: "plantItem", items: [{ id: "5b4391a586f7745321235ab2" }] })') && w.eval('isToolStep({ type: "mark", markerItem: "5991b51486f77447b112d44f" })'), "camera and marker steps are tool steps");
  assert(!w.eval('isToolStep({ type: "plantItem", items: ["5448fee04bdc2dbc018b4567"] })') && !w.eval('isToolStep({ type: "findItem", items: ["5991b51486f77447b112d44f"] })'), "other items and other step types are not");
  // a zone that holds a smaller zone of the same step (the general area) is left out
  const sq = (x, z, r) => `{ kind: "zone", pos: { x: ${x}, z: ${z} }, outline: [{ x: ${x - r}, z: ${z - r} }, { x: ${x + r}, z: ${z - r} }, { x: ${x + r}, z: ${z + r} }, { x: ${x - r}, z: ${z + r} }] }`;
  assert(w.eval(`dropAreas([${sq(0, 0, 10)}, ${sq(2, 2, 1)}]).map((p) => p.pos.x).join()`) === "2", "the area around a spot is left out");
  assert(w.eval(`dropAreas([${sq(0, 0, 1)}, ${sq(0.2, 0, 1)}]).length`) === 1, "two copies of one zone show once");
  assert(w.eval(`dropAreas([${sq(0, 0, 1)}, ${sq(50, 0, 1)}, { kind: "item", pos: { x: 0, z: 0 } }]).length`) === 3, "separate zones and item spots stay");
  // marker colors: a key that the step needs adds a red ring
  const stepMarks = [...d.querySelectorAll(".leaflet-marker-pane .q-icon, .leaflet-marker-pane .q-item")];
  assert(stepMarks.length > 0 && stepMarks.every((m) => !m.classList.contains("tool") && !m.classList.contains("key")), "task diamonds are drawn in the task color");
  const keyRing = w.eval(`(() => {
    const o = tasksForMap(S.current).flatMap((it) => it.objs).find((x) => x.positions.length).obj, before = o.requiredKeys;
    o.requiredKeys = [["kRing"]]; S.keyLocks.set("kRing", new Set(S.current.ids)); drawQuestMarkers();
    const n = document.querySelectorAll(".leaflet-marker-pane .key").length;
    o.requiredKeys = before; S.keyLocks.delete("kRing"); drawQuestMarkers();
    return n;
  })()`);
  assert(keyRing > 0 && d.querySelectorAll(".leaflet-marker-pane .key").length === 0, "a step that needs a key on this map has a red ring");
  // the mission list shows the map marker of each step on the map, not a pin
  w.eval("renderQuestPanel()");
  const listMarks = [...d.querySelectorAll("#questList .step.go .step-mark > div")];
  assert(listMarks.length > 0 && listMarks.length === d.querySelectorAll("#questList .step.go").length && !d.getElementById("questList").textContent.includes("\u{1f4cd}"), "each step on the map shows its marker in the mission list");
  assert(w.eval('markerClass({ type: "mark", markerItem: "5991b51486f77447b112d44f" }, "zone", "")') === "q-icon tool" && w.eval('markerClass({}, "item", "k")') === "q-item key", "the list marker has the same classes as the map marker");
  assert(w.eval('markerClass({ type: "plantItem", items: [{ id: "5448fee04bdc2dbc018b4567" }] }, "zone", "")') === "q-item stash" && w.eval('markerClass({ type: "plantQuestItem" }, "zone", "")') === "q-item stash", "a stash step is a purple dot");
  assert(w.eval('markerClass({ type: "plantItem", items: [{ id: "5b4391a586f7745321235ab2" }] }, "zone", "")') === "q-icon tool", "a camera step stays a blue diamond");
  assert(w.eval('markerClass({ type: "shoot" }, "zone", "", true)') === "q-area" && w.eval('markerClass({ type: "shoot" }, "zone", "", false)') === "q-icon", "a kill area with an outline is a dashed area; without one it stays a diamond");
  const areaDraw = w.eval(`(() => {
    const obj = S.tasksById.get("checking").objectives[0], had = S.sel.has("checking");
    S.sel.add("checking"); obj.type = "shoot"; drawQuestMarkers();
    const r = [document.querySelectorAll(".q-area-hit").length, document.querySelectorAll(".leaflet-overlay-pane path[stroke-dasharray]").length];
    obj.type = "visit"; if (!had) S.sel.delete("checking"); drawQuestMarkers();
    return r.join();
  })()`);
  assert(/^[1-9]\d*,[1-9]\d*$/.test(areaDraw), "a kill area draws a dashed outline with a hover line (" + areaDraw + ")");
  // a click on the task name collapses the mission card to its name line, and a second click opens it
  w.eval("renderQuestPanel()");
  const card0 = () => d.querySelector("#questList .qcard");
  const name0 = card0().querySelector(".qname").textContent;
  card0().querySelector(".qname").click();
  assert(card0().classList.contains("collapsed") && card0().querySelector(".qname").textContent === name0 && JSON.parse(w.localStorage.getItem("tqm.collapsedCards")).length === 1, "a click on the name collapses the card");
  card0().querySelector(".qname").click();
  assert(!card0().classList.contains("collapsed") && JSON.parse(w.localStorage.getItem("tqm.collapsedCards")).length === 0, "a second click shows the steps again");
  const markerCount = () => d.querySelectorAll(".leaflet-marker-pane .q-icon, .leaflet-marker-pane .q-item, .leaflet-overlay-pane .q-area-hit").length;
  w.eval("renderQuestPanel(); drawQuestMarkers()");
  const markedCard = () => [...d.querySelectorAll("#questList .qcard:not(.collapsed)")].find((c) => c.querySelector(".step.go"));
  const allMarkers = markerCount(), markedName = markedCard().querySelector(".qname").textContent;
  markedCard().querySelector(".qname").click();
  const foldedCard = [...d.querySelectorAll("#questList .qcard")].find((c) => c.querySelector(".qname").textContent === markedName);
  assert(allMarkers > 0 && foldedCard.classList.contains("collapsed") && markerCount() < allMarkers, "a collapsed card hides the task's markers");
  foldedCard.querySelector(".qname").click();
  assert(markerCount() === allMarkers, "opening the card shows the markers again");
  // a long task name loses words from its middle
  assert(w.eval('middleCut("The Survivalist Path - Wounded Beast", 26)') === "The Survivali…Wounded Beast" && w.eval('middleCut("Health Care Privacy - Part 2", 16)') === "Health C…Part 2", "a long name loses letters from its middle, with no dash at the cut");
  // the mission list leaves out "hand over" steps
  const handOver = w.eval(`(() => {
    const task = S.tasksById.get("checking"), before = task.objectives;
    task.objectives = [...before, { id: "gv", description: "gv", type: "giveQuestItem", maps: [] }];
    const a = missionCard(task, true).textContent;
    task.objectives = [{ id: "gv", description: "gv", type: "giveItem", maps: [] }];
    const b = missionCard(task, true).textContent;
    task.objectives = before;
    return [a.includes("gv"), b.includes("Only hand-over steps left")].join();
  })()`);
  assert(handOver === "false,true", "the mission list leaves out hand-over steps");
  // long step openings are made short
  w.eval('S.tasksEn["fir1"] = "Find the item in raid: Salewa first aid kit"; S.tasksEn["ob1"] = "Obtain the item: Golden rooster"');
  assert(w.eval('stepText({ description: "fir1" })') === "Find in raid: Salewa first aid kit" && w.eval('stepText({ description: "ob1" })') === "Obtain: Golden rooster", "short step openings");
  // steps with no spot on the map: red X (kill), white magnifier (obtain), gold magnifier (find in raid)
  assert(w.eval('stepIcon({ type: "shoot" })').includes("si-kill") && w.eval('stepIcon({ type: "findItem", foundInRaid: false })').includes("si-obtain") && w.eval('stepIcon({ type: "findItem", foundInRaid: true })').includes("si-fir") && w.eval('stepIcon({ type: "visit" })') === "• ", "step icons for steps with no spot");
  // locked doors layer: off by default; orange bars, brighter when a ticked task needs the key
  const locks = () => d.querySelectorAll(".leaflet-marker-pane .lock-mark");
  assert(locks().length === 0 && !d.getElementById("showLocks").checked, "the locked doors layer is off by default");
  d.getElementById("showLocks").click();
  assert(locks().length === 2 && w.localStorage.getItem("tqm.showLocks") === "true", "the layer shows each lock that has a position");
  assert(d.querySelectorAll(".leaflet-marker-pane .lock-mark.need").length === 0, "no lock is marked before a ticked task needs its key");
  const needLock = w.eval(`(() => {
    const o = tasksForMap(S.current).filter((it) => isShown(it.task.id)).flatMap((it) => it.objs).find((x) => !x.done).obj, before = o.requiredKeys;
    o.requiredKeys = [["k208"]]; drawLocks();
    const n = document.querySelectorAll(".leaflet-marker-pane .lock-mark.need").length;
    o.requiredKeys = before; drawLocks();
    return n;
  })()`);
  assert(needLock === 1, "the lock of a key that a ticked task needs is brighter");
  const otherMap = w.eval(`(() => {
    const it = tasksForMap(S.current).find((x) => isShown(x.task.id)), before = it.task.neededKeys;
    it.task.neededKeys = [{ map: "${WOODS}", keys: ["k208"] }]; drawLocks();
    const n = document.querySelectorAll(".leaflet-marker-pane .lock-mark.need").length;
    it.task.neededKeys = before; drawLocks();
    return n;
  })()`);
  assert(otherMap === 0, "a key that the task needs on another map does not mark the lock here");
  d.getElementById("showLocks").click();
  assert(locks().length === 0, "the option hides the layer");
  // a click on a marker shows the floor of that marker (Customs dorms: 2nd floor)
  const floorBefore = w.eval("S.floorIndex");
  w.eval("goFloor({ x: 200, y: 4, z: 150 })");
  assert(w.eval("S.floorIndex") === 0, "a point in the dorms at 2nd-floor height selects the 2nd floor");
  w.eval("[...S.markersByKey.values()][0].fire('click')");
  await sleep(30);
  assert(w.eval("S.floorIndex") === -1, "a click on a ground-level task marker goes back to the ground level");
  w.eval(`showFloor(${floorBefore})`);
  // − / + / ✓ on a mission card step, only when progress can be sent
  const cardBtns = (o) => w.eval(`[...cardButtons(${o}).querySelectorAll("button")].map((b) => b.textContent).join("")`);
  w.eval("S.cfgSaved = S.cfg; S.cfg = { ...S.cfg, hasToken: true, writeTT: true, canWrite: true }");
  w.eval("S.objDone.set('cb1', { id: 'cb1', count: 2 })");
  assert(cardBtns('{ id: "cb1", count: 5 }') === "−+✓" && cardBtns('{ id: "cb0", count: 5 }') === "+✓" && cardBtns('{ id: "cb2", count: 1 }') === "✓", "counted steps get − and +, every step gets ✓");
  w.eval("S.objDone.delete('cb1'); S.cfg = S.cfgSaved");
  assert(w.eval("canWrite()") || cardBtns('{ id: "cb2" }') === "", "no buttons when progress cannot be sent");
  // keys that a task needs
  assert(w.eval('keyText([["k206", "k207"]])') === "Dorm 206 or Spare key" && w.eval('keyText([{ map: "m", keys: ["k206"] }])') === "Dorm 206", "key names for a step and for a task: the icon name, else the full name");
  assert(w.eval('keyText([["k206", "k207"]], { full: true })') === "Dorm room 206 key or Spare key", "full key names for tooltips");
  // a key belongs to the map that has its lock (here: Woods), not to each map of the step
  const cfg = (k) => `S.mapCfgs.find((mc) => mc.key === "${k}")`;
  assert(w.eval(`keyText([["k206"]], { on: ${cfg("customs")} })`) === "" && w.eval(`keyText([["k206"]], { on: ${cfg("woods")} })`) === "Dorm 206", "on the map, a key shows only where its lock is");
  assert(w.eval(`keyText([["k206"]], { mapIds: ["${CUST}", "${WOODS}"] })`) === "Dorm 206 (Woods)" && w.eval(`keyText([["k206"]], { mapIds: ["${WOODS}"] })`) === "Dorm 206", "a step on two maps names the map of the key");
  assert(w.eval(`keyText([["k207"]], { on: ${cfg("customs")} })`) === "Spare key", "a key with no lock data shows on each map");
  // a step that names its map loses the locations on other maps, and the keys for them (Vitamins)
  const stale = w.eval(`(() => {
    const loc = (m) => ({ map: m, positions: [{ x: 1, y: 0, z: 1 }] });
    const obj = { id: "os", description: "os", type: "findQuestItem", maps: ["${CUST}", "${WOODS}"], possibleLocations: [loc("${CUST}"), loc("${WOODS}")], requiredKeys: [["k206"]] };
    const same = { id: "ot", description: "ot", type: "findQuestItem", maps: ["${CUST}", "${WOODS}"], possibleLocations: [loc("${CUST}"), loc("${WOODS}")], requiredKeys: [["k206"]] };
    const task = { id: "staleTask", name: "x", objectives: [obj, same], neededKeys: [{ map: "${CUST}", keys: ["k206"] }] };
    S.tasksEn.os = "Find the box on Customs"; S.tasksEn.ot = "Find the box";
    S.tasks.push(task); pruneStaleLocations(); S.tasks.pop();
    return JSON.stringify([obj.maps, obj.possibleLocations.map((l) => l.map), obj.requiredKeys, same.possibleLocations.length, same.requiredKeys, task.neededKeys]);
  })()`);
  assert(stale === JSON.stringify([[CUST], [CUST], [], 2, [["k206"]], [{ map: CUST, keys: ["k206"] }]]), "a step that names Customs keeps only its Customs location and loses the Woods key; a step that names no map is not changed");
  pick("Prapor");
  assert([...d.querySelectorAll(".trow")].find((r) => r.querySelector(".tname").textContent === "Checking").querySelector(".tmeta").textContent.includes("🔑 Dorm 206"), "the task line shows the key that the task needs");
  assert([...d.querySelectorAll(".trow")].find((r) => r.querySelector(".tname").textContent === "Checking").querySelector(".tmeta").title .startsWith("Keys: Dorm room 206 key"), "the full key name shows on hover");
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
  w.eval('S.tasksById.get("debut").wikiLink = "https://wiki.example/Debut"; renderQuestPanel()');
  const wl = [...d.querySelectorAll("#questList .qcard")].find((c) => c.querySelector(".qname")?.textContent === "Debut").querySelector("a.wiki");
  assert(wl && wl.getAttribute("href") === "https://wiki.example/Debut" && wl.target === "_blank", "a mission card has a link to the task's wiki page");
  // a card shows only the steps of this map, and a count of the steps on other maps
  const cardSteps = (others) => w.eval(`(() => {
    const here = S.current.primary.id, obj = (id, maps) => ({ id, description: id, type: id, maps });
    const objectives = [obj("cam here", [here]), obj("hand over", []), ...Array.from({ length: ${others} }, (_, i) => obj("cam " + i, ["otherMap"]))];
    return [...missionCard({ id: "ref", name: "ref", trader: "${PRAPOR}", objectives }, true).querySelectorAll(".step")].map((s) => s.textContent);
  })()`);
  const many = cardSteps(4), one = cardSteps(1), none = cardSteps(0);
  assert(many.length === 3 && many.some((x) => x.includes("cam here")) && many.some((x) => x.includes("hand over")) && many.at(-1) === "+ 4 steps on other maps", "steps on other maps are left out of the card");
  assert(one.length === 3 && !one.some((x) => x.includes("cam 0")) && one.at(-1) === "+ 1 step on other maps", "one step on another map is left out too");
  assert(none.length === 2 && !none.some((x) => x.includes("other maps")), "no count when all steps are on this map");
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
  assert(!text("#questList .qname").includes("Brand New Quest"), "the mission list leaves out an unknown task");
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
  assert(d.querySelector("#info #raidTimer") && d.querySelector("header > #status") && d.querySelector("#brand #tabs"), "the timer is at the right; the status line is apart, so it can go on the second row");
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

  // the Layers option puts "any map" tasks apart from the tasks of this map
  assert(d.getElementById("app").classList.contains("split-list") && d.querySelector("#questList .qg-here"), "the any-map tasks are apart by default");
  d.getElementById("splitList").click();
  assert(!d.getElementById("app").classList.contains("split-list") && w.localStorage.getItem("tqm.splitList") === "false", "the option turns it off");
  d.getElementById("splitList").click();
  assert(d.getElementById("app").classList.contains("split-list"), "and on again");
  assert(!d.getElementById("showAll"), "the every-available-task option is gone");
  assert(d.querySelectorAll(".leaflet-marker-pane .q-icon").length === 2, "the map shows the two ticked zones");

  // the Settings tab also shows the status: counters, connections and the activity lines
  d.getElementById("tabSettings").click();
  await sleep(50);
  assert(!d.getElementById("tabStatus") && d.querySelector("#settings #statusPart #statCards") && d.querySelector("#settings #activity"), "the status is part of the Settings tab");
  assert(text("#statCards .v").join("|") === "PvP|4,812|2|93", "status cards: mode, log lines, changes waiting, writes left");
  const conn = (name) => [...d.querySelectorAll("#connRows .conn")].find((c) => c.querySelector(".name").textContent === name);
  assert(conn("TarkovTracker").classList.contains("good") && conn("TarkovTracker").textContent.includes("read and write"), "TarkovTracker row shows the token rights");
  assert(conn("Game data").textContent.includes("tasks") && conn("Game logs").textContent.includes("3 files"), "game data and game logs rows");
  assert(conn("Screenshots").classList.contains("wait") && conn("Game").querySelector(".pill").textContent === "Running", "screenshots wait for a position; the game runs");
  assert(conn("Flea prices").classList.contains("good") && conn("Flea prices").textContent.includes("360 items, 214 crafts") && conn("Flea prices").textContent.includes("new download after")
    && conn("Flea prices").querySelector(".pill").textContent === "Saved" && d.getElementById("fleaRefresh"), "the flea prices row shows the saved prices and a download button");
  assert(conn("Story chapters").classList.contains("good") && conn("Story chapters").textContent.includes("10 chapters, 437 steps") && d.getElementById("storyRefresh"),
    "the story chapters row shows the saved chapters and a download button");
  routes["/api/status"].flea = { ...routes["/api/status"].flea, error: "offline", errorTime: Date.now() / 1000 };
  await w.eval("loadStatus()");
  assert(conn("Flea prices").classList.contains("wait") && conn("Flea prices").querySelector(".pill").textContent === "Old prices" && conn("Flea prices").textContent.includes("offline"), "a failed download keeps the old prices");
  routes["/api/status"].flea = { busy: false, maxAge: 28800, error: null, errorTime: null };
  await w.eval("loadStatus()");
  assert(conn("Flea prices").querySelector(".pill").textContent === "Not loaded" && conn("Flea prices").textContent.includes("open the Crafts tab"), "no saved prices yet");
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
  assert(groups().join() === "Prapor,Jaeger" && rows().includes("Jaeger Job") && rows().includes("Debut"), "All traders: the lines of each trader under its name");
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
  // the level: typed by hand, sent to the helper, and used for the task states at once
  const lvl = d.getElementById("levelInput");
  assert(lvl && lvl.value === "12", "with sending on, the level is a box");
  lvl.value = "80"; lvl.dispatchEvent(new w.Event("change"));
  assert(progressPosts.at(-1)[0] !== "/api/progress/level" && d.getElementById("levelInput").value === "12", "a level out of range is not sent");
  d.getElementById("levelInput").value = "40"; d.getElementById("levelInput").dispatchEvent(new w.Event("change"));
  assert(JSON.stringify(progressPosts.at(-1)) === JSON.stringify(["/api/progress/level", { level: 40 }]), "a new level goes to the helper");
  assert(w.eval("S.available.some((x) => x.id === 'highLevel')") && d.getElementById("levelInput").value === "40", "a task that needs the new level becomes available");
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
  console.log("floors:", text("#floorSelect option"), "style:", d.getElementById("styleBtn").textContent);
  // the level buttons go through the levels from the lowest to the highest
  const floorName = () => d.getElementById("floorSelect").selectedOptions[0].textContent;
  const up = d.getElementById("floorUp"), down = d.getElementById("floorDown");
  w.eval("showFloor(-1)");
  const seen = [floorName()];
  while (!up.disabled) { up.click(); seen.push(floorName()); }
  assert(seen.join() === "Ground level,2nd Floor,3rd Floor,4th Floor", "the up button goes up to the highest level: " + seen.join());
  down.click(); down.click(); down.click(); down.click();
  assert(floorName() === "Underground" && down.disabled && !up.disabled, "the down button goes below the ground level and stops at the lowest level");
  w.eval("showFloor(-1)");
  // the style button shows the current style and changes to the other one
  const styleBtn = d.getElementById("styleBtn");
  assert(styleBtn.textContent === "Abstract" && !styleBtn.disabled, "the style button shows the current style");
  styleBtn.click(); await sleep(100);
  assert(styleBtn.textContent === "Satellite" && w.localStorage.getItem("tqm.style") === '"tile"', "a click changes to the satellite map and keeps the choice");
  styleBtn.click(); await sleep(100);
  assert(styleBtn.textContent === "Abstract", "a second click goes back to the abstract map");

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
  assert([...d.querySelectorAll(".ex-shared")].length > 0 && [...d.querySelectorAll(".ex-shared")].every((x) => x.classList.contains("ex-scav") && !x.classList.contains("ex-pmc")), "in a Scav raid, a shared extract has the Scav color");
  const mode = d.getElementById("extractMode");
  mode.value = "both"; mode.dispatchEvent(new w.Event("change"));
  assert(exNames().includes("ex_scav_b") && exNames().includes("Crossroads"), "PMC and Scav shows both");
  mode.value = "off"; mode.dispatchEvent(new w.Event("change"));
  assert(exNames().length === 0, "None shows no extracts");
  mode.value = "auto"; mode.dispatchEvent(new w.Event("change"));
  // a transit: the raid ends for a moment and the next map loads; the Map tab stays open
  w.eval("S.backDelay = 150");
  raid({});
  await sleep(50);
  assert(d.getElementById("app").dataset.tab === "map", "the Map tab stays open for a moment after the raid");
  raid({ phase: "loading", scenePath: "maps/customs_preset.bundle", since: Date.now() / 1000 });
  await sleep(200);
  assert(d.getElementById("app").dataset.tab === "map", "a transit to the next map keeps the Map tab open");
  raid({});
  await sleep(200);
  assert(d.getElementById("app").dataset.tab === "tasks", "after the wait the page goes back to the Tasks tab");
  // a raid that starts while the Map tab is open also goes back to Tasks after it
  d.getElementById("tabMap").click();
  raid({ phase: "raid", scenePath: "maps/customs_preset.bundle", location: "bigmap", online: true, raidId: "MAP01", side: "pmc", started: Date.now() / 1000 });
  await sleep(50);
  raid({});
  await sleep(200);
  assert(d.getElementById("app").dataset.tab === "tasks", "a raid that starts on the Map tab goes back to Tasks after it");
  // a click on the Map tab during the raid keeps the Map tab open after it
  raid({ phase: "raid", scenePath: "maps/customs_preset.bundle", location: "bigmap", online: true, raidId: "MAP02", side: "pmc", started: Date.now() / 1000 });
  await sleep(50);
  d.getElementById("tabMap").click();
  raid({});
  await sleep(200);
  assert(d.getElementById("app").dataset.tab === "map", "a tab click during the raid cancels the switch back");
  d.getElementById("tabTasks").click();
  assert(exNames().includes("Crossroads") && !exNames().includes("ex_scav_b"), "after the raid the PMC extracts are back");
  assert(d.querySelector("#layersPanel #extractMode") && d.querySelector("#layersPanel #splitList") && !d.querySelector("#settings #showQuests"), "the map options are in the Layers panel of the Map tab");
  d.getElementById("layersBtn").click();
  assert(d.getElementById("layersPanel").classList.contains("open") && d.getElementById("layersBtn").classList.contains("on"), "the Layers button opens the panel");
  d.getElementById("layersBtn").click();
  assert(!d.getElementById("layersPanel").classList.contains("open"), "and closes it");
  // a task that tarkov.dev does not have: found in the old logs, shown as text, can get a name
  {
    const GHOST = "6a763df2161e4b45b1015663", before = d.getElementById("app").dataset.tab;
    const ghostRow = () => d.querySelector("#taskLines .trow.unknown");
    logOnlyTasks.push(GHOST);
    await w.eval("findUnknownInLogs()");
    d.getElementById("tabTasks").click(); pick("My tasks");
    assert(quests.modes.regular.selected.includes(GHOST) && ghostRow()?.querySelector(".tname").textContent === "Unknown task …015663", "a started task that the data does not have shows under My tasks");
    w.prompt = () => "A Familiar Face...";
    ghostRow().querySelectorAll("button")[1].click();
    assert(ghostRow().querySelector(".tname").textContent === "A Familiar Face..." && !text("#questList .qname").includes("A Familiar Face..."), "the task can get a name; the mission list still leaves it out");
    ghostRow().querySelector("button").click();
    await sleep(20);
    assert(!ghostRow() && !quests.modes.regular.selected.includes(GHOST), "the × button removes it");
    await w.eval("findUnknownInLogs()");
    assert(!quests.modes.regular.selected.includes(GHOST), "and the old logs do not put it back");
    logOnlyTasks.length = 0;
    d.getElementById("tab" + before[0].toUpperCase() + before.slice(1)).click();
  }
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
  assert(text("#settings h2").join("|") === "TarkovTracker|Folders|Automatic actions|Updates|Status|Connections|Activity|About, credits and licenses", "the Settings tab has a heading for each group");
  // updates: the page asks before it installs a new version
  const ubox = d.getElementById("updateBox");
  // patch notes load when the list is opened
  routes["/api/update/notes"] = { notes: [
    { sha: "c".repeat(40), date: "2026-11-22T10:00:00Z", subject: "Newest change", body: "- detail", installed: false },
    { sha: "a".repeat(40), date: "2026-11-21T10:00:00Z", subject: "Installed change", body: "", installed: true }] };
  const pn = d.getElementById("patchNotes");
  pn.open = true; pn.dispatchEvent(new w.Event("toggle"));
  await sleep(50);
  assert(text("#notesList .subj").join("|") === "Newest change|Installed change" && text("#notesList .tag").join("|") === "new|installed", "patch notes show the changes and mark the new and the installed one");
  assert(ubox.hidden && d.getElementById("autoUpdate") && d.getElementById("checkUpdate") && d.getElementById("openGithub"), "no question without a new version; Settings has the update options");
  send({ type: "update", state: "available", local: "a".repeat(40), remote: "b".repeat(40), behind: 2, message: "Add a thing", changed: [], startedAt: 1 });
  await sleep(20);
  assert(!ubox.hidden && ubox.textContent.includes("Add a thing") && ubox.textContent.includes("2 new changes") && d.getElementById("updNow"), "a new version shows the question");
  assert(d.getElementById("updateStatus").textContent.includes("Version aaaaaaa"), "Settings shows the installed version");
  d.getElementById("updLater").click();
  assert(ubox.hidden, "Not now closes the question");
  send({ type: "update", state: "updated", local: "b".repeat(40), remote: "b".repeat(40), behind: 0, changed: [], startedAt: 1 });
  await sleep(20);
  assert(!ubox.hidden && d.getElementById("updRestart"), "after the update the page offers a restart");
  d.getElementById("updLater").click();
  send({ type: "update", state: "error", error: "Could not check for updates: offline", startedAt: 1 });
  await sleep(20);
  assert(ubox.hidden && d.getElementById("updateStatus").textContent.includes("offline"), "a failed check at start shows only in Settings");
  assert(app.dataset.tab === "tasks" && !timer.classList.contains("on"), "raid end goes back to the Tasks tab and hides the timer");
  send({ type: "game", mode: "pve", session: "s", raid: { phase: "idle" } });
  await sleep(20);
  assert(d.getElementById("status").textContent.includes("no TarkovTracker token"), "warns when the game mode has no token");

  // Crafts tab: each station with its crafts, and the profit at flea and trader prices
  d.getElementById("tabCrafts").click();
  await sleep(60);
  assert(app.dataset.tab === "crafts" && w.eval("!!S.craftData"), "the Crafts tab loads the crafts");
  const stBtns = [...d.querySelectorAll("#craftStations .stbtn")];
  assert(stBtns.map((b) => b.title).join() === "Medstation,Workbench" && stBtns.every((b) => b.classList.contains("on")), "a button for each station with crafts, by name, all on");
  const crow = () => [...d.querySelectorAll("#craftList tbody tr .stn")].map((e) => e.title);
  assert(text("#craftList tbody tr .stn").join() === "Me01,Wo01,Wo02", "the station column has the icon and the level number only");
  assert(crow().join("|") === "Medstation, level 1|Workbench, level 1|Workbench, level 2" && d.querySelectorAll("#craftList tbody tr")[2].classList.contains("lvlstart"),
    "one table in level order, then station; a line at a new level");
  stBtns[1].click();
  assert(crow().join() === "Medstation, level 1" && !stBtns[1].classList.contains("on") && w.localStorage.getItem("tqm.craftHidden").includes("st1"), "a station button hides its crafts, and the choice is kept");
  stBtns[1].click();
  assert(crow().length === 3 && stBtns[1].classList.contains("on"), "a second click shows them again");
  const fee = w.eval("fleaFee(5000, 10000)");
  assert(fee > 0 && fee < 10000, "the flea fee is calculated");
  const c1 = w.eval("craftCalc(S.craftData.crafts[0])");
  assert(c1.cost === 1600 && c1.parts[0].unit.src === "Prapor 2", "a component comes from the cheaper of flea and trader; a tool costs nothing");
  assert(c1.sale.price === 10000 - fee && c1.profit === 10000 - fee - 1600 && c1.hour === c1.profit / 2, "profit = flea price less the fee, less the cost; per hour");
  const c2 = w.eval("craftCalc(S.craftData.crafts[1])");
  assert(c2.sale.price === 1200 && c2.sale.src === "Sell to Jaeger", "a product that cannot go on the flea sells to a trader, times the count");
  assert(w.eval("craftCalc(S.craftData.crafts[2]).profit") === null && d.querySelector("#craftList tbody td.num:nth-last-child(2)").textContent === "?", "a component with no price gives no profit");
  d.getElementById("craftTraders").click();
  assert(w.eval("craftCalc(S.craftData.crafts[0]).cost") === 2000, "with no trader prices the components come from the flea");
  d.getElementById("craftTraders").click();
  d.getElementById("craftPrice").value = "low"; d.getElementById("craftPrice").dispatchEvent(new w.Event("change"));
  assert(w.eval("craftCalc(S.craftData.crafts[0]).sale.price") === 9000 - w.eval("fleaFee(5000, 9000)"), "the lowest offer can be the flea price");
  d.getElementById("craftPrice").value = "avg"; d.getElementById("craftPrice").dispatchEvent(new w.Event("change"));
  d.getElementById("craftSort").value = "hour"; d.getElementById("craftSort").dispatchEvent(new w.Event("change"));
  assert(text("#craftList tbody tr .prod")[0].startsWith("Weapon parts"), "sort by profit per hour");
  d.getElementById("craftSort").value = "level"; d.getElementById("craftSort").dispatchEvent(new w.Event("change"));
  const wrow = [...d.querySelectorAll("#craftList tbody tr")].find((r) => r.textContent.includes("Gunpowder"));
  assert(wrow.querySelector(".parts").textContent.includes("Bolts @ 800 ₽") && !wrow.querySelector(".parts").textContent.includes("×") && wrow.querySelector(".parts").textContent.indexOf("each") < 0, "one component: no price each");
  const prow = [...d.querySelectorAll("#craftList tbody tr")].find((r) => r.textContent.includes("Weapon parts") && r.textContent.includes("Bolts"));
  assert(prow.querySelector(".parts").textContent.includes("Bolts @ 800 ₽ × 2 = 1,600 ₽"), "two or more components: the price as a formula");
  assert(wrow.textContent.includes("400 ₽ each") && !prow.querySelectorAll("td.num")[2].textContent.includes("each"), "a product made in a stack shows the value of one");
  d.getElementById("craftSearch").value = "gunpow"; d.getElementById("craftSearch").dispatchEvent(new w.Event("input"));
  assert(d.querySelectorAll("#craftList tbody tr").length === 1, "the search finds a craft by an item name");
  d.getElementById("craftSearch").value = ""; d.getElementById("craftSearch").dispatchEvent(new w.Event("input"));
  routes["/api/crafts?mode=regular&force=1"] = { ...routes["/api/crafts?mode=regular"], fetched: 1700003600 };
  assert(!d.getElementById("craftRefresh"), "the download button is in Settings, not on the Crafts tab");
  d.getElementById("tabSettings").click();
  await sleep(30);
  d.getElementById("fleaRefresh").click();
  await sleep(60);
  assert(w.eval("S.craftData.fetched") === 1700003600, "the Settings button downloads the prices again");

  // Story tab: an icon for each chapter, the steps of the selected chapter with ✓ and ✕, a wiki arrow on each step
  d.getElementById("tabStory").click();
  await sleep(60);
  const tiles = () => [...d.querySelectorAll("#storyNav .ctile")];
  const head = () => d.querySelector("#storyList .chead");
  const pickChap = (id) => d.querySelector(`#storyNav .ctile[data-chap="${id}"]`).click();
  assert([...d.querySelectorAll("#tabs .tab")].map((b) => b.textContent).join() === "Storyβ,Tasks,Map,Crafts,Settings", "the tabs are in order, Story first, with a beta mark");
  assert(app.dataset.tab === "story" && tiles().map((t) => t.dataset.chap).join() === "tour,skies" && tiles()[0].classList.contains("on")
    && tiles()[0].querySelector("img").getAttribute("src") === "https://tarkovtracker.org/img/storyline/tour.webp", "a tile with an icon for each chapter; the first is selected");
  assert(head().querySelector("h2").textContent === "Tour ↗" && head().querySelector("a.warrow").getAttribute("href") === W + "Tour", "the chapter name has a wiki arrow");
  assert(head().querySelector(".scnt").textContent === "1/3", "a tutorial step is done; an optional step does not count");
  const steps = () => [...d.querySelectorAll("#storyList .sstep")];
  assert(steps().map((li) => li.querySelector(".stxt").textContent).join("|") === "Escape Ground Zero|Hand over cash to Therapist|Collect the cash|Talk to Ragman"
    && steps()[2].classList.contains("kid"), "an optional step is under its parent");
  assert(steps().map((li) => li.querySelector("a.warrow").getAttribute("href")).join() === [W + "Tour#Escape", W + "Tour#Cash", W + "Tour#Cash", W + "Tour"].join()
    && steps().every((li) => li.lastElementChild.matches("a.warrow") && li.querySelector("a.warrow").textContent === "↗" && li.querySelector("a.warrow").target === "_blank"),
    "each step ends with a ↗ to its wiki section in a new window");
  assert(!d.querySelector("#storyList input[type=checkbox]") && steps()[1].querySelector("[data-done]").textContent === "✓" && steps()[1].querySelector("[data-fail]").textContent === "✕",
    "each step has a ✓ and a ✕ button, no checkbox");
  assert(steps()[0].querySelector("[data-done]").disabled && steps()[0].querySelector("[data-done]").classList.contains("on") && !steps()[0].querySelector("[data-fail]"),
    "the tutorial step is done and cannot change");
  const unl = steps()[0].querySelector(".sunl");
  assert(unl.textContent === "Opens trader Therapist" && unl.parentElement === steps()[0] && unl.nextElementSibling.matches("a.warrow"), "what a step opens is on the right of its row, before the arrow");
  steps()[1].querySelector("[data-done]").click();
  await sleep(30);
  assert(JSON.stringify(storyPosts.at(-1)) === JSON.stringify({ mode: "regular", done: ["s2"], undone: [], failed: [], unfailed: [] }) && head().querySelector(".scnt").textContent === "2/3"
    && steps()[1].querySelector("[data-done]").classList.contains("on"), "✓ marks the step done on the server");
  steps()[1].querySelector("[data-done]").click();
  await sleep(30);
  assert(JSON.stringify(storyPosts.at(-1).undone) === '["s2"]' && head().querySelector(".scnt").textContent === "1/3", "a second ✓ removes the done mark");
  send({ type: "story", mode: "regular", done: ["s2", "s4"] });
  await sleep(20);
  assert(head().querySelector("h2").classList.contains("complete") && tiles()[0].classList.contains("complete") && w.eval("S.storyDone.has('s4')"),
    "a mark from another page shows; all main steps done completes the chapter");
  pickChap("skies");
  assert(tiles()[1].classList.contains("on") && head().querySelector("h2").textContent.startsWith("Falling Skies") && w.localStorage.getItem("tqm.storyChapter") === '"skies"',
    "a tile selects its chapter, and the choice is kept");
  assert(steps()[0].textContent.includes("Choice: path A") && steps()[1].textContent.includes("Choice: path B"), "the two paths of a choice have a label");
  steps()[1].querySelector("[data-done]").click();
  await sleep(30);
  assert(steps()[0].classList.contains("blocked") && head().querySelector(".scnt").textContent === "1/2", "a mark on path B blocks path A, which does not count");
  d.getElementById("storyHideDone").click();
  assert(steps().length === 1 && steps()[0].textContent.includes("Last step"), "hide done steps hides the done and the blocked steps");
  d.getElementById("storyHideDone").click();
  d.querySelector("#storyList [data-untick-all]").click();
  await sleep(30);
  assert(JSON.stringify(storyPosts.at(-1).undone) === '["f2"]' && !steps().some((li) => li.classList.contains("blocked")), "clear all marks removes the marks of the chapter");
  d.querySelector("#storyList [data-tick-all]").click();
  await sleep(30);
  assert(JSON.stringify(storyPosts.at(-1).done) === '["f3"]', "mark all done leaves out the steps of a choice");
  steps()[2].querySelector("[data-fail]").click();
  await sleep(30);
  assert(steps()[2].classList.contains("failed") && !steps()[2].querySelector("[data-done]").classList.contains("on") && steps()[2].querySelector("[data-fail]").classList.contains("on")
    && steps()[2].textContent.includes("Failed") && JSON.stringify(storyFailed.regular) === '["f3"]' && !storyDone.regular.includes("f3"), "✕ marks a done step failed, and it is no longer done");
  assert(head().querySelector(".scnt").textContent === "0/2", "a failed step leaves the total");
  steps()[2].querySelector("[data-done]").click();
  await sleep(30);
  assert(!steps()[2].classList.contains("failed") && storyDone.regular.includes("f3") && !storyFailed.regular.length, "✓ on a failed step makes it done");
  steps()[2].querySelector("[data-fail]").click();
  await sleep(30);
  steps()[2].querySelector("[data-fail]").click();
  await sleep(30);
  assert(!storyFailed.regular.length && !storyDone.regular.includes("f3") && !steps()[2].classList.contains("failed"), "a second ✕ removes the failed mark");
  steps()[0].querySelector("[data-fail]").click();
  await sleep(30);
  d.querySelector("#storyList [data-untick-all]").click();
  await sleep(30);
  assert(!storyFailed.regular.length, "clear all marks also removes the failed marks");
  // ending routes: a chapter with routes has a button for each route
  const rbtn = (id) => d.querySelector(`#routeBar [data-route="${id}"]`);
  assert(!d.getElementById("routeBar") === false && rbtn("all").classList.contains("on") && rbtn("one").textContent === "One" && d.getElementById("routeBar").textContent.includes("Endings chart ↗ by Someone, version 1.0"),
    "a chapter with routes shows the route buttons and the source of the routes");
  pickChap("tour");
  assert(!d.getElementById("routeBar"), "a chapter with no routes has no route buttons");
  pickChap("skies");
  rbtn("one").click();
  const secs = () => [...d.querySelectorAll("#storyList .ssec")].map((e) => e.textContent);
  assert(secs().join() === "The case,Route one" && d.querySelector("#storyList .snote").textContent === "Decision: keep the case or not." && w.localStorage.getItem("tqm.storyRoute") === '"one"',
    "a route shows its sections, notes and steps, and the choice is kept");
  const rstep = (t) => steps().find((li) => li.querySelector(".stxt").textContent === t);
  assert(rstep("Route text for the last step").querySelector("a.warrow").getAttribute("href") === W + "Falling_Skies" && rstep("Keep the case").querySelector("a.warrow").getAttribute("href") === W + "Endings",
    "a step with a ref has the wiki link of the TarkovTracker step; the others link to the source");
  assert(rstep("Do route one").textContent.includes("Mandatory") && rstep("Do route one").textContent.includes("Fast") && rstep("Pay more").textContent.includes("If: You kept the case"), "route steps show their tags");
  assert(head().querySelector(".scnt").textContent === "0/3", "the count: main steps and the case choice once; optional and if steps do not count");
  rstep("Route text for the last step").querySelector("[data-done]").click();
  await sleep(30);
  assert(storyDone.regular.includes("f3") && head().querySelector(".scnt").textContent === "1/3", "a step with a ref uses the mark of the TarkovTracker step");
  rstep("Give the case").querySelector("[data-done]").click();
  await sleep(30);
  assert(rstep("Keep the case").classList.contains("blocked") && rstep("Pay more").classList.contains("blocked") && head().querySelector(".scnt").textContent === "2/3",
    "a case choice blocks the other side and its if steps");
  rstep("Give the case").querySelector("[data-done]").click();
  rstep("Keep the case").querySelector("[data-done]").click();
  await sleep(40);
  assert(!rstep("Pay more").classList.contains("blocked") && head().querySelector(".scnt").textContent === "2/4", "the if steps of the chosen side count");
  d.querySelector("#storyList [data-tick-all]").click();
  await sleep(30);
  assert(JSON.stringify(storyPosts.at(-1).done) === '["r-one"]', "mark all done in a route marks its main steps, not choices, if steps or optional steps");
  d.querySelector("#storyList [data-untick-all]").click();
  await sleep(30);
  assert(JSON.stringify(storyPosts.at(-1).undone.sort()) === '["f3","r-keep","r-one"]', "clear all marks in a route clears the marks of its steps");
  rbtn("two").click();
  assert(secs().join() === "The case,Route two", "another route shows its own sections");
  rbtn("all").click();
  assert(!d.querySelector("#storyList .ssec") && steps().length === 3, "all steps shows the TarkovTracker steps again");
  const search = d.getElementById("storySearch");
  search.value = "ragman"; search.dispatchEvent(new w.Event("input"));
  assert(tiles()[0].classList.contains("on") && tiles()[1].classList.contains("nomatch") && steps().length === 1, "a search moves to the first chapter with a match and dims the others");
  search.value = ""; search.dispatchEvent(new w.Event("input"));
  d.getElementById("tabTasks").click();

  // completing Checking in TarkovTracker drops it automatically
  routes["/api/progress"].data.tasksProgress.push({ id: "checking", complete: true });
  d.getElementById("refreshBtn").click();
  await sleep(100);
  assert(!text("#questList .qname").includes("Checking"), "completed ticked task drops off");
  console.log("ticked on the helper:", JSON.stringify(quests.modes.regular));
  console.log("errors:", errors);
  assert(!errors.filter((e) => !e.startsWith("warn")).length, "no page errors");

  // a reload on the Crafts tab: the item names come after the crafts, and the task list comes last
  const dom2 = new JSDOM(html, {
    runScripts: "dangerously", pretendToBeVisual: true, url: "http://localhost:3000/",
    beforeParse(w2) {
      w2.localStorage.setItem("tqm.tab", JSON.stringify("crafts"));
      // a PvE token: the page starts with the PvP mode until it has read the config
      w2.fetch = async (url) => {
        const u = String(url).replace("/pve/", "/regular/").replace("mode=pve", "mode=regular");
        const wait = { "/api/quests": 200, "https://json.tarkov.dev/regular/items_en": 80 }[u] || 0;
        if (wait) await new Promise((r) => setTimeout(r, wait));
        const pve = { "/api/config": { ...routes["/api/config"], gameMode: "pve" }, "/api/crafts?mode=regular": { ...routes["/api/crafts?mode=regular"], mode: String(url).includes("mode=pve") ? "pve" : "regular" } }[u];
        if (pve) return { ok: true, status: 200, json: async () => JSON.parse(JSON.stringify(pve)) };
        if (u === "/api/quests") return { ok: true, status: 200, json: async () => JSON.parse(JSON.stringify(quests)) };
        if (u.endsWith(".svg")) return { ok: true, status: 200, text: async () => svg };
        if (!(u in routes)) return { ok: false, status: 404, statusText: "nf", json: async () => ({}) };
        return { ok: true, status: 200, json: async () => JSON.parse(JSON.stringify(routes[u])) };
      };
      w2.EventSource = function () {};
      w2.SVGElement.prototype.getBBox = () => ({ x: 0, y: 0, width: 0, height: 0 });
      w2.SVGSVGElement.prototype.createSVGRect = () => ({});
    },
  });
  await sleep(600);
  const d2 = dom2.window.document;
  assert(d2.getElementById("app").dataset.tab === "crafts" && [...d2.querySelectorAll("#craftList tbody tr .prod")].map((e) => e.textContent.trim()).includes("Weapon parts"),
    "a reload on the Crafts tab shows the item names");
  assert(d2.getElementById("craftNote").textContent.startsWith("PvE"), "and the prices of the game mode of the token");
  dom2.window.close();
  process.exit();
})();
