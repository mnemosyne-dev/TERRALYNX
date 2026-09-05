"""
Pan-India Unified Location & Landmark Geocoding Service for TerraLynx.
Provides dynamic search indexing across all 28 States & 8 UTs of India,
high-risk coastal cyclone corridors, river basins, universities, and hospitals.
"""

import httpx
import re
from typing import List, Dict, Any

PAN_INDIA_GAZETTEER = [
    # ==================== ODISHA (ALL 30 DISTRICTS) ====================
    {"title": "Cuttack Millennium City", "subtitle": "CMC, Cuttack, Odisha 753001", "category": "district", "category_label": "District / City", "lat": 20.4625, "lng": 85.8828, "keywords": ["cuttack", "kataka", "cuttack district", "dist cuttack"]},
    {"title": "Bhubaneswar Capital City", "subtitle": "BMC, Khordha, Odisha 751001", "category": "district", "category_label": "State Capital", "lat": 20.2961, "lng": 85.8245, "keywords": ["bhubaneswar", "bhubaneshwar", "bbsr", "khordha", "khurda"]},
    {"title": "Puri Coastal District", "subtitle": "High-Surge Coastal District, Odisha 752001", "category": "district", "category_label": "Coastal District", "lat": 19.8135, "lng": 85.8312, "keywords": ["puri", "puri beach", "puri coast", "puri district"]},
    {"title": "Ganjam District (Berhampur / Chhatrapur)", "subtitle": "South Coastal Cyclone Risk, Odisha 760001", "category": "district", "category_label": "South Coastal District", "lat": 19.3552, "lng": 85.0187, "keywords": ["ganjam", "berhampur", "chhatrapur", "gopalpur"]},
    {"title": "Balasore District (Baleswar)", "subtitle": "North Coastal Cyclone Gateway, Odisha 756001", "category": "district", "category_label": "North Coastal District", "lat": 21.4934, "lng": 86.9135, "keywords": ["balasore", "baleswar", "chandipur"]},
    {"title": "Bhadrak District", "subtitle": "Salandi & Baitarani Basin, Odisha 756100", "category": "district", "category_label": "Coastal District", "lat": 21.0544, "lng": 86.5008, "keywords": ["bhadrak", "dhamra"]},
    {"title": "Kendrapara District", "subtitle": "Bhitarkanika & Delta Floodplain, Odisha 754211", "category": "district", "category_label": "Estuary District", "lat": 20.5015, "lng": 86.4225, "keywords": ["kendrapara", "bhitarkanika"]},
    {"title": "Jagatsinghpur District (Paradeep)", "subtitle": "Deepwater Port Super-Cyclone Corridor, Odisha", "category": "district", "category_label": "Port District", "lat": 20.2588, "lng": 86.1685, "keywords": ["jagatsinghpur", "paradeep", "paradip"]},
    {"title": "Jajpur District", "subtitle": "Baitarani Flood Basin, Odisha 755001", "category": "district", "category_label": "Flood Basin", "lat": 20.8467, "lng": 86.3333, "keywords": ["jajpur", "jajpur road", "panikoili"]},
    {"title": "Mayurbhanj District (Baripada)", "subtitle": "Northern Forest Watershed, Odisha 757001", "category": "district", "category_label": "Highland District", "lat": 21.9322, "lng": 86.7389, "keywords": ["mayurbhanj", "baripada", "similipal"]},
    {"title": "Sambalpur District", "subtitle": "Hirakud Dam Complex, Odisha 768001", "category": "district", "category_label": "Dam Basin District", "lat": 21.4669, "lng": 83.9812, "keywords": ["sambalpur", "hirakud", "burla"]},
    {"title": "Sundargarh District (Rourkela)", "subtitle": "Brahmani Basin Industrial Hub, Odisha 770001", "category": "district", "category_label": "Industrial District", "lat": 22.1167, "lng": 84.0333, "keywords": ["sundargarh", "rourkela", "sundergarh"]},
    {"title": "Keonjhar District (Kendujhar)", "subtitle": "Baitarani Headwaters, Odisha 758001", "category": "district", "category_label": "Highland District", "lat": 21.6289, "lng": 85.5817, "keywords": ["keonjhar", "kendujhar"]},
    {"title": "Angul District", "subtitle": "Central Mahanadi Basin, Odisha 759122", "category": "district", "category_label": "Central District", "lat": 20.8400, "lng": 85.1000, "keywords": ["angul", "talcher"]},
    {"title": "Dhenkanal District", "subtitle": "Central Riverine Belt, Odisha 759001", "category": "district", "category_label": "Central Basin", "lat": 20.6667, "lng": 85.6000, "keywords": ["dhenkanal"]},
    {"title": "Nayagarh District", "subtitle": "South Central Hilly Watershed, Odisha 752069", "category": "district", "category_label": "Watershed District", "lat": 20.1250, "lng": 85.1060, "keywords": ["nayagarh"]},
    {"title": "Gajapati District (Paralakhemundi)", "subtitle": "Vansadhara Basin, Odisha 761200", "category": "district", "category_label": "Border District", "lat": 18.7750, "lng": 84.0900, "keywords": ["gajapati", "paralakhemundi"]},
    {"title": "Rayagada District", "subtitle": "Nagavali & Vansadhara Flash Flood Zone, Odisha", "category": "district", "category_label": "Highland District", "lat": 19.1717, "lng": 83.4161, "keywords": ["rayagada", "gunupur"]},
    {"title": "Koraput District (Jeypore)", "subtitle": "Eastern Ghats Plateau District, Odisha 764020", "category": "district", "category_label": "Plateau District", "lat": 18.8135, "lng": 82.7118, "keywords": ["koraput", "jeypore"]},
    {"title": "Malkangiri District", "subtitle": "Sabari River Basin Vulnerable Border, Odisha", "category": "district", "category_label": "Floodplain District", "lat": 18.3436, "lng": 81.9028, "keywords": ["malkangiri", "balimela"]},
    {"title": "Nabarangpur District", "subtitle": "Indravati Basin Agro-District, Odisha 764059", "category": "district", "category_label": "Agro District", "lat": 19.2319, "lng": 82.5511, "keywords": ["nabarangpur", "nowrangpur"]},
    {"title": "Kalahandi District (Bhawanipatna)", "subtitle": "Tel River Basin, Odisha 766001", "category": "district", "category_label": "Valley District", "lat": 19.9075, "lng": 83.1644, "keywords": ["kalahandi", "bhawanipatna"]},
    {"title": "Nuapada District", "subtitle": "Jonk River Western Border, Odisha 766105", "category": "district", "category_label": "Border District", "lat": 20.8333, "lng": 82.5333, "keywords": ["nuapada", "khariar"]},
    {"title": "Bolangir District (Balangir)", "subtitle": "Western Mahanadi Tributary Agro-Belt, Odisha", "category": "district", "category_label": "Agro District", "lat": 20.7107, "lng": 83.4855, "keywords": ["bolangir", "balangir"]},
    {"title": "Subarnapur District (Sonepur)", "subtitle": "Mahanadi-Tel Confluence Delta, Odisha 767017", "category": "district", "category_label": "Confluence District", "lat": 20.8417, "lng": 83.9167, "keywords": ["subarnapur", "sonepur"]},
    {"title": "Boudh District (Baudh)", "subtitle": "Central Mahanadi Valley District, Odisha 762014", "category": "district", "category_label": "Valley District", "lat": 20.8350, "lng": 84.3250, "keywords": ["boudh", "baudh"]},
    {"title": "Kandhamal District (Phulbani)", "subtitle": "Central Hill Range Flash Flood Zone, Odisha", "category": "district", "category_label": "Hill District", "lat": 20.4700, "lng": 84.2300, "keywords": ["kandhamal", "phulbani", "daringbadi"]},
    {"title": "Bargarh District", "subtitle": "Hirakud Command Area Agro-District, Odisha", "category": "district", "category_label": "Command District", "lat": 21.3333, "lng": 83.6167, "keywords": ["bargarh", "baragarh"]},
    {"title": "Jharsuguda District", "subtitle": "Ib River Valley Industrial Belt, Odisha 768201", "category": "district", "category_label": "Industrial District", "lat": 21.8554, "lng": 84.0086, "keywords": ["jharsuguda"]},
    {"title": "Deogarh District (Debagarh)", "subtitle": "Northern Brahmani Basin, Odisha 768108", "category": "district", "category_label": "Basin District", "lat": 21.5333, "lng": 84.7333, "keywords": ["deogarh", "debagarh"]},

    # ==================== METROS & NATIONAL CAPITALS ====================
    {"title": "New Delhi / NCR", "subtitle": "National Capital Territory of India", "category": "city", "category_label": "National Capital", "lat": 28.6139, "lng": 77.2090, "keywords": ["delhi", "new delhi", "ncr", "noida", "gurugram"]},
    {"title": "Mumbai Metropolitan Region", "subtitle": "Maharashtra Coastal Financial Capital", "category": "city", "category_label": "Financial Metro", "lat": 19.0760, "lng": 72.8777, "keywords": ["mumbai", "bombay", "thane", "navi mumbai"]},
    {"title": "Kolkata Metropolitan Area", "subtitle": "Hooghly River Delta Core, West Bengal", "category": "city", "category_label": "Eastern Metro", "lat": 22.5726, "lng": 88.3639, "keywords": ["kolkata", "calcutta", "howrah"]},
    {"title": "Chennai Metropolitan Area", "subtitle": "Coromandel Coast Coastal Metro, Tamil Nadu", "category": "city", "category_label": "Coastal Metro", "lat": 13.0827, "lng": 80.2707, "keywords": ["chennai", "madras"]},
    {"title": "Bengaluru (Bangalore)", "subtitle": "State Capital, Karnataka", "category": "city", "category_label": "Southern Metro", "lat": 12.9716, "lng": 77.5946, "keywords": ["bengaluru", "bangalore"]},
    {"title": "Hyderabad Metropolitan City", "subtitle": "State Capital, Telangana", "category": "city", "category_label": "Metropolitan City", "lat": 17.3850, "lng": 78.4867, "keywords": ["hyderabad", "secunderabad"]},
    {"title": "Ahmedabad Metropolitan City", "subtitle": "Sabarmati Basin Core, Gujarat", "category": "city", "category_label": "Major Metro", "lat": 23.0225, "lng": 72.5714, "keywords": ["ahmedabad", "gandhinagar"]},
    {"title": "Pune City", "subtitle": "Western Ghats Plateau Metro, Maharashtra", "category": "city", "category_label": "Major Metro", "lat": 18.5204, "lng": 73.8567, "keywords": ["pune"]},
    {"title": "Jaipur Pink City", "subtitle": "State Capital, Rajasthan", "category": "city", "category_label": "State Capital", "lat": 26.9124, "lng": 75.7873, "keywords": ["jaipur"]},
    {"title": "Lucknow City", "subtitle": "Gomti River Basin Capital, Uttar Pradesh", "category": "city", "category_label": "State Capital", "lat": 26.8467, "lng": 80.9462, "keywords": ["lucknow"]},
    {"title": "Chandigarh Union Territory", "subtitle": "Capital of Punjab and Haryana", "category": "city", "category_label": "Union Territory", "lat": 30.7333, "lng": 76.7794, "keywords": ["chandigarh", "mohali", "panchkula"]},

    # ==================== COASTAL CYCLONE CORRIDORS ====================
    # West Bengal
    {"title": "South 24 Parganas (Sundarbans)", "subtitle": "Sundarbans Delta High-Risk Surge Zone, West Bengal", "category": "district", "category_label": "Coastal Delta", "lat": 22.1452, "lng": 88.5430, "keywords": ["sundarbans", "south 24 parganas", "kakdwip", "sagar island"]},
    {"title": "East Medinipur (Digha / Haldia)", "subtitle": "Coastal Beach & Port Complex, West Bengal", "category": "district", "category_label": "Coastal Surge Zone", "lat": 21.9300, "lng": 87.7700, "keywords": ["digha", "haldia", "east medinipur", "purba medinipur"]},
    {"title": "North 24 Parganas", "subtitle": "Ganga-Brahmaputra Deltaic Belt, West Bengal", "category": "district", "category_label": "Delta District", "lat": 22.7230, "lng": 88.4800, "keywords": ["north 24 parganas", "barasat", "basirhat"]},

    # Andhra Pradesh
    {"title": "Visakhapatnam Metropolitan Port", "subtitle": "GVMC, Coastal Apex Port, Andhra Pradesh", "category": "district", "category_label": "Coastal Port", "lat": 17.6868, "lng": 83.2185, "keywords": ["visakhapatnam", "vizag", "vizag port"]},
    {"title": "East Godavari (Kakinada)", "subtitle": "Godavari Delta Surge Corridor, Andhra Pradesh", "category": "district", "category_label": "Coastal Delta", "lat": 16.9891, "lng": 82.2475, "keywords": ["kakinada", "east godavari", "godavari"]},
    {"title": "Srikakulam Coastal District", "subtitle": "Vansadhara Basin Cyclone Corridor, Andhra Pradesh", "category": "district", "category_label": "Coastal District", "lat": 18.2969, "lng": 83.8967, "keywords": ["srikakulam"]},
    {"title": "Krishna District (Machilipatnam)", "subtitle": "Krishna River Delta Lowlands, Andhra Pradesh", "category": "district", "category_label": "Delta District", "lat": 16.1800, "lng": 81.1300, "keywords": ["machilipatnam", "krishna district", "vijayawada"]},
    {"title": "Nellore District (Sri Potti Sriramulu)", "subtitle": "Penna River Coastal Lowlands, Andhra Pradesh", "category": "district", "category_label": "Coastal District", "lat": 14.4426, "lng": 79.9865, "keywords": ["nellore"]},

    # Tamil Nadu & Puducherry
    {"title": "Cuddalore Coastal District", "subtitle": "High Cyclone Inundation Zone, Tamil Nadu", "category": "district", "category_label": "Coastal District", "lat": 11.7480, "lng": 79.7714, "keywords": ["cuddalore"]},
    {"title": "Nagapattinam Coastal District", "subtitle": "Cauvery Delta Vulnerable Coast, Tamil Nadu", "category": "district", "category_label": "Delta District", "lat": 10.7672, "lng": 79.8423, "keywords": ["nagapattinam", "velankanni"]},
    {"title": "Kanyakumari District", "subtitle": "Southern Peninsula Cape, Tamil Nadu", "category": "district", "category_label": "Coastal District", "lat": 8.0883, "lng": 77.5385, "keywords": ["kanyakumari", "nagercoil"]},
    {"title": "Puducherry (Pondicherry)", "subtitle": "Coromandel Coastal Union Territory", "category": "district", "category_label": "Union Territory", "lat": 11.9416, "lng": 79.8083, "keywords": ["puducherry", "pondicherry"]},

    # Gujarat
    {"title": "Kutch District (Bhuj / Gandhidham)", "subtitle": "Arabian Sea Coastal Surge Corridor, Gujarat", "category": "district", "category_label": "Coastal District", "lat": 23.2420, "lng": 69.6669, "keywords": ["kutch", "bhuj", "gandhidham", "kandla"]},
    {"title": "Jamnagar Coastal District", "subtitle": "Gulf of Kutch Coastal Belt, Gujarat", "category": "district", "category_label": "Coastal District", "lat": 22.4707, "lng": 70.0577, "keywords": ["jamnagar"]},
    {"title": "Surat Metropolitan City", "subtitle": "Tapi River Delta Floodplain, Gujarat", "category": "district", "category_label": "Coastal Port", "lat": 21.1702, "lng": 72.8311, "keywords": ["surat"]},
    {"title": "Bhavnagar Coastal District", "subtitle": "Gulf of Khambhat Surge Corridor, Gujarat", "category": "district", "category_label": "Coastal District", "lat": 21.7645, "lng": 72.1519, "keywords": ["bhavnagar"]},

    # Kerala, Goa & Maharashtra Coast
    {"title": "Ernakulam District (Kochi)", "subtitle": "Arabian Sea Major Port & Backwaters, Kerala", "category": "district", "category_label": "Coastal Port", "lat": 9.9312, "lng": 76.2673, "keywords": ["kochi", "cochin", "ernakulam"]},
    {"title": "Alappuzha (Alleppey)", "subtitle": "Vulnerable Coastal Backwaters Lowlands, Kerala", "category": "district", "category_label": "Backwater District", "lat": 9.4981, "lng": 76.3388, "keywords": ["alappuzha", "alleppey"]},
    {"title": "Wayanad Highland District", "subtitle": "Western Ghats Landslide Sensitive Zone, Kerala", "category": "district", "category_label": "Landslide Zone", "lat": 11.6854, "lng": 76.1320, "keywords": ["wayanad", "kalpetta", "meppadi"]},
    {"title": "North Goa (Panaji)", "subtitle": "Mandovi River Estuary Coast, Goa", "category": "district", "category_label": "Coastal District", "lat": 15.4909, "lng": 73.8278, "keywords": ["goa", "panaji", "panjim"]},
    {"title": "Ratnagiri Coastal District", "subtitle": "Konkan Coastal Surging Belt, Maharashtra", "category": "district", "category_label": "Coastal District", "lat": 16.9902, "lng": 73.3120, "keywords": ["ratnagiri"]},

    # Major River Flood Basins (Brahmaputra, Ganga, Kosi)
    {"title": "Guwahati Metropolitan Area", "subtitle": "Brahmaputra River Basin Core, Assam", "category": "district", "category_label": "River Basin Core", "lat": 26.1445, "lng": 91.7362, "keywords": ["guwahati", "kamrup", "assam"]},
    {"title": "Dibrugarh District", "subtitle": "Upper Brahmaputra Flood-Prone Basin, Assam", "category": "district", "category_label": "River Basin", "lat": 27.4728, "lng": 94.9120, "keywords": ["dibrugarh"]},
    {"title": "Patna Metropolitan City", "subtitle": "Ganga River Basin Capital, Bihar", "category": "district", "category_label": "River Basin", "lat": 25.5941, "lng": 85.1376, "keywords": ["patna", "bihar"]},
    {"title": "Muzaffarpur District", "subtitle": "Burhi Gandak River Flood Zone, Bihar", "category": "district", "category_label": "Flood Basin", "lat": 26.1209, "lng": 85.3647, "keywords": ["muzaffarpur"]},
    {"title": "Varanasi (Kashi)", "subtitle": "Ganga River Basin Core, Uttar Pradesh", "category": "district", "category_label": "River Core", "lat": 25.3176, "lng": 82.9739, "keywords": ["varanasi", "banaras", "kashi"]},
    {"title": "Dehradun / Haridwar", "subtitle": "Himalayan Foothills Flash Flood Basin, Uttarakhand", "category": "district", "category_label": "Himalayan Basin", "lat": 30.3165, "lng": 78.0322, "keywords": ["dehradun", "haridwar", "rishikesh"]},
    {"title": "Srinagar Valley", "subtitle": "Jhelum River Basin Valley Core, Jammu & Kashmir", "category": "district", "category_label": "River Valley Core", "lat": 34.0837, "lng": 74.7973, "keywords": ["srinagar", "kashmir"]},

    # ==================== KEY CAMPUSES & MUNICIPAL SECTORS ====================
    {"title": "C. V. Raman Global University (CVRGU)", "subtitle": "Mahura, Janla, Bhubaneswar, Odisha 752054", "category": "university", "category_label": "University / Tech", "lat": 20.2198, "lng": 85.7358, "keywords": ["c.v raman", "cv raman", "cvrgu", "cvrce", "c.v. raman", "c.v raman global university", "cv raman university"]},
    {"title": "IIT Bhubaneswar", "subtitle": "Argul, Jatni, Khordha, Odisha 752050", "category": "university", "category_label": "National Institute", "lat": 20.1485, "lng": 85.6712, "keywords": ["iit", "iit bhubaneswar", "iit bbs", "argul"]},
    {"title": "AIIMS Bhubaneswar", "subtitle": "Sijua, Patrapada, Bhubaneswar, Odisha 751019", "category": "hospital", "category_label": "Apex Hospital / Medical", "lat": 20.2312, "lng": 85.7766, "keywords": ["aiims", "aiims bhubaneswar", "aiims hospital"]},
    {"title": "KIIT Deemed to be University", "subtitle": "Patia, Bhubaneswar, Odisha 751024", "category": "university", "category_label": "University Campus", "lat": 20.3533, "lng": 85.8189, "keywords": ["kiit", "kiit university", "patia"]},
    {"title": "SCB Medical College & Hospital", "subtitle": "Mangalabag, Cuttack, Odisha 753007", "category": "hospital", "category_label": "Apex Hospital", "lat": 20.4682, "lng": 85.8895, "keywords": ["scb", "scb medical", "scb hospital"]},
    {"title": "CDA Sector 9, Cuttack", "subtitle": "Bidanasi Colony, CDA Sector 9, Cuttack, Odisha 753014", "category": "suburb", "category_label": "Municipal Sector", "lat": 20.47937, "lng": 85.82872, "keywords": ["cda sector 9", "cda sec 9", "cda 9"]},
    {"title": "CDA Sector 6, Cuttack", "subtitle": "CDA Sector 6, Cuttack, Odisha 753014", "category": "suburb", "category_label": "Municipal Sector", "lat": 20.47658, "lng": 85.84028, "keywords": ["cda sector 6", "cda sec 6", "cda 6"]},
    {"title": "CDA Sector 10, Cuttack", "subtitle": "CDA Sector 10, Cuttack, Odisha 753014", "category": "suburb", "category_label": "Municipal Sector", "lat": 20.48354, "lng": 85.81933, "keywords": ["cda sector 10", "cda sec 10", "cda 10"]},
    {"title": "CDA Sector 11, Cuttack", "subtitle": "CDA Sector 11, Cuttack, Odisha 753014", "category": "suburb", "category_label": "Municipal Sector", "lat": 20.47979, "lng": 85.81866, "keywords": ["cda sector 11", "cda sec 11", "cda 11"]},
    {"title": "CDA Sector 7, Cuttack", "subtitle": "CDA Sector 7, Cuttack, Odisha 753014", "category": "suburb", "category_label": "Municipal Sector", "lat": 20.4820, "lng": 85.8360, "keywords": ["cda sector 7", "cda sec 7", "cda 7"]},
    {"title": "CDA Sector 8, Cuttack", "subtitle": "CDA Sector 8, Cuttack, Odisha 753014", "category": "suburb", "category_label": "Municipal Sector", "lat": 20.4860, "lng": 85.8320, "keywords": ["cda sector 8", "cda sec 8", "cda 8"]},
    {"title": "Bidanasi Embankment, Cuttack", "subtitle": "Bidanasi Old Village & Mahanadi Embankment Lowlands, Cuttack", "category": "suburb", "category_label": "River Embankment", "lat": 20.4710, "lng": 85.8230, "keywords": ["bidanasi", "bidanasi cuttack"]}
]

