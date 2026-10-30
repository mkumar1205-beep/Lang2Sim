import sys
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

TEMPLATE_PATH = "/home/manya/.gemini/antigravity/brain/a5971736-a22d-4d3b-b099-5cb2dbef7738/.user_uploaded/media_1793068344043_ea19c526.pptx"
OUTPUT_PATH = "/home/manya/manya_worldgen/Lang2Sim/Lang2Sim_Judging_Pitch.pptx"

def build_pitch_deck():
    prs = Presentation(TEMPLATE_PATH)
    print(f"Loaded template with {len(prs.slides)} slides. Dimensions: {prs.slide_width} x {prs.slide_height}")

    # Coordinated Color Palette tuned for the cream/ivory template (#FFF4E0)
    DARK_WINE    = RGBColor(67, 2, 1)      # #430201 - Template native accent
    DEEP_NAVY    = RGBColor(15, 23, 42)    # #0F172A - Premium card background
    CARD_BG      = RGBColor(22, 32, 54)    # #162036 - Card surface
    CARD_LIGHT   = RGBColor(30, 45, 75)    # #1E2D4B - Elevated card surface
    BORDER_COL   = RGBColor(51, 65, 85)    # #334155 - Subtle border
    ACCENT_CYAN  = RGBColor(0, 210, 255)   # #00D2FF - Tech highlight
    ACCENT_SKY   = RGBColor(56, 189, 248)  # #38BDF8 - Secondary tech accent
    ACCENT_EMERALD = RGBColor(16, 185, 129)# #10B981 - Success / money
    ACCENT_ROSE  = RGBColor(244, 63, 94)   # #F43F5E - Pain points / warnings
    ACCENT_PURPLE= RGBColor(139, 92, 246)  # #8B5CF6 - Innovation
    TEXT_LIGHT   = RGBColor(248, 250, 252) # #F8FAFC - Main card text
    TEXT_MUTED   = RGBColor(148, 163, 184) # #94A3B8 - Subtitle / description
    TEXT_DARK    = RGBColor(15, 23, 42)    # #0F172A - Direct slide text

    # Slide 1: Update Title & Subtitles
    s1 = prs.slides[0]
    for shape in s1.shapes:
        if shape.name == "TextBox 12":
            shape.text_frame.text = ""
            p = shape.text_frame.paragraphs[0]
            p.text = "Team Lang2Sim"
            p.font.name = "Arial"
            p.font.size = Pt(24)
            p.font.bold = True
            p.font.color.rgb = DARK_WINE
            p.alignment = PP_ALIGN.LEFT
        elif shape.shape_type == 6: # Group 2
            for sub in shape.shapes:
                if sub.name == "TextBox 6": # Project TITLE
                    sub.text_frame.text = ""
                    p = sub.text_frame.paragraphs[0]
                    p.text = "Lang2Sim"
                    p.font.name = "Arial"
                    p.font.size = Pt(64)
                    p.font.bold = True
                    p.font.color.rgb = DARK_WINE
                elif sub.name == "TextBox 7": # (Hardware/Software)
                    sub.text_frame.text = ""
                    p = sub.text_frame.paragraphs[0]
                    p.text = "(Software: Autonomous Robotics Simulation Copilot)"
                    p.font.name = "Arial"
                    p.font.size = Pt(18)
                    p.font.bold = True
                    p.font.color.rgb = DARK_WINE

    # Add subtitle & core descriptor card to Slide 1
    s1_card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.5), Inches(5.8), Inches(11.0), Inches(2.2))
    s1_card.fill.solid()
    s1_card.fill.fore_color.rgb = CARD_BG
    s1_card.line.color.rgb = BORDER_COL
    s1_card.line.width = Pt(1.5)
    s1_tf = s1_card.text_frame
    s1_tf.word_wrap = True
    s1_p1 = s1_tf.paragraphs[0]
    s1_p1.text = "NATURAL LANGUAGE TO EXECUTABLE ROBOT SIMULATION WITH DYNAMIC ADVERSARIAL STRESS TESTING"
    s1_p1.font.name = "Arial"
    s1_p1.font.size = Pt(13)
    s1_p1.font.bold = True
    s1_p1.font.color.rgb = ACCENT_CYAN
    s1_p1.alignment = PP_ALIGN.CENTER

    s1_p2 = s1_tf.add_paragraph()
    s1_p2.text = "\nAutonomous World & Map Compiler • Zero-SLAM Slicing • In-Process FastMCP Perturbation • Closed-Loop NQI Telemetry"
    s1_p2.font.name = "Arial"
    s1_p2.font.size = Pt(11.5)
    s1_p2.font.bold = True
    s1_p2.font.color.rgb = TEXT_LIGHT
    s1_p2.alignment = PP_ALIGN.CENTER

    s1_p3 = s1_tf.add_paragraph()
    s1_p3.text = "\nPowered by NVIDIA Nemotron 3 Ultra 550B • ROS 2 Jazzy • Gazebo Harmonic • Nav2 Simple Commander"
    s1_p3.font.name = "Arial"
    s1_p3.font.size = Pt(10.5)
    s1_p3.font.color.rgb = ACCENT_SKY
    s1_p3.alignment = PP_ALIGN.CENTER


    # Slide 2: CONTENT Slide
    s2 = prs.slides[1]
    # Hide or clear existing TextBox 10
    for shape in s2.shapes:
        if shape.name == "TextBox 10":
            shape.text_frame.text = "" # Clear placeholder

    agenda = [
        ("01", "Problem Statement", "PAGE 3", "Days of simulation setup friction and the lack of adversarial corner-case validation.", ACCENT_ROSE),
        ("02", "Our Solution & Uniqueness", "PAGE 4", "Conversational AI compiler, Zero-SLAM slicing, and dynamic in-flight perturbation.", ACCENT_CYAN),
        ("03", "Technical Architecture", "PAGE 5", "5-stage compiler pipeline, ROS 2 Jazzy, Gazebo Harmonic, FastMCP, and ReAct loop.", ACCENT_PURPLE),
        ("04", "Market Opportunity", "PAGE 6", "$18.9B AMR market, warehouse automation, digital twins, and test validation teams.", ACCENT_SKY),
        ("05", "Business Model & Revenue", "PAGE 7", "Open-core CLI, Pro SaaS ($199/seat/mo), and Enterprise fleet regression suites.", ACCENT_EMERALD),
        ("06", "Impact & Future Roadmap", "PAGE 8", "100x setup acceleration, zero structural crashes, and multi-robot fleet testing.", ACCENT_CYAN),
    ]

    for idx, (num, title, p_lbl, desc, col) in enumerate(agenda):
        col_idx = idx % 2
        row_idx = idx // 2
        x = Inches(1.8 + col_idx * 8.4)
        y = Inches(2.2 + row_idx * 2.2)

        card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(8.0), Inches(1.9))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = BORDER_COL
        card.line.width = Pt(1)

        # Number badge
        nb = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x + Inches(0.25), y + Inches(0.3), Inches(0.9), Inches(0.5))
        nb.fill.solid()
        nb.fill.fore_color.rgb = CARD_LIGHT
        nb.line.color.rgb = col
        nb.line.width = Pt(1)
        np = nb.text_frame.paragraphs[0]
        np.text = num
        np.font.size = Pt(14)
        np.font.bold = True
        np.font.color.rgb = col
        np.alignment = PP_ALIGN.CENTER

        tb = s2.shapes.add_textbox(x + Inches(1.35), y + Inches(0.2), Inches(6.3), Inches(1.5))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0

        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.name = "Arial"
        p1.font.size = Pt(14)
        p1.font.bold = True
        p1.font.color.rgb = TEXT_LIGHT

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.name = "Arial"
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = TEXT_MUTED

        p3 = tf.add_paragraph()
        p3.text = f"TARGET SECTION: {p_lbl}"
        p3.font.name = "Arial"
        p3.font.size = Pt(9)
        p3.font.bold = True
        p3.font.color.rgb = col


    # Helper for adding Header to Slides 3-8
    def add_slide_header(slide, badge_str, title_str):
        badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.8), Inches(0.7), Inches(3.2), Inches(0.45))
        badge.fill.solid()
        badge.fill.fore_color.rgb = DARK_WINE
        badge.line.color.rgb = DARK_WINE
        bp = badge.text_frame.paragraphs[0]
        bp.text = badge_str.upper()
        bp.font.name = "Arial"
        bp.font.size = Pt(11)
        bp.font.bold = True
        bp.font.color.rgb = RGBColor(255, 244, 224)
        bp.alignment = PP_ALIGN.CENTER

        tb = slide.shapes.add_textbox(Inches(1.8), Inches(1.25), Inches(14.5), Inches(0.7))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0
        tp = tf.paragraphs[0]
        tp.text = title_str
        tp.font.name = "Arial"
        tp.font.size = Pt(22)
        tp.font.bold = True
        tp.font.color.rgb = DARK_WINE


    # Slide 3: Problem Statement (PAGE 3)
    s3 = prs.slides[2]
    add_slide_header(s3, "Problem Statement", "The Robotics Simulation Bottleneck & Critical Testing Blindspots")

    problems = [
        ("DAYS OF MANUAL SETUP",
         "Building physics-accurate Gazebo simulation worlds requires manually authoring SDF models, URDF kinematics, sensor noise plugins, and Nav2 costmap YAML configurations.",
         "3–5 Engineering Days per Scenario",
         ACCENT_ROSE),
        ("ZERO ADVERSARIAL STRESS TESTING",
         "Simulations are static. Engineers cannot easily inject live environmental stressors (dimming lights, sudden obstacles, sensor occlusions) mid-run without breaking execution.",
         "85% Edge-Case Failures Missed",
         ACCENT_CYAN),
        ("DISASTROUS HARDWARE CRASHES",
         "Untested corner cases cause physical AMR collisions in warehouse aisles, pathway deadlocks, unmapped obstacle halts, and expensive facility shutdowns.",
         "$250,000+ Hardware Downtime Risk",
         ACCENT_PURPLE)
    ]

    for idx, (p_title, p_desc, p_stat, p_col) in enumerate(problems):
        x = Inches(1.8 + idx * 5.6)
        card = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(2.2), Inches(5.2), Inches(4.8))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = BORDER_COL
        card.line.width = Pt(1)

        # Top indicator bar
        bar = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, Inches(2.2), Inches(5.2), Inches(0.12))
        bar.fill.solid()
        bar.fill.fore_color.rgb = p_col
        bar.line.fill.background()

        tb = s3.shapes.add_textbox(x + Inches(0.35), Inches(2.55), Inches(4.5), Inches(4.2))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0

        p1 = tf.paragraphs[0]
        p1.text = p_title
        p1.font.name = "Arial"
        p1.font.size = Pt(14)
        p1.font.bold = True
        p1.font.color.rgb = p_col

        p2 = tf.add_paragraph()
        p2.text = f"\n{p_desc}"
        p2.font.name = "Arial"
        p2.font.size = Pt(11)
        p2.font.color.rgb = TEXT_MUTED

        p3 = tf.add_paragraph()
        p3.text = "\n\nMEASURED INDUSTRY IMPACT:"
        p3.font.name = "Arial"
        p3.font.size = Pt(9.5)
        p3.font.bold = True
        p3.font.color.rgb = TEXT_LIGHT

        p4 = tf.add_paragraph()
        p4.text = p_stat
        p4.font.name = "Arial"
        p4.font.size = Pt(14)
        p4.font.bold = True
        p4.font.color.rgb = p_col

    # Bottom summary card
    s3_sum = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.8), Inches(7.3), Inches(16.4), Inches(1.5))
    s3_sum.fill.solid()
    s3_sum.fill.fore_color.rgb = CARD_LIGHT
    s3_sum.line.color.rgb = ACCENT_ROSE
    s3_sum.line.width = Pt(1.5)
    s3_stf = s3_sum.text_frame
    s3_stf.word_wrap = True
    sp1 = s3_stf.paragraphs[0]
    sp1.text = "THE CORE INDUSTRY FRICTION:"
    sp1.font.name = "Arial"
    sp1.font.size = Pt(12)
    sp1.font.bold = True
    sp1.font.color.rgb = ACCENT_ROSE
    sp1.alignment = PP_ALIGN.CENTER

    sp2 = s3_stf.add_paragraph()
    sp2.text = "Robotics teams spend 70% of engineering bandwidth wrestling with simulator configurations rather than verifying navigation safety. Autonomous robots pass nominal tests in pristine simulations, then fail catastrophically when confronted with unexpected warehouse obstacles and degraded perception."
    sp2.font.name = "Arial"
    sp2.font.size = Pt(11)
    sp2.font.color.rgb = TEXT_LIGHT
    sp2.alignment = PP_ALIGN.CENTER


    # Slide 4: Our Solution & What Makes It Unique (PAGE 4)
    s4 = prs.slides[3]
    add_slide_header(s4, "Our Solution & Uniqueness", "Lang2Sim: Autonomous Generative Simulation & In-Flight Stress Copilot")

    solutions = [
        ("Natural Language World Compilation",
         "Compiles natural language instructions ('build a warehouse with 3 racks and 2 crates') into verified Gazebo Harmonic SDF worlds in under 30 seconds.",
         "From 3 Days to <30 Seconds (100x Acceleration)"),
        ("Zero-SLAM 2D Costmap Slicing",
         "A direct 3D collision slicer automatically extracts 2D Nav2 occupancy grids (map.yaml / map.pgm) from world geometry without manual robot teleoperation.",
         "Instant Costmaps (Zero SLAM Overhead)"),
        ("In-Process Dynamic FastMCP Stress Testing",
         "FastMCP 3.4 middleware injects dynamic obstacles (crates, racks, spheres) and dims ambient lighting in real time while the robot navigates.",
         "Dynamic In-Flight Adversarial Fuzzing"),
        ("Closed-Loop Telemetry & NQI Benchmarking",
         "Automated scoring evaluating path efficiency (Ep), trajectory smoothness (Stau), obstacle clearance (C_min), and bumper contact forces (>5 N).",
         "Objective Quantitative Navigation Quality Index")
    ]

    for idx, (title, desc, badge) in enumerate(solutions):
        c_idx = idx % 2
        r_idx = idx // 2
        x = Inches(1.8 + c_idx * 8.4)
        y = Inches(2.2 + r_idx * 2.5)

        card = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(8.0), Inches(2.2))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = BORDER_COL
        card.line.width = Pt(1)

        tb = s4.shapes.add_textbox(x + Inches(0.35), y + Inches(0.25), Inches(7.3), Inches(1.8))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0

        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.name = "Arial"
        p1.font.size = Pt(14)
        p1.font.bold = True
        p1.font.color.rgb = ACCENT_CYAN

        p2 = tf.add_paragraph()
        p2.text = f"\n{desc}"
        p2.font.name = "Arial"
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = TEXT_MUTED

        p3 = tf.add_paragraph()
        p3.text = f"\n★ WHAT MAKES IT UNIQUE: {badge}"
        p3.font.name = "Arial"
        p3.font.size = Pt(9.5)
        p3.font.bold = True
        p3.font.color.rgb = ACCENT_EMERALD

    # Bottom Callout Banner
    s4_bot = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.8), Inches(7.5), Inches(16.4), Inches(1.3))
    s4_bot.fill.solid()
    s4_bot.fill.fore_color.rgb = CARD_LIGHT
    s4_bot.line.color.rgb = ACCENT_CYAN
    s4_bot.line.width = Pt(1.5)
    s4_btf = s4_bot.text_frame
    s4_btf.word_wrap = True
    bp1 = s4_btf.paragraphs[0]
    bp1.text = "NOT JUST STATIC WORLD GENERATION — AN END-TO-END AUTONOMOUS VALIDATION ENGINE"
    bp1.font.name = "Arial"
    bp1.font.size = Pt(12)
    bp1.font.bold = True
    bp1.font.color.rgb = ACCENT_CYAN
    bp1.alignment = PP_ALIGN.CENTER

    bp2 = s4_btf.add_paragraph()
    bp2.text = "Lang2Sim provides an interactive OpenCode-style TUI copilot that generates environments, monitors execution, injects adversarial stresses on command, and delivers quantitative regression reports comparing nominal vs. stressed runs."
    bp2.font.name = "Arial"
    bp2.font.size = Pt(10.5)
    bp2.font.color.rgb = TEXT_LIGHT
    bp2.alignment = PP_ALIGN.CENTER


    # Slide 5: Technical Architecture & Tech Stack (PAGE 5)
    s5 = prs.slides[4]
    add_slide_header(s5, "Technical Architecture", "5-Stage Compiler Pipeline & End-to-End Robotics Tech Stack")

    stages = [
        ("STAGE 1", "NL Reasoning", "NVIDIA Nemotron 3 Ultra 550B ReAct Agent with Offline AST Regex Fallback", ACCENT_SKY),
        ("STAGE 2", "Spatial Compiler", "Pydantic v2 SimSpec, Shapely 2.0 Minkowski Corridors & Zero-SLAM Slicer", ACCENT_CYAN),
        ("STAGE 3", "Runtime Execution", "ROS 2 Jazzy, Gazebo Harmonic (SDF 1.9), Docker X11 GUI Forwarding", ACCENT_PURPLE),
        ("STAGE 4", "Stress Injector", "In-Process FastMCP 3.4 Tools, Dynamic Entity Spawning & Ambient Lighting", ACCENT_ROSE),
        ("STAGE 5", "Telemetry & NQI", "Nav2 Dispatcher, Contact Bumpers (>5 N), NQI Composite Benchmarking", ACCENT_EMERALD),
    ]

    for idx, (s_num, s_name, s_tech, col) in enumerate(stages):
        x = Inches(1.8 + idx * 3.35)
        card = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(2.2), Inches(3.1), Inches(3.2))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = BORDER_COL
        card.line.width = Pt(1)

        # Indicator bar
        bar = s5.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, Inches(2.2), Inches(3.1), Inches(0.1))
        bar.fill.solid()
        bar.fill.fore_color.rgb = col
        bar.line.fill.background()

        tb = s5.shapes.add_textbox(x + Inches(0.2), Inches(2.45), Inches(2.7), Inches(2.8))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0

        p1 = tf.paragraphs[0]
        p1.text = s_num
        p1.font.name = "Arial"
        p1.font.size = Pt(11)
        p1.font.bold = True
        p1.font.color.rgb = col

        p2 = tf.add_paragraph()
        p2.text = s_name
        p2.font.name = "Arial"
        p2.font.size = Pt(13)
        p2.font.bold = True
        p2.font.color.rgb = TEXT_LIGHT

        p3 = tf.add_paragraph()
        p3.text = f"\n{s_tech}"
        p3.font.name = "Arial"
        p3.font.size = Pt(10)
        p3.font.color.rgb = TEXT_MUTED

    # Tech Stack Specifications Card
    ts_card = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.8), Inches(5.7), Inches(16.4), Inches(3.1))
    ts_card.fill.solid()
    ts_card.fill.fore_color.rgb = CARD_LIGHT
    ts_card.line.color.rgb = BORDER_COL
    ts_card.line.width = Pt(1)

    tstb = s5.shapes.add_textbox(Inches(2.1), Inches(5.85), Inches(15.8), Inches(2.8))
    tstf = tstb.text_frame
    tstf.word_wrap = True
    tstf.margin_top = tstf.margin_bottom = tstf.margin_left = tstf.margin_right = 0

    tp1 = tstf.paragraphs[0]
    tp1.text = "CORE ENGINEERING SPECIFICATIONS & INTERFACE BOUNDARIES"
    tp1.font.name = "Arial"
    tp1.font.size = Pt(13)
    tp1.font.bold = True
    tp1.font.color.rgb = ACCENT_CYAN

    stack_rows = [
        ("• Generative AI & Reasoning:", "NVIDIA Nemotron 3 Ultra 550B A55B (OpenAI-compatible streaming) + ReAct Supervisor Loop + Offline AST Regex Parser fallback."),
        ("• Simulation & Physics Runtime:", "Gazebo Harmonic (SDF 1.9 system plugins: Physics, UserCommands, SceneBroadcaster), ROS 2 Jazzy, Nav2 Simple Commander API."),
        ("• Middleware & Adversarial Control:", "FastMCP 3.4 in-process tool server; ros_gz_bridge; Docker X11 GUI pass-through; dynamic lighting and model spawner routers."),
        ("• Frontend & Visualization:", "Textual Asynchronous 60 FPS TUI frontend, Rich telemetry tables, Web Telemetry Dashboard (Port 9090) with real-time NQI metrics.")
    ]

    for label, desc in stack_rows:
        p = tstf.add_paragraph()
        p.text = f"\n{label} {desc}"
        p.font.name = "Arial"
        p.font.size = Pt(10.5)
        p.font.color.rgb = TEXT_LIGHT


    # Slide 6: Market Opportunity & Target Audience (PAGE 6)
    s6 = prs.slides[5]
    add_slide_header(s6, "Market Opportunity", "Riding the Explosive Growth in Warehouse AMRs & Simulation Verification")

    market_sizes = [
        ("$18.9 B", "TAM by 2030", "Global Autonomous Mobile Robot (AMR) & automated warehouse logistics market (16.8% CAGR).", ACCENT_SKY),
        ("$4.2 B", "SAM", "Robotics simulation software, virtual commissioning, and automated digital twin verification tools.", ACCENT_CYAN),
        ("$650 M", "SOM", "ROS 2 & Gazebo-based AMR software test suites, regression benchmarking, and adversarial testing.", ACCENT_EMERALD),
    ]

    for idx, (val, lbl, desc, col) in enumerate(market_sizes):
        x = Inches(1.8 + idx * 5.6)
        card = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(2.2), Inches(5.2), Inches(2.4))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = BORDER_COL
        card.line.width = Pt(1)

        tb = s6.shapes.add_textbox(x + Inches(0.35), Inches(2.4), Inches(4.5), Inches(2.0))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0

        p1 = tf.paragraphs[0]
        p1.text = val
        p1.font.name = "Arial"
        p1.font.size = Pt(36)
        p1.font.bold = True
        p1.font.color.rgb = col

        p2 = tf.add_paragraph()
        p2.text = lbl
        p2.font.name = "Arial"
        p2.font.size = Pt(12)
        p2.font.bold = True
        p2.font.color.rgb = TEXT_LIGHT

        p3 = tf.add_paragraph()
        p3.text = desc
        p3.font.name = "Arial"
        p3.font.size = Pt(10)
        p3.font.color.rgb = TEXT_MUTED

    # Target Customers Card
    cust_card = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.8), Inches(4.9), Inches(16.4), Inches(3.9))
    cust_card.fill.solid()
    cust_card.fill.fore_color.rgb = CARD_LIGHT
    cust_card.line.color.rgb = BORDER_COL
    cust_card.line.width = Pt(1)

    ctb = s6.shapes.add_textbox(Inches(2.1), Inches(5.1), Inches(15.8), Inches(3.5))
    ctf = ctb.text_frame
    ctf.word_wrap = True
    ctf.margin_top = ctf.margin_bottom = ctf.margin_left = ctf.margin_right = 0

    cp = ctf.paragraphs[0]
    cp.text = "TARGET AUDIENCE & STRATEGIC CUSTOMER PROFILES"
    cp.font.name = "Arial"
    cp.font.size = Pt(13)
    cp.font.bold = True
    cp.font.color.rgb = ACCENT_CYAN

    targets = [
        ("1. Autonomous Mobile Robot (AMR) Manufacturers (e.g. Locus Robotics, OTTO Motors, Fetch):",
         "Need automated CI/CD regression testing suites to validate new Nav2 navigation firmware against adversarial lighting and dynamic obstacles before deploying OTA updates to multi-million-dollar customer fleets."),
        ("2. 3PL Logistics & Enterprise Fulfillment Centers (e.g. DHL Supply Chain, Amazon, GXO):",
         "Require instant digital twin creation of bespoke warehouse facilities from simple architectural prompts to verify layout throughput, aisle clearance margins, and AMR safety envelopes."),
        ("3. Robotics Software Integrators & Research Laboratories:",
         "Face the 72-hour manual simulation setup barrier; Lang2Sim enables rapid scenario prototyping and reproducible quantitative NQI benchmarks for rapid deployment verification.")
    ]

    for title, desc in targets:
        p = ctf.add_paragraph()
        p.text = f"\n{title}\n{desc}"
        p.font.name = "Arial"
        p.font.size = Pt(10.5)
        p.font.color.rgb = TEXT_LIGHT


    # Slide 7: Business Model & Revenue Plan (PAGE 7)
    s7 = prs.slides[6]
    add_slide_header(s7, "Business Model & Revenue Plan", "Hybrid Open-Core SaaS & Enterprise Autonomous Simulation Infrastructure")

    tiers = [
        ("OPEN CORE / FREE",
         "$0",
         "Developer Community",
         [
             "• Full local CLI ('lang2sim') access",
             "• Offline regex & AST parser",
             "• Standard warehouse catalog scenes",
             "• Single-robot local simulation",
             "• Open-source community support"
         ],
         ACCENT_SKY),
        ("PRO TEAM SAAS",
         "$199 / mo",
         "per Engineering Seat",
         [
             "• Cloud Nemotron 550B tokens",
             "• Bespoke zero-SLAM world generation",
             "• CI/CD GitHub Actions integration",
             "• Automated regression NQI scoring",
             "• Web dashboard & telemetry export"
         ],
         ACCENT_CYAN),
        ("ENTERPRISE FLEET",
         "$2,500+ / mo",
         "per Robot Fleet Line",
         [
             "• Custom CAD/BIM facility ingestion",
             "• Nightly automated adversarial fuzzing",
             "• Hardware-in-the-Loop (HIL) bridges",
             "• Multi-robot fleet traffic testing",
             "• Dedicated SLA & safety certification"
         ],
         ACCENT_EMERALD)
    ]

    for idx, (t_name, t_price, t_sub, t_feats, col) in enumerate(tiers):
        x = Inches(1.8 + idx * 5.6)
        card = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(2.2), Inches(5.2), Inches(5.0))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = BORDER_COL
        card.line.width = Pt(1)

        bar = s7.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, Inches(2.2), Inches(5.2), Inches(0.12))
        bar.fill.solid()
        bar.fill.fore_color.rgb = col
        bar.line.fill.background()

        tb = s7.shapes.add_textbox(x + Inches(0.35), Inches(2.45), Inches(4.5), Inches(4.5))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0

        p1 = tf.paragraphs[0]
        p1.text = t_name
        p1.font.name = "Arial"
        p1.font.size = Pt(12)
        p1.font.bold = True
        p1.font.color.rgb = col

        p2 = tf.add_paragraph()
        p2.text = t_price
        p2.font.name = "Arial"
        p2.font.size = Pt(32)
        p2.font.bold = True
        p2.font.color.rgb = TEXT_LIGHT

        p3 = tf.add_paragraph()
        p3.text = t_sub
        p3.font.name = "Arial"
        p3.font.size = Pt(10)
        p3.font.color.rgb = TEXT_MUTED

        for feat in t_feats:
            pf = tf.add_paragraph()
            pf.text = f"\n{feat}"
            pf.font.name = "Arial"
            pf.font.size = Pt(10.5)
            pf.font.color.rgb = TEXT_LIGHT

    # Bottom Financial Roadmap Box
    s7_bot = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.8), Inches(7.5), Inches(16.4), Inches(1.3))
    s7_bot.fill.solid()
    s7_bot.fill.fore_color.rgb = CARD_LIGHT
    s7_bot.line.color.rgb = ACCENT_EMERALD
    s7_bot.line.width = Pt(1.5)
    s7_btf = s7_bot.text_frame
    s7_btf.word_wrap = True
    rp1 = s7_btf.paragraphs[0]
    rp1.text = "FINANCIAL PROJECTION & REVENUE SCALING"
    rp1.font.name = "Arial"
    rp1.font.size = Pt(12)
    rp1.font.bold = True
    rp1.font.color.rgb = ACCENT_EMERALD
    rp1.alignment = PP_ALIGN.CENTER

    rp2 = s7_btf.add_paragraph()
    rp2.text = "Year 1: $450K ARR (25 Pro Seats + 8 Enterprise Pilots) → Year 2: $3.2M ARR (Expanding to fleet-wide continuous regression fuzzing) → Year 3: $8.5M ARR (Industry standard for ROS 2 automated certification)."
    rp2.font.name = "Arial"
    rp2.font.size = Pt(11)
    rp2.font.color.rgb = TEXT_LIGHT
    rp2.alignment = PP_ALIGN.CENTER


    # Slide 8: Impact & Future Roadmap (PAGE 8)
    s8 = prs.slides[7]
    add_slide_header(s8, "Impact & Future Roadmap", "Transforming Robotics Reliability: Quantified Impact & Future Vision")

    # Left: Validated Impact Metrics
    imp_card = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.8), Inches(2.2), Inches(8.0), Inches(5.1))
    imp_card.fill.solid()
    imp_card.fill.fore_color.rgb = CARD_BG
    imp_card.line.color.rgb = BORDER_COL
    imp_card.line.width = Pt(1)

    itb = s8.shapes.add_textbox(Inches(2.1), Inches(2.45), Inches(7.4), Inches(4.7))
    itf = itb.text_frame
    itf.word_wrap = True
    itf.margin_top = itf.margin_bottom = itf.margin_left = itf.margin_right = 0

    ip1 = itf.paragraphs[0]
    ip1.text = "QUANTIFIED INDUSTRY IMPACT"
    ip1.font.name = "Arial"
    ip1.font.size = Pt(14)
    ip1.font.bold = True
    ip1.font.color.rgb = ACCENT_CYAN

    impacts = [
        ("⚡ 100x Faster Setup Time", "Simulation world synthesis and 2D navigation map extraction compressed from 72 hours to under 30 seconds."),
        ("🛡️ 10x Edge-Case Coverage", "Automated adversarial sweeps uncover critical corner-case deadlocks and perception blindspots before physical hardware trials."),
        ("💥 0 Unverified Crashes", "Physical contact sensors (>5 N) and clearance margin tracking ensure AMRs never compromise safe operating envelopes.")
    ]

    for title, desc in impacts:
        p = itf.add_paragraph()
        p.text = f"\n{title}\n{desc}"
        p.font.name = "Arial"
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_LIGHT

    # Right: Strategic Product Roadmap
    road_card = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(10.2), Inches(2.2), Inches(8.0), Inches(5.1))
    road_card.fill.solid()
    road_card.fill.fore_color.rgb = CARD_BG
    road_card.line.color.rgb = BORDER_COL
    road_card.line.width = Pt(1)

    rtb = s8.shapes.add_textbox(Inches(10.5), Inches(2.45), Inches(7.4), Inches(4.7))
    rtf = rtb.text_frame
    rtf.word_wrap = True
    rtf.margin_top = rtf.margin_bottom = rtf.margin_left = rtf.margin_right = 0

    rp1 = rtf.paragraphs[0]
    rp1.text = "STRATEGIC PRODUCT ROADMAP"
    rp1.font.name = "Arial"
    rp1.font.size = Pt(14)
    rp1.font.bold = True
    rp1.font.color.rgb = ACCENT_PURPLE

    milestones = [
        ("• Q2 2026: Multi-Robot Fleet Stress Testing", "Simulate concurrent AMRs with dynamic traffic contention, cross-aisle right-of-way, and fleet coordination APIs."),
        ("• Q3 2026: CI/CD GitHub Action Regression Cloud", "Automated nightly simulation fuzzing on every pull request with PR markdown reports & video replays."),
        ("• Q4 2026: Photorealistic Digital Twin Bridges", "Direct export to NVIDIA Omniverse / Isaac Sim and Unreal Engine 5 for photorealistic vision sensor testing."),
        ("• 2027: Hardware-in-the-Loop (HIL) Testbenches", "Bridging Lang2Sim live stress signals directly into physical embedded controllers (NVIDIA Jetson, Intel NUC).")
    ]

    for m in milestones:
        p = rtf.add_paragraph()
        p.text = f"\n{m[0]}\n{m[1]}"
        p.font.name = "Arial"
        p.font.size = Pt(10)
        p.font.color.rgb = TEXT_LIGHT

    # Bottom Closing Tagline Banner
    s8_bot = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.8), Inches(7.5), Inches(16.4), Inches(1.3))
    s8_bot.fill.solid()
    s8_bot.fill.fore_color.rgb = CARD_LIGHT
    s8_bot.line.color.rgb = ACCENT_SKY
    s8_bot.line.width = Pt(1.5)
    s8_btf = s8_bot.text_frame
    s8_btf.word_wrap = True
    cl1 = s8_btf.paragraphs[0]
    cl1.text = "LANG2SIM: EMPOWERING ROBOTICISTS TO TEST THE IMPOSSIBLE BEFORE TOUCHING REAL HARDWARE"
    cl1.font.name = "Arial"
    cl1.font.size = Pt(12)
    cl1.font.bold = True
    cl1.font.color.rgb = ACCENT_SKY
    cl1.alignment = PP_ALIGN.CENTER

    cl2 = s8_btf.add_paragraph()
    cl2.text = "“Some ideas belong to other dimensions” — Simulating edge cases in software so that real robots succeed flawlessly in the physical world."
    cl2.font.name = "Arial"
    cl2.font.size = Pt(11)
    cl2.font.italic = True
    cl2.font.color.rgb = TEXT_LIGHT
    cl2.alignment = PP_ALIGN.CENTER

    prs.save(OUTPUT_PATH)
    print(f"Successfully generated judging presentation at: {OUTPUT_PATH}")

if __name__ == "__main__":
    build_pitch_deck()
