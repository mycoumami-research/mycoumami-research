
import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import f
from pathlib import Path

# ==========================================
# 1. CAU HINH WEBSITE
# ==========================================

st.set_page_config(
    page_title="MYCOUMAMI Research Lab",
    page_icon="🍄",
    layout="wide"
)

# ==========================================
# 2. THIET KE GIAO DIEN TRANG - DO
# ==========================================

st.markdown("""
<style>

.stApp {
    background-color: #F5F5F7;
    color: #252525;
}

[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg, #A41420, #790E19
    );
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label {
    color: white;
}

[data-testid="stHeader"] {
    background-color: white;
}

[data-testid="stMetric"] {
    background-color: white;
    padding: 20px;
    border-radius: 12px;
    border-left: 5px solid #A41420;
    box-shadow: 0 4px 15px #00000010;
}

[data-testid="stMetricValue"] {
    color: #A41420;
    font-weight: bold;
}

h1, h2, h3 {
    color: #A41420;
    font-weight: 700;
}

.stButton > button,
.stDownloadButton > button {
    background-color: #A41420;
    color: white;
    border: none;
    border-radius: 8px;
}

.stButton > button:hover {
    background-color: #790E19;
    color: white;
}

.hero {
    background: linear-gradient(
        120deg, #790E19, #C92332
    );
    padding: 35px;
    border-radius: 16px;
    color: white;
    margin-bottom: 25px;
}

.hero h1 {
    color: white;
    font-size: 48px;
    letter-spacing: 2px;
}

.hero h3 {
    color: #FFE5E7;
}

.panel {
    background-color: white;
    border-radius: 12px;
    padding: 20px;
    border: 1px solid #EEEEEE;
    margin-bottom: 15px;
}

[data-testid="stPlotlyChart"] {
    background-color: white;
    border-radius: 12px;
    padding: 10px;
}

html, body {
    font-family: "Segoe UI", sans-serif;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. DU LIEU THI NGHIEM
# ==========================================

raw = [
    ["TN01",2000,1,55,.150,.006,1352],
    ["TN02",4000,1,55,.168,.003,1523],
    ["TN03",2000,3,55,.178,.004,1612],
    ["TN04",4000,3,55,.220,.018,1997],
    ["TN05",2000,2,45,.218,.008,1979],
    ["TN06",4000,2,45,.265,.005,2410],
    ["TN07",2000,2,65,.226,.007,2052],
    ["TN08",4000,2,65,.184,.006,1667],
    ["TN09",3000,1,45,.145,.005,1309],
    ["TN10",3000,3,45,.187,.007,1691],
    ["TN11",3000,1,65,.153,.005,1382],
    ["TN12",3000,3,65,.140,.008,1260],
    ["TN13",3000,2,55,.285,.008,2593],
    ["TN14",3000,2,55,.290,.011,2639],
    ["TN15",3000,2,55,.288,.016,2621],
    ["TN16",2000,2,55,.232,.004,2110],
    ["TN17",4000,2,55,.248,.011,2257]
]

columns = [
    "Mẫu",
    "Papain",
    "Thời gian",
    "Nhiệt độ",
    "A570",
    "SD",
    "Glu-eq"
]

original = pd.DataFrame(raw, columns=columns)

if "data" not in st.session_state:
    st.session_state.data = original.copy()

# ==========================================
# 4. THANH MENU
# ==========================================

st.sidebar.title("🍄 MYCOUMAMI")

st.sidebar.caption(
    "RESEARCH & INNOVATION LAB"
)

st.sidebar.divider()

menu = st.sidebar.radio(
    "DANH MỤC",
    [
        "Dashboard",
        "Giới thiệu sản phẩm",
        "Dữ liệu thí nghiệm",
        "Box-Behnken RSM",
        "Phân tích ANOVA",
        "Tối ưu hóa",
        "Quy trình công nghệ",
        "Phát triển bền vững",
        "Thương mại hóa"
    ]
)

st.sidebar.divider()

mode = st.sidebar.selectbox(
    "Thiết kế thí nghiệm",
    [
        "17 nghiệm thức mở rộng",
        "15 nghiệm thức Box-Behnken"
    ]
)

response = st.sidebar.selectbox(
    "Biến đáp ứng",
    ["A570", "Glu-eq"]
)

chart_colors = st.sidebar.selectbox(
    "Bang mau bieu do RSM",
    ["Turbo", "Viridis", "Plasma", "Cividis"]
)

unit = (
    "mg/L"
    if response == "Glu-eq"
    else "AU"
)

st.sidebar.divider()

st.sidebar.markdown("**YERSIN UNIVERSITY**")
st.sidebar.caption("Food Innovation and Development 2026")
st.sidebar.caption("Version 1.0")

# ==========================================
# 5. HAM HIEN THI ANH SAN PHAM
# ==========================================

def show_product():

    path = Path(__file__).parent / "product.png"

    if path.exists():

        st.image(
            str(path),
            caption="Thiết kế bao bì MYCOUMAMI 100 g"
        )

    else:

        uploaded = st.file_uploader(
            "Tải ảnh sản phẩm",
            type=["png","jpg","jpeg"]
        )

        if uploaded is not None:
            st.image(uploaded)

# ==========================================
# 6. MO HINH HOI QUY BAC HAI
# ==========================================

data = st.session_state.data.copy()

if mode == "15 nghiệm thức Box-Behnken":
    data = data.iloc[:15].copy()

def design(x1,x2,x3):

    x1,x2,x3 = np.broadcast_arrays(x1,x2,x3)

    return np.stack([
        np.ones_like(x1),
        x1,
        x2,
        x3,
        x1*x2,
        x1*x3,
        x2*x3,
        x1**2,
        x2**2,
        x3**2
    ],axis=-1)

def actual_design(p,t,T):

    return design(
        (p-3000)/1000,
        t-2,
        (T-55)/10
    )

X = actual_design(
    data["Papain"].to_numpy(),
    data["Thời gian"].to_numpy(),
    data["Nhiệt độ"].to_numpy()
)

Y = data[response].to_numpy(dtype=float)

if not np.all(np.isfinite(Y)):
    st.error("Dữ liệu có giá trị không hợp lệ.")
    st.stop()

b = np.linalg.lstsq(X,Y,rcond=None)[0]

def predict(p,t,T):
    return actual_design(p,t,T) @ b

Y_pred = X @ b

SSE = np.sum((Y-Y_pred)**2)
SST = np.sum((Y-Y.mean())**2)
SSR = SST-SSE

n = len(Y)

df_model = 9
df_error = n-10

R2 = (
    1-SSE/SST
    if SST > 0 else np.nan
)

R2_adj = (
    1-(1-R2)*(n-1)/df_error
)

F_model = (
    (SSR/df_model)/(SSE/df_error)
    if SSE > 0 else np.nan
)

p_model = f.sf(
    F_model,
    df_model,
    df_error
)

terms = [
    "Intercept",
    "X1","X2","X3",
    "X1X2","X1X3","X2X3",
    "X1²","X2²","X3²"
]

# ==========================================
# 7. TRANG DASHBOARD
# ==========================================

if menu == "Dashboard":

    st.markdown("""
    <div class="hero">
        <h1>MYCOUMAMI</h1>
        <h3>Tinh hoa vị umami Đà Lạt</h3>
        <p>
        Kết nối nông sản địa phương với
        công nghệ enzyme và chuỗi giá trị
        thực phẩm bền vững.
        </p>
    </div>
    """, unsafe_allow_html=True)

    c1,c2,c3,c4 = st.columns(4)

    c1.metric(
        "Nghiệm thức",
        len(data)
    )

    c2.metric(
        "Yếu tố khảo sát",
        3
    )

    c3.metric(
        "R² mô hình",
        f"{R2:.4f}"
    )

    c4.metric(
        "Đáp ứng cao nhất",
        f"{Y.max():.4g}"
    )

    left,right = st.columns([1,1])

    with left:

        st.subheader("MYCOUMAMI PRODUCT")

        show_product()

    with right:

        st.subheader("Experimental Results")

        fig = px.bar(
            data,
            x="Mẫu",
            y=response,
            error_y=(
                "SD"
                if response=="A570"
                else None
            ),
            color=response,
            color_continuous_scale="Viridis",
            template="plotly_white"
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

    st.subheader("Tiến độ nghiên cứu")

    a,c,d = st.columns(3)

    a.success(
        "Nhánh A: Có dữ liệu thủy phân Papain"
    )

    c.warning(
        "Nhánh B: Cần xác nhận Pectinase"
    )

    d.warning(
        "Nhánh C: Cần tối ưu khoai tây"
    )

    st.subheader("Response Surface")

    P,t = np.meshgrid(
        np.linspace(2000,4000,60),
        np.linspace(1,3,60)
    )

    Z = predict(P,t,55)

    surface = go.Figure(
        go.Surface(contours=dict(z=dict(show=True, usecolormap=True, project=dict(z=True))), 
            x=P,
            y=t,
            z=Z,
            colorscale=chart_colors
        )
    )

    surface.update_layout(
        template="plotly_white",
        height=500,
        scene=dict(
            xaxis_title="Papain (U/g CK)",
            yaxis_title="Thời gian (giờ)",
            zaxis_title=response
        )
    )

    st.plotly_chart(
        surface,
        width="stretch"
    )

# ==========================================
# 8. GIOI THIEU SAN PHAM
# ==========================================

elif menu == "Giới thiệu sản phẩm":

    st.title("HẠT NÊM MYCOUMAMI")

    st.subheader(
        "Tinh hoa vị umami Đà Lạt"
    )

    a,c = st.columns([1.3,1])

    with a:
        show_product()

    with c:

        st.markdown("""
        ### Câu chuyện sản phẩm

        MYCOUMAMI được phát triển từ gốc nấm
        kim châm và nông sản ngoài chuẩn
        thương mại tại Đà Lạt, còn phù hợp
        để chế biến thực phẩm.

        Dự án ứng dụng công nghệ enzyme nhằm
        nâng cao giá trị nguyên liệu địa phương.

        **Quy cách bao bì thiết kế:** 100 g.

        **Định hướng sử dụng:**

        - Canh và súp.
        - Các món xào.
        - Nước sốt.
        - Nền gia vị chế biến thực phẩm.
        """)

    st.subheader("Ba dòng nguyên liệu")

    a,c,d = st.columns(3)

    with a:

        st.markdown("### 🍄 Nấm kim châm")

        st.write(
            "Nguồn amino acid, nucleotide "
            "và nền mùi vị nấm."
        )

    with c:

        st.markdown("### 🍅 Cà chua")

        st.write(
            "Nguồn glutamate tự do, "
            "độ chua và màu sắc."
        )

    with d:

        st.markdown("### 🥔 Khoai tây")

        st.write(
            "Khảo sát khả năng tạo độ đầy vị "
            "và kiểm soát lượng cặn."
        )

    st.caption(
        "Sản phẩm đang trong giai đoạn "
        "nghiên cứu và phát triển."
    )

# ==========================================
# 9. QUAN LY DU LIEU
# ==========================================

elif menu == "Dữ liệu thí nghiệm":

    st.title("Laboratory Data Management")

    st.info(
        "Chỉnh sửa A570, SD và Glu-eq "
        "trực tiếp trên bảng."
    )

    edited = st.data_editor(
        st.session_state.data,
        disabled=[
            "Mẫu",
            "Papain",
            "Thời gian",
            "Nhiệt độ"
        ],
        hide_index=True,
        width="stretch"
    )

    if st.button("Lưu dữ liệu"):

        values = edited[
            ["A570","SD","Glu-eq"]
        ].to_numpy(dtype=float)

        if (
            np.all(np.isfinite(values))
            and np.all(values >= 0)
        ):

            st.session_state.data = edited.copy()

            st.success(
                "Đã cập nhật dữ liệu trong phiên."
            )

        else:

            st.error(
                "Kiểm tra ô trống hoặc giá trị âm."
            )

    if st.button("Khôi phục dữ liệu gốc"):

        st.session_state.data = original.copy()
        st.rerun()

    st.download_button(
        "Tải dữ liệu CSV",
        st.session_state.data.to_csv(
            index=False
        ).encode("utf-8-sig"),
        "MYCOUMAMI_Data.csv",
        "text/csv"
    )

    st.caption(
        "Glu-eq được quy đổi theo chuẩn MSG, "
        "không phải phép đo L-glutamate đặc hiệu."
    )

# ==========================================
# 10. BOX-BEHNKEN RESPONSE SURFACE
# ==========================================

elif menu == "Box-Behnken RSM":

    st.title(
        "Box-Behnken Response Surface"
    )

    st.latex(
        r"X_1=\frac{P-3000}{1000},"
        r"\quad X_2=t-2,"
        r"\quad X_3=\frac{T-55}{10}"
    )

    st.subheader("Phương trình hồi quy")

    equation = f"Y = {b[0]:.5f}"

    for name,value in zip(
        terms[1:],b[1:]
    ):

        equation += (
            f" {value:+.5f} × {name}"
        )

    st.code(
        equation,
        language="text"
    )

    pair = st.selectbox(
        "Chọn cặp yếu tố khảo sát",
        [
            "Papain - Thời gian",
            "Papain - Nhiệt độ",
            "Thời gian - Nhiệt độ"
        ]
    )

    P = np.linspace(2000,4000,80)
    t = np.linspace(1,3,80)
    T = np.linspace(45,65,80)

    if pair == "Papain - Thời gian":

        fixed = st.slider(
            "Nhiệt độ cố định",
            45.0,65.0,55.0
        )

        A,B = np.meshgrid(P,t)
        Z = predict(A,B,fixed)

        xlabel = "Papain (U/g CK)"
        ylabel = "Thời gian (giờ)"

    elif pair == "Papain - Nhiệt độ":

        fixed = st.slider(
            "Thời gian cố định",
            1.0,3.0,2.0
        )

        A,B = np.meshgrid(P,T)
        Z = predict(A,fixed,B)

        xlabel = "Papain (U/g CK)"
        ylabel = "Nhiệt độ (°C)"

    else:

        fixed = st.slider(
            "Papain cố định",
            2000,4000,3000
        )

        A,B = np.meshgrid(t,T)
        Z = predict(fixed,A,B)

        xlabel = "Thời gian (giờ)"
        ylabel = "Nhiệt độ (°C)"

    c1,c2 = st.columns(2)

    with c1:

        fig = go.Figure(
            go.Surface(contours=dict(z=dict(show=True, usecolormap=True, project=dict(z=True))), 
                x=A,
                y=B,
                z=Z,
                colorscale=chart_colors,
                colorbar=dict(
                    title=response
                )
            )
        )

        fig.update_layout(
            title="Response Surface 3D",
            template="plotly_white",
            height=550,
            scene=dict(
                xaxis_title=xlabel,
                yaxis_title=ylabel,
                zaxis_title=f"{response} ({unit})"
            )
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

    with c2:

        contour = go.Figure(
            go.Contour(
                x=A[0],
                y=B[:,0],
                z=Z,
                colorscale=chart_colors,
                contours=dict(
                    showlabels=True
                )
            )
        )

        contour.update_layout(
            title="Contour Plot",
            template="plotly_white",
            xaxis_title=xlabel,
            yaxis_title=ylabel,
            height=550
        )

        st.plotly_chart(
            contour,
            width="stretch"
        )

    st.caption(
        "Dùng chuột để xoay biểu đồ 3D. "
        "Màu đỏ đậm biểu thị đáp ứng cao."
    )

    st.warning(
        "Một số vùng ở góc bề mặt có thể "
        "nằm ngoài bao lồi của thiết kế BBD."
    )

# ==========================================
# 11. PHAN TICH ANOVA
# ==========================================

elif menu == "Phân tích ANOVA":

    st.title("Analysis of Variance")

    a,c,d = st.columns(3)

    a.metric("R²",f"{R2:.4f}")

    c.metric(
        "Adjusted R²",
        f"{R2_adj:.4f}"
    )

    d.metric(
        "p-value",
        f"{p_model:.6f}"
    )

    anova = pd.DataFrame({
        "Nguồn": [
            "Model",
            "Residual",
            "Total"
        ],
        "SS": [SSR,SSE,SST],
        "df": [9,df_error,n-1],
        "MS": [
            SSR/9,
            SSE/df_error,
            np.nan
        ],
        "F": [
            F_model,
            np.nan,
            np.nan
        ],
        "p-value": [
            p_model,
            np.nan,
            np.nan
        ]
    })

    st.subheader("Bảng ANOVA tổng thể")

    st.dataframe(
        anova,
        width="stretch"
    )

    st.subheader("Hệ số hồi quy")

    st.dataframe(
        pd.DataFrame({
            "Biến":terms,
            "Hệ số":b
        }),
        width="stretch"
    )

    st.subheader("Lack of Fit")

    independent = st.checkbox(
        "Xác nhận các điểm tâm TN13–TN15 "
        "là các mẻ thí nghiệm độc lập"
    )

    if independent:

        groups = data.groupby([
            "Papain",
            "Thời gian",
            "Nhiệt độ"
        ])[response]

        SS_pe = sum(
            ((g-g.mean())**2).sum()
            for _,g in groups
        )

        df_pe = n-groups.ngroups
        df_lof = df_error-df_pe
        SS_lof = max(0,SSE-SS_pe)

        if (
            df_pe>0
            and df_lof>0
            and SS_pe>0
        ):

            F_lof = (
                SS_lof/df_lof
            )/(SS_pe/df_pe)

            p_lof = f.sf(
                F_lof,
                df_lof,
                df_pe
            )

            st.metric(
                "p-value Lack of Fit",
                f"{p_lof:.5f}"
            )

            if p_lof<0.05:

                st.warning(
                    "Mô hình có dấu hiệu thiếu "
                    "phù hợp. Cần xác nhận thêm."
                )

            else:

                st.info(
                    "Chưa phát hiện thiếu phù hợp "
                    "ở mức ý nghĩa 5%."
                )

        else:

            st.warning(
                "Không đủ dữ liệu sai số thuần."
            )

    st.subheader("Thực nghiệm và dự đoán")

    fig = px.scatter(
        x=Y,
        y=Y_pred,
        labels={
            "x":"Thực nghiệm",
            "y":"Dự đoán"
        },
        template="plotly_white"
    )

    fig.update_traces(
        marker=dict(
            color="#2A6F97",
            size=10
        )
    )

    lo = min(Y.min(),Y_pred.min())
    hi = max(Y.max(),Y_pred.max())

    fig.add_trace(
        go.Scatter(
            x=[lo,hi],
            y=[lo,hi],
            mode="lines",
            name="Đường lý tưởng",
            line=dict(
                color="gray",
                dash="dash"
            )
        )
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

    st.subheader("Biểu đồ phần dư")

    residual = px.scatter(
        x=Y_pred,
        y=Y-Y_pred,
        labels={
            "x":"Giá trị dự đoán",
            "y":"Phần dư"
        },
        template="plotly_white"
    )

    residual.update_traces(
        marker=dict(color="#2A6F97",size=9)
    )

    residual.add_hline(
        y=0,
        line_dash="dash"
    )

    st.plotly_chart(
        residual,
        width="stretch"
    )

# ==========================================
# 12. TOI UU HOA
# ==========================================

elif menu == "Tối ưu hóa":

    st.title("Optimization Center")

    H = np.array([
        [2*b[7],b[4],b[5]],
        [b[4],2*b[8],b[6]],
        [b[5],b[6],2*b[9]]
    ])

    opt = np.linalg.lstsq(
        H,-b[1:4],rcond=None
    )[0]

    if (
        np.all(np.abs(opt)<=1)
        and np.sum(np.abs(opt))<=2
        and np.all(np.linalg.eigvalsh(H)<0)
    ):

        P_opt = 3000+1000*opt[0]
        t_opt = 2+opt[1]
        T_opt = 55+10*opt[2]

        c1,c2,c3 = st.columns(3)

        c1.metric(
            "Papain dự đoán",
            f"{P_opt:.1f} U/g"
        )

        c2.metric(
            "Thời gian dự đoán",
            f"{t_opt:.3f} giờ"
        )

        c3.metric(
            "Nhiệt độ dự đoán",
            f"{T_opt:.2f} °C"
        )

        st.metric(
            "Đáp ứng cực đại dự đoán",
            f"{predict(P_opt,t_opt,T_opt):.5g} {unit}"
        )

    else:

        st.warning(
            "Cần thực hiện tối ưu có ràng buộc."
        )

    st.warning(
        "Điều kiện tối ưu dự đoán cần "
        "thí nghiệm xác nhận."
    )

    st.divider()

    st.subheader("Mô phỏng điều kiện thủy phân")

    p = st.slider(
        "Papain (U/g)",
        2000,4000,3000
    )

    t = st.slider(
        "Thời gian (giờ)",
        1.0,3.0,2.0,0.01
    )

    T = st.slider(
        "Nhiệt độ (°C)",
        45.0,65.0,55.0,0.1
    )

    result = predict(p,t,T)

    st.metric(
        "Đáp ứng dự đoán",
        f"{result:.5g} {unit}"
    )

    if (
        abs((p-3000)/1000)
        +abs(t-2)
        +abs((T-55)/10)>2
    ):

        st.warning(
            "Điều kiện nằm ngoài bao lồi "
            "của thiết kế Box-Behnken."
        )

# ==========================================
# 13. QUY TRINH CONG NGHE
# ==========================================

elif menu == "Quy trình công nghệ":

    st.title("Production Technology")

    st.info(
        "Tiếp nhận → Phân loại → Sơ chế"
    )

    a,c,d = st.columns(3)

    with a:

        st.markdown("### Nhánh A")

        st.write(
            "Gốc nấm kim châm"
        )

        st.write("↓")
        st.write("Thủy phân Papain")
        st.write("↓")
        st.write("Lọc dịch thủy phân")

    with c:

        st.markdown("### Nhánh B")

        st.write("Cà chua")
        st.write("↓")
        st.write("Xử lý Pectinase")
        st.write("↓")
        st.write("Thu hồi pha dịch")

    with d:

        st.markdown("### Nhánh C")

        st.write("Khoai tây")
        st.write("↓")
        st.write("Làm chín và nghiền")
        st.write("↓")
        st.write("Khảo sát phối trộn")

    st.divider()

    steps = [
        "Phối trộn ba dòng nguyên liệu",
        "Sấy",
        "Nghiền và rây",
        "Đánh giá chất lượng",
        "Prototype MYCOUMAMI"
    ]

    for i,step in enumerate(steps):

        st.markdown(
            f"""
            <div class="panel"
            style="text-align:center">
            <b style="color:#A41420">
            {i+1}. {step}
            </b>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.caption(
        "Quy trình định hướng. Các nhánh B, C "
        "và công thức cuối cần xác nhận thêm."
    )

# ==========================================
# 14. PHAT TRIEN BEN VUNG
# ==========================================

elif menu == "Phát triển bền vững":

    st.title("Sustainable Food Value Chain")

    a,c,d = st.columns(3)

    a.info(
        "KINH TẾ\n\n"
        "Nâng giá trị nguyên liệu địa phương."
    )

    c.info(
        "XÃ HỘI\n\n"
        "Kết nối nông hộ, nhà trường "
        "và doanh nghiệp."
    )

    d.info(
        "MÔI TRƯỜNG\n\n"
        "Tiềm năng tăng hiệu suất "
        "sử dụng sinh khối."
    )

    st.subheader("Chỉ số cần kiểm chứng")

    st.dataframe(
        pd.DataFrame({
            "Chỉ số":[
                "Hiệu suất thu hồi chất khô",
                "Nước sử dụng",
                "Điện năng sấy",
                "Khối lượng bã",
                "Truy xuất nguyên liệu"
            ],
            "Đơn vị":[
                "kg/kg",
                "L/kg",
                "kWh/kg",
                "kg/kg",
                "%"
            ],
            "Trạng thái":[
                "Cần đo",
                "Cần đo",
                "Cần đo",
                "Cần đo",
                "Cần xác nhận"
            ]
        }),
        width="stretch"
    )

# ==========================================
# 15. THUONG MAI HOA
# ==========================================

elif menu == "Thương mại hóa":

    st.title("Business Development")

    a,c = st.columns(2)

    with a:

        st.subheader("B2C")

        st.markdown("""
        - Hạt nêm nấm và rau củ.
        - Người tiêu dùng gia đình.
        - Hội chợ và bán thử trực tiếp.
        - Kênh bán hàng trực tuyến.
        - Cửa hàng đặc sản.
        """)

    with c:

        st.subheader("B2B")

        st.markdown("""
        - Nền vị nấm và rau củ.
        - Doanh nghiệp sản xuất súp.
        - Doanh nghiệp mì và snack.
        - Doanh nghiệp sản xuất nước sốt.
        - Thực phẩm plant-based.
        """)

    st.subheader(
        "Lộ trình thương mại hóa"
    )

    st.markdown("""
    1. Xác nhận công thức.
    2. Sản xuất pilot và kiểm nghiệm.
    3. Thử nghiệm thị trường.
    4. Chuẩn hóa chuỗi cung ứng.
    5. Mở rộng quy mô.
    """)

    st.subheader(
        "Công cụ tính giá thành"
    )

    costs = []

    for item in [
        "Nguyên liệu",
        "Enzyme",
        "Điện và nước",
        "Nhân công",
        "Bao bì",
        "Kiểm nghiệm",
        "Chi phí khác"
    ]:

        costs.append(
            st.number_input(
                item+" (VNĐ/mẻ)",
                min_value=0.0,
                step=1000.0
            )
        )

    mass = st.number_input(
        "Khối lượng thành phẩm (kg)",
        min_value=0.001,
        value=1.0
    )

    price = sum(costs)/mass

    a,c = st.columns(2)

    a.metric(
        "Tổng chi phí",
        f"{sum(costs):,.0f} VNĐ"
    )

    c.metric(
        "Giá thành dự toán",
        f"{price:,.0f} VNĐ/kg"
    )

# ==========================================
# 16. FOOTER
# ==========================================

st.divider()

st.caption(
    "MYCOUMAMI RESEARCH & INNOVATION LAB"
    " | YERSIN UNIVERSITY | FID 2026"
)

st.caption(
    "Nguồn: Báo cáo toàn văn MYCOUMAMI "
    "01.11.2026. Website phục vụ nghiên cứu "
    "và trình diễn sản phẩm."
)

