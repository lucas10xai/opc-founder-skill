# Bộ skill Founder

[English version below](#the-founder-skill)

**Đừng đợi đến khi ký hợp đồng thuê mặt bằng mới biết ý tưởng có sống được không.**

17 skill cho Claude giúp bạn kiểm tra một ý tưởng kinh doanh trước khi tiêu tiền, rồi theo dõi nó sau khi mở bán. Miễn phí, giấy phép MIT, không cần đăng ký, không cần API key, không phải kết nối gì.

`skills/founder-board` `skills/founder-marketing` `skills/founder-cfo`
`skills/founder-consumer` `skills/founder-launch` `skills/founder-pricing`
`skills/founder-offer` `skills/founder-competitors` `skills/founder-brand`
`skills/founder-ops` `skills/founder-plan` `skills/founder-interview`
`skills/founder-compliance` `skills/founder-sales` `skills/founder-metrics`
`skills/founder-pitch` `skills/founder-run`

## Mục lục

- [Vì sao có bộ skill này](#vì-sao-có-bộ-skill-này)
- [Bắt đầu nhanh](#bắt-đầu-nhanh)
- [Cài đặt](#cài-đặt)
- [Bạn nhận được gì](#bạn-nhận-được-gì)
- [17 skill, chia theo giai đoạn](#17-skill-chia-theo-giai-đoạn)
- [Một ví dụ chạy từ đầu đến cuối](#một-ví-dụ-chạy-từ-đầu-đến-cuối)
- [Sau khi mở bán](#sau-khi-mở-bán)
- [Dành cho thị trường Việt Nam](#dành-cho-thị-trường-việt-nam)
- [Bán cho doanh nghiệp (B2B)](#bán-cho-doanh-nghiệp-b2b)
- [Các công cụ Python](#các-công-cụ-python)
- [Câu hỏi thường gặp](#câu-hỏi-thường-gặp)
- [Những điều bộ skill này không làm được](#những-điều-bộ-skill-này-không-làm-được)
- [Cấu trúc repo](#cấu-trúc-repo)

## Vì sao có bộ skill này

Phần lớn người mới kinh doanh học bài học đắt nhất theo thứ tự ngược: đặt cọc mặt bằng, làm biển hiệu, nhập hàng, chạy quảng cáo, rồi mới phát hiện mỗi đơn bán ra không đủ lãi để trả tiền thuê, hoặc khách quen ở quán bên cạnh không bao giờ đổi quán.

Bộ skill này đảo thứ tự đó. Trước khi chi một đồng, bạn cho ý tưởng đi qua:

- **Hội đồng quản trị.** Ba thành viên, mỗi người đọc ý tưởng qua một khung tư duy đã công bố (Alex Hormozi, Peter Thiel, Steve Jobs), chấm điểm, nêu điều có thể giết dự án và bỏ phiếu.
- **Giám đốc marketing.** Định vị, kênh khách thật sự dùng, chiến dịch 30 ngày có lịch cụ thể.
- **CFO.** Biên lợi nhuận thật, điểm hòa vốn mỗi ngày, năm 1 theo từng tháng, số tiền mặt bạn cần có trước khi dự án tự nuôi được mình.
- **Hội đồng người tiêu dùng.** 100 khách hàng giả lập dựng theo đúng tệp khách mục tiêu của bạn, mỗi người một mức thu nhập, thói quen và nỗi băn khoăn, cùng xem một lời chào hàng và trả lời có mua hay không, vì sao.

Và vì mô phỏng thì chưa phải thật, bộ skill còn có phần kiểm chứng với người thật (`/founder-interview`) và phần theo dõi sau khi mở bán (`/founder-metrics`).

Ba nguyên tắc xuyên suốt:

1. **Số liệu được tính, không được đoán.** Mọi con số trong báo cáo truy về một đầu vào bạn đưa. Thiếu trường là công cụ báo lỗi, không tự điền.
2. **Phân biệt rõ ba loại bằng chứng:** giả lập (hội đồng người tiêu dùng), dự phóng (số liệu CFO) và thật (phỏng vấn, đặt cọc, doanh số thực). Kế hoạch cuối ghi riêng từng loại, và kết luận không bao giờ coi giả lập là thật.
3. **Không bịa nguồn.** Đối thủ, giá, đánh giá, quy định đều lấy từ nguồn công khai kèm link. Không có nguồn thì skill nói là chưa có.

## Bắt đầu nhanh

1. Cài bộ skill (xem [Cài đặt](#cài-đặt)).
2. Mở Claude Code trong thư mục dự án của bạn và gõ:

```
/founder-run Tôi muốn mở quán matcha mang đi ở Quận 1, TP. Hồ Chí Minh, bán khoảng 55.000đ một ly.
```

`/founder-run` hỏi bạn một lần ba câu (nước nào, tiền tệ gì, viết bằng ngôn ngữ nào), ghi `founder/market.json`, rồi chạy lần lượt các skill theo đúng thứ tự. Sau mỗi skill nó tóm tắt hai dòng: tìm được gì và điều đó đổi gì cho phần còn lại.

3. Nếu chỉ muốn thử nhanh một ý tưởng còn đang nghĩ:

```
/founder-consumer --quick
```

Lệnh này chạy 20 khách giả lập thay vì 100, đủ để biết có nên theo tiếp không.

4. Biết mình đang ở đâu và bước tiếp theo là gì, bất cứ lúc nào:

```bash
python3 skills/founder-run/status.py
```

## Cài đặt

Cách nhanh nhất: dán link repo vào Claude và nói `install skill`.

```
https://github.com/lucas10xai/opc-founder-skill

install skill
```

Hoặc cài như plugin trong Claude Code:

```
/plugin marketplace add lucas10xai/opc-founder-skill
/plugin install opc-founder-skill@opc-founder-skill
```

Claude Code gắn tiền tố cho skill của plugin, nên khi cài kiểu plugin chúng hiện là `/opc-founder-skill:founder-board` và tương tự. Muốn gõ gọn `/founder-board` thì copy thư mục:

```bash
git clone https://github.com/lucas10xai/opc-founder-skill.git
cp -r opc-founder-skill/skills/founder-* ~/.claude/skills/
```

Muốn dùng riêng cho một dự án thay vì toàn máy: copy các thư mục `founder-*` vào `.claude/skills/` của repo dự án.

Không dùng Claude Code? Dán một file `SKILL.md` bất kỳ lên đầu cuộc trò chuyện và nó chạy như một chế độ làm việc. Bạn mất phần sub-agent và công cụ Python (nên không có hội đồng 100 khách và không có phép tính tự động), nhưng phương pháp vẫn dùng được.

Yêu cầu: Python 3.8 trở lên cho các công cụ. Không phải cài thêm gói nào.

## Bạn nhận được gì

Mọi kết quả nằm trong thư mục `founder/` ngay trong dự án của bạn, toàn file văn bản (markdown, JSON, CSV) mà bạn đọc, sửa và đưa vào git được. Các skill đọc file của nhau, nên làm đến đâu có bằng chứng đến đó.

```
founder/
  market.json            quốc gia, tiền tệ, ngôn ngữ (do /founder-run ghi)
  idea.md                ý tưởng, viết rõ ràng
  board.md               phiếu bầu và điều kiện của hội đồng
  competitors.md         đối thủ, giá, điều khách của họ phàn nàn
  customer.json          tệp khách mục tiêu (đầu vào của hội đồng)
  pitch.md               lời chào hàng mà mỗi khách giả lập nhìn thấy
  panel/results.md       ai mua, ai không, vì sao, bằng lời của họ
  interviews/results.md  người thật so với hội đồng giả lập
  pricing.md             khoảng giá chấp nhận được và giá nên thử
  offer.md               gói ưu đãi trả lời các băn khoăn
  numbers.json           đầu vào của CFO: giá, chi phí, sản lượng
  cfo.md                 biên lợi nhuận, hòa vốn, năm 1, tiền mặt cần có
  compliance.md          giấy phép, thuế, hóa đơn cần xác nhận
  marketing.md           định vị, kênh, chiến dịch 30 ngày
  brand.md               tên, giọng điệu, lời hứa
  ops.md                 nhà cung cấp, nhân sự, quy trình, sổ rủi ro
  launch.md              thử nghiệm thật, đếm ngược, ngày khai trương
  business-plan.md       kế hoạch kinh doanh, kết luận nằm ở đầu trang
  one-pager.md           bản một trang cho đối tác hoặc ngân hàng
  actuals.csv            doanh số và chi phí thật (bạn cập nhật sau khi mở bán)
  metrics.md             kế hoạch so với thực tế
```

## 17 skill, chia theo giai đoạn

Thứ tự chạy:

```
board -> competitors -> consumer -> pricing -> offer -> cfo -> compliance -> marketing -> brand -> ops -> launch -> plan
          (interview song song sau consumer; sales cho B2B; metrics sau khi mở bán; pitch nếu gọi vốn)
```

Bạn không bắt buộc đi hết chuỗi. Mỗi skill chạy riêng được, và `/founder-run` luôn biết còn thiếu gì.

### Giai đoạn 1: ý tưởng này có đáng làm không

| lệnh | vai trò | làm gì | ghi ra |
| --- | --- | --- | --- |
| `/founder-board` | Hội đồng quản trị | Ba thành viên, mỗi người là một sub-agent áp dụng một khung đã công bố (Offers từ *$100M Offers*; Monopoly từ *Zero to One*; Product từ tiểu sử *Steve Jobs* của Isaacson). Mỗi người chấm điểm, nêu điều có thể giết ý tưởng và bỏ phiếu: đầu tư, đầu tư nếu có điều kiện, hoặc bỏ qua. | `idea.md`, `board.md` |
| `/founder-competitors` | Trinh sát đối thủ | Lập bản đồ đối thủ trực tiếp, gián tiếp và hàng thay thế từ nguồn công khai: giá, định vị, khách của họ phàn nàn gì. Mỗi dữ kiện có link. | `competitors.md`, `competitors.csv` |
| `/founder-consumer` | Hội đồng người tiêu dùng | Dựng bầy khách giả lập (mặc định 100, `--quick` là 20) từ tệp khách mục tiêu, mỗi khách một sub-agent. Tổng hợp tỷ lệ mua theo phân khúc, lý do không mua bằng lời của họ, điều gì có thể đổi câu trả lời "không", và bốn câu trả lời về giá cho `/founder-pricing`. | `customer.json`, `pitch.md`, `panel/` |
| `/founder-interview` | Huấn luyện khám phá khách hàng | Hội đồng chỉ là giả lập; skill này kiểm tra nó với 5 đến 10 người thật. Soạn bản sàng lọc và kịch bản phỏng vấn theo kiểu hỏi về hành vi thật, lưu hồ sơ từng cuộc, rồi đặt tỷ lệ người thật trả tiền hoặc đặt cọc cạnh tỷ lệ mua của hội đồng. | `interviews/` |

### Giai đoạn 2: tiền và giá

| lệnh | vai trò | làm gì | ghi ra |
| --- | --- | --- | --- |
| `/founder-pricing` | Chiến lược giá | Biến bốn câu trả lời về giá của mỗi khách thành khoảng giá chấp nhận được (phương pháp Van Westendorp), đặt cạnh giá đối thủ và biên lợi nhuận, rồi chọn hai mức nên thử với khách thật. | `pricing.md`, `pricing-curve.md` |
| `/founder-offer` | Kiến trúc sư ưu đãi | Dựng gói ưu đãi (quà tặng, cam kết, tính khan hiếm thật, tên gọi) trả lời từng băn khoăn hàng đầu của hội đồng, tính chi phí của từng thứ để gói vẫn có lãi, rồi chạy lại hội đồng để xem tỷ lệ mua có nhích lên không. | `offer.md` |
| `/founder-cfo` | CFO | Kinh tế đơn vị: lãi trên mỗi đơn vị bán, biên lợi nhuận thật, điểm hòa vốn mỗi ngày, năm 1 theo từng tháng (kể cả giai đoạn tăng chậm), tiền mặt cần có, tháng hoàn vốn, mức giá thấp nhất vẫn hòa vốn, bảng lợi nhuận theo giá nhân sản lượng và các kịch bản "nếu". | `numbers.json`, `cfo.md` |
| `/founder-compliance` | Checklist tuân thủ | Giấy phép, thuế, hóa đơn, mặt bằng, lao động, quy định quảng cáo cần xác nhận theo quốc gia và loại hình kinh doanh. Mỗi mục có trang chính thức, người xác nhận và thời gian xử lý tính vào ngày ra mắt. Không nêu quy định nào nếu không tìm được nguồn. | `compliance.md` |

### Giai đoạn 3: đưa ra thị trường

| lệnh | vai trò | làm gì | ghi ra |
| --- | --- | --- | --- |
| `/founder-marketing` | Giám đốc marketing | Định vị một câu, kênh mà nhóm mua nhiều nhất thật sự dùng, chiến dịch 30 ngày có ngày đăng cụ thể, 10 câu mở đầu, chia ngân sách, và số tiền tối đa có thể trả để có một khách. Mỗi thông điệp trả lời một băn khoăn có thật. | `marketing.md` |
| `/founder-sales` | Trưởng nhóm bán hàng | Cho doanh nghiệp bán cho doanh nghiệp: chân dung khách lý tưởng, tin nhắn tiếp cận và hai lần theo dõi, kịch bản cuộc gọi, phễu tính ngược. | `icp.md`, `sales.md`, `funnel.json` |
| `/founder-brand` | Thiết kế thương hiệu | Danh sách tên kèm các bước kiểm tra nhãn hiệu, tên miền, tài khoản mạng xã hội; giọng điệu, lời hứa và bản brief cho phần hình ảnh. | `brand.md` |
| `/founder-ops` | Quản lý vận hành | Nhà cung cấp và báo giá, lịch làm việc, quy trình cho các khoảnh khắc quyết định (mở cửa, phục vụ, xử lý khiếu nại, đóng cửa), công cụ tối thiểu và sổ 10 rủi ro. Chi phí thật tìm được sẽ đưa về lại cho CFO. | `ops.md` |
| `/founder-launch` | Trưởng nhóm ra mắt | Bắt đầu bằng một thử nghiệm thật rẻ tiền (đặt trước, điểm bán thử, hoặc khách thí điểm trả tiền), rồi đếm ngược có ngày tháng và người phụ trách, kịch bản ngày khai trương theo giờ và 30 ngày đầu. | `launch.md` |

### Giai đoạn 4: chốt, theo dõi, gọi vốn

| lệnh | vai trò | làm gì | ghi ra |
| --- | --- | --- | --- |
| `/founder-plan` | Lập kế hoạch kinh doanh | Gộp mọi thứ thành một kế hoạch có kết luận tính từ số liệu (xem phần dưới), kèm bản tóm tắt và bản một trang. | `summary.md`, `business-plan.md`, `one-pager.md` |
| `/founder-metrics` | Phân tích hiệu quả | Sau khi mở bán: so doanh số và chi phí thật với kế hoạch từng tháng, kết luận và vẽ lại năm 1 từ các tháng thực tế. | `actuals.csv`, `metrics.md` |
| `/founder-pitch` | Soạn bài gọi vốn | Chỉ dùng khi bạn gọi vốn hoặc vay. Dàn ý 10 slide và 15 câu hỏi khó nhất, dựng từ chính số liệu của kế hoạch. Từ chối chạy nếu kết luận là Incomplete, và không bao giờ bịa số liệu tăng trưởng hay quy mô thị trường. | `pitch-deck.md`, `pitch-qa.md` |
| `/founder-run` | Chánh văn phòng | Đặt thị trường một lần, xem trong `founder/` đã có gì, chạy skill kế tiếp đúng thứ tự, và dừng lại nếu một bước tự kiểm tra thất bại (ví dụ mỗi đơn vị bán đang lỗ). | `market.json` |

### Kết luận của kế hoạch được tính như thế nào

Dòng đầu của `business-plan.md` là một trong ba kết luận, do `compile.py` tính, không ai viết tay:

- **Profitable:** mọi kiểm tra có dữ liệu đều đạt.
- **Not yet:** ít nhất một kiểm tra không đạt, và kế hoạch liệt kê con số không đạt.
- **Incomplete:** chưa có số liệu CFO.

Năm kiểm tra:

1. Mỗi đơn vị bán có lãi trước chi phí cố định.
2. Năm 1 có lợi nhuận hoạt động.
3. Điểm hòa vốn nằm trong công suất (nếu bạn khai công suất).
4. Đủ khách giả lập mua (mặc định từ 25%, chỉnh bằng `--min-buy-rate`).
5. Khi đã phỏng vấn từ 5 người thật trở lên: đủ số đó đã trả tiền hoặc đặt cọc (mặc định từ 10%, chỉnh bằng `--min-real-rate`). Dưới 5 người thì kế hoạch chỉ hiện số đếm, không phán xét.

Hai ngưỡng 25% và 10% là mặc định của bộ skill, không phải chuẩn ngành. Bạn đổi được, nhưng nên ghi lại lý do.

## Một ví dụ chạy từ đầu đến cuối

Giả sử bạn muốn mở **Moss Matcha Bar Sài Gòn**, quán matcha mang đi ở Quận 1, TP. Hồ Chí Minh, matcha latte 55.000đ một ly. Mọi đầu vào của ví dụ này nằm sẵn trong repo (`skills/founder-cfo/example.vn.json`, `skills/founder-consumer/customer.example.vn.json`, `pitch.example.vn.md`) nên bạn chạy lại được. Đây là quán giả định, số liệu chỉ để minh họa.

1. **`/founder-board`** ghi `founder/idea.md` từ những gì bạn kể và đưa nó trước ba thành viên hội đồng. Mỗi người chấm điểm và bỏ phiếu. Các điều kiện ("chỉ đầu tư nếu...") trở thành checklist cho phần còn lại.
2. **`/founder-competitors`** lập bản đồ các quán matcha và quán cà phê trong tầm đi bộ: họ bán latte giá bao nhiêu, bán qua kênh nào, khách phàn nàn gì trong đánh giá.
3. **`/founder-consumer`** dựng tệp khách mục tiêu (nhân viên văn phòng trẻ, 22 đến 35 tuổi, uống cà phê hoặc trà sữa ít nhất 4 lần một tuần) chia thành ba phân khúc thu nhập, bảy kiểu hành vi mua (khách quen mỗi sáng, săn khuyến mãi, đọc kỹ đánh giá...) và bảy băn khoăn ("55.000đ một ly hơi mắc", "quán quen của mình gần hơn", "đặt qua app giao đồ ăn thì giá bị đội lên"...). Mỗi khách trong 100 khách trả lời bằng tiếng Việt, có tên Việt và mức lương theo tháng bằng VND. Kết quả: ai mua, ai không, và lý do nguyên văn.
4. **`/founder-pricing`** đọc bốn câu trả lời về giá của mỗi khách để ra khoảng giá chấp nhận được, rồi so 55.000đ với khoảng đó và với giá đối thủ.
5. **`/founder-offer`** trả lời các băn khoăn hàng đầu bằng ưu đãi (giá tuần khai trương 45.000đ, thẻ tích điểm) và chạy lại một hội đồng nhanh.
6. **`/founder-cfo`** chạy kinh tế đơn vị trên `numbers.json`. Với số liệu ví dụ:

   - mỗi ly còn lại **32,300₫** sau chi phí riêng của nó (biên đóng góp 59%);
   - điểm hòa vốn là **88 ly mỗi ngày**;
   - biên lợi nhuận ở mức dự kiến 200 ly mỗi ngày là **33%**;
   - năm 1 lãi hoạt động **786,216,000₫** sau giai đoạn tăng chậm (tháng 1 chỉ 70 ly mỗi ngày và còn lỗ);
   - khoản đầu tư ban đầu 232,000,000₫ được hoàn lại ở **tháng 7**;
   - người sáng lập cần **249,170,000₫** tiền mặt trước khi dự án tự nuôi được mình;
   - mức giá thấp nhất vẫn hòa vốn cả năm 1 là 40,940₫.

7. **`/founder-compliance`**, **`/founder-marketing`**, **`/founder-brand`**, **`/founder-ops`** và **`/founder-launch`** biến nó thành danh sách giấy phép cần xác nhận, chiến dịch 30 ngày, một cái tên và diện mạo, nhà cung cấp và quy trình, và đợt ra mắt có ngày tháng cụ thể, bắt đầu bằng một điểm bán thử để thử với khách thật.
8. **`/founder-interview`** (chạy song song từ sau bước 3, vì phỏng vấn người thật cần nhiều ngày): bạn nói chuyện với 5 đến 10 người, ghi từng cuộc. Bạn bè không được tính, vì họ nói "có" cho vui lòng nhau.
9. **`/founder-plan`** biên soạn kế hoạch. Với số liệu trên và một hội đồng có 38 khách mua, đây là kết quả thật của lệnh `compile.py --check`:

```
Verdict: Profitable
  ✓ Each ly earns 32,300₫ before fixed costs (59% contribution).
  ✓ Year 1 operating profit: 786,216,000₫.
  ✓ Break-even is 88 ly a day against a capacity of 350.
  ✓ 38 of 100 simulated buyers buy (38%, the bar is 25%).
```

Nếu chỉ 12 trong 100 khách giả lập mua, dòng cuối đổi thành `✗ 12 of 100 simulated buyers buy (12%, the bar is 25%).` và kết luận thành **Not yet**, kèm lời nhắc skill nào sửa được (`/founder-offer`, `/founder-pricing`). Bảng báo cáo của công cụ dùng tiêu đề tiếng Anh; các đoạn giải thích do skill viết sẽ theo ngôn ngữ bạn chọn.

Muốn có bản đẹp để gửi người khác:

```bash
python3 skills/founder-plan/compile.py --html                    # trang HTML, mở bằng trình duyệt rồi in ra PDF
python3 skills/founder-plan/compile.py --vault ~/Vault/Plans    # ghi vào kho Obsidian, có frontmatter
```

File `.md` trong kho Obsidian cũng import được vào Notion dạng markdown.

## Sau khi mở bán

Đây là phần mà hầu hết các bộ công cụ bỏ qua. Khi đã có doanh số thật, ghi vào `founder/actuals.csv`, mỗi tháng một dòng (cập nhật dòng đó khi tháng chạy dần):

```
month,units,days,revenue,variable_cost,fixed_cost,ad_spend,new_customers
1,1500,,82500000,34050000,85000000,9000000,420
2,1900,,104500000,43130000,85000000,6000000,300
```

Cột nào chưa có thì để trống, công cụ dùng số của kế hoạch và ghi rõ là đã dùng số kế hoạch. Rồi chạy `/founder-metrics`:

```
Status: change something.
- Sales are 70% of plan in month 2 (the bar is 80%).

| month | ly a day (plan) | ly a day (real) | vs plan | profit (plan) | profit (real) | cumulative (real) |
| 1 | 70 | 50.0 | 71% | -17,170,000₫ | -36,550,000₫ | -268,550,000₫ |
| 2 | 90 | 63.3 | 70% | 2,210,000₫ | -23,630,000₫ | -292,180,000₫ |

Customers cost 20,833₫ each to win.
Year 1 operating profit: plan 786,216,000₫, reforecast 259,403,000₫.
```

(Rút gọn từ kết quả thật của `metrics.py` trên số liệu minh họa ở trên.)

Công cụ đưa ra một trong ba kết luận dựa trên dòng mới nhất:

- **Đúng kế hoạch:** doanh số, lãi trên mỗi đơn vị và chi phí tìm khách đều nằm trong ngưỡng.
- **Cần đổi:** doanh số dưới 80% kế hoạch, hoặc lãi trên mỗi đơn vị thấp hơn kế hoạch quá 15%, hoặc một khách tốn hơn mức trần `max_cac` bạn đặt.
- **Dừng lại và nghĩ lại:** mỗi đơn vị bán đang lỗ ở giá và chi phí thật, hoặc doanh số dưới 60% kế hoạch trong hai tháng liên tiếp.

Phần "Year 1 now" giữ nguyên các tháng thật và chạy phần còn lại của năm theo kế hoạch, thu nhỏ theo tỷ lệ doanh số thật so với kế hoạch. Đó là phép tính trên số liệu thật, không phải dự đoán. Sau đó skill đối chiếu con số lệch với skill sửa được nó (ít người mua thì `/founder-offer`; khách tốn quá nhiều tiền thì `/founder-marketing`; giá vốn cao thì `/founder-ops`...) và đưa ra một quyết định duy nhất: tiếp tục, đổi một thứ cụ thể rồi xem lại sau vài tuần, hoặc dừng.

## Dành cho thị trường Việt Nam

Cứ nói bạn kinh doanh ở Việt Nam, hoặc chạy `/founder-run` (nó hỏi một lần rồi ghi `founder/market.json`). Từ đó:

- Mỗi skill đọc thêm file `locale-vn.md` nằm ngay trong thư mục của nó, viết riêng cho nhiệm vụ của skill đó. Ví dụ ops nhắc về hộ kinh doanh, hóa đơn điện tử, an toàn thực phẩm, PCCC, Tết; marketing nhắc về Facebook, Zalo, TikTok Shop, Shopee, Google Maps và các dịp 8/3, 20/10, 11/11, 12/12, 20/11; offer nhắc về combo, freeship, tặng kèm, COD và rủi ro của nó.
- Tiền tính bằng VND, hiển thị như `45,000₫`, không có số lẻ. Phí sàn Shopee, TikTok Shop, Grab và phí thanh toán được đưa vào chi phí biến đổi của từng đơn vị.
- Hội đồng khách giả lập dùng tên Việt, thu nhập theo tháng bằng VND, và trả lời bằng tiếng Việt (khóa JSON vẫn bằng tiếng Anh để công cụ đọc được).
- Công cụ giá hiểu `45000`, `45,000`, `45.000`, `45k`, `45000đ`.
- Mọi file `.md` do skill viết sẽ bằng tiếng Việt.

Ví dụ bằng VND có sẵn: `skills/founder-cfo/example.vn.json`, `skills/founder-consumer/customer.example.vn.json`, `skills/founder-consumer/pitch.example.vn.md`.

Hai điều cần biết:

- Bảng số liệu do công cụ Python sinh ra (báo cáo CFO, kết quả hội đồng, báo cáo metrics) vẫn dùng tiêu đề tiếng Anh. Phần giải thích do skill viết thì theo tiếng Việt.
- Quy định thuế, hóa đơn, giấy phép của Việt Nam thay đổi thường xuyên (cách tính thuế hộ kinh doanh đã đổi từ 2026). Vì vậy các file `locale-vn.md` chỉ trỏ tới trang chính thức (cổng đăng ký kinh doanh, cổng thuế, cổng hóa đơn điện tử, cổng dịch vụ công, cơ sở dữ liệu văn bản pháp luật, cục sở hữu trí tuệ, cục an toàn thực phẩm, bảo hiểm xã hội) để bạn kiểm tra, không nêu mức thuế hay ngưỡng từ trí nhớ. Hãy xác nhận từng mục với cơ quan có thẩm quyền hoặc kế toán của bạn.

## Bán cho doanh nghiệp (B2B)

Hội đồng người tiêu dùng mặc định là khách cá nhân. Nếu khách của bạn là doanh nghiệp (agency, phần mềm, dịch vụ, bán sỉ):

- Trong `founder/customer.json` đặt `"kind": "business"` và một câu `income_line`, ví dụ `"Nhóm của bạn chi khoảng {amount} mỗi năm cho công cụ kiểu này."` (`{amount}` được thay bằng con số của từng khách). Khi đó phân khúc là các loại công ty, hành vi là cách mua (do người dùng dẫn dắt, do bộ phận mua hàng dẫn dắt, thử trước rồi mua) và băn khoăn là các băn khoăn của người mua doanh nghiệp (duyệt bảo mật, chi phí đổi sang giải pháp khác, chu kỳ ngân sách).
- Chạy `/founder-sales`: chân dung khách lý tưởng, tin nhắn tiếp cận, kịch bản gọi, và `funnel.py` tính ngược từ mục tiêu ra số cuộc tiếp xúc cần có mỗi tháng và mỗi ngày bán, CAC, LTV trên CAC và thời gian hoàn vốn. Công cụ cảnh báo khi LTV trên CAC dưới 3, thời gian hoàn vốn quá 12 tháng, hoặc số cuộc tiếp xúc cần có vượt khả năng của một người.
- Với dịch vụ bán theo tháng (client-month, dự án, gói duy trì), trong `numbers.json` đặt `"volume_period": "month"`: khi đó `plan_per_day` và `ramp_per_day` nghĩa là số đơn vị mỗi **tháng**, tên trường giữ nguyên.

## Các công cụ Python

Tám công cụ, đều là Python chuẩn, không kết nối mạng, không gọi lệnh hệ thống.

```bash
python3 skills/founder-cfo/unit_economics.py founder/numbers.json --out founder/cfo.md   # biên lợi nhuận, hòa vốn, năm 1
python3 skills/founder-consumer/panel.py init --customer founder/customer.json --pitch founder/pitch.md
python3 skills/founder-pricing/van_westendorp.py founder/panel/answers --price 55000      # khoảng giá chấp nhận được
python3 skills/founder-interview/interview.py tally                                        # người thật so với hội đồng
python3 skills/founder-sales/funnel.py founder/funnel.json                                 # số cuộc tiếp xúc cần có, CAC, hoàn vốn
python3 skills/founder-metrics/metrics.py founder/numbers.json founder/actuals.csv         # kế hoạch so với thực tế
python3 skills/founder-plan/compile.py --dir founder                                     # kế hoạch và kết luận
python3 skills/founder-run/status.py                                                      # đang ở đâu, bước tiếp theo là gì
```

- **`unit_economics.py`** đọc một file JSON (ví dụ `example.json` bằng USD hoặc `example.vn.json` bằng VND) và tính lãi trên mỗi đơn vị, hòa vốn, biên lợi nhuận ở mức dự kiến, năm 1 theo tháng, tiền mặt cần có, tháng hoàn vốn, mức giá thấp nhất vẫn hòa vốn, các kịch bản "nếu" (giá giảm 10%, sản lượng giảm 20%, chi phí đơn vị tăng 15%) và bảng lợi nhuận theo giá nhân sản lượng. Thiếu trường là báo lỗi, không đoán. `--price` và `--volume` cho chạy thử một kịch bản mà không phải sửa file.
- **`panel.py`** chia thẻ khách từ tệp khách mục tiêu (cùng seed thì ra cùng thẻ, nên chạy lại được), viết một bản brief cho mỗi khách, kiểm tra câu trả lời và tổng hợp. Nó không bao giờ trả lời thay một khách.
- **`van_westendorp.py`** đọc bốn câu trả lời về giá của mỗi khách (từ hội đồng, hoặc file CSV từ khảo sát thật) và tìm điểm quá rẻ, quá đắt, giá tối ưu và giá thờ ơ. Nên ưu tiên dữ liệu khảo sát thật hơn dữ liệu giả lập.
- **`interview.py`** lưu một hồ sơ cho mỗi cuộc trò chuyện thật (mức cam kết: không, quan tâm, đăng ký chờ, đặt trước, đã trả tiền) và tổng hợp. Bạn bè được liệt kê nhưng không tính vào tỷ lệ.
- **`funnel.py`** tính ngược mục tiêu bán hàng qua các giai đoạn ra số cuộc tiếp xúc đầu tiên bạn cần.
- **`metrics.py`** so `numbers.json` với `actuals.csv`, đưa ra kết luận, bảng kế hoạch so với thực tế và dự báo lại năm 1.
- **`compile.py`** gộp kế hoạch, tính kết luận và xuất HTML hoặc ghi vào kho Obsidian.
- **`status.py`** đọc `founder/` và cho biết skill kế tiếp; nó cũng ghi được `founder/market.json`.

Chạy kiểm thử (95 bài, chưa đến một giây):

```bash
python3 -m unittest discover -s tests -v
```

## Câu hỏi thường gặp

**Chạy hội đồng 100 khách có tốn nhiều không?**
Là 100 lượt gọi sub-agent, chia thành 10 đợt, mỗi đợt 10 khách. Hãy chạy `--quick` (20 khách) trước để xem thử. Mỗi sub-agent ghi một file nhỏ vào `founder/panel/answers/`, nên ở chế độ cấp quyền mặc định bạn sẽ phải duyệt nhiều lần; bật chế độ accept-edits (Shift+Tab) trong lúc chạy.

**Kết quả của hội đồng có đáng tin không?**
Nó tốt ở việc phát hiện băn khoăn, phân khúc và cách diễn đạt bạn chưa nghĩ tới. Nó kém ở việc dự đoán tỷ lệ mua thật, vì mô hình ngôn ngữ có xu hướng dễ đồng ý. Hãy coi tỷ lệ mua là mức trần, và dùng `/founder-interview` hoặc thử nghiệm của `/founder-launch` (đặt trước, điểm bán thử, trang đăng ký có giá) để xác nhận. Nếu người thật thấp hơn hội đồng nhiều, hãy tin người thật.

**Bộ skill có hợp với mọi ngành không?**
Hợp nhất với ngành có đơn vị bán rõ ràng và chi phí tính được: quán ăn, cửa hàng, bán hàng online, dịch vụ, agency, đăng ký thuê bao. Với sản phẩm phải đầu tư nghiên cứu nhiều năm hoặc mô hình mà doanh thu không tính theo đơn vị, phần CFO sẽ gượng ép.

**Tại sao kết luận là Not yet dù tôi thấy ý tưởng tốt?**
Vì một trong năm kiểm tra không đạt, và kế hoạch ghi rõ kiểm tra nào cùng con số. Đó là mục đích của nó: không làm dịu một con số đang đỏ. Sửa đầu vào (giá, chi phí, ưu đãi), chạy lại `/founder-cfo` rồi `/founder-plan`.

**Tôi đổi giá giữa chừng thì sao?**
Cập nhật `founder/numbers.json` (hoặc để `/founder-pricing` làm), chạy lại `/founder-cfo`, rồi `/founder-plan`. `/founder-run` nhắc việc này.

**Dữ liệu của tôi đi đâu?**
Các công cụ Python chạy trên máy bạn và không kết nối mạng. Nội dung bạn trao đổi với skill vẫn đi qua Claude như mọi cuộc trò chuyện khác, và các bước nghiên cứu (đối thủ, giấy phép) dùng tìm kiếm web công khai.

**Tôi có thể thêm hoặc sửa skill không?**
Được. Mỗi skill là một thư mục với `SKILL.md` (và công cụ nếu có). Giấy phép MIT: cứ lấy, sửa, rồi mang đi dùng. Test cấu trúc trong `tests/test_repo.py` sẽ báo nếu bạn làm hỏng một skill, ví dụ thiếu `name`, trỏ tới công cụ không tồn tại hoặc dùng dấu gạch dài.

## Những điều bộ skill này không làm được

**Hội đồng quản trị áp dụng các khung đã công bố, không phải là những người đó.** Ba lăng kính là bản tóm tắt ngắn, bằng lời của chúng tôi, về các ý tưởng trong *$100M Offers* của Alex Hormozi, *Zero to One* của Peter Thiel và Blake Masters, và tiểu sử Steve Jobs của Walter Isaacson. Hội đồng không bao giờ nói như họ, trích lời họ hay nói họ ủng hộ điều gì. Dự án này không liên kết với bất kỳ ai trong số họ.

**Hội đồng người tiêu dùng là khách giả lập, không phải khách thật.** Nó là cách nhanh và rẻ để tìm băn khoăn trước khi bạn chi tiền, không phải dự báo. Câu trả lời của hội đồng là tài liệu nghiên cứu; không bao giờ dùng làm lời chứng thực của khách hàng.

**Con số chỉ tốt bằng đầu vào.** CFO đánh dấu mọi ước tính là ước tính và đòi báo giá thật. Hãy kiểm tra chi phí với nhà cung cấp, còn cấu trúc công ty, lương và thuế thì với kế toán.

**Nghiên cứu dùng nguồn công khai, có link.** Không bịa đối thủ, giá, đánh giá hay lời trích. Không cào dữ liệu trái điều khoản của trang web.

**Không phải tư vấn tài chính, pháp lý hay thuế.** Giấy phép, nhãn hiệu và các tuyên bố quảng cáo phụ thuộc vào nơi bạn ở. Các skill cho bạn biết cần kiểm tra gì và ở đâu; một chuyên gia xác nhận.

**Chưa có gì thay thế được việc nói chuyện với khách thật.** Bộ skill giúp bạn đến buổi nói chuyện đó với câu hỏi tốt hơn và ít tốn kém hơn, không thay thế nó.

## Cấu trúc repo

```
skills/founder-board/        SKILL.md, lenses.md, locale-vn.md
skills/founder-competitors/  SKILL.md, locale-vn.md
skills/founder-consumer/     SKILL.md, panel.py, các file ví dụ (cả bản .vn), locale-vn.md
skills/founder-interview/    SKILL.md, interview.py, interview.example/
skills/founder-pricing/      SKILL.md, van_westendorp.py, locale-vn.md
skills/founder-offer/        SKILL.md, locale-vn.md
skills/founder-cfo/          SKILL.md, unit_economics.py, example.json, example.vn.json, locale-vn.md
skills/founder-compliance/   SKILL.md, locale-vn.md
skills/founder-marketing/    SKILL.md, locale-vn.md
skills/founder-sales/        SKILL.md, funnel.py, funnel.example.json
skills/founder-brand/        SKILL.md, locale-vn.md
skills/founder-ops/          SKILL.md, locale-vn.md
skills/founder-launch/       SKILL.md, locale-vn.md
skills/founder-metrics/      SKILL.md, metrics.py, actuals.example.csv
skills/founder-plan/         SKILL.md, compile.py
skills/founder-pitch/        SKILL.md
skills/founder-run/          SKILL.md, status.py
tests/                       kiểm thử cho mọi công cụ
```

## Tác giả

Made by Lucas from [opcaios.org](https://opcaios.org).

## Giấy phép

MIT. Cứ lấy, sửa, rồi mang đi dùng.

---

# The Founder skill

Seventeen Claude skills that test a business before you launch it, and check it
once it is live. Free, MIT, no signup, no API key, nothing to connect.

`skills/founder-board` `skills/founder-marketing` `skills/founder-cfo`
`skills/founder-consumer` `skills/founder-launch` `skills/founder-pricing`
`skills/founder-offer` `skills/founder-competitors` `skills/founder-brand`
`skills/founder-ops` `skills/founder-plan` `skills/founder-interview`
`skills/founder-compliance` `skills/founder-sales` `skills/founder-metrics`
`skills/founder-pitch` `skills/founder-run`

One of them is your board of directors, trained on the frameworks of Alex
Hormozi, Peter Thiel and Steve Jobs. One is your marketing director. One is your
CFO and finds your real profit margins. And one is the consumer panel: it spins
up 100 buyer agents trained on your target customer and runs your business
through 100 buyer scenarios.

So you know how to launch, how to market and how to actually make money, before
you spend thousands of dollars finding out the hard way.

## Install

Paste this repo link into Claude and say `install skill`:

```
https://github.com/lucas10xai/opc-founder-skill

install skill
```

Or as a plugin, in Claude Code:

```
/plugin marketplace add lucas10xai/opc-founder-skill
/plugin install opc-founder-skill@opc-founder-skill
```

Claude Code namespaces plugin skills, so installed as a plugin they show up as
`/opc-founder-skill:founder-board` and so on. Copy the folders instead if you want
plain `/founder-board`:

```bash
git clone https://github.com/lucas10xai/opc-founder-skill.git
cp -r opc-founder-skill/skills/founder-* ~/.claude/skills/
```

Project-local instead of global: copy the same folders into your repo's
`.claude/skills/`. No Claude Code at all? Paste any single `SKILL.md` at the top
of a chat and it runs as a mode. You lose the sub-agents and the Python tools,
but the method works.

The tools need Python 3.8 or newer. Nothing to pip install.

Working in Vietnam? Say so (or run `/founder-run`, which asks once and writes
`founder/market.json`). Every skill then reads its `locale-vn.md`, counts in VND,
and writes in Vietnamese. Examples in VND: `skills/founder-cfo/example.vn.json` and
`skills/founder-consumer/customer.example.vn.json`.

## The seventeen

| command | job | what it does |
| --- | --- | --- |
| `/founder-board` | Board of Directors | Three board members, each a sub-agent applying one published framework (Offers, from *$100M Offers*; Monopoly, from *Zero to One*; Product, from Isaacson's *Steve Jobs*), score the idea, name what would kill it and vote. |
| `/founder-competitors` | Competitor Scout | Maps direct competitors, indirect ones and substitutes from public sources, with prices, positioning and what their customers complain about, every fact linked. |
| `/founder-consumer` | Consumer Panel | Spins up a swarm of buyer agents (100 by default) from your target customer, each with its own income, habits and objection, and tallies who buys, who doesn't and why. |
| `/founder-pricing` | Pricing Strategist | Turns the panel's price answers into an acceptable price range, sets it against competitors and your margin, and picks what to test. |
| `/founder-offer` | Offer Architect | Builds the offer stack (bonuses, guarantee, real urgency, a name) that answers the panel's objections, then re-tests it on the panel. |
| `/founder-cfo` | CFO | Unit economics: contribution per sale, the real profit margin, break-even per day, year 1 month by month, cash needed, payback, what-ifs. |
| `/founder-marketing` | Marketing Director | Positioning, the channels your buyers use, a dated 30-day launch campaign, ten hooks and the most you can pay for a customer. |
| `/founder-brand` | Brand Designer | Name candidates with the trademark, domain and handle checks to run, a voice, a promise and a brief for the look. |
| `/founder-ops` | Operations Manager | Suppliers, staffing, day-one routines, tools, the permits to check and a risk register, feeding real costs back to the CFO. |
| `/founder-launch` | Launch Lead | A cheap real-world test first, then a dated countdown, the launch-day run sheet and the first 30 days. |
| `/founder-plan` | Business Planner | Compiles everything into one business plan with a verdict computed from the numbers: Profitable, Not yet or Incomplete. |
| `/founder-interview` | Customer Discovery Coach | The panel is simulated; this checks it against 5 to 10 real people. A screener and interview script, a record for each conversation, and the real pay-or-pre-order rate set beside the panel's buy rate. Friends are listed but not counted. |
| `/founder-compliance` | Compliance Checklist | Licences, tax, invoicing, premises, employment and advertising rules to confirm for your country and business, each with the official page to check, who confirms it and the lead time before launch. It refuses to state a rule it cannot source. |
| `/founder-sales` | Sales Lead | For businesses that sell to businesses: the ideal customer, outreach and follow-ups, a call script, and the funnel maths (conversations needed a week, CAC, LTV to CAC, payback). |
| `/founder-metrics` | Performance Analyst | After launch: real sales and costs against the plan, month by month. On track, change something or stop and rethink, with the failing number named, and year 1 redrawn from the real months. |
| `/founder-pitch` | Pitch Writer | Only if you are raising money or asking a lender: a 10-slide outline and the 15 hardest questions, built from the plan's own numbers. Never invents traction. |
| `/founder-run` | Chief of Staff | Sets the market once, sees what is already in `founder/`, and runs the next skill in order. |

## How to use it

Run them in this order. Each one reads what the others wrote, in a `founder/`
folder in your project.

```
board -> competitors -> consumer -> pricing -> offer -> cfo -> compliance -> marketing -> brand -> ops -> launch -> plan
          (interview in parallel after consumer; sales for B2B; metrics after launch; pitch if raising)
```

An example: a matcha café in Toronto, iced matcha lattes at $6.50 a cup. (Every
input is in the example files in this repo, so you can run the tools on it.)

1. **`/founder-board`** writes `founder/idea.md` from what you told it and puts it
   in front of three board members. Each scores it, lists the risks and votes:
   fund, fund if, or pass. The conditions become a checklist for the rest.
2. **`/founder-competitors`** maps the matcha bars and coffee shops within walking
   distance, what they charge for a latte and what their reviews complain about.
3. **`/founder-consumer`** builds the target customer (urban professionals, 24 to
   38, who buy coffee most days), deals 100 buyer cards across income, habits and
   objections, and runs one sub-agent per buyer. Back comes who buys, who passes,
   the reasons in their words ("my coffee place is closer", "$6.50 is steep for a
   drink") and what would flip a no.
4. **`/founder-pricing`** reads the panel's four price answers per buyer into a
   price range and checks $6.50 against it and against the competitors.
5. **`/founder-offer`** answers the top objections with the offer (a launch-week
   price, a loyalty card) and re-runs a quick panel to see if the buy rate moves.
6. **`/founder-cfo`** runs the unit economics. With the example numbers: each cup
   leaves $4.76 after its own costs, break-even is 186 cups a day, the profit
   margin at the planned 383 cups a day is 38%, year 1 makes $93,926 on operations
   after a slow ramp, the $25,280 startup spend is earned back in month 8, and the
   founder needs $34,092 in cash before it pays for itself.
7. **`/founder-marketing`**, **`/founder-brand`**, **`/founder-ops`** and
   **`/founder-launch`** turn it into a 30-day campaign, a name and a look, the
   suppliers and routines, and a dated launch that starts with a pop-up to test
   real buyers.
8. **`/founder-plan`** compiles `founder/business-plan.md`. Its verdict is
   computed, not written: Profitable only if every unit earns money, year 1 makes
   a profit, break-even fits capacity, enough of the panel buys and, once five or
   more real people have been interviewed, enough of them paid or pre-ordered.
   `compile.py --html` gives a page you can print to PDF; `compile.py --vault
   <folder>` writes the plan into an Obsidian vault (or a Notion markdown import).
9. **`/founder-metrics`**, once you are open: put the real sales and costs in
   `founder/actuals.csv` each week and it tells you if you are on plan.

You can also run any one on its own. `/founder-consumer --quick` on an idea you
are only thinking about is a good way to find out if you should.

## The tools

Eight of them, all standard-library Python. None touch the network.

```bash
python3 skills/founder-cfo/unit_economics.py founder/numbers.json --out founder/cfo.md   # margins, break-even, year 1
python3 skills/founder-consumer/panel.py init --customer founder/customer.json --pitch founder/pitch.md
python3 skills/founder-pricing/van_westendorp.py founder/panel/answers --price 6.50       # the acceptable price range
python3 skills/founder-interview/interview.py tally                                        # real people against the panel
python3 skills/founder-sales/funnel.py founder/funnel.json                                 # conversations needed, CAC, payback
python3 skills/founder-metrics/metrics.py founder/numbers.json founder/actuals.csv         # plan against reality
python3 skills/founder-plan/compile.py --dir founder                                     # the plan and its verdict
python3 skills/founder-run/status.py                                                      # where you are and what is next
```

**`unit_economics.py`** reads one JSON (example: `skills/founder-cfo/example.json`)
and reports contribution, break-even, the margin at plan, year 1 by month, cash
needed, payback, the lowest price that still breaks even, and what-ifs including a
price against volume grid. Money shows in the file's `currency` (USD, VND...). Every
number traces to an input; a missing field is an error, never a guess.

**`panel.py`** deals persona cards from your target customer (same seed, same
cards), writes one brief per buyer, checks the answers and tallies them. It never
answers for a buyer.

**`van_westendorp.py`** reads four price answers per buyer (from the panel, or a
CSV from a real survey) and finds the points of marginal cheapness and
expensiveness, the optimal and the indifference price.

**`interview.py`** files one record per real conversation and tallies them. People
who are friends are listed but not counted, because they say yes to be kind.

**`funnel.py`** works a sales target backwards through your stages to the number of
first conversations you need, and the CAC and payback if you give it a spend.

**`metrics.py`** compares `numbers.json` with `actuals.csv` and gives a call, a
table of plan against real, and a reforecast of year 1.

**`compile.py`** assembles the plan and computes the verdict.

**`status.py`** reads `founder/` and names the next skill; it can also write
`founder/market.json`.

```bash
python3 -m unittest discover -s tests -v
```

## Fine print

**The board applies published frameworks. It is not those people.** The three
lenses are short summaries, in our words, of ideas from *$100M Offers* by Alex
Hormozi, *Zero to One* by Peter Thiel with Blake Masters, and Walter Isaacson's
biography of Steve Jobs. The board never speaks as them, quotes them or claims
they endorse anything. This project is not affiliated with any of them.

**The consumer panel is simulated buyers, not customers.** It is a fast, cheap way
to find objections, segments and wording before you spend. It is not a forecast:
language models lean agreeable, so read the buy rate as an upper bound, and
confirm the big calls with real people: `/founder-interview` is built for that,
and `/founder-launch` starts with a real test too. Panel answers are research;
never use them as testimonials.

**The numbers are only as good as the inputs.** The CFO marks every estimate as an
estimate and asks for real quotes. Check costs with suppliers and the structure,
payroll and tax with an accountant.

**Research uses public sources, with links.** No invented competitors, prices,
reviews or quotes. No scraping against a site's terms.

**Not financial, legal or tax advice.** Permits, trademarks and claims depend on
where you are. The skills tell you what to check and where; a professional
confirms it.

## Files

```
skills/founder-board/        SKILL.md, lenses.md, locale-vn.md
skills/founder-competitors/  SKILL.md, locale-vn.md
skills/founder-consumer/     SKILL.md, panel.py, customer.example.json, pitch.example.md, *.vn.* examples, locale-vn.md
skills/founder-interview/    SKILL.md, interview.py, interview.example/
skills/founder-pricing/      SKILL.md, van_westendorp.py, locale-vn.md
skills/founder-offer/        SKILL.md, locale-vn.md
skills/founder-cfo/          SKILL.md, unit_economics.py, example.json, example.vn.json, locale-vn.md
skills/founder-compliance/   SKILL.md, locale-vn.md
skills/founder-marketing/    SKILL.md, locale-vn.md
skills/founder-sales/        SKILL.md, funnel.py, funnel.example.json
skills/founder-brand/        SKILL.md, locale-vn.md
skills/founder-ops/          SKILL.md, locale-vn.md
skills/founder-launch/       SKILL.md, locale-vn.md
skills/founder-metrics/      SKILL.md, metrics.py, actuals.example.csv
skills/founder-plan/         SKILL.md, compile.py
skills/founder-pitch/        SKILL.md
skills/founder-run/          SKILL.md, status.py
tests/                       the tests for every tool
```

Your own files live in `founder/` in your project. The skills read each other's.

## Made by

Made by Lucas from [opcaios.org](https://opcaios.org).

## License

MIT. Take it, change it, ship it.
