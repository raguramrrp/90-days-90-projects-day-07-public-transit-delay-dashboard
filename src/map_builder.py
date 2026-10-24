"""Interactive Leaflet map builder for Tirunelveli Local Transport Platform.
Renders route polylines, verified station nodes, vehicle markers, and stops
with honest data freshness tagging and clean civic styling.
"""

from typing import List, Optional
import folium
from folium.plugins import MarkerCluster, Fullscreen
from config import TIRUNELVELI_MAP_CENTER, DEFAULT_ZOOM_LEVEL
from src.tirunelveli_data import TIRUNELVELI_ROUTES, TIRUNELVELI_STATIONS


def create_transit_leaflet_map(
    routes_df=None,
    stations_df=None,
    vehicles_df=None,
    positions_df=None,
    selected_modes: Optional[List[str]] = None,
    selected_routes: Optional[List[str]] = None,
    selected_statuses: Optional[List[str]] = None,
    enable_clustering: bool = False,
    show_route_lines: bool = True,
    show_stations: bool = True,
    focus_vehicle_id: Optional[str] = None,
    focus_stop_id: Optional[str] = None,
    is_demo_mode: bool = False
) -> folium.Map:
    """Builds and returns a styled Leaflet transit map for Tirunelveli."""
    map_center = list(TIRUNELVELI_MAP_CENTER)
    zoom = DEFAULT_ZOOM_LEVEL

    # Center on focused stop if provided
    if focus_stop_id:
        stn = next((s for s in TIRUNELVELI_STATIONS if s["station_id"] == focus_stop_id), None)
        if stn:
            map_center = [stn["latitude"], stn["longitude"]]
            zoom = 15

    # Center on focused vehicle if requested
    if focus_vehicle_id and positions_df is not None and not positions_df.empty:
        focus_pos = positions_df[positions_df["vehicle_id"] == focus_vehicle_id]
        if not focus_pos.empty:
            map_center = [float(focus_pos.iloc[0]["latitude"]), float(focus_pos.iloc[0]["longitude"])]
            zoom = 14

    m = folium.Map(
        location=map_center,
        zoom_start=zoom,
        tiles="OpenStreetMap",
        control_scale=True
    )
    Fullscreen().add_to(m)

    # 1. Draw Route Polylines
    if show_route_lines:
        station_coords = {s["station_id"]: [s["latitude"], s["longitude"]] for s in TIRUNELVELI_STATIONS}

        for r_meta in TIRUNELVELI_ROUTES:
            if selected_routes and r_meta["route_short_name"] not in selected_routes and r_meta["route_id"] not in selected_routes:
                continue
            if selected_modes and r_meta["route_type"] not in selected_modes:
                continue

            stops = r_meta.get("stops", [])
            points = [station_coords[sid] for sid in stops if sid in station_coords]
            if len(points) >= 2:
                folium.PolyLine(
                    locations=points,
                    color=r_meta.get("color_hex", "#0D9488"),
                    weight=4,
                    opacity=0.8,
                    tooltip=f"{r_meta['route_short_name']} ({r_meta.get('operating_hours', 'Regular')})"
                ).add_to(m)

    # 2. Draw Station Nodes
    if show_stations:
        station_group = folium.FeatureGroup(name="Transit Stations & Stops").add_to(m)
        for stn in TIRUNELVELI_STATIONS:
            is_focused_stop = (focus_stop_id == stn["station_id"])
            popup_html = f"""
            <div style="font-family: -apple-system, sans-serif; width: 230px; line-height: 1.4; color: #0F172A;">
                <div style="font-size: 13px; font-weight: 700; color: #0F172A;">{stn['station_name']}</div>
                <div style="font-size: 11px; color: #0D9488; font-weight: 600;">{stn.get('tamil_name', '')}</div>
                <div style="font-size: 11px; color: #64748B; margin-bottom: 6px;">Code: {stn['station_code']} • {stn['zone_id']}</div>
                <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; padding: 5px 8px; border-radius: 4px; font-size: 11px; margin-bottom: 4px;">
                    <strong>Type:</strong> {'Interchange Hub' if stn.get('is_transfer_station') == 1 else 'Local Stop'}<br/>
                    <strong>Platforms / Bays:</strong> {stn.get('platforms_count', 2)}<br/>
                    <strong>Modes:</strong> {stn.get('accessible_modes', 'Bus')}
                </div>
                <div style="font-size: 10px; color: #94A3B8;">GPS: {stn['latitude']:.4f}° N, {stn['longitude']:.4f}° E</div>
            </div>
            """

            folium.CircleMarker(
                location=[stn["latitude"], stn["longitude"]],
                radius=8 if is_focused_stop else (6 if stn.get("is_transfer_station") == 1 else 4),
                color="#0D9488" if is_focused_stop else "#0F172A",
                weight=3 if is_focused_stop else 1.5,
                fill=True,
                fill_color="#FEF08A" if is_focused_stop else ("#FFFFFF" if stn.get("is_transfer_station") == 1 else "#94A3B8"),
                fill_opacity=0.95,
                popup=folium.Popup(popup_html, max_width=260),
                tooltip=f"🚏 {stn['station_name']} ({stn['station_code']})"
            ).add_to(station_group)

    # 3. Vehicle Markers Layer
    if positions_df is not None and not positions_df.empty and vehicles_df is not None and not vehicles_df.empty:
        veh_cols = [c for c in vehicles_df.columns if c not in ["route_id", "operator_id"]]
        merged = positions_df.merge(vehicles_df[veh_cols], on="vehicle_id", how="left")
        if routes_df is not None and not routes_df.empty:
            merged = merged.merge(routes_df[["route_id", "route_short_name", "color_hex"]], on="route_id", how="left")

        if selected_modes:
            merged = merged[merged["transport_mode"].isin(selected_modes)]
        if selected_routes:
            merged = merged[merged["route_short_name"].isin(selected_routes)]

        target_layer = MarkerCluster(name="Vehicle Cluster").add_to(m) if enable_clustering else m

        for _, v in merged.iterrows():
            mode = v.get("transport_mode", "Bus")
            icon_name = "bus" if mode == "Bus" else "train"
            icon_color = "cadetblue" if mode == "Bus" else "red"
            v_name = v.get("vehicle_label", v["vehicle_id"])
            speed = v.get("speed_kmh", 0.0)

            is_focused = (focus_vehicle_id == v["vehicle_id"])

            status_tag = "SIMULATED TEST DATA" if is_demo_mode else "SCHEDULED RUNTIME"
            tag_color = "#D97706" if is_demo_mode else "#475569"

            popup_html = f"""
            <div style="font-family: -apple-system, sans-serif; width: 250px; line-height: 1.4; color: #0F172A;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                    <span style="font-size: 13px; font-weight: 700; color: #0F172A;">{v_name}</span>
                    <span style="background-color: #F1F5F9; color: {tag_color}; padding: 2px 6px; border-radius: 4px; font-size: 9px; font-weight: 700;">
                        {status_tag}
                    </span>
                </div>
                <div style="font-size: 11px; font-weight: 600; color: #0D9488; margin-bottom: 2px;">{v.get('route_short_name', 'Corridor')}</div>
                <div style="font-size: 11px; color: #64748B; margin-bottom: 6px;">Mode: {mode}</div>
                <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; padding: 5px 8px; border-radius: 4px; font-size: 11px;">
                    • <strong>Speed:</strong> {speed} km/h<br/>
                    • <strong>Location:</strong> {v['latitude']:.4f}° N, {v['longitude']:.4f}° E<br/>
                    • <strong>Schedule:</strong> Regular Operational Hours
                </div>
            </div>
            """

            folium.Marker(
                location=[v["latitude"], v["longitude"]],
                popup=folium.Popup(popup_html, max_width=270),
                tooltip=f"📍 {v_name} • {mode}",
                icon=folium.Icon(color="green" if is_focused else icon_color, icon=icon_name, prefix="fa")
            ).add_to(target_layer)

    return m
