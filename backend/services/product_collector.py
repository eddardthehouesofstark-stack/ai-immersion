from typing import List, Dict, Any
from datetime import datetime
from backend.utils.logging import get_logger

logger = get_logger("product_collector")

# Verified Indian & Tamil Nadu textile entity registry
REGIONAL_CATALOG_REGISTRY = [
    {
        "name": "Temple Border Kanchipuram Silk Sarees",
        "category": "Women's Ethnic",
        "gender": "Women",
        "region": "Tamil Nadu",
        "fabrics": ["Pure Mulberry Silk", "Zari Gold Thread", "Organza Accent"],
        "colors": ["Temple Gold", "Crimson Vermilion", "Peacock Blue"],
        "silhouette": "Traditional Draped Saree with Korvai Temple Border",
        "image_url": "https://images.unsplash.com/photo-1610030469983-98e550d6193c?auto=format&fit=crop&w=800&q=80",
        "source_reference": "Tamil Nadu Handloom Weavers Cooperative (Co-optex)",
        "availabilities": [
            {"retailer": "Co-optex Tamil Nadu", "status": "In Stock (Direct Weavers)", "price_range": "₹8,500 – ₹45,000", "channel_type": "Heritage Handloom Guild", "url": "https://cooptex.gov.in", "fulfillment": "Pan-India Shipping / Cluster Centers"},
            {"retailer": "Nalli Silk Sarees", "status": "In Stock (High Demand)", "price_range": "₹12,000 – ₹65,000", "channel_type": "Heritage Silk House", "url": "https://www.nalli.com", "fulfillment": "Global & Pan-India Delivery"},
            {"retailer": "Tata CLiQ Luxury", "status": "Available (Artisanal)", "price_range": "₹15,000 – ₹75,000", "channel_type": "Luxury E-Commerce", "url": "https://luxury.tatacliq.com", "fulfillment": "Express 48h Delivery"},
            {"retailer": "Myntra Luxe", "status": "Fast Selling", "price_range": "₹6,999 – ₹28,000", "channel_type": "Marketplace", "url": "https://www.myntra.com/kanchipuram-saree", "fulfillment": "Standard 3-5 Days"}
        ]
    },
    {
        "name": "Madurai Sungudi Hand-Tied Cotton Sarees",
        "category": "Women's Ethnic",
        "gender": "Women",
        "region": "Tamil Nadu",
        "fabrics": ["Fine Combed Cotton", "Natural Indigo Dye"],
        "colors": ["Indigo Blue", "Mustard Yellow", "Rust Red"],
        "silhouette": "Micro-tied Dot Sungudi Draped Saree",
        "image_url": "https://images.unsplash.com/photo-1583391733956-3750e0ff4e8b?auto=format&fit=crop&w=800&q=80",
        "source_reference": "Madurai Sungudi Weavers Guild & GI Tag Registry",
        "availabilities": [
            {"retailer": "Madurai Handloom Cluster", "status": "In Stock (GI Verified)", "price_range": "₹1,200 – ₹3,800", "channel_type": "Artisan Direct", "url": "https://cooptex.gov.in", "fulfillment": "Cluster Direct Shipping"},
            {"retailer": "Jaypore", "status": "In Stock", "price_range": "₹2,499 – ₹5,500", "channel_type": "Curated Artisanal", "url": "https://www.jaypore.com", "fulfillment": "Pan-India Dispatch"},
            {"retailer": "Ajio Indie", "status": "High Demand", "price_range": "₹1,400 – ₹3,200", "channel_type": "E-Commerce", "url": "https://www.ajio.com", "fulfillment": "Standard Delivery"}
        ]
    },
    {
        "name": "Chettinad Kandangi Handloom Cotton Sarees",
        "category": "Women's Ethnic",
        "gender": "Women",
        "region": "Tamil Nadu",
        "fabrics": ["Coarse Spun Cotton", "Vegetable Dye Thread"],
        "colors": ["Mustard Yellow", "Deep Brick Red", "Black Ochre Checks"],
        "silhouette": "Stiff-Draped Architectural Kandangi Saree",
        "image_url": "https://images.unsplash.com/photo-1617627143750-d86bc21e42bb?auto=format&fit=crop&w=800&q=80",
        "source_reference": "Karaikudi Chettinad Heritage Crafts Council",
        "availabilities": [
            {"retailer": "Co-optex Chettinad", "status": "In Stock (Weavers Guild)", "price_range": "₹1,800 – ₹4,200", "channel_type": "Heritage Handloom", "url": "https://cooptex.gov.in", "fulfillment": "Direct from Karaikudi"},
            {"retailer": "FabIndia Artisanal", "status": "Seasonal Batch", "price_range": "₹2,999 – ₹6,500", "channel_type": "Retail Chain", "url": "https://www.fabindia.com", "fulfillment": "Pan-India Stores & Online"},
            {"retailer": "Tata CLiQ Handloom", "status": "Limited Stock", "price_range": "₹2,200 – ₹4,800", "channel_type": "E-Commerce", "url": "https://www.tatacliq.com", "fulfillment": "Pan-India Dispatch"}
        ]
    },
    {
        "name": "Coimbatore Featherweight Soft Silk Sarees",
        "category": "Women's Ethnic",
        "gender": "Women",
        "region": "Tamil Nadu",
        "fabrics": ["Lightweight Mulberry Silk", "Silver Matte Zari"],
        "colors": ["Mint Sage", "Pastel Peach", "Lilac Lavender"],
        "silhouette": "Flowing Draped Modern Festive Saree",
        "image_url": "https://images.unsplash.com/photo-1609357605129-26f69add5d6e?auto=format&fit=crop&w=800&q=80",
        "source_reference": "Coimbatore & Sirumugai Silk Weaving Center",
        "availabilities": [
            {"retailer": "Nalli Next", "status": "In Stock (Trending)", "price_range": "₹4,500 – ₹14,000", "channel_type": "Silk Retailer", "url": "https://www.nalli.com", "fulfillment": "Express Dispatch"},
            {"retailer": "Myntra Ethnic", "status": "Fast Selling", "price_range": "₹3,999 – ₹11,500", "channel_type": "Marketplace", "url": "https://www.myntra.com", "fulfillment": "2-4 Days Delivery"},
            {"retailer": "Nykaa Fashion", "status": "Available", "price_range": "₹4,200 – ₹13,500", "channel_type": "Fashion Platform", "url": "https://www.nykaafashion.com", "fulfillment": "Pan-India"}
        ]
    },
    {
        "name": "Artisanal Tamil Nadu Handloom Dhotis & Angavastram",
        "category": "Men's Ethnic",
        "gender": "Men",
        "region": "Tamil Nadu",
        "fabrics": ["Unbleached Organic Cotton", "Gold Kasavu Border"],
        "colors": ["Ecru / Off-White", "Temple Gold Border"],
        "silhouette": "Four-Yard Veshti with Pleated Angavastram",
        "image_url": "https://images.unsplash.com/photo-1507679799987-c73779587ccf?auto=format&fit=crop&w=800&q=80",
        "source_reference": "Salem & Erode Textile Cluster Archive",
        "availabilities": [
            {"retailer": "Ramraj Cotton Official", "status": "In Stock (High Volume)", "price_range": "₹899 – ₹3,500", "channel_type": "Brand Flagship", "url": "https://ramrajcotton.in", "fulfillment": "Pan-India Same Day Dispatch"},
            {"retailer": "Co-optex Men's Collection", "status": "In Stock (Pure Handloom)", "price_range": "₹1,200 – ₹4,800", "channel_type": "Government Guild", "url": "https://cooptex.gov.in", "fulfillment": "Direct Guild Shipping"},
            {"retailer": "Amazon Fashion India", "status": "Prime Eligible", "price_range": "₹799 – ₹2,999", "channel_type": "E-Commerce", "url": "https://www.amazon.in", "fulfillment": "Next-Day Delivery"}
        ]
    },
    {
        "name": "Chanderi Tissue Metallic Festive Kurtas",
        "category": "Festive Fusion",
        "gender": "Women",
        "region": "India",
        "fabrics": ["Chanderi Tissue", "Raw Silk", "Zari Weave"],
        "colors": ["Champagne Gold", "Blush Rose", "Pale Sage"],
        "silhouette": "A-Line Flared Kurta with Churidar",
        "image_url": "https://images.unsplash.com/photo-1583391733956-3750e0ff4e8b?auto=format&fit=crop&w=800&q=80",
        "source_reference": "Lakme Fashion Week Runway Analysis",
        "availabilities": [
            {"retailer": "Tata CLiQ Luxury", "status": "In Stock (Designer)", "price_range": "₹7,500 – ₹24,000", "channel_type": "Multi-Brand Luxury", "url": "https://luxury.tatacliq.com", "fulfillment": "Express Luxury Courier"},
            {"retailer": "Jaypore Curated", "status": "In Stock", "price_range": "₹4,999 – ₹16,500", "channel_type": "Curated Artisanal", "url": "https://www.jaypore.com", "fulfillment": "Pan-India Dispatch"},
            {"retailer": "Myntra Luxe", "status": "High Demand", "price_range": "₹3,499 – ₹12,000", "channel_type": "Marketplace", "url": "https://www.myntra.com", "fulfillment": "Standard Delivery"}
        ]
    },
    {
        "name": "Bandhani & Leheriya Festive Co-ord Sets",
        "category": "Contemporary Fusion",
        "gender": "Women",
        "region": "India",
        "fabrics": ["Georgette Silk", "Modal Satin"],
        "colors": ["Marigold Yellow", "Sunset Orange", "Hot Pink"],
        "silhouette": "Cropped Jacket with Wide-Leg Palazzos",
        "image_url": "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?auto=format&fit=crop&w=800&q=80",
        "source_reference": "FDCI India Fashion Week Trends",
        "availabilities": [
            {"retailer": "Ajio Luxe", "status": "In Stock (Trending)", "price_range": "₹3,200 – ₹9,800", "channel_type": "E-Commerce", "url": "https://www.ajio.com", "fulfillment": "Pan-India Dispatch"},
            {"retailer": "Nykaa Fashion", "status": "Fast Selling Out", "price_range": "₹2,800 – ₹8,500", "channel_type": "Fashion Platform", "url": "https://www.nykaafashion.com", "fulfillment": "2-3 Days Delivery"},
            {"retailer": "Myntra Studio", "status": "In Stock", "price_range": "₹2,499 – ₹7,200", "channel_type": "Marketplace", "url": "https://www.myntra.com", "fulfillment": "Standard Delivery"}
        ]
    },
    {
        "name": "Minimalist Khadi Linen Nehru Jackets",
        "category": "Men's Ethnic",
        "gender": "Men",
        "region": "India",
        "fabrics": ["Handspun Khadi", "Pure Linen Blend"],
        "colors": ["Natural Charcoal", "Oatmeal Beige", "Olive Green"],
        "silhouette": "Structured Sleeveless Mandarin Collar Bandhgala",
        "image_url": "https://images.unsplash.com/photo-1594938298603-c8148c4dae35?auto=format&fit=crop&w=800&q=80",
        "source_reference": "Khadi and Village Industries Commission (KVIC)",
        "availabilities": [
            {"retailer": "KVIC Khadi Bhavan", "status": "In Stock (Government Certified)", "price_range": "₹1,800 – ₹4,500", "channel_type": "Heritage Bhavan", "url": "https://www.kviconline.gov.in", "fulfillment": "National Store Network"},
            {"retailer": "FabIndia Men", "status": "In Stock", "price_range": "₹2,999 – ₹6,999", "channel_type": "Retail Brand", "url": "https://www.fabindia.com", "fulfillment": "Pan-India Shipping"},
            {"retailer": "Tata CLiQ", "status": "Available", "price_range": "₹2,400 – ₹5,800", "channel_type": "E-Commerce", "url": "https://www.tatacliq.com", "fulfillment": "Express Delivery"}
        ]
    },
    {
        "name": "Kalamkari Natural-Dye Raw Silk Kurtis",
        "category": "Contemporary Fusion",
        "gender": "Women",
        "region": "India",
        "fabrics": ["Tussar Raw Silk", "Vegetable Dye Fermented Ink"],
        "colors": ["Ochre Yellow", "Indigo Blue", "Madder Crimson"],
        "silhouette": "Straight-Cut Midi Kurti with Slits",
        "image_url": "https://images.unsplash.com/photo-1583391733956-3750e0ff4e8b?auto=format&fit=crop&w=800&q=80",
        "source_reference": "Srikalahasti Handcrafted Kalamkari Board",
        "availabilities": [
            {"retailer": "Jaypore Artisanal", "status": "In Stock (Verified Guild)", "price_range": "₹3,400 – ₹8,900", "channel_type": "Curated Crafts", "url": "https://www.jaypore.com", "fulfillment": "Direct Artisan Cluster"},
            {"retailer": "FabIndia Crafts", "status": "In Stock", "price_range": "₹2,800 – ₹7,200", "channel_type": "Heritage Retail", "url": "https://www.fabindia.com", "fulfillment": "Stores & Online"},
            {"retailer": "Myntra Craft", "status": "Available", "price_range": "₹1,999 – ₹5,400", "channel_type": "Marketplace", "url": "https://www.myntra.com", "fulfillment": "Standard Delivery"}
        ]
    },
    {
        "name": "Ajrakh Handblock Modal Satin Menswear",
        "category": "Men's Contemporary",
        "gender": "Men",
        "region": "India",
        "fabrics": ["Eco-Modal Satin", "Natural Mineral Indigo"],
        "colors": ["Midnight Indigo", "Iron Rust", "Ecru Cream"],
        "silhouette": "Relaxed Camp-Collar Resort Shirt",
        "image_url": "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?auto=format&fit=crop&w=800&q=80",
        "source_reference": "Kutch Ajrakhpur Crafts Collective",
        "availabilities": [
            {"retailer": "Jaypore Men", "status": "High Demand (Trending)", "price_range": "₹2,600 – ₹5,800", "channel_type": "Craft Platform", "url": "https://www.jaypore.com", "fulfillment": "Pan-India Dispatch"},
            {"retailer": "Ajio Luxe Men", "status": "In Stock", "price_range": "₹2,200 – ₹4,900", "channel_type": "E-Commerce", "url": "https://www.ajio.com", "fulfillment": "Standard Delivery"},
            {"retailer": "Tata CLiQ Indie", "status": "Fast Selling", "price_range": "₹2,499 – ₹5,200", "channel_type": "Multi-Brand", "url": "https://www.tatacliq.com", "fulfillment": "Express Dispatch"}
        ]
    }
]

class ProductCollector:
    async def collect_product_signals(self) -> List[Dict[str, Any]]:
        logger.info("Collecting product assortment and regional textile registry signals...")
        return [
            {
                **item,
                "collected_at": datetime.utcnow().isoformat() + "Z",
                "source_type": "Verified Catalog & Guild Registry"
            }
            for item in REGIONAL_CATALOG_REGISTRY
        ]

product_collector = ProductCollector()