def clean_search_term(term: str) -> str:
    if not term:
        return ""
    t = term.lower().strip()
    t = re.sub(r'[^a-zA-Z0-9\s]', ' ', t)
    t = re.sub(r'(district|dist|headquarters|hq|block|tehsil|city|town)', '', t)
    t = re.sub(r'\s+', ' ', t).strip()
    t = t.replace('bhubaneshwar', 'bhubaneswar')
    t = t.replace('kataka', 'cuttack')
    t = t.replace('paradip', 'paradeep')
    t = t.replace('baleswar', 'balasore')
    return t

def search_local_gazetteer(query: str) -> List[Dict[str, Any]]:
    cq = clean_search_term(query)
    tokens = [tok for tok in cq.split() if len(tok) > 1]
    scored = []
    for item in PAN_INDIA_GAZETTEER:
        score = 0
        clean_title = clean_search_term(item["title"])
        for kw in item.get("keywords", []):
            ckw = clean_search_term(kw)
            if cq == ckw:
                score = 300
                break
            if ckw.startswith(cq) or cq.startswith(ckw):
                score = max(score, 220)
            elif cq in ckw:
                score = max(score, 180)
        if score == 0:
            if cq == clean_title or clean_title.startswith(cq):
                score = 250
            elif cq in clean_title:
                score = 160
            else:
                matched = sum(1 for t in tokens if t in clean_title)
                if matched > 0:
                    score = matched * 45
        if score > 0:
            scored.append((score, item))
    scored.sort(key=lambda x: -x[0])
    return [item for score, item in scored[:14]]

