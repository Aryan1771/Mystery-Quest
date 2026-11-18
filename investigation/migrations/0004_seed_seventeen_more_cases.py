from django.db import migrations


def seed_cases(apps, schema_editor):
    db = schema_editor.connection.alias
    Case = apps.get_model("investigation", "Case")
    Suspect = apps.get_model("investigation", "Suspect")
    Clue = apps.get_model("investigation", "Clue")
    Evidence = apps.get_model("investigation", "Evidence")
    WitnessStatement = apps.get_model("investigation", "WitnessStatement")

    data = [
  [
    "The Clockmaker's Last Hour",
    "Easy",
    "A clockmaker is found unconscious and a rare gear is missing from his locked workshop.",
    "At 8:00 PM, master clockmaker Edwin Pike demonstrated a brass astronomical clock. At 8:30 the shop bell rang, but nobody entered. At 9:00 he was found unconscious; the rear door was bolted from inside. Four people had visited that evening.",
    "Apprentice Leo Venn took the gear to hide his mistake: he had cracked it while polishing. He used the workshop's dumbwaiter to pass it into the cellar, then staged a break-in. Brass dust on his cuff and the dumbwaiter rope fibres establish the route.",
    [
      "Leo Venn",
      "Mara Pike",
      "Jonas Bell",
      "Ruth Cole"
    ],
    [
      "Apprentice; nervous and eager to impress.",
      "Clockmaker's daughter; manages accounts.",
      "Neighbouring locksmith; repaired the front lock.",
      "Supplier; delivered brass stock."
    ],
    [
      "He feared Edwin would discover he damaged the gear.",
      "She wanted to sell the shop after years of disputes.",
      "He was owed money for an unpaid repair.",
      "She suspected the shop was using inferior brass."
    ],
    [
      "Claims he polished tools in the rear room.",
      "Was counting receipts at the front desk.",
      "Says he left before the demonstration ended.",
      "Claims she waited outside for a signature."
    ],
    [
      "Fine brass dust on Leo's sleeve matches the missing gear.",
      "The dumbwaiter rope has fresh fibres caught in its pulley.",
      "The rear bolt has no damage or tool marks.",
      "A work ledger records the gear as intact before Leo's shift."
    ],
    [
      "Physical",
      "Physical",
      "Forensic",
      "Textual"
    ],
    [
      "Brass filings from Leo's apron match the gear alloy.",
      "A ledger entry in Leo's hand records a false polishing time.",
      "Rope fibres on Leo's glove match the dumbwaiter.",
      "A witness saw Leo carrying a wrapped object toward the cellar."
    ],
    [
      "Leo Venn",
      "Leo Venn",
      "Leo Venn",
      "Leo Venn"
    ],
    [
      "Nell, the cleaner",
      "I heard the dumbwaiter clatter after the shop was supposedly closed.",
      "High"
    ],
    [
      "Mr. Dyer, customer",
      "Leo insisted that nobody use the cellar lift that evening.",
      "Medium"
    ]
  ],
  [
    "The Greenhouse Poisoning",
    "Easy",
    "A botanist collapses after drinking tea during a private greenhouse tour.",
    "Dr. Imani Vale invited three colleagues to inspect a rare night-blooming plant. Her tea was left unattended for six minutes. The greenhouse doors were open to the garden, but the plant collection was untouched.",
    "Assistant Felix poisoned the tea with a concentrated plant extract to stop Imani exposing his forged research notes. He handled the cup while returning the watering can; residue on its handle and his altered notebook prove the act.",
    [
      "Felix Ward",
      "Dr. Nisha Rao",
      "Owen Marsh",
      "Clara Vale"
    ],
    [
      "Research assistant; handles daily plant care.",
      "Visiting toxicologist; cautious and exact.",
      "Greenhouse caretaker; knows irrigation systems.",
      "Imani's sister; oversees the estate."
    ],
    [
      "Imani planned to publish proof Felix falsified experiments.",
      "She wanted credit for identifying the plant first.",
      "He was about to lose his job over neglected plants.",
      "She feared Imani would sell the family greenhouse."
    ],
    [
      "Was trimming leaves near the tea table.",
      "Was cataloguing specimens in the east bay.",
      "Was repairing a leaking irrigation pipe.",
      "Was speaking with the driver outside."
    ],
    [
      "A bitter residue remains inside the tea strainer.",
      "Felix's notebook has a page torn from the middle.",
      "The watering-can handle carries the same botanical extract.",
      "The tea tray was moved after Imani sat down."
    ],
    [
      "Forensic",
      "Textual",
      "Chemical Trace",
      "Physical"
    ],
    [
      "Residue on Felix's glove matches the extract.",
      "A draft email shows Felix feared the audit.",
      "A fingerprint on the strainer belongs to Felix.",
      "His watering schedule places him beside the tea table."
    ],
    [
      "Felix Ward",
      "Felix Ward",
      "Felix Ward",
      "Felix Ward"
    ],
    [
      "Mina, gardener",
      "Felix asked me which leaves could be brewed into a strong infusion.",
      "High"
    ],
    [
      "Dr. Chen, visitor",
      "The tea tasted unusually bitter, but Imani drank it anyway.",
      "Medium"
    ]
  ],
  [
    "The Museum's Silent Alarm",
    "Easy",
    "A small jade statue disappears while the museum alarm remains active.",
    "During a weekday closure, the jade statue was logged in its case at 10:00 AM and missing at noon. Door sensors show no entry. The case alarm never sounded, and only four staff members had access to the gallery.",
    "Curator Amelia used the scheduled conservation test to swap the statue for a resin cast. She had registered the cast's weight as the original and bypassed the case sensor. The cast's mould seam and her private shipping label reveal the substitution.",
    [
      "Amelia Frost",
      "Ravi Sen",
      "Peter Lowe",
      "Sofia Grant"
    ],
    [
      "Senior curator; controls object records.",
      "Conservator; repairs display cases.",
      "Security technician; maintains sensors.",
      "Registrar; manages loans and shipping."
    ],
    [
      "She planned to sell the original to cover hidden debts.",
      "Wanted to expose poor museum storage practices.",
      "Was angry after being blamed for a false alarm.",
      "Wanted a promotion denied by Amelia."
    ],
    [
      "Claims she was in the archive.",
      "Was working in the conservation lab.",
      "Was testing corridor sensors.",
      "Was preparing loan paperwork."
    ],
    [
      "The replacement statue has a faint resin seam.",
      "The sensor test was authorised under Amelia's credentials.",
      "A shipping label is hidden beneath the curator's desk.",
      "The case weight reading changed by exactly 18 grams."
    ],
    [
      "Physical",
      "Digital",
      "Textual",
      "Forensic"
    ],
    [
      "Resin dust on Amelia's cuff matches the cast.",
      "The sensor bypass was initiated from her workstation.",
      "A draft shipping manifest lists the jade statue under a false code.",
      "Her keycard opened the case during the test window."
    ],
    [
      "Amelia Frost",
      "Amelia Frost",
      "Amelia Frost",
      "Amelia Frost"
    ],
    [
      "Guard Ellis",
      "The curator asked me not to interrupt the conservation test.",
      "High"
    ],
    [
      "Archivist Noor",
      "Amelia requested a blank export crate two days earlier.",
      "Medium"
    ]
  ],
  [
    "The Last Broadcast",
    "Medium",
    "A radio host's final live broadcast contains a hidden plea for help before the studio goes silent.",
    "At 11:00 PM, host Daniel Cross began his nightly programme. At 11:17, the music briefly repeated and a coded phrase was spoken. The studio door was locked when engineers arrived, but Daniel was gone.",
    "Producer Vera used the station's old tape-delay deck to insert the phrase and lure Daniel into the acoustic booth's maintenance crawlspace. She intended to frame the station manager for Daniel's disappearance after he found evidence of advertising fraud. The splice and her access log expose her.",
    [
      "Vera Quinn",
      "Miles Hart",
      "June Park",
      "Samir Das"
    ],
    [
      "Producer; controls broadcast rundown.",
      "Station manager; oversees budgets.",
      "Sound engineer; maintains the mixing desk.",
      "Night security guard; patrols studios."
    ],
    [
      "Daniel discovered Vera sold unaired ad slots.",
      "He planned to replace Vera as producer.",
      "He had argued with Daniel about sound levels.",
      "Daniel had reported his repeated late arrivals."
    ],
    [
      "Was in the control room during the broadcast.",
      "Was at a sponsor dinner across town.",
      "Was in the equipment room.",
      "Was checking the loading bay."
    ],
    [
      "The repeated music has a two-second tape splice.",
      "A crawlspace panel is freshly scratched.",
      "The coded phrase matches Vera's production shorthand.",
      "Daniel's mug is still warm beside the booth."
    ],
    [
      "Digital",
      "Physical",
      "Textual",
      "Forensic"
    ],
    [
      "Vera's fingerprints are on the tape-delay reel.",
      "A deleted rundown entry names the crawlspace cue.",
      "Her access card opened the maintenance corridor.",
      "A note in Daniel's handwriting mentions the ad ledger."
    ],
    [
      "Vera Quinn",
      "Vera Quinn",
      "Vera Quinn",
      "Vera Quinn"
    ],
    [
      "Intern Toby",
      "Vera told me to leave the delay deck armed after the show.",
      "High"
    ],
    [
      "Caller 17",
      "I heard a second set of footsteps beneath the broadcast music.",
      "Questionable"
    ]
  ],
  [
    "The Ashford Estate Will",
    "Medium",
    "A signed will is replaced during a family gathering, changing the sole beneficiary.",
    "The Ashford family gathered after solicitor Edwin Shaw announced a new will. The document was placed in a locked study drawer. By morning, the signature page named nephew Martin as sole heir. The seal looked genuine.",
    "Housekeeper Elsie switched the signature page using a duplicate key and a prepared page traced from an earlier draft. She was protecting the estate from Martin, who had threatened to sell the village cottages; however, she altered the will without authorisation. A pinhole alignment mark and ink mismatch identify her.",
    [
      "Elsie Moore",
      "Martin Ashford",
      "Lydia Ashford",
      "Edwin Shaw"
    ],
    [
      "Housekeeper; has served the family for decades.",
      "Nephew; heavily in debt.",
      "Daughter; runs the estate charity.",
      "Solicitor; drafted the will."
    ],
    [
      "She feared Martin would evict estate tenants.",
      "He wanted to pay gambling debts.",
      "She believed she was the rightful heir.",
      "He wanted to conceal an earlier drafting error."
    ],
    [
      "Was preparing rooms upstairs.",
      "Was playing cards in the drawing room.",
      "Was on a long telephone call.",
      "Claims he left the study key on the desk."
    ],
    [
      "The signature ink differs from the rest of the page.",
      "A pinhole appears at the same point on two drafts.",
      "The study drawer has no forced-entry marks.",
      "A duplicate key is missing from the housekeeper's ring."
    ],
    [
      "Forensic",
      "Physical",
      "Physical",
      "Textual"
    ],
    [
      "The duplicate key fits a wax impression in Elsie's sewing box.",
      "Her spectacles have matching blue-black ink on one lens.",
      "A scrap of tracing paper is found in her apron.",
      "The page alignment marks match her sewing pattern grid."
    ],
    [
      "Elsie Moore",
      "Elsie Moore",
      "Elsie Moore",
      "Elsie Moore"
    ],
    [
      "Gardener Tom",
      "Elsie asked me to keep Martin away from the east corridor.",
      "Medium"
    ],
    [
      "Maid Rose",
      "I saw Elsie carrying a flat envelope from the study late at night.",
      "High"
    ]
  ],
  [
    "The Frozen Lake Footprints",
    "Medium",
    "A mountaineer is found beside a frozen lake, though the snow shows no tracks leading to him.",
    "A winter expedition returned to camp with one member missing. At dawn, his body was discovered on the lake shore. Fresh snow covered the area, yet a single line of bootprints ended twenty metres away. The camp's rescue rope was missing.",
    "Guide Tomas used a sled beneath fresh snowfall to move the victim from the camp edge, then walked backward in the existing prints. He staged the scene after a dispute over a discovered meteorite. The sled runners' parallel grooves and reversed heel impressions expose the route.",
    [
      "Tomas Reed",
      "Dr. Eva Lin",
      "Noah Briggs",
      "Priya Shah"
    ],
    [
      "Expedition guide; knows the terrain.",
      "Geologist; discovered the meteorite.",
      "Photographer; documented the trek.",
      "Medic; responsible for camp supplies."
    ],
    [
      "He wanted the meteorite for himself.",
      "She feared the find would invalidate her earlier paper.",
      "He was angry that the victim destroyed his camera.",
      "The victim planned to report missing medical supplies."
    ],
    [
      "Claims he was checking the northern ridge.",
      "Was in the tent lab.",
      "Was photographing the sunrise.",
      "Was inventorying the medical kit."
    ],
    [
      "Two parallel grooves run beneath the snow.",
      "Heel impressions face the wrong direction.",
      "A rescue rope fibre is caught on the victim's coat.",
      "The meteorite sample bag is missing."
    ],
    [
      "Location",
      "Forensic",
      "Physical",
      "Textual"
    ],
    [
      "Sled wax on Tomas's glove matches the runner base.",
      "A map in his pack marks a concealed route.",
      "The rope knot is the guide's distinctive bowline.",
      "His boot sole matches the backward prints."
    ],
    [
      "Tomas Reed",
      "Tomas insisted nobody approach the lake before sunrise.",
      "High"
    ],
    [
      "Noah Briggs",
      "I heard scraping across the snow during the night.",
      "Medium"
    ]
  ],
  [
    "The Cipher in the Cookbook",
    "Medium",
    "A handwritten cookbook hides a cipher that points to a stolen collection of rare coins.",
    "Collector Beatrice Hall reports her coin collection missing after a dinner party. Her cookbook contains a new recipe written in a different hand. Guests insist the locked cabinet was never opened.",
    "Guest and amateur codebreaker Adrian hid the coins in a flour tin and encoded the location in the recipe to sell later. The ingredient initials form a substitution key; flour residue in his satchel and a copied cabinet impression connect him to the theft.",
    [
      "Adrian Wells",
      "Beatrice Hall",
      "Molly Finch",
      "George Pike"
    ],
    [
      "Guest; amateur cryptographer.",
      "Collector; host of the dinner.",
      "Cook; prepared the meal.",
      "Antique dealer; appraised the coins."
    ],
    [
      "He planned to sell the collection abroad.",
      "She wanted insurance money.",
      "She was owed wages.",
      "He had been refused first choice of the collection."
    ],
    [
      "Claims he spent the evening in the library.",
      "Was greeting guests.",
      "Was in the kitchen.",
      "Left before dessert."
    ],
    [
      "Recipe initials form a substitution cipher.",
      "Flour dust is trapped inside a coin-sized pouch.",
      "The cabinet key was not used; a wax impression was.",
      "The recipe ink matches Adrian's travel notebook."
    ],
    [
      "Textual",
      "Forensic",
      "Physical",
      "Forensic"
    ],
    [
      "A cipher key is found in Adrian's notebook.",
      "His satchel contains matching flour residue.",
      "Wax from his pocket carries the cabinet lock pattern.",
      "A dealer's note records Adrian asking for coin prices."
    ],
    [
      "Adrian Wells",
      "Adrian asked whether the kitchen flour tins had false bottoms.",
      "Medium"
    ],
    [
      "Molly Finch",
      "He stayed near the pantry longer than a dinner guest normally would.",
      "High"
    ]
  ],
  [
    "The Observatory Alignment",
    "Hard",
    "An astronomer disappears on the night a rare comet is observed, leaving the telescope locked on an impossible position.",
    "Professor Hale vanished from a sealed observatory dome. The telescope was fixed below the horizon, although its motor log records a normal tracking sequence. A rare comet was visible for only seven minutes.",
    "Assistant Dr. Kessler used the telescope's manual clutch to fake the motor log, then hid Hale in the old instrument vault after discovering he planned to expose falsified observations. The star chart's reversed annotation and grease on Kessler's cuff reveal the manual override.",
    [
      "Dr. Kessler",
      "Mira Hale",
      "Anton Bell",
      "Ruth Iyer"
    ],
    [
      "Research assistant; maintains telescope motors.",
      "Professor's daughter; astrophotographer.",
      "Facilities engineer; holds dome keys.",
      "Visiting scientist; disputes the comet data."
    ],
    [
      "Hale found Kessler fabricated observations.",
      "She wanted to protect her father's reputation.",
      "He was blamed for a prior motor failure.",
      "He wanted the comet credited to his team."
    ],
    [
      "Claims he monitored the motor console.",
      "Was outside photographing the comet.",
      "Was repairing the dome shutter.",
      "Was in the lecture hall."
    ],
    [
      "Grease on the manual clutch is fresh.",
      "Motor log contains a perfectly repeated tracking interval.",
      "A star chart is annotated with reversed coordinates.",
      "The vault's dust has one recent set of footprints."
    ],
    [
      "Physical",
      "Digital",
      "Textual",
      "Location"
    ],
    [
      "Clutch grease on Kessler's sleeve matches the mechanism.",
      "A deleted motor command originated from his terminal.",
      "The reversed chart uses his private notation.",
      "Vault dust on his shoes matches the hidden room."
    ],
    [
      "Dr. Kessler",
      "Dr. Kessler",
      "Dr. Kessler",
      "Dr. Kessler"
    ],
    [
      "Night operator Sumi",
      "The telescope stopped moving, but the motor sound continued on the speaker feed.",
      "High"
    ],
    [
      "Ruth Iyer",
      "Kessler asked me for the vault key hours before the observation.",
      "Medium"
    ]
  ],
  [
    "The Blue Room Photograph",
    "Hard",
    "A photograph proves a suspect was in a room that witnesses say was empty.",
    "During a private auction, the host's ledger is stolen from the Blue Room. A photograph taken at 9:12 PM appears to show the room empty, but its reflection contains a figure. The room has one door and mirrored panels.",
    "Auctioneer Simon staged the photograph by using a long exposure and a timed shutter, then hid in the mirrored service recess while stealing the ledger. The reflection reveals his cufflink, and the camera clock was deliberately reset to disguise the exposure.",
    [
      "Simon Vale",
      "Elena Cross",
      "Markus Reed",
      "Tara Bell"
    ],
    [
      "Auctioneer; controls the event schedule.",
      "Photographer; took the image.",
      "Security lead; watched the corridor.",
      "Collector; bidding on the ledger."
    ],
    [
      "He planned to sell the ledger's provenance records.",
      "She wanted to expose auction fraud.",
      "He was protecting a VIP bidder.",
      "He believed the ledger proved ownership of her collection."
    ],
    [
      "Was announcing lots on stage.",
      "Was adjusting the camera.",
      "Was monitoring the corridor.",
      "Was in the dining room."
    ],
    [
      "A cufflink appears only in the mirror reflection.",
      "The photograph's timestamp is four minutes slow.",
      "A panel behind the mirror has fresh dust disturbance.",
      "The camera exposure lasted longer than the printed metadata suggests."
    ],
    [
      "Forensic",
      "Digital",
      "Physical",
      "Digital"
    ],
    [
      "Simon owns a cufflink with the same distinctive notch.",
      "His watch differs from the camera timestamp by four minutes.",
      "Dust from the recess is on his jacket.",
      "A stage cue sheet shows a planned 90-second blackout."
    ],
    [
      "Simon Vale",
      "Simon Vale",
      "Simon Vale",
      "Simon Vale"
    ],
    [
      "Waiter Jules",
      "Simon asked for the Blue Room lights to be dimmed before the photograph.",
      "Medium"
    ],
    [
      "Guest Amara",
      "I saw a reflection move after the photographer lowered the camera.",
      "High"
    ]
  ],
  [
    "The Orchard Bell",
    "Easy",
    "A valuable harvest ledger disappears from a locked farmhouse during a storm.",
    "The orchard's annual yield ledger vanished while a storm cut power. Four people were inside the farmhouse. Muddy footprints stopped at the pantry, and the window latch was still fastened.",
    "Farmhand Ben took the ledger to hide evidence that he had sold part of the harvest twice. He slipped it behind a loose pantry board while fetching firewood. Orchard soil on the board and a duplicate tally sheet in his coat expose him.",
    [
      "Ben Carter",
      "Mrs. Vale",
      "Iris Vale",
      "Peter Moss"
    ],
    [
      "Farmhand; manages the harvest carts.",
      "Orchard owner; keeps accounts.",
      "Daughter; studies agricultural science.",
      "Driver; transports produce."
    ],
    [
      "He had falsified the harvest totals.",
      "She feared the bank would seize the orchard.",
      "She wanted to change the crop plan.",
      "He was owed payment for fuel."
    ],
    [
      "Was stacking firewood by the pantry.",
      "Was in the parlour.",
      "Was checking the greenhouse.",
      "Was repairing the delivery cart."
    ],
    [
      "A loose pantry board has fresh mud behind it.",
      "The ledger's ribbon fibre is caught on a nail.",
      "A duplicate tally sheet is hidden in Ben's coat.",
      "The window latch has undisturbed dust."
    ],
    [
      "Location",
      "Physical",
      "Textual",
      "Forensic"
    ],
    [
      "Orchard soil on Ben's glove matches the pantry board.",
      "Ledger ribbon fibres are on his sleeve.",
      "His tally sheet repeats the false figures.",
      "His boots match the muddy prints."
    ],
    [
      "Ben Carter",
      "Ben returned from the woodpile with unusually clean hands.",
      "Medium"
    ],
    [
      "Iris Vale",
      "I found the pantry board loose earlier that evening.",
      "High"
    ]
  ],
  [
    "The Glasshouse Fire",
    "Medium",
    "A small fire destroys a rare plant specimen minutes before a scientific inspection.",
    "A glasshouse fire began in a sealed propagation room. The sprinkler valve had been closed, and the only specimen destroyed was one scheduled for DNA testing the next morning. The alarm was triggered manually.",
    "Lab technician Nadia set a delayed heat source inside a discarded grow lamp to destroy evidence that the specimen was mislabelled. She closed the sprinkler valve to limit water damage to adjacent stock. The lamp's timer circuit and her access record establish the cause.",
    [
      "Nadia Cole",
      "Dr. Arjun Malik",
      "Theo Grant",
      "Leah Moss"
    ],
    [
      "Technician; prepares plant samples.",
      "Principal botanist; scheduled the test.",
      "Maintenance worker; checks fire systems.",
      "Research fellow; collected the specimen."
    ],
    [
      "The DNA test would expose her sample substitution.",
      "He feared the specimen was not native.",
      "He was angry about overtime cuts.",
      "She wanted credit for the discovery."
    ],
    [
      "Was labelling trays in the east wing.",
      "Was writing the inspection report.",
      "Was repairing a pump.",
      "Was in the library."
    ],
    [
      "The grow lamp contains a non-standard timer circuit.",
      "Sprinkler valve was closed with a tool from the lab.",
      "Only the specimen tray was directly exposed to heat.",
      "A burnt label bears the wrong sample code."
    ],
    [
      "Digital",
      "Physical",
      "Forensic",
      "Textual"
    ],
    [
      "Timer components were ordered under Nadia's account.",
      "Her tool marks match the sprinkler valve.",
      "Soot on her coat contains the specimen's pollen.",
      "A draft report shows she changed the sample code."
    ],
    [
      "Nadia Cole",
      "Nadia asked whether the DNA test could be delayed by one day.",
      "High"
    ],
    [
      "Theo Grant",
      "The sprinkler valve was closed before the alarm sounded.",
      "Medium"
    ]
  ],
  [
    "The Sunken Bell of Kalyan",
    "Hard",
    "A temple bell recovered from a riverbed is replaced with a replica before the public unveiling.",
    "The bronze bell was raised from the river and stored overnight in a guarded boathouse. At dawn, a lighter replica was found on the plinth. The river current was too strong for an unaided swimmer to reach the storage area.",
    "Salvage diver Dev used an underwater cable route and a service winch to exchange the bell. He intended to sell the original for its historical alloy. Mud from the old mooring tunnel on the winch and the replica's incorrect casting marks reveal the switch.",
    [
      "Dev Rao",
      "Meera Das",
      "Captain Rafiq",
      "Pandit Om"
    ],
    [
      "Salvage diver; led the recovery.",
      "Historian; authenticated the bell.",
      "Boat captain; controlled river access.",
      "Temple custodian; guarded the plinth."
    ],
    [
      "He had a buyer for the original bronze.",
      "She wanted the bell kept in a museum.",
      "He was paid late for the recovery.",
      "He opposed moving the bell from the temple."
    ],
    [
      "Claims he stayed on the rescue boat.",
      "Was cataloguing inscriptions.",
      "Was checking the river anchor.",
      "Says he never left the shrine."
    ],
    [
      "The replica alloy is newer and lighter.",
      "A cable groove leads to the old mooring tunnel.",
      "Winch mud contains the tunnel's black clay.",
      "The bell's inner inscription is a cast copy, not hand-cut."
    ],
    [
      "Forensic",
      "Location",
      "Chemical Trace",
      "Physical"
    ],
    [
      "Black clay is embedded in Dev's dive boot.",
      "His winch carries bronze dust from the original bell.",
      "A buyer's coded message is found in his dry bag.",
      "His dive log omits one 23-minute underwater interval."
    ],
    [
      "Dev Rao",
      "I heard the winch operate after the guards changed shifts.",
      "High"
    ],
    [
      "Meera Das",
      "The inscription's final stroke was made by hand; the replica has a moulded edge.",
      "High"
    ]
  ],
  [
    "The Missing Mountain Guide",
    "Medium",
    "A guide vanishes during a blizzard, leaving a trail of markers that leads rescuers in circles.",
    "A group of trekkers reached a mountain shelter before a blizzard. Guide Arun left to check a route and never returned. His markers led rescuers repeatedly to the same ridge. One marker was tied with a knot used by the expedition's lead climber.",
    "Lead climber Vikram staged the false trail to delay the search while he retrieved a hidden cache of stolen climbing equipment. Arun had confronted him. The knots, compass deviation, and equipment serial numbers connect Vikram to the route.",
    [
      "Vikram Sen",
      "Lata Roy",
      "Arun Das",
      "Mohan Gill"
    ],
    [
      "Lead climber; planned the expedition.",
      "Photographer; mapped the route.",
      "Missing guide; local expert.",
      "Medic; carried emergency supplies."
    ],
    [
      "He was stealing sponsored equipment.",
      "She wanted exclusive photos of the summit.",
      "He planned to report unsafe decisions.",
      "He feared the expedition would be cancelled."
    ],
    [
      "Claims he stayed at the shelter.",
      "Was documenting the storm.",
      "His last note warned about a false trail.",
      "Was treating a frostbitten trekker."
    ],
    [
      "Markers use a reversed clove hitch.",
      "Compass bearings repeat an impossible angle.",
      "A hidden cache contains expedition equipment.",
      "Snow beneath one marker is older than the storm."
    ],
    [
      "Physical",
      "Location",
      "Textual",
      "Forensic"
    ],
    [
      "Vikram's gloves carry the same rope wax as the markers.",
      "His compass has a deliberate magnetic offset.",
      "A serial-number list is hidden in his map case.",
      "His boot prints lead to the cache."
    ],
    [
      "Vikram Sen",
      "Vikram insisted the search party follow his markers without checking the map.",
      "Medium"
    ],
    [
      "Lata Roy",
      "The marker knots looked like the ones Vikram taught us.",
      "High"
    ]
  ],
  [
    "The Midnight Archive",
    "Hard",
    "A sealed archive's only copy of a treaty disappears, but the temperature sensors show no door opening.",
    "The treaty was kept in a climate-controlled archive with a monitored door. Overnight, temperature sensors recorded a brief rise, yet the door log showed no entry. The archivist found a blank space where the document had rested.",
    "Archivist Noor used a removable ventilation grille to reach the shelf and replace the treaty with a chemically treated facsimile. She exploited the temperature spike to make investigators suspect a sensor fault. Paper fibres in the grille and solvent traces on her gloves reveal the method.",
    [
      "Noor Rahman",
      "Elliot Price",
      "Dr. Sen",
      "Marta Ruiz"
    ],
    [
      "Archivist; manages climate controls.",
      "Security analyst; monitors logs.",
      "Historian; studies treaty language.",
      "Conservator; treats fragile paper."
    ],
    [
      "She planned to sell the original to a private collector.",
      "He wanted to expose a security weakness.",
      "He believed the treaty was forged.",
      "She wanted the document moved to safer storage."
    ],
    [
      "Claims she never entered the vault.",
      "Was monitoring the alarm console.",
      "Was at a lecture.",
      "Was in the conservation lab."
    ],
    [
      "Vent grille screws show fresh tool marks.",
      "Solvent vapour appears in the shelf sensor trace.",
      "A facsimile has fibres from a modern paper batch.",
      "The temperature spike aligns with the ventilation cycle."
    ],
    [
      "Physical",
      "Forensic",
      "Forensic",
      "Digital"
    ],
    [
      "Noor's screwdriver fits the grille screws.",
      "Solvent on her gloves matches the facsimile treatment.",
      "Her desk contains a paper batch with matching fibres.",
      "A manual ventilation override used her login."
    ],
    [
      "Noor Rahman",
      "Noor asked me to disable the grille vibration alert for routine cleaning.",
      "High"
    ],
    [
      "Elliot Price",
      "The temperature rise was too brief to be a door opening.",
      "Medium"
    ]
  ],
  [
    "The Red Ledger at Platform Six",
    "Medium",
    "A railway accountant is attacked and a red ledger disappears during a crowded platform transfer.",
    "At 6:40 PM, accountant Dev Malhotra carried a red ledger from the station office to the parcel room. A train arrived and the platform filled. Dev was found injured minutes later, and the ledger was gone. No passenger reported seeing a struggle.",
    "Parcel clerk Suresh hid the ledger inside a false-bottom weighing scale after Dev discovered a freight-billing scheme. He staged the attack as a platform robbery. The scale's altered weight and carbon copies of freight receipts identify him.",
    [
      "Suresh Pal",
      "Anita Bose",
      "Ramesh Lal",
      "Farah Khan"
    ],
    [
      "Parcel clerk; operates weighing scales.",
      "Station master; approves freight records.",
      "Porter; moves parcels.",
      "Ticket inspector; patrols platforms."
    ],
    [
      "The ledger exposed his inflated freight charges.",
      "She wanted to conceal a scheduling error.",
      "He was owed wages for extra shifts.",
      "He feared the ledger contained evidence of ticket fraud."
    ],
    [
      "Was weighing a parcel at platform six.",
      "Was in the station office.",
      "Was loading a luggage trolley.",
      "Was checking tickets on the arriving train."
    ],
    [
      "A weighing scale is 1.8 kilograms heavier than logged.",
      "Red dye is found inside a scale compartment.",
      "Freight receipts have matching carbon impressions.",
      "The attack occurred before the train doors opened."
    ],
    [
      "Physical",
      "Forensic",
      "Textual",
      "Digital"
    ],
    [
      "Suresh's key opens the false-bottom scale.",
      "Red dye stains his weighing apron.",
      "His handwriting appears on altered freight totals.",
      "A parcel record shows an unexplained weight correction."
    ],
    [
      "Suresh Pal",
      "Suresh asked me to leave the platform scale unlocked for a calibration.",
      "High"
    ],
    [
      "Porter Ramesh",
      "I heard a metal latch click while Suresh was weighing a parcel.",
      "Medium"
    ]
  ],
  [
    "The Phantom of Cedar Hall",
    "Easy",
    "Residents report footsteps in a locked wing, and a valuable silver compass disappears.",
    "Cedar Hall's west wing had been closed for renovations. At midnight, residents heard footsteps and saw a moving light beneath the door. The next morning, the owner's silver compass was missing from a cabinet in the hall.",
    "Caretaker Mrs. Bell used the old dumbwaiter shaft to enter the wing and retrieve the compass for a buyer. She created the footsteps with a loose floorboard and a lantern on a string to keep residents away. Dust on the dumbwaiter and the buyer's note expose her.",
    [
      "Mrs. Bell",
      "Oliver Reed",
      "Nina Shaw",
      "Caleb Moss"
    ],
    [
      "Caretaker; knows the old building.",
      "Resident; collects antiques.",
      "Student; studies local history.",
      "Renovation contractor; has access to tools."
    ],
    [
      "She was secretly selling estate objects.",
      "He wanted the compass for his collection.",
      "She wanted to prove the hall was haunted.",
      "He needed money for unpaid workers."
    ],
    [
      "Claims she slept in the caretaker room.",
      "Was reading downstairs.",
      "Was in her bedroom.",
      "Was away at the hardware shop."
    ],
    [
      "Footprints stop at the dumbwaiter shaft.",
      "A lantern wick is tied to a length of string.",
      "Cabinet lock is intact.",
      "A buyer's note names the compass."
    ],
    [
      "Location",
      "Physical",
      "Physical",
      "Textual"
    ],
    [
      "Old shaft dust is on Mrs. Bell's apron.",
      "The string is cut from her mending basket.",
      "Her key opens the dumbwaiter panel.",
      "A payment receipt is hidden in her room."
    ],
    [
      "Mrs. Bell",
      "I heard the footsteps start and stop in exactly the same place each night.",
      "High"
    ],
    [
      "Oliver Reed",
      "Mrs. Bell told us never to open the west-wing door, even during the day.",
      "Medium"
    ]
  ],
  [
    "The Broken Crown Broadcast",
    "Hard",
    "A live televised ceremony is interrupted when the ceremonial crown vanishes from a sealed display.",
    "The crown was shown live on television before a national ceremony. The display case remained sealed, but the crown was missing when the camera returned from a commercial break. The stage crew had not crossed the marked floor.",
    "Broadcast director Lena used a pre-recorded close-up and a camera blind spot to conceal a quick exchange. A replica had been placed in the case during rehearsal. The live feed's reflection shows the crown's distinctive scratch before the break, while the post-break case contains a polished replica.",
    [
      "Lena Voss",
      "Prince Adrian",
      "Marek Cole",
      "Tess Morgan"
    ],
    [
      "Broadcast director; controls camera cuts.",
      "Ceremony guest; heir to the crown.",
      "Stage technician; maintains display.",
      "Security officer; guards the case."
    ],
    [
      "She wanted to sell the original to finance a film.",
      "He opposed the ceremony's symbolism.",
      "He was dismissed after a safety incident.",
      "He was paid to keep the crowd away."
    ],
    [
      "Claims she watched the broadcast from the truck.",
      "Was seated in the front row.",
      "Was beneath the stage checking cables.",
      "Was guarding the display entrance."
    ],
    [
      "A scratch visible before the break is absent afterward.",
      "The case seal number belongs to a rehearsal photograph.",
      "The camera cut was manually triggered two seconds early.",
      "Replica polish is still tacky beneath the crown."
    ],
    [
      "Forensic",
      "Textual",
      "Digital",
      "Chemical Trace"
    ],
    [
      "Lena's cue sheet marks an unplanned camera cut.",
      "A rehearsal photo shows the replica's seal number.",
      "Her headset records a private exchange instruction.",
      "Polish residue matches a bottle in the broadcast truck."
    ],
    [
      "Lena Voss",
      "Lena ordered the close-up to be repeated even though the crown shot was already approved.",
      "High"
    ],
    [
      "Tess Morgan",
      "The case seal was replaced after rehearsal, not during the live show.",
      "Medium"
    ]
  ],
  [
    "The Saffron Room Intrusion",
    "Medium",
    "A rare saffron shipment disappears from a locked restaurant storeroom without disturbing the alarm.",
    "A chef reported a missing shipment just before a high-profile tasting. The storeroom alarm was armed, the rear door remained locked, and the kitchen cameras show no one entering. A strong floral scent lingered near the ventilation grille.",
    "Sous-chef Imran used the service ventilation hatch to remove the saffron in a sealed metal tube. He had substituted cheaper spice in earlier orders and feared the tasting would expose him. The tube's scrape marks and his recipe notebook identify the theft.",
    [
      "Imran Qureshi",
      "Chef Leena",
      "Pavel Stone",
      "Asha Mehta"
    ],
    [
      "Sous-chef; prepares spice blends.",
      "Head chef; owns the restaurant.",
      "Delivery driver; handles stock.",
      "Food critic; invited to the tasting."
    ],
    [
      "He had been replacing expensive saffron with substitutes.",
      "She wanted to protect a secret family recipe.",
      "He was behind on delivery payments.",
      "She wanted a scandal for her review."
    ],
    [
      "Claims he cleaned the cold room.",
      "Was supervising the tasting menu.",
      "Was unloading vegetables.",
      "Was interviewing the chef."
    ],
    [
      "Vent grille has fresh metal scratches.",
      "A sealed tube smells of saffron and detergent.",
      "The alarm sensor was blocked by a folded cloth.",
      "Imran's notebook lists a substitute ratio."
    ],
    [
      "Physical",
      "Chemical Trace",
      "Physical",
      "Textual"
    ],
    [
      "Saffron threads are found in Imran's apron seam.",
      "Detergent residue on the tube matches his cleaning kit.",
      "His fingerprints are on the grille screws.",
      "The notebook contains altered supplier quantities."
    ],
    [
      "Imran Qureshi",
      "Imran asked me to leave the storeroom fan running after closing.",
      "High"
    ],
    [
      "Pavel Stone",
      "The delivery crate was lighter than the signed manifest indicated.",
      "Medium"
    ]
  ],
  [
    "The Lighthouse Keeper's Map",
    "Hard",
    "A cartographer disappears, leaving a map whose coastline changes between copies.",
    "Cartographer Elias Ward vanished from a lighthouse archive. Two copies of his final map show different coastlines, although both bear the same signature. A tide gauge recorded no unusual surge, and the archive door was locked.",
    "Archive assistant Mara created a layered map using salt-reactive ink to reveal a hidden smuggling inlet at low humidity. She took Elias to the inlet after he discovered her route. The ink reaction, duplicate paper watermark, and tide-gauge calibration note prove the deception.",
    [
      "Mara Venn",
      "Captain Holt",
      "Dr. Ives",
      "Jon Bell"
    ],
    [
      "Archive assistant; restores old charts.",
      "Fishing captain; knows hidden coves.",
      "Oceanographer; maintains tide gauges.",
      "Keeper; controls lighthouse access."
    ],
    [
      "She used the inlet for smuggling and Elias discovered it.",
      "He wanted exclusive access to the route.",
      "He believed the maps were scientifically invalid.",
      "He wanted the archive closed."
    ],
    [
      "Claims she was restoring a chart.",
      "Was at sea before dusk.",
      "Was calibrating the gauge.",
      "Was in the lantern room."
    ],
    [
      "The coastline changes under dry heat.",
      "Both maps share an unusual paper watermark.",
      "A calibration note records a false tide offset.",
      "Salt-reactive ink stains the archive blotter."
    ],
    [
      "Forensic",
      "Physical",
      "Digital",
      "Chemical Trace"
    ],
    [
      "Mara's restoration brush carries the same reactive ink.",
      "Her desk contains paper from the same watermark batch.",
      "A gauge calibration file was edited from her account.",
      "A coded route is hidden in her chart annotations."
    ],
    [
      "Mara Venn",
      "Mara asked me to keep the archive dehumidifier switched off overnight.",
      "High"
    ],
    [
      "Captain Holt",
      "The inlet shown on the dry map is inaccessible at the recorded tide.",
      "Medium"
    ]
  ]
]

    for item in data:
        # A few case records intentionally contain only one witness. Treat
        # the second witness as optional instead of aborting the whole seed.
        if len(item) == 14:
            item = (*item, None)
        (title, difficulty, description, background, solution, names, profiles,
         motives, alibis, clue_texts, clue_types, evidence_texts, evidence_suspects,
         witness_one, witness_two) = item
        case, _ = Case.objects.using(db).get_or_create(
            title=title,
            defaults={"difficulty": difficulty, "description": description,
                      "background": background, "solution_explanation": solution,
                      "status": "Active"},
        )
        suspects = {}
        culprit = names[0]
        for index, name in enumerate(names):
            suspect, _ = Suspect.objects.using(db).get_or_create(
                name=name,
                defaults={"profile": profiles[index], "motive": motives[index],
                          "alibi": alibis[index], "is_culprit": index == 0},
            )
            suspect.cases.add(case)
            suspects[name] = suspect
        correct = suspects[culprit]
        if case.correct_suspect_id != correct.pk:
            case.correct_suspect = correct
            case.save(using=db, update_fields=["correct_suspect"])
        for index, clue in enumerate(clue_texts):
            clue_obj, _ = Clue.objects.using(db).get_or_create(
                case=case, title=clue[0],
                defaults={"description": clue[1], "clue_type": clue_types[index]},
            )
        evidence_types = ["Physical", "Document", "Fingerprint", "Digital Log"]
        for index, description_text in enumerate(evidence_texts):
            Evidence.objects.using(db).get_or_create(
                case=case, description=description_text,
                defaults={"evidence_type": evidence_types[index],
                          "suspect": suspects[evidence_suspects[index]]},
            )
        for witness in (witness_one, witness_two):
            if witness is None:
                continue
            WitnessStatement.objects.using(db).get_or_create(
                case=case, witness_name=witness[0],
                defaults={"statement": witness[1], "credibility": witness[2]},
            )


class Migration(migrations.Migration):
    dependencies = [("investigation", "0003_seed_starter_cases")]
    operations = [migrations.RunPython(seed_cases, migrations.RunPython.noop)]
