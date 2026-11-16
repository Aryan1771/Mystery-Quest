from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import UserProfile
from investigation.models import (
    Case, Clue, Suspect, Evidence, WitnessStatement,
    UserCaseProgress, Accusation
)


class Command(BaseCommand):
    help = 'Populates the database with 5 detailed fictional mystery cases, clues, suspects, and sample detectives.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Initializing Mystery Quest sample data..."))

        # 1. Create Superuser / Administrator
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@mysteryquest.local',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS("Created admin user: admin / admin123"))
        else:
            self.stdout.write("Admin user already exists.")

        # Ensure admin has profile
        admin_profile, _ = UserProfile.objects.get_or_create(user=admin_user)
        admin_profile.rank = 'Chief Inspector'
        admin_profile.total_score = 950
        admin_profile.cases_solved = 5
        admin_profile.save()

        # 2. Create Sample Detectives for Leaderboard
        detectives_data = [
            ('vansh123', 'vansh@detectiveagency.org', 'Master Detective', 1250, 8, 'Elite senior lead investigator and deductive reasoning specialist.'),
            ('hercule_p', 'hercule@belgianpolice.be', 'Master Detective', 1100, 7, 'Method, order, and the little grey cells.'),
            ('miss_marple', 'marple@stmarymead.org', 'Senior Investigator', 620, 4, 'Keen observer of human nature and quiet villages.'),
            ('detective_novak', 'novak@cityprecinct.org', 'Junior Detective', 180, 1, 'Cyber and digital forensics specialist.'),
        ]

        for uname, email, rank, score, solved, bio in detectives_data:
            user, u_created = User.objects.get_or_create(
                username=uname,
                defaults={'email': email}
            )
            # Set password to detective123 (and if vansh123, allow vansh123 or detective123)
            user.set_password('vansh123' if uname == 'vansh123' else 'detective123')
            user.save()
            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile.rank = rank
            profile.total_score = score
            profile.cases_solved = solved
            profile.bio = bio
            profile.save()

        self.stdout.write(self.style.SUCCESS("Sample detective profiles ready."))

        # 3. Create Case 1: The Midnight Sapphire Heist
        c1, _ = Case.objects.update_or_create(
            title="The Midnight Sapphire Heist",
            defaults={
                'difficulty': 'Medium',
                'status': 'Active',
                'description': "During an opulent thunderstorm gala at Harrington Manor, the priceless 80-carat 'Midnight Sapphire' vanished from Lord Harrington's private biometric vault.",
                'background': "Lord Percival Harrington hosted his annual autumn salon. At 11:45 PM, a sudden lightning strike tripped the mansion's circuit breakers, cutting illumination for precisely 6 minutes. When emergency auxiliary generators kicked in at 11:51 PM, the shatterproof vault was unlocked cleanly without physical damage, and the velvet cushion was bare.",
                'solution_explanation': "Julian Harrington staged a fake car breakdown excuse, snuck into the conservatory using his insider knowledge of estate blindspots, deployed a custom RF cloner to bypass the safe without triggering the alarm, and escaped into the night.",
            }
        )

        s1_1, _ = Suspect.objects.update_or_create(
            name="James Sterling",
            defaults={
                'profile': "Personal Butler. Served the Harrington estate for 18 years. Knows household schedules intimately.",
                'motive': "Deep gambling debts in the underground docks club.",
                'alibi': "Claims he was in the wine cellar procuring vintage Port when the power cut out.",
                'is_culprit': False,
            }
        )
        s1_1.cases.add(c1)

        s1_2, _ = Suspect.objects.update_or_create(
            name="Victoria Ashford",
            defaults={
                'profile': "Gemologist & Appraiser. Renowned London gem specialist hired to evaluate the collection.",
                'motive': "Her consulting firm is facing insolvency and foreclosure.",
                'alibi': "Claims she was in the main drawing room chatting with socialites.",
                'is_culprit': False,
            }
        )
        s1_2.cases.add(c1)

        s1_3, _ = Suspect.objects.update_or_create(
            name="Julian Harrington",
            defaults={
                'profile': "Estranged Nephew. Amateur electronics hacker and disowned family heir.",
                'motive': "Cut out of the family trust fund last month due to reckless conduct.",
                'alibi': "Claims his sports car broke down on West Hill Road two miles away.",
                'is_culprit': True,
            }
        )
        s1_3.cases.add(c1)
        c1.correct_suspect = s1_3
        c1.save()

        clue1_1, _ = Clue.objects.update_or_create(
            case=c1, title="Tripped Digital Bypass Key",
            defaults={
                'clue_type': 'Digital',
                'description': "A custom Arduino frequency emulator was found hidden behind the safe pedestal, replicating Lord Harrington's master fob."
            }
        )
        clue1_2, _ = Clue.objects.update_or_create(
            case=c1, title="Muddy Bootprints in Conservatory",
            defaults={
                'clue_type': 'Physical',
                'description': "Tire-tread and wet clay footprints leading from the conservatory side terrace toward the private study."
            }
        )
        clue1_3, _ = Clue.objects.update_or_create(
            case=c1, title="Torn Silk Ribbon Thread",
            defaults={
                'clue_type': 'Physical',
                'description': "A violet silk thread matching bespoke Savile Row tailored jackets of Harrington family design."
            }
        )
        clue1_4, _ = Clue.objects.update_or_create(
            case=c1, title="Cell-Tower Telemetry Ping",
            defaults={
                'clue_type': 'Location',
                'description': "Tower logs indicate Julian's phone pinged within 100 meters of the estate at 11:47 PM, disproving his West Hill Road breakdown alibi."
            }
        )

        Evidence.objects.update_or_create(
            case=c1, description="High-frequency RF cloner with Julian's latent thumbprint on casing.",
            defaults={'evidence_type': 'Digital Log', 'suspect': s1_3, 'clue': clue1_1}
        )
        Evidence.objects.update_or_create(
            case=c1, description="Violet silk cufflink thread found caught on vault hinge.",
            defaults={'evidence_type': 'Physical Evidence', 'suspect': s1_3, 'clue': clue1_3}
        )

        WitnessStatement.objects.update_or_create(
            case=c1, witness_name="Chef Gaston",
            defaults={
                'credibility': 'High',
                'statement': "I saw Butler James in the pantry with lantern light at 11:46 PM searching for candles; he was nowhere near the study."
            }
        )
        WitnessStatement.objects.update_or_create(
            case=c1, witness_name="Lady Genevieve",
            defaults={
                'credibility': 'High',
                'statement': "Victoria Ashford was with me by the fireplace when the lights went black. She screamed when thunder struck and held my hand."
            }
        )
        WitnessStatement.objects.update_or_create(
            case=c1, witness_name="Chauffeur Harris",
            defaults={
                'credibility': 'High',
                'statement': "I found Nephew Julian's sports car parked behind the estate hedges with the engine hood still warm at midnight."
            }
        )

        # 4. Create Case 2: The Poisoned Cryptographer
        c2, _ = Case.objects.update_or_create(
            title="The Poisoned Cryptographer",
            defaults={
                'difficulty': 'Hard',
                'status': 'Active',
                'description': "Renowned intelligence codebreaker Dr. Alistair Finch was discovered dead in his university study, a half-finished decipherment notebook on his desk and a lethal alkaloid in his tea.",
                'background': "Dr. Finch had been working on the classified 'Boreas Cipher' rumored to expose corporate espionage. On Tuesday evening at 9:00 PM, campus security responded to an unanswered distress buzzer. Finch was slumped over his desk. No forced entry; windows were locked from the inside.",
                'solution_explanation': "Dr. Elena Rostova intercepted the tea tray, spiked the cup with synthetic aconite synthesized in her private laboratory, entered Finch's office before he locked up, and fabricated an alibi with an unused classical recital ticket.",
            }
        )

        s2_1, _ = Suspect.objects.update_or_create(
            name="Dr. Elena Rostova",
            defaults={
                'profile': "Research Partner & Biochemist. Brilliant linguist and toxicologist co-authoring the codebook.",
                'motive': "Finch discovered she was covertly selling decoding algorithms to an offshore syndicate.",
                'alibi': "Claims she left campus at 6:30 PM to attend a classical piano recital in town.",
                'is_culprit': True,
            }
        )
        s2_1.cases.add(c2)

        s2_2, _ = Suspect.objects.update_or_create(
            name="Marcus Thorne",
            defaults={
                'profile': "University Chief Archivist. Bitter academic passed over for department chair in favor of Finch.",
                'motive': "Professional jealousy and intellectual patent disputes.",
                'alibi': "Was cataloging rare manuscripts in the basement archive with timestamped card access.",
                'is_culprit': False,
            }
        )
        s2_2.cases.add(c2)

        s2_3, _ = Suspect.objects.update_or_create(
            name="Liam Vance",
            defaults={
                'profile': "Graduate Courier & Research Assistant. Delivers Finch's mail and daily herbal tea.",
                'motive': "Finch threatened to fail his doctoral thesis for plagiarism.",
                'alibi': "Claims he left the tea tray at Finch's door at 7:15 PM and went to the student union.",
                'is_culprit': False,
            }
        )
        s2_3.cases.add(c2)
        c2.correct_suspect = s2_1
        c2.save()

        clue2_1, _ = Clue.objects.update_or_create(
            case=c2, title="Laced Porcelain Teacup",
            defaults={
                'clue_type': 'Forensic',
                'description': "Spectrometry reveals traces of rare Wolfsbane (Aconite alkaloid) dissolved in Earl Grey tea."
            }
        )
        clue2_2, _ = Clue.objects.update_or_create(
            case=c2, title="Unscanned Recital Ticket",
            defaults={
                'clue_type': 'Textual',
                'description': "Elena's recital ticket was purchased online, but venue scanners confirm the barcode was never scanned at the door."
            }
        )
        clue2_3, _ = Clue.objects.update_or_create(
            case=c2, title="Cipher Sticky Note",
            defaults={
                'clue_type': 'Digital',
                'description': "A scrap of paper reading 'ER-901: Protocol Breached. Meet in laboratory 8:15 PM'."
            }
        )
        clue2_4, _ = Clue.objects.update_or_create(
            case=c2, title="Missing Aconite Reagent Log",
            defaults={
                'clue_type': 'Textual',
                'description': "The biochemistry lab inventory log has a torn page dated Monday, with erasure marks over Dr. Rostova's locker shelf."
            }
        )

        Evidence.objects.update_or_create(
            case=c2, description="Synthetic aconitine batch traces matching Dr. Rostova's restricted laboratory stash.",
            defaults={'evidence_type': 'Chemical Trace', 'suspect': s2_1, 'clue': clue2_1}
        )
        Evidence.objects.update_or_create(
            case=c2, description="Biology quad surveillance footage of Dr. Elena heading towards Finch's annex at 7:55 PM.",
            defaults={'evidence_type': 'CCTV Footage', 'suspect': s2_1, 'clue': clue2_2}
        )

        WitnessStatement.objects.update_or_create(
            case=c2, witness_name="Concert Usher Timothy",
            defaults={
                'credibility': 'High',
                'statement': "The seat corresponding to Dr. Rostova's reservation (Row C, Seat 14) remained conspicuously empty throughout the performance."
            }
        )
        WitnessStatement.objects.update_or_create(
            case=c2, witness_name="Liam Vance",
            defaults={
                'credibility': 'High',
                'statement': "Dr. Elena offered to take the tea kettle from my hands in the hallway, saying she would personally bring it in to Alistair."
            }
        )

        # 5. Create Case 3: The Phantom of Blackwood Manor
        c3, _ = Case.objects.update_or_create(
            title="The Phantom of Blackwood Manor",
            defaults={
                'difficulty': 'Easy',
                'status': 'Active',
                'description': "A first-edition illuminated medieval manuscript vanished from the ancestral library of Blackwood Manor during Lord Sterling's private cocktail hour.",
                'background': "The 14th-century 'Codex Aureus' was kept inside a reinforced mahogany glass display. At 8:30 PM, the glass showcase was found open and empty. The key was supposed to remain on Lord Sterling's pocket watch chain.",
                'solution_explanation': "Silas Vance had made a wax copy of the display key during a prior appraisal visit, slipped into the library while everyone was enjoying piano music, took the manuscript, dropped his distinctive cigar ash, and prepped it for Zurich delivery.",
            }
        )

        s3_1, _ = Suspect.objects.update_or_create(
            name="Silas Vance",
            defaults={
                'profile': "Traveling Antiquarian & Rare Book Dealer. Known for shady transactions on the private black market.",
                'motive': "Already had an overseas private buyer lined up for half a million dollars.",
                'alibi': "Claims he was smoking a cigar on the garden terrace alone.",
                'is_culprit': True,
            }
        )
        s3_1.cases.add(c3)

        s3_2, _ = Suspect.objects.update_or_create(
            name="Lady Eleanor Sterling",
            defaults={
                'profile': "Sister of the Lord. High-society socialite with an expensive lifestyle.",
                'motive': "Resents her brother's refusal to finance her European art gallery tour.",
                'alibi': "Was playing Chopin on the grand piano in front of five guests.",
                'is_culprit': False,
            }
        )
        s3_2.cases.add(c3)

        s3_3, _ = Suspect.objects.update_or_create(
            name="Thomas Higgins",
            defaults={
                'profile': "Veteran Groundskeeper. Rough-hewn estate caretaker of 25 years.",
                'motive': "Dispute over impending tenant cottage rent increases.",
                'alibi': "Was securing the greenhouse storm shutters against the cold wind.",
                'is_culprit': False,
            }
        )
        s3_3.cases.add(c3)
        c3.correct_suspect = s3_1
        c3.save()

        clue3_1, _ = Clue.objects.update_or_create(
            case=c3, title="Wax Key Impression Mold",
            defaults={
                'clue_type': 'Physical',
                'description': "A soft jeweler's wax impression of Lord Sterling's cabinet key discovered discarded in a library potted fern."
            }
        )
        clue3_2, _ = Clue.objects.update_or_create(
            case=c3, title="Fine Cigar Ash near Showcase",
            defaults={
                'clue_type': 'Physical',
                'description': "Rare imported Havana Cuban cigar ash found on the Persian rug directly beside the looted display."
            }
        )
        clue3_3, _ = Clue.objects.update_or_create(
            case=c3, title="Courier Shipping Label",
            defaults={
                'clue_type': 'Textual',
                'description': "A pre-printed express shipping label addressed to a Zurich numbered locker under the pseudonym 'S. Vance'."
            }
        )

        Evidence.objects.update_or_create(
            case=c3, description="Rare Havana cigar band matching the brand Silas Vance carries in his breast pocket.",
            defaults={'evidence_type': 'Incriminating Weapon / Object', 'suspect': s3_1, 'clue': clue3_2}
        )
        WitnessStatement.objects.update_or_create(
            case=c3, witness_name="Guest Mrs. Abernathy",
            defaults={
                'credibility': 'High',
                'statement': "Lady Eleanor never left the piano stool between 8:00 and 8:45 PM; her music was delightful."
            }
        )
        WitnessStatement.objects.update_or_create(
            case=c3, witness_name="Groundskeeper Thomas",
            defaults={
                'credibility': 'High',
                'statement': "I saw Mr. Vance loitering in the library corridor holding a bulky leather briefcase around 8:20 PM."
            }
        )

        # 6. Create Case 4: Curse of the Clockwork Automaton
        c4, _ = Case.objects.update_or_create(
            title="Curse of the Clockwork Automaton",
            defaults={
                'difficulty': 'Medium',
                'status': 'Active',
                'description': "Hours before the Victorian Industrial Grand Exposition, the revolutionary mechanical thinking automaton 'Prometheus' was systematically smashed and had its gear-escapement core removed.",
                'background': "Master horologist and mechanical engineer Edward Drake spent seven years perfecting Prometheus. On Saturday morning, the workshop door was unlocked, gears and springs lay scattered across the floor, and the central gold-plated differential gear was gone.",
                'solution_explanation': "Victor Vance sneaked out of his club early, broke into Drake's workshop using a custom counter-threaded tool, sabotaged the automaton, stole the differential core to eliminate his rival, but left grease and his unique wrench behind.",
            }
        )

        s4_1, _ = Suspect.objects.update_or_create(
            name="Victor Vance",
            defaults={
                'profile': "Rival Mechanical Inventor. Owner of Vance Clockworks, whose competing brass automaton was heavily favored to lose the gold medal.",
                'motive': "Exposition defeat would cause investors to withdraw capital from his firm.",
                'alibi': "Claims he was dining at the Royal Athenaeum Club until midnight.",
                'is_culprit': True,
            }
        )
        s4_1.cases.add(c4)

        s4_2, _ = Suspect.objects.update_or_create(
            name="Clara Bell",
            defaults={
                'profile': "Workshop Apprentice. Talented young machinist underpaid and overworked by Drake.",
                'motive': "Angry that Drake refused to put her name as co-inventor on the patent.",
                'alibi': "Was with her sick mother in Kensington.",
                'is_culprit': False,
            }
        )
        s4_2.cases.add(c4)

        s4_3, _ = Suspect.objects.update_or_create(
            name="Baron Gregory Croft",
            defaults={
                'profile': "Lead Financier. Wealthy industrialist who insured Prometheus for a massive sum.",
                'motive': "Financial speculation on insurance payouts.",
                'alibi': "Attending a private poker game at his gentlemen's club.",
                'is_culprit': False,
            }
        )
        s4_3.cases.add(c4)
        c4.correct_suspect = s4_1
        c4.save()

        clue4_1, _ = Clue.objects.update_or_create(
            case=c4, title="Left-Handed Brass Spanner",
            defaults={
                'clue_type': 'Physical',
                'description': "An unusual counter-clockwise threaded wrench stamped with the insignia of Vance Clockworks."
            }
        )
        clue4_2, _ = Clue.objects.update_or_create(
            case=c4, title="Club Registry Discrepancy",
            defaults={
                'clue_type': 'Textual',
                'description': "The Athenaeum dining registry shows Victor Vance checked out at 10:15 PM, not midnight as he claimed."
            }
        )
        clue4_3, _ = Clue.objects.update_or_create(
            case=c4, title="Whale-Oil Grease Stains",
            defaults={
                'clue_type': 'Forensic',
                'description': "Industrial whale-oil lubricant—unique to Drake's automaton gears—identified on Victor Vance's hired brougham carriage seats."
            }
        )

        Evidence.objects.update_or_create(
            case=c4, description="Left-handed counter-threaded wrench belonging to Victor Vance found beside the vandalized pedestal.",
            defaults={'evidence_type': 'Incriminating Weapon / Object', 'suspect': s4_1, 'clue': clue4_1}
        )
        WitnessStatement.objects.update_or_create(
            case=c4, witness_name="Nightwatchman Miller",
            defaults={
                'credibility': 'High',
                'statement': "I spotted a tall man carrying a heavy iron toolkit and walking with a limp entering the Drake workshop at 11:10 PM. Victor Vance walks with a pronounced limp."
            }
        )
        WitnessStatement.objects.update_or_create(
            case=c4, witness_name="Baron Croft's Card Partner",
            defaults={
                'credibility': 'High',
                'statement': "Baron Croft was at our poker table without leaving until 2:00 AM; he lost three hundred pounds."
            }
        )

        # 7. Create Case 5: The Venetian Masquerade Betrayal
        c5, _ = Case.objects.update_or_create(
            title="The Venetian Masquerade Betrayal",
            defaults={
                'difficulty': 'Hard',
                'status': 'Active',
                'description': "During the Venice Carnival masked ball at Palazzo Ducale, the top-secret peace treaty between sovereign powers was stolen from the ambassador's private dispatch case.",
                'background': "Guests wore elaborate costumes and porcelain masks. At midnight, while fireworks exploded over the Grand Canal, a smoke flare was set off in the ambassador's private salon. When the smoke cleared, the dispatch lock had been picked and the signed treaty was missing.",
                'solution_explanation': "Count Orsini disguised himself in a Golden Harlequin disguise, set off a sulfur smoke distraction, grabbed the treaty, fled via his awaiting gondola, and planned to telegraph foreign buyers in Vienna.",
            }
        )

        s5_1, _ = Suspect.objects.update_or_create(
            name="Count Leonardo Orsini",
            defaults={
                'profile': "Disgraced Venetian Diplomat. Former ambassador ousted due to suspected double-dealing with foreign empires.",
                'motive': "Revenge and selling the treaty terms to hostile powers for vast riches.",
                'alibi': "Claims he was dancing in the main ballroom dressed as a golden harlequin.",
                'is_culprit': True,
            }
        )
        s5_1.cases.add(c5)

        s5_2, _ = Suspect.objects.update_or_create(
            name="Francesca Moretti",
            defaults={
                'profile': "Opera Prima Donna. World-famous soprano performing at the gala; known for political sympathies.",
                'motive': "Sympathetic to revolutionary separatist factions.",
                'alibi': "Singing aria on the balcony overlooking the canal at midnight.",
                'is_culprit': False,
            }
        )
        s5_2.cases.add(c5)

        s5_3, _ = Suspect.objects.update_or_create(
            name="Marco Barone",
            defaults={
                'profile': "Ambassador's Gondolier & Bodyguard. Loyal naval veteran assigned to guard the water entrance.",
                'motive': "Family held hostage by foreign agents (rumored).",
                'alibi': "Stationed on the palace canal steps watching the gondola dock.",
                'is_culprit': False,
            }
        )
        s5_3.cases.add(c5)
        c5.correct_suspect = s5_1
        c5.save()

        clue5_1, _ = Clue.objects.update_or_create(
            case=c5, title="Golden Harlequin Ribbon with Sulfur",
            defaults={
                'clue_type': 'Physical',
                'description': "Torn metallic gold silk ribbon smelling of sulfur potassium nitrate matching the smoke flare."
            }
        )
        clue5_2, _ = Clue.objects.update_or_create(
            case=c5, title="Diplomatic Imperial Wax Trace",
            defaults={
                'clue_type': 'Forensic',
                'description': "Microscopic scarlet wax with the imperial double-eagle seal found on Count Orsini's velvet sleeve."
            }
        )
        clue5_3, _ = Clue.objects.update_or_create(
            case=c5, title="Gondola Route Log",
            defaults={
                'clue_type': 'Location',
                'description': "Water patrol recorded a private black gondola belonging to Orsini departing Palazzo Ducale at 12:08 AM toward the train station."
            }
        )

        Evidence.objects.update_or_create(
            case=c5, description="Sulfur smoke residue on the golden harlequin costume found stashed in Orsini's private palazzo.",
            defaults={'evidence_type': 'Chemical Trace', 'suspect': s5_1, 'clue': clue5_1}
        )
        WitnessStatement.objects.update_or_create(
            case=c5, witness_name="Ambassador Lord Sterling",
            defaults={
                'credibility': 'High',
                'statement': "The thief wore a gilded feathered Harlequin mask and spoke fluent aristocratic Venetian dialect before triggering the smoke device."
            }
        )
        WitnessStatement.objects.update_or_create(
            case=c5, witness_name="Prima Donna Francesca",
            defaults={
                'credibility': 'High',
                'statement': "Hundreds of spectators cheered my midnight performance from the Grand Canal; I was singing until 12:15 AM."
            }
        )

        # 8. Create a sample solved case for Vansh to demonstrate completed investigation progress & accusation
        vansh_user = User.objects.get(username='vansh123')
        prog, _ = UserCaseProgress.objects.update_or_create(
            user=vansh_user, case=c1,
            defaults={
                'completion_status': 'Solved',
                'score': 150,
                'hints_used': 0,
                'investigation_notes': 'Primary suspect Julian Harrington attempted to fabricate breakdown alibi. Cell telemetry ping placed him at east garden hedge at 11:47 PM. Case closed.',
            }
        )
        prog.collected_clues.set([clue1_1, clue1_2, clue1_3, clue1_4])
        Accusation.objects.update_or_create(
            user=vansh_user, case=c1,
            defaults={
                'selected_suspect': s1_3,
                'correctness': True,
                'deduction_notes': 'RF frequency bypass key matches Julian\'s equipment. Muddy footprints and cell ping eliminate any doubt.'
            }
        )

        self.stdout.write(self.style.SUCCESS("All 5 fictional cases, clues, suspects, evidence, and witness statements successfully seeded!"))
