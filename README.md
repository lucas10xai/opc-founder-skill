# Bộ skill Founder

[English version below](#the-founder-skill)

17 skill cho Claude giúp bạn kiểm tra một ý tưởng kinh doanh trước khi tung ra, và theo dõi nó sau khi chạy thật. Miễn phí, giấy phép MIT, không cần đăng ký, không cần API key, không phải kết nối gì.

`skills/founder-board` `skills/founder-marketing` `skills/founder-cfo`
`skills/founder-consumer` `skills/founder-launch` `skills/founder-pricing`
`skills/founder-offer` `skills/founder-competitors` `skills/founder-brand`
`skills/founder-ops` `skills/founder-plan` `skills/founder-interview`
`skills/founder-compliance` `skills/founder-sales` `skills/founder-metrics`
`skills/founder-pitch` `skills/founder-run`

Một skill là hội đồng quản trị của bạn, dựa trên các khung tư duy của Alex Hormozi, Peter Thiel và Steve Jobs. Một skill là giám đốc marketing. Một skill là CFO, tìm ra biên lợi nhuận thật. Và một skill là hội đồng người tiêu dùng: nó dựng 100 khách hàng giả lập theo đúng tệp khách hàng mục tiêu của bạn, rồi chạy ý tưởng qua 100 tình huống mua hàng.

Nhờ vậy bạn biết cách tung sản phẩm, cách làm marketing và cách thực sự kiếm ra tiền, trước khi tiêu hàng chục triệu đồng để học bài học đó theo cách đắt đỏ.

## Cài đặt

Dán link repo này vào Claude và nói `install skill`:

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

Muốn dùng riêng cho một dự án thay vì toàn máy: copy các thư mục đó vào `.claude/skills/` của repo. Không dùng Claude Code? Dán một file `SKILL.md` bất kỳ lên đầu cuộc trò chuyện và nó chạy như một chế độ làm việc. Bạn mất phần sub-agent và công cụ Python, nhưng phương pháp vẫn dùng được.

Các công cụ cần Python 3.8 trở lên. Không phải cài thêm gói nào.

### Dùng cho thị trường Việt Nam

Cứ nói bạn kinh doanh ở Việt Nam, hoặc chạy `/founder-run`: nó hỏi một lần rồi ghi `founder/market.json` (quốc gia, tiền tệ, ngôn ngữ). Sau đó mỗi skill đọc file `locale-vn.md` của mình, tính tiền bằng VND và viết bằng tiếng Việt. Ví dụ bằng VND: `skills/founder-cfo/example.vn.json` và `skills/founder-consumer/customer.example.vn.json`.

Lưu ý: file `.md` do skill viết sẽ bằng tiếng Việt, nhưng bảng số liệu do các công cụ Python sinh ra (ví dụ báo cáo của `unit_economics.py`) vẫn dùng tiêu đề tiếng Anh. Các quy định thuế, hóa đơn, giấy phép của Việt Nam thay đổi thường xuyên (hộ kinh doanh đã đổi cách tính thuế từ 2026), nên skill chỉ trỏ tới trang chính thức để bạn kiểm tra, không nêu mức thuế hay ngưỡng từ trí nhớ.

## 17 skill

| lệnh | vai trò | làm gì |
| --- | --- | --- |
| `/founder-board` | Hội đồng quản trị | Ba thành viên, mỗi người là một sub-agent áp dụng một khung đã công bố (Offers từ *$100M Offers*; Monopoly từ *Zero to One*; Product từ tiểu sử *Steve Jobs* của Isaacson), chấm điểm ý tưởng, nêu điều có thể giết nó và bỏ phiếu. |
| `/founder-competitors` | Trinh sát đối thủ | Lập bản đồ đối thủ trực tiếp, gián tiếp và hàng thay thế từ nguồn công khai: giá, định vị, khách của họ phàn nàn gì. Mỗi dữ kiện đều có link. |
| `/founder-consumer` | Hội đồng người tiêu dùng | Dựng một bầy khách hàng giả lập (mặc định 100) từ tệp khách mục tiêu, mỗi người có thu nhập, thói quen và nỗi băn khoăn riêng, rồi tổng hợp ai mua, ai không và vì sao. |
| `/founder-pricing` | Chiến lược giá | Biến các câu trả lời về giá của hội đồng thành khoảng giá chấp nhận được, đặt cạnh giá đối thủ và biên lợi nhuận của bạn, rồi chọn mức giá nên thử. |
| `/founder-offer` | Kiến trúc sư ưu đãi | Dựng gói ưu đãi (quà tặng, cam kết, tính khan hiếm thật, tên gọi) để trả lời các băn khoăn của hội đồng, rồi chạy lại để kiểm tra. |
| `/founder-cfo` | CFO | Kinh tế đơn vị: lãi trên mỗi đơn vị bán, biên lợi nhuận thật, điểm hòa vốn mỗi ngày, năm 1 theo từng tháng, tiền mặt cần có, thời gian hoàn vốn, các kịch bản "nếu". |
| `/founder-marketing` | Giám đốc marketing | Định vị, kênh khách thật sự dùng, chiến dịch 30 ngày có lịch cụ thể, 10 câu mở đầu và số tiền tối đa có thể trả để có một khách. |
| `/founder-brand` | Thiết kế thương hiệu | Danh sách tên kèm các bước kiểm tra nhãn hiệu, tên miền, tài khoản mạng xã hội; giọng điệu, lời hứa và bản brief cho phần hình ảnh. |
| `/founder-ops` | Quản lý vận hành | Nhà cung cấp, nhân sự, quy trình ngày đầu, công cụ, giấy phép cần kiểm tra và sổ rủi ro; đưa chi phí thật về lại cho CFO. |
| `/founder-launch` | Trưởng nhóm ra mắt | Trước hết là một thử nghiệm thật rẻ tiền, sau đó là đếm ngược có ngày tháng, kịch bản ngày khai trương và 30 ngày đầu. |
| `/founder-plan` | Lập kế hoạch kinh doanh | Gộp mọi thứ thành một kế hoạch với kết luận tính từ số liệu: Profitable (có lãi), Not yet (chưa đạt) hoặc Incomplete (chưa đủ dữ liệu). |
| `/founder-interview` | Huấn luyện khám phá khách hàng | Hội đồng chỉ là giả lập; skill này kiểm tra nó với 5 đến 10 người thật. Có bản sàng lọc và kịch bản phỏng vấn, hồ sơ từng cuộc trò chuyện, và tỷ lệ người thật trả tiền hoặc đặt cọc đặt cạnh tỷ lệ mua của hội đồng. Bạn bè được liệt kê nhưng không tính. |
| `/founder-compliance` | Checklist tuân thủ | Giấy phép, thuế, hóa đơn, mặt bằng, lao động, quy định quảng cáo cần xác nhận theo quốc gia và loại hình kinh doanh, mỗi mục có trang chính thức để kiểm tra, người xác nhận và thời gian xử lý trước ngày ra mắt. Không nêu quy định nào nếu không có nguồn. |
| `/founder-sales` | Trưởng nhóm bán hàng | Cho doanh nghiệp bán cho doanh nghiệp: chân dung khách lý tưởng, tin nhắn tiếp cận và theo dõi, kịch bản cuộc gọi, tính ngược phễu (số cuộc tiếp xúc cần mỗi tuần, CAC, LTV trên CAC, thời gian hoàn vốn). |
| `/founder-metrics` | Phân tích hiệu quả | Sau khi mở bán: so doanh số và chi phí thật với kế hoạch từng tháng. Kết luận "đúng kế hoạch", "cần đổi" hoặc "dừng lại và nghĩ lại", nêu rõ con số đang lệch, và vẽ lại năm 1 từ các tháng thực tế. |
| `/founder-pitch` | Soạn bài gọi vốn | Chỉ khi bạn gọi vốn hoặc vay: dàn ý 10 slide và 15 câu hỏi khó nhất, dựng từ chính số liệu của kế hoạch. Không bịa số liệu tăng trưởng. |
| `/founder-run` | Chánh văn phòng | Đặt thị trường một lần, xem trong `founder/` đã có gì, và chạy skill kế tiếp theo đúng thứ tự. |

## Cách dùng

Chạy theo thứ tự này. Mỗi skill đọc những gì skill trước đã viết, trong thư mục `founder/` ở dự án của bạn.

```
board -> competitors -> consumer -> pricing -> offer -> cfo -> compliance -> marketing -> brand -> ops -> launch -> plan
          (interview song song sau consumer; sales cho B2B; metrics sau khi mở bán; pitch nếu gọi vốn)
```

Ví dụ: một quán matcha mang đi ở Quận 1, TP. Hồ Chí Minh, matcha latte 55.000đ một ly. (Mọi đầu vào đều có trong các file ví dụ của repo nên bạn chạy được công cụ trên đó.)

1. **`/founder-board`** ghi `founder/idea.md` từ những gì bạn kể và đưa nó trước ba thành viên hội đồng. Mỗi người chấm điểm, liệt kê rủi ro và bỏ phiếu: đầu tư, đầu tư nếu có điều kiện, hoặc bỏ qua. Các điều kiện trở thành checklist cho phần còn lại.
2. **`/founder-competitors`** lập bản đồ các quán matcha và quán cà phê trong tầm đi bộ, họ bán latte giá bao nhiêu và khách phàn nàn gì trong đánh giá.
3. **`/founder-consumer`** dựng tệp khách mục tiêu (nhân viên văn phòng trẻ, 22 đến 35 tuổi, uống cà phê hoặc trà sữa hầu hết các ngày), chia 100 thẻ khách theo thu nhập, thói quen và băn khoăn, rồi chạy mỗi khách một sub-agent. Kết quả: ai mua, ai không, lý do bằng lời của họ ("quán quen của mình gần hơn", "55.000đ một ly hơi mắc") và điều gì có thể đổi câu trả lời "không".
4. **`/founder-pricing`** đọc bốn câu trả lời về giá của mỗi khách để ra khoảng giá, rồi so 55.000đ với khoảng đó và với giá đối thủ.
5. **`/founder-offer`** trả lời các băn khoăn hàng đầu bằng ưu đãi (giá tuần khai trương, thẻ tích điểm) và chạy lại một hội đồng nhanh để xem tỷ lệ mua có nhích lên không.
6. **`/founder-cfo`** chạy kinh tế đơn vị. Với số liệu ví dụ: mỗi ly còn lại 32,300₫ sau chi phí riêng của nó, điểm hòa vốn là 88 ly mỗi ngày, biên lợi nhuận ở mức dự kiến 200 ly mỗi ngày là 33%, năm 1 lãi hoạt động 786,216,000₫ sau giai đoạn tăng chậm, khoản đầu tư ban đầu 232,000,000₫ được hoàn lại ở tháng 7, và người sáng lập cần 249,170,000₫ tiền mặt trước khi tự nuôi được mình.
7. **`/founder-marketing`**, **`/founder-brand`**, **`/founder-ops`** và **`/founder-launch`** biến nó thành chiến dịch 30 ngày, một cái tên và diện mạo, nhà cung cấp và quy trình, và đợt ra mắt có ngày tháng cụ thể, bắt đầu bằng một điểm bán thử để thử với khách thật.
8. **`/founder-plan`** biên soạn `founder/business-plan.md`. Kết luận được tính, không phải viết tay: chỉ Profitable khi mỗi đơn vị bán đều có lãi, năm 1 có lợi nhuận, điểm hòa vốn nằm trong công suất, đủ khách trong hội đồng mua và, khi đã phỏng vấn từ 5 người thật trở lên, đủ số đó đã trả tiền hoặc đặt cọc. `compile.py --html` tạo trang để in ra PDF; `compile.py --vault <thư mục>` ghi kế hoạch vào kho Obsidian (hoặc để import vào Notion dạng markdown).
9. **`/founder-metrics`**, khi đã mở bán: mỗi tuần ghi doanh số và chi phí thật vào `founder/actuals.csv`, nó cho biết bạn có đang đúng kế hoạch không.

Bạn cũng có thể chạy riêng từng skill. `/founder-consumer --quick` trên một ý tưởng mới chỉ đang nghĩ là cách tốt để biết có nên theo đuổi không.

## Các công cụ

Tám công cụ, đều là Python chuẩn, không kết nối mạng.

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

**`unit_economics.py`** đọc một file JSON (ví dụ: `skills/founder-cfo/example.json`, hoặc `example.vn.json` bằng VND) và báo cáo lãi trên mỗi đơn vị, hòa vốn, biên lợi nhuận ở mức dự kiến, năm 1 theo tháng, tiền mặt cần có, thời gian hoàn vốn, mức giá thấp nhất vẫn hòa vốn và các kịch bản "nếu" gồm bảng giá nhân sản lượng. Tiền hiển thị theo `currency` của file (USD, VND...). Mọi con số đều truy về một đầu vào; thiếu trường là báo lỗi, không bao giờ đoán.

**`panel.py`** chia thẻ khách từ tệp khách mục tiêu của bạn (cùng seed thì ra cùng thẻ), viết một bản brief cho mỗi khách, kiểm tra câu trả lời và tổng hợp. Nó không bao giờ trả lời thay một khách.

**`van_westendorp.py`** đọc bốn câu trả lời về giá của mỗi khách (từ hội đồng, hoặc file CSV từ khảo sát thật) và tìm các điểm quá rẻ, quá đắt, giá tối ưu và giá thờ ơ. Hiểu được `45000`, `45.000`, `45k`, `45000đ`.

**`interview.py`** lưu một hồ sơ cho mỗi cuộc trò chuyện thật và tổng hợp. Bạn bè được liệt kê nhưng không tính, vì họ nói "có" cho vui lòng nhau.

**`funnel.py`** tính ngược mục tiêu bán hàng qua các giai đoạn ra số cuộc tiếp xúc đầu tiên bạn cần, cùng CAC và thời gian hoàn vốn nếu bạn đưa vào chi phí.

**`metrics.py`** so `numbers.json` với `actuals.csv`, đưa ra kết luận, bảng kế hoạch so với thực tế và dự báo lại năm 1.

**`compile.py`** gộp kế hoạch và tính kết luận.

**`status.py`** đọc `founder/` và cho biết skill kế tiếp; nó cũng ghi được `founder/market.json`.

Chạy kiểm thử:

```bash
python3 -m unittest discover -s tests -v
```

## Lưu ý quan trọng

**Hội đồng quản trị áp dụng các khung đã công bố, không phải là những người đó.** Ba lăng kính là bản tóm tắt ngắn, bằng lời của chúng tôi, về các ý tưởng trong *$100M Offers* của Alex Hormozi, *Zero to One* của Peter Thiel và Blake Masters, và tiểu sử Steve Jobs của Walter Isaacson. Hội đồng không bao giờ nói như họ, trích lời họ hay nói họ ủng hộ điều gì. Dự án này không liên kết với bất kỳ ai trong số họ.

**Hội đồng người tiêu dùng là khách giả lập, không phải khách thật.** Đây là cách nhanh và rẻ để tìm băn khoăn, phân khúc và cách diễn đạt trước khi bạn chi tiền. Nó không phải dự báo: mô hình ngôn ngữ có xu hướng dễ đồng ý, nên hãy coi tỷ lệ mua là mức trần, và xác nhận các quyết định lớn với người thật: `/founder-interview` sinh ra cho việc đó, và `/founder-launch` cũng bắt đầu bằng một thử nghiệm thật. Câu trả lời của hội đồng là tài liệu nghiên cứu; không bao giờ dùng làm lời chứng thực của khách hàng.

**Con số chỉ tốt bằng đầu vào.** CFO đánh dấu mọi ước tính là ước tính và đòi báo giá thật. Hãy kiểm tra chi phí với nhà cung cấp, còn cấu trúc công ty, lương và thuế thì với kế toán.

**Nghiên cứu dùng nguồn công khai, có link.** Không bịa đối thủ, giá, đánh giá hay lời trích. Không cào dữ liệu trái điều khoản của trang web.

**Không phải tư vấn tài chính, pháp lý hay thuế.** Giấy phép, nhãn hiệu và các tuyên bố quảng cáo phụ thuộc vào nơi bạn ở. Các skill cho bạn biết cần kiểm tra gì và ở đâu; một chuyên gia xác nhận.

## Cấu trúc thư mục

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

Các file của riêng bạn nằm trong `founder/` ở dự án của bạn. Các skill đọc file của nhau.

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
