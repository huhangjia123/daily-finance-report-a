import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
import os
import sys

# ========== 邮箱配置 ==========
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

# ========== 数据获取函数 ==========
def get_usd_index():
    try:
        r = requests.get("https://api.exchangerate.host/latest?base=USD")
        return r.json().get("rates", {}).get("CNY", None)
    except:
        return None

def get_china_macro():
    # 模拟宏观数据，可替换成真实 API
    return {
        "PMI": 49.2,
        "M1": 2.2,
        "M2": 10.0,
        "CPI": 0.6,
        "PPI": -2.5,
        "SocialFinancing": 9.0
    }

def get_sector_rotation():
    # 模拟板块轮动
    return {
        "新能源": "+3.5%",
        "半导体": "-1.2%",
        "军工": "+2.8%",
        "消费": "+0.5%",
        "地产": "-0.8%"
    }

def get_anti_involution():
    # 模拟反内卷题材
    return {
        "面板出货量": "本月同比+12%，供需改善",
        "存储芯片": "库存下滑，现货价格上涨",
        "新能源车电池": "上游锂矿价格反弹 5%"
    }

# ========== 生成报告 ==========
def generate_report(report_type="daily"):
    today = datetime.date.today()
    title_map = {
        "daily": "📊 金融市场日报",
        "weekly": "📈 金融市场周报",
        "monthly": "📅 金融市场月报",
        "quarterly": "🌍 金融市场季报"
    }
    title = f"{title_map.get(report_type, '📊 金融市场日报')} ({today})"

    usd_cny = get_usd_index()
    macro = get_china_macro()
    sectors = get_sector_rotation()
    anti_inv = get_anti_involution()

    text = f"""{title}

美元兑人民币: {usd_cny if usd_cny else "暂无"}

【宏观数据】
- 制造业PMI: {macro['PMI']} → {'收缩' if macro['PMI']<50 else '扩张'}
- M1同比: {macro['M1']}% → 资金活跃度参考
- M2同比: {macro['M2']}% → 流动性充裕，对股市支撑
- CPI: {macro['CPI']}% → 消费物价压力
- PPI: {macro['PPI']}% → 工业品价格趋势
- 社融增速: {macro['SocialFinancing']}% → 融资环境

【板块轮动】
"""
    for sector, perf in sectors.items():
        text += f"- {sector}: {perf}\n"
    text += "解读: 资金流向偏好成长与政策扶持板块，周期股暂时承压。\n\n"

    text += "【反内卷题材追踪】\n"
    for k, v in anti_inv.items():
        text += f"- {k}: {v}\n"
    text += "解读: 行业去库存+涨价趋势显现，相关产业链公司有望率先受益。\n"

    return title, text

# ========== 邮件发送 ==========
def send_email(subject, body):
    if not all([EMAIL_USER, EMAIL_PASS, EMAIL_RECEIVER]):
        print("❌ 邮箱配置不完整，请检查 GitHub Secrets")
        return
    msg = MIMEMultipart()
    msg["From"] = EMAIL_USER
    msg["To"] = EMAIL_RECEIVER
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain", "utf-8"))

    try:
        with smtplib.SMTP_SSL("smtp.qq.com", 465) as server:
            server.login(EMAIL_USER, EMAIL_PASS)
            server.sendmail(EMAIL_USER, EMAIL_RECEIVER, msg.as_string())
        print("✅ 邮件发送成功")
    except Exception as e:
        print(f"❌ 邮件发送失败: {e}")

# ========== 主函数 ==========
if __name__ == "__main__":
    report_type = sys.argv[1] if len(sys.argv) > 1 else "daily"
    subject, body = generate_report(report_type)
    print(body)  # 打印日志方便 GitHub Actions 查看
    send_email(subject, body)
