---
name: Tirunelveli Civic Transit
colors:
  surface: '#faf8ff'
  surface-dim: '#d2d9f4'
  surface-bright: '#faf8ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f2f3ff'
  surface-container: '#eaedff'
  surface-container-high: '#e2e7ff'
  surface-container-highest: '#dae2fd'
  on-surface: '#131b2e'
  on-surface-variant: '#40474f'
  inverse-surface: '#283044'
  inverse-on-surface: '#eef0ff'
  outline: '#707881'
  outline-variant: '#c0c7d1'
  surface-tint: '#006399'
  primary: '#00507d'
  on-primary: '#ffffff'
  primary-container: '#0369a1'
  on-primary-container: '#cbe4ff'
  inverse-primary: '#94ccff'
  secondary: '#006a61'
  on-secondary: '#ffffff'
  secondary-container: '#86f2e4'
  on-secondary-container: '#006f66'
  tertiary: '#733f00'
  on-tertiary: '#ffffff'
  tertiary-container: '#955301'
  on-tertiary-container: '#ffdbbe'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#cde5ff'
  primary-fixed-dim: '#94ccff'
  on-primary-fixed: '#001d32'
  on-primary-fixed-variant: '#004b74'
  secondary-fixed: '#89f5e7'
  secondary-fixed-dim: '#6bd8cb'
  on-secondary-fixed: '#00201d'
  on-secondary-fixed-variant: '#005049'
  tertiary-fixed: '#ffdcc1'
  tertiary-fixed-dim: '#ffb878'
  on-tertiary-fixed: '#2e1500'
  on-tertiary-fixed-variant: '#6c3a00'
  background: '#faf8ff'
  on-background: '#131b2e'
  surface-variant: '#dae2fd'
typography:
  headline-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.02em
  headline-lg-mobile:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '700'
    lineHeight: 32px
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Inter
    fontSize: 22px
    fontWeight: '600'
    lineHeight: 28px
    letterSpacing: -0.01em
  headline-sm:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '600'
    lineHeight: 24px
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  body-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 16px
  label-lg:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '600'
    lineHeight: 20px
    letterSpacing: 0.01em
  label-md:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.02em
  label-sm:
    fontFamily: Inter
    fontSize: 11px
    fontWeight: '700'
    lineHeight: 14px
    letterSpacing: 0.04em
  code-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 20px
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  gutter: 1rem
  gutter-mobile: 0.75rem
  margin: 1.5rem
  margin-mobile: 1rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 0.75rem
  space-lg: 1rem
  space-xl: 1.5rem
---

## Brand & Style
This design system embodies the pragmatic authority of municipal civic infrastructure. Tailored for daily commuters, students, and travelers navigating Tirunelveli Junction, new bus stands (Veinthankulam), and rural route connections across the district, the visual ethos prioritizes speed, readability under direct South Indian sunlight, and rock-solid reliability.

The design movement is **Austere Civic Utility**—a high-contrast, functionalist aesthetic that strips away all modern startup ornament (no blurred glass, no saturated mesh gradients, no playful floating blobs). The interface reflects institutional integrity: structured layouts, tabular alignment, clear status signifiers, and instant glanceability over poor network conditions.

## Colors
The palette is calibrated for high sunlight contrast, clear hierarchy, and immediate civic legibility.

- **Primary (`#0369A1` / Deep Municipal Slate Blue):** Anchor color for main interactive elements, primary transit routes, and verified government data feeds.
- **Secondary (`#0D9488` / Restrained Civic Teal):** Route badges, interchange indicators, and public utility actions.
- **Neutral (`#0F172A` / Dark Navy Slate):** Primary text and foundational outlines, ensuring WCAG AAA legibility against white and light slate backdrops.
- **Surfaces:**
  - Base: `#FFFFFF` (Crisp White canvas)
  - Surface Muted: `#F8FAFC` (App bars, outer gutters, card backgrounds)
  - Surface Subdued: `#F1F5F9` (Data table headers, zebra-striping, inactive badges)
  - Surface Border: `#CBD5E1` (Crisp dividing rules and field boundaries)
- **Transit Status Accents:**
  - **Live (Active GPS):** Text `#059669` / Surface `#ECFDF5` / Border `#A7F3D0`
  - **Recently Updated:** Text `#0284C7` / Surface `#F0F9FF` / Border `#BAE6FD`
  - **Scheduled (Timetable):** Text `#475569` / Surface `#F1F5F9` / Border `#CBD5E1`
  - **Moderate Delay:** Text `#D97706` / Surface `#FFFBEB` / Border `#FDE68A`
  - **Severe Delay / Cancelled:** Text `#DC2626` / Surface `#FEF2F2` / Border `#FECACA`
  - **Unavailable / No Signal:** Text `#94A3B8` / Surface `#F8FAFC` / Border `#E2E8F0`

## Typography
Typography is strictly utilitarian. **Inter** provides high legibility across small screens and dense operational timetables.

- **Tabular Figures (`tnum`):** Timings (e.g., `14:35`, `+12 min`), platform numbers, and route codes (e.g., `TN-72-N-1892`, `Train 16127`) must strictly enable OpenType tabular numbers (`font-feature-settings: "tnum"`) to ensure seamless vertical alignment in data tables and route manifests.
- **Hierarchy:** Limited to weights `400` (Regular for labels and descriptions), `500` (Medium for route markers and numbers), `600` (SemiBold for structural groupings and table headers), and `700` (Bold for station names and terminal destinations).
- **Tamil Script Compatibility:** Fallbacks must target high-readability system Tamil typefaces (`Nirmala UI`, `Latha`, system-ui) at identical line-height multipliers to prevent vertical shift during language toggles.

