# -*- coding: utf-8 -*-
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily

# 1. Đăng ký font tiếng Việt (Times New Roman hỗ trợ unicode đầy đủ trên Windows)
FONT_DIR = r"C:\Windows\Fonts"
times_regular = os.path.join(FONT_DIR, "times.ttf")
times_bold = os.path.join(FONT_DIR, "timesbd.ttf")
times_italic = os.path.join(FONT_DIR, "timesi.ttf")
times_bold_italic = os.path.join(FONT_DIR, "timesbi.ttf")

pdfmetrics.registerFont(TTFont('TimesNewRoman', times_regular))
pdfmetrics.registerFont(TTFont('TimesNewRoman-Bold', times_bold))
pdfmetrics.registerFont(TTFont('TimesNewRoman-Italic', times_italic))
pdfmetrics.registerFont(TTFont('TimesNewRoman-BoldItalic', times_bold_italic))

registerFontFamily('TimesNewRoman', normal='TimesNewRoman', bold='TimesNewRoman-Bold', italic='TimesNewRoman-Italic', boldItalic='TimesNewRoman-BoldItalic')

# 2. Định nghĩa Palette màu sắc (Đồng bộ với theme Streamlit xanh lá đậm thanh lịch)
COLOR_PRIMARY = colors.HexColor('#0D5C3A')    # Xanh lá đậm
COLOR_SECONDARY = colors.HexColor('#F59E0B')  # Hổ phách/cam nhạt
COLOR_DARK = colors.HexColor('#1E293B')       # Chữ chính xám tối
COLOR_MUTED = colors.HexColor('#64748B')      # Chữ chú thích xám trung bình
COLOR_BG_LIGHT = colors.HexColor('#F8FAFC')   # Nền hộp callout xám nhạt
COLOR_BORDER = colors.HexColor('#E2E8F0')     # Đường viền xám nhạt

# 3. Tạo mẫu PDF với Header/Footer tự động
from reportlab.pdfgen import canvas
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        page_count = len(self._saved_page_states)
        for page in self._saved_page_states:
            self.__dict__.update(page)
            self.draw_page_number(page_count)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("TimesNewRoman", 9)
        self.setFillColor(COLOR_MUTED)
        
        # Không vẽ header/footer ở trang bìa
        if self._pageNumber > 1:
            # Header (Sentence case)
            self.drawString(54, 750, "Báo cáo phân tích tác động của trí tuệ nhân tạo đối với lực lượng lao động công nghệ và dữ liệu")
            self.setStrokeColor(COLOR_PRIMARY)
            self.setLineWidth(0.5)
            self.line(54, 742, 558, 742)
            
            # Footer (Sentence case)
            page_text = f"Trang {self._pageNumber} / {page_count}"
            self.drawRightString(558, 40, page_text)
            self.drawString(54, 40, "Dự án nghiên cứu phân tích định vị tác vụ công việc và lộ trình reskilling")
            self.line(54, 52, 558, 52)
            
        self.restoreState()