async def search_photon_osm_live(query: str) -> List[Dict[str, Any]]:
    cq = clean_search_term(query)
    url = f"https://photon.komoot.io/api/?q={httpx.URL('', params={'q': cq}).params['q']}&lat=20.5937&lon=78.9629&limit=8"
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
                    name = props.get("name") or props.get("city") or props.get("district") or props.get("state")
                    if not name:
                        continue
                    state = props.get("state") or ""
                    country = props.get("country") or ""
                    sub = f"{state}, {country}" if state and country else state or country
                    cat = "district" if props.get("type") in ("administrative", "district", "city") else "locality"
                    results.append({
                        "title": name,
                        "subtitle": f"{name}, {sub}" if sub else name,
                        "category": cat,
                        "category_label": "District / Locality",
                        "lat": round(float(coords[1]), 5),
                        "lng": round(float(coords[0]), 5),
                    })
    except Exception:
        pass
    return results

async def search_locations(query: str) -> List[Dict[str, Any]]:
    if not query or len(query.strip()) < 2:
        return []
    gazetteer_items = search_local_gazetteer(query)
    photon_items = await search_photon_osm_live(query)
    combined = []
    seen = set()
    for g in gazetteer_items:
        key = (round(g["lat"], 2), round(g["lng"], 2))
        if key not in seen:
            seen.add(key)
            combined.append(g)
    for p in photon_items:
        key = (round(p["lat"], 2), round(p["lng"], 2))
        if key not in seen:
            seen.add(key)
            combined.append(p)
    return combined[:15]
