import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
from sympy import symbols, diff, latex, solve

# ==================== KONFIGURASI HALAMAN ====================
st.set_page_config(
    page_title="Mathematical Function & Optimization WebApp",
    page_icon="📊",
    layout="wide"
)

# ==================== FUNGSI BANTU ====================
def parse_function(func_str):
    """Mengubah string fungsi menjadi ekspresi sympy"""
    try:
        x = sp.symbols('x')
        # Preprocessing input
        func_str = func_str.strip()
        func_str = func_str.replace('^', '')  # Convert ^ to **
        func_str = func_str.replace(' ', '')    # Remove spaces
        
        # Handle common functions
        func_str = func_str.replace('sin', 'sp.sin')
        func_str = func_str.replace('cos', 'sp.cos') 
        func_str = func_str.replace('exp', 'sp.exp')
        func_str = func_str.replace('log', 'sp.log')
        func_str = func_str.replace('sqrt', 'sp.sqrt')
        func_str = func_str.replace('tan', 'sp.tan')
        
        # Parse menggunakan eval dengan namespace aman
        safe_dict = {
            'x': x,
            'sp': sp,
            'sin': sp.sin,
            'cos': sp.cos,
            'tan': sp.tan,
            'exp': sp.exp,
            'log': sp.log,
            'sqrt': sp.sqrt,
            'pi': sp.pi,
            'e': sp.E
        }
        
        func = eval(func_str, {"_builtins_": None}, safe_dict)
        return func, x
        
    except Exception as e:
        st.error(f"Error parsing: {e}")
        return None, None

def plot_function(func, x_sym, x_range=(-10, 10), title="Function Plot"):
    """Membuat plot fungsi matematika dengan error handling"""
    try:
        x_vals = np.linspace(x_range[0], x_range[1], 400)
        
        # Convert sympy function to numpy function
        func_numpy = sp.lambdify(x_sym, func, 'numpy')
        y_vals = func_numpy(x_vals)
        
        # Handle NaN or inf values
        y_vals = np.nan_to_num(y_vals, nan=0.0, posinf=10, neginf=-10)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(x_vals, y_vals, 'b-', linewidth=2, label=f'f(x)')
        ax.set_xlabel('x')
        ax.set_ylabel('f(x)')
        ax.set_title(title)
        ax.grid(True, alpha=0.3)
        ax.legend()
        ax.set_xlim(x_range)
        
        return fig
        
    except Exception as e:
        # Fallback plot jika error
        st.error(f"Error dalam plotting: {e}")
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.text(0.5, 0.5, f"Error: {e}", ha='center', va='center', transform=ax.transAxes)
        ax.set_title("Plot Error")
        return fig

# ==================== HALAMAN 1: ANGGOTA TIM ====================
def show_team_page():
    st.title("👥 Anggota Tim")
    st.markdown("---")
    
    st.success("🦸‍♂ *Tim Pengembang Aplikasi Web Matematika*")
    
    # Row 1: 2 anggota
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🧠 Dwy Nursari")
        st.image(
            "https://img.sanishtech.com/u/56325981e4b73d85858c1c503b5b73cb.jpg",
            width=150,
            caption="Project Manager & Full Stack Developer"
        )
        st.write("*ID:* 004202505035")
        st.write("*Peran:* Project Leader")
        st.info("""
        *Kontribusi:*
        - Backend Development
        - Deployment & DevOps  
        - System Integration
        - Team Coordination
        """)
    
    with col2:
        st.markdown("### 🎨 Adhitya Suseno ")
        st.image(
            "https://img.sanishtech.com/u/e97ac70f3dbe832a0ee2c2c0e5a33dfe.jpg",
            width=150,
            caption="Frontend Developer & UI/UX Designer"
        )
        st.write("*ID:* 004202505051")
        st.write("*Peran:* Frontend Specialist")
        st.info("""
        *Kontribusi:*
        - UI/UX Design
        - Data Visualization
        - LaTeX Integration
        - Responsive Design
        """)
    
    # Row 2: 2 anggota
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("### 🔢 Alvina Nazwa")
        st.image(
            "https://img.sanishtech.com/u/bd9e17d8183379d999c5028b05b046ec.jpg",
            width=150,
            caption="Mathematics & Algorithm Specialist"
        )
        st.write("*ID:* 004202505036")
        st.write("*Peran:* Math Expert")
        st.info("""
        *Kontribusi:*
        - Mathematical Modeling
        - Algorithm Development
        - Symbolic Computation
        - Optimization Logic
        """)
    
    with col4:
        st.markdown("### 🧪Julian Nauval Saputra")
        st.image(
            "https://img.sanishtech.com/u/40ec2b8a5f71f27324ed6436aa426c37.jpg",
            width=150,
            caption="Testing & Documentation Specialist"
        )
        st.write("*ID:* 004202505047")
        st.write("*Peran:* QA & Documentation")
        st.info("""
        *Kontribusi:*
        - Quality Assurance
        - Data Visualization
        - User Testing
        - Documentation
        """)
    
    # Skills overview
    st.markdown("---")
    st.subheader("📊 Overview Keahlian Tim")
    
    skills_col1, skills_col2, skills_col3, skills_col4 = st.columns(4)
    
    with skills_col1:
        st.metric("Backend Development", "100%", "Python & Streamlit")
    with skills_col2:
        st.metric("Frontend Design", "100%", "UI/UX & Visualization")
    with skills_col3:
        st.metric("Mathematics", "100%", "Algorithms & SymPy")
    with skills_col4:
        st.metric("Quality Assurance", "100%", "Testing & Docs")