def build_pdf(filename="Báo cáo phân tích tác động của trí tuệ nhân tạo đối với lực lượng lao động công nghệ và dữ liệu.pdf"):
    # Tạo tài liệu kích thước Letter, lề 0.75 inch (54 points)
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=72,
        bottomMargin=72
    )

    styles = getSampleStyleSheet()
    
    # Định nghĩa các styles mới dựa trên Times New Roman tiếng Việt
    style_normal = ParagraphStyle(
        'VietNormal',
        parent=styles['Normal'],
        fontName='TimesNewRoman',
        fontSize=11,
        leading=16,
        textColor=COLOR_DARK
    )
    
    style_bold = ParagraphStyle(
        'VietBold',
        parent=style_normal,
        fontName='TimesNewRoman-Bold'
    )
    
    style_italic = ParagraphStyle(
        'VietItalic',
        parent=style_normal,
        fontName='TimesNewRoman-Italic'
    )
    
    style_title = ParagraphStyle(
        'VietTitle',
        parent=style_normal,
        fontName='TimesNewRoman-Bold',
        fontSize=20,
        leading=26,
        textColor=COLOR_PRIMARY,
        alignment=1, # Center
        spaceAfter=15
    )
    
    style_subtitle = ParagraphStyle(
        'VietSubtitle',
        parent=style_normal,
        fontSize=12,
        leading=18,
        textColor=COLOR_MUTED,
        alignment=1, # Center
        spaceAfter=40
    )
    
    style_h1 = ParagraphStyle(
        'VietH1',
        parent=style_normal,
        fontName='TimesNewRoman-Bold',
        fontSize=15,
        leading=20,
        textColor=COLOR_PRIMARY,
        spaceBefore=18,
        spaceAfter=10,
        keepWithNext=True
    )
    
    style_h2 = ParagraphStyle(
        'VietH2',
        parent=style_normal,
        fontName='TimesNewRoman-Bold',
        fontSize=12,
        leading=16,
        textColor=COLOR_PRIMARY,
        spaceBefore=12,
        spaceAfter=8,
        keepWithNext=True
    )

    style_callout = ParagraphStyle(
        'VietCallout',
        parent=style_normal,
        fontName='TimesNewRoman-Italic',
        fontSize=10,
        leading=15,
        textColor=COLOR_PRIMARY
    )

    story = []



    # =========================================================================
    # TRANG 1: Hiện trạng nhân sự và bản đồ rủi ro công nghiệp (Dữ liệu gốc O*NET Mỹ)
    # =========================================================================
    story.append(Paragraph("Trang 1: Hiện trạng nhân sự và bản đồ rủi ro công nghiệp", style_h1))
    story.append(Paragraph(
        "Trang này đi sâu vào cấp độ tác vụ công việc để đối chiếu mong muốn của lập trình viên và năng lực thực tế của AI. "
        "Dữ liệu nền tảng được trích xuất từ cơ sở dữ liệu O*NET của Mỹ (WorkBank), phản ánh cấu trúc tác vụ chuẩn hóa quốc tế của ngành công nghệ.",
        style_normal
    ))
    story.append(Spacer(1, 10))

    story.append(Paragraph("1. Cơ cấu thâm niên và kinh nghiệm làm việc", style_h2))
    story.append(Paragraph(
        "Thông qua dữ liệu khảo sát thâm niên làm việc của nhân sự ngành công nghệ, chúng ta thiết lập cơ cấu phân bổ kinh nghiệm. "
        "Cơ cấu này đóng vai trò quan trọng khi đối chiếu với mức độ phức tạp của tác vụ: nhân sự có thâm niên cao thường thực thi các tác vụ đòi hỏi khả năng phán đoán cao, "
        "trong khi nhân sự Junior (dưới 2 năm kinh nghiệm) chủ yếu xử lý các tác vụ lặp đi lặp lại và dễ bị tự động hóa.",
        style_normal
    ))
    story.append(Spacer(1, 10))

    story.append(Paragraph("2. Phân cụm tác vụ bằng thuật toán K-Means", style_h2))
    story.append(Paragraph(
        "Để định vị cấu trúc rủi ro một cách khách quan, thuật toán học máy K-Means được áp dụng để phân nhóm toàn bộ các tác vụ công việc thành 4 phân cụm (vùng rủi ro) "
        "dựa trên sự kết hợp đa chiều của 6 chỉ số cốt lõi: khả năng tự động hóa của chuyên gia, mong muốn tự động hóa của lập trình viên, yêu cầu chuyên môn nghiệp vụ, "
        "mức độ bất định của tác vụ, yêu cầu giao tiếp tương tác con người, và mức lương trung bình năm của ngành.",
        style_normal
    ))
    story.append(Spacer(1, 10))

    # Bảng định nghĩa 4 phân cụm (Sentence case)
    cluster_data = [
        [Paragraph("<b>Vùng rủi ro (K-Means)</b>", style_bold), Paragraph("<b>Hệ số điều chỉnh tốc độ (m)</b>", style_bold), Paragraph("<b>Mô tả đặc trưng tác vụ</b>", style_bold)],
        [Paragraph("Vùng an toàn (Safe zone)", style_normal), Paragraph("0.5", style_normal), Paragraph("Yêu cầu chuyên môn cao, mức lương lớn, khả năng tự động hóa thấp.", style_normal)],
        [Paragraph("Vùng ổn định (Stable zone)", style_normal), Paragraph("0.8", style_normal), Paragraph("Yêu cầu giao tiếp tương tác liên nhân sự cao, rủi ro AI ở mức trung bình thấp.", style_normal)],
        [Paragraph("Vùng tiềm ẩn nguy cơ (At-risk zone)", style_normal), Paragraph("1.2", style_normal), Paragraph("AI có khả năng tự động hóa trung bình khá, lương trung bình.", style_normal)],
        [Paragraph("Vùng báo động (Alert zone)", style_normal), Paragraph("1.5", style_normal), Paragraph("Tác vụ lặp lại, yêu cầu chuyên môn thấp, dễ bị thay thế nhất.", style_normal)],
    ]
    cluster_table = Table(cluster_data, colWidths=[140, 100, 260])
    cluster_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), COLOR_PRIMARY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('GRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, COLOR_BG_LIGHT]),
    ]))
    # Sửa chữ trắng trong header của bảng
    for i in range(3):
        cluster_data[0][i].style.textColor = colors.white
        
    story.append(cluster_table)
    story.append(Spacer(1, 10))
    
    # Hộp Callout tóm tắt kết quả
    callout_1_data = [[
        Paragraph(
            "<b>Nhận định cốt lõi:</b> Bản đồ tác vụ từ dữ liệu gốc O*NET của Mỹ cho thấy ranh giới rõ ràng giữa các tác vụ thô sơ "
            "(thuộc Vùng báo động) và các tác vụ kiến trúc hệ thống chuyên sâu (thuộc Vùng an toàn). K-Means đã chứng minh "
            "rằng mức lương và yêu cầu chuyên môn tỷ lệ nghịch với rủi ro tự động hóa của AI.",
            style_callout
        )
    ]]
    callout_table_1 = Table(callout_1_data, colWidths=[500])
    callout_table_1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), COLOR_BG_LIGHT),
        ('BOX', (0,0), (-1,-1), 1, COLOR_PRIMARY),
        ('LEFTPADDING', (0,0), (-1,-1), 15),
        ('RIGHTPADDING', (0,0), (-1,-1), 15),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(callout_table_1)
    
    story.append(PageBreak())

    # =========================================================================
    # TRANG 2: Động lực chuyển giao và tấm khiên phòng ngự con người (Dữ liệu gốc O*NET Mỹ)
    # =========================================================================
    story.append(Paragraph("Trang 2: Động lực chuyển giao và tấm khiên phòng ngự con người", style_h1))
    story.append(Paragraph(
        "Để hiểu rõ tại sao và làm thế nào người lao động có thể tự bảo vệ trước làn sóng tự động hóa, "
        "báo cáo phân tích hai khía cạnh: động cơ thúc đẩy họ chuyển giao tác vụ cho AI và các rào cản phòng ngự phi kỹ thuật.",
        style_normal
    ))
    story.append(Spacer(1, 10))

    story.append(Paragraph("1. Động lực thúc đẩy tự động hóa tác vụ", style_h2))
    story.append(Paragraph(
        "Lập trình viên có xu hướng chuyển giao các tác vụ nhàm chán, lặp đi lặp lại hoặc đòi hỏi tốc độ xử lý nhanh cho AI. "
        "Mong muốn tự động hóa của người lao động tỷ lệ thuận với tần suất lặp lại của tác vụ. Tuy nhiên, việc tự động hóa quá mức "
        "có thể dẫn đến sự suy giảm tư duy phản biện độc lập.",
        style_normal
    ))
    story.append(Spacer(1, 10))

    story.append(Paragraph("2. Mật độ phân bổ rào cản phòng thủ phi kỹ thuật", style_h2))
    story.append(Paragraph(
        "Hai chiều rào cản phi kỹ thuật quan trọng nhất bảo vệ con người trước AI là: (1) mức độ bất định của tác vụ (Involved Uncertainty) "
        "và (2) yêu cầu giao tiếp tương tác liên nhân sự (Interpersonal Communication Requirement). "
        "Dữ liệu cho thấy các tác vụ đòi hỏi sự thích ứng nhanh với môi trường thay đổi hoặc sự thấu cảm, thương lượng giữa con người "
        "vẫn nằm ngoài khả năng xử lý hoàn toàn của các mô hình AI hiện tại.",
        style_normal
    ))
    story.append(Spacer(1, 10))

    story.append(Paragraph("3. Bẫy năng lực từ AI agent và độ lệch kiểm duyệt (Verification Deficit)", style_h2))
    story.append(Paragraph(
        "Khảo sát thực tế chỉ ra một hiện tượng đáng báo động: **Độ lệch kiểm duyệt (Verification Deficit)**. "
        "Nhóm Junior (dưới 2 năm kinh nghiệm) có xu hướng chấp nhận ngay lập tức kết quả đầu ra của các AI agent mà không qua kiểm chứng, "
        "dẫn đến tích lũy kinh nghiệm thực tế bằng không và dễ bị mắc kẹt mãi ở trình độ cơ bản. "
        "Ngược lại, nhóm Senior sử dụng AI như một công cụ tăng năng suất, đồng thời áp dụng năng lực chuyên môn để phát hiện và sửa đổi các lỗi logic do AI tạo ra.",
        style_normal
    ))
    story.append(Spacer(1, 10))

    callout_2_data = [[
        Paragraph(
            "<b>Nhận định cốt lõi:</b> Sự chênh lệch trong sử dụng LLM giữa Senior và Junior chứng minh rằng: "
            "AI không thay thế người có kinh nghiệm, mà thay thế những người phụ thuộc hoàn toàn vào nó mà không hiểu bản chất. "
            "Rào cản phi kỹ thuật chính là tấm khiên vững chắc nhất bảo vệ vị thế của lập trình viên.",
            style_callout
        )
    ]]
    callout_table_2 = Table(callout_2_data, colWidths=[500])
    callout_table_2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), COLOR_BG_LIGHT),
        ('BOX', (0,0), (-1,-1), 1, COLOR_PRIMARY),
        ('LEFTPADDING', (0,0), (-1,-1), 15),
        ('RIGHTPADDING', (0,0), (-1,-1), 15),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(callout_table_2)

    story.append(PageBreak())

    # =========================================================================
    # TRANG 3: Mô phỏng đà phát triển AI và dự báo rủi ro tác vụ (Vận dụng Việt Nam)
    # =========================================================================
    story.append(Paragraph("Trang 3: Mô phỏng đà phát triển AI và dự báo rủi ro tác vụ tại Việt Nam", style_h1))
    story.append(Paragraph(
        "Trang này chuyển trọng tâm phân tích từ dữ liệu tĩnh sang mô phỏng động, chính thức vận dụng điều kiện thực tế của Việt Nam "
        "để tính toán rủi ro tự động hóa qua các mốc thời gian từ 2025 đến 2030.",
        style_normal
    ))
    story.append(Spacer(1, 10))

    story.append(Paragraph("1. Mô hình toán học giả lập đà phát triển AI", style_h2))
    story.append(Paragraph(
        "Mô hình giả lập đà phát triển AI áp dụng quy luật hàm số mũ để dự báo năng lực công nghệ dựa trên hai thông số quốc gia:<br/>"
        "&nbsp;&nbsp;&bull;&nbsp;&nbsp;<b>Tốc độ phát triển AI tại Mỹ (g_US):</b> Cố định ở mức 24.1% năm.<br/>"
        "&nbsp;&nbsp;&bull;&nbsp;&nbsp;<b>Tốc độ phát triển AI tại Việt Nam (g_VN):</b> Đạt mức 20.0% năm.<br/>"
        "&nbsp;&nbsp;&bull;&nbsp;&nbsp;<b>Chỉ số sẵn sàng AI (Readiness Index - K_Readiness):</b> Tỷ lệ sẵn sàng công nghệ của Việt Nam so với Mỹ đạt 59.98 / 88.36 (khoảng 67.9%).",
        style_normal
    ))
    story.append(Spacer(1, 10))

    # Công thức toán học
    story.append(Paragraph("Công thức dự báo năng lực AI tại Việt Nam theo thời gian t:", style_bold))
    story.append(Paragraph(
        "<i>AI_VN(t) = AI_US(0) * K_Readiness * (1 + g_VN * m)^n</i>",
        style_normal
    ))
    story.append(Paragraph(
        "Trong đó, <i>n = t - 2025</i> là số năm mô phỏng, và <i>m</i> là hệ số điều chỉnh tốc độ từ phân cụm K-Means. "
        "Hệ số <i>m</i> lớn hơn ở Vùng báo động (1.5) đẩy nhanh tốc độ tự động hóa các tác vụ lặp đi lặp lại.",
        style_italic
    ))
    story.append(Spacer(1, 10))

    story.append(Paragraph("2. Bất đối xứng công nghệ và sự lệ thuộc lõi", style_h2))
    story.append(Paragraph(
        "Sự nguy hiểm vĩ mô đối với Việt Nam nằm ở **chênh lệch tấm khiên thích ứng**. "
        "Mỹ sở hữu hạ tầng đám mây khổng lồ và làm chủ các mô hình AI gốc (LLM foundation models). "
        "Trong khi đó, Việt Nam chủ yếu đóng vai trò ứng dụng API từ nước ngoài. Khi Mỹ phát triển AI nhanh hơn Việt Nam, "
        "các tập đoàn đa quốc gia sẽ tự động hóa nhanh chóng các dịch vụ thuê ngoài (offshoring), đe dọa trực tiếp đến mô hình "
        "gia công phần mềm cơ bản (IT outsourcing) - nguồn thu và việc làm chính của lao động công nghệ Việt Nam hiện tại.",
        style_normal
    ))
    story.append(Spacer(1, 10))

    callout_3_data = [[
        Paragraph(
            "<b>Nhận định cốt lõi:</b> Khoảng cách sẵn sàng công nghệ (59.98 vs 88.36) khiến Việt Nam dễ bị tổn thương "
            "trước các cú sốc tự động hóa toàn cầu. Tốc độ phát triển AI nhanh ở Mỹ không phải là cơ hội, mà là nguy cơ vĩ mô "
            "nếu Việt Nam không nhanh chóng nâng cao năng lực tự chủ công nghệ.",
            style_callout
        )
    ]]
    callout_table_3 = Table(callout_3_data, colWidths=[500])
    callout_table_3.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), COLOR_BG_LIGHT),
        ('BOX', (0,0), (-1,-1), 1, COLOR_PRIMARY),
        ('LEFTPADDING', (0,0), (-1,-1), 15),
        ('RIGHTPADDING', (0,0), (-1,-1), 15),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(callout_table_3)

    story.append(PageBreak())

    # =========================================================================
    # TRANG 4: Hệ thống khuyến nghị dịch chuyển nghề nghiệp và định hướng chiến lược (Vận dụng Việt Nam)
    # =========================================================================
    story.append(Paragraph("Trang 4: Hệ thống khuyến nghị dịch chuyển nghề nghiệp và định hướng chiến lược", style_h1))
    story.append(Paragraph(
        "Để hỗ trợ lực lượng lao động chủ động ứng phó, trang này trình bày thuật toán đề xuất dịch chuyển sự nghiệp tối ưu "
        "và các khuyến nghị chính sách vĩ mô cho Việt Nam.",
        style_normal
    ))
    story.append(Spacer(1, 10))

    story.append(Paragraph("1. La bàn dịch chuyển sự nghiệp và chỉ số Jaccard", style_h2))
    story.append(Paragraph(
        "Thuật toán đề xuất dịch chuyển dựa trên ba điều kiện ràng buộc tối ưu hóa:<br/>"
        "&nbsp;&nbsp;&bull;&nbsp;&nbsp;<b>Ràng buộc an toàn:</b> Rủi ro AI của ngành mục tiêu phải thấp hơn ngành gốc.<br/>"
        "&nbsp;&nbsp;&bull;&nbsp;&nbsp;<b>Ràng buộc thu nhập:</b> Mức lương ngành mục tiêu tối thiểu bằng 85% lương gốc (quy đổi VND thực tế).<br/>"
        "&nbsp;&nbsp;&bull;&nbsp;&nbsp;<b>Chỉ số tương đồng Jaccard (Jaccard Similarity Index):</b> Đạt tối thiểu 20% (J >= 20%). Chỉ số này đo lường sự chồng chéo kỹ năng giữa hai ngành nghề.",
        style_normal
    ))
    story.append(Spacer(1, 10))

    story.append(Paragraph("2. Chỉ số độ sẵn sàng chuyển đổi (Transition Readiness Score - TRS)", style_h2))
    story.append(Paragraph(
        "Thay vì sử dụng thuật ngữ 'gánh nặng đào tạo lại' gây nản lòng cho người lao động, chỉ số TRS (100% - RLI) thể hiện "
        "tỷ lệ % kỹ năng cũ có thể tái sử dụng ngay trong công việc mới. Đồng thời, hệ thống phân rã các kỹ năng mới cần học thành:<br/>"
        "&nbsp;&nbsp;&bull;&nbsp;&nbsp;<b>Tác vụ bổ trợ dễ học:</b> Các kỹ năng nhẹ nhàng, dễ học nhanh qua các khóa ngắn hạn.<br/>"
        "&nbsp;&nbsp;&bull;&nbsp;&nbsp;<b>Tác vụ chuyên sâu cần học:</b> Kỹ năng cốt lõi đòi hỏi đào tạo bài bản.",
        style_normal
    ))
    story.append(Spacer(1, 10))

    story.append(Paragraph("3. Khuyến nghị chính sách vĩ mô cho Việt Nam", style_h2))
    story.append(Paragraph(
        "<b>Dịch chuyển chuỗi giá trị IT:</b> Dịch chuyển từ gia công phần mềm cơ bản (IT outsourcing viết mã cơ bắp) "
        "lên các tác vụ có giá trị gia tăng cao thuộc Vùng an toàn như thiết kế hệ thống, kiến trúc giải pháp.<br/>"
        "<b>Tối ưu hóa lộ trình thích ứng và giảm độ trễ đào tạo lại:</b> Áp dụng chỉ số TRS để xây dựng lộ trình học tập cuốn chiếu, "
        "phân tách rõ kỹ năng bổ trợ và kỹ năng chuyên sâu để người lao động thích nghi từng bước mà không bị ngợp.<br/>"
        "<b>Tăng cường tấm khiên thích ứng quốc gia:</b> Chính phủ cần đẩy mạnh Chỉ số sẵn sàng AI thông qua xây dựng hạ tầng đám mây dùng chung, "
        "kiến tạo sandbox pháp lý và thành lập quỹ an sinh xã hội hỗ trợ chuyển đổi nghề nghiệp.",
        style_normal
    ))
    story.append(Spacer(1, 10))

    callout_4_data = [[
        Paragraph(
            "<b>Nhận định cốt lõi:</b> Sự thích ứng của người lao động và chính sách đào tạo lại linh hoạt chính là "
            "chìa khóa để Việt Nam vượt qua làn sóng tự động hóa. Việc chuyển đổi từ 'coder cơ bắp' sang 'strategic power user' "
            "là lộ trình bắt buộc đối với nhân sự ngành công nghệ.",
            style_callout
        )
    ]]
    callout_table_4 = Table(callout_4_data, colWidths=[500])
    callout_table_4.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), COLOR_BG_LIGHT),
        ('BOX', (0,0), (-1,-1), 1, COLOR_PRIMARY),
        ('LEFTPADDING', (0,0), (-1,-1), 15),
        ('RIGHTPADDING', (0,0), (-1,-1), 15),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(callout_table_4)

    # Xây dựng tài liệu sử dụng canvas tùy biến NumberedCanvas để tự động chèn tổng số trang
    doc.build(story, canvasmaker=NumberedCanvas)
    print("Times New Roman PDF report successfully built!")

if __name__ == '__main__':
    build_pdf()
