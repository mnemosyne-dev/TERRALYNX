"""
Unified Location & Landmark Geocoding Service for TerraLynx.
Provides lightning-fast, high-precision fuzzy search across Universities,
Hospitals, Administrative Sectors, Cities, and Global Landmarks.
"""

import httpx
import re
from typing import List, Dict, Any, Optional

COMPREHENSIVE_GAZETTEER = [
    # Universities, Colleges & Educational Campuses
    {
        "title": "C. V. Raman Global University (CVRGU)",
        "subtitle": "Mahura, Janla, Bhubaneswar, Odisha 752054",
        "category": "university",
        "category_label": "University / Tech",
        "lat": 20.2198,
        "lng": 85.7358,
        "keywords": ["c.v raman", "cv raman", "cvrgu", "cvrce", "c.v. raman", "c.v raman global university", "cv raman university", "c.v. raman college of engineering", "cvrce bbsr", "mahura", "janla"]
    },
    {
        "title": "IIT Bhubaneswar",
        "subtitle": "Argul, Jatni, Khordha, Odisha 752050",
        "category": "university",
        "category_label": "National Institute",
        "lat": 20.1485,
        "lng": 85.6712,
        "keywords": ["iit", "iit bhubaneswar", "iit bbs", "argul", "jatni iit", "indian institute of technology bhubaneswar"]
    },
    {
        "title": "AIIMS Bhubaneswar",
        "subtitle": "Sijua, Patrapada, Bhubaneswar, Odisha 751019",
        "category": "hospital",
        "category_label": "Apex Hospital / Medical",
        "lat": 20.2312,
        "lng": 85.7766,
        "keywords": ["aiims", "aiims bhubaneswar", "aiims hospital", "sijua", "patrapada aiims", "all india institute of medical sciences"]
    },
    {
        "title": "KIIT Deemed to be University",
        "subtitle": "Patia, Bhubaneswar, Odisha 751024",
        "category": "university",
        "category_label": "University Campus",
        "lat": 20.3533,
        "lng": 85.8189,
        "keywords": ["kiit", "kiit university", "kalinga institute of industrial technology", "patia", "kiss university"]
    },
    {
        "title": "SOA University / ITER",
        "subtitle": "Jagamara, Khandagiri, Bhubaneswar, Odisha 751030",
        "category": "university",
        "category_label": "University / ITER",
        "lat": 20.2520,
        "lng": 85.7950,
        "keywords": ["iter", "soa", "siksha o anusandhan", "iter bhubaneswar", "jagamara", "soa university", "institute of technical education and research"]
    },
    {
        "title": "Silicon University (SiliconTech)",
        "subtitle": "Silicon Hills, Patia, Bhubaneswar, Odisha 751024",
        "category": "university",
        "category_label": "Tech University",
        "lat": 20.3705,
        "lng": 85.8080,
        "keywords": ["silicon", "silicontech", "silicon institute", "silicon university", "silicon hills"]
    },
    {
        "title": "Centurion University (CUTM)",
        "subtitle": "Ramachandrapur, Jatni, Bhubaneswar, Odisha 752050",
        "category": "university",
        "category_label": "University Campus",
        "lat": 20.1745,
        "lng": 85.7065,
        "keywords": ["centurion", "cutm", "centurion university", "ramachandrapur"]
    },
    {
        "title": "GITA Autonomous College",
        "subtitle": "Madanpur, Janla, Bhubaneswar, Odisha 752054",
        "category": "university",
        "category_label": "Engineering College",
        "lat": 20.2110,
        "lng": 85.7315,
        "keywords": ["gita", "gita college", "gita autonomous", "madanpur", "gita bhubaneswar"]
    },
    {
        "title": "Trident Academy of Technology",
        "subtitle": "Infocity Area, Chandrasekharpur, Bhubaneswar, Odisha 751024",
        "category": "university",
        "category_label": "Tech Academy",
        "lat": 20.3470,
        "lng": 85.8115,
        "keywords": ["trident", "trident academy", "infocity trident"]
    },
    {
        "title": "Utkal University (Vani Vihar)",
        "subtitle": "Vani Vihar, Saheed Nagar, Bhubaneswar, Odisha 751004",
        "category": "university",
        "category_label": "State University",
        "lat": 20.3015,
        "lng": 85.8450,
        "keywords": ["utkal", "utkal university", "vani vihar", "saheed nagar"]
    },
    {
        "title": "Ravenshaw University",
        "subtitle": "College Square, Cuttack, Odisha 753003",
        "category": "university",
        "category_label": "Historic University",
        "lat": 20.4635,
        "lng": 85.8942,
        "keywords": ["ravenshaw", "ravenshaw university", "college square cuttack"]
    },
    {
        "title": "SCB Medical College & Hospital",
        "subtitle": "Mangalabag, Cuttack, Odisha 753007",
        "category": "hospital",
        "category_label": "Apex Hospital",
        "lat": 20.4682,
        "lng": 85.8895,
        "keywords": ["scb", "scb medical", "scb medical college", "scb hospital", "mangalabag"]
    },
    {
        "title": "National Law University Odisha (NLUO)",
        "subtitle": "Brahmabarda, CDA Sector 13, Cuttack, Odisha 753015",
        "category": "university",
        "category_label": "Law University",
        "lat": 20.4890,
        "lng": 85.7950,
        "keywords": ["nlu", "nluo", "national law university", "cda sector 13"]
    },
    {
        "title": "Sri Sri University",
        "subtitle": "Bidyadharpur, Arilo, Cuttack, Odisha 754006",
        "category": "university",
        "category_label": "University Campus",
        "lat": 20.4410,
        "lng": 85.7890,
        "keywords": ["sri sri", "sri sri university", "ssu", "arilo"]
    },
    {
        "title": "VSSUT Burla (UCE Burla)",
        "subtitle": "Burla, Sambalpur, Odisha 768018",
        "category": "university",
        "category_label": "Tech University",
        "lat": 21.4975,
        "lng": 83.8760,
        "keywords": ["vssut", "vssut burla", "uce burla", "burla engineering"]
    },
    {
        "title": "NIT Rourkela",
        "subtitle": "Sector 1, Rourkela, Sundargarh, Odisha 769008",
        "category": "university",
        "category_label": "National Institute",
        "lat": 22.2530,
        "lng": 84.9010,
        "keywords": ["nit", "nit rourkela", "nit rkl"]
    },

    # All 30 Districts of Odisha & Administrative Headquarters
    {
        "title": "Cuttack Millennium City",
        "subtitle": "Cuttack Municipal Corporation (CMC), Cuttack, Odisha 753001",
        "category": "city",
        "category_label": "District / City",
        "lat": 20.4625,
        "lng": 85.8828,
        "keywords": ["cuttack", "kataka", "cmc cuttack", "silver city", "cuttack district", "dist cuttack"]
    },
    {
        "title": "Bhubaneswar Capital City",
        "subtitle": "Bhubaneswar Municipal Corporation, Khordha, Odisha 751001",
        "category": "city",
        "category_label": "State Capital / District",
        "lat": 20.2961,
        "lng": 85.8245,
        "keywords": ["bhubaneswar", "bhubaneshwar", "bbsr", "khordha", "khurda", "smart city bhubaneswar", "khordha district"]
    },
    {
        "title": "Puri Coastal District",
        "subtitle": "Puri Municipality, High-Surge Vulnerable Coastal District, Odisha 752001",
        "category": "city",
        "category_label": "Coastal District",
        "lat": 19.8135,
        "lng": 85.8312,
        "keywords": ["puri", "puri beach", "puri coast", "jagannath puri", "puri district", "dist puri"]
    },
    {
        "title": "Ganjam District (Berhampur / Chhatrapur)",
        "subtitle": "Chhatrapur / Berhampur Municipal Corp, High Cyclone Risk District, Odisha 760001",
        "category": "city",
        "category_label": "South Coastal District",
        "lat": 19.3552,
        "lng": 85.0187,
        "keywords": ["ganjam", "ganjam district", "berhampur", "brahmapur", "chhatrapur", "gopalpur", "dist ganjam"]
    },
    {
        "title": "Balasore District (Baleswar)",
        "subtitle": "Balasore Municipality, Coastal Cyclone Gateway District, Odisha 756001",
        "category": "city",
        "category_label": "North Coastal District",
        "lat": 21.4934,
        "lng": 86.9135,
        "keywords": ["balasore", "baleswar", "chandipur", "balasore district", "dist balasore", "baleswar district"]
    },
    {
        "title": "Bhadrak District",
        "subtitle": "Bhadrak Municipality, Salandi & Baitarani River Basin, Odisha 756100",
        "category": "city",
        "category_label": "Coastal District",
        "lat": 21.0544,
        "lng": 86.5008,
        "keywords": ["bhadrak", "bhadrak district", "dhamra", "dist bhadrak"]
    },
    {
        "title": "Kendrapara District",
        "subtitle": "Kendrapara Municipality, Bhitarkanika & Delta Floodplain, Odisha 754211",
        "category": "city",
        "category_label": "Estuary Coastal District",
        "lat": 20.5015,
        "lng": 86.4225,
        "keywords": ["kendrapara", "kendrapara district", "bhitarkanika", "dist kendrapara", "kendrapara dist"]
    },
    {
        "title": "Jagatsinghpur District (Paradeep)",
        "subtitle": "Jagatsinghpur / Paradeep Port Area, Super Cyclone Corridor, Odisha 754103",
        "category": "city",
        "category_label": "Coastal Port District",
        "lat": 20.2588,
        "lng": 86.1685,
        "keywords": ["jagatsinghpur", "jagatsinghpur district", "paradeep", "paradip", "dist jagatsinghpur"]
    },
    {
        "title": "Jajpur District (Jajpur Town / Panikoili)",
        "subtitle": "Baitarani Flood Basin & Industrial Corridor, Odisha 755001",
        "category": "city",
        "category_label": "Inland Flood District",
        "lat": 20.8467,
        "lng": 86.3333,
        "keywords": ["jajpur", "jajpur district", "panikoili", "vyasanagar", "jajpur road", "dist jajpur"]
    },
    {
        "title": "Mayurbhanj District (Baripada)",
        "subtitle": "Baripada, Northern Forest Watershed & Flash Flood District, Odisha 757001",
        "category": "city",
        "category_label": "North Highland District",
        "lat": 21.9322,
        "lng": 86.7389,
        "keywords": ["mayurbhanj", "mayurbhanj district", "baripada", "similipal", "dist mayurbhanj"]
    },
    {
        "title": "Sambalpur District",
        "subtitle": "Sambalpur Municipal Corporation, Hirakud Dam Complex, Odisha 768001",
        "category": "city",
        "category_label": "Major Dam Basin District",
        "lat": 21.4669,
        "lng": 83.9812,
        "keywords": ["sambalpur", "sambalpur district", "hirakud", "burla", "dist sambalpur"]
    },
    {
        "title": "Sundargarh District (Rourkela)",
        "subtitle": "Rourkela Steel City / Sundargarh, Northern Brahmani Basin, Odisha 770001",
        "category": "city",
        "category_label": "Industrial North District",
        "lat": 22.1167,
        "lng": 84.0333,
        "keywords": ["sundargarh", "sundergarh", "rourkela", "sundargarh district", "dist sundargarh"]
    },
    {
        "title": "Keonjhar District (Kendujhar)",
        "subtitle": "Kendujhar Municipality, Baitarani River Headwaters, Odisha 758001",
        "category": "city",
        "category_label": "Highland Watershed District",
        "lat": 21.6289,
        "lng": 85.5817,
        "keywords": ["keonjhar", "kendujhar", "keonjhar district", "dist keonjhar"]
    },
    {
        "title": "Angul District",
        "subtitle": "Angul Municipality, Central Mahanadi & Brahmani Belt, Odisha 759122",
        "category": "city",
        "category_label": "Central Industrial District",
        "lat": 20.8400,
        "lng": 85.1000,
        "keywords": ["angul", "angul district", "talcher", "dist angul"]
    },
    {
        "title": "Dhenkanal District",
        "subtitle": "Dhenkanal Municipality, Central Riverine Belt, Odisha 759001",
        "category": "city",
        "category_label": "Central Basin District",
        "lat": 20.6667,
        "lng": 85.6000,
        "keywords": ["dhenkanal", "dhenkanal district", "dist dhenkanal"]
    },
    {
        "title": "Nayagarh District",
        "subtitle": "Nayagarh Municipality, South Central Hilly Watershed, Odisha 752069",
        "category": "city",
        "category_label": "Central Watershed District",
        "lat": 20.1250,
        "lng": 85.1060,
        "keywords": ["nayagarh", "nayagarh district", "dist nayagarh"]
    },
    {
        "title": "Gajapati District (Paralakhemundi)",
        "subtitle": "Paralakhemundi, Vansadhara River Basin & Mountain Zone, Odisha 761200",
        "category": "city",
        "category_label": "Southern Border District",
        "lat": 18.7750,
        "lng": 84.0900,
        "keywords": ["gajapati", "gajapati district", "paralakhemundi", "dist gajapati"]
    },
    {
        "title": "Rayagada District",
        "subtitle": "Rayagada Municipality, Nagavali & Vansadhara Flash Flood Zone, Odisha 765001",
        "category": "city",
        "category_label": "Southern Highland District",
        "lat": 19.1717,
        "lng": 83.4161,
        "keywords": ["rayagada", "rayagada district", "gunupur", "dist rayagada"]
    },
    {
        "title": "Koraput District (Jeypore)",
        "subtitle": "Koraput / Jeypore, Eastern Ghats Plateau District, Odisha 764020",
        "category": "city",
        "category_label": "Southwest Highland District",
        "lat": 18.8135,
        "lng": 82.7118,
        "keywords": ["koraput", "koraput district", "jeypore", "dist koraput"]
    },
    {
        "title": "Malkangiri District",
        "subtitle": "Malkangiri Municipality, Sabari River Basin Vulnerable Border, Odisha 764045",
        "category": "city",
        "category_label": "Southern Floodplain District",
        "lat": 18.3436,
        "lng": 81.9028,
        "keywords": ["malkangiri", "malkangiri district", "dist malkangiri", "balimela"]
    },
    {
        "title": "Nabarangpur District",
        "subtitle": "Nabarangpur Municipality, Indravati Basin Agro-District, Odisha 764059",
        "category": "city",
        "category_label": "Southern Agro District",
        "lat": 19.2319,
        "lng": 82.5511,
        "keywords": ["nabarangpur", "nabarangpur district", "nowrangpur", "dist nabarangpur"]
    },
    {
        "title": "Kalahandi District (Bhawanipatna)",
        "subtitle": "Bhawanipatna Municipality, Tel River Basin, Odisha 766001",
        "category": "city",
        "category_label": "Western Valley District",
        "lat": 19.9075,
        "lng": 83.1644,
        "keywords": ["kalahandi", "kalahandi district", "bhawanipatna", "dist kalahandi"]
    },
    {
        "title": "Nuapada District",
        "subtitle": "Nuapada Municipality, Jonk River Western Border District, Odisha 766105",
        "category": "city",
        "category_label": "Western Border District",
        "lat": 20.8333,
        "lng": 82.5333,
        "keywords": ["nuapada", "nuapada district", "khariar", "dist nuapada"]
    },
    {
        "title": "Bolangir District (Balangir)",
        "subtitle": "Balangir Municipality, Western Mahanadi Tributary Agro-Belt, Odisha 767001",
        "category": "city",
        "category_label": "Western Agro District",
        "lat": 20.7107,
        "lng": 83.4855,
        "keywords": ["bolangir", "balangir", "bolangir district", "dist bolangir"]
    },
    {
        "title": "Subarnapur District (Sonepur)",
        "subtitle": "Sonepur, Mahanadi & Tel River Confluence Delta, Odisha 767017",
        "category": "city",
        "category_label": "River Confluence District",
        "lat": 20.8417,
        "lng": 83.9167,
        "keywords": ["subarnapur", "sonepur", "subarnapur district", "sonepur district", "dist subarnapur"]
    },
    {
        "title": "Boudh District (Baudh)",
        "subtitle": "Baudh Municipality, Central Mahanadi Valley District, Odisha 762014",
        "category": "city",
        "category_label": "Central Riverine District",
        "lat": 20.8350,
        "lng": 84.3250,
        "keywords": ["boudh", "baudh", "boudh district", "dist boudh"]
    },
    {
        "title": "Kandhamal District (Phulbani)",
        "subtitle": "Phulbani, Central Highland Hill Range & Flash Flood Zone, Odisha 762001",
        "category": "city",
        "category_label": "Highland Hill District",
        "lat": 20.4700,
        "lng": 84.2300,
        "keywords": ["kandhamal", "kandhamal district", "phulbani", "daringbadi", "dist kandhamal"]
    },
    {
        "title": "Bargarh District",
        "subtitle": "Bargarh Municipality, Hirakud Command Agro-District, Odisha 768028",
        "category": "city",
        "category_label": "Western Command District",
        "lat": 21.3333,
        "lng": 83.6167,
        "keywords": ["bargarh", "bargarh district", "dist bargarh", "baragarh"]
    },
    {
        "title": "Jharsuguda District",
        "subtitle": "Jharsuguda Municipal Corporation, Ib River Valley Industrial Hub, Odisha 768201",
        "category": "city",
        "category_label": "Industrial West District",
        "lat": 21.8554,
        "lng": 84.0086,
        "keywords": ["jharsuguda", "jharsuguda district", "dist jharsuguda"]
    },
    {
        "title": "Deogarh District (Debagarh)",
        "subtitle": "Debagarh Municipality, Northern Brahmani Basin, Odisha 768108",
        "category": "city",
        "category_label": "North Central District",
        "lat": 21.5333,
        "lng": 84.7333,
        "keywords": ["deogarh", "debagarh", "deogarh district", "dist deogarh"]
    },

    # Major Coastal Disaster Hubs across Eastern & Southern India
    {
        "title": "Visakhapatnam Metropolitan Port",
        "subtitle": "Greater Visakhapatnam Municipal Corporation (GVMC), Andhra Pradesh",
        "category": "city",
        "category_label": "Coastal Apex Port",
        "lat": 17.6868,
        "lng": 83.2185,
        "keywords": ["visakhapatnam", "vizag", "vizag port", "gvmc"]
    },
    {
        "title": "East Godavari (Kakinada Port)",
        "subtitle": "Kakinada, Godavari Delta Lowland Surge Corridor, Andhra Pradesh",
        "category": "city",
        "category_label": "Coastal Delta District",
        "lat": 16.9891,
        "lng": 82.2475,
        "keywords": ["kakinada", "east godavari", "godavari delta"]
    },
    {
        "title": "Srikakulam Coastal District",
        "subtitle": "Srikakulam Municipality, Vamsadhara Basin Surge Corridor, Andhra Pradesh",
        "category": "city",
        "category_label": "Coastal Surge District",
        "lat": 18.2969,
        "lng": 83.8967,
        "keywords": ["srikakulam", "srikakulam district", "bhavanapadu"]
    },
    {
        "title": "South 24 Parganas (Sundarbans)",
        "subtitle": "Sundarbans Estuary Delta High Surge Risk District, West Bengal",
        "category": "city",
        "category_label": "Estuary Delta District",
        "lat": 22.1452,
        "lng": 88.5430,
        "keywords": ["south 24 parganas", "sundarbans", "kakdwip", "sagar island"]
    },
    {
        "title": "East Medinipur (Digha / Haldia)",
        "subtitle": "Digha Coastal Beach & Haldia Port Industrial Complex, West Bengal",
        "category": "city",
        "category_label": "Coastal Surge District",
        "lat": 21.9300,
        "lng": 87.7700,
        "keywords": ["digha", "haldia", "east medinipur", "purba medinipur"]
    },

    # Local Municipal Sectors & Suburbs
    {
        "title": "CDA Sector 9, Cuttack",
        "subtitle": "Bidanasi Colony, CDA Sector 9, Cuttack, Odisha 753014",
        "category": "suburb",
        "category_label": "Municipal Sector",
        "lat": 20.47937,
        "lng": 85.82872,
        "keywords": ["cda sector 9", "cda sec 9", "cda 9", "cda sector 9 cuttack", "bidanasi sector 9"]
    },
    {
        "title": "CDA Sector 6, Cuttack",
        "subtitle": "CDA Sector 6, Cuttack, Odisha 753014",
        "category": "suburb",
        "category_label": "Municipal Sector",
        "lat": 20.47658,
        "lng": 85.84028,
        "keywords": ["cda sector 6", "cda sec 6", "cda 6", "cda sector vi"]
    },
    {
        "title": "CDA Sector 10, Cuttack",
        "subtitle": "CDA Sector 10, Cuttack, Odisha 753014",
        "category": "suburb",
        "category_label": "Municipal Sector",
        "lat": 20.48354,
        "lng": 85.81933,
        "keywords": ["cda sector 10", "cda sec 10", "cda 10"]
    },
    {
        "title": "CDA Sector 11, Cuttack",
        "subtitle": "CDA Sector 11, Cuttack, Odisha 753014",
        "category": "suburb",
        "category_label": "Municipal Sector",
        "lat": 20.47979,
        "lng": 85.81866,
        "keywords": ["cda sector 11", "cda sec 11", "cda 11"]
    },
    {
        "title": "CDA Sector 7, Cuttack",
        "subtitle": "CDA Sector 7, Cuttack, Odisha 753014",
        "category": "suburb",
        "category_label": "Municipal Sector",
        "lat": 20.4820,
        "lng": 85.8360,
        "keywords": ["cda sector 7", "cda sec 7", "cda 7"]
    },
    {
        "title": "CDA Sector 8, Cuttack",
        "subtitle": "CDA Sector 8, Cuttack, Odisha 753014",
        "category": "suburb",
        "category_label": "Municipal Sector",
        "lat": 20.4860,
        "lng": 85.8320,
        "keywords": ["cda sector 8", "cda sec 8", "cda 8"]
    },
    {
        "title": "Bidanasi Embankment, Cuttack",
        "subtitle": "Bidanasi Old Village & Mahanadi Embankment Lowlands, Cuttack 753014",
        "category": "suburb",
        "category_label": "River Embankment",
        "lat": 20.4710,
        "lng": 85.8230,
        "keywords": ["bidanasi", "bidanasi cuttack", "bidanasi embankment"]
    }
]