# ==================== HALAMAN 2: VISUALISASI FUNGSI ====================
def show_function_page():
    st.title("📈 Visualisasi Fungsi & Turunan")
    st.markdown("---")
    
    st.info("💡 *Contoh fungsi yang bisa dicoba:* x*2, x3 - 3*x*2 + 2, sin(x), exp(x), log(x+1)")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Input Fungsi")
        func_input = st.text_input(
            "Masukkan fungsi f(x):",
            value="x**2",
            help="Gunakan x sebagai variabel. Contoh: x**2 + 2*x + 1"
        )
    
    with col2:
        st.subheader("Rentang Plot")
        x_min = st.number_input("x minimum", value=-5.0)
        x_max = st.number_input("x maksimum", value=5.0)
    
    if func_input:
        with st.spinner("Memproses fungsi..."):
            func, x = parse_function(func_input)
            
            if func is not None:
                # Display function
                st.subheader("🎯 Fungsi Matematika")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("*Format Mudah Dibaca:*")
                    st.code(f"f(x) = {sp.pretty(func)}")
                
                with col2:
                    st.write("*Format LaTeX:*")
                    st.latex(f"f(x) = {sp.latex(func)}")
                
                # Plot original function
                st.subheader("📊 Plot Fungsi Asli")
                try:
                    fig_original = plot_function(func, x, (x_min, x_max), f"Fungsi: {func_input}")
                    st.pyplot(fig_original)
                except Exception as e:
                    st.error(f"Error plotting fungsi: {e}")
                
                # Calculate derivative
                st.subheader("🧮 Kalkulasi Turunan")
                try:
                    derivative = sp.diff(func, x)
                    
                    st.write("*Turunan Fungsi:*")
                    st.code(f"f'(x) = {sp.pretty(derivative)}")
                    st.latex(f"f'(x) = {sp.latex(derivative)}")
                    
                    # Plot derivative
                    st.subheader("📈 Plot Fungsi Turunan")
                    fig_derivative = plot_function(derivative, x, (x_min, x_max), f"Turunan: {sp.pretty(derivative)}")
                    st.pyplot(fig_derivative)
                    
                except Exception as e:
                    st.error(f"Error menghitung turunan: {e}")
                
            else:
                st.error("❌ Tidak dapat memproses fungsi. Pastikan format benar!")
                st.info("""
                *Contoh format yang benar:*
                - x**2 + 2*x + 1
                - x*3 - 3*x*2 + 2*x
                - sin(x)
                - exp(x)
                - log(x+1)
                - sqrt(x)
                """)

