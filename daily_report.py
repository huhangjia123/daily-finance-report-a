import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def get_data():
    data = {}

    # 美元指数
    try:
        resp = requests.get("https://api.exchangerate.host/latest?base=USD").json()
        usd_index = resp.get("rates", {}).get("EUR")
        if usd_index:
            data["美元指数"] = round(1 / usd_index, 2)  # 粗略用 EUR 反推
        else:
            data["美元指数"] = "暂无"
    except Exception as e:
        print("⚠️ 获取美元指数失败:", e)
        data["美元指数"] = "错误"

    # 人民币汇率
    try:
        resp = requests.get("https://api.exchangerate.host/latest?base=USD&symbols=CNY").json()
        usd_cny = resp.get("rates", {}).get("CNY")
        if usd_cny:
            data["人民币汇率(USD/CNY)"] = round(usd_cny, 4)
        else:
            data["人民币汇率(USD/CNY)"] = "暂无"
    except Exception as e:
        print("⚠️ 获取人民币汇率失败:", e)
        data["人民币汇率(USD/CNY)"] = "错误"

    # 采购经理人指数 PMI（用中国制造业 PMI，国家统计局）
    try:
        resp = requests.get("https://data.stats.gov.cn/easyquery.htm?cn=A01").text
        # 简化处理，假设最新 PMI=49.2
        data["中国制造业PMI"] = 49.2
    except Exception:
        data["中国制造业PMI"] = "暂无"

    # M1 / M2 货币供应量（这里写死示例数据，实际需调用央行API）
    data["M1同比"] = "2.2%"
    data["M2同比"] = "10.0%"

    return data

def generate_report(data):
    report = "📊 今日金融数据日报\n\n"
    for k, v in data.items():
        report += f"{k}: {v}\n"

    # 简单解读
    report += "\n📌 解读:\n"
    if isinstance(data.get("中国制造业PMI"), (int, float)) and data["中国制造业PMI"] < 50:
        report += "- 制造业PMI低于50，显示经济处于收缩区间。\n"
    if isinstance(data.get("人民币汇率(USD/CNY)"), (int, float)) and data["人民币汇率(USD/CNY)"] > 7.2:
        report += "- 人民币汇率偏弱，美元相对走强。\n"
    report += "- M2同比维持高位，显示流动性充裕。\n"

    return report

def send_email(report):
    EMAIL_USER = os.getenv("EMAIL_USER")
    EMAIL_PASS = os.getenv("EMAIL_PASS")
    EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

    if not all([EMAIL_USER, EMAIL_PASS, EMAIL_RECEIVER]):
        print("❌ 邮箱配置不完整，请检查 GitHub Secrets")
        return

    msg = MIMEMultipart()
    msg["From"] = EMAIL_USER
    msg["To"] = EMAIL_RECEIVER
    msg["Subject"] = "📈 每日金融数据日报"

    msg.attach(MIMEText(report, "plain", "utf-8"))

    try:
        if "qq.com" in EMAIL_USER:
            server = smtplib.SMTP_SSL("smtp.qq.com", 465)
        elif "gmail.com" in EMAIL_USER:
            server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        else:
            server = smtplib.SMTP_SSL("smtp.office365.com", 587)

        server.login(EMAIL_USER, EMAIL_PASS)
        server.sendmail(EMAIL_USER, EMAIL_RECEIVER, msg.as_string())
        server.quit()
        print("✅ 邮件已发送")
    except Exception as e:
        print("❌ 邮件发送失败:", e)

if __name__ == "__main__":
    data = get_data()
    if not data:
        print("⚠️ 无数据生成日报")
    else:
        report = generate_report(data)
        print(report)
        send_email(report)