def clean_search_term(term: str) -> str:
    if not term:
        return ""
    t = term.lower().strip()
    t = re.sub(r'[\.\,\-\_\/\(\)\'\"\#]', ' ', t)
    t = re.sub(r'\s+', ' ', t).strip()
    # Common administrative terms to normalize
    t = re.sub(r'\b(district|dist|headquarters|hq|block|tehsil)\b', '', t)
    t = re.sub(r'\s+', ' ', t).strip()
    # Common phonetic and vernacular variants
    t = t.replace('bhubaneshwar', 'bhubaneswar')
    t = t.replace('kataka', 'cuttack')
    t = t.replace('paradip', 'paradeep')
    t = t.replace('baleswar', 'balasore')
    return t

def score_gazetteer_item(item: Dict[str, Any], query_clean: str, query_tokens: List[str]) -> int:
    score = 0
    clean_title = clean_search_term(item["title"])
    
    # 1. Direct match with exact keywords
    for kw in item.get("keywords", []):
        ckw = clean_search_term(kw)
        if query_clean == ckw:
            return 300
        if ckw.startswith(query_clean) or query_clean.startswith(ckw):
            score = max(score, 220)
        elif query_clean in ckw:
            score = max(score, 180)
            
    # 2. Match with Title
    if query_clean == clean_title:
        return 300
    if clean_title.startswith(query_clean) or query_clean.startswith(clean_title):
        score = max(score, 200)
    elif query_clean in clean_title:
        score = max(score, 160)
        
    # 3. Token-based overlap
    title_tokens = set(clean_title.split())
    matched_title_tokens = sum(1 for tok in query_tokens if tok in title_tokens)
    if matched_title_tokens == len(query_tokens) and len(query_tokens) > 1:
        score = max(score, 190)
    elif matched_title_tokens > 0:
        score = max(score, matched_title_tokens * 40)
        
    return score

