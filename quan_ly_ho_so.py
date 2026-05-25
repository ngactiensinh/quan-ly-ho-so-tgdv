# ==========================================
# MODULE 1: DASHBOARD - ĐÃ TỐI ƯU HÓA
# Thay thế toàn bộ phần "if menu == "📊 Dashboard":"
# trong file app.py gốc bằng đoạn code này
# ==========================================

if menu == "📊 Dashboard":
    section_title("📊", "THỐNG KÊ NHÂN SỰ TỔNG QUAN")

    if df_hoso.empty:
        st.info("📭 Chưa có dữ liệu để thống kê. Vui lòng nhập hồ sơ cán bộ trước.")
    else:
        df = df_hoso.fillna("Chưa xác định").copy()
        total  = len(df)
        nam    = len(df[df["gioi_tinh"] == "Nam"])
        nu     = len(df[df["gioi_tinh"] == "Nữ"])
        dang   = len(df[df["ngay_vao_dang"].notna() & (df["ngay_vao_dang"] != "Chưa xác định") & (df["ngay_vao_dang"] != "")])
        thac_si= len(df[df["trinh_do_chuyen_mon"].str.contains("Thạc|Tiến", case=False, na=False)])
        tyle_nu = round(nu / total * 100) if total else 0

        # ---- METRIC CARDS (hàng 1) ----
        st.markdown(f"""
        <div class="metric-grid">
            <div class="metric-card">
                <div class="m-label">👥 Tổng Cán bộ</div>
                <div class="m-value">{total}</div>
                <div class="m-sub">Biên chế chính thức toàn Ban</div>
            </div>
            <div class="metric-card gold">
                <div class="m-label">👨 Cán bộ Nam</div>
                <div class="m-value">{nam}</div>
                <div class="m-sub">{round(nam/total*100) if total else 0}% tổng số</div>
            </div>
            <div class="metric-card navy">
                <div class="m-label">👩 Cán bộ Nữ</div>
                <div class="m-value">{nu}</div>
                <div class="m-sub">{tyle_nu}% tổng số</div>
            </div>
            <div class="metric-card green">
                <div class="m-label">🎓 Thạc sĩ trở lên</div>
                <div class="m-value">{thac_si}</div>
                <div class="m-sub">{round(thac_si/total*100) if total else 0}% tổng số</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ============================================================
        # HÀNG 2: GIỚI TÍNH (Donut) + TRÌNH ĐỘ CHUYÊN MÔN (Cột ngang)
        # ============================================================
        col_a, col_b = st.columns([1, 2])

        with col_a:
            # ---- Biểu đồ Giới tính (Donut) ----
            df_gt = df[df['gioi_tinh'].isin(["Nam", "Nữ"])]['gioi_tinh'].value_counts().reset_index()
            df_gt.columns = ['Giới tính', 'Số lượng']
            if not df_gt.empty:
                fig_gt = px.pie(
                    df_gt, values='Số lượng', names='Giới tính',
                    hole=0.60,
                    color='Giới tính',
                    color_discrete_map={'Nam': '#1A2E4A', 'Nữ': '#C8102E'},
                    title='<b>Cơ cấu Giới tính</b>'
                )
                fig_gt.update_traces(
                    textposition='outside',
                    textinfo='label+percent+value',
                    textfont_size=13,
                    marker=dict(line=dict(color='#ffffff', width=3)),
                    pull=[0.04, 0.04]
                )
                fig_gt.add_annotation(
                    text=f"<b>{total}</b><br>CB",
                    x=0.5, y=0.5, showarrow=False,
                    font=dict(size=20, color='#1A2E4A', family='Merriweather')
                )
                fig_gt.update_layout(
                    font_family="Source Sans 3",
                    title_font=dict(size=14, color='#1A2E4A'),
                    title_x=0.5,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    showlegend=True,
                    legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5, font=dict(size=12)),
                    margin=dict(t=50, b=30, l=20, r=20),
                    height=320
                )
                st.plotly_chart(fig_gt, use_container_width=True)

        with col_b:
            # ---- Biểu đồ Trình độ Chuyên môn (Cột dọc, màu gradient đỏ) ----
            df_cm = df[df['trinh_do_chuyen_mon'] != 'Chưa xác định']['trinh_do_chuyen_mon'].value_counts().reset_index()
            df_cm.columns = ['Trình độ', 'Số lượng']
            df_cm = df_cm.sort_values('Số lượng', ascending=False)

            if not df_cm.empty:
                # Tạo thang màu từ đỏ đậm -> đỏ nhạt
                n = len(df_cm)
                colors_cm = [f'rgba({int(168 + (232-168)*i/(max(n-1,1)))},{int(12 + (32-12)*i/(max(n-1,1)))},{int(35 + (63-35)*i/(max(n-1,1)))},0.85)' for i in range(n)]

                fig_cm = go.Figure(go.Bar(
                    x=df_cm['Trình độ'],
                    y=df_cm['Số lượng'],
                    marker_color=colors_cm,
                    marker_line=dict(color='#ffffff', width=1.5),
                    text=df_cm['Số lượng'],
                    textposition='outside',
                    textfont=dict(size=14, color='#1A2E4A', family='Merriweather'),
                    hovertemplate='<b>%{x}</b><br>Số lượng: %{y} người<extra></extra>'
                ))
                fig_cm.update_layout(
                    title=dict(text='<b>Trình độ Chuyên môn</b>', x=0.5, font=dict(size=14, color='#1A2E4A')),
                    font_family="Source Sans 3",
                    plot_bgcolor='rgba(248,244,239,0.6)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    xaxis=dict(
                        title=None,
                        tickfont=dict(size=11, color='#3D3D5C'),
                        gridcolor='rgba(0,0,0,0)',
                        linecolor='#D4AF37', linewidth=1.5
                    ),
                    yaxis=dict(
                        title='Số người',
                        tickfont=dict(size=11),
                        gridcolor='rgba(212,175,55,0.15)',
                        zeroline=False
                    ),
                    margin=dict(t=55, b=20, l=40, r=20),
                    height=320,
                    bargap=0.35
                )
                st.plotly_chart(fig_cm, use_container_width=True)

        # ============================================================
        # HÀNG 3: NGẠCH CÔNG CHỨC + LÝ LUẬN CHÍNH TRỊ
        # ============================================================
        col_c, col_d = st.columns(2)

        with col_c:
            # ---- Biểu đồ Ngạch Công chức (Cột ngang - navy) ----
            df_ng = df[df['ngach_cong_chuc'] != 'Chưa xác định']['ngach_cong_chuc'].value_counts().reset_index()
            df_ng.columns = ['Ngạch', 'Số lượng']
            df_ng = df_ng.sort_values('Số lượng', ascending=True)

            if not df_ng.empty:
                n2 = len(df_ng)
                colors_ng = [f'rgba({int(10 + (42-10)*i/(max(n2-1,1)))},{int(22 + (74-22)*i/(max(n2-1,1)))},{int(40 + (112-40)*i/(max(n2-1,1)))},0.85)' for i in range(n2)]

                fig_ng = go.Figure(go.Bar(
                    y=df_ng['Ngạch'],
                    x=df_ng['Số lượng'],
                    orientation='h',
                    marker_color=colors_ng,
                    marker_line=dict(color='#D4AF37', width=0.8),
                    text=df_ng['Số lượng'],
                    textposition='outside',
                    textfont=dict(size=13, color='#1A2E4A', family='Merriweather'),
                    hovertemplate='<b>%{y}</b><br>Số lượng: %{x} người<extra></extra>'
                ))
                fig_ng.update_layout(
                    title=dict(text='<b>Ngạch Công chức hiện hưởng</b>', x=0.5, font=dict(size=14, color='#1A2E4A')),
                    font_family="Source Sans 3",
                    plot_bgcolor='rgba(248,244,239,0.6)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    xaxis=dict(
                        title='Số người',
                        tickfont=dict(size=11),
                        gridcolor='rgba(212,175,55,0.15)',
                        zeroline=False
                    ),
                    yaxis=dict(
                        title=None,
                        tickfont=dict(size=11, color='#1A2E4A'),
                        gridcolor='rgba(0,0,0,0)',
                        linecolor='#D4AF37', linewidth=1.5,
                        automargin=True
                    ),
                    margin=dict(t=55, b=20, l=10, r=50),
                    height=340,
                    bargap=0.3
                )
                st.plotly_chart(fig_ng, use_container_width=True)
            else:
                st.info("Chưa có dữ liệu ngạch công chức.")

        with col_d:
            # ---- Biểu đồ Lý luận Chính trị (Cột ngang - vàng) ----
            # Sắp xếp theo thứ tự chuẩn chính trị
            thu_tu_ll = ["Chưa qua đào tạo", "Sơ cấp", "Trung cấp", "Cao cấp", "Cử nhân"]
            df_ll_raw = df[df['ly_luan_chinh_tri'] != 'Chưa xác định']['ly_luan_chinh_tri'].value_counts().reset_index()
            df_ll_raw.columns = ['Lý luận CT', 'Số lượng']
            # Sắp xếp theo thứ tự quy định
            df_ll_raw['Lý luận CT'] = pd.Categorical(df_ll_raw['Lý luận CT'], categories=thu_tu_ll, ordered=True)
            df_ll = df_ll_raw.sort_values('Lý luận CT', ascending=True).dropna()

            if not df_ll.empty:
                color_map_ll = {
                    "Chưa qua đào tạo": "rgba(180,180,180,0.7)",
                    "Sơ cấp":           "rgba(212,175,55,0.55)",
                    "Trung cấp":        "rgba(212,175,55,0.72)",
                    "Cao cấp":          "rgba(212,175,55,0.90)",
                    "Cử nhân":          "rgba(184,134,11,0.95)"
                }
                bar_colors_ll = [color_map_ll.get(x, "rgba(212,175,55,0.7)") for x in df_ll['Lý luận CT'].astype(str)]

                fig_ll = go.Figure(go.Bar(
                    y=df_ll['Lý luận CT'].astype(str),
                    x=df_ll['Số lượng'],
                    orientation='h',
                    marker_color=bar_colors_ll,
                    marker_line=dict(color='#8B6914', width=0.8),
                    text=df_ll['Số lượng'],
                    textposition='outside',
                    textfont=dict(size=13, color='#1A2E4A', family='Merriweather'),
                    hovertemplate='<b>%{y}</b><br>Số lượng: %{x} người<extra></extra>'
                ))
                fig_ll.update_layout(
                    title=dict(text='<b>Trình độ Lý luận Chính trị</b>', x=0.5, font=dict(size=14, color='#1A2E4A')),
                    font_family="Source Sans 3",
                    plot_bgcolor='rgba(248,244,239,0.6)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    xaxis=dict(
                        title='Số người',
                        tickfont=dict(size=11),
                        gridcolor='rgba(212,175,55,0.15)',
                        zeroline=False
                    ),
                    yaxis=dict(
                        title=None,
                        tickfont=dict(size=11, color='#1A2E4A'),
                        gridcolor='rgba(0,0,0,0)',
                        linecolor='#D4AF37', linewidth=1.5
                    ),
                    margin=dict(t=55, b=20, l=10, r=50),
                    height=340,
                    bargap=0.3
                )
                st.plotly_chart(fig_ll, use_container_width=True)
            else:
                st.info("Chưa có dữ liệu lý luận chính trị.")

        # ============================================================
        # HÀNG 4: HỌC VỊ (Donut + bảng chú thích) - FULL WIDTH
        # ============================================================
        section_title("🎓", "CƠ CẤU HỌC VỊ VÀ ĐẢNG VỤ")
        col_e, col_f = st.columns([1.4, 1])

        with col_e:
            # ---- Biểu đồ Học vị ----
            df_hv = df[
                (df['hoc_vi'] != 'Chưa xác định') & (df['hoc_vi'] != '') & (df['hoc_vi'] != '—')
            ]['hoc_vi'].value_counts().reset_index()
            df_hv.columns = ['Học vị', 'Số lượng']

            # Gộp các CB chưa có học vị vào "Đại học / Chưa có học vị"
            co_hoc_vi = set(df_hv['Học vị'].tolist())
            chua_hoc_vi = total - df_hv['Số lượng'].sum()
            if chua_hoc_vi > 0:
                new_row = pd.DataFrame([{'Học vị': 'Đại học / Chưa có học vị', 'Số lượng': chua_hoc_vi}])
                df_hv = pd.concat([df_hv, new_row], ignore_index=True)

            # Bảng màu sang trọng
            palette_hv = ['#0A1628', '#1A2E4A', '#2A4A70', '#C8102E', '#A00C23', '#D4AF37', '#B8860B', '#6B7280']

            fig_hv = go.Figure(go.Pie(
                labels=df_hv['Học vị'],
                values=df_hv['Số lượng'],
                hole=0.55,
                marker=dict(
                    colors=palette_hv[:len(df_hv)],
                    line=dict(color='#ffffff', width=3)
                ),
                textinfo='label+percent',
                textposition='outside',
                textfont=dict(size=12, color='#1A2E4A'),
                pull=[0.04] * len(df_hv),
                hovertemplate='<b>%{label}</b><br>Số người: %{value}<br>Tỷ lệ: %{percent}<extra></extra>'
            ))
            fig_hv.add_annotation(
                text="<b>Học vị</b>",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=13, color='#1A2E4A', family='Source Sans 3')
            )
            fig_hv.update_layout(
                title=dict(text='<b>Cơ cấu Học vị cán bộ</b>', x=0.5, font=dict(size=14, color='#1A2E4A')),
                font_family="Source Sans 3",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                showlegend=True,
                legend=dict(
                    orientation="v", yanchor="middle", y=0.5,
                    xanchor="left", x=1.02,
                    font=dict(size=11, color='#1A2E4A'),
                    bgcolor='rgba(253,248,240,0.8)',
                    bordercolor='#D4AF37', borderwidth=1
                ),
                margin=dict(t=55, b=20, l=20, r=160),
                height=360
            )
            st.plotly_chart(fig_hv, use_container_width=True)

        with col_f:
            # ---- Thống kê đảng viên + bảng tóm tắt ----
            tyle_dang = round(dang / total * 100) if total else 0
            tyle_nu_str = f"{tyle_nu}%"

            st.markdown(f"""
            <div style="background:#fff;border-radius:12px;padding:22px 24px;
                border-left:5px solid #D4AF37;box-shadow:0 4px 20px rgba(0,0,0,0.08);
                margin-top:8px;">
                <div style="font-family:'Merriweather',serif;font-size:13px;font-weight:700;
                    color:#0A1628;letter-spacing:1px;text-transform:uppercase;
                    border-bottom:1px dashed rgba(212,175,55,0.4);padding-bottom:10px;margin-bottom:14px;">
                    📋 Bảng Tổng hợp Chỉ tiêu
                </div>
                <table style="width:100%;border-collapse:collapse;font-size:13px;">
                    <tr style="background:rgba(200,16,46,0.06);">
                        <td style="padding:9px 10px;color:#6B7280;font-weight:600;">👥 Tổng biên chế</td>
                        <td style="padding:9px 10px;text-align:right;font-weight:900;color:#C8102E;font-family:'Merriweather',serif;font-size:16px;">{total}</td>
                    </tr>
                    <tr>
                        <td style="padding:9px 10px;color:#6B7280;font-weight:600;">👨 Cán bộ Nam</td>
                        <td style="padding:9px 10px;text-align:right;font-weight:700;color:#1A2E4A;">{nam} ({round(nam/total*100) if total else 0}%)</td>
                    </tr>
                    <tr style="background:rgba(212,175,55,0.05);">
                        <td style="padding:9px 10px;color:#6B7280;font-weight:600;">👩 Cán bộ Nữ</td>
                        <td style="padding:9px 10px;text-align:right;font-weight:700;color:#C8102E;">{nu} ({tyle_nu}%)</td>
                    </tr>
                    <tr>
                        <td style="padding:9px 10px;color:#6B7280;font-weight:600;">☭ Đảng viên</td>
                        <td style="padding:9px 10px;text-align:right;font-weight:700;color:#1A2E4A;">{dang} ({tyle_dang}%)</td>
                    </tr>
                    <tr style="background:rgba(200,16,46,0.06);">
                        <td style="padding:9px 10px;color:#6B7280;font-weight:600;">🎓 Thạc sĩ trở lên</td>
                        <td style="padding:9px 10px;text-align:right;font-weight:700;color:#2E7D32;">{thac_si} ({round(thac_si/total*100) if total else 0}%)</td>
                    </tr>
                    <tr>
                        <td style="padding:9px 10px;color:#6B7280;font-weight:600;">🏛️ Lý luận Cao cấp/CN</td>
                        <td style="padding:9px 10px;text-align:right;font-weight:700;color:#B8860B;">
                        {len(df[df['ly_luan_chinh_tri'].isin(['Cao cấp','Cử nhân'])])} người
                        </td>
                    </tr>
                    <tr style="background:rgba(212,175,55,0.05);">
                        <td style="padding:9px 10px;color:#6B7280;font-weight:600;">📅 Cập nhật lần cuối</td>
                        <td style="padding:9px 10px;text-align:right;font-weight:600;color:#6B7280;font-size:11px;">{datetime.now().strftime('%d/%m/%Y %H:%M')}</td>
                    </tr>
                </table>
            </div>
            """, unsafe_allow_html=True)

        # ============================================================
        # HÀNG 5: DANH SÁCH CÁN BỘ
        # ============================================================
        section_title("📋", "DANH SÁCH CÁN BỘ, CÔNG CHỨC")
        cols_show = ['id', 'ho_ten', 'chuc_vu', 'don_vi', 'ngay_sinh', 'gioi_tinh', 'hoc_vi', 'trinh_do_chuyen_mon', 'ly_luan_chinh_tri', 'ngach_cong_chuc']
        df_show = df[[c for c in cols_show if c in df.columns]].rename(columns={
            'id': 'Mã CB', 'ho_ten': 'Họ và tên', 'chuc_vu': 'Chức vụ', 'don_vi': 'Đơn vị',
            'ngay_sinh': 'Ngày sinh', 'gioi_tinh': 'Giới tính',
            'hoc_vi': 'Học vị', 'trinh_do_chuyen_mon': 'Chuyên môn',
            'ly_luan_chinh_tri': 'Lý luận CT', 'ngach_cong_chuc': 'Ngạch CC'
        })
        # Lọc bỏ các hàng "Chưa xác định" cho hiển thị gọn
        st.dataframe(df_show, hide_index=True, use_container_width=True)

        # Nút xuất danh sách
        csv_data = df_show.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')
        st.download_button(
            label="📥  XUẤT DANH SÁCH (.CSV)",
            data=csv_data,
            file_name=f"DanhSach_CBCC_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
