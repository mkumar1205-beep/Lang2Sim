import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_deck(filename="Lang2Sim_Judging_Pitch.pptx"):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Colors
    BG_DARK = RGBColor(11, 15, 25)        # #0B0F19 deep slate
    CARD_BG = RGBColor(22, 30, 49)        # #161E31 card dark
    CARD_BORDER = RGBColor(37, 51, 82)    # #253352 card border
    ACCENT_CYAN = RGBColor(0, 210, 255)   # #00D2FF neon cyan
    ACCENT_BLUE = RGBColor(56, 189, 248)  # #38BDF8 sky blue
    ACCENT_PURPLE = RGBColor(129, 140, 248) # #818CF8 indigo
    TEXT_WHITE = RGBColor(248, 250, 252)  # #F8FAFC
    TEXT_MUTED = RGBColor(148, 163, 184)  # #94A3B8 slate
    TEXT_DIM = RGBColor(100, 116, 139)    # #64748B
    ACCENT_GREEN = RGBColor(16, 185, 129) # #10B981 emerald
    ACCENT_ROSE = RGBColor(244, 63, 94)   # #F43F5E rose
    CARD_LIGHT = RGBColor(30, 41, 59)     # #1E293B

    def set_slide_bg(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_DARK
        bg.line.fill.background()
        return bg

    def add_header(slide, badge_text, title_text, page_num=None):
        # Category Badge
        badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.5), Inches(2.2), Inches(0.35))
        badge.fill.solid()
        badge.fill.fore_color.rgb = RGBColor(15, 35, 60)
        badge.line.color.rgb = ACCENT_CYAN
        badge.line.width = Pt(1)
        tf = badge.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = badge_text.upper()
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = ACCENT_CYAN
        p.alignment = PP_ALIGN.CENTER

        # Slide Page Number (Right side)
        if page_num:
            p_box = slide.shapes.add_textbox(Inches(11.5), Inches(0.45), Inches(1.0), Inches(0.4))
            p_tf = p_box.text_frame
            p_p = p_tf.paragraphs[0]
            p_p.text = f"PAGE {page_num}"
            p_p.font.size = Pt(11)
            p_p.font.bold = True
            p_p.font.color.rgb = ACCENT_BLUE
            p_p.alignment = PP_ALIGN.RIGHT

        # Title
        t_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.9), Inches(11.7), Inches(0.65))
        t_tf = t_box.text_frame
        t_tf.word_wrap = True
        t_tf.margin_left = t_tf.margin_right = t_tf.margin_top = t_tf.margin_bottom = 0
        tp = t_tf.paragraphs[0]
        tp.text = title_text
        tp.font.size = Pt(22)
        tp.font.bold = True
        tp.font.color.rgb = TEXT_WHITE

    # -------------------------------------------------------------
    # SLIDE 1: Title Slide
    # -------------------------------------------------------------
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s1)

    # Quote banner at top
    q_box = s1.shapes.add_textbox(Inches(0.8), Inches(0.6), Inches(11.7), Inches(0.5))
    q_tf = q_box.text_frame
    qp = q_tf.paragraphs[0]
    qp.text = "“Some ideas belong to other dimensions”"
    qp.font.size = Pt(14)
    qp.font.italic = True
    qp.font.color.rgb = ACCENT_CYAN
    qp.alignment = PP_ALIGN.CENTER

    # Project Title Box
    title_box = s1.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(11.7), Inches(1.3))
    t_tf = title_box.text_frame
    tp = t_tf.paragraphs[0]
    tp.text = "Lang2Sim"
    tp.font.size = Pt(56)
    tp.font.bold = True
    tp.font.color.rgb = TEXT_WHITE
    tp.alignment = PP_ALIGN.CENTER

    # Subtitle / Category
    sub_badge = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.5), Inches(2.9), Inches(4.333), Inches(0.45))
    sub_badge.fill.solid()
    sub_badge.fill.fore_color.rgb = RGBColor(16, 42, 77)
    sub_badge.line.color.rgb = ACCENT_BLUE
    sub_badge.line.width = Pt(1)
    sbtf = sub_badge.text_frame
    sbp = sbtf.paragraphs[0]
    sbp.text = "SOFTWARE PLATFORM | ROBOTICS SIMULATION"
    sbp.font.size = Pt(12)
    sbp.font.bold = True
    sbp.font.color.rgb = ACCENT_CYAN
    sbp.alignment = PP_ALIGN.CENTER

    desc_box = s1.shapes.add_textbox(Inches(1.5), Inches(3.6), Inches(10.333), Inches(0.9))
    d_tf = desc_box.text_frame
    d_tf.word_wrap = True
    dp = d_tf.paragraphs[0]
    dp.text = "Natural Language to Executable 3D Robot Simulation with Autonomous Adversarial Stress Testing"
    dp.font.size = Pt(18)
    dp.font.color.rgb = TEXT_MUTED
    dp.alignment = PP_ALIGN.CENTER

    # Center card: Highlights
    hl_card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(2.2), Inches(4.7), Inches(8.933), Inches(1.4))
    hl_card.fill.solid()
    hl_card.fill.fore_color.rgb = CARD_BG
    hl_card.line.color.rgb = CARD_BORDER
    hl_card.line.width = Pt(1)
    hltf = hl_card.text_frame
    hltf.word_wrap = True
    
    hp1 = hltf.paragraphs[0]
    hp1.text = "Autonomous Compiler • Zero-SLAM Costmap Slicing • In-Process FastMCP Perturbation • Closed-Loop NQI Telemetry"
    hp1.font.size = Pt(13)
    hp1.font.bold = True
    hp1.font.color.rgb = ACCENT_BLUE
    hp1.alignment = PP_ALIGN.CENTER

    hp2 = hltf.add_paragraph()
    hp2.text = "Powered by NVIDIA Nemotron 3 Ultra 550B • ROS 2 Jazzy • Gazebo Harmonic • Nav2 Simple Commander"
    hp2.font.size = Pt(11)
    hp2.font.color.rgb = TEXT_DIM
    hp2.alignment = PP_ALIGN.CENTER

    # Team Name footer
    team_box = s1.shapes.add_textbox(Inches(0.8), Inches(6.4), Inches(11.7), Inches(0.5))
    ttf = team_box.text_frame
    tp = ttf.paragraphs[0]
    tp.text = "Presented by Team Lang2Sim | Judging Round 2026"
    tp.font.size = Pt(13)
    tp.font.bold = True
    tp.font.color.rgb = TEXT_WHITE
    tp.alignment = PP_ALIGN.CENTER

    # -------------------------------------------------------------
    # SLIDE 2: Table of Contents (PAGE 2)
    # -------------------------------------------------------------
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s2)
    add_header(s2, "AGENDA", "CONTENT & PRESENTATION ROADMAP", page_num=2)

    agenda_items = [
        ("01", "PAGE 3", "Problem Statement", "The multi-day bottleneck in robotics simulation & untested corner-case crashes."),
        ("02", "PAGE 4", "Our Solution & What Makes It Unique", "Conversational AI compiler, Zero-SLAM slicing, and dynamic adversarial injection."),
        ("03", "PAGE 5", "Technical Architecture & Tech Stack", "5-stage compiler, ROS 2 Jazzy, Gazebo Harmonic, FastMCP, and ReAct supervisor."),
        ("04", "PAGE 6", "Market Opportunity & Target Audience", "$18.9B AMR market, warehouse automation, digital twins, and test validation teams."),
        ("05", "PAGE 7", "Business Model & Revenue Plan", "Open-core CLI, Pro SaaS ($199/seat), and Enterprise fleet regression suites."),
        ("06", "PAGE 8", "Impact & Future Roadmap", "100x setup acceleration, 0 structural crashes, and multi-robot fleet roadmap.")
    ]

    for idx, (num, page_lbl, title, desc) in enumerate(agenda_items):
        row = idx // 2
        col = idx % 2
        x = Inches(0.8 + col * 5.95)
        y = Inches(1.8 + row * 1.65)
        
        card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(5.7), Inches(1.4))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = CARD_BORDER
        card.line.width = Pt(1)

        # Number badge inside card
        num_box = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, x + Inches(0.2), y + Inches(0.25), Inches(0.85), Inches(0.4))
        num_box.fill.solid()
        num_box.fill.fore_color.rgb = RGBColor(16, 42, 77)
        num_box.line.color.rgb = ACCENT_CYAN
        ntf = num_box.text_frame
        np = ntf.paragraphs[0]
        np.text = num
        np.font.size = Pt(14)
        np.font.bold = True
        np.font.color.rgb = ACCENT_CYAN
        np.alignment = PP_ALIGN.CENTER

        # Content text
        c_box = s2.shapes.add_textbox(x + Inches(1.2), y + Inches(0.15), Inches(4.3), Inches(1.1))
        ctf = c_box.text_frame
        ctf.word_wrap = True
        ctf.margin_top = ctf.margin_bottom = ctf.margin_left = ctf.margin_right = 0

        p1 = ctf.paragraphs[0]
        p1.text = title
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = TEXT_WHITE

        p2 = ctf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(10)
        p2.font.color.rgb = TEXT_MUTED

        p3 = ctf.add_paragraph()
        p3.text = page_lbl
        p3.font.size = Pt(9)
        p3.font.bold = True
        p3.font.color.rgb = ACCENT_PURPLE

    # -------------------------------------------------------------
    # SLIDE 3: Problem Statement (PAGE 3)
    # -------------------------------------------------------------
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s3)
    add_header(s3, "PROBLEM STATEMENT", "THE ROBOTICS SIMULATION BOTTLENECK & CRITICAL TESTING BLINDSPOT", page_num=3)

    problems = [
        ("DAYS OF MANUAL SETUP",
         "Building physics-accurate Gazebo worlds requires writing SDF models, URDF kinematics, sensor noise plugins, and ROS 2 launch scripts by hand.",
         "3–5 Engineering Days per Scenario",
         ACCENT_ROSE),
        ("ZERO DYNAMIC ADVERSARIAL TESTING",
         "Simulations are static. Engineers cannot easily inject live environmental stresses (dimming lights, sudden obstacles, sensor occlusions) mid-run.",
         "85% Edge-Case Failures Missed",
         ACCENT_CYAN),
        ("CATASTROPHIC REAL-WORLD DEPLOYMENT",
         "Untested corner cases lead to warehouse AMR collisions, unmapped obstacles causing deadlocks, and costly emergency shutdowns.",
         "$250,000+ Hardware Downtime Risk",
         ACCENT_PURPLE)
    ]

    for idx, (p_title, p_desc, p_stat, p_color) in enumerate(problems):
        x = Inches(0.8 + idx * 3.97)
        card = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.8), Inches(3.75), Inches(3.8))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = CARD_BORDER
        card.line.width = Pt(1)

        # Top indicator bar
        bar = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, Inches(1.8), Inches(3.75), Inches(0.1))
        bar.fill.solid()
        bar.fill.fore_color.rgb = p_color
        bar.line.fill.background()

        tb = s3.shapes.add_textbox(x + Inches(0.25), Inches(2.1), Inches(3.25), Inches(3.3))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0

        p1 = tf.paragraphs[0]
        p1.text = p_title
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = p_color

        p2 = tf.add_paragraph()
        p2.text = "\n" + p_desc
        p2.font.size = Pt(11)
        p2.font.color.rgb = TEXT_MUTED

        p3 = tf.add_paragraph()
        p3.text = "\n\nCRITICAL IMPACT:"
        p3.font.size = Pt(9)
        p3.font.bold = True
        p3.font.color.rgb = TEXT_DIM

        p4 = tf.add_paragraph()
        p4.text = p_stat
        p4.font.size = Pt(12)
        p4.font.bold = True
        p4.font.color.rgb = TEXT_WHITE

    # Bottom summary box
    sum_box = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.9), Inches(11.7), Inches(0.95))
    sum_box.fill.solid()
    sum_box.fill.fore_color.rgb = CARD_LIGHT
    sum_box.line.color.rgb = ACCENT_ROSE
    sum_box.line.width = Pt(1)
    stf = sum_box.text_frame
    stf.word_wrap = True
    sp = stf.paragraphs[0]
    sp.text = "CORE FRICTION: Robotics teams spend 70% of engineering time wrestling simulator configs instead of validating autonomy."
    sp.font.size = Pt(11)
    sp.font.bold = True
    sp.font.color.rgb = TEXT_WHITE
    sp.alignment = PP_ALIGN.CENTER

    sp2 = stf.add_paragraph()
    sp2.text = "Robots pass nominal tests in pristine simulations, then fail catastrophically under real warehouse lighting and unexpected dynamic obstacles."
    sp2.font.size = Pt(10)
    sp2.font.color.rgb = TEXT_MUTED
    sp2.alignment = PP_ALIGN.CENTER

    # -------------------------------------------------------------
    # SLIDE 4: Solution & What Makes It Unique (PAGE 4)
    # -------------------------------------------------------------
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s4)
    add_header(s4, "OUR SOLUTION", "LANG2SIM: NATURAL LANGUAGE ROBOT SIMULATION & ADVERSARIAL STRESS COPILOT", page_num=4)

    solutions = [
        ("Natural Language World Compilation",
         "Transforms plain English instructions into physics-verified Gazebo Harmonic .sdf worlds in under 30 seconds, eliminating manual XML/SDF coding.",
         "From 3 Days to <30 Seconds"),
        ("Zero-SLAM 2D Costmap Slicing",
         "Direct 3D geometry collision slicer automatically extracts 2D Nav2 occupancy grids (map.yaml / map.pgm) without teleoperating the robot.",
         "Instant Costmaps (0 SLAM Overhead)"),
        ("Live In-Process Stress Injection",
         "FastMCP 3.4 middleware injects dynamic obstacles (crates, racks, spheres) and dims ambient lighting mid-run while the robot navigates.",
         "Sub-Second Runtime Perturbation"),
        ("Closed-Loop Telemetry & NQI Scoring",
         "Automated scoring measuring path length, trajectory jerk, obstacle clearance margin (C_min), and bumper contact forces.",
         "Objective Quantitative Benchmarks")
    ]

    for idx, (s_title, s_desc, s_badge) in enumerate(solutions):
        col = idx % 2
        row = idx // 2
        x = Inches(0.8 + col * 5.95)
        y = Inches(1.8 + row * 2.1)

        card = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(5.7), Inches(1.85))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = CARD_BORDER
        card.line.width = Pt(1)

        tb = s4.shapes.add_textbox(x + Inches(0.25), y + Inches(0.15), Inches(5.2), Inches(1.55))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0

        p1 = tf.paragraphs[0]
        p1.text = s_title
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = ACCENT_CYAN

        p2 = tf.add_paragraph()
        p2.text = s_desc
        p2.font.size = Pt(10)
        p2.font.color.rgb = TEXT_MUTED

        p3 = tf.add_paragraph()
        p3.text = "WHAT MAKES IT UNIQUE: " + s_badge
        p3.font.size = Pt(9)
        p3.font.bold = True
        p3.font.color.rgb = ACCENT_GREEN

    # Bottom Uniqueness Banner
    u_box = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(6.15), Inches(11.7), Inches(0.75))
    u_box.fill.solid()
    u_box.fill.fore_color.rgb = CARD_LIGHT
    u_box.line.color.rgb = ACCENT_CYAN
    u_box.line.width = Pt(1)
    utf = u_box.text_frame
    utf.word_wrap = True
    up = utf.paragraphs[0]
    up.text = "NOT JUST WORLD GENERATION — AN END-TO-END AUTOMATED STRESS-TESTING & BENCHMARKING COPILOT"
    up.font.size = Pt(11)
    up.font.bold = True
    up.font.color.rgb = TEXT_WHITE
    up.alignment = PP_ALIGN.CENTER

    # -------------------------------------------------------------
    # SLIDE 5: Technical Architecture & Tech Stack (PAGE 5)
    # -------------------------------------------------------------
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s5)
    add_header(s5, "TECHNICAL ARCHITECTURE", "5-STAGE COMPILER PIPELINE & ROBUST TECH STACK", page_num=5)

    stages = [
        ("STAGE 1", "NL Reasoning", "Nemotron 3 550B\nReAct Agent Loop\nOffline AST Parser", ACCENT_BLUE),
        ("STAGE 2", "Geometry Compiler", "Shapely 2.0 OBB\nMinkowski Corridors\nZero-SLAM Slicer", ACCENT_CYAN),
        ("STAGE 3", "Runtime Launch", "ROS 2 Jazzy\nGazebo Harmonic\nDocker X11 GUI", ACCENT_PURPLE),
        ("STAGE 4", "Stress Injector", "FastMCP 3.4 Bridge\nDynamic Spawner\nLighting Controls", ACCENT_ROSE),
        ("STAGE 5", "Telemetry & NQI", "Nav2 Dispatcher\nBumper Sensors\nBenchmark Scorer", ACCENT_GREEN),
    ]

    for idx, (s_num, s_name, s_tech, s_col) in enumerate(stages):
        x = Inches(0.8 + idx * 2.38)
        card = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.8), Inches(2.2), Inches(2.6))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = CARD_BORDER
        card.line.width = Pt(1)

        # Top indicator bar
        bar = s5.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, Inches(1.8), Inches(2.2), Inches(0.08))
        bar.fill.solid()
        bar.fill.fore_color.rgb = s_col
        bar.line.fill.background()

        tb = s5.shapes.add_textbox(x + Inches(0.15), Inches(2.0), Inches(1.9), Inches(2.3))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0

        p1 = tf.paragraphs[0]
        p1.text = s_num
        p1.font.size = Pt(10)
        p1.font.bold = True
        p1.font.color.rgb = s_col

        p2 = tf.add_paragraph()
        p2.text = s_name
        p2.font.size = Pt(11)
        p2.font.bold = True
        p2.font.color.rgb = TEXT_WHITE

        p3 = tf.add_paragraph()
        p3.text = "\n" + s_tech
        p3.font.size = Pt(9)
        p3.font.color.rgb = TEXT_MUTED

    # Tech Stack Summary Grid below
    ts_card = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.6), Inches(11.7), Inches(2.3))
    ts_card.fill.solid()
    ts_card.fill.fore_color.rgb = CARD_LIGHT
    ts_card.line.color.rgb = CARD_BORDER
    ts_card.line.width = Pt(1)

    tstb = s5.shapes.add_textbox(Inches(1.0), Inches(4.75), Inches(11.3), Inches(2.0))
    tstf = tstb.text_frame
    tstf.word_wrap = True
    tstf.margin_top = tstf.margin_bottom = tstf.margin_left = tstf.margin_right = 0

    tp1 = tstf.paragraphs[0]
    tp1.text = "CORE TECHNOLOGY STACK SPECIFICATION"
    tp1.font.size = Pt(11)
    tp1.font.bold = True
    tp1.font.color.rgb = ACCENT_CYAN

    stack_rows = [
        ("• AI & Reasoning Engine:", "NVIDIA Nemotron 3 Ultra 550B A55B (via OpenAI-compatible API) + Deterministic Offline AST Regex Fallback"),
        ("• Simulation & Physics:", "Gazebo Harmonic (SDF 1.9/1.10 system plugins), ROS 2 Jazzy, Nav2 Simple Commander, TurtleBot3/TurtleBot4"),
        ("• Middleware & Protocol:", "FastMCP 3.4 for dynamic in-process model injection & lighting mutations, ros_gz_bridge, Docker X11 GUI"),
        ("• Frontend & Interface:", "Textual Full-Screen Asynchronous TUI (60 FPS event loop), Rich terminal tables, Web Dashboard (Port 9090)")
    ]

    for label, val in stack_rows:
        p = tstf.add_paragraph()
        p.text = f"{label} {val}"
        p.font.size = Pt(10)
        p.font.color.rgb = TEXT_WHITE

    # -------------------------------------------------------------
    # SLIDE 6: Market Opportunity & Target Audience (PAGE 6)
    # -------------------------------------------------------------
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s6)
    add_header(s6, "MARKET OPPORTUNITY", "EXPANDING WAREHOUSE AUTOMATION & AUTONOMOUS AMR VERIFICATION", page_num=6)

    # Market Sizing Cards
    m_cards = [
        ("$18.9 B", "TAM by 2030", "Global Autonomous Mobile Robot (AMR) & Warehouse Automation market growing at 16.8% CAGR.", ACCENT_BLUE),
        ("$4.2 B", "SAM", "Robotics simulation software, virtual commissioning, and automated digital twin validation tools.", ACCENT_CYAN),
        ("$650 M", "SOM", "ROS 2 and Gazebo-based AMR software test suites, regression benchmarking, and stress-testing tools.", ACCENT_PURPLE),
    ]

    for idx, (m_val, m_label, m_desc, m_col) in enumerate(m_cards):
        x = Inches(0.8 + idx * 3.97)
        card = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.8), Inches(3.75), Inches(2.2))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = CARD_BORDER
        card.line.width = Pt(1)

        tb = s6.shapes.add_textbox(x + Inches(0.25), Inches(1.95), Inches(3.25), Inches(1.9))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0

        p1 = tf.paragraphs[0]
        p1.text = m_val
        p1.font.size = Pt(32)
        p1.font.bold = True
        p1.font.color.rgb = m_col

        p2 = tf.add_paragraph()
        p2.text = m_label
        p2.font.size = Pt(12)
        p2.font.bold = True
        p2.font.color.rgb = TEXT_WHITE

        p3 = tf.add_paragraph()
        p3.text = m_desc
        p3.font.size = Pt(10)
        p3.font.color.rgb = TEXT_MUTED

    # Target Customers Card
    cust_card = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.2), Inches(11.7), Inches(2.7))
    cust_card.fill.solid()
    cust_card.fill.fore_color.rgb = CARD_LIGHT
    cust_card.line.color.rgb = CARD_BORDER
    cust_card.line.width = Pt(1)

    ctb = s6.shapes.add_textbox(Inches(1.0), Inches(4.35), Inches(11.3), Inches(2.4))
    ctf = ctb.text_frame
    ctf.word_wrap = True
    ctf.margin_top = ctf.margin_bottom = ctf.margin_left = ctf.margin_right = 0

    cp = ctf.paragraphs[0]
    cp.text = "TARGET AUDIENCE & SEGMENT VALIDATION"
    cp.font.size = Pt(12)
    cp.font.bold = True
    cp.font.color.rgb = ACCENT_CYAN

    targets = [
        ("1. Warehouse AMR Manufacturers (e.g. Locus, OTTO, Fetch):", "Need rapid automated regression suites to validate Nav2 firmware releases against adversarial obstacles before shipping updates to physical fleets."),
        ("2. 3PL Logistics & Fulfillment Operators (e.g. DHL, Amazon, GXO):", "Require instant digital twin generation of bespoke customer warehouse layouts to verify robot route efficiency and safety clearances."),
        ("3. Industrial Robotics Startups & Research Labs:", "Struggle with the 72-hour simulation setup barrier; need rapid prototyping and reproducible quantitative NQI benchmarks for grant and deployment milestones.")
    ]

    for t_title, t_desc in targets:
        p = ctf.add_paragraph()
        p.text = f"\n{t_title}\n{t_desc}"
        p.font.size = Pt(10)
        p.font.color.rgb = TEXT_WHITE

    # -------------------------------------------------------------
    # SLIDE 7: Business Model & Revenue Plan (PAGE 7)
    # -------------------------------------------------------------
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s7)
    add_header(s7, "BUSINESS MODEL", "TIERED B2B SAAS & ENTERPRISE FLEET VALIDATION SUITES", page_num=7)

    tiers = [
        ("OPEN CORE / FREE",
         "$0",
         "Developer Community",
         [
             "• Local CLI ('lang2sim') install",
             "• Offline regex & AST parser",
             "• Standard warehouse catalog",
             "• Single-robot local simulation",
             "• Community GitHub support"
         ],
         ACCENT_BLUE),
        ("PRO TEAM SAAS",
         "$199 / mo",
         "per Engineering Seat",
         [
             "• Cloud Nemotron 550B tokens",
             "• Zero-SLAM bespoke room generator",
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
         ACCENT_PURPLE)
    ]

    for idx, (t_name, t_price, t_sub, t_features, t_col) in enumerate(tiers):
        x = Inches(0.8 + idx * 3.97)
        card = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.8), Inches(3.75), Inches(4.0))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = CARD_BORDER
        card.line.width = Pt(1)

        # Header bar
        bar = s7.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, Inches(1.8), Inches(3.75), Inches(0.08))
        bar.fill.solid()
        bar.fill.fore_color.rgb = t_col
        bar.line.fill.background()

        tb = s7.shapes.add_textbox(x + Inches(0.25), Inches(2.0), Inches(3.25), Inches(3.6))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0

        p1 = tf.paragraphs[0]
        p1.text = t_name
        p1.font.size = Pt(11)
        p1.font.bold = True
        p1.font.color.rgb = t_col

        p2 = tf.add_paragraph()
        p2.text = t_price
        p2.font.size = Pt(28)
        p2.font.bold = True
        p2.font.color.rgb = TEXT_WHITE

        p3 = tf.add_paragraph()
        p3.text = t_sub
        p3.font.size = Pt(9)
        p3.font.color.rgb = TEXT_MUTED

        for feat in t_features:
            pf = tf.add_paragraph()
            pf.text = feat
            pf.font.size = Pt(10)
            pf.font.color.rgb = TEXT_WHITE

    # Bottom Projection
    rev_box = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(6.05), Inches(11.7), Inches(0.85))
    rev_box.fill.solid()
    rev_box.fill.fore_color.rgb = CARD_LIGHT
    rev_box.line.color.rgb = ACCENT_GREEN
    rev_box.line.width = Pt(1)
    rtf = rev_box.text_frame
    rtf.word_wrap = True
    rp = rtf.paragraphs[0]
    rp.text = "FINANCIAL PROJECTION: $450K ARR in Year 1 (25 Pro Seats + 8 Enterprise Pilots) → Scaling to $3.2M ARR in Year 2"
    rp.font.size = Pt(11)
    rp.font.bold = True
    rp.font.color.rgb = TEXT_WHITE
    rp.alignment = PP_ALIGN.CENTER

    # -------------------------------------------------------------
    # SLIDE 8: Impact & Future Roadmap (PAGE 8)
    # -------------------------------------------------------------
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s8)
    add_header(s8, "IMPACT & ROADMAP", "MEASURABLE INDUSTRY IMPACT & MULTI-YEAR ROADMAP", page_num=8)

    # Left: Impact Highlights
    imp_card = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.7), Inches(4.2))
    imp_card.fill.solid()
    imp_card.fill.fore_color.rgb = CARD_BG
    imp_card.line.color.rgb = CARD_BORDER
    imp_card.line.width = Pt(1)

    itb = s8.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.3), Inches(3.8))
    itf = itb.text_frame
    itf.word_wrap = True
    itf.margin_top = itf.margin_bottom = itf.margin_left = itf.margin_right = 0

    ip1 = itf.paragraphs[0]
    ip1.text = "QUANTIFIED INDUSTRY IMPACT"
    ip1.font.size = Pt(13)
    ip1.font.bold = True
    ip1.font.color.rgb = ACCENT_CYAN

    impacts = [
        ("⚡ 100x Faster Setup Time", "Simulation world synthesis and 2D navigation map extraction compressed from 72 hours to <30 seconds."),
        ("🛡️ 10x Edge-Case Coverage", "Automated adversarial sweeps uncover critical corner-case deadlocks and perception blindspots before physical hardware trials."),
        ("💥 0 Unverified Crashes", "Physical contact sensors (>5 N) and clearance margin tracking ensure AMRs never compromise safe operating envelopes.")
    ]

    for title, desc in impacts:
        p = itf.add_paragraph()
        p.text = f"\n{title}\n{desc}"
        p.font.size = Pt(10)
        p.font.color.rgb = TEXT_WHITE

    # Right: Future Roadmap
    road_card = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.2))
    road_card.fill.solid()
    road_card.fill.fore_color.rgb = CARD_BG
    road_card.line.color.rgb = CARD_BORDER
    road_card.line.width = Pt(1)

    rtb = s8.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(3.8))
    rtf = rtb.text_frame
    rtf.word_wrap = True
    rtf.margin_top = rtf.margin_bottom = rtf.margin_left = rtf.margin_right = 0

    rp1 = rtf.paragraphs[0]
    rp1.text = "STRATEGIC PRODUCT ROADMAP"
    rp1.font.size = Pt(13)
    rp1.font.bold = True
    rp1.font.color.rgb = ACCENT_PURPLE

    milestones = [
        ("• Q2 2026: Multi-Robot Fleet Stress Testing", "Simulate concurrent AMRs with dynamic traffic contention, cross-aisle right-of-way, and fleet manager APIs."),
        ("• Q3 2026: CI/CD GitHub Action Regression Cloud", "Automated nightly simulation fuzzing on every pull request with automated PR markdown reports & video replays."),
        ("• Q4 2026: Photorealistic Digital Twin Bridges", "Direct export to NVIDIA Omniverse / Isaac Sim and Unreal Engine 5 for photorealistic vision sensor testing."),
        ("• 2027: Hardware-in-the-Loop (HIL) Testbenches", "Bridging Lang2Sim live stress signals directly into physical embedded controllers (NVIDIA Jetson, Intel NUC).")
    ]

    for m in milestones:
        p = rtf.add_paragraph()
        p.text = f"\n{m[0]}\n{m[1]}"
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_WHITE

    # Closing quote banner
    callout = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(6.15), Inches(11.7), Inches(0.75))
    callout.fill.solid()
    callout.fill.fore_color.rgb = CARD_LIGHT
    callout.line.color.rgb = ACCENT_BLUE
    callout.line.width = Pt(1)
    ctf = callout.text_frame
    ctf.word_wrap = True
    cp = ctf.paragraphs[0]
    cp.text = "LANG2SIM: EMPOWERING ROBOTICISTS TO TEST THE IMPOSSIBLE BEFORE TOUCHING REAL HARDWARE."
    cp.font.size = Pt(11)
    cp.font.bold = True
    cp.font.color.rgb = TEXT_WHITE
    cp.alignment = PP_ALIGN.CENTER

    prs.save(filename)
    print(f"Presentation saved successfully to {filename}")

if __name__ == "__main__":
    create_deck()