def search_local_gazetteer(query: str) -> List[Dict[str, Any]]:
    cq = clean_search_term(query)
    tokens = [tok for tok in cq.split() if len(tok) > 1 and tok not in ("in", "of", "and", "the", "at", "to")]
    
    scored = []
    for item in COMPREHENSIVE_GAZETTEER:
        s = score_gazetteer_item(item, cq, tokens)
        if s > 0:
            scored.append((s, item))
            
    scored.sort(key=lambda x: -x[0])
    return [item for score, item in scored[:10]]

async def search_photon_osm_live(query: str) -> List[Dict[str, Any]]:
    cq = clean_search_term(query)
    url = f"https://photon.komoot.io/api/?q={httpx.URL('', params={'q': cq}).params['q']}&limit=6"
    results = []
    try:
        async with httpx.AsyncClient(timeout=3.5) as client:
            res = await client.get(url)
            if res.status_code == 200:
                data = res.json()
                for feat in data.get("features", []):
                    props = feat.get("properties", {})
                    coords = feat.get("geometry", {}).get("coordinates", [])
                    if not coords or len(coords) < 2:
                        continue
                    name = props.get("name") or props.get("city") or props.get("district") or props.get("county") or ""
                    if not name:
                        continue
                    state = props.get("state") or props.get("county") or ""
                    country = props.get("country") or ""
                    sub = f"{state}, {country}" if state and country else state or country
                    osm_type = props.get("type", "locality")
                    
                    cat = "university" if any(w in name.lower() for w in ["university", "college", "institute", "campus"]) else \
                          "hospital" if any(w in name.lower() for w in ["hospital", "medical", "clinic", "health"]) else \
                          "city" if osm_type in ("city", "town", "administrative") else "locality"
                          
                    cat_label = "University / Institute" if cat == "university" else \
                                "Hospital" if cat == "hospital" else \
                                "City / Region" if cat == "city" else "Location"

                    results.append({
                        "title": name,
                        "subtitle": f"{name}, {sub}" if sub else name,
                        "category": cat,
                        "category_label": cat_label,
                        "lat": round(float(coords[1]), 5),
                        "lng": round(float(coords[0]), 5),
                    })
    except Exception:
        pass
    return results

async def search_locations(query: str) -> List[Dict[str, Any]]:
    """
    Unified multi-layered search combining local high-precision landmark gazetteer
    and live Photon OpenStreetMap engine.
    """
    if not query or len(query.strip()) < 2:
        return []
        
    gazetteer_items = search_local_gazetteer(query)
    photon_items = await search_photon_osm_live(query)
    
    combined: List[Dict[str, Any]] = []
    seen = set()
    
    # Prioritize gazetteer items
    for g in gazetteer_items:
        key = (round(g["lat"], 2), round(g["lng"], 2))
        if key not in seen:
            seen.add(key)
            combined.append({
                "title": g["title"],
                "subtitle": g["subtitle"],
                "category": g["category"],
                "category_label": g["category_label"],
                "lat": g["lat"],
                "lng": g["lng"]
            })
            
    # Append photon results
    for p in photon_items:
        key = (round(p["lat"], 2), round(p["lng"], 2))
        if key not in seen:
            seen.add(key)
            combined.append(p)
            
    return combined[:12]
