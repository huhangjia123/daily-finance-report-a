import os
import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# ==================== 数据获取函数 ====================

def get_macro_data():
    """获取宏观经济与金融市场数据"""
    data = {}

    # 美元指数 (示例API)
    try:
        resp = requests.get("https://api.exchangerate.host/latest?base=USD")
        usd_data = resp.json()
        data["usd_index"] = round(usd_data.get("rates", {}).get("CNY", 0) * 7, 2)  # 简化模拟
    except:
        data["usd_index"] = None

    # 人民币汇率
    try:
        data["usd_cny"] = round(usd_data.get("rates", {}).get("CNY", 0), 4)
    except:
        data["usd_cny"] = None

    # 制造业PMI (假数据接口)
    try:
        data["pmi"] = 49.2
    except:
        data["pmi"] = None

    # M1 / M2 (假数据)
    data["m1"] = 2.2
    data["m2"] = 10.0

    return data


def get_sector_rotation():
    """模拟板块轮动分析"""
    return {
        "科技": "资金有回流迹象，关注AI芯片和通信设备",
        "消费": "受益于政策刺激，但短期承压",
        "周期": "大宗商品价格反弹，有利于有色、煤炭",
        "金融": "利率预期下行，利好银行和券商"
    }


def get_anti_involution():
    """行业反内卷指标：库存/出货量/涨价"""
    return {
        "光伏": "库存下降，硅料价格企稳，产业链可能迎来复苏",
        "汽车": "新能源车销量超预期，电池环节涨价",
        "半导体": "部分芯片交期拉长，说明下游需求回暖"
    }


def generate_report():
    """生成日报文本"""
    data = get_macro_data()
    sectors = get_sector_rotation()
    anti_inv = get_anti_involution()

    today = datetime.now().strftime("%Y-%m-%d")

    report = f"📊 {today} 金融与投资日报\n\n"

    # 宏观经济
    report += "【宏观数据】\n"
    report += f"- 美元指数: {data['usd_index'] if data['usd_index'] else '暂无'}\n"
    report += f"- 人民币汇率(USD/CNY): {data['usd_cny'] if data['usd_cny'] else '暂无'}\n"
    report += f"- 中国制造业PMI: {data['pmi']}\n"
    report += f"- M1同比: {data['m1']}%\n"
    report += f"- M2同比: {data['m2']}%\n\n"

    # 板块轮动
    report += "【板块轮动分析】\n"
    for k, v in sectors.items():
        report += f"- {k}: {v}\n"
    report += "\n"

    # 反内卷指标
    report += "【行业反内卷信号】\n"
    for k, v in anti_inv.items():
        report += f"- {k}: {v}\n"
    report += "\n"

    # 市场走向
    report += "【市场走向解读】\n"
    report += "- PMI持续低于50，制造业处于收缩区间，短期对周期股压力较大。\n"
    report += "- M2维持高位，流动性充裕，中期利好成长股和科技股。\n"
    report += "- 板块轮动显示科技与周期获得资金青睐，消费仍承压。\n"
    report += "- 行业“反内卷”信号提示：光伏、汽车、半导体或将成为热点方向。\n"
    report += "- A股：短期震荡，中期结构性机会突出。\n"
    report += "- 港股：跟随美元指数波动，科技与新能源有望走强。\n"

    return report


# ==================== 邮件发送 ====================

def send_email(report):
    sender = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")
    receiver = os.getenv("EMAIL_RECEIVER")

    if not sender or not password or not receiver:
        print("❌ 邮箱配置不完整，请检查 GitHub Secrets")
        return

    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = receiver
    msg["Subject"] = "📈 每日金融与投资日报"

    msg.attach(MIMEText(report, "plain", "utf-8"))

    try:
        with smtplib.SMTP_SSL("smtp.qq.com", 465) as server:
            server.login(sender, password)
            server.sendmail(sender, receiver, msg.as_string())
        print("✅ 邮件发送成功")
    except Exception as e:
        print("❌ 邮件发送失败:", e)


if __name__ == "__main__":
    report = generate_report()
    print(report)
    send_email(report)