## Layout & Spacing
The layout follows a dense, structured civic grid designed for compact display of high-frequency route schedules.

- **Grid Architecture:** Desktop views utilize a 12-column structured layout capped at a maximum width of 1140px for single-glance readability on utility monitors. Mobile and handheld devices follow a 4-column compact layout with `1rem` outer screen margins.
- **Information Density:** Spacing between timetable rows, station stops, and platform cards is restrained (`0.5rem` to `0.75rem`), allowing maximum timetable lines per viewport without vertical clutter.
- **Responsive Adaptations:**
  - **Mobile (< 640px):** Single-column stacked transit lists; fixed top search and route filters; sticky bottom status updates.
  - **Tablet (640px - 1024px):** Split layout featuring searchable route lists on the left (40% width) and arrival schedules/live stop timeline on the right (60% width).
  - **Desktop (> 1024px):** Three-tier layout: Filter sidebar, main arrival boards, and detailed live platform/tracking panel.

## Elevation & Depth
In keeping with public utility standards, visual hierarchy is achieved via **low-contrast outlines and surface shading** rather than drop shadows.

- **Borders over Shadows:** All containers, station stop cards, and search filters use a single `1px solid #CBD5E1` outline.
- **Flat Surface Tiering:**
  - Level 0 (Base Canvas): `#FFFFFF`
  - Level 1 (Panels & Table Cards): `#F8FAFC` bordered with `#E2E8F0`
  - Level 2 (Selected Rows & Active Filter Bars): `#F1F5F9` bordered with `#94A3B8`
- **Minimal Elevated State:** A single functional elevation is permitted solely for floating alerts, contextual dropdowns, and mobile bottom sheets: `0 4px 6px -1px rgba(15, 23, 42, 0.08), 0 2px 4px -2px rgba(15, 23, 42, 0.06)`. No colored or blurred ambient shadows are allowed.

## Shapes
Shapes are strict, structured, and modest (`roundedness: 1`).

- **Base Radius:** `4px` (`0.25rem`) applied to input fields, buttons, table containers, search modules, and badges.
- **Secondary Containers:** `8px` (`0.5rem`) applied to primary modal dialogs and outer station cards.
- **Anti-Pill Rule:** Rounded pill shapes, stadium buttons, and high-radius circles are strictly forbidden for buttons and standard tags to maintain an architectural civic interface. Circular geometry is reserved solely for live status radar dots and route stop node pins on the vertical transit line.

## Components

### Buttons & Controls
- **Primary Action (Search Route, Track Live):** `#0369A1` background, `#FFFFFF` text, `4px` radius, `1px solid #0284C7` border. Hover: `#075985`. Height: 40px (Desktop), 44px (Mobile touch target).
- **Secondary / Filter Buttons:** `#FFFFFF` background, `#1E293B` text, `1px solid #CBD5E1` border. Hover: `#F8FAFC` and border `#94A3B8`.
- **Icon Buttons (Swap Origin/Destination):** Sharp square `36px × 36px`, `4px` radius, `1px solid #CBD5E1`, `#334155` glyph.

### Status Badges & Transit Integrity Indicators
- Constructed with `4px` radius, `1px solid` border, uppercase `11px` bold text (`label-sm`), and `padding: 2px 6px`.
- **Live Tracking:** `#ECFDF5` background, `#059669` text, `#A7F3D0` border. Accompanied by a `6px` solid emerald dot with CSS scale keyframe pulse.
- **Recently Updated:** `#F0F9FF` background, `#0284C7` text, `#BAE6FD` border.
- **Scheduled:** `#F1F5F9` background, `#475569` text, `#CBD5E1` border.
- **Delayed:** `#FFFBEB` background, `#D97706` text, `#FDE68A` border.
- **Cancelled / Critical Delay:** `#FEF2F2` background, `#DC2626` text, `#FECACA` border.
- **Offline / Untracked:** `#F8FAFC` background, `#94A3B8` text, `#E2E8F0` border.

### Input Fields & Select Menus
- **Origin & Destination Inputs:** `#FFFFFF` surface, `1px solid #CBD5E1` border, `4px` radius, `14px` text (`#0F172A`).
- **Focus State:** `1px solid #0369A1` accompanied by a flat `2px` focus outline `rgba(3, 105, 161, 0.2)`. Zero ambient glow.
- **Placeholder:** `#94A3B8` for instant clarity.

### Timetable & Route Cards
- Flat container with `1px solid #E2E8F0` border, `4px` radius, and `#FFFFFF` background.
- Left edge features a `4px` solid vertical accent bar indicating route type (Bus: `#0D9488`, Local Train: `#0369A1`, Express: `#475569`).
- Station stops arranged vertically along a 2px `#CBD5E1` line with `8px` hollow square nodes for intermediate stops and solid `8px` disks for junctions.

### Data Tables & Stop Lists
- Border collapse with `1px solid #E2E8F0` horizontal divider rules.
- Header row `#F8FAFC` with bold, uppercase `#475569` text (`label-md`).
- Alternating zebra row shading with `#F8FAFC` on hover for rapid scan tracking across dense platform timelines.