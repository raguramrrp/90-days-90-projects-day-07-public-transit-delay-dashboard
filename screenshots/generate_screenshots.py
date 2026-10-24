"""Generates authentic visual screenshot assets for documentation and portfolio presentation.
Reflects the Tirunelveli Public Transport Intelligence Platform (Nellai Transit).
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from PIL import Image, ImageDraw
from config import SCREENSHOTS_DIR


def create_header(draw, title, subtitle, width, height=90, badge_text="📍 Tirunelveli District • TNSTC & Southern Railway • 10 Routes • 20 Stations"):
    """Draws top dark executive header banner."""
    draw.rectangle([(0, 0), (width, height)], fill="#0F172A")
    # Accent top border (Tamil Nadu gold / transit amber)
    draw.rectangle([(0, 0), (width, 4)], fill="#F59E0B")
    draw.text((30, 20), title, fill="#FFFFFF", font_size=23)
    draw.text((30, 52), subtitle, fill="#94A3B8", font_size=13)
    # Status pill
    badge_w = 460
    draw.rounded_rectangle([(width - badge_w - 25, 28), (width - 25, 62)], radius=16, fill="#1E293B", outline="#334155")
    draw.text((width - badge_w - 12, 36), badge_text, fill="#E2E8F0", font_size=11)


def generate_overview_screenshot():
    """Generates Command Center overview screenshot preview."""
    w, h = 1200, 750
    img = Image.new("RGB", (w, h), color="#F8FAFC")
    draw = ImageDraw.Draw(img)

    create_header(draw, "🏛️ Tirunelveli Public Transport Intelligence Platform", "Command Center • Nellai Multimodal Operations (TNSTC Nellai • Southern Railway • SETC)", w)

    # 5 Top KPI Cards
    card_w = 210
    card_h = 110
    start_x = 35
    gap = 22
    y_card = 115

    kpis = [
        ("TOTAL TRIPS MONITORED", "2,220", "14,640 Station Arrivals", "#0F172A"),
        ("ON-TIME ARRIVAL RATE", "82.4%", "≤ 2.0 mins or Early (SLA)", "#10B981"),
        ("AVERAGE DELAY", "2.85 min", "Fleet Variance from Sched", "#3B82F6"),
        ("CHRONIC BOTTLENECKS", "6 Hubs", "Jct, New Bus Stand, etc.", "#EF4444"),
        ("TRANSIT RELIABILITY (TRI)", "84.2/100", "Tier 2: Optimal Reliability", "#10B981")
    ]

    for i, (label, val, sub, color) in enumerate(kpis):
        x = start_x + i * (card_w + gap)
        draw.rounded_rectangle([(x, y_card), (x + card_w, y_card + card_h)], radius=10, fill="#FFFFFF", outline="#E2E8F0", width=1)
        draw.rounded_rectangle([(x, y_card), (x + card_w, y_card + 4)], radius=2, fill=color)
        draw.text((x + 14, y_card + 14), label, fill="#64748B", font_size=11)
        draw.text((x + 14, y_card + 36), val, fill=color, font_size=26)
        draw.text((x + 14, y_card + 78), sub, fill="#475569", font_size=11)

    # Chart 1: 30-Day Delay Trend
    y_chart1 = 250
    w_chart1 = 700
    h_chart1 = 260
    draw.rounded_rectangle([(start_x, y_chart1), (start_x + w_chart1, y_chart1 + h_chart1)], radius=10, fill="#FFFFFF", outline="#E2E8F0", width=1)
    draw.text((start_x + 20, y_chart1 + 16), "📈 30-Day Nellai Delay Trend & 7-Day Rolling Moving Average", fill="#0F172A", font_size=15)
    draw.line([(start_x + 20, y_chart1 + 45), (start_x + w_chart1 - 20, y_chart1 + 45)], fill="#F1F5F9", width=1)

    bar_y_base = y_chart1 + h_chart1 - 40
    import random
    random.seed(42)
    daily_delays = [random.uniform(2.0, 4.1) for _ in range(28)]
    pts = []
    for idx, d in enumerate(daily_delays):
        bx = start_x + 40 + idx * 22
        b_height = int(d * 30)
        draw.rectangle([(bx, bar_y_base - b_height), (bx + 14, bar_y_base)], fill="#CBD5E1")
        pts.append((bx + 7, bar_y_base - int(sum(daily_delays[max(0, idx-3):idx+1]) / len(daily_delays[max(0, idx-3):idx+1]) * 30)))

    for j in range(len(pts) - 1):
        draw.line([pts[j], pts[j+1]], fill="#2563EB", width=3)

    sla_y = bar_y_base - int(3.0 * 30)
    draw.line([(start_x + 40, sla_y), (start_x + w_chart1 - 30, sla_y)], fill="#10B981", width=2)
    draw.text((start_x + w_chart1 - 160, sla_y - 18), "Target SLA (3.0m)", fill="#10B981", font_size=11)

    # Chart 2: Modal Breakdown Card
    x_chart2 = start_x + w_chart1 + 25
    w_chart2 = 410
    draw.rounded_rectangle([(x_chart2, y_chart1), (x_chart2 + w_chart2, y_chart1 + h_chart1)], radius=10, fill="#FFFFFF", outline="#E2E8F0", width=1)
    draw.text((x_chart2 + 20, y_chart1 + 16), "🚏 Nellai Transport Mode Share", fill="#0F172A", font_size=15)
    draw.line([(x_chart2 + 20, y_chart1 + 45), (x_chart2 + w_chart2 - 20, y_chart1 + 45)], fill="#F1F5F9", width=1)

    cat_items = [
        ("🚌 TNSTC Nellai City Buses (6 Routes)", "60% Trips • Avg Delay: 3.4m", "#D97706"),
        ("🚆 Southern Railway Trains (TEN Express)", "30% Trips • Avg Delay: 1.8m", "#DC2626"),
        ("🚍 SETC Long Distance Express Buses", "10% Trips • Avg Delay: 2.9m", "#2563EB"),
        ("🟢 Live Fleet Telemetry Engine", "Active Vehicle GPS Tracking", "#10B981"),
        ("📡 Open Transport Catalog", "Tirunelveli Master Feeds Active", "#64748B")
    ]
    for idx, (cat_name, pct, col) in enumerate(cat_items):
        cy = y_chart1 + 65 + idx * 36
        draw.rounded_rectangle([(x_chart2 + 25, cy + 4), (x_chart2 + 40, cy + 19)], radius=3, fill=col)
        draw.text((x_chart2 + 50, cy + 2), cat_name, fill="#334155", font_size=13)
        draw.text((x_chart2 + 50, cy + 18), pct, fill="#64748B", font_size=10)

    # Row 3: Operator Comparison Summary
    y_chart3 = 530
    h_chart3 = 190
    draw.rounded_rectangle([(start_x, y_chart3), (w - start_x, y_chart3 + h_chart3)], radius=10, fill="#FFFFFF", outline="#E2E8F0", width=1)
    draw.text((start_x + 20, y_chart3 + 14), "⚖️ Operator Performance & SLA Scorecard", fill="#0F172A", font_size=15)

    headers = [("Operator", 300), ("Mode", 160), ("Trips", 110), ("Avg Delay", 120), ("On-Time SLA", 130), ("TRI Index", 120), ("Status", 150)]
    hx = start_x + 25
    for hname, hw in headers:
        draw.text((hx, y_chart3 + 45), hname, fill="#64748B", font_size=11)
        hx += hw

    op_rows = [
        ("TNSTC Tirunelveli City Division", "City Bus", "1,332", "3.42 mins", "78.2%", "80.5 / 100", "Moderate (Amber)"),
        ("Southern Railway (Nellai Hub)", "Express / Passenger", "666", "1.85 mins", "91.4%", "92.6 / 100", "Excellent (Green)"),
        ("State Express Transport Corp (SETC)", "Intercity Bus", "222", "2.90 mins", "84.0%", "85.2 / 100", "High (Green)")
    ]
    for idx, rdata in enumerate(op_rows):
        ry = y_chart3 + 75 + idx * 34
        draw.line([(start_x + 20, ry - 4), (w - start_x - 20, ry - 4)], fill="#F1F5F9", width=1)
        rx = start_x + 25
        for cidx, (val, col_w) in enumerate(zip(rdata, [300, 160, 110, 120, 130, 120, 150])):
            t_col = "#2563EB" if cidx == 0 else ("#10B981" if "Green" in val or "91" in val or "85" in val else "#1E293B")
            draw.text((rx, ry), str(val), fill=t_col, font_size=12)
            rx += col_w

    out_file = SCREENSHOTS_DIR / "dashboard_overview.png"
    img.save(out_file)
    print("Generated:", out_file)


def generate_map_screenshot():
    """Generates Live Tracking Map screenshot preview."""
    w, h = 1200, 750
    img = Image.new("RGB", (w, h), color="#F8FAFC")
    draw = ImageDraw.Draw(img)

    create_header(draw, "🛰️ Live Fleet Tracker & ETAs • Tirunelveli Transit Network", "Real-Time Bus & Train Telemetry • Stop-by-Stop Expected Arrivals & Delays", w)

    start_x = 35
    y_banner = 105
    w_box = w - 2 * start_x

    # Live fleet telemetry status bar
    draw.rounded_rectangle([(start_x, y_banner), (start_x + w_box, y_banner + 38)], radius=8, fill="#ECFDF5", outline="#10B981", width=1)
    draw.text((start_x + 18, y_banner + 11), "🟢 LIVE FLEET TELEMETRY ACTIVE — Active TNSTC Buses & Southern Railway Trains across Tirunelveli Hub • Satellite Fix: 3D GPS", fill="#065F46", font_size=11)

    # Search & Filter Toolbar with Bus Name & Train Number Search
    y_tool = 155
    draw.rounded_rectangle([(start_x, y_tool), (start_x + w_box, y_tool + 46)], radius=8, fill="#FFFFFF", outline="#E2E8F0", width=1)
    draw.text((start_x + 20, y_tool + 15), "🔍 Track Vehicle: [Bus TN-72-N-1042 (TNSTC Route 1) ▼]   [Mode: All Modes ▼]   [Route: All Corridors ▼]   [Status: En-Route]", fill="#334155", font_size=12)
    # Action button
    draw.rounded_rectangle([(start_x + w_box - 170, y_tool + 8), (start_x + w_box - 15, y_tool + 38)], radius=6, fill="#2563EB")
    draw.text((start_x + w_box - 158, y_tool + 15), "⚡ Refresh Live GPS", fill="#FFFFFF", font_size=12)

    # Interactive Map Viewport Mock
    y_map = 215
    h_map = 500
    draw.rounded_rectangle([(start_x, y_map), (start_x + w_box, y_map + h_map)], radius=10, fill="#E2E8F0", outline="#CBD5E1", width=1)

    # Thamirabarani River winding through Tirunelveli
    draw.line([(start_x + 320, y_map + 480), (start_x + 460, y_map + 310), (start_x + 580, y_map + 220), (start_x + 750, y_map + 150), (start_x + 950, y_map + 120)], fill="#93C5FD", width=14)
    draw.text((start_x + 600, y_map + 175), "🌊 Thamirabarani River", fill="#1D4ED8", font_size=12)

    # Tirunelveli Transit Polylines
    # Main Southern Railway Mainline (TEN - Madurai / Chennai)
    draw.line([(start_x + 530, y_map + 460), (start_x + 530, y_map + 240), (start_x + 530, y_map + 50)], fill="#DC2626", width=5)
    # Tirunelveli - Tenkasi Line (via Cheranmahadevi, Ambasamudram)
    draw.line([(start_x + 530, y_map + 240), (start_x + 340, y_map + 280), (start_x + 200, y_map + 310), (start_x + 100, y_map + 220)], fill="#EA580C", width=4)
    # Tirunelveli - Tiruchendur Line
    draw.line([(start_x + 530, y_map + 240), (start_x + 680, y_map + 320), (start_x + 880, y_map + 430)], fill="#16A34A", width=4)
    # City Bus Corridor (New Bus Stand <-> Junction <-> Palayamkottai)
    draw.line([(start_x + 380, y_map + 180), (start_x + 530, y_map + 240), (start_x + 660, y_map + 260)], fill="#D97706", width=4)

    # Stations Circles
    map_stations = [
        (start_x + 530, y_map + 240, "Tirunelveli Junction (TEN)", "#DC2626"),
        (start_x + 380, y_map + 180, "New Bus Stand (Veinthaankulam)", "#D97706"),
        (start_x + 460, y_map + 215, "Town Nellaiyappar Temple", "#D97706"),
        (start_x + 505, y_map + 210, "Vannarpettai Roundabout", "#D97706"),
        (start_x + 660, y_map + 260, "Palayamkottai Market", "#D97706"),
        (start_x + 610, y_map + 340, "Medical College High Ground", "#D97706"),
        (start_x + 340, y_map + 280, "Cheranmahadevi Station", "#EA580C"),
        (start_x + 200, y_map + 310, "Ambasamudram (ASD)", "#EA580C"),
        (start_x + 100, y_map + 220, "Tenkasi Junction (TSI)", "#EA580C"),
        (start_x + 680, y_map + 320, "Srivaikuntam (SVT)", "#16A34A"),
        (start_x + 880, y_map + 430, "Tiruchendur Terminal (TCN)", "#16A34A")
    ]
    for sx, sy, sname, scol in map_stations:
        draw.ellipse([(sx - 7, sy - 7), (sx + 7, sy + 7)], fill="#FFFFFF", outline=scol, width=3)
        draw.text((sx + 10, sy - 6), sname, fill="#1E293B", font_size=10)

    # Vehicle Markers with authentic Bus Plate Numbers & Train Numbers
    vehicles = [
        (start_x + 450, y_map + 200, "🚌 Bus TN-72-N-1042", "26 km/h • ON-TIME", "#D97706"),
        (start_x + 530, y_map + 150, "🚆 12632 Nellai Superfast", "58 km/h • ON-TIME", "#DC2626"),
        (start_x + 600, y_map + 250, "🚌 Bus TN-72-N-3011", "24 km/h • +2m DELAY", "#D97706"),
        (start_x + 260, y_map + 300, "🚌 Bus TN-72-N-4105", "36 km/h • +3m DELAY", "#D97706"),
        (start_x + 780, y_map + 375, "🚆 06682 Tiruchendur Spl", "44 km/h • ON-TIME", "#16A34A")
    ]
    for vx, vy, vlabel, vsub, vcol in vehicles:
        draw.rounded_rectangle([(vx - 6, vy - 6), (vx + 6, vy + 6)], radius=4, fill=vcol, outline="#FFFFFF", width=2)
        # Detailed ETA Card Popup for 12632 Nellai Superfast
        if "12632" in vlabel:
            draw.rounded_rectangle([(vx + 15, vy - 35), (vx + 275, vy + 40)], radius=8, fill="#0F172A", outline="#DC2626")
            draw.text((vx + 23, vy - 30), "🚆 Southern Railway • 12632 Nellai Superfast", fill="#F87171", font_size=11)
            draw.text((vx + 23, vy - 14), "Approaching: Tirunelveli Junction (Platform 1)", fill="#F8FAFC", font_size=10)
            draw.text((vx + 23, vy + 2), "ETA: 19:45 (in 4 mins) • Speed: 58 km/h", fill="#10B981", font_size=10)
            draw.text((vx + 23, vy + 18), "Status: ON-TIME (0.0m variance)", fill="#E2E8F0", font_size=9)
        else:
            draw.text((vx + 10, vy - 8), vlabel, fill=vcol, font_size=10)

    # Legend box
    draw.rounded_rectangle([(start_x + 20, y_map + h_map - 110), (start_x + 310, y_map + h_map - 20)], radius=8, fill="#FFFFFF", outline="#CBD5E1")
    draw.text((start_x + 30, y_map + h_map - 100), "🗺️ Nellai Multimodal Legend", fill="#0F172A", font_size=11)
    draw.text((start_x + 30, y_map + h_map - 80), "━━ TNSTC City Bus Routes (#D97706)", fill="#D97706", font_size=10)
    draw.text((start_x + 30, y_map + h_map - 64), "━━ SR Mainline / Express (#DC2626)", fill="#DC2626", font_size=10)
    draw.text((start_x + 30, y_map + h_map - 48), "━━ Tiruchendur & Tenkasi Lines (#16A34A)", fill="#16A34A", font_size=10)
    draw.text((start_x + 30, y_map + h_map - 32), "● Station / Terminal  |  ■ Active Vehicle", fill="#475569", font_size=10)

    out_file = SCREENSHOTS_DIR / "live_tracking_map.png"
    img.save(out_file)
    print("Generated:", out_file)


def generate_route_screenshot():
    """Generates Route Analysis screenshot preview."""
    w, h = 1200, 750
    img = Image.new("RGB", (w, h), color="#F8FAFC")
    draw = ImageDraw.Draw(img)

    create_header(draw, "🚏 Tirunelveli Transit Route Performance & Reliability", "Nellai Transit Platform • Route Rankings & Stop Cascades", w)

    # Route Table Card
    start_x = 35
    y_card = 115
    w_table = 720
    h_table = 380

    draw.rounded_rectangle([(start_x, y_card), (start_x + w_table, y_card + h_table)], radius=10, fill="#FFFFFF", outline="#E2E8F0", width=1)
    draw.text((start_x + 20, y_card + 16), "🚆 Tirunelveli Bus & Train Performance Rankings", fill="#0F172A", font_size=16)
    draw.line([(start_x + 20, y_card + 48), (start_x + w_table - 20, y_card + 48)], fill="#E2E8F0", width=1)

    headers = [("Rank", 30), ("Route / Service", 200), ("Mode", 80), ("Stops", 60), ("Avg Delay", 75), ("On-Time %", 85), ("TRI Score", 80)]
    hx = start_x + 20
    for hname, hw in headers:
        draw.text((hx, y_card + 56), hname, fill="#64748B", font_size=12)
        hx += hw

    route_rows = [
        ("1", "20666 Vande Bharat Express", "Train", "4", "0.65m", "96.4%", "97.1", "#10B981"),
        ("2", "12632 Nellai Superfast Express", "Train", "6", "1.20m", "93.8%", "94.5", "#10B981"),
        ("3", "06682 Tiruchendur Special", "Train", "5", "1.85m", "89.2%", "90.4", "#10B981"),
        ("4", "TNSTC Route 1 (VBS - TEN Jct)", "Bus", "5", "2.60m", "82.5%", "84.0", "#3B82F6"),
        ("5", "TNSTC Route 3 (TEN Jct - PLM)", "Bus", "5", "3.10m", "79.0%", "80.2", "#F59E0B"),
        ("6", "TNSTC Route 10 (Town - MED)", "Bus", "5", "3.45m", "77.1%", "78.0", "#F59E0B"),
        ("7", "TNSTC Route 41 (Jct - Ambasamudram)", "Bus", "6", "4.15m", "72.4%", "73.8", "#EF4444")
    ]

    for idx, rdata in enumerate(route_rows):
        ry = y_card + 90 + idx * 40
        draw.line([(start_x + 20, ry - 6), (start_x + w_table - 20, ry - 6)], fill="#F1F5F9", width=1)
        rx = start_x + 20
        for cidx, (val, col_w) in enumerate(zip(rdata[:7], [30, 200, 80, 60, 75, 85, 80])):
            text_col = rdata[7] if cidx == 6 else "#1E293B"
            draw.text((rx, ry + 4), str(val), fill=text_col, font_size=12)
            rx += col_w

    # Side chart: TRI comparison
    x_chart2 = start_x + w_table + 25
    w_chart2 = 390
    draw.rounded_rectangle([(x_chart2, y_card), (x_chart2 + w_chart2, y_card + h_table)], radius=10, fill="#FFFFFF", outline="#E2E8F0", width=1)
    draw.text((x_chart2 + 20, y_card + 16), "📊 Transit Reliability Index (TRI)", fill="#0F172A", font_size=15)
    draw.line([(x_chart2 + 20, y_card + 48), (x_chart2 + w_chart2 - 20, y_card + 48)], fill="#E2E8F0", width=1)

    for idx, (rn, rname, rtype, stops, avg_d, ot, tri_v, col) in enumerate(route_rows):
        cy = y_card + 75 + idx * 42
        short_n = rname.split("(")[0].strip()
        draw.text((x_chart2 + 20, cy), short_n[:20], fill="#334155", font_size=11)
        score_val = float(tri_v)
        b_len = int(score_val * 1.8)
        draw.rounded_rectangle([(x_chart2 + 155, cy + 2), (x_chart2 + 155 + b_len, cy + 18)], radius=4, fill=col)
        draw.text((x_chart2 + 165 + b_len, cy), f"{tri_v}", fill="#475569", font_size=11)

    # Bottom Cascade Chart
    y_casc = 520
    h_casc = 200
    draw.rounded_rectangle([(start_x, y_casc), (w - start_x, y_casc + h_casc)], radius=10, fill="#FFFFFF", outline="#E2E8F0", width=1)
    draw.text((start_x + 20, y_casc + 14), "🌊 Stop-by-Stop Delay Cascading Profile (TNSTC Route 41: Tirunelveli Jct <-> Ambasamudram)", fill="#0F172A", font_size=15)

    stops = [
        ("Tirunelveli Jct", 0.4),
        ("Nellaiyappar Town", 1.2),
        ("Pettai Market", 2.1),
        ("Cheranmahadevi", 3.0),
        ("Kallidaikurichi", 3.6),
        ("Ambasamudram", 4.2)
    ]
    base_cx = start_x + 85
    base_cy = y_casc + h_casc - 45
    pts = []
    for sidx, (stn, del_val) in enumerate(stops):
        sx = base_cx + sidx * 180
        sy = base_cy - int(del_val * 28)
        pts.append((sx, sy))
        draw.ellipse([(sx - 6, sy - 6), (sx + 6, sy + 6)], fill="#EA580C", outline="#FFFFFF", width=2)
        draw.text((sx - 15, sy - 24), f"{del_val:.1f}m", fill="#EA580C", font_size=12)
        draw.text((sx - 35, base_cy + 12), stn.split(" ")[0], fill="#475569", font_size=11)

    for i in range(len(pts) - 1):
        draw.line([pts[i], pts[i+1]], fill="#EA580C", width=3)

    out_file = SCREENSHOTS_DIR / "route_analysis.png"
    img.save(out_file)
    print("Generated:", out_file)


def generate_station_screenshot():
    """Generates Station Bottlenecks screenshot preview."""
    w, h = 1200, 750
    img = Image.new("RGB", (w, h), color="#F8FAFC")
    draw = ImageDraw.Draw(img)

    create_header(draw, "📍 Station Hotspots & Congestion Bottlenecks", "Tirunelveli Transit Platform • Hub Delays & Dwell Times", w)

    start_x = 35
    y_top = 115
    w_col = 550
    h_box = 400

    # Box 1: Geographic Map Bubble Representation
    draw.rounded_rectangle([(start_x, y_top), (start_x + w_col, y_top + h_box)], radius=10, fill="#FFFFFF", outline="#E2E8F0", width=1)
    draw.text((start_x + 20, y_top + 16), "🗺️ Nellai Station Delay Hotspots (Bubble = Delay)", fill="#0F172A", font_size=15)
    draw.line([(start_x + 20, y_top + 48), (start_x + w_col - 20, y_top + 48)], fill="#E2E8F0", width=1)

    map_x = start_x + 30
    map_y = y_top + 70
    map_w = w_col - 60
    map_h = h_box - 90
    draw.rounded_rectangle([(map_x, map_y), (map_x + map_w, map_y + map_h)], radius=8, fill="#F8FAFC", outline="#CBD5E1")

    stations = [
        (map_x + 250, map_y + 110, 24, "#EF4444", "Tirunelveli Jct (4.35m)"),
        (map_x + 150, map_y + 80, 22, "#EF4444", "New Bus Stand (4.10m)"),
        (map_x + 200, map_y + 160, 20, "#EA580C", "Town Temple (3.85m)"),
        (map_x + 320, map_y + 180, 19, "#EA580C", "Palayamkottai (3.60m)"),
        (map_x + 230, map_y + 220, 17, "#F59E0B", "Vannarpettai (3.25m)"),
        (map_x + 80, map_y + 260, 15, "#F59E0B", "Tenkasi Jct (2.95m)"),
        (map_x + 130, map_y + 290, 14, "#10B981", "Ambasamudram (2.70m)")
    ]
    for bx, by, br, bcol, bname in stations:
        draw.ellipse([(bx - br, by - br), (bx + br, by + br)], fill=bcol, outline="#FFFFFF", width=2)
        draw.text((bx - 20, by + br + 4), bname.split(" ")[0], fill="#334155", font_size=11)

    # Box 2: Top Bottleneck Ranking Bar Chart
    x_col2 = start_x + w_col + 30
    draw.rounded_rectangle([(x_col2, y_top), (x_col2 + w_col, y_top + h_box)], radius=10, fill="#FFFFFF", outline="#E2E8F0", width=1)
    draw.text((x_col2 + 20, y_top + 16), "🏆 Top 7 Bottleneck Stations in Tirunelveli", fill="#0F172A", font_size=15)
    draw.line([(x_col2 + 20, y_top + 48), (x_col2 + w_col - 20, y_top + 48)], fill="#E2E8F0", width=1)

    bottlenecks = [
        ("Tirunelveli Junction (TEN)", "4.35 min", 255, "#DC2626"),
        ("New Bus Stand Veinthaankulam (VBS)", "4.10 min", 235, "#DC2626"),
        ("Town Nellaiyappar Temple (TOWN)", "3.85 min", 215, "#EA580C"),
        ("Palayamkottai Market (PLM)", "3.60 min", 195, "#EA580C"),
        ("Vannarpettai Roundabout (VNR)", "3.25 min", 175, "#F59E0B"),
        ("Tenkasi Junction (TSI)", "2.95 min", 155, "#F59E0B"),
        ("Ambasamudram Bus Stand (ASD)", "2.70 min", 140, "#10B981")
    ]
    for idx, (st_name, avg_d, bar_w, col) in enumerate(bottlenecks):
        by = y_top + 70 + idx * 44
        draw.text((x_col2 + 20, by), st_name, fill="#1E293B", font_size=12)
        draw.rounded_rectangle([(x_col2 + 245, by + 2), (x_col2 + 245 + bar_w, by + 18)], radius=4, fill=col)
        draw.text((x_col2 + 255 + bar_w, by), avg_d, fill="#64748B", font_size=11)

    # Bottom Table: Bottleneck Details
    y_bot = 540
    h_bot = 180
    draw.rounded_rectangle([(start_x, y_bot), (w - start_x, y_bot + h_bot)], radius=10, fill="#FFFFFF", outline="#E2E8F0", width=1)
    draw.text((start_x + 20, y_bot + 14), "📋 Station Transit Connectivity & Delay Severity", fill="#0F172A", font_size=15)

    headers = [("Rank", 50), ("Station Name", 230), ("Zone", 140), ("Interchange Modes", 170), ("Avg Delay", 90), ("Peak Delay", 90), ("On-Time SLA", 90)]
    hx = start_x + 20
    for hname, hw in headers:
        draw.text((hx, y_bot + 45), hname, fill="#64748B", font_size=11)
        hx += hw

    trows = [
        ("1", "Tirunelveli Junction (TEN)", "Central Hub", "Bus, Train, Auto Hub", "4.35m", "5.90m", "71.4%"),
        ("2", "New Bus Stand (VBS)", "Intercity Hub", "TNSTC City, SETC, Omni", "4.10m", "5.60m", "73.2%"),
        ("3", "Town Nellaiyappar", "Heritage Zone", "City Bus, Commercial", "3.85m", "5.15m", "75.0%")
    ]
    for idx, tr in enumerate(trows):
        ry = y_bot + 75 + idx * 32
        rx = start_x + 20
        draw.line([(start_x + 20, ry - 4), (w - start_x - 20, ry - 4)], fill="#F1F5F9", width=1)
        for cidx, (val, col_w) in enumerate(zip(tr, [50, 230, 140, 170, 90, 90, 90])):
            t_col = "#EF4444" if cidx in [4, 5] else "#1E293B"
            draw.text((rx, ry), val, fill=t_col, font_size=12)
            rx += col_w

    out_file = SCREENSHOTS_DIR / "station_bottlenecks.png"
    img.save(out_file)
    print("Generated:", out_file)


def generate_peak_screenshot():
    """Generates Peak Hours & Congestion screenshot preview."""
    w, h = 1200, 750
    img = Image.new("RGB", (w, h), color="#F8FAFC")
    draw = ImageDraw.Draw(img)

    create_header(draw, "⏰ Peak-Hour Congestion Dynamics & Surge Analysis", "Tirunelveli Transit Platform • Morning/Evening Peaks across Nellai Corridors", w)

    # 4 Metric Cards
    start_x = 35
    card_w = 265
    card_h = 100
    gap = 20
    y_card = 115

    p_kpis = [
        ("PEAK HOUR AVG DELAY", "4.62 min", "+2.40m vs Off-Peak", "#EF4444"),
        ("OFF-PEAK AVG DELAY", "2.22 min", "Midday / Normal Traffic", "#3B82F6"),
        ("CONGESTION SURGE RATIO", "2.08x", "Delay Multiplier in Peak", "#EA580C"),
        ("PEAK ON-TIME SLA", "71.5%", "Target SLA: ≥80.0%", "#F59E0B")
    ]
    for i, (l, v, s, col) in enumerate(p_kpis):
        x = start_x + i * (card_w + gap)
        draw.rounded_rectangle([(x, y_card), (x + card_w, y_card + card_h)], radius=10, fill="#FFFFFF", outline="#E2E8F0", width=1)
        draw.rounded_rectangle([(x, y_card), (x + card_w, y_card + 4)], radius=2, fill=col)
        draw.text((x + 16, y_card + 14), l, fill="#64748B", font_size=11)
        draw.text((x + 16, y_card + 36), v, fill=col, font_size=26)
        draw.text((x + 16, y_card + 72), s, fill="#475569", font_size=11)

    # 24-Hour Delay Curve Chart
    y_chart = 240
    h_chart = 270
    draw.rounded_rectangle([(start_x, y_chart), (w - start_x, y_chart + h_chart)], radius=10, fill="#FFFFFF", outline="#E2E8F0", width=1)
    draw.text((start_x + 20, y_chart + 16), "📊 24-Hour Fleet Congestion Curve across Tirunelveli District (00:00 - 23:00)", fill="#0F172A", font_size=15)

    base_x = start_x + 60
    base_y = y_chart + h_chart - 40
    step_x = 42

    # Morning Peak (7 to 10)
    draw.rectangle([(base_x + 7 * step_x, y_chart + 50), (base_x + 10 * step_x, base_y)], fill="#FEF3C7")
    draw.text((base_x + 7 * step_x + 10, y_chart + 55), "Morning Peak (07-10h)", fill="#B45309", font_size=11)

    # Evening Peak (16 to 20)
    draw.rectangle([(base_x + 16 * step_x, y_chart + 50), (base_x + 20 * step_x, base_y)], fill="#FEE2E2")
    draw.text((base_x + 16 * step_x + 10, y_chart + 55), "Evening Peak (16-20h)", fill="#B91C1C", font_size=11)

    hourly_delays = [
        1.0, 0.8, 0.7, 0.8, 1.1, 1.7, 3.1, 4.6, 5.0, 4.0,
        2.4, 2.2, 2.3, 2.1, 2.2, 3.0, 4.7, 5.2, 4.6, 3.7,
        2.5, 1.9, 1.5, 1.2
    ]
    pts = []
    for h_idx, d_val in enumerate(hourly_delays):
        cx = base_x + h_idx * step_x
        cy = base_y - int(d_val * 32)
        pts.append((cx, cy))
        draw.ellipse([(cx - 4, cy - 4), (cx + 4, cy + 4)], fill="#DC2626")
        draw.text((cx - 8, base_y + 10), f"{h_idx:02d}", fill="#64748B", font_size=10)

    for i in range(len(pts) - 1):
        draw.line([pts[i], pts[i+1]], fill="#DC2626", width=3)

    # Bottom Heatmap Matrix
    y_heat = 530
    h_heat = 190
    draw.rounded_rectangle([(start_x, y_heat), (w - start_x, y_heat + h_heat)], radius=10, fill="#FFFFFF", outline="#E2E8F0", width=1)
    draw.text((start_x + 20, y_heat + 14), "🔥 Day-of-Week vs. Hour Congestion Heatmap Matrix", fill="#0F172A", font_size=15)

    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    heat_colors = ["#FEF2F2", "#FEE2E2", "#FECACA", "#FCA5A5", "#F87171", "#EF4444", "#DC2626"]
    for didx, day in enumerate(days):
        dy = y_heat + 45 + didx * 19
        draw.text((start_x + 25, dy + 2), day, fill="#475569", font_size=11)
        for hidx in range(24):
            hx = start_x + 70 + hidx * 43
            intensity = min(6, int((hourly_delays[hidx] + (0.5 if didx < 5 else -0.8)) * 1.2))
            draw.rectangle([(hx, dy), (hx + 40, dy + 16)], fill=heat_colors[intensity])

    out_file = SCREENSHOTS_DIR / "peak_hours_surge.png"
    img.save(out_file)
    print("Generated:", out_file)


if __name__ == "__main__":
    SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    generate_overview_screenshot()
    generate_map_screenshot()
    generate_route_screenshot()
    generate_station_screenshot()
    generate_peak_screenshot()
    print("All screenshots generated successfully in:", SCREENSHOTS_DIR)