# ==================== HALAMAN 3: OPTIMIZATION SOLVER ====================
def show_optimization_page():
    st.title("🎯 Penyelesaian Masalah Optimisasi")
    st.markdown("---")
    
    st.subheader("Pilih Masalah Optimisasi")
    
    problem_option = st.selectbox(
        "Pilih contoh masalah:",
        ["Volume Maksimum Kotak", "Luas Maksimum Persegi Panjang"]
    )
    
    if problem_option == "Volume Maksimum Kotak":
        st.write("📝 Deskripsi Masalah:")
        st.write("Sebuah kotak tanpa tutup dibuat dari karton berukuran 20 cm × 30 cm.")
        st.write("Tentukan ukuran kotak untuk volume maksimum dengan memotong sudut-sudut persegi yang sama besar.")
        
        x = symbols('x')
        # Volume = panjang × lebar × tinggi
        # Panjang = 30 - 2x, Lebar = 20 - 2x, Tinggi = x
        volume_func = x * (20 - 2*x) * (30 - 2*x)
        
    else:  # Luas Maksimum Persegi Panjang
        st.write("📝 Deskripsi Masalah:")
        st.write("Tentukan ukuran persegi panjang dengan keliling 100 meter yang memiliki luas maksimum.")
        
        x = symbols('x')
        # Keliling = 2(panjang + lebar) = 100
        # Lebar = x, Panjang = 50 - x
        # Luas = panjang × lebar
        volume_func = x * (50 - x)
    
    if st.button("🚀 Selesaikan Masalah"):
        with st.spinner("Menghitung solusi..."):
            # Hitung turunan
            derivative = diff(volume_func, x)
            
            # Cari titik kritis
            critical_points = solve(derivative, x)
            
            # Filter solusi yang valid
            valid_solutions = []
            for cp in critical_points:
                if cp.is_real and 0 < float(cp) < 25:
                    valid_solutions.append(float(cp))
            
            # Tampilkan solusi
            st.subheader("📋 Langkah-langkah Penyelesaian")
            
            st.write("*1. Fungsi yang Dioptimasi:*")
            st.latex(f"f(x) = {latex(volume_func)}")
            
            st.write("*2. Turunan Pertama:*")
            st.latex(f"f'(x) = {latex(derivative)}")
            
            st.write("*3. Titik Kritis (f'(x) = 0):*")
            if valid_solutions:
                for i, sol in enumerate(valid_solutions, 1):
                    st.code(f"x = {sol:.4f}")
            else:
                st.warning("Tidak ditemukan titik kritis yang valid")
            
            st.write("*4. Solusi Optimal:*")
            if valid_solutions:
                optimal_x = valid_solutions[0]
                optimal_value = volume_func.subs(x, optimal_x)
                st.success(f"*Nilai optimal: x = {optimal_x:.4f}*")
                st.success(f"*Nilai fungsi: f({optimal_x:.4f}) = {optimal_value:.4f}*")
            else:
                st.error("Tidak dapat menemukan solusi optimal")
            
            # Plot
            st.subheader("📊 Visualisasi Solusi")
            fig = plot_function(volume_func, x, (0, 15), "Fungsi Optimisasi")
            
            # Tandai titik optimal pada plot
            if valid_solutions:
                optimal_x = valid_solutions[0]
                optimal_y = volume_func.subs(x, optimal_x)
                
                x_vals = np.linspace(0, 15, 400)
                func_numpy = sp.lambdify(x, volume_func, 'numpy')
                y_vals = func_numpy(x_vals)
                
                plt.figure(figsize=(10, 6))
                plt.plot(x_vals, y_vals, 'b-', linewidth=2, label='f(x)')
                plt.plot(optimal_x, optimal_y, 'ro', markersize=10, 
                        label=f'Titik Optimal: x = {optimal_x:.2f}')
                plt.xlabel('x')
                plt.ylabel('f(x)')
                plt.title('Fungsi Optimisasi dengan Titik Optimal')
                plt.grid(True, alpha=0.3)
                plt.legend()
                st.pyplot(plt)

# ==================== MAIN APP ROUTING ====================
st.sidebar.title("🧭 Navigasi")
page = st.sidebar.radio(
    "Pilih Halaman:",
    ["Anggota Tim", "Visualisasi Fungsi", "Penyelesaian Optimisasi"]
)

st.sidebar.markdown("---")
st.sidebar.info(
    """
    *Aplikasi Web Matematika*
    
    *Fitur:*
    • Visualisasi fungsi
    • Kalkulasi turunan  
    • Penyelesaian optimisasi
    • Plot interaktif
    
    *Teknologi:*
    Python + Streamlit + SymPy
    """
)

if page == "Anggota Tim":
    show_team_page()
elif page == "Visualisasi Fungsi":
    show_function_page()
else:
    show_optimization_page()
