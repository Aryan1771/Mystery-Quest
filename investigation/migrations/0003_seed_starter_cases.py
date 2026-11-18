from django.db import migrations


def seed_starter_cases(apps, schema_editor):
    Case = apps.get_model("investigation", "Case")
    Suspect = apps.get_model("investigation", "Suspect")
    Clue = apps.get_model("investigation", "Clue")
    Evidence = apps.get_model("investigation", "Evidence")
    WitnessStatement = apps.get_model("investigation", "WitnessStatement")

    cases = [
        {
            "title": "The Midnight Express Heist",
            "description": "A sealed railway mail compartment was opened during a twelve-minute tunnel passage. A prototype cipher machine vanished, yet none of the passengers remembers seeing anyone enter or leave the compartment.",
            "background": "The year is 1932. The Midnight Express left Calcutta at 8:40 PM carrying a prototype cipher machine bound for a government laboratory. At 11:16 PM the train entered the long Barakar tunnel. The guard heard a metallic click from the mail compartment. When the train emerged twelve minutes later, the compartment was locked from the inside and the machine was gone. The only key was supposedly in the station master's sealed envelope.",
            "difficulty": "Medium",
            "solution_explanation": "The culprit is Elias D'Souza, the railway telegraph operator. He had copied the key pattern earlier while repairing the lock and made a wax impression. He used the tunnel's darkness to open the compartment, remove the machine, and pass it through a maintenance hatch into a tool bag carried by the track inspector. The oil on the hatch and the reversed telegraph timestamp expose the plan. The inspector was unknowingly used as a courier.",
            "suspects": [
                ("Elias D'Souza", "Railway telegraph operator; precise, soft-spoken, and responsible for sending train position reports.", "The cipher machine could expose a forged message network he has been operating.", "Claims he remained in the telegraph cabin sending routine position reports throughout the tunnel."),
                ("Mira Sen", "Government cryptographer travelling with the machine; brilliant but visibly anxious.", "She feared the prototype would be blamed for a recent failed codebreaking trial.", "Says she was in her berth reviewing cipher notes; a passenger saw her there shortly before the tunnel."),
                ("Harold Finch", "Mail-carriage guard; veteran employee with access to the compartment.", "He was recently passed over for promotion and has debts.", "Claims he never left the carriage and kept the compartment key in his sealed pouch."),
                ("Rafiq Ali", "Track inspector who joined the train at the previous stop with a maintenance tool bag.", "A smuggling gang has threatened his family, though he denies helping them.", "Says he was checking a vibration near the rear coupling during the tunnel.")
            ],
            "culprit": "Elias D'Souza",
            "clues": [
                ("Fresh Machine Oil on the Hatch", "A thin smear of machine oil marks the inside lip of the mail-compartment maintenance hatch. The oil is used on telegraph equipment, not railway locks.", "Physical"),
                ("The Impossible Telegraph Time", "The station log records a position report at 11:20 PM, but the receiving office's clock was four minutes slow. The message was actually sent before the train entered the tunnel.", "Digital"),
                ("A Wax Key Impression", "A softened wax fragment found in a waste bin carries the tooth pattern of the mail-compartment lock.", "Forensic"),
                ("The Guard's Unbroken Seal", "The key pouch seal is genuine and unbroken. The thief therefore used a copied key rather than stealing the guard's key.", "Textual")
            ],
            "evidence": [
                ("Chemical Trace", "The oil composition matches the lubricant issued to the telegraph cabin. It is inconsistent with the guard's lock-maintenance kit.", "Elias D'Souza"),
                ("Document", "A carbon copy of the position report has a handwritten correction in Elias's distinctive narrow lettering.", "Elias D'Souza"),
                ("Fingerprint", "Partial wax residue on the discarded impression carries a thumb ridge pattern consistent with the operator's maintenance notebook.", "Elias D'Souza"),
                ("CCTV Footage", "A platform porter recalls a tool bag with a newly stitched inner pocket being loaded beside the rear coupling.", "Rafiq Ali")
            ],
            "witnesses": [
                ("Porter Gopal", "I saw the telegraph operator leave his cabin just before the tunnel. He said he was checking a loose signal wire, but he returned without his usual tool roll.", "Medium"),
                ("Passenger Mrs. Roy", "The guard's pouch was hanging from his belt when I passed him. The seal looked untouched after the train came out of the tunnel.", "High")
            ]
        },
        {
            "title": "The Vanishing Portrait of Room  nine",
            "description": "A priceless miniature portrait disappeared from a locked hotel suite during a charity reception. The display case remained locked and every guest insists they stayed in the ballroom.",
            "background": "At the Halcyon Hotel's winter charity reception, the miniature portrait of the founder was displayed in Suite 9 behind a glass case. At 9:30 PM the curator confirmed it was present. At 9:47 PM the lights flickered for less than a minute. At 10:05 PM the case was found locked but empty. The suite's only door was watched by two attendants, and the windows were painted shut.",
            "difficulty": "Easy",
            "solution_explanation": "The culprit is Celeste Ward, the event photographer. She had made a high-resolution photograph of the portrait earlier and printed a convincing flat replica on thin archival paper. During the brief blackout she slid the replica into the display mount and removed the original through a narrow service slot at the rear of the case. The slot was hidden by the velvet backing. Her camera tripod was positioned to block the attendant's view. The tiny fibres on the rear latch and the photograph's missing negative frame reveal the substitution.",
            "suspects": [
                ("Celeste Ward", "Official event photographer; observant, charming, and allowed to move between rooms.", "She has been secretly selling reproductions of valuable artworks to collectors.", "Claims she was photographing the ballroom stage during the blackout."),
                ("Dr. Arun Mehta", "Art historian who authenticated the miniature; protective of its provenance.", "He wanted the portrait returned to the family rather than sold at auction.", "Says he was giving a talk in the library; several guests remember his lecture."),
                ("Nora Bell", "Hotel manager; has master keys and knows the building's service passages.", "The hotel is in debt and the portrait could cover a large loan.", "Claims she was at the reception desk dealing with a guest complaint."),
                ("Victor Hale", "Private collector and the event's largest donor.", "He had offered to buy the portrait privately and was refused.", "Says he never left the ballroom and was speaking with the mayor.")
            ],
            "culprit": "Celeste Ward",
            "clues": [
                ("Velvet Fibres on the Rear Latch", "A few dark velvet fibres are caught in the narrow service slot behind the display mount. The slot is too small for a hand but wide enough for a thin sheet.", "Forensic"),
                ("A Missing Negative Frame", "The photographer's contact sheet jumps from frame 118 to frame 120. Frame 119 is absent, though the camera counter advanced normally.", "Digital"),
                ("The Case Was Never Unlocked", "The lock shows no scratches and the seal is intact. The portrait was removed through the rear service slot, not the front door.", "Physical"),
                ("A Flat Shadow in the Replica", "The replacement image casts no natural shadow at its lower edge and has a faint paper curl under magnification.", "Forensic")
            ],
            "evidence": [
                ("Document", "A discarded archival-paper test strip in the photographer's kit matches the paper fibres in the display case.", "Celeste Ward"),
                ("Digital Log", "The camera metadata shows a photograph of the portrait taken minutes before the reception, followed by the unexplained missing frame.", "Celeste Ward"),
                ("Fingerprint", "The service-slot latch carries a partial print matching the photographer's camera grip.", "Celeste Ward"),
                ("Chemical Trace", "A trace of archival mounting adhesive on the display backing matches the adhesive in Celeste's print-restoration kit.", "Celeste Ward")
            ],
            "witnesses": [
                ("Attendant Peter", "The photographer asked me to move the tripod closer to the suite door. It blocked my view of the display case for a short time.", "High"),
                ("Guest Mrs. Das", "During the blackout I heard a small metallic click from the portrait room, not from the ballroom.", "Medium")
            ]
        },
        {
            "title": "A Signal from Blackwater Lighthouse",
            "description": "A lighthouse keeper vanished during a storm, leaving the lamp flashing a distress pattern that should have been impossible with the generator switched off.",
            "background": "Blackwater Lighthouse stands on a rocky island. Keeper Thomas Vale sent a routine all-clear at 7:00 PM, then disappeared before the supply boat arrived at dawn. The lighthouse lamp continued flashing at irregular intervals despite the generator fuel valve being closed. Three people had reason to visit the island that evening: the supply captain, a marine biologist, and the keeper's apprentice. A storm destroyed the only footbridge, making the timing of the disappearance crucial.",
            "difficulty": "Hard",
            "solution_explanation": "The culprit is apprentice Jonah Reed. He discovered that the lamp's backup hand-crank and rotating shutter could be driven by a concealed clockwork weight. He staged the distress pattern to make investigators believe Thomas was alive after the storm began. Jonah had already moved the keeper through the old drainage tunnel at low tide and hidden him in the boathouse on the mainland. The tide chart marked with two different inks and the apprentice's wet boots contradict his claim that he never left the tower. Thomas is found alive; Jonah's motive was to force the sale of the lighthouse after learning it was to be decommissioned.",
            "difficulty": "Hard",
            "suspects": [
                ("Jonah Reed", "Lighthouse apprentice; knows the lamp mechanism and the island's old drainage tunnels.", "He wanted to prevent the lighthouse from being decommissioned and sold.", "Claims he stayed in the lantern room all night maintaining the lamp by hand."),
                ("Captain Eliza Voss", "Supply-boat captain; knows the surrounding waters and tide schedule.", "The keeper had reported her for smuggling restricted fuel.", "Says she left the island before the storm and never returned."),
                ("Dr. Saira Khan", "Marine biologist studying tidal pools near the lighthouse.", "She had argued with the keeper about access to a protected reef.", "Claims she sheltered in the east storehouse until the storm passed."),
                ("Thomas Vale", "The missing lighthouse keeper; experienced and meticulous.", "He planned to report irregularities in the lighthouse maintenance budget.", "His last radio message said the lamp was functioning normally.")
            ],
            "culprit": "Jonah Reed",
            "clues": [
                ("The Clockwork Weight", "A hidden counterweight behind the lamp housing can keep the shutter moving for hours without generator power.", "Physical"),
                ("Two-Ink Tide Chart", "The tide chart has the 11:40 PM low tide marked in fresh blue ink over an older pencil notation.", "Textual"),
                ("Wet Boots in a Dry Room", "Jonah's boots carry black silt found only near the drainage tunnel, although he claims he stayed upstairs.", "Forensic"),
                ("The False Distress Sequence", "The lamp's flash interval repeats with mechanical precision, unlike a human-operated distress signal.", "Digital")
            ],
            "evidence": [
                ("Weapon", "A heavy brass counterweight has a fresh scrape matching the hidden clockwork housing. It was used to keep the shutter moving.", "Jonah Reed"),
                ("Document", "A tide chart contains a route through the drainage tunnel marked in blue ink.", "Jonah Reed"),
                ("Chemical Trace", "Black silt on the apprentice's boots contains shell fragments unique to the tunnel outlet.", "Jonah Reed"),
                ("Digital Log", "The lamp maintenance recorder shows the generator was inactive while the shutter continued its identical cycle.", "Jonah Reed")
            ],
            "witnesses": [
                ("Fisherman Old Ben", "I saw a lantern moving near the lower rocks around midnight, long after the bridge was washed away.", "Questionable"),
                ("Radio Operator Mae", "The distress flashes repeated at exactly the same interval. It sounded like machinery, not a person signalling.", "High")
            ]
        }
    ]

    for data in cases:
        case, _ = Case.objects.using(schema_editor.connection.alias).get_or_create(
            title=data["title"],
            defaults={
                "description": data["description"],
                "background": data["background"],
                "difficulty": data["difficulty"],
                "status": "Active",
                "solution_explanation": data["solution_explanation"],
            },
        )
        suspects = {}
        for name, profile, motive, alibi in data["suspects"]:
            suspect, _ = Suspect.objects.using(schema_editor.connection.alias).get_or_create(
                name=name,
                defaults={
                    "profile": profile,
                    "motive": motive,
                    "alibi": alibi,
                    "is_culprit": name == data["culprit"],
                },
            )
            if suspect.is_culprit != (name == data["culprit"]):
                suspect.is_culprit = name == data["culprit"]
                suspect.save(using=schema_editor.connection.alias, update_fields=["is_culprit"])
            suspect.cases.add(case)
            suspects[name] = suspect

        culprit = suspects[data["culprit"]]
        if case.correct_suspect_id != culprit.pk:
            case.correct_suspect = culprit
            case.save(using=schema_editor.connection.alias, update_fields=["correct_suspect"])

        for title, description, clue_type in data["clues"]:
            Clue.objects.using(schema_editor.connection.alias).get_or_create(
                case=case, title=title,
                defaults={"description": description, "clue_type": clue_type},
            )

        for evidence_type, description, suspect_name in data["evidence"]:
            Evidence.objects.using(schema_editor.connection.alias).get_or_create(
                case=case, description=description,
                defaults={
                    "evidence_type": evidence_type,
                    "suspect": suspects[suspect_name],
                },
            )

        for witness_name, statement, credibility in data["witnesses"]:
            WitnessStatement.objects.using(schema_editor.connection.alias).get_or_create(
                case=case, witness_name=witness_name,
                defaults={"statement": statement, "credibility": credibility},
            )


class Migration(migrations.Migration):
    dependencies = [
        ("investigation", "0002_usercaseprogress_investigation_notes"),
    ]

    operations = [
        migrations.RunPython(seed_starter_cases, migrations.RunPython.noop),
    ]
