"""Tests for the Google Stitch Civic UI Template and Integration."""

from pathlib import Path


def test_stitch_template_exists_and_valid():
    """Verify stitch_template.html exists and is well-formed HTML."""
    tpl_path = Path(__file__).resolve().parent.parent / "src" / "stitch_template.html"
    assert tpl_path.exists(), "src/stitch_template.html must exist"
    
    content = tpl_path.read_text(encoding="utf-8")
    assert "<!DOCTYPE html>" in content
    assert "Tirunelveli Transport Tracker" in content


def test_stitch_template_civic_palette_and_typography():
    """Verify Stitch Austere Civic utility design tokens are present."""
    tpl_path = Path(__file__).resolve().parent.parent / "src" / "stitch_template.html"
    content = tpl_path.read_text(encoding="utf-8")
    
    # Font & Material Symbols
    assert "Inter" in content
    assert "Material+Symbols+Outlined" in content
    
    # Civic color palette
    assert "#00507d" in content or "primary" in content
    assert "#006a61" in content or "secondary" in content


def test_stitch_template_bus_search_features():
    """Verify Bus Search view contains required elements matching Stitch designs."""
    tpl_path = Path(__file__).resolve().parent.parent / "src" / "stitch_template.html"
    content = tpl_path.read_text(encoding="utf-8")
    
    # Views & navigation
    assert 'id="view-bus"' in content
    assert "Thamirabarani Urban Trunk Line" in content
    assert "THAMIRABARANI RIVER" in content
    assert "Sulochana Mudaliar Bridge" in content
    
    # Routes & vehicles
    assert "11A" in content
    assert "TN-72-N-1842" in content
    assert "Vannarpettai" in content
    assert "Palayamkottai" in content
    assert "Route 11A Vehicle Inspector" in content
    assert "Ashok Leyland BS-VI" in content


def test_stitch_template_train_search_features():
    """Verify Train Search view contains NTES telemetry and 16127 Guruvayur Express."""
    tpl_path = Path(__file__).resolve().parent.parent / "src" / "stitch_template.html"
    content = tpl_path.read_text(encoding="utf-8")
    
    assert 'id="view-train"' in content
    assert "SOUTHERN RAILWAY NTES FEED: ONLINE" in content
    assert "Madurai Railway Division (MDU)" in content
    assert "16127" in content
    assert "Guruvayur Express" in content
    assert "WAP-7 ED 37102" in content
    assert "Gangaikondan" in content
    assert "CRIS NTES CERTIFIED" in content
    # Geographic boundary enforcement demonstration
    assert "12626" in content
    assert "Kerala Express" in content


def test_stitch_template_station_hubs():
    """Verify Station Hubs view contains terminals, SVG schematic, and auto tariff."""
    tpl_path = Path(__file__).resolve().parent.parent / "src" / "stitch_template.html"
    content = tpl_path.read_text(encoding="utf-8")
    
    assert 'id="view-hubs"' in content
    assert "Tirunelveli Central Junction" in content
    assert "Civic Interchange Schematic" in content
    assert "PREPAID AUTO BOOTH" in content
    assert "0462-2331555" in content
    assert "9487440000" in content
