import streamlit as st

# ==============================
# CẤU HÌNH TRANG
# ==============================
st.set_page_config(
    page_title="Tính lãi tiền gửi tiết kiệm",
    page_icon="💰",
    layout="centered"
)

# ==============================
# TIÊU ĐỀ
# ==============================
st.title("💰 Ứng dụng tính lãi tiền gửi tiết kiệm")
st.write("Tính toán tiền lãi theo **lãi đơn** hoặc **lãi kép**.")

st.divider()

# ==============================
# NHẬP THÔNG TIN
# ==============================

so_tien = st.number_input(
    "💵 Số tiền gửi (VNĐ)",
    min_value=0.0,
    value=10_000_000.0,
    step=500_000.0,
    format="%.0f"
)

ky_han = st.number_input(
    "📅 Kỳ hạn (tháng)",
    min_value=1,
    value=12,
    step=1
)

lai_suat = st.number_input(
    "📈 Lãi suất (%/năm)",
    min_value=0.0,
    value=6.0,
    step=0.1,
    format="%.2f"
)

hinh_thuc_lai = st.selectbox(
    "🧮 Hình thức tính lãi",
    [
        "Lãi đơn",
        "Lãi kép"
    ]
)

hinh_thuc_nhan = st.selectbox(
    "💳 Hình thức nhận lãi",
    [
        "Lãnh lãi theo tháng",
        "Lãnh lãi theo quý",
        "Lãnh lãi cuối kỳ"
    ]
)

st.divider()

# ==============================
# NÚT TÍNH TOÁN
# ==============================

if st.button("🧮 TÍNH TIỀN LÃI", use_container_width=True):

    if so_tien <= 0:
        st.error("Vui lòng nhập số tiền gửi lớn hơn 0.")
    elif ky_han <= 0:
        st.error("Vui lòng nhập kỳ hạn lớn hơn 0.")
    elif lai_suat < 0:
        st.error("Lãi suất không được âm.")
    else:

        # Lãi suất năm chuyển sang dạng thập phân
        r = lai_suat / 100

        # Thời gian gửi tính theo năm
        t = ky_han / 12

        # ==================================
        # LÃI ĐƠN
        # ==================================
        if hinh_thuc_lai == "Lãi đơn":

            tong_lai = so_tien * r * t
            tong_tien = so_tien + tong_lai

            # Tính lãi định kỳ
            if hinh_thuc_nhan == "Lãnh lãi theo tháng":
                lai_dinh_ky = so_tien * r / 12

            elif hinh_thuc_nhan == "Lãnh lãi theo quý":
                lai_dinh_ky = so_tien * r / 4

            else:
                lai_dinh_ky = tong_lai

        # ==================================
        # LÃI KÉP
        # ==================================
        else:

            # Lãi kép theo tháng
            if hinh_thuc_nhan == "Lãnh lãi theo tháng":
                so_ky = ky_han
                lai_ky = r / 12

            # Lãi kép theo quý
            elif hinh_thuc_nhan == "Lãnh lãi theo quý":
                so_ky = ky_han / 3
                lai_ky = r / 4

            # Lãi kép cuối kỳ
            else:
                so_ky = t
                lai_ky = r

            tong_tien = so_tien * ((1 + lai_ky) ** so_ky)
            tong_lai = tong_tien - so_tien

            # Lãi của kỳ đầu tiên
            lai_dinh_ky = so_tien * lai_ky

        # ==================================
        # HIỂN THỊ KẾT QUẢ
        # ==================================

        st.success("✅ Tính toán thành công!")

        st.subheader("📊 Kết quả")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "💵 Tiền lãi định kỳ",
                f"{lai_dinh_ky:,.0f} VNĐ"
            )

        with col2:
            st.metric(
                "📈 Tổng tiền lãi",
                f"{tong_lai:,.0f} VNĐ"
            )

        st.metric(
            "💰 Tổng tiền gốc + lãi",
            f"{tong_tien:,.0f} VNĐ"
        )

        # ==================================
        # THÔNG TIN CHI TIẾT
        # ==================================

        st.divider()

        st.subheader("📋 Thông tin khoản gửi")

        st.write(f"**Số tiền gửi:** {so_tien:,.0f} VNĐ")
        st.write(f"**Kỳ hạn:** {ky_han} tháng")
        st.write(f"**Lãi suất:** {lai_suat:.2f}%/năm")
        st.write(f"**Hình thức tính:** {hinh_thuc_lai}")
        st.write(f"**Hình thức nhận lãi:** {hinh_thuc_nhan}")

        # ==================================
        # CÔNG THỨC
        # ==================================

        with st.expander("📖 Xem công thức tính"):

            if hinh_thuc_lai == "Lãi đơn":

                st.write("**Công thức lãi đơn:**")

                st.latex(
                    r"I = P \times r \times t"
                )

                st.write(
                    "Trong đó: P là số tiền gốc, "
                    "r là lãi suất năm, "
                    "t là thời gian gửi tính theo năm."
                )

            else:

                st.write("**Công thức lãi kép:**")

                st.latex(
                    r"A = P(1+r)^n"
                )

                st.write(
                    "Trong đó: P là số tiền gốc, "
                    "r là lãi suất mỗi kỳ, "
                    "n là số kỳ nhập lãi."
                )

else:
    st.info("👆 Nhập thông tin khoản tiền gửi và nhấn **TÍNH TIỀN LÃI**.")
