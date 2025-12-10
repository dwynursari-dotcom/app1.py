import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import requests
from sympy import symbols, diff, latex, solve
from streamlit_lottie import st_lottie

# ==================== PAGE CONFIG (only once) ====================
st.set_page_config(
    page_title="Mathematical Function & Optimization WebApp",
    page_icon="🧮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CUSTOM CSS & DESIGN ====================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Comic+Neue:wght@400;700&family=Poppins:wght@400;600&display=swap');
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }
    /* 1. MENGUBAH BACKGROUND HALAMAN UTAMA JADI PINK */
    .stApp {
        background-color: #FFC0CB; /* Pink lembut */
    }
    .main-header {
        font-family: 'Comic Neue', cursive;
        font-size: 3.3rem;
        color: #000080;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
        text-shadow: 2px 2px 4px #cccccc;
    }

    .sub-header {
        font-family: 'Comic Neue', cursive;
        font-size: 2rem;
        color: #000080;
        margin: 1.5rem 0 1rem 0;
        border-bottom: 3px dashed #FFD700;
        padding-bottom: 0.5rem;
    }

    .card {
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
        background-color: pink;
        margin: 15px 0;
        border-left: 8px solid #000080;;
        transition: transform 0.3s;
    }

    .card:hover {
        transform: scale(1.02);
    }

    /* PREMIUM CARD STYLE FOR OPTIMIZATION */
    .premium-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #555555;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0px;
        text-align: center;
    }
    
    .premium-subtitle {
        font-size: 1.8rem;
        color: #2E8B57;
        font-weight: 600;
        margin-bottom: 20px;
        border-bottom: 3px solid #2E8B57;
        display: inline-block;
        padding-bottom: 5px;
    }

    .premium-card {
        background-color: white;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border: 1px solid #e0e0e0;
        margin-bottom: 20px;
    }
    
    .input-label {
        font-weight: bold;
        color: #333;
    }

    .team-card {
        text-align: center;
        padding: 20px;
        border-radius: 20px;
        background: linear-gradient(135deg, #000080 0%, #191970 100%);
        color: Yellow;
        margin: 15px 0;
        min-height: 420px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-shadow: 0 10px 20px rgba(0,0,0,0.15);
    }

    .profile-image {
        border-radius: 50%;
        border: 5px solid yellow;
        margin: 0 auto 15px auto;
        display: block;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }

    .metric-card {
        background: linear-gradient(135deg, #2E86AB 0%, #A23B72 100%);
        color: white;
        padding: 15px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# ==================== LOTTIE LOADER ====================
@st.cache_data
def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

lottie_math = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_qp1q7mct.json")

# ==================== HELPERS ====================

def parse_function(func_str: str):
    """Parse user input into a SymPy expression in a safe way."""
    try:
        x = sp.symbols('x')
        s = func_str.strip()
        s = s.replace('^', '**')
        safe_dict = {
            'x': x,
            'sin': sp.sin, 'cos': sp.cos, 'tan': sp.tan,
            'exp': sp.exp, 'log': sp.log, 'sqrt': sp.sqrt,
            'pi': sp.pi, 'E': sp.E, 'e': sp.E
        }
        expr = sp.sympify(s, locals=safe_dict)
        return expr, x
    except Exception as e:
        st.error(f"Error parsing function: {e}")
        return None, None


def plot_function(func, x_sym, x_range=(-10, 10), title="Function Plot", optimize_point=None):
    """Create a matplotlib Figure of the given sympy expression over x_range."""
    try:
        x_vals = np.linspace(x_range[0], x_range[1], 400)
        func_numpy = sp.lambdify(x_sym, func, 'numpy')
        y_vals = func_numpy(x_vals)
        
        if np.iscomplexobj(y_vals):
            y_vals = np.real(y_vals)

        # Handle formatting for numpy array
        y_vals = np.nan_to_num(y_vals, nan=np.nan, posinf=np.nan, neginf=np.nan)

        fig, ax = plt.subplots(figsize=(10, 6))
        # Styling plot to match theme
        fig.patch.set_facecolor('#FFF0F5') # Light pink bg for plot
        ax.set_facecolor('#FFFFFF')
        
        ax.plot(x_vals, y_vals, color='#FF1493', linewidth=2.5, label=f'f({x_sym.name})') # Deep pink line
        
        # === PLOT OPTIMIZATION POINT IF EXISTS ===
        if optimize_point:
            opt_x, opt_y = optimize_point
            if opt_x is not None:
                ax.plot(opt_x, opt_y, 'ro', markersize=10, label='Titik Optimal', zorder=5)
                ax.annotate(f'({opt_x:.2f}, {opt_y:.2f})', (opt_x, opt_y), xytext=(10, 10), 
                        textcoords='offset points', fontsize=10, fontweight='bold', color='black')
        # =========================================

        ax.set_xlabel(f'{x_sym.name}', fontsize=12, color='#FF69B4')
        ax.set_ylabel('Nilai', fontsize=12, color='#FF69B4')
        ax.set_title(title, fontsize=14, fontweight='bold', color='#FF1493')
        ax.grid(True, alpha=0.3, color='#FFD700') # Yellow grid
        ax.legend()
        ax.set_xlim(x_range)
        return fig
    except Exception as e:
        st.error(f"Error plotting function: {e}")
        return None


# ==================== PAGE: TEAM ====================

def show_team_page():
    st.markdown('<h1 class="main-header">👥 Tim Pengembang Aplikasi Matematika</h1>', unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("""
    <div class="card">
        <h3 style='color: #FF69B4; margin-top: 0;'>🎯 Tentang Tim Kami</h3>
        <p>Tim mahasiswa berdedikasi yang mengembangkan aplikasi web matematika interaktif untuk memudahkan pembelajaran kalkulus dan optimisasi.</p>
    </div>
    """, unsafe_allow_html=True)

    team_members = [
        {"name": "🧠 Dwy Nursari", "image": "https://img.sanishtech.com/u/56325981e4b73d85858c1c503b5b73cb.jpg", "id": "004202505035", "role": "Project Manager & Full Stack Developer", "contribution": "Backend Development, Deployment & DevOps, System Integration, Team Coordination"},
        {"name": "🎨 Adhitya Suseno", "image": "https://img.sanishtech.com/u/e97ac70f3dbe832a0ee2c2c0e5a33dfe.jpg", "id": "004202505051", "role": "Frontend Developer & UI/UX Designer", "contribution": "UI/UX Design, Data Visualization, LaTeX Integration, Responsive Design"},
        {"name": "🔢 Alvina Nazwa", "image": "https://img.sanishtech.com/u/bd9e17d8183379d999c5028b05b046ec.jpg", "id": "004202505036", "role": "Mathematics & Algorithm Specialist", "contribution": "Mathematical Modeling, Algorithm Development, Symbolic Computation, Optimization Logic"},
        {"name": "🧪 Julian Nauval Saputra", "image": "https://img.sanishtech.com/u/40ec2b8a5f71f27324ed6436aa426c37.jpg", "id": "004202505047", "role": "Testing & Documentation Specialist", "contribution": "Quality Assurance, Data Visualization, User Testing, Documentation"}
    ]

    cols = st.columns(2)
    for i, member in enumerate(team_members):
        with cols[i % 2]:
            st.markdown(f"""
            <div class="team-card">
                <div>
                    <img src="{member['image']}" width="120" height="120" class="profile-image">
                    <h3>{member['name']}</h3>
                    <p style='margin: 5px 0; font-weight: bold;'>ID: {member['id']}</p>
                    <p style='margin: 5px 0; font-style: italic; color: #FF1493;'>{member['role']}</p>
                </div>
                <div style='margin-top: 15px;'>
                    <p style='font-size: 0.9em; text-align: left;'><strong>Kontribusi:</strong><br>{member['contribution']}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="sub-header">📊 Overview Keahlian Tim</div>', unsafe_allow_html=True)

    skills_col1, skills_col2, skills_col3, skills_col4 = st.columns(4)
    with skills_col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Backend", "100%")
        st.markdown('</div>', unsafe_allow_html=True)
    with skills_col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Frontend", "100%")
        st.markdown('</div>', unsafe_allow_html=True)
    with skills_col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Math", "100%")
        st.markdown('</div>', unsafe_allow_html=True)
    with skills_col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("QA", "100%")
        st.markdown('</div>', unsafe_allow_html=True)


# ==================== PAGE: FUNCTION VISUALIZATION ====================

def show_function_page():
    st.markdown('<h1 class="main-header">📈 Visualisasi Fungsi & Turunan</h1>', unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("""
    <div class="card">
        <h3 style='color: #FF69B4; margin-top: 0;'>💡 Panduan Penggunaan</h3>
        <p><strong>Contoh fungsi yang bisa dicoba:</strong> x**2, x**3 - 3*x**2 + 2, sin(x), exp(x), log(x+1)</p>
        <p>Gunakan <strong>x</strong> sebagai variabel. Untuk pangkat gunakan <code>**</code> atau <code>^</code>.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown('<div class="sub-header">✍️ Input Fungsi</div>', unsafe_allow_html=True)
        func_input = st.text_input(
            "Masukkan fungsi f(x):",
            value="x**2",
            help="Gunakan x sebagai variabel. Contoh: x**2 + 2*x + 1",
            placeholder="x**2 + 2*x + 1"
        )
    with col2:
        st.markdown('<div class="sub-header">📊 Rentang Plot</div>', unsafe_allow_html=True)
        col_x1, col_x2 = st.columns(2)
        with col_x1:
            x_min = st.number_input("x minimum", value=-5.0, step=1.0)
        with col_x2:
            x_max = st.number_input("x maksimum", value=5.0, step=1.0)

    if func_input:
        with st.spinner("🔄 Memproses fungsi..."):
            func, x = parse_function(func_input)
            if func is not None:
                st.markdown('<div class="sub-header">🎯 Fungsi Matematika</div>', unsafe_allow_html=True)
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown("""<div class="card"><h4 style='color:#FF1493'>Format Mudah Dibaca</h4>""", unsafe_allow_html=True)
                    st.code(f"f(x) = {sp.pretty(func)}")
                    st.markdown("</div>", unsafe_allow_html=True)
                with c2:
                    st.markdown("""<div class="card"><h4 style='color:#FF1493'>Format LaTeX</h4>""", unsafe_allow_html=True)
                    st.latex(f"f(x) = {sp.latex(func)}")
                    st.markdown("</div>", unsafe_allow_html=True)

                # Plot original function
                st.markdown('<div class="sub-header">📈 Plot Fungsi Asli</div>', unsafe_allow_html=True)
                fig_original = plot_function(func, x, (x_min, x_max), f"Fungsi: {func_input}")
                st.pyplot(fig_original)

                # Calculate derivative
                st.markdown('<div class="sub-header">🧮 Kalkulasi Turunan</div>', unsafe_allow_html=True)
                try:
                    derivative = sp.diff(func, x)
                    d1, d2 = st.columns(2)
                    with d1:
                        st.markdown("""<div class="card"><h4 style='color:#FF1493'>Turunan Fungsi</h4>""", unsafe_allow_html=True)
                        st.code(f"f'(x) = {sp.pretty(derivative)}")
                        st.markdown("</div>", unsafe_allow_html=True)
                    with d2:
                        st.markdown("""<div class="card"><h4 style='color:#FF1493'>Format LaTeX</h4>""", unsafe_allow_html=True)
                        st.latex(f"f'(x) = {sp.latex(derivative)}")
                        st.markdown("</div>", unsafe_allow_html=True)

                    # Plot derivative
                    st.markdown('<div class="sub-header">📊 Plot Fungsi Turunan</div>', unsafe_allow_html=True)
                    fig_derivative = plot_function(derivative, x, (x_min, x_max), f"Turunan: {sp.pretty(derivative)}")
                    st.pyplot(fig_derivative)
                except Exception as e:
                    st.error(f"Error menghitung turunan: {e}")
            else:
                st.error("❌ Tidak dapat memproses fungsi. Pastikan format benar!")


# ==================== PAGE: OPTIMIZATION ====================

def show_optimization_page():
    # 1. Header Section
    st.markdown("""
    <div>
        <p class="premium-title">📐 KALKULATOR OPTIMASI & TURUNAN</p>
        <p style="text-align:center; color:#888; font-size:1.2rem; margin-top:-10px;">PREMIUM VERSION 2.0</p>
    </div>
    """, unsafe_allow_html=True)

    # 2. Main Content Container
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    
    st.markdown('<p class="premium-subtitle">🎯 Solver Optimasi Dinamis Premium</p>', unsafe_allow_html=True)
    
    col_input, col_guide = st.columns([1.5, 1])

    with col_input:
        st.markdown('<p class="input-label">📝 Masukkan Soal Cerita Optimasi</p>', unsafe_allow_html=True)
        # Text Area bebas untuk Soal Cerita
        story = st.text_area(
            "Ceritakan masalah optimasi Anda di sini...",
            height=150,
            placeholder="Contoh: Seorang petani memiliki 100m pagar...",
            label_visibility="collapsed"
        )

        st.markdown("---")

        # Input Fungsi Matematika
        st.markdown("""
        <div style="background-color: #e8f5e9; padding: 15px; border-radius: 8px; border-left: 5px solid #2E8B57; margin-bottom: 15px;">
            <small style="color: #2E8B57; font-weight: bold;">💡 LANGKAH PENTING:</small><br>
            <small style="color: #444;">Berdasarkan cerita di atas, tentukan fungsi tujuan <b>f(x)</b> yang ingin dioptimalkan.</small>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<p class="input-label">∑ Model Matematika (Fungsi f(x))</p>', unsafe_allow_html=True)
        func_input = st.text_input(
            "Fungsi Tujuan",
            placeholder="Contoh: x * (50 - x) atau 200*x - 5*x**2",
            label_visibility="collapsed"
        )
        
        col_limit1, col_limit2 = st.columns(2)
        with col_limit1:
             min_val = st.number_input("Batas Min x", value=0.0)
        with col_limit2:
             max_val = st.number_input("Batas Max x", value=50.0)

    with col_guide:
        st.info("""
        **Panduan Quick Actions:**
        1. **Tulis Cerita:** Masukkan soal cerita lengkap.
        2. **Rumuskan Model:** Terjemahkan cerita menjadi persamaan matematika dalam variabel **x**.
        3. **Klik Analisis:** Algoritma akan mencari titik stasioner (turunan = 0).
        """)
        st_lottie(lottie_math, height=150)

    # Tombol Action
    st.markdown("<br>", unsafe_allow_html=True)
    analyze = st.button("🚀 ANALISIS & SOLUSI PREMIUM", use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True) # End card

    # 3. Logic Execution
    if analyze and func_input:
        with st.spinner("🔄 Sedang melakukan kalkulasi turunan dan optimasi..."):
            func, x = parse_function(func_input)
            
            if func is not None:
                # Menghitung Turunan
                derivative = sp.diff(func, x)
                # Mencari Titik Kritis (Solusi)
                critical_points = sp.solve(derivative, x)
                
                # Filter solusi yang masuk akal (Real dan dalam range)
                valid_solutions = []
                for cp in critical_points:
                    try:
                        val = float(cp)
                        if min_val <= val <= max_val:
                            valid_solutions.append(val)
                    except:
                        pass

                # Menentukan Nilai Optimal
                best_x = None
                best_y = -np.inf
                
                # Cek titik kritis dan ujung interval
                check_points = valid_solutions + [min_val, max_val]
                check_points = sorted(list(set(check_points)))
                
                for pt in check_points:
                    try:
                        val_y = float(func.subs(x, pt))
                        if val_y > best_y: # Asumsi Maksimasi standar
                            best_y = val_y
                            best_x = pt
                    except:
                        pass

                # === HASIL OUTPUT ===
                st.markdown("### 📊 Hasil Analisis Optimasi")
                
                res_col1, res_col2 = st.columns([1, 2])
                
                with res_col1:
                    st.success("**Titik Optimal Ditemukan!**")

                    if best_x is not None:
                        st.metric("Nilai x Optimal", f"{best_x:.4f}")
                        st.metric("Nilai Fungsi Maksimum", f"{best_y:.4f}")
                    else:
                        st.error("Tidak ditemukan nilai optimal dalam rentang yang diberikan.")
                        st.metric("Nilai x Optimal", "-")
                        st.metric("Nilai Fungsi Maksimum", "-")

                    st.markdown("---")
                    st.latex(r"f(x) = " + sp.latex(func))
                    st.latex(r"f'(x) = " + sp.latex(derivative))
                    st.markdown(f"**Titik Kritis:** {valid_solutions}")

                with res_col2:
                    # FIX: Memanggil plot_function dengan argumen yang BENAR
                    fig = plot_function(
                        func,
                        x, 
                        (min_val, max_val),
                        title="Grafik Optimisasi",
                        optimize_point=(best_x, best_y)
                    )

                    if fig:
                        st.pyplot(fig)
            else:
                st.error("⚠️ Format fungsi matematika tidak valid. Gunakan sintaks Python (misal: x**2 untuk kuadrat).")

# ==================== SIDEBAR & ROUTING ====================
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; margin-bottom: 2rem;'>
        <h1 style='color: #FF69B4; margin-bottom: 0;'>🧮</h1>
        <h2 style='color: #FF69B4; margin-top: 0;'>Math WebApp</h2>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("""
    <div class="card">
        <h4 style='color: #FF69B4; margin-top: 0;'>ℹ️ Tentang Aplikasi</h4>
        <p><strong>Fitur Utama:</strong></p>
        <ul>
            <li>📊 Visualisasi fungsi matematika</li>
            <li>🧮 Kalkulasi turunan otomatis</li>
            <li>🎯 Penyelesaian masalah optimisasi</li>
            <li>📈 Plot informatif</li>
        </ul>
        <p><strong>Teknologi:</strong> Python + Streamlit + SymPy + Matplotlib</p>
    </div>
    """, unsafe_allow_html=True)

# Routing logic
menu = st.sidebar.radio(
    "Navigasi",
    ["🏠 Home", "👥 Team", "📈 Fungsi & Turunan", "🎯 Optimisasi"]
)

if menu == "🏠 Home":
    st.markdown('<h1 class="main-header">🧮 MathFun WebApp</h1>', unsafe_allow_html=True)
    if lottie_math:
        st_lottie(lottie_math, height=300)
    st.markdown("<center>Aplikasi untuk belajar fungsi, turunan, dan optimisasi secara visual!</center>", unsafe_allow_html=True)

elif menu == "👥 Team":
    show_team_page()

elif menu == "📈 Fungsi & Turunan":
    show_function_page()

elif menu == "🎯 Optimisasi":
    show_optimization_page()
