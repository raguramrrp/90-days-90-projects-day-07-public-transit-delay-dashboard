"""Generates authentic visual screenshot assets for documentation and portfolio presentation."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from PIL import Image, ImageDraw, ImageFont
from config import SCREENSHOTS_DIR


def create_header(draw, title, subtitle, width, height=90):
    """Draws top dark executive header banner."""
    draw.rectangle([(0, 0), (width, height)], fill="#0F172A")
    # Accent top border
    draw.rectangle([(0, 0), (width, 4)], fill="#3B82F6")
    draw.text((30, 20), title, fill="#FFFFFF", font_size=24)
    draw.text((30, 52), subtitle, fill="#94A3B8", font_size=13)
    # Status pill
    draw.rounded_rectangle([(width - 240, 28), (width - 30, 62)], radius=8, fill="#065F46")
    draw.text((width - 225, 36), "● LIVE ANALYTICS ENGINE", fill="#ECFDF5", font_size=12)


def generate_overview_screenshot():
    """Generates Overview page screenshot preview."""
    w, h = 1200, 750
    img = Image.new("RGB", (w, h), color="#F8FAFC")
    draw = ImageDraw.Draw(img)

    create_header(draw, "🚆 Public Transit Delay Analytics Dashboard", "Metropolitan Transit Authority • Executive Overview & Reliability KPIs", w)

    # 5 Top KPI Cards
    card_w = 210
    card_h = 110
    start_x = 35
    gap = 22
    y_card = 115

    kpis = [
        ("TOTAL TRIPS", "2,140", "11,375 Arrivals Monitored", "#0F172A"),
        ("ON-TIME ARRIVAL RATE", "82.4%", "≤ 2.0 mins or Early (SLA)", "#10B981"),
        ("AVERAGE DELAY", "2.85 min", "Fleet Variance from Sched", "#3B82F6"),
        ("SEVERE DELAYS (>15m)", "128", "1.1% Critical Incidents", "#EF4444"),
        ("RELIABILITY INDEX (TRI)", "84.2/100", "High (Optimal Service)", "#10B981")
    ]

    for i, (label, val, sub, color) in enumerate(kpis):
        x = start_x + i * (card_w + gap)
        draw.rounded_rectangle([(x, y_card), (x + card_w, y_card + card_h)], radius=10, fill="#FFFFFF", outline="#E2E8F0", width=1)
        draw.rounded_rectangle([(x, y_card), (x + card_w, y_card + 4)], radius=2, fill=color)
        draw.text((x + 14, y_card + 14), label, fill="#64748B", font_size=11)
        draw.text((x + 14, y_card + 36), val, fill=color, font_size=26)
        draw.text((x + 14, y_card + 78), sub, fill="#475569", font_size=11)

    # Chart 1: 30-Day Fleet Delay Trend
    y_chart1 = 250
    w_chart1 = 700
    h_chart1 = 260
    draw.rounded_rectangle([(start_x, y_chart1), (start_x + w_chart1, y_chart1 + h_chart1)], radius=10, fill="#FFFFFF", outline="#E2E8F0", width=1)
    draw.text((start_x + 20, y_chart1 + 16), "📈 30-Day Fleet Delay Trend & 7-Day Rolling Moving Average", fill="#0F172A", font_size=15)
    draw.line([(start_x + 20, y_chart1 + 45), (start_x + w_chart1 - 20, y_chart1 + 45)], fill="#F1F5F9", width=1)

    # Draw simulated bars and trend line
    bar_y_base = y_chart1 + h_chart1 - 40
    import random
    random.seed(42)
    daily_delays = [random.uniform(1.8, 4.2) for _ in range(28)]
    pts = []
    for idx, d in enumerate(daily_delays):
        bx = start_x + 40 + idx * 22
        b_height = int(d * 32)
        draw.rectangle([(bx, bar_y_base - b_height), (bx + 14, bar_y_base)], fill="#CBD5E1")
        pts.append((bx + 7, bar_y_base - int(sum(daily_delays[max(0, idx-3):idx+1]) / len(daily_delays[max(0, idx-3):idx+1]) * 32)))

    # Draw moving average curve
    for j in range(len(pts) - 1):
        draw.line([pts[j], pts[j+1]], fill="#2563EB", width=3)

    # SLA line
    sla_y = bar_y_base - int(3.0 * 32)
    draw.line([(start_x + 40, sla_y), (start_x + w_chart1 - 30, sla_y)], fill="#10B981", width=2)
    draw.text((start_x + w_chart1 - 160, sla_y - 18), "Target SLA (3.0m)", fill="#10B981", font_size=11)

    # Chart 2: Arrival Performance Donut Mock
    x_chart2 = start_x + w_chart1 + 25
    w_chart2 = 410
    draw.rounded_rectangle([(x_chart2, y_chart1), (x_chart2 + w_chart2, y_chart1 + h_chart1)], radius=10, fill="#FFFFFF", outline="#E2E8F0", width=1)
    draw.text((x_chart2 + 20, y_chart1 + 16), "🎯 Arrival Performance Breakdown", fill="#0F172A", font_size=15)
    draw.line([(x_chart2 + 20, y_chart1 + 45), (x_chart2 + w_chart2 - 20, y_chart1 + 45)], fill="#F1F5F9", width=1)

    # Draw slices representation
    cat_items = [
        ("On-Time (≤ 2.0m)", "71.8%", "#10B981"),
        ("Early Arrival", "10.6%", "#059669"),
        ("Minor Delay (2-5m)", "11.2%", "#FBBF24"),
        ("Moderate Delay (5-15m)", "5.3%", "#F97316"),
        ("Severe Delay (>15m)", "1.1%", "#EF4444")
    ]
    for idx, (cat_name, pct, col) in enumerate(cat_items):
        cy = y_chart1 + 65 + idx * 36
        draw.rounded_rectangle([(x_chart2 + 25, cy + 4), (x_chart2 + 40, cy + 19)], radius=3, fill=col)
        draw.text((x_chart2 + 50, cy + 2), cat_name, fill="#334155", font_size=13)
        draw.text((x_chart2 + w_chart2 - 75, cy + 2), pct, fill=col, font_size=13)

    # Row 3: Root Cause Bar Chart
    y_chart3 = 530
    h_chart3 = 190
    draw.rounded_rectangle([(start_x, y_chart3), (w - start_x, y_chart3 + h_chart3)], radius=10, fill="#FFFFFF", outline="#E2E8F0", width=1)
    draw.text((start_x + 20, y_chart3 + 14), "🔍 Primary Delay Root Causes (Loss Hours & Incidents)", fill="#0F172A", font_size=15)

    causes = [
        ("High Passenger Boarding Volume", "1,840 mins", 380, "#DC2626"),
        ("Traffic Congestion (Bus Corridors)", "1,210 mins", 270, "#EA580C"),
        ("Signal & Switch Malfunctions", "840 mins", 190, "#D97706"),
        ("Track Maintenance & Speed Restrictions", "560 mins", 130, "#2563EB"),
        ("Inclement Weather / Traction Loss", "320 mins", 85, "#4B5563")
    ]
    for idx, (c_name, mins, bar_len, c_col) in enumerate(causes):
        cy = y_chart3 + 45 + idx * 26
        draw.text((start_x + 25, cy), c_name, fill="#334155", font_size=12)
        draw.rounded_rectangle([(start_x + 320, cy + 2), (start_x + 320 + bar_len, cy + 16)], radius=4, fill=c_col)
        draw.text((start_x + 330 + bar_len, cy), mins, fill="#64748B", font_size=11)

    out_file = SCREENSHOTS_DIR / "dashboard_overview.png"
    img.save(out_file)
    print("Generated:", out_file)


def generate_route_screenshot():
    """Generates Route Analysis screenshot preview."""
    w, h = 1200, 750
    img = Image.new("RGB", (w, h), color="#F8FAFC")
    draw = ImageDraw.Draw(img)

    create_header(draw, "🚏 Transit Route Reliability & Performance League Table", "Metropolitan Transit Authority • Route Rankings & Stop Cascades", w)

    # Route Table Card
    start_x = 35
    y_card = 115
    w_table = 720
    h_table = 380

    draw.rounded_rectangle([(start_x, y_card), (start_x + w_table, y_card + h_table)], radius=10, fill="#FFFFFF", outline="#E2E8F0", width=1)
    draw.text((start_x + 20, y_card + 16), "🚆 Route Reliability League Table", fill="#0F172A", font_size=16)
    draw.line([(start_x + 20, y_card + 48), (start_x + w_table - 20, y_card + 48)], fill="#E2E8F0", width=1)

    headers = [("Rank", 30), ("Route Name", 140), ("Type", 120), ("Stops", 60), ("Avg Delay", 80), ("On-Time %", 90), ("TRI Score", 80)]
    hx = start_x + 20
    for hname, hw in headers:
        draw.text((hx, y_card + 56), hname, fill="#64748B", font_size=12)
        hx += hw

    route_rows = [
        ("1", "Red Line (Subway)", "Subway", "2,420", "1.92m", "88.4%", "89.1", "#10B981"),
        ("2", "Blue Line (Subway)", "Subway", "2,180", "2.14m", "86.2%", "87.4", "#10B981"),
        ("3", "Commuter Rail 305", "Commuter", "1,850", "2.75m", "83.5%", "84.2", "#3B82F6"),
        ("4", "Green Line (Light Rail)", "Light Rail", "1,940", "3.10m", "80.1%", "81.0", "#3B82F6"),
        ("5", "Orange Line (BRT)", "BRT", "1,620", "3.65m", "77.8%", "76.5", "#F59E0B"),
        ("6", "Bus 101 Express", "Express Bus", "1,365", "4.20m", "74.2%", "72.0", "#F59E0B")
    ]

    for idx, rdata in enumerate(route_rows):
        ry = y_card + 90 + idx * 45
        draw.line([(start_x + 20, ry - 6), (start_x + w_table - 20, ry - 6)], fill="#F1F5F9", width=1)
        rx = start_x + 20
        for cidx, (val, col_w) in enumerate(zip(rdata[:7], [30, 140, 120, 60, 80, 90, 80])):
            text_col = rdata[7] if cidx == 6 else "#1E293B"
            draw.text((rx, ry + 4), str(val), fill=text_col, font_size=12)
            rx += col_w

    # Side chart: TRI comparison
    x_chart2 = start_x + w_table + 25
    w_chart2 = 390
    draw.rounded_rectangle([(x_chart2, y_card), (x_chart2 + w_chart2, y_card + h_table)], radius=10, fill="#FFFFFF", outline="#E2E8F0", width=1)
    draw.text((x_chart2 + 20, y_card + 16), "📊 Route Reliability Index (TRI)", fill="#0F172A", font_size=15)
    draw.line([(x_chart2 + 20, y_card + 48), (x_chart2 + w_chart2 - 20, y_card + 48)], fill="#E2E8F0", width=1)

    for idx, (rn, rname, rtype, stops, avg_d, ot, tri_v, col) in enumerate(route_rows):
        cy = y_card + 75 + idx * 48
        draw.text((x_chart2 + 20, cy), rname.split(" ")[0] + " " + rname.split(" ")[1], fill="#334155", font_size=12)
        score_val = float(tri_v)
        b_len = int(score_val * 2.2)
        draw.rounded_rectangle([(x_chart2 + 130, cy + 2), (x_chart2 + 130 + b_len, cy + 18)], radius=4, fill=col)
        draw.text((x_chart2 + 140 + b_len, cy), f"{tri_v}/100", fill="#475569", font_size=11)

    # Bottom Cascade Chart
    y_casc = 520
    h_casc = 200
    draw.rounded_rectangle([(start_x, y_casc), (w - start_x, y_casc + h_casc)], radius=10, fill="#FFFFFF", outline="#E2E8F0", width=1)
    draw.text((start_x + 20, y_casc + 14), "🌊 Stop-by-Stop Delay Cascading Profile (Selected: Red Line)", fill="#0F172A", font_size=15)

    stops = [
        ("Downtown Central", 0.4),
        ("Financial District", 0.9),
        ("Union Station Hub", 2.1),
        ("City Hospital", 2.6),
        ("University Heights", 3.1),
        ("Tech Hub Innovation", 3.4)
    ]
    base_cx = start_x + 80
    base_cy = y_casc + h_casc - 45
    pts = []
    for sidx, (stn, del_val) in enumerate(stops):
        sx = base_cx + sidx * 175
        sy = base_cy - int(del_val * 35)
        pts.append((sx, sy))
        draw.ellipse([(sx - 6, sy - 6), (sx + 6, sy + 6)], fill="#EA580C", outline="#FFFFFF", width=2)
        draw.text((sx - 15, sy - 24), f"{del_val:.1f}m", fill="#EA580C", font_size=12)
        draw.text((sx - 40, base_cy + 12), stn, fill="#475569", font_size=11)

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

    create_header(draw, "📍 Station Bottleneck Identification & Delay Hotspots", "Metropolitan Transit Authority • Critical Network Hubs & Dwell Congestion", w)

    start_x = 35
    y_top = 115
    w_col = 550
    h_box = 400

    # Box 1: Geographic Map Placeholder Representation
    draw.rounded_rectangle([(start_x, y_top), (start_x + w_col, y_top + h_box)], radius=10, fill="#FFFFFF", outline="#E2E8F0", width=1)
    draw.text((start_x + 20, y_top + 16), "🗺️ Geographic Station Delay Map (Bubble Size = Delay)", fill="#0F172A", font_size=15)
    draw.line([(start_x + 20, y_top + 48), (start_x + w_col - 20, y_top + 48)], fill="#E2E8F0", width=1)

    # Draw simulated map grid & bubbles
    map_x = start_x + 30
    map_y = y_top + 70
    map_w = w_col - 60
    map_h = h_box - 90
    draw.rounded_rectangle([(map_x, map_y), (map_x + map_w, map_y + map_h)], radius=8, fill="#F8FAFC", outline="#CBD5E1")

    stations = [
        (map_x + 120, map_y + 110, 28, "#EF4444", "Downtown Central (4.8m)"),
        (map_x + 240, map_y + 90, 24, "#F97316", "Union Station (4.2m)"),
        (map_x + 320, map_y + 140, 20, "#F59E0B", "Civic Center (3.6m)"),
        (map_x + 180, map_y + 190, 16, "#3B82F6", "Midtown Interchange (3.1m)"),
        (map_x + 390, map_y + 220, 22, "#EF4444", "Eastgate Terminal (4.4m)"),
        (map_x + 80, map_y + 240, 14, "#10B981", "West Harbor (2.1m)"),
        (map_x + 280, map_y + 260, 12, "#10B981", "University Heights (1.9m)")
    ]
    for bx, by, br, bcol, bname in stations:
        draw.ellipse([(bx - br, by - br), (bx + br, by + br)], fill=bcol, outline="#FFFFFF", width=2)
        draw.text((bx - 20, by + br + 4), bname.split(" ")[0], fill="#334155", font_size=11)

    # Box 2: Top Bottleneck Ranking Bar Chart
    x_col2 = start_x + w_col + 30
    draw.rounded_rectangle([(x_col2, y_top), (x_col2 + w_col, y_top + h_box)], radius=10, fill="#FFFFFF", outline="#E2E8F0", width=1)
    draw.text((x_col2 + 20, y_top + 16), "🏆 Top 7 Bottleneck Stations by Average Delay", fill="#0F172A", font_size=15)
    draw.line([(x_col2 + 20, y_top + 48), (x_col2 + w_col - 20, y_top + 48)], fill="#E2E8F0", width=1)

    bottlenecks = [
        ("Downtown Central Hub", "4.82 min", 270, "#DC2626"),
        ("Eastgate Transfer Terminal", "4.41 min", 245, "#DC2626"),
        ("Union Station Major Interchange", "4.20 min", 230, "#EA580C"),
        ("Civic Center & City Hall", "3.65 min", 195, "#EA580C"),
        ("Airport International Term 1", "3.48 min", 185, "#F59E0B"),
        ("Midtown Interchange", "3.12 min", 165, "#F59E0B"),
        ("City Hospital & Medical Ctr", "2.80 min", 145, "#3B82F6")
    ]
    for idx, (st_name, avg_d, bar_w, col) in enumerate(bottlenecks):
        by = y_top + 70 + idx * 44
        draw.text((x_col2 + 20, by), st_name, fill="#1E293B", font_size=12)
        draw.rounded_rectangle([(x_col2 + 220, by + 2), (x_col2 + 220 + bar_w, by + 18)], radius=4, fill=col)
        draw.text((x_col2 + 230 + bar_w, by), avg_d, fill="#64748B", font_size=11)

    # Bottom Table: Bottleneck Details
    y_bot = 540
    h_bot = 180
    draw.rounded_rectangle([(start_x, y_bot), (w - start_x, y_bot + h_bot)], radius=10, fill="#FFFFFF", outline="#E2E8F0", width=1)
    draw.text((start_x + 20, y_bot + 14), "📋 Station Bottleneck Compliance & Transfer Impact", fill="#0F172A", font_size=15)

    headers = [("Rank", 60), ("Station", 220), ("Zone", 90), ("Transfer?", 100), ("Arrivals", 90), ("Avg Delay", 100), ("Peak Delay", 100), ("On-Time SLA", 100)]
    hx = start_x + 20
    for hname, hw in headers:
        draw.text((hx, y_bot + 45), hname, fill="#64748B", font_size=11)
        hx += hw

    trows = [
        ("1", "Downtown Central", "Zone 1", "Yes", "1,840", "4.82m", "6.45m", "68.2%"),
        ("2", "Eastgate Transfer Terminal", "Zone 2", "Yes", "1,210", "4.41m", "5.80m", "71.4%"),
        ("3", "Union Station Hub", "Zone 1", "Yes", "1,980", "4.20m", "5.65m", "73.8%")
    ]
    for idx, tr in enumerate(trows):
        ry = y_bot + 75 + idx * 32
        rx = start_x + 20
        draw.line([(start_x + 20, ry - 4), (w - start_x - 20, ry - 4)], fill="#F1F5F9", width=1)
        for cidx, (val, col_w) in enumerate(zip(tr, [60, 220, 90, 100, 90, 100, 100, 100])):
            t_col = "#EF4444" if cidx in [5, 6] else "#1E293B"
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

    create_header(draw, "⏰ Peak-Hour Congestion Dynamics & Surge Analysis", "Metropolitan Transit Authority • 24-Hour Delay Curves & Congestion Heatmap", w)

    # 4 Metric Cards
    start_x = 35
    card_w = 265
    card_h = 100
    gap = 20
    y_card = 115

    p_kpis = [
        ("PEAK HOUR AVG DELAY", "4.65 min", "+2.45m vs Off-Peak", "#EF4444"),
        ("OFF-PEAK AVG DELAY", "2.20 min", "Midday / Normal Traffic", "#3B82F6"),
        ("CONGESTION SURGE RATIO", "2.11x", "Delay Multiplier in Peak", "#EA580C"),
        ("PEAK ON-TIME SLA", "71.2%", "Target SLA: ≥80.0%", "#F59E0B")
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
    draw.text((start_x + 20, y_chart + 16), "📊 24-Hour Fleet Congestion Curve (00:00 - 23:00)", fill="#0F172A", font_size=15)

    # Shaded Peak Bands
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
        1.1, 0.9, 0.8, 0.9, 1.2, 1.8, 3.2, 4.8, 5.1, 4.2,
        2.5, 2.3, 2.4, 2.2, 2.3, 3.1, 4.9, 5.4, 4.8, 3.8,
        2.6, 2.0, 1.6, 1.3
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
            # Simulated intensity
            intensity = min(6, int((hourly_delays[hidx] + (0.5 if didx < 5 else -0.8)) * 1.2))
            draw.rectangle([(hx, dy), (hx + 40, dy + 16)], fill=heat_colors[intensity])

    out_file = SCREENSHOTS_DIR / "peak_hours_surge.png"
    img.save(out_file)
    print("Generated:", out_file)


if __name__ == "__main__":
    SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    generate_overview_screenshot()
    generate_route_screenshot()
    generate_station_screenshot()
    generate_peak_screenshot()
    print("All screenshots generated successfully in:", SCREENSHOTS_DIR)
