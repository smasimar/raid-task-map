# Task step floors

This file lists every task step that has a position on a map, and the floor that the app gives each position.
The positions and heights are from the tarkov.dev task data (regular game mode). The floors are from the floor layers of the map (`maps.json`).

Each task was checked against the Guide section of its page on the [Escape from Tarkov Wiki](https://escapefromtarkov.fandom.com).
Where the wiki names a different floor than the app, the app now uses the wiki floor (`FLOOR_FIXES` in `index.html`).

Columns:
- **x, z**: the position on the map. **y**: the height.
- **Above ground**: the height above the lowest loot, spawns and extracts within 25 m. It is only a hint, because loot in a building makes the ground look higher.
- **Floor**: the floor that the map layers give. **Wiki floor**: the floor that the app uses now, with the words from the wiki.

## Results of the wiki check

- 38 steps (70 positions) were on the wrong floor. Most of them are on Streets of Tarkov. Its floor layers
  are height bands for the whole map (2nd Floor: 10 to 15 m). A building on low ground has its upper floors below 10 m,
  and a building on high ground has its 2nd floor in the 3rd Floor band.
- Interchange: the wiki calls the main level of the mall the first floor. tarkov.dev calls the same layer "2nd Floor" (its ground level is the
  parking garage). The markers are on the correct layer, so they were not changed.
- Customs industrial plant: the wiki calls the top floor of the northern building the third floor. The map layer for that floor is "4th Floor".
  The markers are on the layer that draws that floor, so they were not changed.
- Customs Warehouse 17 and the boiler building have no "2nd Floor" layer. Their upper floor is drawn on the "3rd Floor" layer, so the
  fixed markers use that layer and show "2nd Floor" as their floor name.
- Woods, Lighthouse and The Labyrinth have no floor layers, so their steps were not checked.

## Not confirmed

These positions show as ground level but are more than 3 m above the ground near them. For some of them the wiki does not give the floor.
For others the height comes from loot on an upper floor nearby. They were not changed. Check them in a raid.

| Map | Task | Step | y | Above ground |
|---|---|---|---|---|
| Customs | Bad Rep Evidence | Locate and obtain Secure Folder 0031 in one of the bunkhouses on Customs | 4.7 | 3.6 |
| Customs | Hobby Club | Stash the AK-50 body at the specified spot on Customs | 16.0 | 3.8 |
| Customs | Hobby Club | Stash the AK-50 handguard at the specified spot on Customs | 16.0 | 3.8 |
| Customs | Hobby Club | Stash the AK-50 barrel at the specified spot on Customs | 16.0 | 3.8 |
| Customs | Hobby Club | Stash the AK-50 dust cover at the specified spot on Customs | 16.0 | 3.8 |
| Customs | Hot Wheels | Complete the main objective as soon as possible | 1.7 | 5.7 |
| Customs | Rite of Passage | Eliminate Scavs at the new gas station on Customs | 9.2 | 8.1 |
| Customs | The Extortionist | Locate and obtain the hidden valuable cargo on Customs | 1.3 | 3.7 |
| Customs | The Extortionist | Locate the place where the messenger hid the cargo on Customs | 1.6 | 4.0 |
| Factory | Is This a Reference? | Install a WI-FI Camera in the room where the firefighter burned the books to become happy on Factory | 1.8 | 4.1 |
| Factory | Is This a Reference? | Install a WI-FI Camera in the room where the firefighter burned the books to become happy on Factory | 1.8 | 4.1 |
| Factory | Is This a Reference? | Install a WI-FI Camera near where someone thought he'd get transported to the magic school on Factory | 1.4 | 4.1 |
| Factory | Is This a Reference? | Install a WI-FI Camera near where someone thought he'd get transported to the magic school on Factory | 1.9 | 4.5 |
| Factory | Playing the Market | Fix the first control board with a Toolset on Factory | 1.1 | 3.7 |
| Factory | Playing the Market | Fix the second control board with a Toolset on Factory | 1.1 | 3.4 |
| Factory | Sanitary Standards | Locate the room with gas analyzers on Factory | 1.1 | 3.7 |
| Factory | Scout | Locate the fourth Factory extraction | 1.2 | 3.9 |
| Factory | Secrets of Polikhim | Stash the package at the laboratory storage room on Factory | 1.1 | 3.8 |
| Factory | Secrets of Polikhim | Stash the package at the laboratory storage room on Factory | 1.1 | 3.7 |
| Ground Zero | Is This a Reference? | Install a WI-FI Camera at the high rise where one die-hard guy kicked ass on Ground Zero | 23.9 | 6.6 |
| Ground Zero | Is This a Reference? | Install a WI-FI Camera at the high rise where one die-hard guy kicked ass on Ground Zero | 24.3 | 7.0 |
| Ground Zero | Luxurious Life | Locate the liquor store on Ground Zero | 24.2 | 11.6 |
| Ground Zero | Luxurious Life | Locate and obtain the wine bottle in the store | 24.2 | 11.3 |
| Ground Zero | Rough Tarkov | Locate the Claymore mine on Ground Zero | 23.7 | 9.5 |
| Ground Zero | Rough Tarkov | Locate the Claymore mine on Ground Zero | 24.3 | 10.3 |
| Interchange | No Swiping | Eliminate any target at the smuggler bases on Shoreline or Interchange | 32.4 | 7.4 |
| Interchange | Provocation | Stash a Toilet paper inside the secret container stash on Interchange | 25.1 | 3.6 |
| Reserve | Hobby Club | Locate and obtain the AK-50 barrel on Reserve | -4.3 | 7.6 |
| Reserve | Hobby Club | Locate and obtain the AK-50 barrel on Reserve | -4.0 | 8.0 |
| Reserve | Hobby Club | Locate and obtain the AK-50 barrel on Reserve | -4.2 | 7.0 |
| Reserve | Hobby Club | Locate Glukhar's workshop on Reserve | 2.1 | 13.3 |
| Reserve | Is This a Reference? | Install a WI-FI Camera at the place where conscripts did a very important task on Reserve | -6.5 | 7.4 |
| Reserve | Order From Outside | Locate and obtain the electronic jammer at the electromechanical warehouse on Reserve | -6.5 | 3.8 |
| Reserve | Order From Outside | Locate and obtain the electronic jammer at the electromechanical warehouse on Reserve | -6.5 | 3.5 |
| Reserve | Order From Outside | Locate and obtain the electronic jammer at the electromechanical warehouse on Reserve | -6.5 | 4.0 |
| Reserve | Special Comms | Stash a Bulbex cable cutter at the sandbags next to LAV III above the storage warehouse on Reserve | -0.1 | 6.8 |
| Reserve | The Huntsman Path - Administrator | Launch a yellow signal flare at the train depot on Reserve (In one raid) | 1.5 | 13.5 |
| Reserve | The Huntsman Path - Administrator | Eliminate any target at the train depot on Reserve (In one raid) | 0.3 | 10.6 |
| Shoreline | Health Care Privacy - Part 1 | Locate and mark the first ambulance with an MS2000 Marker on Shoreline | -59.2 | 5.6 |
| Shoreline | Humanitarian Supplies | Locate and mark the first UN truck with an MS2000 Marker | -3.5 | 3.8 |
| Shoreline | Humanitarian Supplies | Locate the first truck that was holding the lost UN cargo on Shoreline | -3.5 | 3.8 |
| Shoreline | Needle in a Haystack | Investigate the coast-side construction site on Shoreline | -54.7 | 4.9 |
| Shoreline | Proper Comeback | Stash a Golden rooster figurine at Prapor's WI-FI Camera on Shoreline | -47.8 | 15.3 |
| Shoreline | Viewer | Install a WI-FI Camera at the pier tower on Shoreline | -47.6 | 15.5 |
| Streets of Tarkov | Dandies | Stash a Bomber beanie inside the barber shop on Streets of Tarkov | 4.3 | 4.5 |
| Streets of Tarkov | Gendarmerie - Mall Cop | Eliminate any target at the stylobate building while using Pistols on Streets of Tarkov | 8.6 | 8.0 |
| Streets of Tarkov | Green Corridor | Determine the ambush spot | 7.1 | 4.3 |
| Streets of Tarkov | Needle in a Haystack | Investigate the children's playground by Concordia on Streets of Tarkov | 6.9 | 8.2 |
| Streets of Tarkov | Paramedic | Locate and obtain the ambulance paramedic's smartphone on Streets of Tarkov | 3.5 | 4.7 |
| Streets of Tarkov | Pyramid Scheme | Locate the first ATM inside Klimov Shopping Mall on Streets of Tarkov | 6.1 | 5.4 |
| Streets of Tarkov | Road Closed | Determine the ambush spot | 7.1 | 4.3 |
| Streets of Tarkov | The Delicious Sausage | Scout the Goshan store in Concordia | 4.3 | 5.5 |
| Streets of Tarkov | The Secret Recipe | Locate and obtain the red vial at the TerraGroup office on Streets of Tarkov | 7.4 | 4.5 |
| Streets of Tarkov | Trouble in the Big City | Launch a yellow flare near the armored convoy | 8.6 | 6.4 |
| The Lab | Beneath The Streets | Scout the hazard dome in The Lab (In one raid) | 1.1 | 3.9 |
| The Lab | Following the Bread Crumbs | Search the weapon testing area in The Lab | 1.3 | 4.0 |

## All steps

### Customs

| Task | Step | x, z | y | Above ground | Floor | Wiki floor |
|---|---|---|---|---|---|---|
| [Abandoned Cargo](https://escapefromtarkov.fandom.com/wiki/Abandoned_Cargo) | Mark any of the special TerraGroup cargo boxes with an MS2000 Marker on Customs | -184.3, -132.6 | 1.6 |  | Ground level |  |
| [Abandoned Cargo](https://escapefromtarkov.fandom.com/wiki/Abandoned_Cargo) | Mark any of the special TerraGroup cargo boxes with an MS2000 Marker on Customs | 147.9, -67.5 | 1.9 | 0.4 | Ground level |  |
| [Abandoned Cargo](https://escapefromtarkov.fandom.com/wiki/Abandoned_Cargo) | Mark any of the special TerraGroup cargo boxes with an MS2000 Marker on Customs | 60.3, -65.6 | 5.3 | 3.9 | Ground level | **2nd Floor**: Warehouse 17, cargo on the second floor |
| [Abandoned Cargo](https://escapefromtarkov.fandom.com/wiki/Abandoned_Cargo) | Mark any of the special TerraGroup cargo boxes with an MS2000 Marker on Customs | 115.6, -38.2 | 2.2 | 1.1 | Ground level |  |
| [Abandoned Cargo](https://escapefromtarkov.fandom.com/wiki/Abandoned_Cargo) | Mark any of the special TerraGroup cargo boxes with an MS2000 Marker on Customs | 103.1, -64.8 | 2.2 | 1.1 | Ground level |  |
| [Abandoned Cargo](https://escapefromtarkov.fandom.com/wiki/Abandoned_Cargo) | Mark any of the special TerraGroup cargo boxes with an MS2000 Marker on Customs | 66.6, -60.3 | 9.5 | 8.3 | 3rd Floor |  |
| [Abandoned Cargo](https://escapefromtarkov.fandom.com/wiki/Abandoned_Cargo) | Mark any of the special TerraGroup cargo boxes with an MS2000 Marker on Customs | 65.2, -47.7 | 1.9 | 0.8 | Ground level |  |
| [Abandoned Cargo](https://escapefromtarkov.fandom.com/wiki/Abandoned_Cargo) | Locate the first special TerraGroup cargo on Customs | 147.9, -67.8 | 1.9 | 0.3 | Ground level |  |
| [Abandoned Cargo](https://escapefromtarkov.fandom.com/wiki/Abandoned_Cargo) | Locate the second special TerraGroup cargo on Customs | -184.3, -132.6 | 1.6 |  | Ground level |  |
| [Abandoned Cargo](https://escapefromtarkov.fandom.com/wiki/Abandoned_Cargo) | Locate the third special TerraGroup cargo on Customs | 60.3, -66.2 | 5.3 | 3.9 | Ground level | **2nd Floor**: Warehouse 17, cargo on the second floor |
| [Abandoned Cargo](https://escapefromtarkov.fandom.com/wiki/Abandoned_Cargo) | Locate the fourth special TerraGroup cargo on Customs | 115.6, -38.5 | 2.2 | 1.1 | Ground level |  |
| [Abandoned Cargo](https://escapefromtarkov.fandom.com/wiki/Abandoned_Cargo) | Locate the fifth special TerraGroup cargo on Customs | 103.1, -65.3 | 2.2 | 1.1 | Ground level |  |
| [Abandoned Cargo](https://escapefromtarkov.fandom.com/wiki/Abandoned_Cargo) | Locate the sixth special TerraGroup cargo on Customs | 66.6, -60.3 | 9.5 | 8.3 | 3rd Floor |  |
| [Abandoned Cargo](https://escapefromtarkov.fandom.com/wiki/Abandoned_Cargo) | Locate the seventh special TerraGroup cargo on Customs | 65.1, -47.7 | 1.9 | 0.8 | Ground level |  |
| [Against the Conscience - Part 1 [PVP ZONE]](https://escapefromtarkov.fandom.com/wiki/Against_the_Conscience_-_Part_1) | Locate the old champion's room on Customs | 179.9, 164.8 | 4.0 | 3.3 | 2nd Floor |  |
| [Against the Conscience - Part 1 [PVP ZONE]](https://escapefromtarkov.fandom.com/wiki/Against_the_Conscience_-_Part_1) | Find out what happened to the champion | 182.8, 163.8 | 3.4 | 2.8 | 2nd Floor |  |
| [Background Check](https://escapefromtarkov.fandom.com/wiki/Background_Check) | Locate and obtain the bronze pocket watch on Customs | 102.3, -5.9 | 3.0 |  | Ground level |  |
| [Bad Rep Evidence](https://escapefromtarkov.fandom.com/wiki/Bad_Rep_Evidence) | Locate and obtain Secure Folder 0031 in one of the bunkhouses on Customs | 204.1, 12.4 | 4.7 | 3.6 | Ground level |  |
| [Between Two Fires [PVP ZONE]](https://escapefromtarkov.fandom.com/wiki/Between_Two_Fires) | Return to the old champion's hideout on Customs | 179.9, 164.8 | 4.0 | 3.3 | 2nd Floor |  |
| [Between Two Fires [PVP ZONE]](https://escapefromtarkov.fandom.com/wiki/Between_Two_Fires) | Locate and obtain the compromising information on Ref | 183.1, 164.0 | 2.8 | 2.2 | 2nd Floor |  |
| [Big Customer](https://escapefromtarkov.fandom.com/wiki/Big_Customer) | Locate the transport with the chemicals on Customs | 480.8, -76.7 | 3.3 | 0.6 | Ground level |  |
| [Big Customer](https://escapefromtarkov.fandom.com/wiki/Big_Customer) | Mark the vehicle with an MS2000 Marker | 480.8, -76.7 | 3.3 | 0.6 | Ground level |  |
| [Break the Deal](https://escapefromtarkov.fandom.com/wiki/Break_the_Deal) | Stash a DVL-10 sniper rifle at the specified spot on Customs | 248.6, -36.5 | 12.7 | 9.4 | 4th Floor |  |
| [Break the Deal](https://escapefromtarkov.fandom.com/wiki/Break_the_Deal) | Stash a DVL-10 magazine at the specified spot on Customs | 251.2, -21.0 | 9.4 | 6.6 | 3rd Floor |  |
| [Break the Deal](https://escapefromtarkov.fandom.com/wiki/Break_the_Deal) | Stash an ELCAN SpecterDR scope at the specified spot on Customs | 248.9, -36.7 | 5.9 | 2.5 | 2nd Floor |  |
| [Break the Deal](https://escapefromtarkov.fandom.com/wiki/Break_the_Deal) | Stash a pack of any 7.62x51 ammo at the specified spot on Customs | 255.7, -3.7 | 12.2 | 10.5 | 4th Floor |  |
| [Capturing Outposts](https://escapefromtarkov.fandom.com/wiki/Capturing_Outposts) | Eliminate PMC operatives at the specified Scav bases on Customs, Shoreline, or Woods | 202.7, -126.8 | 7.9 | 6.1 | 2nd Floor |  |
| [Chemical - Part 1](https://escapefromtarkov.fandom.com/wiki/Chemical_-_Part_1) | Locate and obtain any information about the deputy chief’s past life on Customs | 487.3, -138.6 | 5.6 |  | Ground level |  |
| [Chemical - Part 1](https://escapefromtarkov.fandom.com/wiki/Chemical_-_Part_1) | Locate and obtain any information about the deputy chief’s past life on Customs | 485.9, -140.6 | 5.6 |  | Ground level |  |
| [Chemical - Part 1](https://escapefromtarkov.fandom.com/wiki/Chemical_-_Part_1) | Locate and obtain any information about the deputy chief’s past life on Customs | 498.5, -141.5 | 5.6 |  | Ground level |  |
| [Chemical - Part 1](https://escapefromtarkov.fandom.com/wiki/Chemical_-_Part_1) | Locate the sleeping place of the former deputy chief of security on Customs | 487.9, -139.8 | 6.1 |  | Ground level |  |
| [Chemical - Part 2](https://escapefromtarkov.fandom.com/wiki/Chemical_-_Part_2) | Locate and obtain any evidence that could help with the investigation on Customs | 194.2, 171.1 | 3.7 | 3.5 | 2nd Floor |  |
| [Chemical - Part 2](https://escapefromtarkov.fandom.com/wiki/Chemical_-_Part_2) | Locate and obtain any information that could help with the investigation on Customs | 194.8, 173.1 | 4.4 | 4.0 | 2nd Floor |  |
| [Chemical - Part 4](https://escapefromtarkov.fandom.com/wiki/Chemical_-_Part_4) | Locate the transport with the chemicals on Customs | 480.8, -76.7 | 3.3 | 0.6 | Ground level |  |
| [Chemical - Part 4](https://escapefromtarkov.fandom.com/wiki/Chemical_-_Part_4) | Mark the vehicle with an MS2000 Marker | 480.8, -76.7 | 3.3 | 0.6 | Ground level |  |
| [Chemical Experiments](https://escapefromtarkov.fandom.com/wiki/Chemical_Experiments) | Stash a Corrugated hose in the med lab on Customs | 88.6, -145.8 | 5.7 | 3.9 | 2nd Floor |  |
| [Chemical Experiments](https://escapefromtarkov.fandom.com/wiki/Chemical_Experiments) | Stash a Corrugated hose in the med lab on Customs | 90.5, -156.6 | 5.7 | 4.0 | 2nd Floor |  |
| [Chumming](https://escapefromtarkov.fandom.com/wiki/Chumming) | Stash Golden neck chains in the microwave on the 3rd floor of the dorm on Customs | 170.8, 172 | 6.9 | 6.2 | 3rd Floor |  |
| [Closer to the People](https://escapefromtarkov.fandom.com/wiki/Closer_to_the_People) | Locate and obtain the delivery crew's shipment notes on Customs | 93.3, -61.9 | 1.3 | 0.2 | Ground level |  |
| [Closer to the People](https://escapefromtarkov.fandom.com/wiki/Closer_to_the_People) | Locate and obtain the delivery crew's shipment notes on Customs | 90.4, -57.5 | 2.9 | 1.6 | Ground level |  |
| [Closer to the People](https://escapefromtarkov.fandom.com/wiki/Closer_to_the_People) | Locate and obtain the delivery crew's shipment notes on Customs | 96.9, -64.5 | 1.3 | 0.2 | Ground level |  |
| [Closer to the People](https://escapefromtarkov.fandom.com/wiki/Closer_to_the_People) | Locate and obtain the delivery crew's shipment notes on Customs | 95.3, -59.0 | 1.9 | 0.8 | Ground level |  |
| [Decisions, Decisions [PVP ZONE]](https://escapefromtarkov.fandom.com/wiki/Decisions%2C_Decisions) | Locate and obtain the compromising information on Ref | 183.1, 164.0 | 2.8 | 2.2 | 2nd Floor |  |
| [Delivery From the Past](https://escapefromtarkov.fandom.com/wiki/Delivery_From_the_Past) | Locate and obtain the valuable folder in Tarcone director's office on Customs | -202.9, -102.4 | 7.7 | 5.4 | 2nd Floor |  |
| [Easy Money - Part 1 [PVP ZONE]](https://escapefromtarkov.fandom.com/wiki/Easy_Money_-_Part_1) | Plant the Arena advertisement poster in the living quarters at the Scav base on Customs | 203.2, -116.6 | 2.0 | -0.1 | Ground level |  |
| [Easy Money - Part 1 [PVP ZONE]](https://escapefromtarkov.fandom.com/wiki/Easy_Money_-_Part_1) | Plant the Arena advertisement poster in the living quarters at the Scav base on Customs | 206.8, -120.2 | 2.0 | -0.0 | Ground level |  |
| [Easy Money - Part 1 [PVP ZONE]](https://escapefromtarkov.fandom.com/wiki/Easy_Money_-_Part_1) | Plant the Arena advertisement poster in the living quarters at the Scav base on Customs | 192.3, -103.8 | 2.2 | -0.0 | Ground level |  |
| [Easy Money - Part 1 [PVP ZONE]](https://escapefromtarkov.fandom.com/wiki/Easy_Money_-_Part_1) | Plant the Arena advertisement poster in the living quarters at the Scav base on Customs | 187.2, -102.0 | 2.2 | -0.1 | Ground level |  |
| [Easy Money - Part 1 [PVP ZONE]](https://escapefromtarkov.fandom.com/wiki/Easy_Money_-_Part_1) | Plant the Arena advertisement poster in the living quarters at the Scav base on Customs | 206.9, -124.6 | 2.0 | 0.2 | Ground level |  |
| [Every Hunter Knows This](https://escapefromtarkov.fandom.com/wiki/Every_Hunter_Knows_This) | Locate a good tripwire installation spot at the three-story dorm stairs on Customs | 171.8, 160.0 | 1 | 0.5 | Ground level |  |
| [Farming](https://escapefromtarkov.fandom.com/wiki/Farming) | Obtain the package of graphics cards | -202.6, -98.4 | 7.2 | 4.9 | 2nd Floor |  |
| [Farming](https://escapefromtarkov.fandom.com/wiki/Farming) | Obtain the package of graphics cards | -201.8, -102.9 | 7.3 | 5.0 | 2nd Floor |  |
| [Farming](https://escapefromtarkov.fandom.com/wiki/Farming) | Obtain the package of graphics cards | -204.4, -98.6 | 7.3 | 5.0 | 2nd Floor |  |
| [Farming](https://escapefromtarkov.fandom.com/wiki/Farming) | Obtain the package of graphics cards | -200.8, -100.6 | 7.2 | 4.9 | 2nd Floor |  |
| [Farming](https://escapefromtarkov.fandom.com/wiki/Farming) | Locate the warehouse of seized goods on Customs | -212.6, -109.0 | 1.2 | -0.5 | Ground level |  |
| [Golden Swag](https://escapefromtarkov.fandom.com/wiki/Golden_Swag) | Locate and obtain the golden Zibbo lighter from Dorm room 303 on Customs | 180.8, 150.1 | 6.7 | 6.1 | 3rd Floor |  |
| [Golden Swag](https://escapefromtarkov.fandom.com/wiki/Golden_Swag) | Stash a regular Zibbo lighter at Dorm room 303 on Customs | 180.6, 149.3 | 6.8 | 6.1 | 3rd Floor |  |
| [Hobby Club](https://escapefromtarkov.fandom.com/wiki/Hobby_Club) | Locate and obtain the AK-50 dust cover at one of Tarkov's security checkpoints | 582.0, 5.9 | 3.9 | 4.1 | 2nd Floor |  |
| [Hobby Club](https://escapefromtarkov.fandom.com/wiki/Hobby_Club) | Locate the checkpoint with seized cargo | 584.3, 5.0 | 0.9 | 1.1 | Ground level |  |
| [Hobby Club](https://escapefromtarkov.fandom.com/wiki/Hobby_Club) | Stash the AK-50 body at the specified spot on Customs | 502.8, 91.8 | 16.0 | 3.8 | Ground level |  |
| [Hobby Club](https://escapefromtarkov.fandom.com/wiki/Hobby_Club) | Stash the AK-50 handguard at the specified spot on Customs | 502.8, 91.8 | 16.0 | 3.8 | Ground level |  |
| [Hobby Club](https://escapefromtarkov.fandom.com/wiki/Hobby_Club) | Stash the AK-50 barrel at the specified spot on Customs | 502.8, 91.8 | 16.0 | 3.8 | Ground level |  |
| [Hobby Club](https://escapefromtarkov.fandom.com/wiki/Hobby_Club) | Stash the AK-50 dust cover at the specified spot on Customs | 502.8, 91.8 | 16.0 | 3.8 | Ground level |  |
| [Hot Wheels](https://escapefromtarkov.fandom.com/wiki/Hot_Wheels) | Complete the main objective as soon as possible | 377.3, 20.9 | 0.8 | 2.2 | Ground level |  |
| [Hot Wheels](https://escapefromtarkov.fandom.com/wiki/Hot_Wheels) | Complete the main objective as soon as possible | 117.6, -85.6 | 1.8 | 2.0 | Ground level |  |
| [Hot Wheels](https://escapefromtarkov.fandom.com/wiki/Hot_Wheels) | Complete the main objective as soon as possible | 317.8, -191.2 | 1.9 | 0.7 | Ground level |  |
| [Hot Wheels](https://escapefromtarkov.fandom.com/wiki/Hot_Wheels) | Complete the main objective as soon as possible | 573.1, -90.0 | 2.0 | 0.5 | Ground level |  |
| [Hot Wheels](https://escapefromtarkov.fandom.com/wiki/Hot_Wheels) | Complete the main objective as soon as possible | 6.0, -98.7 | 1.7 | 5.7 | Ground level |  |
| [Hot Wheels](https://escapefromtarkov.fandom.com/wiki/Hot_Wheels) | Complete the main objective as soon as possible | 343.1, -158.9 | 1.9 | 0.4 | Ground level |  |
| [Hot Wheels](https://escapefromtarkov.fandom.com/wiki/Hot_Wheels) | Complete the main objective as soon as possible | 557.5, -0.9 | -0.1 | 0.3 | Ground level |  |
| [Hot Wheels](https://escapefromtarkov.fandom.com/wiki/Hot_Wheels) | Complete the main objective as soon as possible | -176.7, -209.0 | 1.9 | 0.4 | Ground level |  |
| [Hot Wheels](https://escapefromtarkov.fandom.com/wiki/Hot_Wheels) | Complete the main objective as soon as possible | -279.1, -141.9 | 1.5 |  | Ground level |  |
| [Hot Wheels](https://escapefromtarkov.fandom.com/wiki/Hot_Wheels) | Complete the main objective as soon as possible | 43.8, -157.2 | 1.7 |  | Ground level |  |
| [Hot Wheels](https://escapefromtarkov.fandom.com/wiki/Hot_Wheels) | Complete the main objective as soon as possible | 113.2, -94.7 | 2.5 | 1.3 | Ground level |  |
| [Hot Wheels](https://escapefromtarkov.fandom.com/wiki/Hot_Wheels) | Complete the main objective as soon as possible | 21.9, 96.8 | -0.5 |  | Ground level |  |
| [Hot Wheels](https://escapefromtarkov.fandom.com/wiki/Hot_Wheels) | Complete the main objective as soon as possible | 96.4, -86.8 | 1.8 | 0.7 | Ground level |  |
| [Hot Wheels](https://escapefromtarkov.fandom.com/wiki/Hot_Wheels) | Complete the main objective as soon as possible | -226.7, -89.0 | 1.5 |  | Ground level |  |
| [Hot Wheels](https://escapefromtarkov.fandom.com/wiki/Hot_Wheels) | Complete the main objective as soon as possible | 92.3, -152 | 1.7 | 0.0 | Ground level |  |
| [Hot Wheels](https://escapefromtarkov.fandom.com/wiki/Hot_Wheels) | Complete the main objective as soon as possible | 67.3, -142.8 | 1.8 | 0.3 | Ground level |  |
| [Hot Wheels](https://escapefromtarkov.fandom.com/wiki/Hot_Wheels) | Complete the main objective as soon as possible | -203.2, -188.3 | 1.5 | -0.2 | Ground level |  |
| [Hot Wheels](https://escapefromtarkov.fandom.com/wiki/Hot_Wheels) | Complete the main objective as soon as possible | -254.8, -91.3 | 1.6 | 0.5 | Ground level |  |
| [Hot Wheels](https://escapefromtarkov.fandom.com/wiki/Hot_Wheels) | Complete the main objective as soon as possible | -226.1, -91.7 | 1.6 |  | Ground level |  |
| [Is This a Reference?](https://escapefromtarkov.fandom.com/wiki/Is_This_a_Reference%3F) | Install a WI-FI Camera at the bucket-head villain on Customs | 568.4, -58.3 | 8.0 | 6.5 | 2nd Floor |  |
| [Is This a Reference?](https://escapefromtarkov.fandom.com/wiki/Is_This_a_Reference%3F) | Install a WI-FI Camera at Anvil 3-4 crew member's execution site on Customs | 568.5, -80.7 | 7.6 | 5.6 | 2nd Floor |  |
| [Is This a Reference?](https://escapefromtarkov.fandom.com/wiki/Is_This_a_Reference%3F) | Install a WI-FI Camera at every indie developer's worst nightmare on Customs | 172.4, 182.4 | 4.0 | 3.6 | 2nd Floor |  |
| [Oil Run](https://escapefromtarkov.fandom.com/wiki/Oil_Run) | Locate and mark any of the fuel tank trucks with an MS2000 Marker on Customs | 429.9, 16.2 | 2.7 | 1.6 | Ground level |  |
| [Oil Run](https://escapefromtarkov.fandom.com/wiki/Oil_Run) | Locate and mark any of the fuel tank trucks with an MS2000 Marker on Customs | 101.5, -14.1 | 3.1 |  | Ground level |  |
| [Oil Run](https://escapefromtarkov.fandom.com/wiki/Oil_Run) | Locate and mark any of the fuel tank trucks with an MS2000 Marker on Customs | 335.0, -190.0 | 3.0 | 1.9 | Ground level |  |
| [Oil Run](https://escapefromtarkov.fandom.com/wiki/Oil_Run) | Locate and mark any of the fuel tank trucks with an MS2000 Marker on Customs | -334.9, -163.5 | 2.2 | 1.9 | Ground level |  |
| [Operation Aquarius](https://escapefromtarkov.fandom.com/wiki/Operation_Aquarius) | Locate the water stockpile hidden inside one of the dorm rooms on Customs | 232.2, 138.9 | 3.4 | 3.3 | 2nd Floor |  |
| [Out of Curiosity](https://escapefromtarkov.fandom.com/wiki/Out_of_Curiosity) | Locate the transport with the chemicals on Customs | 480.8, -76.7 | 3.3 | 0.6 | Ground level |  |
| [Out of Curiosity](https://escapefromtarkov.fandom.com/wiki/Out_of_Curiosity) | Mark the vehicle with an MS2000 Marker | 480.8, -76.7 | 3.3 | 0.6 | Ground level |  |
| [Passion for Ergonomics](https://escapefromtarkov.fandom.com/wiki/Passion_for_Ergonomics) | Locate and obtain the customized tool set at the garage complex on Customs | -320.0, -178.7 | 1.1 | 0.8 | Ground level |  |
| [Passion for Ergonomics](https://escapefromtarkov.fandom.com/wiki/Passion_for_Ergonomics) | Locate and obtain the customized tool set at the garage complex on Customs | -316.4, -179.9 | 1.1 | 0.1 | Ground level |  |
| [Passion for Ergonomics](https://escapefromtarkov.fandom.com/wiki/Passion_for_Ergonomics) | Locate and obtain the customized tool set at the garage complex on Customs | -318.5, -176.0 | 1.2 | 0.8 | Ground level |  |
| [Passion for Ergonomics](https://escapefromtarkov.fandom.com/wiki/Passion_for_Ergonomics) | Locate and obtain the customized tool set at the garage complex on Customs | -316.7, -178.1 | 1.1 | 0.1 | Ground level |  |
| [Pharmacist](https://escapefromtarkov.fandom.com/wiki/Pharmacist) | Locate and obtain the suitcase with the device on Customs | 239.2, 160.6 | 0.7 | 0.6 | Ground level |  |
| [Pharmacist](https://escapefromtarkov.fandom.com/wiki/Pharmacist) | Locate the paramedic’s car on Customs | 579.4, -1.8 | 0.1 | 0.3 | Ground level |  |
| [Pharmacist](https://escapefromtarkov.fandom.com/wiki/Pharmacist) | Find a way inside the two-story dorm room 114 on Customs | 235.5, 160.1 | 0.4 | 0.3 | Ground level |  |
| [Private Club](https://escapefromtarkov.fandom.com/wiki/Private_Club) | Locate and obtain Skier's wallet on Customs | 50.0, -57.8 | 5.2 | 4.0 | Ground level | **2nd Floor**: Warehouse 17, room on the second floor |
| [Private Club](https://escapefromtarkov.fandom.com/wiki/Private_Club) | Locate and obtain Skier's wallet on Customs | 46.6, -57.8 | 5.3 | 3.9 | Ground level | **2nd Floor**: Warehouse 17, room on the second floor |
| [Private Club](https://escapefromtarkov.fandom.com/wiki/Private_Club) | Locate and obtain Skier's wallet on Customs | 46.8, -58.1 | 4.5 | 3.1 | Ground level | **2nd Floor**: Warehouse 17, room on the second floor |
| [Private Club](https://escapefromtarkov.fandom.com/wiki/Private_Club) | Locate and obtain Skier's wallet on Customs | 44.6, -58.4 | 4.4 | 2.9 | Ground level | **2nd Floor**: Warehouse 17, room on the second floor |
| [Provide Viewership](https://escapefromtarkov.fandom.com/wiki/Provide_Viewership) | Install the first WI-FI Camera inside the industrial plant on Customs | 257.0, -75.4 | 14.1 | 12.4 | 4th Floor |  |
| [Provide Viewership](https://escapefromtarkov.fandom.com/wiki/Provide_Viewership) | Install the second WI-FI Camera inside the industrial plant on Customs | 254.7, -75.2 | 2.5 | 0.8 | Ground level |  |
| [Provide Viewership](https://escapefromtarkov.fandom.com/wiki/Provide_Viewership) | Install the third WI-FI Camera inside the industrial plant on Customs | 264.0, -38.9 | 7.0 | 5.4 | 2nd Floor |  |
| [Provide Viewership](https://escapefromtarkov.fandom.com/wiki/Provide_Viewership) | Install the fourth WI-FI Camera inside the industrial plant on Customs | 278.2, -51.6 | 2.7 | 1.1 | Ground level |  |
| [Provide Viewership](https://escapefromtarkov.fandom.com/wiki/Provide_Viewership) | Eliminate any target inside the industrial plant on Customs | 267.1, -51.6 | 8.6 | 7.1 | 3rd Floor |  |
| [Rite of Passage](https://escapefromtarkov.fandom.com/wiki/Rite_of_Passage) | Eliminate Scavs at the old gas station on Customs | 307.9, -144.6 | 3.7 |  | Ground level |  |
| [Rite of Passage](https://escapefromtarkov.fandom.com/wiki/Rite_of_Passage) | Eliminate Scavs at the new gas station on Customs | 417.4, 35.9 | 9.2 | 8.1 | Ground level |  |
| [Secrets of Polikhim](https://escapefromtarkov.fandom.com/wiki/Secrets_of_Polikhim) | Locate and obtain the precision tools package in the med lab on Customs | 88.5, -142.8 | 4.7 | 3.0 | 2nd Floor |  |
| [Secrets of Polikhim](https://escapefromtarkov.fandom.com/wiki/Secrets_of_Polikhim) | Locate and obtain the precision tools package in the med lab on Customs | 92.4, -161.5 | 4.7 | 3.0 | 2nd Floor |  |
| [Secrets of Polikhim](https://escapefromtarkov.fandom.com/wiki/Secrets_of_Polikhim) | Locate and obtain the precision tools package in the med lab on Customs | 88.1, -146.9 | 5.2 | 3.5 | 2nd Floor |  |
| [Secrets of Polikhim](https://escapefromtarkov.fandom.com/wiki/Secrets_of_Polikhim) | Locate and obtain the precision tools package in the med lab on Customs | 76.3, -151.7 | 4.6 | 2.9 | 2nd Floor |  |
| [Secrets of Polikhim](https://escapefromtarkov.fandom.com/wiki/Secrets_of_Polikhim) | Locate and obtain the precision tools package in the med lab on Customs | 87.9, -162.6 | 4.7 | 3.0 | 2nd Floor |  |
| [Secrets of Polikhim](https://escapefromtarkov.fandom.com/wiki/Secrets_of_Polikhim) | Locate and obtain the precision tools package in the med lab on Customs | 81.1, -152.6 | 4.7 | 3.0 | 2nd Floor |  |
| [Shaking Up the Teller](https://escapefromtarkov.fandom.com/wiki/Shaking_Up_the_Teller) | Locate and obtain the valuable item in dorm room 203 on Customs | 178.1, 148.7 | 2.9 | 2.2 | 2nd Floor |  |
| [Shaking Up the Teller](https://escapefromtarkov.fandom.com/wiki/Shaking_Up_the_Teller) | Gain access to dorm room 214 on Customs | 176.4, 184.2 | 3.3 | 2.9 | 2nd Floor |  |
| [Shipment Tracking](https://escapefromtarkov.fandom.com/wiki/Shipment_Tracking) | Locate and obtain the TerraGroup shipment lists on Customs | 90.8, -54.6 | 7.1 | 5.8 | 3rd Floor | **2nd Floor**: director's room on the second floor of the boiler building |
| [Shipment Tracking](https://escapefromtarkov.fandom.com/wiki/Shipment_Tracking) | Locate and obtain the TerraGroup shipment lists on Customs | 89.9, -58.1 | 7.2 | 5.9 | 3rd Floor | **2nd Floor**: director's room on the second floor of the boiler building |
| [Shipment Tracking](https://escapefromtarkov.fandom.com/wiki/Shipment_Tracking) | Locate and obtain the TerraGroup shipment lists on Customs | 90.7, -56.4 | 7.7 | 6.4 | 3rd Floor | **2nd Floor**: director's room on the second floor of the boiler building |
| [Shipment Tracking](https://escapefromtarkov.fandom.com/wiki/Shipment_Tracking) | Locate and obtain the TerraGroup shipment lists on Customs | 90.3, -59.9 | 7.9 | 6.7 | 3rd Floor | **2nd Floor**: director's room on the second floor of the boiler building |
| [Supplements](https://escapefromtarkov.fandom.com/wiki/Supplements) | Locate and obtain the chemical vial on Customs | 89.0, -143.7 | 5.8 | 4.1 | 2nd Floor |  |
| [Supplements](https://escapefromtarkov.fandom.com/wiki/Supplements) | Locate and obtain the chemical vial on Customs | 91.6, -158.8 | 5.6 | 3.9 | 2nd Floor |  |
| [Surprise Gift [PVP ZONE]](https://escapefromtarkov.fandom.com/wiki/Surprise_Gift) | Return to the old champion's hideout on Customs | 179.9, 164.8 | 4.0 | 3.3 | 2nd Floor |  |
| [Surprise Gift [PVP ZONE]](https://escapefromtarkov.fandom.com/wiki/Surprise_Gift) | Locate and obtain the compromising information on Ref | 183.1, 164.0 | 2.8 | 2.2 | 2nd Floor |  |
| [The Courier](https://escapefromtarkov.fandom.com/wiki/The_Courier) | Stash a Trijicon REAP-IR scope behind the trash containers at the new gas station on Customs | 425.0, 28.4 | 2.3 | 1.0 | Ground level |  |
| [The Extortionist](https://escapefromtarkov.fandom.com/wiki/The_Extortionist) | Locate and obtain the hidden valuable cargo on Customs | 367.7, -50.6 | 1.3 | 3.7 | Ground level |  |
| [The Extortionist](https://escapefromtarkov.fandom.com/wiki/The_Extortionist) | Locate the messenger's body on Customs | 27.5, -110.2 | 1.5 | 0.4 | Ground level |  |
| [The Extortionist](https://escapefromtarkov.fandom.com/wiki/The_Extortionist) | Locate the place where the messenger hid the cargo on Customs | 368.9, -49.9 | 1.6 | 4.0 | Ground level |  |
| [The Huntsman Path - Angry Watchman](https://escapefromtarkov.fandom.com/wiki/The_Huntsman_Path_-_Angry_Watchman) | Eliminate PMC operatives in the Dorms area on Customs | 194.6, 116.4 | 5.3 |  | Ground level |  |
| [The Price of Independence](https://escapefromtarkov.fandom.com/wiki/The_Price_of_Independence) | Locate and obtain the incriminating letter on Customs | 264.3, -75.3 | 13.3 | 11.8 | 4th Floor |  |
| [The Price of Independence](https://escapefromtarkov.fandom.com/wiki/The_Price_of_Independence) | Locate and obtain the incriminating letter on Customs | 268.6, -73.8 | 12.7 | 11.2 | 4th Floor |  |
| [The Price of Independence](https://escapefromtarkov.fandom.com/wiki/The_Price_of_Independence) | Locate and obtain the incriminating letter on Customs | 271.1, -72.4 | 12.8 | 11.3 | 4th Floor |  |
| [The Price of Independence](https://escapefromtarkov.fandom.com/wiki/The_Price_of_Independence) | Locate and obtain the incriminating letter on Customs | 269.9, -77.5 | 13.4 | 11.9 | 4th Floor |  |
| [The Price of Independence](https://escapefromtarkov.fandom.com/wiki/The_Price_of_Independence) | Locate and obtain the incriminating letter on Customs | 264.0, -76.9 | 14.1 | 12.6 | 4th Floor |  |
| [The Price of Independence](https://escapefromtarkov.fandom.com/wiki/The_Price_of_Independence) | Locate and obtain the incriminating letter on Customs | 264.3, -75.3 | 13.3 | 11.8 | 4th Floor |  |
| [The Price of Independence](https://escapefromtarkov.fandom.com/wiki/The_Price_of_Independence) | Locate and obtain the incriminating letter on Customs | 268.6, -73.8 | 12.7 | 11.2 | 4th Floor |  |
| [The Price of Independence](https://escapefromtarkov.fandom.com/wiki/The_Price_of_Independence) | Locate and obtain the incriminating letter on Customs | 271.1, -72.4 | 12.8 | 11.3 | 4th Floor |  |
| [The Price of Independence](https://escapefromtarkov.fandom.com/wiki/The_Price_of_Independence) | Locate and obtain the incriminating letter on Customs | 269.9, -77.5 | 13.4 | 11.9 | 4th Floor |  |
| [The Price of Independence](https://escapefromtarkov.fandom.com/wiki/The_Price_of_Independence) | Locate and obtain the incriminating letter on Customs | 264.0, -76.9 | 14.1 | 12.6 | 4th Floor |  |
| [Thirsty - Delivery](https://escapefromtarkov.fandom.com/wiki/Thirsty_-_Delivery) | Locate the specified stash spot on Customs | 11.7, 35.6 | -0.7 | 0.2 | Ground level |  |
| [Thirsty - Delivery](https://escapefromtarkov.fandom.com/wiki/Thirsty_-_Delivery) | Stash the second Propane tank (5L) | 11.7, 35.6 | -0.7 | 0.2 | Ground level |  |
| [Tigr Safari](https://escapefromtarkov.fandom.com/wiki/Tigr_Safari) | Locate and mark any UN Tigr vehicle with an MS2000 Marker on Customs | 505.0, -11.3 | 1.2 |  | Ground level |  |
| [Tigr Safari](https://escapefromtarkov.fandom.com/wiki/Tigr_Safari) | Locate and mark any UN Tigr vehicle with an MS2000 Marker on Customs | 17.9, 0.4 | 0.3 |  | Ground level |  |
| [Tigr Safari](https://escapefromtarkov.fandom.com/wiki/Tigr_Safari) | Locate and mark any UN Tigr vehicle with an MS2000 Marker on Customs | 565.8, -24.2 | -0.0 | 1.5 | Ground level |  |
| [Work Smarter](https://escapefromtarkov.fandom.com/wiki/Work_Smarter) | Locate the secret exfil on Customs | -41.5, 122.7 | -12.6 |  | Ground level |  |
| [Work Smarter](https://escapefromtarkov.fandom.com/wiki/Work_Smarter) | Locate the secret exfil on Customs | 463.2, -112.4 | -1.5 | 1.1 | Underground |  |
| [Work Smarter](https://escapefromtarkov.fandom.com/wiki/Work_Smarter) | Locate the secret exfil on Customs | 462.5, -112.2 | -1.5 | 1.1 | Underground |  |

### Factory

| Task | Step | x, z | y | Above ground | Floor | Wiki floor |
|---|---|---|---|---|---|---|
| [All Is Revealed](https://escapefromtarkov.fandom.com/wiki/All_Is_Revealed) | Take a sample of the chemicals from the damaged tank container on Factory | -5.1, 18.6 | -2.7 | -0.1 | Tunnels |  |
| [Bad Rep Evidence](https://escapefromtarkov.fandom.com/wiki/Bad_Rep_Evidence) | Gain access to the locked room in the office hallway on the third floor on Factory | 30.1, 38.9 | 8.7 | 8.6 | 3rd Floor |  |
| [Black Swan](https://escapefromtarkov.fandom.com/wiki/Black_Swan) | Locate and mark any of the heat exchangers with an MS2000 Marker on Factory | -17.0, 34.8 | -1.6 | 1.0 | Tunnels |  |
| [Black Swan](https://escapefromtarkov.fandom.com/wiki/Black_Swan) | Locate and mark any of the heat exchangers with an MS2000 Marker on Factory | 34.4, -4.5 | -1.5 | 1.2 | Tunnels |  |
| [Black Swan](https://escapefromtarkov.fandom.com/wiki/Black_Swan) | Locate and mark any of the heat exchangers with an MS2000 Marker on Factory | 34.4, -4.4 | -1.5 | 1.2 | Tunnels |  |
| [Black Swan](https://escapefromtarkov.fandom.com/wiki/Black_Swan) | Locate and mark any of the heat exchangers with an MS2000 Marker on Factory | 45.6, -36.1 | -1.6 | 0.7 | Tunnels |  |
| [Chemical - Part 3](https://escapefromtarkov.fandom.com/wiki/Chemical_-_Part_3) | Locate and obtain the chemical syringe on Factory | 26.3, 36.8 | 9.0 | 8.8 | 3rd Floor |  |
| [Chemical - Part 3](https://escapefromtarkov.fandom.com/wiki/Chemical_-_Part_3) | Locate and obtain the chemical syringe on Factory | 25.6, 38.5 | 8.1 | 8.0 | 3rd Floor |  |
| [Chemical - Part 3](https://escapefromtarkov.fandom.com/wiki/Chemical_-_Part_3) | Locate and obtain the chemical syringe on Factory | 23.2, 39.4 | 8.5 | 8.4 | 3rd Floor |  |
| [Claustrophobia](https://escapefromtarkov.fandom.com/wiki/Claustrophobia) | Eliminate any target in basement tunnel network on Factory | 19.8, 3.3 | -2.6 | 0.1 | Tunnels |  |
| [Claustrophobia](https://escapefromtarkov.fandom.com/wiki/Claustrophobia) | Eliminate any target in basement tunnel network on Factory | -51.1, 13.6 | -3.0 | -3.3 | Tunnels |  |
| [Claustrophobia](https://escapefromtarkov.fandom.com/wiki/Claustrophobia) | Eliminate any target in basement tunnel network on Factory | 19.8, -28.6 | -3.0 | -0.3 | Tunnels |  |
| [Claustrophobia](https://escapefromtarkov.fandom.com/wiki/Claustrophobia) | Eliminate any target in basement tunnel network on Factory | 65.0, 13.6 | -3.0 | -0.4 | Tunnels |  |
| [Claustrophobia](https://escapefromtarkov.fandom.com/wiki/Claustrophobia) | Eliminate any target in basement tunnel network on Factory | 19.8, 46.8 | -2.6 | -0.3 | Tunnels |  |
| [Delivery From the Past](https://escapefromtarkov.fandom.com/wiki/Delivery_From_the_Past) | Stash the package in the break room on the 2nd floor near Gate 3 on Factory | 41.7, 40.8 | 5.5 | 5.3 | 2nd Floor |  |
| [Delivery From the Past](https://escapefromtarkov.fandom.com/wiki/Delivery_From_the_Past) | Stash the package in the break room on the 2nd floor near Gate 3 on Factory | 41.7, 40.8 | 5.4 | 5.3 | 2nd Floor |  |
| [Dragnet](https://escapefromtarkov.fandom.com/wiki/Dragnet) | Locate and obtain the chemical container at the TerraGroup warehouse on Factory | -22.7, 48.7 | -1.9 | 0.6 | Tunnels |  |
| [Dragnet](https://escapefromtarkov.fandom.com/wiki/Dragnet) | Locate and obtain the chemical container at the TerraGroup warehouse on Factory | -18.4, 46.7 | -2.0 | 0.7 | Tunnels |  |
| [Dragnet](https://escapefromtarkov.fandom.com/wiki/Dragnet) | Locate and obtain the chemical container at the TerraGroup warehouse on Factory | -23.3, 44.8 | -1.9 | 0.4 | Tunnels |  |
| [Dragnet](https://escapefromtarkov.fandom.com/wiki/Dragnet) | Locate and obtain the chemical container at the TerraGroup warehouse on Factory | -21.7, 44.4 | -2.1 | 0.4 | Tunnels |  |
| [Every Hunter Knows This](https://escapefromtarkov.fandom.com/wiki/Every_Hunter_Knows_This) | Locate a good tripwire installation spot in the breach room on Factory | 24.5, 38.7 | 9.3 | 9.2 | 3rd Floor |  |
| [Every Hunter Knows This](https://escapefromtarkov.fandom.com/wiki/Every_Hunter_Knows_This) | Locate a good tripwire installation spot in the breach room on Factory | 25.4, 39.2 | 8.8 | 8.6 | 3rd Floor |  |
| [Health Care Privacy - Part 5](https://escapefromtarkov.fandom.com/wiki/Health_Care_Privacy_-_Part_5) | Locate the drop spot on night-time Factory | 24.6, 39.1 | 9.2 | 9.1 | 3rd Floor |  |
| [Health Care Privacy - Part 5](https://escapefromtarkov.fandom.com/wiki/Health_Care_Privacy_-_Part_5) | Stash any Gunpowder in the designated spot | 24.6, 39.1 | 9.2 | 9.1 | 3rd Floor |  |
| [Health Care Privacy - Part 6](https://escapefromtarkov.fandom.com/wiki/Health_Care_Privacy_-_Part_6) | Locate the dead worker and take their blood sample on Factory | -19.5, -52.2 | 0.5 | 2.9 | Ground level |  |
| [Is This a Reference?](https://escapefromtarkov.fandom.com/wiki/Is_This_a_Reference%3F) | Install a WI-FI Camera in the room where the firefighter burned the books to become happy on Factory | 16.4, 42.8 | 1.8 | 4.1 | Ground level |  |
| [Is This a Reference?](https://escapefromtarkov.fandom.com/wiki/Is_This_a_Reference%3F) | Install a WI-FI Camera in the room where the firefighter burned the books to become happy on Factory | 17.4, 43.0 | 1.8 | 4.1 | Ground level |  |
| [Is This a Reference?](https://escapefromtarkov.fandom.com/wiki/Is_This_a_Reference%3F) | Install a WI-FI Camera at the place where some valve technicians couldn't finish their third project on Factory | 21, 12.1 | -1.6 | -0.3 | Tunnels |  |
| [Is This a Reference?](https://escapefromtarkov.fandom.com/wiki/Is_This_a_Reference%3F) | Install a WI-FI Camera at the place where some valve technicians couldn't finish their third project on Factory | 21.4, 11.7 | -1.9 | -0.6 | Tunnels |  |
| [Is This a Reference?](https://escapefromtarkov.fandom.com/wiki/Is_This_a_Reference%3F) | Install a WI-FI Camera at the dangerous Russian chocolate beauty on Factory | -49.4, 60.4 | 2.7 | 1.6 | Ground level |  |
| [Is This a Reference?](https://escapefromtarkov.fandom.com/wiki/Is_This_a_Reference%3F) | Install a WI-FI Camera at the dangerous Russian chocolate beauty on Factory | -49.6, 60.4 | 2.3 | 1.3 | Ground level |  |
| [Is This a Reference?](https://escapefromtarkov.fandom.com/wiki/Is_This_a_Reference%3F) | Install a WI-FI Camera in the conspiracy theorist's room on Factory | 27.6, 38.6 | 9.5 | 9.3 | 3rd Floor |  |
| [Is This a Reference?](https://escapefromtarkov.fandom.com/wiki/Is_This_a_Reference%3F) | Install a WI-FI Camera in the conspiracy theorist's room on Factory | 27.4, 38.4 | 9.2 | 9.1 | 3rd Floor |  |
| [Is This a Reference?](https://escapefromtarkov.fandom.com/wiki/Is_This_a_Reference%3F) | Install a WI-FI Camera near where someone thought he'd get transported to the magic school on Factory | 52.7, -17.2 | 1.4 | 4.1 | Ground level |  |
| [Is This a Reference?](https://escapefromtarkov.fandom.com/wiki/Is_This_a_Reference%3F) | Install a WI-FI Camera near where someone thought he'd get transported to the magic school on Factory | 52.4, -17.5 | 1.9 | 4.5 | Ground level |  |
| [Is This a Reference?](https://escapefromtarkov.fandom.com/wiki/Is_This_a_Reference%3F) | Install a WI-FI Camera at the mother of all strategy games on Factory | 30.4, -31 | 4.5 | 7.1 | 2nd Floor |  |
| [Is This a Reference?](https://escapefromtarkov.fandom.com/wiki/Is_This_a_Reference%3F) | Install a WI-FI Camera at the mother of all strategy games on Factory | 30.7, -31.1 | 4.3 | 6.9 | 2nd Floor |  |
| [Is This a Reference?](https://escapefromtarkov.fandom.com/wiki/Is_This_a_Reference%3F) | Install a WI-FI Camera at the stairway to the skies on Factory | 59.8, 50.3 | 1.2 | 1.0 | Ground level |  |
| [Is This a Reference?](https://escapefromtarkov.fandom.com/wiki/Is_This_a_Reference%3F) | Install a WI-FI Camera at the stairway to the skies on Factory | 59.6, 50.5 | 0.7 | 0.4 | Ground level |  |
| [One Less Loose End](https://escapefromtarkov.fandom.com/wiki/One_Less_Loose_End) | Locate and obtain the lab journal on Factory | 29.0, -17.6 | 3.7 | 6.4 | 2nd Floor |  |
| [One Less Loose End](https://escapefromtarkov.fandom.com/wiki/One_Less_Loose_End) | Locate and obtain the lab journal on Factory | 29.3, -31.7 | 3.7 | 6.4 | 2nd Floor |  |
| [One Less Loose End](https://escapefromtarkov.fandom.com/wiki/One_Less_Loose_End) | Locate and obtain the lab journal on Factory | 26.6, -36.0 | 4.5 | 7.2 | 2nd Floor |  |
| [One Less Loose End](https://escapefromtarkov.fandom.com/wiki/One_Less_Loose_End) | Locate and obtain the lab journal on Factory | 25.8, -19.1 | 4.4 | 7.1 | 2nd Floor |  |
| [One Less Loose End](https://escapefromtarkov.fandom.com/wiki/One_Less_Loose_End) | Locate and obtain the lab journal on Factory | 29.3, -28.9 | 3.7 | 6.4 | 2nd Floor |  |
| [Playing the Market](https://escapefromtarkov.fandom.com/wiki/Playing_the_Market) | Fix the first control board with a Toolset on Factory | 68.2, -7.4 | 1.1 | 3.7 | Ground level |  |
| [Playing the Market](https://escapefromtarkov.fandom.com/wiki/Playing_the_Market) | Fix the second control board with a Toolset on Factory | 60.1, -48.4 | 1.1 | 3.4 | Ground level |  |
| [Possessor](https://escapefromtarkov.fandom.com/wiki/Possessor) | Locate and obtain the helicopter logbook on Factory | 26.2, -3.6 | 7.9 | 10.5 | 3rd Floor |  |
| [Postman Pat - Part 1](https://escapefromtarkov.fandom.com/wiki/Postman_Pat_-_Part_1) | Locate the dead messenger and obtain his letter on Factory | -20.0, 21.9 | 0.0 | 2.6 | Ground level |  |
| [Proper Comeback](https://escapefromtarkov.fandom.com/wiki/Proper_Comeback) | Stash a Golden rooster figurine at Prapor's WI-FI Camera on Factory | 34.8, 35.5 | 8.5 | 8.4 | 3rd Floor |  |
| [Sanitary Standards](https://escapefromtarkov.fandom.com/wiki/Sanitary_Standards) | Stash a Gas analyzer in the med lab on Daytime Factory | 27.7, -31.9 | 4.5 | 7.2 | 2nd Floor |  |
| [Sanitary Standards](https://escapefromtarkov.fandom.com/wiki/Sanitary_Standards) | Locate the room with gas analyzers on Factory | 40.3, -11.6 | 1.1 | 3.7 | Ground level |  |
| [Scout](https://escapefromtarkov.fandom.com/wiki/Scout) | Locate the first Factory extraction | 66.7, -28.9 | -1.7 | 0.6 | Tunnels |  |
| [Scout](https://escapefromtarkov.fandom.com/wiki/Scout) | Locate the second Factory extraction | -53.1, 58.2 | 2.3 | 1.2 | Ground level |  |
| [Scout](https://escapefromtarkov.fandom.com/wiki/Scout) | Locate the third Factory extraction | 59.7, 57.0 | 1.2 | 0.9 | Ground level |  |
| [Scout](https://escapefromtarkov.fandom.com/wiki/Scout) | Locate the fourth Factory extraction | -18.4, -49.0 | 1.2 | 3.9 | Ground level |  |
| [Secrets of Polikhim](https://escapefromtarkov.fandom.com/wiki/Secrets_of_Polikhim) | Stash the package at the laboratory storage room on Factory | 28.1, -34.4 | 1.1 | 3.8 | Ground level |  |
| [Secrets of Polikhim](https://escapefromtarkov.fandom.com/wiki/Secrets_of_Polikhim) | Stash the package at the laboratory storage room on Factory | 27.9, -32.9 | 1.1 | 3.7 | Ground level |  |
| [The Walls Have Eyes](https://escapefromtarkov.fandom.com/wiki/The_Walls_Have_Eyes) | Install a WI-FI Camera in the first crane's cockpit on Factory | 63.6, 35.1 | 6.4 | 6.2 | 3rd Floor |  |
| [The Walls Have Eyes](https://escapefromtarkov.fandom.com/wiki/The_Walls_Have_Eyes) | Install a WI-FI Camera in the second crane's cockpit on Factory | -5.5, -32.5 | 5.8 | 9.3 | 2nd Floor |  |
| [The Walls Have Eyes](https://escapefromtarkov.fandom.com/wiki/The_Walls_Have_Eyes) | Install a WI-FI Camera in the third crane's cockpit on Factory | -24.4, 60.4 | 6.2 | 8.4 | 3rd Floor |  |
| [Viewer](https://escapefromtarkov.fandom.com/wiki/Viewer) | Install a WI-FI Camera at the office corridor on Factory | 36.9, 35.5 | 9.4 | 9.3 | 3rd Floor |  |
| [Vitamins](https://escapefromtarkov.fandom.com/wiki/Vitamins) | Locate and obtain the chemical container on Factory | 29.3, -21.5 | 4.5 | 7.1 | 2nd Floor |  |

### Ground Zero

| Task | Step | x, z | y | Above ground | Floor | Wiki floor |
|---|---|---|---|---|---|---|
| [Create a Distraction - Part 1 [PVP ZONE]](https://escapefromtarkov.fandom.com/wiki/Create_a_Distraction_-_Part_1) | Plant TP-200 TNT bricks on the second floor of the cafe on Ground Zero | 107.5, 148.1 | 29.1 | 10.5 | 2nd Floor |  |
| [First in Line](https://escapefromtarkov.fandom.com/wiki/First_in_Line) | Locate the Emercom station on Ground Zero | 156.2, -83.6 | 25.5 | 2.9 | Ground level |  |
| [Is This a Reference?](https://escapefromtarkov.fandom.com/wiki/Is_This_a_Reference%3F) | Install a WI-FI Camera at the high rise where one die-hard guy kicked ass on Ground Zero | 4.6, 337.2 | 23.9 | 6.6 | Ground level |  |
| [Is This a Reference?](https://escapefromtarkov.fandom.com/wiki/Is_This_a_Reference%3F) | Install a WI-FI Camera at the high rise where one die-hard guy kicked ass on Ground Zero | 4.0, 336.3 | 24.3 | 7.0 | Ground level |  |
| [Is This a Reference?](https://escapefromtarkov.fandom.com/wiki/Is_This_a_Reference%3F) | Install a WI-FI Camera at the computer with a joke for programmers on Ground Zero | 118.7, 190.3 | 24.2 | 1.0 | Ground level |  |
| [Is This a Reference?](https://escapefromtarkov.fandom.com/wiki/Is_This_a_Reference%3F) | Install a WI-FI Camera at the computer with a joke for programmers on Ground Zero | 118.7, 190.6 | 24.5 | 1.3 | Ground level |  |
| [Is This a Reference?](https://escapefromtarkov.fandom.com/wiki/Is_This_a_Reference%3F) | Install a WI-FI Camera at the little chair surrounded by big black chairs on Ground Zero | 41.1, 140.8 | 31.4 | 7.9 | 2nd Floor | **3rd Floor**: Tarbank conference room on the third floor |
| [Is This a Reference?](https://escapefromtarkov.fandom.com/wiki/Is_This_a_Reference%3F) | Install a WI-FI Camera at the little chair surrounded by big black chairs on Ground Zero | 40.4, 140.7 | 31.7 | 8.2 | 2nd Floor | **3rd Floor**: Tarbank conference room on the third floor |
| [Luxurious Life](https://escapefromtarkov.fandom.com/wiki/Luxurious_Life) | Locate the liquor store on Ground Zero | 117.1, 26.9 | 24.2 | 11.6 | Ground level |  |
| [Luxurious Life](https://escapefromtarkov.fandom.com/wiki/Luxurious_Life) | Locate and obtain the wine bottle in the store | 130.3, 23.7 | 23.7 | 0.6 | Ground level |  |
| [Luxurious Life](https://escapefromtarkov.fandom.com/wiki/Luxurious_Life) | Locate and obtain the wine bottle in the store | 119.7, 22.9 | 23.7 | 1.0 | Ground level |  |
| [Luxurious Life](https://escapefromtarkov.fandom.com/wiki/Luxurious_Life) | Locate and obtain the wine bottle in the store | 129.7, 25.2 | 23.3 | 0.3 | Ground level |  |
| [Luxurious Life](https://escapefromtarkov.fandom.com/wiki/Luxurious_Life) | Locate and obtain the wine bottle in the store | 128.2, 25.1 | 24.1 | 1.0 | Ground level |  |
| [Luxurious Life](https://escapefromtarkov.fandom.com/wiki/Luxurious_Life) | Locate and obtain the wine bottle in the store | 126.0, 26.2 | 23.7 | 0.7 | Ground level |  |
| [Luxurious Life](https://escapefromtarkov.fandom.com/wiki/Luxurious_Life) | Locate and obtain the wine bottle in the store | 114.0, 27.8 | 24.2 | 11.3 | Ground level |  |
| [Needle in a Haystack](https://escapefromtarkov.fandom.com/wiki/Needle_in_a_Haystack) | Investigate the courtyard park by TerraGroup HQ on Ground Zero | -15.4, 68.9 | 23.8 | -5.9 | Ground level |  |
| [Needle in a Haystack](https://escapefromtarkov.fandom.com/wiki/Needle_in_a_Haystack) | Investigate the courtyard park by TerraGroup HQ on Ground Zero | 18.5, 41.0 | 23.8 |  | Ground level |  |
| [New Paths](https://escapefromtarkov.fandom.com/wiki/New_Paths) | Scout the intersection of Mira Ave and the overpass on Ground Zero (In one raid) | 172.4, 64.7 | 17.3 | 0.9 | Ground level |  |
| [New Paths](https://escapefromtarkov.fandom.com/wiki/New_Paths) | Scout the intersection of Mira Ave and the overpass on Ground Zero (In one raid) | 205.4, 36.8 | 17.3 | 1.3 | Ground level |  |
| [New Paths](https://escapefromtarkov.fandom.com/wiki/New_Paths) | Locate the passage leading to Streets of Tarkov on Ground Zero (In one raid) | 222.8, 65.7 | 16.0 |  | Ground level |  |
| [New Paths](https://escapefromtarkov.fandom.com/wiki/New_Paths) | Locate the passage leading to Streets of Tarkov on Ground Zero (In one raid) | 227.4, 66.5 | 17.0 |  | Ground level |  |
| [Rough Tarkov](https://escapefromtarkov.fandom.com/wiki/Rough_Tarkov) | Locate the Claymore mine on Ground Zero | 60.4, 170.9 | 23.7 | 9.5 | Ground level |  |
| [Rough Tarkov](https://escapefromtarkov.fandom.com/wiki/Rough_Tarkov) | Locate the Claymore mine on Ground Zero | 59.5, 172.8 | 24.3 | 10.3 | Ground level |  |
| [Saving the Mole](https://escapefromtarkov.fandom.com/wiki/Saving_the_Mole) | Access the lab scientist's office on Ground Zero | -13.5, 51.3 | 31.0 | 5.0 | 2nd Floor |  |
| [Saving the Mole](https://escapefromtarkov.fandom.com/wiki/Saving_the_Mole) | Locate the USEC group at the parking lot of the TerraGroup complex | -21.0, -25.1 | 24.2 | 0.4 | Ground level |  |
| [Saving the Mole](https://escapefromtarkov.fandom.com/wiki/Saving_the_Mole) | Locate the lab scientist in the TerraGroup complex | -60.5, 27.4 | 25.6 | 1.4 | Ground level |  |
| [Saving the Mole](https://escapefromtarkov.fandom.com/wiki/Saving_the_Mole) | Locate and obtain the scientist's hard drive | -12.4, 49.0 | 30.7 | 5.4 | 2nd Floor |  |
| [Saving the Mole](https://escapefromtarkov.fandom.com/wiki/Saving_the_Mole) | Locate and obtain the scientist's hard drive | -11.9, 49.6 | 30.2 | 4.9 | 2nd Floor |  |
| [Saving the Mole](https://escapefromtarkov.fandom.com/wiki/Saving_the_Mole) | Locate and obtain the scientist's hard drive | -12.1, 48.0 | 30.7 | 5.5 | 2nd Floor |  |
| [Saving the Mole](https://escapefromtarkov.fandom.com/wiki/Saving_the_Mole) | Locate and obtain the scientist's hard drive | -12.3, 49.0 | 30.7 | 5.4 | 2nd Floor |  |
| [Shady Contractor](https://escapefromtarkov.fandom.com/wiki/Shady_Contractor) | Locate the Knossos LLC senior manager's car on Ground Zero | 55.3, 252.8 | 23.8 | 0.9 | Ground level |  |
| [Shady Contractor](https://escapefromtarkov.fandom.com/wiki/Shady_Contractor) | Locate the Knossos LLC senior manager's car on Ground Zero | 89.2, 224.9 | 23.8 | 1.2 | Ground level |  |
| [Shady Contractor](https://escapefromtarkov.fandom.com/wiki/Shady_Contractor) | Locate and obtain the manager's diary | 89.4, 225.0 | 23.6 | 1.0 | Ground level |  |
| [Shady Contractor](https://escapefromtarkov.fandom.com/wiki/Shady_Contractor) | Locate and obtain the manager's diary | 86.8, 226.1 | 23.1 | 0.3 | Ground level |  |
| [Shady Contractor](https://escapefromtarkov.fandom.com/wiki/Shady_Contractor) | Locate and obtain the manager's diary | 89.0, 225.3 | 23.2 | 0.5 | Ground level |  |
| [Shooting Cans](https://escapefromtarkov.fandom.com/wiki/Shooting_Cans) | Locate the Utyos machine gun on Ground Zero | 56.6, 130.6 | 32.3 | 10.3 | 3rd Floor |  |
| [Shooting Cans](https://escapefromtarkov.fandom.com/wiki/Shooting_Cans) | Locate the AGS grenade launcher on Ground Zero | 101.0, 276.4 | 34.2 | 10.7 | 3rd Floor |  |
| [The Tarkov Butcher](https://escapefromtarkov.fandom.com/wiki/The_Tarkov_Butcher) | Locate and obtain the chemical container on Ground Zero | 78.6, 100.9 | 16.4 | 2.2 | Garage |  |
| [The Tarkov Butcher](https://escapefromtarkov.fandom.com/wiki/The_Tarkov_Butcher) | Locate and obtain the chemical container on Ground Zero | 78.9, 96.3 | 15.8 | 1.6 | Garage |  |
| [The Tarkov Butcher](https://escapefromtarkov.fandom.com/wiki/The_Tarkov_Butcher) | Locate and obtain the chemical container on Ground Zero | 80.1, 96.3 | 15.8 | 1.7 | Garage |  |

### Icebreaker

| Task | Step | x, z | y | Above ground | Floor | Wiki floor |
|---|---|---|---|---|---|---|
| [Peaceful Atom](https://escapefromtarkov.fandom.com/wiki/Peaceful_Atom) | Locate and obtain the nuclear power unit control log on Icebreaker | 3.6, 26.8 | 16.4 | -0.2 | Storage/Security |  |
| [Peaceful Atom](https://escapefromtarkov.fandom.com/wiki/Peaceful_Atom) | Locate and obtain the nuclear power unit control log on Icebreaker | 8.0, -18.0 | 11.3 | 1.0 | Fuel Pumps (lower) |  |
| [Peaceful Atom](https://escapefromtarkov.fandom.com/wiki/Peaceful_Atom) | Locate and obtain the nuclear power unit control log on Icebreaker | 4.8, -17.6 | 8.6 | -1.7 | Engine Room (upper) |  |

### Interchange

| Task | Step | x, z | y | Above ground | Floor | Wiki floor |
|---|---|---|---|---|---|---|
| [A Big Loss](https://escapefromtarkov.fandom.com/wiki/A_Big_Loss) | Locate and obtain the OLI cargo route documents on Interchange | 86.6, 120.9 | 28.1 | 0.9 | 2nd Floor |  |
| [Big Sale](https://escapefromtarkov.fandom.com/wiki/Big_Sale) | Locate the AVOKADO store on Interchange | -33.2, 25.8 | 28.6 | 7.1 | 2nd Floor |  |
| [Big Sale](https://escapefromtarkov.fandom.com/wiki/Big_Sale) | Locate the KOSTIN store on Interchange | -24.7, -103.5 | 28.6 | 0.8 | 2nd Floor |  |
| [Big Sale](https://escapefromtarkov.fandom.com/wiki/Big_Sale) | Locate the tRend store on Interchange | 64.2, -155.4 | 28.1 | 6.0 | 2nd Floor |  |
| [Big Sale](https://escapefromtarkov.fandom.com/wiki/Big_Sale) | Locate the DINO CLOTHES store on Interchange | 94.4, -120.6 | 28.2 | 6.6 | 2nd Floor |  |
| [Big Sale](https://escapefromtarkov.fandom.com/wiki/Big_Sale) | Locate the TOP BRAND store on Interchange | 94.2, 10.2 | 28.2 | 5.4 | 2nd Floor |  |
| [Fuel Crisis](https://escapefromtarkov.fandom.com/wiki/Fuel_Crisis) | Locate and mark any fuel tank near the power station with an MS2000 Marker on Interchange | -208.4, -74.4 | 22.8 | 2.3 | Ground level |  |
| [Fuel Crisis](https://escapefromtarkov.fandom.com/wiki/Fuel_Crisis) | Locate and mark any fuel tank near the power station with an MS2000 Marker on Interchange | -172.6, -359.5 | 22.8 | 1.5 | Ground level |  |
| [Fuel Crisis](https://escapefromtarkov.fandom.com/wiki/Fuel_Crisis) | Locate and mark any fuel tank in the northern territory with an MS2000 Marker on Interchange | 429.1, 125.0 | 28.7 | 1.4 | Ground level |  |
| [Fuel Crisis](https://escapefromtarkov.fandom.com/wiki/Fuel_Crisis) | Locate and mark any fuel tank in the northern territory with an MS2000 Marker on Interchange | 40.7, 308.3 | 23.2 | 2.0 | Ground level |  |
| [Hot Delivery](https://escapefromtarkov.fandom.com/wiki/Hot_Delivery) | Stash a ComTac II headset in the specified place on Interchange | -50.4, 25.1 | 27.7 | 6.0 | 2nd Floor |  |
| [Hot Delivery](https://escapefromtarkov.fandom.com/wiki/Hot_Delivery) | Stash a 6B47 helmet (Olive Drab) in the specified place on Interchange | -50.4, 25.1 | 27.7 | 6.0 | 2nd Floor |  |
| [Hot Delivery](https://escapefromtarkov.fandom.com/wiki/Hot_Delivery) | Stash a Gzhel-K body armor in the specified place on Interchange | 179.9, -40.9 | 22.3 |  | Ground level |  |
| [Informed Means Armed](https://escapefromtarkov.fandom.com/wiki/Informed_Means_Armed) | Install a WI-FI Camera to watch the Kiba Arms store entrance on Interchange | 8.1, -36.7 | 27.6 | 5.3 | 2nd Floor |  |
| [Inventory Files](https://escapefromtarkov.fandom.com/wiki/Inventory_Files) | Locate and obtain the Goshan cargo manifests on Interchange | -76.5, -157.7 | 28.0 | 6.3 | 2nd Floor |  |
| [Inventory Files](https://escapefromtarkov.fandom.com/wiki/Inventory_Files) | Locate and obtain the OLI cargo manifests on Interchange | 38.0, 147.1 | 28.0 | 0.7 | 2nd Floor |  |
| [Inventory Files](https://escapefromtarkov.fandom.com/wiki/Inventory_Files) | Locate and obtain the IDEA cargo manifests on Interchange | -2.0, -292.9 | 28.0 | 0.6 | 2nd Floor |  |
| [Irresistible](https://escapefromtarkov.fandom.com/wiki/Irresistible) | Locate and obtain the lost weapon crate on Interchange | 138.0, 268.1 | 24.1 | 2.6 | Ground level |  |
| [Minibus](https://escapefromtarkov.fandom.com/wiki/Minibus) | Locate and mark the first yellow minibus with an MS2000 Marker on Interchange | 109.9, 288.8 | 22.3 |  | Ground level |  |
| [Minibus](https://escapefromtarkov.fandom.com/wiki/Minibus) | Locate and mark the second yellow minibus with an MS2000 Marker on Interchange | 17.6, -25.5 | 22.8 | 0.3 | Ground level |  |
| [Minibus](https://escapefromtarkov.fandom.com/wiki/Minibus) | Locate and mark the third yellow minibus with an MS2000 Marker on Interchange | -49.8, 59.0 | 22.9 | 1.1 | Ground level |  |
| [Minute of Fame](https://escapefromtarkov.fandom.com/wiki/Minute_of_Fame) | Locate and obtain the special edition of the gaming magazine on Interchange | 8.7, -18.5 | 37.3 | 10.0 | 3rd Floor |  |
| [Minute of Fame](https://escapefromtarkov.fandom.com/wiki/Minute_of_Fame) | Locate and obtain the special edition of the gaming magazine on Interchange | 26.2, 0.7 | 37.2 | 10.0 | 3rd Floor |  |
| [Minute of Fame](https://escapefromtarkov.fandom.com/wiki/Minute_of_Fame) | Locate and obtain the special edition of the gaming magazine on Interchange | 18.4, -3.7 | 36.6 | 15.2 | 3rd Floor |  |
| [Minute of Fame](https://escapefromtarkov.fandom.com/wiki/Minute_of_Fame) | Locate and obtain the special edition of the gaming magazine on Interchange | 19.5, -12.6 | 36.6 | 9.2 | 3rd Floor |  |
| [Minute of Fame](https://escapefromtarkov.fandom.com/wiki/Minute_of_Fame) | Locate and obtain the special edition of the gaming magazine on Interchange | 16.3, -12.5 | 36.9 | 15.2 | 3rd Floor |  |
| [Minute of Fame](https://escapefromtarkov.fandom.com/wiki/Minute_of_Fame) | Locate and obtain the special edition of the gaming magazine on Interchange | 14.6, -4.8 | 38.5 | 17.0 | 3rd Floor |  |
| [Minute of Fame](https://escapefromtarkov.fandom.com/wiki/Minute_of_Fame) | Locate and obtain the special edition of the gaming magazine on Interchange | 14.3, -2.5 | 37.8 | 16.4 | 3rd Floor |  |
| [Minute of Fame](https://escapefromtarkov.fandom.com/wiki/Minute_of_Fame) | Locate and obtain the special edition of the gaming magazine on Interchange | 30.5, -19.5 | 37.5 | 10.1 | 3rd Floor |  |
| [Minute of Fame](https://escapefromtarkov.fandom.com/wiki/Minute_of_Fame) | Locate and obtain the special edition of the gaming magazine on Interchange | 18.9, -5.5 | 37.4 | 16.0 | 3rd Floor |  |
| [Needle in a Haystack](https://escapefromtarkov.fandom.com/wiki/Needle_in_a_Haystack) | Investigate the kart track on Interchange | 159.9, -246.7 | 23.4 |  | Ground level |  |
| [Needle in a Haystack](https://escapefromtarkov.fandom.com/wiki/Needle_in_a_Haystack) | Investigate the indoor children's playground on Interchange | 42.5, -216.4 | 29.9 | 2.2 | 2nd Floor |  |
| [No Swiping](https://escapefromtarkov.fandom.com/wiki/No_Swiping) | Eliminate any target at the smuggler bases on Shoreline or Interchange | 438.8, 145.6 | 32.4 | 7.4 | Ground level |  |
| [Pathfinder](https://escapefromtarkov.fandom.com/wiki/Pathfinder) | Visit the Railway Exfil exit on Interchange | 462.9, -415.8 | 27.2 |  | Ground level |  |
| [Pathfinder](https://escapefromtarkov.fandom.com/wiki/Pathfinder) | Visit the Emercom Checkpoint exit on Interchange | -311.5, 260.4 | 21.3 |  | Ground level |  |
| [Pathfinder](https://escapefromtarkov.fandom.com/wiki/Pathfinder) | Visit the Power Station V-Ex exit on Interchange | -252.2, -367.2 | 21.8 | 0.5 | Ground level |  |
| [Provocation](https://escapefromtarkov.fandom.com/wiki/Provocation) | Eliminate any target inside the ULTRA Mall with an ASh-12 assault rifle on Interchange | -19.4, -239.9 | 33.1 | 5.9 | 2nd Floor |  |
| [Provocation](https://escapefromtarkov.fandom.com/wiki/Provocation) | Eliminate any target inside the ULTRA Mall with an ASh-12 assault rifle on Interchange | -19.4, 129.3 | 33.1 | 11.5 | 2nd Floor |  |
| [Provocation](https://escapefromtarkov.fandom.com/wiki/Provocation) | Eliminate any target inside the ULTRA Mall with an ASh-12 assault rifle on Interchange | -40.7, -54.6 | 33.1 | 6.1 | 2nd Floor |  |
| [Provocation](https://escapefromtarkov.fandom.com/wiki/Provocation) | Stash a Salty Dog beef sausage inside the Kiba Arms store on Interchange | -19.5, -22.4 | 27.6 | 0.5 | 2nd Floor |  |
| [Provocation](https://escapefromtarkov.fandom.com/wiki/Provocation) | Stash a Bottle of Fierce Hatchling moonshine inside the Saferoom Exfil on Interchange | -49.3, 45.0 | 21.8 | 0.0 | Ground level |  |
| [Provocation](https://escapefromtarkov.fandom.com/wiki/Provocation) | Stash a Toilet paper inside the secret container stash on Interchange | 138.8, 274.4 | 25.1 | 3.6 | Ground level |  |
| [Supervisor](https://escapefromtarkov.fandom.com/wiki/Supervisor) | Stash the Goshan cash register key at the BIZARRO store fitting rooms on Interchange | -62.0, -99.1 | 27.6 | 0.1 | 2nd Floor |  |
| [Supervisor](https://escapefromtarkov.fandom.com/wiki/Supervisor) | Stash the IDEA cash register key at Register #9 on Interchange | 25.3, -242.5 | 28.2 | 0.5 | 2nd Floor |  |
| [Supervisor](https://escapefromtarkov.fandom.com/wiki/Supervisor) | Stash the OLI cash register key at Register #7-8 on Interchange | -3.2, 99.8 | 28.2 | 0.5 | 2nd Floor |  |
| [The Key to Success](https://escapefromtarkov.fandom.com/wiki/The_Key_to_Success) | Locate and obtain the first book of clothes design on Interchange | 20.3, -4.4 | 36.6 | 15.2 | 3rd Floor |  |
| [The Key to Success](https://escapefromtarkov.fandom.com/wiki/The_Key_to_Success) | Locate and obtain the second book of clothes design on Interchange | -31.4, -136.2 | 27.6 |  | 2nd Floor |  |

### Lighthouse (no floor layers)

| Task | Step | x, z | y | Above ground | Floor | Wiki floor |
|---|---|---|---|---|---|---|
| [Ask for Directions](https://escapefromtarkov.fandom.com/wiki/Ask_for_Directions) | Locate and mark the first section of the cliff path with an MS2000 Marker on Lighthouse | -143.4, -8.3 | 30.1 |  | Ground level |  |
| [Ask for Directions](https://escapefromtarkov.fandom.com/wiki/Ask_for_Directions) | Locate and mark the second section of the cliff path with an MS2000 Marker on Lighthouse | -171.0, -54.7 | 31.1 |  | Ground level |  |
| [Ask for Directions](https://escapefromtarkov.fandom.com/wiki/Ask_for_Directions) | Locate and mark the third section of the cliff path with an MS2000 Marker on Lighthouse | -181.1, -115.7 | 36.6 |  | Ground level |  |
| [Ask for Directions](https://escapefromtarkov.fandom.com/wiki/Ask_for_Directions) | Locate and mark the fourth section of the cliff path with an MS2000 Marker on Lighthouse | -182.6, -177.4 | 23.8 |  | Ground level |  |
| [Broadcast - Part 1](https://escapefromtarkov.fandom.com/wiki/Broadcast_-_Part_1) | Locate the hidden recording studio on Lighthouse | 32.5, -640.3 | 6.4 | 1.3 | Ground level |  |
| [Broadcast - Part 1](https://escapefromtarkov.fandom.com/wiki/Broadcast_-_Part_1) | Place a Signal Jammer inside the studio | 32.5, -640.3 | 6.4 | 1.3 | Ground level |  |
| [Bullshit](https://escapefromtarkov.fandom.com/wiki/Bullshit) | Stash an AXMC sniper rifle in the trash bags at the chalet tennis court on Lighthouse | -62.2, 133.0 | 29.4 | 2.6 | Ground level |  |
| [Bullshit](https://escapefromtarkov.fandom.com/wiki/Bullshit) | Stash a Roler Submariner gold wrist watch in the trash bags at the chalet tennis court on Lighthouse | -62.2, 133.0 | 29.4 | 2.6 | Ground level |  |
| [Bullshit](https://escapefromtarkov.fandom.com/wiki/Bullshit) | Stash a Military flash drive in the trash bags at the chalet tennis court on Lighthouse | -62.2, 133.0 | 29.4 | 2.6 | Ground level |  |
| [Corporate Secrets](https://escapefromtarkov.fandom.com/wiki/Corporate_Secrets) | Locate and obtain the data on the water pump operation on Lighthouse | -111.0, -750.1 | 9.2 | 4.1 | Ground level |  |
| [Corporate Secrets](https://escapefromtarkov.fandom.com/wiki/Corporate_Secrets) | Locate and obtain the data on the pumping station operation on Lighthouse | 53.2, -638.9 | 8.7 | 3.6 | Ground level |  |
| [Drug Trafficking](https://escapefromtarkov.fandom.com/wiki/Drug_Trafficking) | Locate the hidden drug lab on Lighthouse | -119.2, -841.1 | 13.0 | 2.2 | Ground level |  |
| [Drug Trafficking](https://escapefromtarkov.fandom.com/wiki/Drug_Trafficking) | Stash a WI-FI Camera in the drug lab | -119.2, -841.1 | 13.0 | 2.2 | Ground level |  |
| [Easy Job](https://escapefromtarkov.fandom.com/wiki/Easy_Job) | Locate the helicopter at the water treatment plant on Lighthouse | -96.0, -553.4 | 2.4 | 2.5 | Ground level |  |
| [Easy Job](https://escapefromtarkov.fandom.com/wiki/Easy_Job) | Mark the helicopter with an MS2000 Marker | -96.5, -552.6 | 2.4 | 2.5 | Ground level |  |
| [Easy Job](https://escapefromtarkov.fandom.com/wiki/Easy_Job) | Eliminate any target around the helicopter area | -51.2, -573.2 | 14.5 | 13.0 | Ground level |  |
| [Easy Job - Part 2](https://escapefromtarkov.fandom.com/wiki/Easy_Job_-_Part_2) | Eliminate any target around the helicopter area at the water treatment plant on Lighthouse | -51.2, -573.2 | 14.5 | 13.0 | Ground level |  |
| [Energy Crisis](https://escapefromtarkov.fandom.com/wiki/Energy_Crisis) | Find and mark the group of fuel tanks with an MS2000 Marker on Lighthouse | -116.6, -921.9 | 11.5 | 2.1 | Ground level |  |
| [Energy Crisis](https://escapefromtarkov.fandom.com/wiki/Energy_Crisis) | Find and mark the first tanker truck with an MS2000 Marker on Lighthouse | -73.7, -875.5 | 11.8 |  | Ground level |  |
| [Energy Crisis](https://escapefromtarkov.fandom.com/wiki/Energy_Crisis) | Find and mark the second tanker truck with an MS2000 Marker on Lighthouse | -156.4, -610.5 | 6.3 |  | Ground level |  |
| [Energy Crisis](https://escapefromtarkov.fandom.com/wiki/Energy_Crisis) | Find and mark the third tanker truck with an MS2000 Marker on Lighthouse | 30.3, -422.2 | 6.2 |  | Ground level |  |
| [From Hand to Hand](https://escapefromtarkov.fandom.com/wiki/From_Hand_to_Hand) | Stash a Virtex programmable processor inside the makeshift lab on Lighthouse | -119.2, -841.1 | 13.0 | 2.2 | Ground level |  |
| [From Hand to Hand](https://escapefromtarkov.fandom.com/wiki/From_Hand_to_Hand) | Stash a Military COFDM Wireless Signal Transmitter inside the makeshift lab on Lighthouse | -119.2, -841.1 | 13.0 | 2.2 | Ground level |  |
| [Gifts from Tarkov](https://escapefromtarkov.fandom.com/wiki/Gifts_from_Tarkov) | Locate and mark the TerraGroup cargo with an MS2000 Marker on Lighthouse | 136.9, 47.9 | 0.8 |  | Ground level |  |
| [Invasive Therapy](https://escapefromtarkov.fandom.com/wiki/Invasive_Therapy) | Stash any Obdolbos cocktail injector in the med bay at the upper Rogue chalet on Lighthouse | -120.6, 79.7 | 37.6 | 4.1 | Ground level |  |
| [Invasive Therapy](https://escapefromtarkov.fandom.com/wiki/Invasive_Therapy) | Stash any Obdolbos cocktail injector in the guest hall supplies at the upper Rogue chalet on Lighthouse | -123.4, 97.3 | 40.9 | 6.7 | Ground level |  |
| [Invasive Therapy](https://escapefromtarkov.fandom.com/wiki/Invasive_Therapy) | Stash any Obdolbos cocktail injector in the ammo stockpile at the lower Rogue chalet on Lighthouse | -79.9, -88.4 | 19.3 | 0.5 | Ground level |  |
| [Is This a Reference?](https://escapefromtarkov.fandom.com/wiki/Is_This_a_Reference%3F) | Install a WI-FI Camera by your friend Wilson on Lighthouse | 117.1, -154.5 | 0.9 |  | Ground level |  |
| [Is This a Reference?](https://escapefromtarkov.fandom.com/wiki/Is_This_a_Reference%3F) | Install a WI-FI Camera at the kindled rest place on Lighthouse | 97.6, -165.6 | 3.9 |  | Ground level |  |
| [Is This a Reference?](https://escapefromtarkov.fandom.com/wiki/Is_This_a_Reference%3F) | Install a WI-FI Camera at the ominous welcome sign on Lighthouse | 35.6, -261.5 | 8.3 |  | Ground level |  |
| [Is This a Reference?](https://escapefromtarkov.fandom.com/wiki/Is_This_a_Reference%3F) | Install a WI-FI Camera at the megagenius scientist's seat on Lighthouse | 97.0, 115.7 | 24.4 |  | Ground level |  |
| [Long Road](https://escapefromtarkov.fandom.com/wiki/Long_Road) | Eliminate Scavs along the shore and the main road on Lighthouse or Shoreline | 19.0, 104.0 | 7.8 |  | Ground level |  |
| [Lost Contact](https://escapefromtarkov.fandom.com/wiki/Lost_Contact) | Locate the lost group in the chalet area on Lighthouse | -70.4, 132.2 | 26.8 | 0.0 | Ground level |  |
| [Missing Cargo](https://escapefromtarkov.fandom.com/wiki/Missing_Cargo) | Locate and obtain the informant's intelligence folder | -115.7, 88.9 | 40.8 | 7.2 | Ground level |  |
| [Missing Cargo](https://escapefromtarkov.fandom.com/wiki/Missing_Cargo) | Locate the crashed helicopter on Lighthouse | -126.7, 301.5 | 22.4 | 1.2 | Ground level |  |
| [Overpopulation](https://escapefromtarkov.fandom.com/wiki/Overpopulation) | Eliminate any target around the chalets on Lighthouse | -123.8, 9.4 | 39.2 |  | Ground level |  |
| [Reconnaissance](https://escapefromtarkov.fandom.com/wiki/Reconnaissance) | Investigate the roof of any water treatment plant facility on Lighthouse | -63.6, -673.2 | 31.0 | 29.2 | Ground level |  |
| [Revision - Lighthouse](https://escapefromtarkov.fandom.com/wiki/Revision_-_Lighthouse) | Locate and mark the first BRDM with an MS2000 Marker on Lighthouse | 13.1, -503.2 | 2.8 | 0.8 | Ground level |  |
| [Revision - Lighthouse](https://escapefromtarkov.fandom.com/wiki/Revision_-_Lighthouse) | Locate and mark the second BRDM with an MS2000 Marker on Lighthouse | -65.1, -691.7 | 3.4 |  | Ground level |  |
| [Revision - Lighthouse](https://escapefromtarkov.fandom.com/wiki/Revision_-_Lighthouse) | Locate and mark the first Stryker with an MS2000 Marker on Lighthouse | 66.0, 516.8 | 2.8 |  | Ground level |  |
| [Revision - Lighthouse](https://escapefromtarkov.fandom.com/wiki/Revision_-_Lighthouse) | Locate and mark the second Stryker with an MS2000 Marker on Lighthouse | -41.0, 16.5 | 10.2 |  | Ground level |  |
| [Saving Private Roman](https://escapefromtarkov.fandom.com/wiki/Saving_Private_Roman) | Mark the transit to Woods with an MS2000 Marker on Lighthouse | 107.6, -957.6 | 6.8 |  | Ground level |  |
| [Seaside Vacation](https://escapefromtarkov.fandom.com/wiki/Seaside_Vacation) | Locate and obtain the informant's briefcase on Lighthouse | 139.2, -129.9 | 3.3 | 2.1 | Ground level |  |
| [Sisyphus](https://escapefromtarkov.fandom.com/wiki/Sisyphus) | Stash the second case in the railcar with the Ural truck at the train platform on Lighthouse | -16.6, -823.7 | 14.0 | 2.7 | Ground level |  |
| [Snatch](https://escapefromtarkov.fandom.com/wiki/Snatch) | Obtain the forged intelligence at the Rogue base on Lighthouse | 32.0, -454.5 | 4.9 | 0.3 | Ground level |  |
| [Snatch](https://escapefromtarkov.fandom.com/wiki/Snatch) | Obtain the forged intelligence at the Rogue base on Lighthouse | 21.3, -445.5 | 5.3 | 0.7 | Ground level |  |
| [Stimulating Demand](https://escapefromtarkov.fandom.com/wiki/Stimulating_Demand) | Locate and obtain the cargo package at the Rogue chalets on Lighthouse | -122.1, 95.0 | 36.9 | 3.3 | Ground level |  |
| [The Hermit](https://escapefromtarkov.fandom.com/wiki/The_Hermit) | Locate the hideout of Jaeger's friend on Lighthouse | -247.6, -328.3 | 1.2 | 0.1 | Ground level |  |
| [The Hermit](https://escapefromtarkov.fandom.com/wiki/The_Hermit) | Find and obtain the message for Jaeger | -248.4, -328.3 | 0.2 | -1.0 | Ground level |  |
| [The Huntsman Path - Administrator](https://escapefromtarkov.fandom.com/wiki/The_Huntsman_Path_-_Administrator) | Launch a yellow signal flare at the train station on Lighthouse | -5.8, -872.3 | 12.3 | 0.1 | Ground level |  |
| [The Huntsman Path - Administrator](https://escapefromtarkov.fandom.com/wiki/The_Huntsman_Path_-_Administrator) | Eliminate any target at the train station territory on Lighthouse | -39.5, -863.1 | 23.9 |  | Ground level |  |
| [The Price of Independence](https://escapefromtarkov.fandom.com/wiki/The_Price_of_Independence) | Launch a yellow signal flare at the train station warehouse on Lighthouse | -5.8, -872.3 | 12.3 | 0.1 | Ground level |  |
| [The Price of Independence](https://escapefromtarkov.fandom.com/wiki/The_Price_of_Independence) | Launch a yellow signal flare at the pier on Lighthouse | 148.9, -154.7 | 2.3 | 1.6 | Ground level |  |
| [The Price of Independence](https://escapefromtarkov.fandom.com/wiki/The_Price_of_Independence) | Launch a yellow signal flare at the train station warehouse on Lighthouse | -5.8, -872.3 | 12.3 | 0.1 | Ground level |  |
| [The Price of Independence](https://escapefromtarkov.fandom.com/wiki/The_Price_of_Independence) | Launch a yellow signal flare at the pier on Lighthouse | 148.9, -154.7 | 2.3 | 1.6 | Ground level |  |
| [Top Secret](https://escapefromtarkov.fandom.com/wiki/Top_Secret) | Locate the radar station commandant's office on Lighthouse | 353.1, 547.8 | 17.0 | 1.5 | Ground level |  |
| [Top Secret](https://escapefromtarkov.fandom.com/wiki/Top_Secret) | Locate and obtain the HDD with archived flight routes inside the room | 352.6, 545.5 | 16.3 | 2.2 | Ground level |  |

### Reserve

| Task | Step | x, z | y | Above ground | Floor | Wiki floor |
|---|---|---|---|---|---|---|
| [A Fuel Matter](https://escapefromtarkov.fandom.com/wiki/A_Fuel_Matter) | Mark the first group of fuel tanks with an MS2000 Marker on Reserve | 11.9, 73.8 | -5.0 |  | Ground level |  |
| [A Fuel Matter](https://escapefromtarkov.fandom.com/wiki/A_Fuel_Matter) | Mark the second group of fuel tanks with an MS2000 Marker on Reserve | 170.0, -97.9 | -4.4 | 2.5 | Ground level |  |
| [Back Door](https://escapefromtarkov.fandom.com/wiki/Back_Door) | Locate the secret underground bunker exit on Reserve | -119.8, 171.8 | -16.6 | 1.8 | Bunkers |  |
| [Back Door](https://escapefromtarkov.fandom.com/wiki/Back_Door) | Locate the switch that activates the exit | -117.2, 22.4 | -13.0 | 1.4 | Bunkers |  |
| [Classified Technologies](https://escapefromtarkov.fandom.com/wiki/Classified_Technologies) | Obtain the package with T-90M Commander control panel on Reserve | -88.1, 151.1 | -19.1 | 0.1 | Bunkers |  |
| [Disease History](https://escapefromtarkov.fandom.com/wiki/Disease_History) | Obtain Medical record #1 on Reserve | -59.0, -36.2 | -3.6 | 5.9 | 2nd Floor |  |
| [Disease History](https://escapefromtarkov.fandom.com/wiki/Disease_History) | Obtain Medical record #2 on Reserve | -80.5, -30.8 | -3.6 | 5.6 | 2nd Floor |  |
| [Documents](https://escapefromtarkov.fandom.com/wiki/Documents) | Obtain the first folder with military documents in the command bunker offices on Reserve | -114.4, 27.4 | -13.7 | 0.6 | Bunkers |  |
| [Documents](https://escapefromtarkov.fandom.com/wiki/Documents) | Obtain the second folder with military documents in the command bunker offices on Reserve | -114.2, 39.8 | -13.7 | 0.7 | Bunkers |  |
| [Documents](https://escapefromtarkov.fandom.com/wiki/Documents) | Obtain the third folder with military documents in the command bunker offices on Reserve | -121.9, 38.7 | -14.3 | 0.1 | Bunkers |  |
| [Hobby Club](https://escapefromtarkov.fandom.com/wiki/Hobby_Club) | Locate and obtain the AK-50 barrel on Reserve | 40.6, -125.9 | -4.3 | 7.6 | Ground level |  |
| [Hobby Club](https://escapefromtarkov.fandom.com/wiki/Hobby_Club) | Locate and obtain the AK-50 barrel on Reserve | 55.6, -116.5 | -4.0 | 8.0 | Ground level |  |
| [Hobby Club](https://escapefromtarkov.fandom.com/wiki/Hobby_Club) | Locate and obtain the AK-50 barrel on Reserve | 62.0, -108.8 | -4.2 | 7.0 | Ground level |  |
| [Hobby Club](https://escapefromtarkov.fandom.com/wiki/Hobby_Club) | Locate Glukhar's workshop on Reserve | 45.5, -117.5 | 2.1 | 13.3 | Ground level |  |
| [Hot Wheels](https://escapefromtarkov.fandom.com/wiki/Hot_Wheels) | Locate and mark the spare BTR wheels with an MS2000 Marker | 100.4, 27.7 | -6.3 | 0.5 | Ground level |  |
| [Hot Wheels - Let's Try Again](https://escapefromtarkov.fandom.com/wiki/Hot_Wheels_-_Let's_Try_Again) | Locate and mark the spare BTR wheels with an MS2000 Marker on Reserve | 100.4, 27.7 | -6.3 | 0.5 | Ground level |  |
| [Is This a Reference?](https://escapefromtarkov.fandom.com/wiki/Is_This_a_Reference%3F) | Install a WI-FI Camera at the place where conscripts did a very important task on Reserve | -84.4, 60.7 | -6.5 | 7.4 | Ground level |  |
| [Is This a Reference?](https://escapefromtarkov.fandom.com/wiki/Is_This_a_Reference%3F) | Install a WI-FI Camera at the two chair riddle on Reserve | 125.4, -88.9 | -6.2 | 0.2 | Ground level |  |
| [Is This a Reference?](https://escapefromtarkov.fandom.com/wiki/Is_This_a_Reference%3F) | Install a WI-FI Camera at every tank driver's first videogame on Reserve | -77.1, -20.0 | -6.3 | 3.0 | Ground level |  |
| [No Place for Renegades](https://escapefromtarkov.fandom.com/wiki/No_Place_for_Renegades) | Eliminate Raiders in the command bunker on Reserve | -111.4, 38.0 | -12.8 | 1.5 | Bunkers |  |
| [Order From Outside](https://escapefromtarkov.fandom.com/wiki/Order_From_Outside) | Locate and obtain the electronic jammer at the electromechanical warehouse on Reserve | -68.7, 32.4 | -6.5 | 3.8 | Ground level |  |
| [Order From Outside](https://escapefromtarkov.fandom.com/wiki/Order_From_Outside) | Locate and obtain the electronic jammer at the electromechanical warehouse on Reserve | -66.9, 29.5 | -6.5 | 3.5 | Ground level |  |
| [Order From Outside](https://escapefromtarkov.fandom.com/wiki/Order_From_Outside) | Locate and obtain the electronic jammer at the electromechanical warehouse on Reserve | -71.6, 23.1 | -6.5 | 4.0 | Ground level |  |
| [Payback](https://escapefromtarkov.fandom.com/wiki/Payback) | Shoot a yellow signal flare at the radar station on Reserve (In one raid) | -15.8, 184.8 | 19.9 | 0.9 | Ground level |  |
| [Pest Control](https://escapefromtarkov.fandom.com/wiki/Pest_Control) | Eliminate Scavs around the main barracks on Reserve | -106.0, 32.2 | 0.3 | 14.8 | 3rd Floor |  |
| [Reserve](https://escapefromtarkov.fandom.com/wiki/Reserve_(quest)) | Locate the food warehouse on Reserve | 78.8, -117.1 | -12.3 | -0.4 | Bunkers |  |
| [Reserve Expert](https://escapefromtarkov.fandom.com/wiki/Reserve_Expert) | Check the first armory in the eastern barracks (Black Pawn) on Reserve | -167.4, 31.4 | 3.6 | 12.5 | 4th Floor |  |
| [Reserve Expert](https://escapefromtarkov.fandom.com/wiki/Reserve_Expert) | Check the duty room in the eastern barracks (Black Pawn) on Reserve | -165.0, 34.5 | 0.7 | 9.6 | 3rd Floor |  |
| [Reserve Expert](https://escapefromtarkov.fandom.com/wiki/Reserve_Expert) | Check the second armory in the eastern barracks (Black Pawn) on Reserve | -167.4, 31.4 | -2.1 | 6.7 | 2nd Floor |  |
| [Reserve Expert](https://escapefromtarkov.fandom.com/wiki/Reserve_Expert) | Check the first armory in the southern barracks (White Pawn) on Reserve | -125.5, 95.7 | 3.6 | 12.5 | 4th Floor |  |
| [Reserve Expert](https://escapefromtarkov.fandom.com/wiki/Reserve_Expert) | Check the second armory in the southern barracks (White Pawn) on Reserve | -125.5, 95.7 | -2.1 | 6.7 | 2nd Floor |  |
| [Revision - Reserve](https://escapefromtarkov.fandom.com/wiki/Revision_-_Reserve) | Locate and inspect the first BMP-2 on Reserve | -100.4, -155.7 | -4.3 |  | Ground level |  |
| [Revision - Reserve](https://escapefromtarkov.fandom.com/wiki/Revision_-_Reserve) | Locate and inspect the second BMP-2 on Reserve | 79.0, -31.6 | -4.6 | 2.1 | Ground level |  |
| [Revision - Reserve](https://escapefromtarkov.fandom.com/wiki/Revision_-_Reserve) | Locate and inspect the third BMP-2 on Reserve | 103.4, 63.9 | -4.6 | 1.9 | Ground level |  |
| [Revision - Reserve](https://escapefromtarkov.fandom.com/wiki/Revision_-_Reserve) | Locate and inspect the fourth BMP-2 on Reserve | 53.8, 122.0 | -4.1 | 1.4 | Ground level |  |
| [Revision - Reserve](https://escapefromtarkov.fandom.com/wiki/Revision_-_Reserve) | Mark the first BMP-2 with an MS2000 Marker | -100.6, -156.0 | -3.7 |  | Ground level |  |
| [Revision - Reserve](https://escapefromtarkov.fandom.com/wiki/Revision_-_Reserve) | Mark the second BMP-2 with an MS2000 Marker | 79.0, -31.8 | -5.4 | 1.3 | Ground level |  |
| [Revision - Reserve](https://escapefromtarkov.fandom.com/wiki/Revision_-_Reserve) | Mark the third BMP-2 with an MS2000 Marker | 101.7, 64.4 | -5.6 | 0.9 | Ground level |  |
| [Revision - Reserve](https://escapefromtarkov.fandom.com/wiki/Revision_-_Reserve) | Mark the fourth BMP-2 with an MS2000 Marker | 53.6, 122.7 | -4 | 1.6 | Ground level |  |
| [Safe Corridor](https://escapefromtarkov.fandom.com/wiki/Safe_Corridor) | Eliminate Scavs in the underground storage warehouse on Reserve | 74.4, -107.0 | -20.2 | -9.1 | Bunkers |  |
| [Simple Side Job](https://escapefromtarkov.fandom.com/wiki/Simple_Side_Job) | Locate and obtain Lightkeeper's cargo crate on the roof of the military hospital on Reserve | -78.2, -35.2 | 0.3 | 9.7 | 3rd Floor |  |
| [Simple Side Job](https://escapefromtarkov.fandom.com/wiki/Simple_Side_Job) | Locate and obtain Lightkeeper's cargo crate on the roof of the military hospital on Reserve | -83.6, -28.8 | -0.5 | 8.7 | 3rd Floor |  |
| [Simple Side Job](https://escapefromtarkov.fandom.com/wiki/Simple_Side_Job) | Locate and obtain Lightkeeper's cargo crate on the roof of the military hospital on Reserve | -75.8, -28.7 | -0.5 | 9.0 | 3rd Floor |  |
| [Simple Side Job](https://escapefromtarkov.fandom.com/wiki/Simple_Side_Job) | Locate and obtain Lightkeeper's cargo crate on the roof of the military hospital on Reserve | -57.9, -40.6 | -0.5 | 9.0 | 3rd Floor |  |
| [Sisyphus](https://escapefromtarkov.fandom.com/wiki/Sisyphus) | Stash the first case in the guard booth near the Woods transit on Reserve | 208.4, -171.8 | -6.1 | 0.8 | Ground level |  |
| [Snatch](https://escapefromtarkov.fandom.com/wiki/Snatch) | Obtain the original intelligence in the repair station on Reserve | 102.2, 65.6 | -6.8 | -0.3 | Ground level |  |
| [Snatch](https://escapefromtarkov.fandom.com/wiki/Snatch) | Stash the forged intelligence under the BMP-2 in place of the original | 101.7, 64.4 | -5.6 | 0.9 | Ground level |  |
| [Special Comms](https://escapefromtarkov.fandom.com/wiki/Special_Comms) | Stash a Bulbex cable cutter at the sandbags next to LAV III above the storage warehouse on Reserve | 51.8, -181.6 | -0.1 | 6.8 | Ground level |  |
| [Surplus Goods](https://escapefromtarkov.fandom.com/wiki/Surplus_Goods) | Obtain the MBT Integrated Navigation System on Reserve | 99.8, 59.2 | -6.7 | -0.2 | Ground level |  |
| [The Bunker](https://escapefromtarkov.fandom.com/wiki/The_Bunker) | Locate the underground bunker on Reserve | -115.0, 33.9 | -11.9 | 2.5 | Bunkers |  |
| [The Bunker](https://escapefromtarkov.fandom.com/wiki/The_Bunker) | Locate the control room in the underground bunker on Reserve | -116.8, 31.7 | -13.2 | 1.2 | Bunkers |  |
| [The Bunker](https://escapefromtarkov.fandom.com/wiki/The_Bunker) | Locate the hermetic door leading to the hospital (White Bishop) on Reserve | -90.3, -5.2 | -13.4 | 1.3 | Bunkers |  |
| [The Bunker](https://escapefromtarkov.fandom.com/wiki/The_Bunker) | Locate one of the two hermetic doors leading to the academy building (Black Bishop) on Reserve | -144.2, 6.2 | -10.0 | -1.0 | Bunkers |  |
| [The Bunker](https://escapefromtarkov.fandom.com/wiki/The_Bunker) | Locate one of the two hermetic doors leading to barracks #1 (Black Pawn) on Reserve | -149.4, 50 | -9.3 | 4.9 | Bunkers |  |
| [The Bunker](https://escapefromtarkov.fandom.com/wiki/The_Bunker) | Locate one of the two hermetic doors leading to barracks #2 (White Pawn) on Reserve | -107.0, 77.5 | -9.4 | 0.6 | Bunkers |  |
| [The Bunker](https://escapefromtarkov.fandom.com/wiki/The_Bunker) | Locate the hermetic door leading to the air control center building (King) on Reserve | -73, 30.0 | -9.7 | 3.9 | Bunkers |  |
| [The Bunker - Part 2](https://escapefromtarkov.fandom.com/wiki/The_Bunker_-_Part_2) | Locate the hermetic door leading to the hospital (White Bishop) on Reserve | -90.3, -5.2 | -13.4 | 1.3 | Bunkers |  |
| [The Bunker - Part 2](https://escapefromtarkov.fandom.com/wiki/The_Bunker_-_Part_2) | Locate one of the two hermetic doors leading to the academy building (Black Bishop) on Reserve | -144.2, 6.2 | -10.0 | -1.0 | Bunkers |  |
| [The Bunker - Part 2](https://escapefromtarkov.fandom.com/wiki/The_Bunker_-_Part_2) | Locate one of the two hermetic doors leading to barracks #1 (Black Pawn) on Reserve | -149.4, 50 | -9.3 | 4.9 | Bunkers |  |
| [The Bunker - Part 2](https://escapefromtarkov.fandom.com/wiki/The_Bunker_-_Part_2) | Locate one of the two hermetic doors leading to barracks #2 (White Pawn) on Reserve | -107.0, 77.5 | -9.4 | 0.6 | Bunkers |  |
| [The Bunker - Part 2](https://escapefromtarkov.fandom.com/wiki/The_Bunker_-_Part_2) | Locate the hermetic door leading to the building of the air control center (King) on Reserve | -73, 30.0 | -9.7 | 3.9 | Bunkers |  |
| [The Huntsman Path - Administrator](https://escapefromtarkov.fandom.com/wiki/The_Huntsman_Path_-_Administrator) | Launch a yellow signal flare at the train depot on Reserve (In one raid) | 89.3, -124.5 | 1.5 | 13.5 | Ground level |  |
| [The Huntsman Path - Administrator](https://escapefromtarkov.fandom.com/wiki/The_Huntsman_Path_-_Administrator) | Eliminate any target at the train depot on Reserve (In one raid) | 130.4, -139.4 | 0.3 | 10.6 | Ground level |  |
| [The Price of Independence](https://escapefromtarkov.fandom.com/wiki/The_Price_of_Independence) | Stash the letter on the third floor of the military headquarters on Reserve | -127.4, -21.0 | 0.7 | 9.5 | 3rd Floor |  |
| [The Price of Independence](https://escapefromtarkov.fandom.com/wiki/The_Price_of_Independence) | Stash the letter on the third floor of the military headquarters on Reserve | -127.4, -21.0 | 0.7 | 9.5 | 3rd Floor |  |

### Shoreline

| Task | Step | x, z | y | Above ground | Floor | Wiki floor |
|---|---|---|---|---|---|---|
| [Anesthesia](https://escapefromtarkov.fandom.com/wiki/Anesthesia) | Locate and mark the first trading post with an MS2000 Marker on Shoreline | -264.0, -85.3 | -4.0 | -0.2 | Ground level |  |
| [Anesthesia](https://escapefromtarkov.fandom.com/wiki/Anesthesia) | Locate and mark the second trading post with an MS2000 Marker on Shoreline | 96.7, 97.1 | -47.2 | 1.0 | Ground level |  |
| [Anesthesia](https://escapefromtarkov.fandom.com/wiki/Anesthesia) | Locate and mark the third trading post with an MS2000 Marker on Shoreline | -306.2, 494.1 | -60.9 | 1.2 | Ground level |  |
| [Capturing Outposts](https://escapefromtarkov.fandom.com/wiki/Capturing_Outposts) | Eliminate PMC operatives at the specified Scav bases on Customs, Shoreline, or Woods | -257.1, -99.5 | -5.7 | -0.7 | Ground level |  |
| [Cargo X](https://escapefromtarkov.fandom.com/wiki/Cargo_X) | Locate and obtain the data in Health Resort east wing computer room on Shoreline | -285.1, -89.4 | 2.5 | 5.6 | 3rd Floor |  |
| [Cargo X - Part 3](https://escapefromtarkov.fandom.com/wiki/Cargo_X_-_Part_3) | Locate the TerraGroup cargo hidden inside the Health Resort on Shoreline | -149.9, -77 | -6.1 | -2.9 | Underground |  |
| [Chemistry Closet](https://escapefromtarkov.fandom.com/wiki/Chemistry_Closet) | Locate Sanitar's office in the health resort on Shoreline | -322.8, -77.5 | -2.8 | 0.9 | Ground level |  |
| [Colleagues](https://escapefromtarkov.fandom.com/wiki/Colleagues) | Locate the group that was sent to the Health Resort on Shoreline | -253.2, -56.9 | -4.1 |  | Ground level |  |
| [Colleagues](https://escapefromtarkov.fandom.com/wiki/Colleagues) | Locate the group that was sent to the pier on Shoreline | -311.9, 489.7 | -60.9 | 1.1 | Ground level |  |
| [Colleagues](https://escapefromtarkov.fandom.com/wiki/Colleagues) | Locate the group that was sent to the cottages on Shoreline | 94.2, 62.0 | -47.5 |  | Ground level |  |
| [Courtesy Visit](https://escapefromtarkov.fandom.com/wiki/Courtesy_Visit) | Locate the chairman's house in the abandoned village on Shoreline | 405.9, -44.5 | -51.9 | 0.8 | Ground level |  |
| [Courtesy Visit](https://escapefromtarkov.fandom.com/wiki/Courtesy_Visit) | Locate the fisherman's house in the abandoned village on Shoreline | 382.9, -125.9 | -51.9 |  | Ground level |  |
| [Courtesy Visit](https://escapefromtarkov.fandom.com/wiki/Courtesy_Visit) | Locate the priest's house in the abandoned village on Shoreline | 287.1, -46.3 | -49.2 |  | Ground level |  |
| [Eagle Eye](https://escapefromtarkov.fandom.com/wiki/Eagle_Eye) | Locate the first UAV crash site on Shoreline | -553.1, -127.7 | -29.4 |  | Ground level |  |
| [Eagle Eye](https://escapefromtarkov.fandom.com/wiki/Eagle_Eye) | Obtain the SAS disk from the second crashed drone | 81.4, -166.8 | -31.8 |  | Ground level |  |
| [Eagle Eye](https://escapefromtarkov.fandom.com/wiki/Eagle_Eye) | Obtain the SAS disk from the first crashed drone | -552.9, -128.2 | -31.2 |  | Ground level |  |
| [Eagle Eye](https://escapefromtarkov.fandom.com/wiki/Eagle_Eye) | Locate the second UAV crash site on Shoreline | 81.4, -166.8 | -31.8 |  | Ground level |  |
| [Fishing Gear](https://escapefromtarkov.fandom.com/wiki/Fishing_Gear) | Locate the boat hidden next to the breakwater on Shoreline | -182.0, 459.9 | -63.7 |  | Ground level |  |
| [Fishing Gear](https://escapefromtarkov.fandom.com/wiki/Fishing_Gear) | Stash an MF-UNTAR body armor in the boat | -182.0, 459.9 | -63.7 |  | Ground level |  |
| [Fishing Gear](https://escapefromtarkov.fandom.com/wiki/Fishing_Gear) | Stash a Leatherman Multitool in the boat | -182.0, 459.9 | -63.7 |  | Ground level |  |
| [Forge a Friendship](https://escapefromtarkov.fandom.com/wiki/Forge_a_Friendship) | Locate and obtain Prapor's cargo on Shoreline | -320.0, 483.6 | -61.3 | 0.7 | Ground level |  |
| [Forge a Friendship](https://escapefromtarkov.fandom.com/wiki/Forge_a_Friendship) | Locate and obtain Prapor's cargo on Shoreline | -310.6, 484.4 | -60.5 | 1.6 | Ground level |  |
| [Forge a Friendship](https://escapefromtarkov.fandom.com/wiki/Forge_a_Friendship) | Locate and obtain Prapor's cargo on Shoreline | -327.8, 490.2 | -60.3 | 1.7 | Ground level |  |
| [Forge a Friendship](https://escapefromtarkov.fandom.com/wiki/Forge_a_Friendship) | Locate and obtain Prapor's cargo on Shoreline | -315.5, 478.9 | -57.4 | 4.3 | Ground level | **2nd Floor**: pier office building, second-floor spawns |
| [Forge a Friendship](https://escapefromtarkov.fandom.com/wiki/Forge_a_Friendship) | Locate and obtain Prapor's cargo on Shoreline | -320.9, 490.2 | -57.4 | 4.7 | Ground level | **2nd Floor**: pier office building, second-floor spawns |
| [Health Care Privacy - Part 1](https://escapefromtarkov.fandom.com/wiki/Health_Care_Privacy_-_Part_1) | Locate and mark the first ambulance with an MS2000 Marker on Shoreline | 312.7, 314.5 | -59.2 | 5.6 | Ground level |  |
| [Health Care Privacy - Part 1](https://escapefromtarkov.fandom.com/wiki/Health_Care_Privacy_-_Part_1) | Locate and mark the second ambulance with an MS2000 Marker on Shoreline | 354.9, 306.1 | -58.6 |  | Ground level |  |
| [Health Care Privacy - Part 1](https://escapefromtarkov.fandom.com/wiki/Health_Care_Privacy_-_Part_1) | Locate and mark the third ambulance with an MS2000 Marker on Shoreline | -258.1, -85.7 | -4.0 | 1.0 | Ground level |  |
| [Health Care Privacy - Part 1](https://escapefromtarkov.fandom.com/wiki/Health_Care_Privacy_-_Part_1) | Locate and mark the fourth ambulance with an MS2000 Marker on Shoreline | 97.7, 70.8 | -47.2 |  | Ground level |  |
| [Health Care Privacy - Part 2](https://escapefromtarkov.fandom.com/wiki/Health_Care_Privacy_-_Part_2) | Locate and obtain any info about TerraGroup's research in Health Resort west wing on Shoreline | -218.0, -86.1 | 2.8 | 9.8 | 3rd Floor |  |
| [Hidden Layer](https://escapefromtarkov.fandom.com/wiki/Hidden_Layer) | Locate a good lead related to Knossos LLC | -196.5, -81 | -6 | -0.0 | Underground |  |
| [Hidden Layer](https://escapefromtarkov.fandom.com/wiki/Hidden_Layer) | Find a way inside the Knossos LLC facility | -196, -77 | -6.5 | -0.5 | Underground |  |
| [Humanitarian Supplies](https://escapefromtarkov.fandom.com/wiki/Humanitarian_Supplies) | Locate and mark the first UN truck with an MS2000 Marker | -234.5, -164.4 | -3.5 | 3.8 | Ground level |  |
| [Humanitarian Supplies](https://escapefromtarkov.fandom.com/wiki/Humanitarian_Supplies) | Locate the first truck that was holding the lost UN cargo on Shoreline | -234.5, -164.4 | -3.5 | 3.8 | Ground level |  |
| [Humanitarian Supplies](https://escapefromtarkov.fandom.com/wiki/Humanitarian_Supplies) | Locate and mark the second UN truck with an MS2000 Marker | -596.3, 475.5 | -58.5 |  | Ground level |  |
| [Humanitarian Supplies](https://escapefromtarkov.fandom.com/wiki/Humanitarian_Supplies) | Locate the second truck that was holding the lost UN cargo on Shoreline | -596.3, 475.5 | -58.5 |  | Ground level |  |
| [I Need More Power](https://escapefromtarkov.fandom.com/wiki/I_Need_More_Power) | Locate the generators in the east wing of the Health Resort on Shoreline | -336.6, -76.4 | 0.1 | 3.8 | 2nd Floor |  |
| [I Need More Power](https://escapefromtarkov.fandom.com/wiki/I_Need_More_Power) | Locate the generators in the west wing of the Health Resort on Shoreline | -171.2, -75.5 | 0.1 | 3.8 | 2nd Floor |  |
| [Ill-Wisher](https://escapefromtarkov.fandom.com/wiki/Ill-Wisher) | Locate the first signal source on Shoreline | -230.4, -93.6 | 8.3 | 15.3 | 3rd Floor |  |
| [Ill-Wisher](https://escapefromtarkov.fandom.com/wiki/Ill-Wisher) | Place a Signal jammer on the first signal source | -230.6, -92.4 | 8.3 | 15.3 | 3rd Floor |  |
| [Ill-Wisher](https://escapefromtarkov.fandom.com/wiki/Ill-Wisher) | Locate the second signal source on Shoreline | -483.3, 253.7 | -25.8 | -0.6 | Ground level |  |
| [Ill-Wisher](https://escapefromtarkov.fandom.com/wiki/Ill-Wisher) | Place a Signal jammer on the second signal source | -483.8, 248.8 | -24.5 | 1.0 | Ground level |  |
| [Is This a Reference?](https://escapefromtarkov.fandom.com/wiki/Is_This_a_Reference%3F) | Install a WI-FI Camera at the upside-down chair on Shoreline | 326.9, 129.4 | -54.2 | 2.2 | Ground level |  |
| [Is This a Reference?](https://escapefromtarkov.fandom.com/wiki/Is_This_a_Reference%3F) | Install a WI-FI Camera at the not-so-lonely bathroom on Shoreline | -322.4, 488.1 | -60.7 | 1.4 | Ground level |  |
| [Long Road](https://escapefromtarkov.fandom.com/wiki/Long_Road) | Eliminate Scavs along the shore and the main road on Lighthouse or Shoreline | -143.4, 451.2 | -22 |  | Ground level |  |
| [Master Key](https://escapefromtarkov.fandom.com/wiki/Master_Key) | Locate and obtain the key to the closed premises of the Health Resort on Shoreline | -152.3, -301.2 | -14.5 |  | Ground level |  |
| [Natural Exchange](https://escapefromtarkov.fandom.com/wiki/Natural_Exchange) | Stash the first metal fuel tank at the smugglers' base on Shoreline | -610.5, -176.1 | -28.7 | 1.2 | Ground level |  |
| [Natural Exchange](https://escapefromtarkov.fandom.com/wiki/Natural_Exchange) | Stash the second metal fuel tank at the smugglers' base on Shoreline | -625.4, -228.3 | -25.4 | 1.3 | Ground level |  |
| [Needle in a Haystack](https://escapefromtarkov.fandom.com/wiki/Needle_in_a_Haystack) | Investigate the coast-side construction site on Shoreline | -625.8, 482.2 | -54.7 | 4.9 | Ground level |  |
| [Needle in a Haystack](https://escapefromtarkov.fandom.com/wiki/Needle_in_a_Haystack) | Investigate the children's playground by the Health Resort on Shoreline | -351.3, -134 | -1.2 |  | Ground level |  |
| [No Swiping](https://escapefromtarkov.fandom.com/wiki/No_Swiping) | Eliminate any target at the smuggler bases on Shoreline or Interchange | -591.8, -117.7 | -20.3 |  | Ground level |  |
| [Nostalgia](https://escapefromtarkov.fandom.com/wiki/Nostalgia) | Locate and obtain Jaeger's photo album | -226.6, -87.6 | 2.1 | 9.1 | 3rd Floor |  |
| [Nostalgia](https://escapefromtarkov.fandom.com/wiki/Nostalgia) | Locate Jaeger's Health Resort room with a view of the bay on Shoreline | -229.1, -88.9 | 3.3 | 10.3 | 3rd Floor |  |
| [Nothing Fishy About This](https://escapefromtarkov.fandom.com/wiki/Nothing_Fishy_About_This) | Locate Ragman's SUV on Shoreline | 227.2, -159.9 | -54.9 |  | Ground level |  |
| [Proper Comeback](https://escapefromtarkov.fandom.com/wiki/Proper_Comeback) | Stash a Golden rooster figurine at Prapor's WI-FI Camera on Shoreline | -459.7, 564.8 | -47.8 | 15.3 | Ground level |  |
| [Rigged Game](https://escapefromtarkov.fandom.com/wiki/Rigged_Game) | Mark the medical container at the Health Resort with an MS2000 Marker on Shoreline | -263.6, -85.7 | -4.0 | -0.2 | Ground level |  |
| [Rigged Game](https://escapefromtarkov.fandom.com/wiki/Rigged_Game) | Mark the medical container by cottages with an MS2000 Marker on Shoreline | 98.1, 97.0 | -47.2 | 1.2 | Ground level |  |
| [Rigged Game](https://escapefromtarkov.fandom.com/wiki/Rigged_Game) | Mark the medical container at the river pier with an MS2000 Marker on Shoreline | -305.4, 492.2 | -60.9 | 1.2 | Ground level |  |
| [Scrap Metal](https://escapefromtarkov.fandom.com/wiki/Scrap_Metal) | Locate and mark the first T-90 tank with an MS2000 Marker on Shoreline | -153.1, -280.2 | -17.1 | -2.3 | Ground level |  |
| [Scrap Metal](https://escapefromtarkov.fandom.com/wiki/Scrap_Metal) | Locate and mark the second T-90 tank with an MS2000 Marker on Shoreline | 378.7, 166.9 | -54.4 |  | Ground level |  |
| [Scrap Metal](https://escapefromtarkov.fandom.com/wiki/Scrap_Metal) | Locate and mark the third T-90 tank with an MS2000 Marker on Shoreline | -349.7, 185.9 | -39.9 |  | Ground level |  |
| [Serious Allegations](https://escapefromtarkov.fandom.com/wiki/Serious_Allegations) | Locate and obtain the hard drive at the old house on Shoreline | 330.0, -143.7 | -54.4 | -0.2 | Ground level |  |
| [Serious Allegations](https://escapefromtarkov.fandom.com/wiki/Serious_Allegations) | Locate and obtain the hard drive at the old house on Shoreline | 286.7, -176.1 | -54.4 | -0.2 | Ground level |  |
| [Serious Allegations](https://escapefromtarkov.fandom.com/wiki/Serious_Allegations) | Locate and obtain the hard drive at the old house on Shoreline | 207.4, 100.2 | -48.3 |  | Ground level |  |
| [Serious Allegations](https://escapefromtarkov.fandom.com/wiki/Serious_Allegations) | Locate and obtain the hard drive at the old house on Shoreline | 283.9, -183.0 | -54.4 | -0.2 | Ground level |  |
| [Serious Allegations](https://escapefromtarkov.fandom.com/wiki/Serious_Allegations) | Locate and obtain the hard drive at the old house on Shoreline | 324.4, -145.4 | -53.8 | 0.5 | Ground level |  |
| [Serious Allegations](https://escapefromtarkov.fandom.com/wiki/Serious_Allegations) | Locate and obtain the hard drive at the old house on Shoreline | 290.5, -40.2 | -49.8 |  | Ground level |  |
| [Serious Allegations](https://escapefromtarkov.fandom.com/wiki/Serious_Allegations) | Locate and obtain the hard drive at the old house on Shoreline | 200.1, 101.4 | -48.3 |  | Ground level |  |
| [Serious Allegations](https://escapefromtarkov.fandom.com/wiki/Serious_Allegations) | Locate and obtain the hard drive at the old house on Shoreline | 356.9, -102.4 | -53.8 |  | Ground level |  |
| [Serious Allegations](https://escapefromtarkov.fandom.com/wiki/Serious_Allegations) | Locate and obtain the hard drive at the old house on Shoreline | 198.8, 99.0 | -47.5 |  | Ground level |  |
| [Serious Allegations](https://escapefromtarkov.fandom.com/wiki/Serious_Allegations) | Locate and obtain the hard drive at the old house on Shoreline | -527.1, 405.4 | -54.8 |  | Ground level |  |
| [Serious Allegations](https://escapefromtarkov.fandom.com/wiki/Serious_Allegations) | Locate and obtain the hard drive at the old house on Shoreline | 290.5, -39.0 | -50.6 |  | Ground level |  |
| [Serious Allegations](https://escapefromtarkov.fandom.com/wiki/Serious_Allegations) | Locate and obtain the hard drive at the old house on Shoreline | 357.5, -108.5 | -54.2 |  | Ground level |  |
| [Serious Allegations](https://escapefromtarkov.fandom.com/wiki/Serious_Allegations) | Locate and obtain the hard drive at the old house on Shoreline | 323.7, -81.7 | -54.3 |  | Ground level |  |
| [Signal - Part 3](https://escapefromtarkov.fandom.com/wiki/Signal_-_Part_3) | Place the Signal jammer on the first specified place on Shoreline | -483.8, 248.8 | -24.5 | 1.0 | Ground level |  |
| [Signal - Part 3](https://escapefromtarkov.fandom.com/wiki/Signal_-_Part_3) | Place the Signal jammer on the second specified place on Shoreline | -230.6, -92.4 | 8.3 | 15.3 | 3rd Floor |  |
| [Signal - Part 3](https://escapefromtarkov.fandom.com/wiki/Signal_-_Part_3) | Place the Signal jammer on the third specified place on Shoreline | -708.7, 90.6 | -26.2 | 1.4 | Ground level |  |
| [Small Business - Part 3](https://escapefromtarkov.fandom.com/wiki/Small_Business_-_Part_3) | Stash a Cultist knife at the sunken village marked circle on Shoreline | 252.0, -105.1 | -52.7 | 1.9 | Ground level |  |
| [Small Business - Part 3](https://escapefromtarkov.fandom.com/wiki/Small_Business_-_Part_3) | Stash a Cultist knife at the Health Resort east wing marked circle on Shoreline | -336.6, -88.7 | 3.5 | 7.3 | 3rd Floor |  |
| [Spa Tour - Part 2](https://escapefromtarkov.fandom.com/wiki/Spa_Tour_-_Part_2) | Locate and mark the helicopter at the Health Resort with an MS2000 Marker on Shoreline | -250.5, -48.3 | -5.1 |  | Ground level |  |
| [Spa Tour - Part 2](https://escapefromtarkov.fandom.com/wiki/Spa_Tour_-_Part_2) | Mark the safe passage to the helicopter with an MS2000 Marker on Shoreline | -280.6, -41.3 | -4.8 | 1.1 | Ground level |  |
| [Tarkov-Style Diplomacy](https://escapefromtarkov.fandom.com/wiki/Tarkov-Style_Diplomacy) | Locate and obtain Sanitar's surgery kit on Shoreline | -314.6, 480.2 | -55.7 | 5.9 | Ground level | **2nd Floor**: pier office building, second floor |
| [Tarkov-Style Diplomacy](https://escapefromtarkov.fandom.com/wiki/Tarkov-Style_Diplomacy) | Locate and obtain Sanitar's ophthalmoscope on Shoreline | 99.5, 107.0 | -44.4 | 3.1 | Ground level | **2nd Floor**: villa, room on the second floor |
| [The Cult](https://escapefromtarkov.fandom.com/wiki/The_Cult) | Locate the missing informant on Shoreline | 287.1, -42.3 | -49.4 |  | Ground level |  |
| [Thirsty - Echo](https://escapefromtarkov.fandom.com/wiki/Thirsty_-_Echo) | Locate any information about Thirsty on Shoreline | -200.3, -76.4 | -6.2 | 0.4 | Underground |  |
| [Thirsty - Echo](https://escapefromtarkov.fandom.com/wiki/Thirsty_-_Echo) | Obtain the information in Thirsty's hideout | -203.1, -76.6 | -6.2 | 0.3 | Underground |  |
| [Thirsty - Echo](https://escapefromtarkov.fandom.com/wiki/Thirsty_-_Echo) | Obtain the information in Thirsty's hideout | -198.7, -74.5 | -6.9 | -0.3 | Underground |  |
| [Thirsty - Echo](https://escapefromtarkov.fandom.com/wiki/Thirsty_-_Echo) | Obtain the information in Thirsty's hideout | -201.4, -79.4 | -7.0 | -0.4 | Underground |  |
| [Tracker](https://escapefromtarkov.fandom.com/wiki/Tracker) | Obtain any information about the second part of the cargo shipment | -341.0, -88.6 | -2.7 | 1.1 | Ground level |  |
| [Tracker](https://escapefromtarkov.fandom.com/wiki/Tracker) | Locate the room with reservoirs in the Health Resort on Shoreline | -337.0, -88.1 | -2.7 | 1.0 | Ground level |  |
| [Tracker](https://escapefromtarkov.fandom.com/wiki/Tracker) | Locate the hidden TerraGroup cargo in the Health Resort on Shoreline | -149.9, -77 | -6.1 | -2.9 | Underground |  |
| [Viewer](https://escapefromtarkov.fandom.com/wiki/Viewer) | Install a WI-FI Camera at the pier tower on Shoreline | -459.3, 567.0 | -47.6 | 15.5 | Ground level |  |
| [Vitamins](https://escapefromtarkov.fandom.com/wiki/Vitamins) | Locate and obtain the chemical container on Factory | -186.1, -86.1 | -2.7 | 1.0 | Ground level |  |
| [Weapons Circulation](https://escapefromtarkov.fandom.com/wiki/Weapons_Circulation) | Locate and mark the ritual spot with an MS2000 Marker on Shoreline | -336.6, -88.7 | 3.5 | 7.3 | 3rd Floor |  |
| [Wet Job - Part 2](https://escapefromtarkov.fandom.com/wiki/Wet_Job_-_Part_2) | Locate the fishermen's dwelling on Shoreline | 235.6, 442.0 | -64.5 | 0.0 | Ground level |  |
| [Wet Job - Part 2](https://escapefromtarkov.fandom.com/wiki/Wet_Job_-_Part_2) | Mark the fishing table with an MS2000 Marker | 235.6, 442.0 | -64.5 | 0.0 | Ground level |  |
| [Wet Job - Part 3](https://escapefromtarkov.fandom.com/wiki/Wet_Job_-_Part_3) | Locate Artyom’s car on Shoreline | 72.9, 348.7 | -59.7 |  | Ground level |  |
| [Wet Job - Part 3](https://escapefromtarkov.fandom.com/wiki/Wet_Job_-_Part_3) | Mark Artyom's car with an MS2000 Marker | 73.0, 348.7 | -58.1 |  | Ground level |  |
| [Wet Job - Part 4](https://escapefromtarkov.fandom.com/wiki/Wet_Job_-_Part_4) | Locate and obtain the list of Health Resort tenants on Shoreline | -267.2, -145.6 | -0.0 | 5.9 | 2nd Floor |  |
| [Wet Job - Part 5](https://escapefromtarkov.fandom.com/wiki/Wet_Job_-_Part_5) | Locate and obtain any information on Artyom’s work on Shoreline | -359.0, -77.0 | 2.5 | 6.3 | 3rd Floor |  |

### Streets of Tarkov

| Task | Step | x, z | y | Above ground | Floor | Wiki floor |
|---|---|---|---|---|---|---|
| [Audiophile](https://escapefromtarkov.fandom.com/wiki/Audiophile) | Locate the musician gathering spot on Streets of Tarkov | 43.0, 151.5 | 11.8 | 9.0 | 2nd Floor | **4th Floor**: Primorsky 48 apartment 10, fourth floor |
| [Audiophile](https://escapefromtarkov.fandom.com/wiki/Audiophile) | Locate and obtain the engraved guitar pick | 44.7, 149.3 | 11.8 | 9.3 | 2nd Floor | **4th Floor**: Primorsky 48 apartment 10, fourth floor |
| [Audiophile](https://escapefromtarkov.fandom.com/wiki/Audiophile) | Locate and obtain the engraved guitar pick | 36.5, 157.5 | 11.8 | 9.1 | 2nd Floor | **4th Floor**: Primorsky 48 apartment 10, fourth floor |
| [Audiophile](https://escapefromtarkov.fandom.com/wiki/Audiophile) | Locate and obtain the engraved guitar pick | 40.6, 153.8 | 11.7 | 8.9 | 2nd Floor | **4th Floor**: Primorsky 48 apartment 10, fourth floor |
| [Audiophile](https://escapefromtarkov.fandom.com/wiki/Audiophile) | Locate and obtain the engraved guitar pick | 42.9, 152.4 | 11.7 | 9.1 | 2nd Floor | **4th Floor**: Primorsky 48 apartment 10, fourth floor |
| [Audiophile](https://escapefromtarkov.fandom.com/wiki/Audiophile) | Locate and obtain the engraved guitar pick | 35.0, 152.3 | 12.5 | 9.8 | 2nd Floor | **4th Floor**: Primorsky 48 apartment 10, fourth floor |
| [Audiophile](https://escapefromtarkov.fandom.com/wiki/Audiophile) | Locate and obtain the engraved guitar pick | 37.0, 153.3 | 12.5 | 9.8 | 2nd Floor | **4th Floor**: Primorsky 48 apartment 10, fourth floor |
| [Audiophile](https://escapefromtarkov.fandom.com/wiki/Audiophile) | Locate and obtain the engraved guitar pick | 44.3, 151.8 | 12.6 | 10.0 | 2nd Floor | **4th Floor**: Primorsky 48 apartment 10, fourth floor |
| [Audiophile](https://escapefromtarkov.fandom.com/wiki/Audiophile) | Locate and obtain the engraved guitar pick | 42.3, 148.5 | 12.6 | 10.1 | 2nd Floor | **4th Floor**: Primorsky 48 apartment 10, fourth floor |
| [Audiophile](https://escapefromtarkov.fandom.com/wiki/Audiophile) | Locate and obtain the engraved guitar pick | 41.1, 155.0 | 12.6 | 9.8 | 2nd Floor | **4th Floor**: Primorsky 48 apartment 10, fourth floor |
| [Audiophile](https://escapefromtarkov.fandom.com/wiki/Audiophile) | Locate and obtain the engraved guitar pick | 36.3, 148.6 | 12.3 | 9.8 | 2nd Floor | **4th Floor**: Primorsky 48 apartment 10, fourth floor |
| [Audit](https://escapefromtarkov.fandom.com/wiki/Audit) | Obtain the financial records on Streets of Tarkov | -177.1, 227.1 | 6.1 | 3.2 | Ground level | **2nd Floor**: second floor, first office to the right |
| [Ballet Lover](https://escapefromtarkov.fandom.com/wiki/Ballet_Lover) | Locate the balletmeister's apartment on Streets of Tarkov | 47.6, 153.1 | 12.7 | 9.9 | 2nd Floor | **4th Floor**: Primorsky 48 apartment 10, fourth floor |
| [Beyond the Red Meat](https://escapefromtarkov.fandom.com/wiki/Beyond_the_Red_Meat) | Locate and obtain information on culinary secrets at the Beluga restaurant on Streets of Tarkov | -26.1, -56.1 | 10.6 | 10.0 | 2nd Floor | **3rd Floor**: Beluga: bar, kitchen and director's room on the third floor |
| [Beyond the Red Meat](https://escapefromtarkov.fandom.com/wiki/Beyond_the_Red_Meat) | Locate and obtain information on culinary secrets at the Beluga restaurant on Streets of Tarkov | -42.8, -66.4 | 10.1 | 9.5 | 2nd Floor | **3rd Floor**: Beluga: bar, kitchen and director's room on the third floor |
| [Beyond the Red Meat](https://escapefromtarkov.fandom.com/wiki/Beyond_the_Red_Meat) | Locate and obtain information on culinary secrets at the Beluga restaurant on Streets of Tarkov | -41.4, -42.9 | 5.9 | 5.2 | Ground level | **2nd Floor**: Beluga: oval bar on the second floor |
| [Beyond the Red Meat](https://escapefromtarkov.fandom.com/wiki/Beyond_the_Red_Meat) | Locate and obtain information on culinary secrets at the Beluga restaurant on Streets of Tarkov | -29.3, -70.2 | 10.1 | 9.5 | 2nd Floor | **3rd Floor**: Beluga: bar, kitchen and director's room on the third floor |
| [Broadcast - Part 2](https://escapefromtarkov.fandom.com/wiki/Broadcast_-_Part_2) | Locate the place of bloody broadcast inside the grocery store on Streets of Tarkov | 157.4, 314.2 | 5.1 | 1.3 | Ground level |  |
| [Broadcast - Part 3](https://escapefromtarkov.fandom.com/wiki/Broadcast_-_Part_3) | Locate the place of bloody broadcast inside the old house on Streets of Tarkov | -204.7, 243.0 | 3.3 | 0.2 | Ground level |  |
| [Broadcast - Part 4](https://escapefromtarkov.fandom.com/wiki/Broadcast_-_Part_4) | Locate the cultist meeting spot on Streets of Tarkov | -130.8, 269.7 | 9.5 | 6.2 | Ground level | **3rd Floor**: third floor of the northern abandoned factory building |
| [Broadcast - Part 5](https://escapefromtarkov.fandom.com/wiki/Broadcast_-_Part_5) | Locate the ritual spot on Chekannaya st. on Streets of Tarkov | 188.4, 226.5 | 0.8 | 0.1 | Ground level |  |
| [Broadcast - Part 5](https://escapefromtarkov.fandom.com/wiki/Broadcast_-_Part_5) | Stash a Cultist knife at the ritual spot | 188.6, 226.4 | 0.4 | -0.3 | Ground level |  |
| [Corporate Perks](https://escapefromtarkov.fandom.com/wiki/Corporate_Perks) | Locate the IT firm office on Streets of Tarkov | 164.4, 148.1 | 1.7 | 1.0 | Ground level |  |
| [Corporate Perks](https://escapefromtarkov.fandom.com/wiki/Corporate_Perks) | Unravel the secret of the firm's success | 164.2, 167.3 | 1.7 | 0.9 | Ground level |  |
| [Dandies](https://escapefromtarkov.fandom.com/wiki/Dandies) | Stash a Bomber beanie inside the barber shop on Streets of Tarkov | 206.6, 411.8 | 4.3 | 4.5 | Ground level |  |
| [Dandies](https://escapefromtarkov.fandom.com/wiki/Dandies) | Stash RayBench Hipster Reserve sunglasses inside the barber shop on Streets of Tarkov | 214.3, 409.3 | 4.2 | 0.9 | Ground level |  |
| [Debtor](https://escapefromtarkov.fandom.com/wiki/Debtor) | Locate the debtor on Streets of Tarkov | -80.3, 50.5 | 6.0 | 4.3 | Ground level | **2nd Floor**: Pinewood room 206, second floor |
| [Debtor](https://escapefromtarkov.fandom.com/wiki/Debtor) | Locate the private prison warden's apartment on Streets of Tarkov | 107.9, 232.2 | 7.6 | 4.0 | Ground level | **2nd Floor**: Chekannaya 15, easternmost apartment on the second floor |
| [Gendarmerie - Mall Cop](https://escapefromtarkov.fandom.com/wiki/Gendarmerie_-_Mall_Cop) | Eliminate any target at the stylobate building while using Pistols on Streets of Tarkov | -97.2, -10.7 | 8.6 | 8.0 | Ground level |  |
| [Gendarmerie - Tickets, Please](https://escapefromtarkov.fandom.com/wiki/Gendarmerie_-_Tickets%2C_Please) | Eliminate any target at the Rodina cinema while using SMGs on Streets of Tarkov | -180.4, 399.5 | 16.5 | 13.7 | 3rd Floor |  |
| [Glory to CPSU](https://escapefromtarkov.fandom.com/wiki/Glory_to_CPSU) | Locate the place of work of Prapor's friend on Streets of Tarkov | 246.2, 52.4 | -0.3 | 5.6 | Ground level | **2nd Floor**: museum: room on the second floor |
| [Glory to CPSU](https://escapefromtarkov.fandom.com/wiki/Glory_to_CPSU) | Locate the apartment of Prapor's friend on Streets of Tarkov | 131.4, 232.4 | 7.6 | 4.0 | Ground level | **2nd Floor**: Chekannaya 15, second floor |
| [Glory to CPSU](https://escapefromtarkov.fandom.com/wiki/Glory_to_CPSU) | Obtain any information on the fate of Prapor's friend | 249.3, 57.8 | -0.6 | 5.4 | Ground level | **2nd Floor**: journal spawns in a room on the second floor |
| [Glory to CPSU](https://escapefromtarkov.fandom.com/wiki/Glory_to_CPSU) | Obtain any information on the fate of Prapor's friend | 245.6, 58.0 | -0.3 | 5.6 | Ground level | **2nd Floor**: journal spawns in a room on the second floor |
| [Glory to CPSU](https://escapefromtarkov.fandom.com/wiki/Glory_to_CPSU) | Obtain any information on the fate of Prapor's friend | 247.2, 51.1 | -0.5 | 5.5 | Ground level | **2nd Floor**: journal spawns in a room on the second floor |
| [Glory to CPSU](https://escapefromtarkov.fandom.com/wiki/Glory_to_CPSU) | Obtain any information on the fate of Prapor's friend | 245.9, 55.2 | -0.7 | 5.3 | Ground level | **2nd Floor**: journal spawns in a room on the second floor |
| [Glory to CPSU - Part 1](https://escapefromtarkov.fandom.com/wiki/Glory_to_CPSU_-_Part_1) | Locate the apartment of Prapor's friend on Streets of Tarkov | 131.4, 232.4 | 7.6 | 4.0 | Ground level | **2nd Floor**: Chekannaya 15, second floor |
| [Green Corridor](https://escapefromtarkov.fandom.com/wiki/Green_Corridor) | Locate the cargo convoy on Streets of Tarkov | 15.7, 226.6 | 3.4 | 1.1 | Ground level |  |
| [Green Corridor](https://escapefromtarkov.fandom.com/wiki/Green_Corridor) | Determine the ambush spot | 62.2, 272.8 | 7.1 | 4.3 | Ground level |  |
| [House Arrest](https://escapefromtarkov.fandom.com/wiki/House_Arrest) | Locate where the missing group was held captive on Streets of Tarkov | 127.1, 232.6 | 10.6 | 7.0 | 2nd Floor | **3rd Floor**: Chekannaya 15, cell no. 1 on the third floor |
| [House Arrest](https://escapefromtarkov.fandom.com/wiki/House_Arrest) | Locate the debtor on Streets of tarkov | -80.3, 50.5 | 6.0 | 4.3 | Ground level | **2nd Floor**: Pinewood room 206, second floor |
| [House Arrest - Part 2](https://escapefromtarkov.fandom.com/wiki/House_Arrest_-_Part_2) | Find out what happened to the warden | 106.8, 222.5 | 4.7 | 1.1 | Ground level |  |
| [House Arrest - Part 2](https://escapefromtarkov.fandom.com/wiki/House_Arrest_-_Part_2) | Locate the improvised jail warden's apartment on Streets of Tarkov | 107.9, 232.2 | 7.6 | 4.0 | Ground level | **2nd Floor**: Chekannaya 15, easternmost apartment on the second floor |
| [Is This a Reference?](https://escapefromtarkov.fandom.com/wiki/Is_This_a_Reference%3F) | Install a WI-FI Camera at the barbed wire body on Streets of Tarkov | 181.2, 228.7 | 1.2 | 0.5 | Ground level |  |
| [Is This a Reference?](https://escapefromtarkov.fandom.com/wiki/Is_This_a_Reference%3F) | Install a WI-FI Camera at the amphibian pizza lovers' hideout on Streets of Tarkov | -263.3, 206.4 | -2.0 |  | Ground level |  |
| [Is This a Reference?](https://escapefromtarkov.fandom.com/wiki/Is_This_a_Reference%3F) | Install a WI-FI Camera at the really scary hole in the wall on Streets of Tarkov | 209.4, 231.0 | 1.0 | 0.5 | Ground level |  |
| [Is This a Reference?](https://escapefromtarkov.fandom.com/wiki/Is_This_a_Reference%3F) | Install a WI-FI Camera at the burned girl's sickroom on Streets of Tarkov | 182.8, 111.7 | 2.5 | 2.7 | Ground level | **2nd Floor**: second floor of the children's polyclinic |
| [Key to the City](https://escapefromtarkov.fandom.com/wiki/Key_to_the_City) | Locate and obtain the souvenir key to the city on Streets of Tarkov | 246.7, 47.8 | -0.1 | 5.9 | Ground level | **2nd Floor**: museum: three spawns on the second floor |
| [Key to the City](https://escapefromtarkov.fandom.com/wiki/Key_to_the_City) | Locate and obtain the souvenir key to the city on Streets of Tarkov | 243.3, 53.0 | -3.6 | 2.3 | Ground level |  |
| [Key to the City](https://escapefromtarkov.fandom.com/wiki/Key_to_the_City) | Locate and obtain the souvenir key to the city on Streets of Tarkov | 248.3, 55.4 | -3.6 | 2.3 | Ground level |  |
| [Key to the City](https://escapefromtarkov.fandom.com/wiki/Key_to_the_City) | Locate and obtain the souvenir key to the city on Streets of Tarkov | 249.0, 53.8 | -3.6 | 2.3 | Ground level |  |
| [Key to the City](https://escapefromtarkov.fandom.com/wiki/Key_to_the_City) | Locate and obtain the souvenir key to the city on Streets of Tarkov | 245.7, 50.8 | -3.6 | 2.3 | Ground level |  |
| [Key to the City](https://escapefromtarkov.fandom.com/wiki/Key_to_the_City) | Locate and obtain the souvenir key to the city on Streets of Tarkov | 247.7, 58.8 | -0.4 | 5.5 | Ground level | **2nd Floor**: museum: three spawns on the second floor |
| [Key to the City](https://escapefromtarkov.fandom.com/wiki/Key_to_the_City) | Locate and obtain the souvenir key to the city on Streets of Tarkov | 243.0, 55.2 | -0.8 | 5.2 | Ground level | **2nd Floor**: museum: three spawns on the second floor |
| [Missing Informant](https://escapefromtarkov.fandom.com/wiki/Missing_Informant) | Locate the informant's backup hideout on Streets of Tarkov | -130.4, 396.5 | 3.2 | 0.9 | Ground level |  |
| [Missing Informant](https://escapefromtarkov.fandom.com/wiki/Missing_Informant) | Obtain the informant's journal | -129.3, 392.6 | 2.4 | 0.0 | Ground level |  |
| [Missing Informant](https://escapefromtarkov.fandom.com/wiki/Missing_Informant) | Obtain the informant's journal | -132.2, 397.6 | 2.4 | 0.0 | Ground level |  |
| [Missing Informant](https://escapefromtarkov.fandom.com/wiki/Missing_Informant) | Obtain the informant's journal | -127.9, 397.0 | 2.4 | 0.0 | Ground level |  |
| [Needle in a Haystack](https://escapefromtarkov.fandom.com/wiki/Needle_in_a_Haystack) | Investigate the children's playground by Concordia on Streets of Tarkov | 207.5, 360.2 | 6.9 | 8.2 | Ground level |  |
| [Paramedic](https://escapefromtarkov.fandom.com/wiki/Paramedic) | Locate and obtain the ambulance paramedic's smartphone on Streets of Tarkov | 157.9, 456.0 | 3.7 | 0.6 | Ground level |  |
| [Paramedic](https://escapefromtarkov.fandom.com/wiki/Paramedic) | Locate and obtain the ambulance paramedic's smartphone on Streets of Tarkov | 311.5, 413.4 | 3.4 |  | Ground level |  |
| [Paramedic](https://escapefromtarkov.fandom.com/wiki/Paramedic) | Locate and obtain the ambulance paramedic's smartphone on Streets of Tarkov | 223.7, 369.4 | 3.5 | 4.7 | Ground level |  |
| [Pets Won't Need It](https://escapefromtarkov.fandom.com/wiki/Pets_Won't_Need_It) | Locate and scout the vet clinic on Streets of Tarkov | 224.9, 172.8 | 4.8 | 4.4 | Ground level | **2nd Floor**: vet clinic: stairs to the 2nd floor |
| [Pets Won't Need It](https://escapefromtarkov.fandom.com/wiki/Pets_Won't_Need_It) | Locate and scout the x-ray technician's room on Streets of Tarkov | 183.0, 102 | 2.8 | 6.6 | Ground level | **2nd Floor**: polyclinic: go upstairs |
| [Pets Won't Need It](https://escapefromtarkov.fandom.com/wiki/Pets_Won't_Need_It) | Locate the first pharmacy on Primorsky Ave on Streets of Tarkov | 39.0, 162.4 | 3.6 | 0.9 | Ground level |  |
| [Pets Won't Need It](https://escapefromtarkov.fandom.com/wiki/Pets_Won't_Need_It) | Locate the second pharmacy on Primorsky Ave on Streets of Tarkov | -44.6, 336.1 | 4.2 | 1.0 | Ground level |  |
| [Pets Won't Need It](https://escapefromtarkov.fandom.com/wiki/Pets_Won't_Need_It) | Locate the pharmacy near Cardinal apartment complex on Streets of Tarkov | 89.3, -275.4 | 5.1 | 0.3 | Ground level |  |
| [Pets Won't Need It - Part 2](https://escapefromtarkov.fandom.com/wiki/Pets_Won't_Need_It_-_Part_2) | Locate the first pharmacy on Primorsky Ave on Streets of Tarkov | 39.0, 162.4 | 3.6 | 0.9 | Ground level |  |
| [Pets Won't Need It - Part 2](https://escapefromtarkov.fandom.com/wiki/Pets_Won't_Need_It_-_Part_2) | Locate the second pharmacy on Primorsky Ave on Streets of Tarkov | -44.6, 336.1 | 4.2 | 1.0 | Ground level |  |
| [Pets Won't Need It - Part 2](https://escapefromtarkov.fandom.com/wiki/Pets_Won't_Need_It_-_Part_2) | Locate the third pharmacy at Cardinal apartment complex on Streets of Tarkov | 89.3, -275.4 | 5.1 | 0.3 | Ground level |  |
| [Population Census](https://escapefromtarkov.fandom.com/wiki/Population_Census) | Obtain the journal containing resident details on Streets of Tarkov | 80.2, 143.7 | 3.9 | 2.8 | Ground level |  |
| [Properties All Around](https://escapefromtarkov.fandom.com/wiki/Properties_All_Around) | Locate the real estate fund on Streets of Tarkov | -58.3, 457.9 | 3.6 | 0.9 | Ground level |  |
| [Properties All Around](https://escapefromtarkov.fandom.com/wiki/Properties_All_Around) | Locate and obtain the Tarkov real estate transactions document | -66.8, 459.4 | 8.0 | 5.3 | Ground level | **2nd Floor**: real estate agency: spawns on the second floor |
| [Properties All Around](https://escapefromtarkov.fandom.com/wiki/Properties_All_Around) | Locate and obtain the Tarkov real estate transactions document | -41.5, 455.1 | 8.6 | 5.9 | Ground level | **2nd Floor**: real estate agency: spawns on the second floor |
| [Properties All Around](https://escapefromtarkov.fandom.com/wiki/Properties_All_Around) | Locate and obtain the Tarkov real estate transactions document | -66.8, 453.5 | 7.4 | 4.7 | Ground level | **2nd Floor**: real estate agency: spawns on the second floor |
| [Pyramid Scheme](https://escapefromtarkov.fandom.com/wiki/Pyramid_Scheme) | Mark any ATM on Klimov Street with an MS2000 Marker on Streets of Tarkov | 83.0, -30.5 | 1.2 | 1.0 | Ground level |  |
| [Pyramid Scheme](https://escapefromtarkov.fandom.com/wiki/Pyramid_Scheme) | Locate the first group of ATMs on Klimov Street on Streets of Tarkov | 97.4, -22.2 | 1.2 | 0.2 | Ground level |  |
| [Pyramid Scheme](https://escapefromtarkov.fandom.com/wiki/Pyramid_Scheme) | Locate the first ATM inside Klimov Shopping Mall on Streets of Tarkov | -148.6, -62.8 | 6.1 | 5.4 | Ground level |  |
| [Pyramid Scheme](https://escapefromtarkov.fandom.com/wiki/Pyramid_Scheme) | Locate the first ATM on Klimov Street on Streets of Tarkov | 83.0, -30.5 | 1.2 | 1.0 | Ground level |  |
| [Pyramid Scheme](https://escapefromtarkov.fandom.com/wiki/Pyramid_Scheme) | Locate the third ATM on Klimov Street on Streets of Tarkov | 8.3, 5.2 | -2.8 | 1.0 | Ground level |  |
| [Pyramid Scheme](https://escapefromtarkov.fandom.com/wiki/Pyramid_Scheme) | Locate the second ATM inside Klimov Shopping Mall on Streets of Tarkov | -113.9, -12.5 | 1.6 | 1.0 | Ground level |  |
| [Pyramid Scheme](https://escapefromtarkov.fandom.com/wiki/Pyramid_Scheme) | Locate the third ATM inside Klimov Shopping Mall on Streets of Tarkov | -166.5, -3.4 | 1.6 | 1.0 | Ground level |  |
| [Pyramid Scheme](https://escapefromtarkov.fandom.com/wiki/Pyramid_Scheme) | Locate the first group of ATMs inside Klimov Shopping Mall on Streets of Tarkov | -160.2, -47.8 | 1.6 | 0.9 | Ground level |  |
| [Pyramid Scheme](https://escapefromtarkov.fandom.com/wiki/Pyramid_Scheme) | Locate the second ATM on Klimov Street on Streets of Tarkov | 0.5, -18.8 | -2.7 | 1.0 | Ground level |  |
| [Pyramid Scheme](https://escapefromtarkov.fandom.com/wiki/Pyramid_Scheme) | Locate the second group of ATMs inside Klimov Shopping Mall on Streets of Tarkov | -35.2, -70.0 | 1.6 | 0.9 | Ground level |  |
| [Pyramid Scheme](https://escapefromtarkov.fandom.com/wiki/Pyramid_Scheme) | Locate the third group of ATMs inside Klimov Shopping Mall on Streets of Tarkov | -53.6, -69.3 | 1.6 | 0.9 | Ground level |  |
| [Revision - Streets of Tarkov](https://escapefromtarkov.fandom.com/wiki/Revision_-_Streets_of_Tarkov) | Locate and mark the first LAV III with an MS2000 Marker on Streets of Tarkov | -139.4, 438.8 | 3.6 |  | Ground level |  |
| [Revision - Streets of Tarkov](https://escapefromtarkov.fandom.com/wiki/Revision_-_Streets_of_Tarkov) | Locate and mark the Stryker with an MS2000 Marker on Streets of Tarkov | 146.3, 408.4 | 4.7 | 1.2 | Ground level |  |
| [Revision - Streets of Tarkov](https://escapefromtarkov.fandom.com/wiki/Revision_-_Streets_of_Tarkov) | Locate and mark the second LAV III with an MS2000 Marker on Streets of Tarkov | 2.2, 34.0 | 0.9 |  | Ground level |  |
| [Road Closed](https://escapefromtarkov.fandom.com/wiki/Road_Closed) | Determine the ambush spot | 62.2, 272.8 | 7.1 | 4.3 | Ground level |  |
| [Road Closed](https://escapefromtarkov.fandom.com/wiki/Road_Closed) | Locate the cargo convoy on Streets of Tarkov | 15.7, 226.6 | 3.4 | 1.1 | Ground level |  |
| [Route Deviation](https://escapefromtarkov.fandom.com/wiki/Route_Deviation) | Mark the Collapsed Crane BTR stop with an MS2000 Marker on Streets of Tarkov | 195.2, 257.0 | 4.1 | 0.7 | Ground level |  |
| [Route Deviation](https://escapefromtarkov.fandom.com/wiki/Route_Deviation) | Mark the Old Scav Checkpoint BTR stop with an MS2000 Marker on Streets of Tarkov | 115.6, 25.8 | -1.6 | -0.5 | Ground level |  |
| [Route Deviation](https://escapefromtarkov.fandom.com/wiki/Route_Deviation) | Mark the Pinewood Hotel BTR stop with an MS2000 Marker on Streets of Tarkov | -133.1, 63.9 | 1.5 | 0.7 | Ground level |  |
| [Route Deviation](https://escapefromtarkov.fandom.com/wiki/Route_Deviation) | Mark the City Center BTR stop with an MS2000 Marker on Streets of Tarkov | -13.1, 218.3 | 3.2 | 1.0 | Ground level |  |
| [Route Deviation](https://escapefromtarkov.fandom.com/wiki/Route_Deviation) | Mark the Tram BTR stop with an MS2000 Marker on Streets of Tarkov | -233.7, 235.9 | 3.3 | 1.1 | Ground level |  |
| [Route Deviation](https://escapefromtarkov.fandom.com/wiki/Route_Deviation) | Mark the Rodina Cinema BTR stop with an MS2000 Marker on Streets of Tarkov | -137.7, 400.4 | 2.8 | 0.5 | Ground level |  |
| [Spotter](https://escapefromtarkov.fandom.com/wiki/Spotter) | Locate a good sniping position in Concordia overlooking the construction site | 219.4, 397.5 | 10.3 | 7.0 | 2nd Floor | **3rd Floor**: Concordia apartment 8, third floor |
| [Spotter](https://escapefromtarkov.fandom.com/wiki/Spotter) | Locate a good sniping position in Concordia overlooking the construction site | 225.0, 396.7 | 10.3 | 7.0 | 2nd Floor | **3rd Floor**: Concordia apartment 8, third floor |
| [Spotter](https://escapefromtarkov.fandom.com/wiki/Spotter) | Locate a good sniping position in Concordia overlooking the construction site | 214.8, 398.1 | 10.3 | 7.0 | 2nd Floor | **3rd Floor**: Concordia apartment 8, third floor |
| [Spotter](https://escapefromtarkov.fandom.com/wiki/Spotter) | Hide AI Tactical Sound Moderator .338 LM near the red table | 228.2, 396.7 | 9.9 | 6.5 | Ground level | **3rd Floor**: Concordia apartment 8, third floor |
| [Spotter](https://escapefromtarkov.fandom.com/wiki/Spotter) | Hide AI Tactical Sound Moderator .338 LM near the red table | 218.2, 396.3 | 9.9 | 6.6 | Ground level | **3rd Floor**: Concordia apartment 8, third floor |
| [Spotter](https://escapefromtarkov.fandom.com/wiki/Spotter) | Hide AI Tactical Sound Moderator .338 LM near the red table | 215.8, 395.9 | 9.8 | 6.4 | Ground level | **3rd Floor**: Concordia apartment 8, third floor |
| [Spotter](https://escapefromtarkov.fandom.com/wiki/Spotter) | Locate a good sniping position at Primorsky overlooking the movie theater | 37.0, 88.2 | 11.1 | 9.4 | 2nd Floor |  |
| [Spotter](https://escapefromtarkov.fandom.com/wiki/Spotter) | Locate a good sniping position at Primorsky overlooking the movie theater | 37.9, 155.8 | 12.7 | 9.9 | 2nd Floor | **4th Floor**: Primorsky 48 apartment 10, fourth floor |
| [Spotter](https://escapefromtarkov.fandom.com/wiki/Spotter) | Hide Trijicon REAP-IR thermal scope under Makhors' bed | 38.0, 156.2 | 12.2 | 9.4 | 2nd Floor | **4th Floor**: Primorsky 48 apartment 10, fourth floor |
| [Surveillance](https://escapefromtarkov.fandom.com/wiki/Surveillance) | Obtain the data on vehicle movement at the Concordia residential complex parking lot on Streets of Tarkov | 213.2, 410.3 | -0.9 | -4.2 | Ground level |  |
| [Surveillance](https://escapefromtarkov.fandom.com/wiki/Surveillance) | Obtain the data on vehicle movement at the Concordia residential complex parking lot on Streets of Tarkov | 208.7, 408.6 | -0.4 | -0.2 | Ground level |  |
| [Surveillance](https://escapefromtarkov.fandom.com/wiki/Surveillance) | Obtain the data on vehicle movement at the Concordia residential complex parking lot on Streets of Tarkov | 208.4, 412.1 | -0.4 | -0.2 | Ground level |  |
| [Surveillance](https://escapefromtarkov.fandom.com/wiki/Surveillance) | Obtain the data on vehicle movement at the Concordia residential complex parking lot on Streets of Tarkov | 210.5, 407.5 | -0.8 | -4.1 | Ground level |  |
| [The Delicious Sausage](https://escapefromtarkov.fandom.com/wiki/The_Delicious_Sausage) | Scout the Shestyorochka store at Nikitskaya street | -204.3, 181.2 | 4.3 | 0.9 | Ground level |  |
| [The Delicious Sausage](https://escapefromtarkov.fandom.com/wiki/The_Delicious_Sausage) | Scout the Sparja store at Primorsky ave | 153.7, 299.0 | 4.7 | 0.9 | Ground level |  |
| [The Delicious Sausage](https://escapefromtarkov.fandom.com/wiki/The_Delicious_Sausage) | Scout the Sparja store in Pinewood hotel | -77.2, 158.9 | 2.3 | 0.9 | Ground level |  |
| [The Delicious Sausage](https://escapefromtarkov.fandom.com/wiki/The_Delicious_Sausage) | Scout the Goshan store in Concordia | 275.6, 380.8 | 4.3 | 5.5 | Ground level |  |
| [The Door](https://escapefromtarkov.fandom.com/wiki/The_Door) | Locate the cause of the signal interference on Streets of Tarkov | 184.4, 55.6 | 6.8 | 11.2 | Ground level | **4th Floor**: behind the locked door on the fourth floor |
| [The Door](https://escapefromtarkov.fandom.com/wiki/The_Door) | Install a WI-FI Camera to watch the door | 183.9, 53.4 | 6.1 | 10.5 | Ground level | **4th Floor**: locked door on the fourth floor |
| [The Door](https://escapefromtarkov.fandom.com/wiki/The_Door) | Install a WI-FI Camera to watch the stairwell | 176.3, 82.2 | 6.3 | 10.6 | Ground level | **4th Floor**: staircase on the fourth floor |
| [The Secret Recipe](https://escapefromtarkov.fandom.com/wiki/The_Secret_Recipe) | Locate and obtain the red vial at the TerraGroup office on Streets of Tarkov | 41.6, -53.9 | 1.6 | 1.3 | Ground level |  |
| [The Secret Recipe](https://escapefromtarkov.fandom.com/wiki/The_Secret_Recipe) | Locate and obtain the red vial at the TerraGroup office on Streets of Tarkov | 58.5, -72.8 | 0.9 | 0.3 | Ground level |  |
| [The Secret Recipe](https://escapefromtarkov.fandom.com/wiki/The_Secret_Recipe) | Locate and obtain the red vial at the TerraGroup office on Streets of Tarkov | -28.5, -117.1 | 7.4 | 4.5 | Ground level |  |
| [The Secret Recipe](https://escapefromtarkov.fandom.com/wiki/The_Secret_Recipe) | Locate and obtain the red vial at the TerraGroup office on Streets of Tarkov | -27.5, -109.5 | 7.4 | 0.8 | Ground level |  |
| [The Secret Recipe](https://escapefromtarkov.fandom.com/wiki/The_Secret_Recipe) | Locate and obtain the red vial at the TerraGroup office on Streets of Tarkov | -41.2, -110.1 | 7.6 | 0.9 | Ground level |  |
| [The Secret to Productivity](https://escapefromtarkov.fandom.com/wiki/The_Secret_to_Productivity) | Unravel the secret of the IT firm's employees' high morale on Streets of Tarkov | -211.8, 297.3 | 4.2 | 1.2 | Ground level |  |
| [The Tarkov Butcher](https://escapefromtarkov.fandom.com/wiki/The_Tarkov_Butcher) | Stash the container by the police station on Streets of Tarkov | -209.7, 135.3 | 4.9 |  | Ground level |  |
| [Trouble in the Big City](https://escapefromtarkov.fandom.com/wiki/Trouble_in_the_Big_City) | Locate the armored convoy holding the cargo on Streets of Tarkov | 15.7, 226.6 | 3.4 | 1.1 | Ground level |  |
| [Trouble in the Big City](https://escapefromtarkov.fandom.com/wiki/Trouble_in_the_Big_City) | Mark the cargo area with an MS2000 Marker | 10.5, 217.6 | 4.8 | 2.5 | Ground level |  |
| [Trouble in the Big City](https://escapefromtarkov.fandom.com/wiki/Trouble_in_the_Big_City) | Launch a yellow flare near the armored convoy | 9.7, 217.2 | 8.6 | 6.4 | Ground level |  |
| [Urban Medicine](https://escapefromtarkov.fandom.com/wiki/Urban_Medicine) | Locate the chemical laboratory on Streets of Tarkov | 93.0, 320.4 | 3.6 | 0.8 | Ground level |  |
| [Urban Medicine](https://escapefromtarkov.fandom.com/wiki/Urban_Medicine) | Obtain the container with drug samples | 95.9, 319.1 | 2.7 | -0.2 | Ground level |  |
| [Urban Medicine](https://escapefromtarkov.fandom.com/wiki/Urban_Medicine) | Obtain the container with drug samples | 91.2, 323.2 | 2.7 | -0.2 | Ground level |  |
| [Watching You](https://escapefromtarkov.fandom.com/wiki/Watching_You) | Locate the surveillance spot on Streets of Tarkov | -67.8, 65.9 | 6.0 | 4.3 | Ground level | **2nd Floor**: Pinewood room 215, second floor |
| [Watching You](https://escapefromtarkov.fandom.com/wiki/Watching_You) | Obtain the observation results | -70.1, 69.4 | 5.8 | 4.1 | Ground level | **2nd Floor**: Pinewood room 215, second floor |
| [Watching You](https://escapefromtarkov.fandom.com/wiki/Watching_You) | Obtain the observation results | -65.3, 66.4 | 5.9 | 4.2 | Ground level | **2nd Floor**: Pinewood room 215, second floor |
| [You've Got Mail](https://escapefromtarkov.fandom.com/wiki/You've_Got_Mail) | Locate and obtain the registered mail on Streets of Tarkov | 39.5, 113.5 | 1.2 | -0.2 | Ground level |  |
| [You've Got Mail](https://escapefromtarkov.fandom.com/wiki/You've_Got_Mail) | Locate and obtain the registered mail on Streets of Tarkov | 42.4, 118.8 | 1.9 | 0.5 | Ground level |  |
| [You've Got Mail](https://escapefromtarkov.fandom.com/wiki/You've_Got_Mail) | Locate and obtain the registered mail on Streets of Tarkov | 39.2, 117.7 | 1.5 | 0.1 | Ground level |  |
| [You've Got Mail](https://escapefromtarkov.fandom.com/wiki/You've_Got_Mail) | Locate and obtain the registered mail on Streets of Tarkov | 36.1, 126.6 | 1.3 | -0.1 | Ground level |  |
| [Your Car Needs a Service](https://escapefromtarkov.fandom.com/wiki/Your_Car_Needs_a_Service) | Obtain the digital storage device from the car dealership manager's office on Streets of Tarkov | 66.8, 303.1 | 7.7 | 4.7 | Ground level | **2nd Floor**: LexOs director's office, second floor |

### The Lab

| Task | Step | x, z | y | Above ground | Floor | Wiki floor |
|---|---|---|---|---|---|---|
| [Beneath The Streets](https://escapefromtarkov.fandom.com/wiki/Beneath_The_Streets) | Scout the server room in The Lab (In one raid) | -127.1, -309.3 | 5.2 | 9.2 | Second Level |  |
| [Beneath The Streets](https://escapefromtarkov.fandom.com/wiki/Beneath_The_Streets) | Locate the passage leading to Streets of Tarkov in The Lab (In one raid) | -170.0, -419.2 | 0.9 | 0.9 | Ground level |  |
| [Beneath The Streets](https://escapefromtarkov.fandom.com/wiki/Beneath_The_Streets) | Scout the hazard dome in The Lab (In one raid) | -172.4, -370.9 | 1.1 | 3.9 | Ground level |  |
| [Beneath The Streets](https://escapefromtarkov.fandom.com/wiki/Beneath_The_Streets) | Scout the control room in The Lab (In one raid) | -170.8, -283.1 | 5.1 | 5.1 | Second Level |  |
| [Following the Bread Crumbs](https://escapefromtarkov.fandom.com/wiki/Following_the_Bread_Crumbs) | Search the weapon testing area in The Lab | -182.9, -312.9 | 1.3 | 4.0 | Ground level |  |
| [Following the Bread Crumbs](https://escapefromtarkov.fandom.com/wiki/Following_the_Bread_Crumbs) | Search the human experiment room in The Lab | -131.5, -357.8 | 1 | 0.8 | Ground level |  |
| [Following the Bread Crumbs](https://escapefromtarkov.fandom.com/wiki/Following_the_Bread_Crumbs) | Obtain the secured tape inside the manager's office in The Lab | -178.3, -344.9 | 5.0 | 9.0 | Second Level |  |
| [Following the Bread Crumbs](https://escapefromtarkov.fandom.com/wiki/Following_the_Bread_Crumbs) | Obtain the secured tape inside the manager's office in The Lab | -160.8, -340.5 | 4.5 | 8.5 | Second Level |  |
| [Following the Bread Crumbs](https://escapefromtarkov.fandom.com/wiki/Following_the_Bread_Crumbs) | Obtain the secured tape inside the manager's office in The Lab | -169.1, -342.1 | 5.2 | 9.1 | Second Level |  |
| [Following the Bread Crumbs](https://escapefromtarkov.fandom.com/wiki/Following_the_Bread_Crumbs) | Obtain the secured tape inside the manager's office in The Lab | -161.4, -346.9 | 4.8 | 8.8 | Second Level |  |
| [Following the Bread Crumbs](https://escapefromtarkov.fandom.com/wiki/Following_the_Bread_Crumbs) | Obtain the secured tape inside the manager's office in The Lab | -163.1, -342.1 | 4.8 | 8.8 | Second Level |  |
| [Following the Bread Crumbs](https://escapefromtarkov.fandom.com/wiki/Following_the_Bread_Crumbs) | Obtain the secured tape inside the manager's office in The Lab | -170.8, -343.6 | 5.1 | 9.0 | Second Level |  |
| [Following the Bread Crumbs](https://escapefromtarkov.fandom.com/wiki/Following_the_Bread_Crumbs) | Obtain the secured tape inside the manager's office in The Lab | -178.5, -343.6 | 5.0 | 9.0 | Second Level |  |
| [Following the Bread Crumbs](https://escapefromtarkov.fandom.com/wiki/Following_the_Bread_Crumbs) | Obtain the secured tape inside the manager's office in The Lab | -167.9, -343.6 | 4.1 | 8.1 | Second Level |  |
| [Health Care Privacy - Part 6](https://escapefromtarkov.fandom.com/wiki/Health_Care_Privacy_-_Part_6) | Stash the blood sample in Sanitar's office in The Lab | -131.9, -336.9 | 5.4 | 9.2 | Second Level |  |
| [Quality Standard](https://escapefromtarkov.fandom.com/wiki/Quality_Standard) | Locate and obtain the special version of the LEDX Skin Transilluminator in The Lab | -173.7, -374.4 | 1.3 | 1.2 | Ground level |  |
| [TerraGroup Employee](https://escapefromtarkov.fandom.com/wiki/TerraGroup_Employee) | Locate and obtain any information about Sanitar's work | -133.0, -335.2 | 5.0 | 9.0 | Second Level |  |
| [TerraGroup Employee](https://escapefromtarkov.fandom.com/wiki/TerraGroup_Employee) | Locate Sanitar's workplace in The Lab | -131.9, -336.9 | 5.4 | 9.2 | Second Level |  |

### The Labyrinth (no floor layers)

| Task | Step | x, z | y | Above ground | Floor | Wiki floor |
|---|---|---|---|---|---|---|
| [Confidential Info](https://escapefromtarkov.fandom.com/wiki/Confidential_Info) | Locate and obtain the special storage module inside The Labyrinth | -8.0, 30.3 | 0.8 | 0.7 | Ground level |  |
| [Confidential Info](https://escapefromtarkov.fandom.com/wiki/Confidential_Info) | Locate and obtain the special storage module inside The Labyrinth | -4.7, 36.1 | 0.8 | 0.7 | Ground level |  |
| [Confidential Info](https://escapefromtarkov.fandom.com/wiki/Confidential_Info) | Locate and obtain the special storage module inside The Labyrinth | -10.5, 22.7 | 0.8 | 0.7 | Ground level |  |
| [Confidential Info](https://escapefromtarkov.fandom.com/wiki/Confidential_Info) | Locate and obtain the special storage module inside The Labyrinth | -5.4, 27.0 | 1.1 | 1.0 | Ground level |  |
| [Confidential Info](https://escapefromtarkov.fandom.com/wiki/Confidential_Info) | Locate and obtain the special storage module inside The Labyrinth | -9.5, 26.2 | 0.9 | 0.7 | Ground level |  |
| [Confidential Info](https://escapefromtarkov.fandom.com/wiki/Confidential_Info) | Locate and obtain the special storage module inside The Labyrinth | -11.0, 26.0 | 0.8 | 0.6 | Ground level |  |
| [Confidential Info](https://escapefromtarkov.fandom.com/wiki/Confidential_Info) | Plant a hand grenade in the assembly workshop inside The Labyrinth | -9.1, 27.6 | 1 | 0.9 | Ground level |  |
| [Hypotheses Testing](https://escapefromtarkov.fandom.com/wiki/Hypotheses_Testing) | Locate the lab area with the prototype weapon inside The Labyrinth | -8.4, 30 | 0 | -0.1 | Ground level |  |
| [Keeper's Word](https://escapefromtarkov.fandom.com/wiki/Keeper's_Word) | Stash a Cultist knife in the first special place inside The Labyrinth | -23.2, 19 | 1 | 0.9 | Ground level |  |
| [Keeper's Word](https://escapefromtarkov.fandom.com/wiki/Keeper's_Word) | Stash a Cultist knife in the second special place inside The Labyrinth | 15.6, 19 | 1 | 0.9 | Ground level |  |
| [Keeper's Word](https://escapefromtarkov.fandom.com/wiki/Keeper's_Word) | Stash a Cultist knife in the third special place inside The Labyrinth | 9.2, -14.8 | 1 | 0.8 | Ground level |  |
| [Offensive Reconnaissance](https://escapefromtarkov.fandom.com/wiki/Offensive_Reconnaissance) | Find out what is behind the Health Resort bunker door on Shoreline | 0, 0 | 0 | -0.2 | Ground level |  |
| [This Tape Sucks](https://escapefromtarkov.fandom.com/wiki/This_Tape_Sucks) | Locate the torture room inside The Labyrinth | 17, 6.5 | 0 | -0.2 | Ground level |  |
| [This Tape Sucks](https://escapefromtarkov.fandom.com/wiki/This_Tape_Sucks) | Locate and obtain any evidence of torture | 13.8, 3.1 | 0.7 | 0.5 | Ground level |  |
| [This Tape Sucks](https://escapefromtarkov.fandom.com/wiki/This_Tape_Sucks) | Locate and obtain any evidence of torture | 12.3, 19.4 | 1.0 | 0.9 | Ground level |  |
| [This Tape Sucks](https://escapefromtarkov.fandom.com/wiki/This_Tape_Sucks) | Locate and obtain any evidence of torture | 12.6, 11.8 | 0.1 | -0.1 | Ground level |  |
| [This Tape Sucks](https://escapefromtarkov.fandom.com/wiki/This_Tape_Sucks) | Locate and obtain any evidence of torture | 17.6, 6.3 | 0.0 | -0.1 | Ground level |  |
| [Work Smarter](https://escapefromtarkov.fandom.com/wiki/Work_Smarter) | Locate the secret exfil on Customs | 19.4, 0.5 | 1.1 | 0.9 | Ground level |  |

### Woods (no floor layers)

| Task | Step | x, z | y | Above ground | Floor | Wiki floor |
|---|---|---|---|---|---|---|
| [A Helping Hand](https://escapefromtarkov.fandom.com/wiki/A_Helping_Hand) | Locate and obtain Prapor's package on Woods | -612.8, 136.1 | 9.2 | 0.7 | Ground level |  |
| [A Helping Hand](https://escapefromtarkov.fandom.com/wiki/A_Helping_Hand) | Locate and obtain Prapor's package on Woods | -619.2, 127.9 | 8.5 | -0.1 | Ground level |  |
| [Airmail](https://escapefromtarkov.fandom.com/wiki/Airmail) | Launch a red signal flare at the old sawmill on Woods | -518.1, -182.4 | 18.2 | 4.1 | Ground level |  |
| [Another Shipping Delay](https://escapefromtarkov.fandom.com/wiki/Another_Shipping_Delay) | Locate the missing courier crew on Woods | -44.4, -251.5 | 20.6 |  | Ground level |  |
| [Capturing Outposts](https://escapefromtarkov.fandom.com/wiki/Capturing_Outposts) | Eliminate PMC operatives at the specified Scav bases on Customs, Shoreline, or Woods | -198.8, 222 | 5.1 | 6.8 | Ground level |  |
| [Chumming](https://escapefromtarkov.fandom.com/wiki/Chumming) | Stash Golden neck chains in the middle wooden cabin at the sawmill on Woods | -6.2, -75.5 | -0.5 | 1.0 | Ground level |  |
| [Discombobulate](https://escapefromtarkov.fandom.com/wiki/Discombobulate) | Stash a VOG-25 Khattabka grenade at the first RPG ammo crate on Woods | -14.5, 48.6 | -2.7 | 0.1 | Ground level |  |
| [Discombobulate](https://escapefromtarkov.fandom.com/wiki/Discombobulate) | Stash a VOG-25 Khattabka grenade at the second RPG ammo crate on Woods | 237.8, -68.9 | -1.1 | 1.0 | Ground level |  |
| [Discombobulate](https://escapefromtarkov.fandom.com/wiki/Discombobulate) | Stash a VOG-25 Khattabka grenade at the third RPG ammo crate on Woods | -93.5, -380.0 | 27.4 |  | Ground level |  |
| [Fair Price - Part 2](https://escapefromtarkov.fandom.com/wiki/Fair_Price_-_Part_2) | Locate the stash spot | -542.4, -203.9 | 18.4 | 3.0 | Ground level |  |
| [Fair Price - Part 2](https://escapefromtarkov.fandom.com/wiki/Fair_Price_-_Part_2) | Locate and obtain the AK-50 handguard at the old sawmill on Woods | -544.4, -204.0 | 19.2 | 3.8 | Ground level |  |
| [Fair Price - Part 2](https://escapefromtarkov.fandom.com/wiki/Fair_Price_-_Part_2) | Locate and obtain the AK-50 handguard at the old sawmill on Woods | -549.1, -200.8 | 19.0 | 3.6 | Ground level |  |
| [Fair Price - Part 2](https://escapefromtarkov.fandom.com/wiki/Fair_Price_-_Part_2) | Locate and obtain the AK-50 handguard at the old sawmill on Woods | -547.7, -198.3 | 15.7 | 0.3 | Ground level |  |
| [Gratitude](https://escapefromtarkov.fandom.com/wiki/Gratitude) | Stash a Shemagh (Green) at the sawmill docks on Woods | 23.8, 99.8 | -15.4 |  | Ground level |  |
| [Gratitude](https://escapefromtarkov.fandom.com/wiki/Gratitude) | Stash RayBench Hipster Reserve sunglasses at the sawmill docks on Woods | 23.8, 99.8 | -15.4 |  | Ground level |  |
| [Health Care Privacy - Part 3](https://escapefromtarkov.fandom.com/wiki/Health_Care_Privacy_-_Part_3) | Take a sample of the blood | -94.3, 219.0 | -15.7 |  | Ground level |  |
| [Health Care Privacy - Part 3](https://escapefromtarkov.fandom.com/wiki/Health_Care_Privacy_-_Part_3) | Locate the van of the Health Resort medical services director on Woods | -97.2, 219.8 | -13.2 |  | Ground level |  |
| [Hiking](https://escapefromtarkov.fandom.com/wiki/Hiking) | Eliminate Scavs at USEC camp, Scav camp, sawmill, or abandoned village on Woods | 125, -378 | 25 |  | Ground level |  |
| [Hindsight 20/20](https://escapefromtarkov.fandom.com/wiki/Hindsight_20%2F20) | Stash the first Russian armor-piercing ammo pack inside the bunker | -273.6, -411.1 | 8.1 | 0.8 | Ground level |  |
| [Hindsight 20/20](https://escapefromtarkov.fandom.com/wiki/Hindsight_20%2F20) | Stash the second Russian armor-piercing ammo pack inside the bunker | -269.8, -412.4 | 8.1 | 0.8 | Ground level |  |
| [Hindsight 20/20](https://escapefromtarkov.fandom.com/wiki/Hindsight_20%2F20) | Locate the bunker under the mountain on Woods | -284.0, -414.3 | 14.5 | 7.1 | Ground level |  |
| [Hindsight 20/20](https://escapefromtarkov.fandom.com/wiki/Hindsight_20%2F20) | Stash the third Russian armor-piercing ammo pack inside the bunker | -269.2, -416 | 8.1 | 0.8 | Ground level |  |
| [Ice Cream Cones](https://escapefromtarkov.fandom.com/wiki/Ice_Cream_Cones) | Locate the locked bunker on Woods | 443.0, 67.7 | -15.0 | -1.1 | Ground level |  |
| [Informed Means Armed](https://escapefromtarkov.fandom.com/wiki/Informed_Means_Armed) | Install a WI-FI Camera to watch the sawmill dock on Woods | 31.1, 83.0 | -13.6 |  | Ground level |  |
| [Introduction](https://escapefromtarkov.fandom.com/wiki/Introduction) | Find Jaeger's camp at the specified spot on Woods | -256, 9.7 | 9.6 |  | Ground level |  |
| [Introduction](https://escapefromtarkov.fandom.com/wiki/Introduction) | Obtain Jaeger's encrypted message | -257.1, 8.0 | 8.5 |  | Ground level |  |
| [Is This a Reference?](https://escapefromtarkov.fandom.com/wiki/Is_This_a_Reference%3F) | Install a WI-FI Camera at the bear who sat into a flaming car on Woods | -116.9, -464.1 | 22.5 |  | Ground level |  |
| [Killer Argument](https://escapefromtarkov.fandom.com/wiki/Killer_Argument) | Locate and obtain the package with RPG ammo on Woods | 344.3, 233.9 | -13.5 |  | Ground level |  |
| [Killer Argument](https://escapefromtarkov.fandom.com/wiki/Killer_Argument) | Locate and obtain the package with RPG ammo on Woods | 406.7, 228.5 | -12.6 |  | Ground level |  |
| [Killer Argument](https://escapefromtarkov.fandom.com/wiki/Killer_Argument) | Locate and obtain the package with RPG ammo on Woods | 409.4, 240.5 | -13.5 |  | Ground level |  |
| [Killer Argument](https://escapefromtarkov.fandom.com/wiki/Killer_Argument) | Locate and obtain the package with RPG ammo on Woods | 361.6, 201.5 | -13.9 |  | Ground level |  |
| [Killer Argument](https://escapefromtarkov.fandom.com/wiki/Killer_Argument) | Locate and obtain the package with RPG ammo on Woods | 368.4, 251.7 | -14.8 |  | Ground level |  |
| [Metal Birds](https://escapefromtarkov.fandom.com/wiki/Metal_Birds) | Locate and obtain the motor controller on Woods | 233.8, -71.1 | -1.2 | 0.8 | Ground level |  |
| [Metal Birds](https://escapefromtarkov.fandom.com/wiki/Metal_Birds) | Locate and obtain the single-axis fiber optic gyroscope on Woods | 56.7, -50.3 | -1.8 | 0.5 | Ground level |  |
| [One Less Loose End](https://escapefromtarkov.fandom.com/wiki/One_Less_Loose_End) | Stash the journal at the old sawmill on Woods | -510.9, -178.2 | 17.1 | 4.5 | Ground level |  |
| [Order From Outside](https://escapefromtarkov.fandom.com/wiki/Order_From_Outside) | Stash the device at the specified location on Woods | -56.4, -496.8 | 9.2 | 0.3 | Ground level |  |
| [Proper Comeback](https://escapefromtarkov.fandom.com/wiki/Proper_Comeback) | Stash a Golden rooster figurine at Prapor's WI-FI Camera on Woods | -219.8, -220.0 | 62.6 | 32.0 | Ground level |  |
| [Protect the Sky](https://escapefromtarkov.fandom.com/wiki/Protect_the_Sky) | Locate the package in the specified spot on Woods | -57.9, -501.5 | 9.0 | 0.1 | Ground level |  |
| [Protect the Sky](https://escapefromtarkov.fandom.com/wiki/Protect_the_Sky) | Locate the package in the specified spot on Woods | -54.6, -494.3 | 8.9 | -0.1 | Ground level |  |
| [Protect the Sky](https://escapefromtarkov.fandom.com/wiki/Protect_the_Sky) | Locate the package in the specified spot on Woods | -51.3, -500.9 | 9.2 | 0.2 | Ground level |  |
| [Protect the Sky](https://escapefromtarkov.fandom.com/wiki/Protect_the_Sky) | Locate the package in the specified spot on Woods | -59.9, -491.7 | 8.9 | -0.0 | Ground level |  |
| [Protect the Sky](https://escapefromtarkov.fandom.com/wiki/Protect_the_Sky) | Locate the package in the specified spot on Woods | -54.8, -495.8 | 8.8 | -0.1 | Ground level |  |
| [Return the Favor](https://escapefromtarkov.fandom.com/wiki/Return_the_Favor) | Hide the TerraGroup "Blue Folders" materials inside the black SUV at the USEC camp on Woods | 290.0, -439.0 | 23.5 | 0.5 | Ground level |  |
| [Return the Favor](https://escapefromtarkov.fandom.com/wiki/Return_the_Favor) | Hide the TerraGroup "Blue Folders" materials in the crates near the satellite antenna at the USEC camp on Woods | 292.5, -507.4 | 23.4 | 0.2 | Ground level |  |
| [Rough Tarkov](https://escapefromtarkov.fandom.com/wiki/Rough_Tarkov) | Locate the heavily mined area at the USEC camp on Woods | 337.3, -490.9 | 18.7 |  | Ground level |  |
| [Saving Private Roman](https://escapefromtarkov.fandom.com/wiki/Saving_Private_Roman) | Mark the transit to Lighthouse with an MS2000 Marker on Woods | 496.7, 347.8 | -16.7 | 2.4 | Ground level |  |
| [Search Mission](https://escapefromtarkov.fandom.com/wiki/Search_Mission) | Locate Prapor's missing convoy on Woods | 195.6, -595.8 | 12.2 | 1.4 | Ground level |  |
| [Search Mission](https://escapefromtarkov.fandom.com/wiki/Search_Mission) | Locate the temporary USEC camp on Woods | 283.1, -439.4 | 24.0 | 1.1 | Ground level |  |
| [Shipping Delay - Part 2](https://escapefromtarkov.fandom.com/wiki/Shipping_Delay_-_Part_2) | Locate and scout the office at the depot on Woods | -615.0, 129.6 | 9.7 | 1.2 | Ground level |  |
| [Shipping Delay - Part 2](https://escapefromtarkov.fandom.com/wiki/Shipping_Delay_-_Part_2) | Locate and scout the warehouses at the depot on Woods | -616.0, 156.4 | 9.7 | 1.5 | Ground level |  |
| [Shipping Delay - Part 2](https://escapefromtarkov.fandom.com/wiki/Shipping_Delay_-_Part_2) | Locate and scout the garages at the depot on Woods | -687.5, 105.0 | 9.7 | 1.5 | Ground level |  |
| [Simple Side Job](https://escapefromtarkov.fandom.com/wiki/Simple_Side_Job) | Stash the cargo at the Scav house on Woods | 413.5, 240.5 | -12.6 |  | Ground level |  |
| [Sisyphus](https://escapefromtarkov.fandom.com/wiki/Sisyphus) | Locate and obtain the first smuggler case in the ZB-014 bunker on Woods | 444.3, 66.9 | -13.7 | 0.1 | Ground level |  |
| [Sisyphus](https://escapefromtarkov.fandom.com/wiki/Sisyphus) | Locate and obtain the second smuggler case behind the shack at the USEC checkpoint on Woods | 243.7, -80.5 | -1.4 | 0.7 | Ground level |  |
| [Small Business - Part 3](https://escapefromtarkov.fandom.com/wiki/Small_Business_-_Part_3) | Stash a Cultist knife at the river village marked circle on Woods | 196.0, -7.2 | 1.0 |  | Ground level |  |
| [Small Business - Part 3](https://escapefromtarkov.fandom.com/wiki/Small_Business_-_Part_3) | Stash a Cultist knife at the sawmill marked circle on Woods | -88.7, -717.6 | 12.6 | 0.3 | Ground level |  |
| [Small Things, Big Help](https://escapefromtarkov.fandom.com/wiki/Small_Things%2C_Big_Help) | Locate and mark the first fuel stash with an MS2000 Marker on Woods | 356.4, -85.9 | 0.3 | 2.3 | Ground level |  |
| [Small Things, Big Help](https://escapefromtarkov.fandom.com/wiki/Small_Things%2C_Big_Help) | Locate and mark the second fuel stash with an MS2000 Marker on Woods | -325.0, 24.0 | 15.3 |  | Ground level |  |
| [Small Things, Big Help](https://escapefromtarkov.fandom.com/wiki/Small_Things%2C_Big_Help) | Locate and mark the third fuel stash with an MS2000 Marker on Woods | -200.4, -210.9 | 31.3 | 0.7 | Ground level |  |
| [Special Comms](https://escapefromtarkov.fandom.com/wiki/Special_Comms) | Stash a Military cable at the boulder next to RUAF gate on Woods | -119.2, 400.4 | -0.7 |  | Ground level |  |
| [Steady Signal](https://escapefromtarkov.fandom.com/wiki/Steady_Signal) | Mark any of the weather stations with an MS2000 Marker on Woods | 412.2, -608.5 | 13.7 |  | Ground level |  |
| [Steady Signal](https://escapefromtarkov.fandom.com/wiki/Steady_Signal) | Mark any of the weather stations with an MS2000 Marker on Woods | -209.2, -279.8 | 77.5 |  | Ground level |  |
| [Steady Signal](https://escapefromtarkov.fandom.com/wiki/Steady_Signal) | Mark any of the weather stations with an MS2000 Marker on Woods | -97.2, -542.0 | 14.0 |  | Ground level |  |
| [Steady Signal](https://escapefromtarkov.fandom.com/wiki/Steady_Signal) | Mark any of the weather stations with an MS2000 Marker on Woods | 247.3, 291.5 | -9.1 |  | Ground level |  |
| [Steady Signal](https://escapefromtarkov.fandom.com/wiki/Steady_Signal) | Mark any of the weather stations with an MS2000 Marker on Woods | -447.1, 249 | 2.1 |  | Ground level |  |
| [Supply Plans](https://escapefromtarkov.fandom.com/wiki/Supply_Plans) | Locate and obtain Secure Folder 0052 in the sawmill cabin on Woods | -3.3, -81.1 | -1.5 | -0.0 | Ground level |  |
| [The Survivalist Path - Thrifty](https://escapefromtarkov.fandom.com/wiki/The_Survivalist_Path_-_Thrifty) | Stash an Iskra ration pack in the ZB-016 bunker on Woods | -386.8, 22.6 | 4.2 | 0.7 | Ground level |  |
| [The Survivalist Path - Thrifty](https://escapefromtarkov.fandom.com/wiki/The_Survivalist_Path_-_Thrifty) | Stash a Bottle of water (0.6L) in the ZB-016 bunker on Woods | -386.8, 22.6 | 4.2 | 0.7 | Ground level |  |
| [The Survivalist Path - Thrifty](https://escapefromtarkov.fandom.com/wiki/The_Survivalist_Path_-_Thrifty) | Stash an Iskra ration pack in the ZB-014 bunker on Woods | 448.0, 71.3 | -13.2 | 0.7 | Ground level |  |
| [The Survivalist Path - Thrifty](https://escapefromtarkov.fandom.com/wiki/The_Survivalist_Path_-_Thrifty) | Stash a Bottle of water (0.6L) in the ZB-014 bunker on Woods | 448.0, 71.3 | -13.2 | 0.7 | Ground level |  |
| [Thirsty - Delivery](https://escapefromtarkov.fandom.com/wiki/Thirsty_-_Delivery) | Locate the specified stash spot on Woods | 227.7, -706.6 | 21.1 | 0.7 | Ground level |  |
| [Thirsty - Delivery](https://escapefromtarkov.fandom.com/wiki/Thirsty_-_Delivery) | Stash the first Propane tank (5L) | 227.7, -706.6 | 21.1 | 0.7 | Ground level |  |
| [Viewer](https://escapefromtarkov.fandom.com/wiki/Viewer) | Install a WI-FI Camera on the mountain ledge on Woods | -219.2, -224.4 | 64.6 | 34.0 | Ground level |  |
| [Weapons Circulation](https://escapefromtarkov.fandom.com/wiki/Weapons_Circulation) | Locate and mark the first ritual spot with an MS2000 Marker on Woods | 196.0, -7.2 | 1.0 |  | Ground level |  |
| [Weapons Circulation](https://escapefromtarkov.fandom.com/wiki/Weapons_Circulation) | Locate and mark the second ritual spot with an MS2000 Marker on Woods | -88.7, -717.6 | 12.6 | 0.3 | Ground level |  |
