from django.core.management.base import BaseCommand
from base.models import Category, Article, Event


class Command(BaseCommand):
    help = "Seed database with initial categories, tech articles, and events"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE("Seeding database..."))

        # 1. Categories
        categories_data = [
            {
                "name": "Artificial Intelligence",
                "slug": "artificial-intelligence",
                "description": "Next-generation machine learning, neural reasoning, and autonomous intelligence systems.",
                "badge_color": "blue",
            },
            {
                "name": "Privacy & Security",
                "slug": "privacy-security",
                "description": "Zero-knowledge architectures, personal data sovereignty, and cryptography.",
                "badge_color": "purple",
            },
            {
                "name": "Hardware Innovations",
                "slug": "hardware-innovations",
                "description": "Advanced nanomaterials, bio-mimetic circuits, and self-restoring electronics.",
                "badge_color": "emerald",
            },
            {
                "name": "Ubiquitous Computing",
                "slug": "ubiquitous-computing",
                "description": "Ambient intelligence, invisible sensors, and human-computer symbiosis.",
                "badge_color": "amber",
            },
        ]

        cat_objs = {}
        for cat in categories_data:
            obj, created = Category.objects.get_or_create(
                slug=cat["slug"],
                defaults={
                    "name": cat["name"],
                    "description": cat["description"],
                    "badge_color": cat["badge_color"],
                }
            )
            cat_objs[cat["slug"]] = obj
            if created:
                self.stdout.write(f"  Created Category: {obj.name}")

        # 2. Articles
        articles_data = [
            {
                "title": "Digital Memory Assistants: The Rise of Cognitive Copilots",
                "slug": "digital-memory-assistants",
                "category": cat_objs["artificial-intelligence"],
                "author": "Dr. Sarah Chen, AI Systems Lab",
                "short_desc": "AI systems that preserve conversations, locations, and sensory data to serve as an infallible personal auxiliary memory by 2035.",
                "content": """Imagine waking up in 2035 with an infallible second memory that seamlessly catalogs the context of your entire intellectual life. A Digital Memory Assistant does not just transcribe notes—it passively understands spoken dialogues, maps geographical timelines, and links complex project discussions together.

Instead of hunting through fragmented chat threads, nested bookmarks, or discarded notes, you could simply query: 'When did we discuss the distributed cache latency bottleneck last quarter?' Within milliseconds, the cognitive assistant reconstructs the exact meeting snippet, the white-board snapshot, and the subsequent decisions made.

### Transforming Knowledge Work
For engineers, medical practitioners, researchers, and students, this fundamentally eliminates the cognitive tax of trivial recall. Rather than expending mental bandwidth remembering *where* an insight was filed, professionals can direct their focus towards creative synthesis, system design, and decision-making.

### The Ethics of Perfect Recall
However, absolute recall introduces profound philosophical and ethical dilemmas. If every slip of the tongue and candid exchange is perpetually indexed, what happens to human forgiveness and the natural grace of forgetting? Furthermore, who holds the cryptographic keys to this personal timeline? By 2035, the defining challenge will not be engineering models capable of remembering more, but building verifiable governance around what machines are permitted to record and retain.""",
                "image_path": "img/digital memory.jpg",
                "read_time": 5,
                "is_featured": True,
            },
            {
                "title": "Personal Data Vaults: Reclaiming Sovereign Identity",
                "slug": "personal-data-vaults",
                "category": cat_objs["privacy-security"],
                "author": "Marcus Vance, Cryptography Fellow",
                "short_desc": "How encrypted personal repositories and zero-knowledge proofs will dismantle predatory ad-tech data harvesting.",
                "content": """In today's digital landscape, users trade intimate telemetry and behavioral data for convenience. By 2035, the Personal Data Vault model proposes an architectural inversion: your browsing logs, financial statements, biometric records, and social interactions reside inside a client-side encrypted repository where you retain sole cryptographic ownership.

Instead of granting third-party web services unbounded blanket access to your identity, modern Zero-Knowledge protocols allow selective disclosure. You can mathematically verify that you are over 21 years old without disclosing your birth date, or prove proof of residency without revealing your street address.

### Decentralized Trust Architecture
Enterprises will no longer maintain massive honeypots of customer records. Instead, applications will become ephemeral processors that request short-lived, verifiable compute tokens over encrypted enclaves. If a platform breaches trust, access can be revoked instantly at the hardware level.

By 2035, Personal Data Vaults will shift consumer technology from passive data extraction into sovereign data management, proving that personalization and uncompromising privacy can thrive in harmony.""",
                "image_path": "img/personal vault.jpg",
                "read_time": 4,
                "is_featured": False,
            },
            {
                "title": "Self-Healing Electronics: Ending Planned Obsolescence",
                "slug": "self-healing-electronics",
                "category": cat_objs["hardware-innovations"],
                "author": "Elena Rostova, Materials Engineer",
                "short_desc": "Micro-vascular polymers and conductive nanogels that autonomously mend micro-fractures, extending gadget lifespans for decades.",
                "content": """What if a cracked smartphone display or an internal solder rupture could heal itself overnight without a visit to the repair shop? Self-healing electronics integrate micro-capsule matrices and thermo-responsive conductive polymers that detect mechanical strain and trigger autonomous chemical cross-linking.

When a microscopic fracture propagates through a substrate, micro-vascular capillaries release liquid healing agents that polymerize upon contact, restoring electrical conductivity in less than sixty seconds.

### Radical Reduction of E-Waste
Consumer electronics are currently engineered under cycles of planned obsolescence. Hundreds of millions of tons of lithium, rare-earth minerals, and silicon end up in landfills annually due to micro-fissures in motherboards. Self-healing architectures prolong device reliability by an order of magnitude.

By 2035, materials science will cross the threshold from passive structural engineering to biological resilience, ushering in an era of hardware that endures as long as the software driving it.""",
                "image_path": "img/self healing.jpg",
                "read_time": 4,
                "is_featured": False,
            },
            {
                "title": "AI-Generated Personal Software: The Post-App Economy",
                "slug": "ai-generated-personal-software",
                "category": cat_objs["artificial-intelligence"],
                "author": "Devon Miller, Principal Architect",
                "short_desc": "Declarative prompt-driven interfaces where custom applications are compiled on the fly and discarded when tasks conclude.",
                "content": """The traditional app store model forces millions of humans to bend their operational workflows to fit static software interfaces. AI-generated personal software reverses this equation: software becomes ephemeral, synthesized in real-time according to immediate human intent.

Imagine requesting: 'Generate an interactive dashboard that correlates my Garmin fitness telemetry with my calendar stress levels, and alert me when recovery windows open.' Instead of subscribing to three separate SaaS products, a bespoke sandboxed application is compiled, rendered, and validated in seconds.

### The Demise of Monolithic SaaS
When micro-applications can be spun up deterministically on edge devices, the barriers between software engineering and domain problem-solving dissolve. Software evolves into an invisible fluid medium rather than a pre-packaged box product.

By 2035, writing code will remain an essential discipline for foundational infrastructure, while everyday end-user applications will be dynamically tailored to individual ergonomics.""",
                "image_path": "img/ai generated software.jpg",
                "read_time": 4,
                "is_featured": False,
            },
            {
                "title": "Invisible Computing: Merging Environment and Intelligence",
                "slug": "invisible-computing",
                "category": cat_objs["ubiquitous-computing"],
                "author": "Aria Tanaka, Human Interface Design",
                "short_desc": "How ambient sensor fabrics, acoustic haptics, and spatial computing will dissolve the rectangular screen from our lives.",
                "content": """The most profound technologies are those that disappear. They weave themselves into the fabric of everyday life until they are indistinguishable from it. Invisible computing marks the transition away from glowing glass rectangles into pervasive ambient intelligence.

Desks, textiles, architectural walls, and optical waveguides embed low-power sensor arrays that respond to micro-gestures, vocal inflections, and physiological cues. You no longer 'open an application' or 'browse a website'—the environment itself computes and responds to your physical environment.

### Calmer Interfaces for a Distracted World
Current screen-based UX patterns demand constant optical capture and notify us into cognitive exhaustion. In contrast, ambient interfaces practice calm technology: delivering contextual ambient illumination, localized directional acoustic cues, and haptic feedback only when critical attention is required.

By 2035, technology's greatest victory will not be how dazzling its displays look, but how gracefully it recedes into the background to let humans be human.""",
                "image_path": "img/invisible computing.jpg",
                "read_time": 5,
                "is_featured": False,
            },
        ]

        for art in articles_data:
            obj, created = Article.objects.get_or_create(
                slug=art["slug"],
                defaults={
                    "title": art["title"],
                    "category": art["category"],
                    "author": art["author"],
                    "short_desc": art["short_desc"],
                    "content": art["content"],
                    "image_path": art["image_path"],
                    "read_time": art["read_time"],
                    "is_featured": art["is_featured"],
                }
            )
            if created:
                self.stdout.write(f"  Created Article: {obj.title}")
            else:
                # Update fields if already exists
                obj.title = art["title"]
                obj.category = art["category"]
                obj.author = art["author"]
                obj.short_desc = art["short_desc"]
                obj.content = art["content"]
                obj.image_path = art["image_path"]
                obj.read_time = art["read_time"]
                obj.is_featured = art["is_featured"]
                obj.save()

        # 3. Events
        events_data = [
            {
                "title": "CES 2026: Future of Autonomous Hardware",
                "date_str": "Jan 6–9, 2026",
                "location": "Las Vegas, Nevada, USA",
                "category_tag": "Consumer Electronics",
                "description": "The world's premier consumer tech exposition featuring edge AI silicon, bionic robotics, and quantum-resistant IoT devices.",
                "is_featured": True,
                "external_link": "https://www.ces.tech",
            },
            {
                "title": "MWC Barcelona 2026: Next-Gen Connectivity",
                "date_str": "Mar 2–5, 2026",
                "location": "Barcelona, Spain",
                "category_tag": "Telecommunications",
                "description": "Flagship global mobile expo unveiling 6G architectural specifications, terrestrial satellite networks, and next-gen mobile neural NPUs.",
                "is_featured": False,
                "external_link": "https://www.mwcbarcelona.com",
            },
            {
                "title": "NVIDIA GTC 2026: AI Infrastructure Summit",
                "date_str": "Mar 16–19, 2026",
                "location": "San Jose, California, USA",
                "category_tag": "Artificial Intelligence",
                "description": "Deep-dive keynotes into exascale computing, frontier neural architectures, robotics simulation, and industrial digital twins.",
                "is_featured": True,
                "external_link": "https://www.nvidia.com/gtc",
            },
            {
                "title": "Microsoft Ignite 2026",
                "date_str": "Nov 17–20, 2026",
                "location": "San Francisco, California, USA",
                "category_tag": "Enterprise Cloud",
                "description": "Comprehensive enterprise showcase covering autonomous AI agents, multi-cloud cyber defense, and developer platform evolutions.",
                "is_featured": False,
                "external_link": "https://ignite.microsoft.com",
            },
            {
                "title": "AWS re:Invent 2026",
                "date_str": "Nov 30 – Dec 4, 2026",
                "location": "Las Vegas, Nevada, USA",
                "category_tag": "Cloud Computing",
                "description": "The marquee cloud engineering gathering exploring serverless orchestration, planetary-scale vector stores, and custom inferencing silicon.",
                "is_featured": False,
                "external_link": "https://reinvent.awsevents.com",
            },
            {
                "title": "Global AI & Robotics Expo 2026",
                "date_str": "Dec 10–12, 2026",
                "location": "Tokyo, Japan",
                "category_tag": "Robotics",
                "description": "Demonstrations of general-purpose humanoid labor bots, soft robotic actuators, and haptic feedback tele-presence systems.",
                "is_featured": False,
                "external_link": "#",
            },
            {
                "title": "Future Mobility Conference 2026",
                "date_str": "Dec 15–17, 2026",
                "location": "Berlin, Germany",
                "category_tag": "Mobility & CleanTech",
                "description": "Leading summit dedicated to magnetic levitation transit, solid-state battery manufacturing, and intelligent urban routing grids.",
                "is_featured": False,
                "external_link": "#",
            },
        ]

        for evt in events_data:
            obj, created = Event.objects.get_or_create(
                title=evt["title"],
                defaults={
                    "date_str": evt["date_str"],
                    "location": evt["location"],
                    "category_tag": evt["category_tag"],
                    "description": evt["description"],
                    "is_featured": evt["is_featured"],
                    "external_link": evt["external_link"],
                }
            )
            if created:
                self.stdout.write(f"  Created Event: {obj.title}")

        self.stdout.write(self.style.SUCCESS("[OK] Database seeded successfully!"))
