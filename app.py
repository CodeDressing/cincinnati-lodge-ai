/* ============================================================
   PROJECT MAPLE
   CINCINNATI LODGE AI
   ============================================================ */

/* ============================================================
   SECTION 1 - DESIGN VARIABLES
   ============================================================ */

:root {

    --navy-primary: #1F2D51;
    --navy-dark: #15203A;

    --gold-primary: #C9A227;
    --gold-light: #D8B84A;

    --white: #FFFFFF;
    --light-gray: #F4F4F4;

    --text-dark: #1A1A1A;
    --text-light: #FFFFFF;

    --shadow-soft:
        0 4px 12px rgba(0,0,0,0.15);

    --shadow-large:
        0 8px 24px rgba(0,0,0,0.20);

    --border-radius:
        10px;

    --max-width:
        1400px;
}

/* ============================================================
   SECTION 2 - GLOBAL RESET
   ============================================================ */

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

/* ============================================================
   SECTION 3 - BODY
   ============================================================ */

body {

    font-family:
        "Segoe UI",
        Arial,
        sans-serif;

    background-color:
        var(--light-gray);

    color:
        var(--text-dark);

    line-height:
        1.6;
}

/* ============================================================
   SECTION 4 - LINKS
   ============================================================ */

a {

    text-decoration:
        none;

    color:
        inherit;

    transition:
        0.25s;
}

a:hover {

    color:
        var(--gold-primary);
}

/* ============================================================
   SECTION 5 - CONTAINERS
   ============================================================ */

.container {

    width: 90%;

    max-width:
        var(--max-width);

    margin:
        0 auto;
}

/* ============================================================
   SECTION 6 - HEADER
   ============================================================ */

.site-header {

    background:
        var(--navy-primary);

    color:
        var(--text-light);

    padding:
        1rem 0;

    box-shadow:
        var(--shadow-soft);
}

/* ============================================================
   SECTION 7 - NAVIGATION
   ============================================================ */

.navbar {

    display:
        flex;

    justify-content:
        space-between;

    align-items:
        center;
}

.nav-logo {

    font-size:
        1.5rem;

    font-weight:
        bold;

    color:
        var(--gold-primary);
}

.nav-links {

    display:
        flex;

    gap:
        1.5rem;
}

/* ============================================================
   SECTION 8 - HERO SECTION
   ============================================================ */

.hero {

    background:
        linear-gradient(
            rgba(31,45,81,.85),
            rgba(21,32,58,.85)
        );

    color:
        white;

    text-align:
        center;

    padding:
        6rem 2rem;
}

.hero h1 {

    font-size:
        3rem;

    margin-bottom:
        1rem;
}

.hero p {

    max-width:
        800px;

    margin:
        auto;

    font-size:
        1.1rem;
}

/* ============================================================
   SECTION 9 - BUTTON SYSTEM
   ============================================================ */

.btn {

    display:
        inline-block;

    padding:
        12px 24px;

    border-radius:
        var(--border-radius);

    font-weight:
        600;

    transition:
        0.25s;
}

.btn-primary {

    background:
        var(--gold-primary);

    color:
        white;
}

.btn-primary:hover {

    background:
        var(--gold-light);
}

/* ============================================================
   SECTION 10 - CARD SYSTEM
   ============================================================ */

.card {

    background:
        white;

    border-radius:
        var(--border-radius);

    box-shadow:
        var(--shadow-soft);

    padding:
        1.5rem;

    margin:
        1rem 0;
}

/* ============================================================
   SECTION 11 - EVENTS
   ============================================================ */

.event-grid {

    display:
        grid;

    grid-template-columns:
        repeat(auto-fit,minmax(300px,1fr));

    gap:
        1.5rem;
}

/* ============================================================
   SECTION 12 - SEO PAGES
   ============================================================ */

.seo-content {

    padding:
        3rem 0;
}

.seo-content h2 {

    color:
        var(--navy-primary);

    margin-bottom:
        1rem;
}

/* ============================================================
   SECTION 13 - ASSISTANT PAGE
   ============================================================ */

.assistant-wrapper {

    max-width:
        900px;

    margin:
        3rem auto;
}

.assistant-box {

    background:
        white;

    padding:
        2rem;

    border-radius:
        var(--border-radius);

    box-shadow:
        var(--shadow-soft);
}

/* ============================================================
   SECTION 14 - FOOTER
   ============================================================ */

.site-footer {

    background:
        var(--navy-dark);

    color:
        white;

    text-align:
        center;

    padding:
        2rem;
}

/* ============================================================
   SECTION 15 - RESPONSIVE DESIGN
   ============================================================ */

@media (max-width: 768px) {

    .navbar {

        flex-direction:
            column;

        gap:
            1rem;
    }

    .hero h1 {

        font-size:
            2rem;
    }

    .hero {

        padding:
            4rem 1rem;
    }
}

/* ============================================================
   END OF FILE
   ============================================================ */