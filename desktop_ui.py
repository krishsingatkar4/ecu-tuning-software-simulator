import os
import sys
import json
import math
import re
import html
import traceback
from io import StringIO
from pathlib import Path
from contextlib import redirect_stdout

from PySide6.QtCore import Qt, QTimer, QThread, Signal, QRectF
from PySide6.QtGui import QColor, QPainter, QPen, QFont, QBrush
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QFrame,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QStackedWidget,
    QFormLayout,
    QLineEdit,
    QTextEdit,
    QTextBrowser,
    QListWidget,
    QListWidgetItem,
    QProgressBar,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QComboBox,
    QMessageBox,
    QDialog,
    QDialogButtonBox,
    QCheckBox,
    QSizePolicy,
)
from PySide6.QtPrintSupport import QPrinter, QPrintDialog

# -------------------------------------------------------------------
# PROJECT PATH
# -------------------------------------------------------------------

ROOT_DIR = Path(__file__).resolve().parent
os.chdir(ROOT_DIR)

from managers.car_manager import CarManager
from models.owner import Owner
from models.engine import Engine
from models.car import Car


# -------------------------------------------------------------------
# THEME
# -------------------------------------------------------------------

APP_STYLE = """
QMainWindow, QWidget {
    background: #090d13;
    color: #e8f0f7;
    font-family: "Segoe UI", "Inter", Arial;
    font-size: 13px;
}

QFrame#sidebar {
    background: #0b1119;
    border-right: 1px solid #1d2a37;
}

QFrame#topbar {
    background: #0c131d;
    border-bottom: 1px solid #1d2a37;
}

QFrame#rightpanel {
    background: #0b1119;
    border-left: 1px solid #1d2a37;
}

QFrame#panel {
    background: #101822;
    border: 1px solid #1c2b3a;
    border-radius: 8px;
}

QFrame#metric {
    background: #111b27;
    border: 1px solid #203242;
    border-radius: 7px;
}

QLabel#logo {
    color: #f5fbff;
    font-size: 20px;
    font-weight: 800;
    letter-spacing: 1px;
}

QLabel#section_title {
    color: #f2f8ff;
    font-size: 24px;
    font-weight: 700;
}

QLabel#section_subtitle {
    color: #8091a3;
    font-size: 12px;
}

QLabel#metric_value {
    color: #eef8ff;
    font-size: 25px;
    font-weight: 800;
}

QLabel#metric_caption {
    color: #7f95a8;
    font-size: 10px;
    font-weight: 700;
}

QLabel#metric_unit {
    color: #45d8ff;
    font-size: 11px;
    font-weight: 700;
}

QLabel#status_good {
    color: #5df7b2;
    background: rgba(32, 176, 111, 0.14);
    border: 1px solid #237b57;
    border-radius: 10px;
    padding: 4px 9px;
    font-weight: 700;
}

QLabel#status_bad {
    color: #ff7b7b;
    background: rgba(224, 71, 71, 0.12);
    border: 1px solid #8b3e3e;
    border-radius: 10px;
    padding: 4px 9px;
    font-weight: 700;
}

QPushButton {
    background: #172331;
    border: 1px solid #294052;
    color: #dcecf8;
    border-radius: 5px;
    padding: 9px 13px;
    font-weight: 700;
}

QPushButton:hover {
    background: #1d3041;
    border: 1px solid #41d4ff;
}

QPushButton:pressed {
    background: #122130;
}

QPushButton#primary_button {
    background: #007da8;
    border: 1px solid #36d2ff;
    color: white;
}

QPushButton#primary_button:hover {
    background: #00a1d5;
}

QPushButton#danger_button {
    background: #5d2228;
    border: 1px solid #ca4e57;
    color: #ffd6d9;
}

QPushButton#nav_button {
    text-align: left;
    color: #9cb0c1;
    background: transparent;
    border: none;
    border-radius: 4px;
    padding: 10px 12px;
    font-weight: 600;
}

QPushButton#nav_button:hover {
    background: #162432;
    color: #e9f8ff;
}

QPushButton#nav_button:checked {
    background: #0c4d69;
    border-left: 3px solid #40d9ff;
    color: #ecfbff;
}

QLineEdit, QTextEdit, QTextBrowser, QComboBox {
    background: #0a1119;
    color: #eaf4fc;
    border: 1px solid #283c4f;
    border-radius: 4px;
    padding: 8px;
    selection-background-color: #007da8;
}

QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
    border: 1px solid #3bd6ff;
}

QTableWidget {
    background: #0c131d;
    color: #dbeaf4;
    gridline-color: #1d2c3a;
    border: 1px solid #233747;
    border-radius: 5px;
}

QHeaderView::section {
    background: #14202c;
    color: #8edff5;
    padding: 9px;
    border: none;
    border-bottom: 1px solid #274052;
    font-weight: 700;
}

QTableWidget::item {
    padding: 7px;
    border-bottom: 1px solid #182633;
}

QScrollBar:vertical {
    background: #0a1017;
    width: 10px;
}

QScrollBar::handle:vertical {
    background: #2a4355;
    min-height: 24px;
    border-radius: 4px;
}
"""


# -------------------------------------------------------------------
# HELPERS
# -------------------------------------------------------------------

def safe_float(value, default=0.0):
    try:
        found = re.search(r"[-+]?\d*\.?\d+", str(value))
        return float(found.group()) if found else default
    except Exception:
        return default


def coerce_value(old_value, new_value):
    """Preserve numeric types where possible."""
    try:
        if isinstance(old_value, int):
            return int(float(new_value))
        if isinstance(old_value, float):
            return float(new_value)
    except ValueError:
        return old_value

    return new_value


def capture_console_output(function):
    output = StringIO()

    try:
        with redirect_stdout(output):
            function()
    except Exception as error:
        return f"ERROR: {error}"

    return output.getvalue()


def make_button(text, primary=False, danger=False):
    button = QPushButton(text)

    if primary:
        button.setObjectName("primary_button")
    elif danger:
        button.setObjectName("danger_button")

    button.setCursor(Qt.CursorShape.PointingHandCursor)
    return button


def make_panel():
    panel = QFrame()
    panel.setObjectName("panel")
    return panel


# -------------------------------------------------------------------
# BACKEND SESSION / FACADE
# -------------------------------------------------------------------

class BackendSession:
    """
    UI ke liye existing backend models ko manage karta hai.
    Backend business logic change nahi karta.
    """

    def __init__(self):
        self.car_manager = CarManager()
        self.active_car = None

        self.ensure_demo_vehicle()

    def ensure_demo_vehicle(self):
        """
        Agar database mein tuned ECU car nahi milti,
        existing create_demo_project() use karke professional demo load karega.
        """
        for car in self.car_manager.cars:
            if car.ecu is not None:
                self.active_car = car
                return

        self.car_manager.create_demo_project()
        self.active_car = self.car_manager.cars[-1]

    @property
    def car(self):
        return self.active_car

    @property
    def ecu(self):
        if self.car and self.car.ecu:
            return self.car.ecu
        return None

    @property
    def profile(self):
        if self.ecu:
            return self.ecu.profile
        return None

    @property
    def dyno(self):
        if self.profile:
            return self.profile.dyno
        return None

    @property
    def live_data(self):
        if self.profile:
            return self.profile.live_data
        return None

    def set_active_car(self, car):
        self.active_car = car

    def recalculate_dyno(self):
        """
        Existing Dyno class ke original methods call hote hain.
        UI koi separate calculation formula implement nahi karti.
        """
        if not self.car or not self.ecu or not self.dyno:
            return

        stock_hp = safe_float(self.car.engine.stock_horsepower)
        stock_torque = safe_float(self.car.engine.stock_torque)
        hp_gain = safe_float(self.profile.horsepower_gain)
        torque_gain = safe_float(self.profile.torque_gain)
        weight = safe_float(self.dyno.vehicle_weight, 1500)

        if weight <= 0:
            weight = 1500
            self.dyno.vehicle_weight = weight

        wheel_hp = self.dyno.calculate_wheel_horsepower(stock_hp, hp_gain)
        self.dyno.calculate_wheel_torque(stock_torque, torque_gain)
        self.dyno.calculate_zero_to_hundred(wheel_hp)
        self.dyno.calculate_quarter_mile(wheel_hp)
        self.dyno.calculate_top_speed(wheel_hp, weight)

    def get_faults(self):
        fault_file = ROOT_DIR / "database" / "fault_codes.json"

        try:
            with open(fault_file, "r", encoding="utf-8") as file:
                return json.load(file)
        except Exception:
            if self.profile:
                return [self.profile.diagnostic.to_dict()]
            return []

    def save_faults(self, faults):
        fault_file = ROOT_DIR / "database" / "fault_codes.json"
        fault_file.parent.mkdir(exist_ok=True)

        with open(fault_file, "w", encoding="utf-8") as file:
            json.dump(faults, file, indent=4)

    def save_cars(self):
        """
        Existing CarManager.save_cars() use karta hai.
        Neeche backend bug-fix section apply karne ke baad permanent save chalega.
        """
        self.car_manager.save_cars()


# -------------------------------------------------------------------
# THREAD WORKER
# -------------------------------------------------------------------

class ConsoleBridge:
    def __init__(self, callback):
        self.callback = callback

    def write(self, text):
        for line in str(text).splitlines():
            if line.strip():
                self.callback(line.strip())
        return len(text)

    def flush(self):
        pass


class BackendWorker(QThread):
    line = Signal(str)
    completed = Signal()
    failed = Signal(str)

    def __init__(self, operation):
        super().__init__()
        self.operation = operation

    def run(self):
        try:
            bridge = ConsoleBridge(self.line.emit)

            with redirect_stdout(bridge):
                self.operation()

            self.completed.emit()

        except Exception:
            self.failed.emit(traceback.format_exc())


# -------------------------------------------------------------------
# CUSTOM UI WIDGETS
# -------------------------------------------------------------------

class MetricCard(QFrame):
    def __init__(self, caption, value="--", unit=""):
        super().__init__()
        self.setObjectName("metric")
        self.setMinimumHeight(102)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(4)

        self.caption = QLabel(caption.upper())
        self.caption.setObjectName("metric_caption")

        self.value = QLabel(str(value))
        self.value.setObjectName("metric_value")

        self.unit = QLabel(unit)
        self.unit.setObjectName("metric_unit")

        layout.addWidget(self.caption)
        layout.addWidget(self.value)
        layout.addWidget(self.unit)

    def set_data(self, value, unit=""):
        self.value.setText(str(value))
        self.unit.setText(unit)


class GaugeWidget(QFrame):
    def __init__(self, label, unit, maximum, color="#2ddcff"):
        super().__init__()

        self.label = label
        self.unit = unit
        self.maximum = maximum
        self.color = QColor(color)
        self.current_value = 0.0

        self.setMinimumSize(180, 180)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def set_value(self, value):
        self.current_value = safe_float(value)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        width = self.width()
        height = self.height()
        size = min(width, height) - 30

        center_x = width / 2
        center_y = height / 2 + 8

        rect = QRectF(
            center_x - size / 2,
            center_y - size / 2,
            size,
            size,
        )

        background_pen = QPen(QColor("#20303e"), 12)
        background_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(background_pen)
        painter.drawArc(rect, 225 * 16, -270 * 16)

        percentage = max(0, min(self.current_value / self.maximum, 1))
        value_pen = QPen(self.color, 12)
        value_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(value_pen)
        painter.drawArc(rect, 225 * 16, int(-270 * 16 * percentage))

        painter.setPen(QColor("#ecf8ff"))
        painter.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        painter.drawText(
            QRectF(0, center_y - 22, width, 36),
            Qt.AlignmentFlag.AlignCenter,
            f"{self.current_value:.0f}",
        )

        painter.setPen(self.color)
        painter.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        painter.drawText(
            QRectF(0, center_y + 14, width, 24),
            Qt.AlignmentFlag.AlignCenter,
            self.unit.upper(),
        )

        painter.setPen(QColor("#8ca4b5"))
        painter.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        painter.drawText(
            QRectF(0, center_y + 45, width, 22),
            Qt.AlignmentFlag.AlignCenter,
            self.label.upper(),
        )


class DynoGraph(QFrame):
    """
    Visual dyno curve only.
    Actual HP / torque result existing Dyno class se hi aata hai.
    """

    def __init__(self, session):
        super().__init__()
        self.session = session
        self.setMinimumHeight(300)
        self.setObjectName("panel")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.rect().adjusted(55, 35, -25, -50)

        painter.fillRect(self.rect(), QColor("#101822"))

        grid_pen = QPen(QColor("#203243"), 1)
        painter.setPen(grid_pen)

        for index in range(6):
            y = rect.top() + (rect.height() / 5) * index
            painter.drawLine(rect.left(), y, rect.right(), y)

        for index in range(7):
            x = rect.left() + (rect.width() / 6) * index
            painter.drawLine(x, rect.top(), x, rect.bottom())

        painter.setPen(QColor("#71899c"))
        painter.setFont(QFont("Segoe UI", 9))

        painter.drawText(15, 24, "DYNO PERFORMANCE CURVE")
        painter.drawText(rect.left(), rect.bottom() + 28, "RPM")
        painter.drawText(10, rect.top() + 10, "POWER")

        dyno = self.session.dyno

        if not dyno:
            return

        peak_hp = safe_float(dyno.wheel_horsepower)
        peak_torque = safe_float(dyno.wheel_torque)

        if peak_hp <= 0:
            return

        max_value = max(peak_hp, peak_torque, 100) * 1.12

        hp_points = []
        torque_points = []

        for i in range(80):
            progress = i / 79

            hp_curve = peak_hp * (math.sin(progress * math.pi / 2) ** 0.70)
            torque_curve = peak_torque * (
                0.55 + 0.45 * math.sin(progress * math.pi)
            )

            x = rect.left() + progress * rect.width()
            y_hp = rect.bottom() - (hp_curve / max_value) * rect.height()
            y_torque = rect.bottom() - (torque_curve / max_value) * rect.height()

            hp_points.append((x, y_hp))
            torque_points.append((x, y_torque))

        hp_pen = QPen(QColor("#35d9ff"), 3)
        hp_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(hp_pen)

        for i in range(len(hp_points) - 1):
            painter.drawLine(
                hp_points[i][0],
                hp_points[i][1],
                hp_points[i + 1][0],
                hp_points[i + 1][1],
            )

        torque_pen = QPen(QColor("#ff8a3d"), 3)
        torque_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(torque_pen)

        for i in range(len(torque_points) - 1):
            painter.drawLine(
                torque_points[i][0],
                torque_points[i][1],
                torque_points[i + 1][0],
                torque_points[i + 1][1],
            )

        painter.setPen(QColor("#35d9ff"))
        painter.drawText(rect.right() - 145, rect.top() + 18, "● WHEEL HP")

        painter.setPen(QColor("#ff8a3d"))
        painter.drawText(rect.right() - 145, rect.top() + 38, "● WHEEL TORQUE")


# -------------------------------------------------------------------
# BASE PAGE
# -------------------------------------------------------------------

class BasePage(QWidget):
    def __init__(self, app, title, subtitle):
        super().__init__()
        self.app = app

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(28, 25, 28, 25)
        self.layout.setSpacing(18)

        title_label = QLabel(title)
        title_label.setObjectName("section_title")

        subtitle_label = QLabel(subtitle)
        subtitle_label.setObjectName("section_subtitle")

        self.layout.addWidget(title_label)
        self.layout.addWidget(subtitle_label)

    def refresh(self):
        pass


# -------------------------------------------------------------------
# DASHBOARD
# -------------------------------------------------------------------

class DashboardPage(BasePage):
    def __init__(self, app):
        super().__init__(
            app,
            "Performance Command Center",
            "Vehicle telemetry, tune status, ECU health and dyno performance overview.",
        )

        hero = make_panel()
        hero_layout = QHBoxLayout(hero)
        hero_layout.setContentsMargins(24, 22, 24, 22)

        left = QVBoxLayout()

        self.vehicle_name = QLabel("BMW M4 Competition")
        self.vehicle_name.setStyleSheet(
            "font-size: 28px; font-weight: 800; color: #f3fbff;"
        )

        self.vehicle_description = QLabel(
            "ECU Tuning Simulator • Professional Calibration Environment"
        )
        self.vehicle_description.setStyleSheet("color: #79a0b7;")

        self.ecu_status = QLabel("● ECU CONNECTED")
        self.ecu_status.setObjectName("status_good")

        buttons = QHBoxLayout()

        dyno_button = make_button("OPEN DYNO", primary=True)
        dyno_button.clicked.connect(lambda: app.navigate("Dyno"))

        live_button = make_button("LIVE DATA")
        live_button.clicked.connect(lambda: app.navigate("Live Data"))

        flash_button = make_button("ECU FLASH")
        flash_button.clicked.connect(lambda: app.navigate("Flash"))

        buttons.addWidget(dyno_button)
        buttons.addWidget(live_button)
        buttons.addWidget(flash_button)
        buttons.addStretch()

        left.addWidget(self.vehicle_name)
        left.addWidget(self.vehicle_description)
        left.addSpacing(8)
        left.addWidget(self.ecu_status)
        left.addSpacing(16)
        left.addLayout(buttons)

        hero_layout.addLayout(left, 3)

        hero_art = QLabel(
            "◢  PERFORMANCE\n    CALIBRATION\n        SYSTEM"
        )
        hero_art.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hero_art.setStyleSheet(
            """
            color: #35d9ff;
            font-size: 19px;
            font-weight: 800;
            letter-spacing: 2px;
            border-left: 1px solid #234257;
            padding-left: 32px;
            """
        )

        hero_layout.addWidget(hero_art, 1)

        self.layout.addWidget(hero)

        cards = QGridLayout()
        cards.setHorizontalSpacing(12)
        cards.setVerticalSpacing(12)

        self.hp_card = MetricCard("Wheel Horsepower", "--", "HP")
        self.torque_card = MetricCard("Wheel Torque", "--", "NM")
        self.zero_card = MetricCard("0 - 100 KM/H", "--", "SECONDS")
        self.top_card = MetricCard("Top Speed", "--", "KM/H")

        cards.addWidget(self.hp_card, 0, 0)
        cards.addWidget(self.torque_card, 0, 1)
        cards.addWidget(self.zero_card, 0, 2)
        cards.addWidget(self.top_card, 0, 3)

        self.layout.addLayout(cards)

        lower = QHBoxLayout()

        tune_panel = make_panel()
        tune_layout = QVBoxLayout(tune_panel)

        tune_title = QLabel("ACTIVE TUNE PROFILE")
        tune_title.setStyleSheet("font-size: 12px; color: #7fa3b7; font-weight: 800;")

        self.tune_details = QLabel()
        self.tune_details.setStyleSheet(
            "font-size: 15px; color: #e5f4fc; line-height: 160%;"
        )

        tune_layout.addWidget(tune_title)
        tune_layout.addWidget(self.tune_details)
        tune_layout.addStretch()

        system_panel = make_panel()
        system_layout = QVBoxLayout(system_panel)

        system_title = QLabel("SYSTEM STATUS")
        system_title.setStyleSheet("font-size: 12px; color: #7fa3b7; font-weight: 800;")

        self.system_details = QLabel()
        self.system_details.setStyleSheet(
            "font-size: 14px; color: #cfdeea; line-height: 170%;"
        )

        system_layout.addWidget(system_title)
        system_layout.addWidget(self.system_details)
        system_layout.addStretch()

        lower.addWidget(tune_panel)
        lower.addWidget(system_panel)

        self.layout.addLayout(lower)
        self.layout.addStretch()

    def refresh(self):
        car = self.app.session.car
        ecu = self.app.session.ecu
        dyno = self.app.session.dyno

        if not car:
            return

        self.vehicle_name.setText(f"{car.company} {car.model} • {car.year}")

        if ecu:
            status = ecu.connection_status.lower() == "connected"

            self.ecu_status.setText(
                "● ECU CONNECTED" if status else "● ECU DISCONNECTED"
            )
            self.ecu_status.setObjectName("status_good" if status else "status_bad")
            self.ecu_status.style().unpolish(self.ecu_status)
            self.ecu_status.style().polish(self.ecu_status)

            self.tune_details.setText(
                f"""
                <b>{ecu.profile.profile_name}</b><br>
                ECU: {ecu.ecu_brand} {ecu.ecu_model}<br>
                Firmware: {ecu.firmware.firmware_version}<br>
                Power gain: +{ecu.profile.horsepower_gain} HP<br>
                Torque gain: +{ecu.profile.torque_gain} Nm
                """
            )

            self.system_details.setText(
                f"""
                ECU Protocol: {ecu.protocol}<br>
                Engine: {car.engine.engine_code}<br>
                Fuel: {car.engine.fuel_type}<br>
                Aspiration: {car.engine.aspiration}<br>
                Engine Health: {car.engine.engine_status}
                """
            )

        if dyno:
            self.hp_card.set_data(f"{safe_float(dyno.wheel_horsepower):.0f}", "HP")
            self.torque_card.set_data(f"{safe_float(dyno.wheel_torque):.0f}", "NM")
            self.zero_card.set_data(f"{safe_float(dyno.zero_to_hundred):.2f}", "SECONDS")
            self.top_card.set_data(f"{safe_float(dyno.top_speed):.0f}", "KM/H")


# -------------------------------------------------------------------
# CAR MANAGEMENT
# -------------------------------------------------------------------

class VehicleEditor(QDialog):
    def __init__(self, car, parent=None):
        super().__init__(parent)
        self.car = car
        self.fields = []

        self.setWindowTitle("Edit Vehicle Configuration")
        self.resize(570, 610)

        layout = QVBoxLayout(self)
        form = QFormLayout()
        form.setSpacing(10)

        field_map = [
            ("VIN", car, "vin"),
            ("Company", car, "company"),
            ("Model", car, "model"),
            ("Year", car, "year"),
            ("Transmission", car, "transmission"),
            ("Drive Type", car, "drive_type"),
            ("Mileage", car, "mileage"),
            ("Color", car, "color"),
            ("License Plate", car, "license_plate"),
            ("Owner Name", car.owner, "name"),
            ("Owner Phone", car.owner, "phone"),
            ("Owner Email", car.owner, "email"),
            ("Owner City", car.owner, "city"),
            ("Engine Code", car.engine, "engine_code"),
            ("Stock HP", car.engine, "stock_horsepower"),
            ("Stock Torque", car.engine, "stock_torque"),
            ("Redline RPM", car.engine, "redline_rpm"),
            ("Engine Status", car.engine, "engine_status"),
        ]

        for label, object_ref, attribute in field_map:
            field = QLineEdit(str(getattr(object_ref, attribute)))
            form.addRow(label, field)
            self.fields.append((object_ref, attribute, field))

        layout.addLayout(form)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.save_changes)
        buttons.rejected.connect(self.reject)

        layout.addWidget(buttons)

    def save_changes(self):
        for object_ref, attribute, field in self.fields:
            old_value = getattr(object_ref, attribute)
            setattr(object_ref, attribute, coerce_value(old_value, field.text()))

        self.accept()


class CarsPage(BasePage):
    def __init__(self, app):
        super().__init__(
            app,
            "Vehicle Garage",
            "Manage connected vehicles, ownership information and engine specification.",
        )

        actions = QHBoxLayout()

        self.edit_button = make_button("EDIT VEHICLE", primary=True)
        self.edit_button.clicked.connect(self.edit_vehicle)

        self.demo_button = make_button("LOAD DEMO PROJECT")
        self.demo_button.clicked.connect(self.create_demo)

        actions.addWidget(self.edit_button)
        actions.addWidget(self.demo_button)
        actions.addStretch()

        self.layout.addLayout(actions)

        content = QHBoxLayout()

        self.car_list = QListWidget()
        self.car_list.setMinimumWidth(260)
        self.car_list.currentRowChanged.connect(self.select_car)

        content.addWidget(self.car_list, 1)

        details = make_panel()
        detail_layout = QVBoxLayout(details)

        self.detail_title = QLabel("Vehicle Information")
        self.detail_title.setStyleSheet("font-size: 19px; font-weight: 800;")

        self.detail_text = QLabel()
        self.detail_text.setStyleSheet(
            "font-size: 14px; color: #cfdeea; line-height: 170%;"
        )
        self.detail_text.setWordWrap(True)

        detail_layout.addWidget(self.detail_title)
        detail_layout.addSpacing(12)
        detail_layout.addWidget(self.detail_text)
        detail_layout.addStretch()

        content.addWidget(details, 2)

        self.layout.addLayout(content)
        self.layout.addStretch()

    def refresh(self):
        selected_car = self.app.session.car

        self.car_list.blockSignals(True)
        self.car_list.clear()

        selected_index = 0

        for index, car in enumerate(self.app.session.car_manager.cars):
            connected = "●" if car.ecu else "○"
            item = QListWidgetItem(
                f"{connected}  {car.company} {car.model}\n     VIN: {car.vin}"
            )
            self.car_list.addItem(item)

            if car is selected_car:
                selected_index = index

        self.car_list.setCurrentRow(selected_index)
        self.car_list.blockSignals(False)

        self.show_car_details(selected_car)

    def select_car(self, row):
        cars = self.app.session.car_manager.cars

        if 0 <= row < len(cars):
            self.app.session.set_active_car(cars[row])
            self.app.refresh_everything()

    def show_car_details(self, car):
        if not car:
            self.detail_text.setText("No vehicle selected.")
            return

        ecu_text = "Not Attached"

        if car.ecu:
            ecu_text = f"{car.ecu.ecu_brand} {car.ecu.ecu_model}"

        self.detail_title.setText(f"{car.company} {car.model}")

        self.detail_text.setText(
            f"""
            <b>VEHICLE IDENTIFICATION</b><br>
            VIN: {car.vin}<br>
            Model Year: {car.year}<br>
            Transmission: {car.transmission}<br>
            Drive Type: {car.drive_type}<br>
            Mileage: {car.mileage} km<br>
            Paint: {car.color}<br>
            License Plate: {car.license_plate}<br><br>

            <b>OWNER</b><br>
            {car.owner.name}<br>
            {car.owner.phone}<br>
            {car.owner.email}<br>
            {car.owner.city}<br><br>

            <b>ENGINE</b><br>
            {car.engine.engine_code} • {car.engine.displacement_cc} cc<br>
            {car.engine.cylinder} Cylinder • {car.engine.aspiration}<br>
            Stock Output: {car.engine.stock_horsepower} HP / {car.engine.stock_torque} Nm<br>
            ECU: {ecu_text}
            """
        )

    def edit_vehicle(self):
        car = self.app.session.car

        if not car:
            return

        editor = VehicleEditor(car, self)

        if editor.exec():
            self.app.session.recalculate_dyno()
            self.app.refresh_everything()

    def create_demo(self):
        self.app.session.car_manager.create_demo_project()
        self.app.session.set_active_car(self.app.session.car_manager.cars[-1])
        self.app.session.recalculate_dyno()
        self.app.refresh_everything()


# -------------------------------------------------------------------
# ECU PAGE
# -------------------------------------------------------------------

class ECUPage(BasePage):
    def __init__(self, app):
        super().__init__(
            app,
            "ECU Control Center",
            "Connection management, firmware overview and active calibration profile.",
        )

        top = QHBoxLayout()

        self.connection_label = QLabel("ECU DISCONNECTED")
        self.connection_label.setObjectName("status_bad")

        self.connection_button = make_button("CONNECT ECU", primary=True)
        self.connection_button.clicked.connect(self.toggle_connection)

        top.addWidget(self.connection_label)
        top.addStretch()
        top.addWidget(self.connection_button)

        self.layout.addLayout(top)

        grid = QGridLayout()
        grid.setSpacing(14)

        self.ecu_info = make_panel()
        self.firmware_info = make_panel()
        self.tune_info = make_panel()
        self.feature_info = make_panel()

        self.ecu_label = QLabel()
        self.firmware_label = QLabel()
        self.tune_label = QLabel()
        self.feature_label = QLabel()

        for panel, heading, label in [
            (self.ecu_info, "ECU HARDWARE", self.ecu_label),
            (self.firmware_info, "FIRMWARE", self.firmware_label),
            (self.tune_info, "ACTIVE TUNE", self.tune_label),
            (self.feature_info, "SUPPORTED FEATURES", self.feature_label),
        ]:
            layout = QVBoxLayout(panel)

            title = QLabel(heading)
            title.setStyleSheet("color: #78b4ca; font-size: 11px; font-weight: 800;")

            label.setStyleSheet("font-size: 14px; color: #dcebf5; line-height: 170%;")
            label.setWordWrap(True)

            layout.addWidget(title)
            layout.addSpacing(8)
            layout.addWidget(label)
            layout.addStretch()

        grid.addWidget(self.ecu_info, 0, 0)
        grid.addWidget(self.firmware_info, 0, 1)
        grid.addWidget(self.tune_info, 1, 0)
        grid.addWidget(self.feature_info, 1, 1)

        self.layout.addLayout(grid)

        options = make_panel()
        options_layout = QHBoxLayout(options)

        self.launch_check = QCheckBox("Launch Control")
        self.pops_check = QCheckBox("Pops & Bangs")

        self.save_options = make_button("SAVE TUNE OPTIONS")
        self.save_options.clicked.connect(self.save_tune_options)

        options_layout.addWidget(self.launch_check)
        options_layout.addWidget(self.pops_check)
        options_layout.addStretch()
        options_layout.addWidget(self.save_options)

        self.layout.addWidget(options)
        self.layout.addStretch()

    def refresh(self):
        ecu = self.app.session.ecu

        if not ecu:
            self.connection_label.setText("NO ECU ATTACHED")
            self.connection_label.setObjectName("status_bad")
            self.connection_button.setEnabled(False)
            return

        connected = ecu.connection_status.lower().strip() == "connected"

        self.connection_label.setText(
            "● ECU CONNECTED" if connected else "● ECU DISCONNECTED"
        )
        self.connection_label.setObjectName("status_good" if connected else "status_bad")

        self.connection_label.style().unpolish(self.connection_label)
        self.connection_label.style().polish(self.connection_label)

        self.connection_button.setText(
            "DISCONNECT ECU" if connected else "CONNECT ECU"
        )

        self.ecu_label.setText(
            f"""
            ECU ID: {ecu.ecu_id}<br>
            Brand: {ecu.ecu_brand}<br>
            Model: {ecu.ecu_model}<br>
            Protocol: {ecu.protocol}<br>
            Status: {ecu.connection_status}
            """
        )

        self.firmware_label.setText(
            f"""
            Version: {ecu.firmware.firmware_version}<br>
            Manufacturer: {ecu.firmware.manufacturer}<br>
            Release Year: {ecu.firmware.release_year}<br>
            Checksum: {ecu.firmware.checksum}<br>
            File Size: {ecu.firmware.file_size_mb} MB
            """
        )

        self.tune_label.setText(
            f"""
            Profile: {ecu.profile.profile_name}<br>
            Rev Limit: {ecu.profile.rev_limit} RPM<br>
            HP Gain: +{ecu.profile.horsepower_gain} HP<br>
            Torque Gain: +{ecu.profile.torque_gain} Nm<br>
            Fuel Map: {ecu.profile.fuel_map.fuel_map_name}
            """
        )

        features = "<br>".join(f"• {feature}" for feature in ecu.supported_features)
        self.feature_label.setText(features)

        self.launch_check.setChecked(
            str(ecu.profile.launch_control).lower() in ["enable", "enabled", "true", "yes"]
        )
        self.pops_check.setChecked(
            str(ecu.profile.pops_and_bangs).lower() in ["enable", "enabled", "true", "yes"]
        )

    def toggle_connection(self):
        ecu = self.app.session.ecu

        if not ecu:
            return

        connected = ecu.connection_status.lower().strip() == "connected"

        operation = ecu.disconnect_ecu if connected else ecu.connect_ecu

        self.connection_button.setEnabled(False)

        self.app.run_worker(
            operation,
            on_line=lambda line: self.connection_label.setText(line.upper()),
            on_complete=self.connection_finished,
        )

    def connection_finished(self):
        self.connection_button.setEnabled(True)
        self.app.refresh_everything()

    def save_tune_options(self):
        profile = self.app.session.profile

        if not profile:
            return

        profile.launch_control = "Enable" if self.launch_check.isChecked() else "Disable"
        profile.pops_and_bangs = "Enable" if self.pops_check.isChecked() else "Disable"

        self.app.show_message("Tune options updated successfully.")
        self.app.refresh_everything()


# -------------------------------------------------------------------
# GENERIC EDITOR PAGE
# -------------------------------------------------------------------

class ObjectEditorPage(BasePage):
    def __init__(self, app, title, subtitle, getter, fields):
        super().__init__(app, title, subtitle)

        self.getter = getter
        self.fields = fields
        self.inputs = {}

        panel = make_panel()
        panel_layout = QVBoxLayout(panel)

        self.notice = QLabel()
        self.notice.setStyleSheet("color: #ffad75; font-weight: 700;")

        form = QFormLayout()
        form.setSpacing(12)

        for attribute, label in self.fields:
            field = QLineEdit()
            self.inputs[attribute] = field
            form.addRow(label, field)

        self.save_button = make_button("APPLY CALIBRATION SETTINGS", primary=True)
        self.save_button.clicked.connect(self.save_changes)

        panel_layout.addWidget(self.notice)
        panel_layout.addSpacing(5)
        panel_layout.addLayout(form)
        panel_layout.addSpacing(10)
        panel_layout.addWidget(self.save_button)

        self.layout.addWidget(panel)
        self.layout.addStretch()

    def refresh(self):
        object_ref = self.getter()

        if not object_ref:
            self.notice.setText("No ECU profile available for the selected vehicle.")
            self.save_button.setEnabled(False)
            return

        self.notice.setText("Changes are applied to the currently active ECU profile.")
        self.save_button.setEnabled(True)

        for attribute, _label in self.fields:
            self.inputs[attribute].setText(str(getattr(object_ref, attribute)))

    def save_changes(self):
        object_ref = self.getter()

        if not object_ref:
            return

        for attribute, _label in self.fields:
            old_value = getattr(object_ref, attribute)
            new_value = self.inputs[attribute].text()
            setattr(object_ref, attribute, coerce_value(old_value, new_value))

        self.app.session.recalculate_dyno()
        self.app.show_message("Calibration settings applied.")
        self.app.refresh_everything()


# -------------------------------------------------------------------
# DYNO PAGE
# -------------------------------------------------------------------

class DynoPage(BasePage):
    def __init__(self, app):
        super().__init__(
            app,
            "Dyno Performance Simulator",
            "Wheel power simulation using the active engine, tune profile and drivetrain loss.",
        )

        action_row = QHBoxLayout()

        self.run_button = make_button("RUN DYNO SIMULATION", primary=True)
        self.run_button.clicked.connect(self.run_dyno)

        self.report_button = make_button("OPEN PERFORMANCE REPORT")
        self.report_button.clicked.connect(lambda: app.navigate("Reports"))

        action_row.addWidget(self.run_button)
        action_row.addWidget(self.report_button)
        action_row.addStretch()

        self.layout.addLayout(action_row)

        gauges = QHBoxLayout()

        self.hp_gauge = GaugeWidget("Wheel Power", "HP", 1000, "#32d9ff")
        self.torque_gauge = GaugeWidget("Wheel Torque", "NM", 1300, "#ff8c42")
        self.speed_gauge = GaugeWidget("Top Speed", "KM/H", 400, "#f0505a")

        gauges.addWidget(self.hp_gauge)
        gauges.addWidget(self.torque_gauge)
        gauges.addWidget(self.speed_gauge)

        self.layout.addLayout(gauges)

        cards = QGridLayout()

        self.zero_card = MetricCard("0 - 100 KM/H", "--", "SECONDS")
        self.quarter_card = MetricCard("Quarter Mile", "--", "SECONDS")
        self.speed_card = MetricCard("Top Speed", "--", "KM/H")
        self.grade_card = MetricCard("Performance Grade", "--", "ANALYSIS")

        cards.addWidget(self.zero_card, 0, 0)
        cards.addWidget(self.quarter_card, 0, 1)
        cards.addWidget(self.speed_card, 0, 2)
        cards.addWidget(self.grade_card, 0, 3)

        self.layout.addLayout(cards)

        self.graph = DynoGraph(app.session)
        self.layout.addWidget(self.graph)

    def get_grade(self):
        dyno = self.app.session.dyno
        car = self.app.session.car
        ecu = self.app.session.ecu

        if not dyno or not car or not ecu:
            return "--"

        result = capture_console_output(
            lambda: dyno.performance_analysis(car, ecu)
        )

        for line in result.splitlines():
            if "Grade" in line:
                return line.split(":")[-1].strip()

        return "--"

    def run_dyno(self):
        try:
            self.app.session.recalculate_dyno()
            self.app.show_message("Dyno simulation completed successfully.")
            self.app.refresh_everything()
        except Exception as error:
            QMessageBox.critical(self, "Dyno Error", str(error))

    def refresh(self):
        dyno = self.app.session.dyno

        if not dyno:
            return

        wheel_hp = safe_float(dyno.wheel_horsepower)
        wheel_torque = safe_float(dyno.wheel_torque)
        top_speed = safe_float(dyno.top_speed)

        self.hp_gauge.set_value(wheel_hp)
        self.torque_gauge.set_value(wheel_torque)
        self.speed_gauge.set_value(top_speed)

        self.zero_card.set_data(f"{safe_float(dyno.zero_to_hundred):.2f}", "SECONDS")
        self.quarter_card.set_data(f"{safe_float(dyno.quarter_mile):.2f}", "SECONDS")
        self.speed_card.set_data(f"{top_speed:.0f}", "KM/H")
        self.grade_card.set_data(self.get_grade(), "ANALYSIS")

        self.graph.update()


# -------------------------------------------------------------------
# FLASH PAGE
# -------------------------------------------------------------------

class FlashPage(BasePage):
    def __init__(self, app):
        super().__init__(
            app,
            "ECU Flash Center",
            "Create a secure backup and flash the selected ECU calibration file.",
        )

        status_panel = make_panel()
        status_layout = QHBoxLayout(status_panel)

        self.flash_status = QLabel("FLASH STATUS: --")
        self.flash_status.setStyleSheet("font-size: 16px; font-weight: 800;")

        self.backup_status = QLabel("BACKUP: --")
        self.backup_status.setStyleSheet("color: #8ca4b5; font-weight: 700;")

        status_layout.addWidget(self.flash_status)
        status_layout.addStretch()
        status_layout.addWidget(self.backup_status)

        self.layout.addWidget(status_panel)

        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        self.progress.setStyleSheet(
            """
            QProgressBar {
                border: 1px solid #294052;
                background: #0a1119;
                border-radius: 4px;
                text-align: center;
                height: 24px;
            }
            QProgressBar::chunk {
                background: #00a4d6;
                border-radius: 3px;
            }
            """
        )

        self.layout.addWidget(self.progress)

        buttons = QHBoxLayout()

        self.backup_button = make_button("CREATE BACKUP", primary=True)
        self.backup_button.clicked.connect(self.create_backup)

        self.flash_button = make_button("START ECU FLASH", danger=True)
        self.flash_button.clicked.connect(self.start_flash)

        buttons.addWidget(self.backup_button)
        buttons.addWidget(self.flash_button)
        buttons.addStretch()

        self.layout.addLayout(buttons)

        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setMinimumHeight(270)
        self.console.setStyleSheet(
            "font-family: Consolas, monospace; color: #8ee7ff; background: #071018;"
        )

        self.layout.addWidget(self.console)
        self.layout.addStretch()

    def refresh(self):
        profile = self.app.session.profile

        if not profile:
            return

        flash = profile.flash

        self.flash_status.setText(f"FLASH STATUS: {flash.flash_status}")
        self.backup_status.setText(f"BACKUP: {flash.backup_status}")

    def lock_buttons(self, locked):
        self.backup_button.setEnabled(not locked)
        self.flash_button.setEnabled(not locked)

    def append_log(self, line):
        self.console.append(f"> {line}")
        current = self.progress.value()
        self.progress.setValue(min(95, current + 14))

    def create_backup(self):
        profile = self.app.session.profile

        if not profile:
            return

        self.console.clear()
        self.progress.setValue(0)
        self.lock_buttons(True)

        self.app.run_worker(
            profile.flash.creat_backup,
            on_line=self.append_log,
            on_complete=self.backup_complete,
        )

    def backup_complete(self):
        self.progress.setValue(100)
        self.lock_buttons(False)
        self.console.append("> BACKUP PROCESS COMPLETED")
        self.app.refresh_everything()

    def start_flash(self):
        profile = self.app.session.profile

        if not profile:
            return

        flash = profile.flash

        if str(flash.backup_status).lower() != "created":
            QMessageBox.warning(
                self,
                "Backup Required",
                "Create ECU backup before starting the flash process.",
            )
            return

        self.console.clear()
        self.progress.setValue(0)
        self.lock_buttons(True)

        self.app.run_worker(
            flash.start_flash,
            on_line=self.append_log,
            on_complete=self.flash_complete,
        )

    def flash_complete(self):
        profile = self.app.session.profile

        if profile:
            profile.flash.flash_status = "Completed"

        self.progress.setValue(100)
        self.lock_buttons(False)
        self.console.append("> ECU FLASH COMPLETED SUCCESSFULLY")
        self.app.refresh_everything()


# -------------------------------------------------------------------
# DIAGNOSTIC PAGE
# -------------------------------------------------------------------

class DiagnosticPage(BasePage):
    def __init__(self, app):
        super().__init__(
            app,
            "Diagnostics & Fault Codes",
            "Read, filter, inspect and clear ECU diagnostic trouble codes.",
        )

        controls = QHBoxLayout()

        self.search = QLineEdit()
        self.search.setPlaceholderText("Search fault code, sensor or description...")
        self.search.textChanged.connect(self.populate_table)

        self.severity_filter = QComboBox()
        self.severity_filter.addItems(["All Severity", "Low", "Medium", "High", "Critical"])
        self.severity_filter.currentTextChanged.connect(self.populate_table)

        self.clear_selected = make_button("CLEAR SELECTED", danger=True)
        self.clear_selected.clicked.connect(self.clear_selected_fault)

        self.clear_all = make_button("CLEAR ALL")
        self.clear_all.clicked.connect(self.clear_all_faults)

        controls.addWidget(self.search, 3)
        controls.addWidget(self.severity_filter, 1)
        controls.addWidget(self.clear_selected)
        controls.addWidget(self.clear_all)

        self.layout.addLayout(controls)

        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(
            ["STATUS", "FAULT CODE", "FAULT NAME", "SEVERITY", "SENSOR"]
        )

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        self.table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )
        self.table.itemSelectionChanged.connect(self.show_fault_details)

        self.layout.addWidget(self.table)

        detail_panel = make_panel()
        detail_layout = QVBoxLayout(detail_panel)

        detail_title = QLabel("FAULT DETAILS")
        detail_title.setStyleSheet("color: #7fc1d8; font-weight: 800;")

        self.detail = QLabel("Select a fault code to view detailed description.")
        self.detail.setWordWrap(True)
        self.detail.setStyleSheet("color: #d2e2ed; line-height: 160%;")

        detail_layout.addWidget(detail_title)
        detail_layout.addWidget(self.detail)

        self.layout.addWidget(detail_panel)

    def filtered_faults(self):
        faults = self.app.session.get_faults()
        search_text = self.search.text().lower().strip()
        severity = self.severity_filter.currentText()

        result = []

        for fault in faults:
            content = " ".join(str(value) for value in fault.values()).lower()

            if search_text and search_text not in content:
                continue

            if severity != "All Severity":
                if str(fault.get("severity", "")).lower() != severity.lower():
                    continue

            result.append(fault)

        return result

    def populate_table(self):
        faults = self.filtered_faults()

        self.table.setRowCount(0)

        severity_colors = {
            "low": QColor("#4da6ff"),
            "medium": QColor("#f5c451"),
            "high": QColor("#ff843f"),
            "critical": QColor("#f14e58"),
        }

        for row, fault in enumerate(faults):
            self.table.insertRow(row)

            status = str(fault.get("status", "Unknown"))
            severity = str(fault.get("severity", "Unknown"))

            values = [
                f"● {status}",
                fault.get("fault_code", "--"),
                fault.get("fault_name", "--"),
                severity,
                fault.get("sensor", "--"),
            ]

            for column, value in enumerate(values):
                item = QTableWidgetItem(str(value))

                if column == 3:
                    item.setForeground(
                        severity_colors.get(
                            severity.lower(),
                            QColor("#dcecf6"),
                        )
                    )

                self.table.setItem(row, column, item)

            self.table.item(row, 0).setData(
                Qt.ItemDataRole.UserRole,
                fault.get("fault_code", ""),
            )

    def show_fault_details(self):
        selected = self.table.selectedItems()

        if not selected:
            return

        code = self.table.item(selected[0].row(), 0).data(
            Qt.ItemDataRole.UserRole
        )

        for fault in self.app.session.get_faults():
            if fault.get("fault_code") == code:
                self.detail.setText(
                    f"""
                    <b>{fault.get("fault_code")}: {fault.get("fault_name")}</b><br><br>
                    Severity: <b>{fault.get("severity")}</b><br>
                    Status: <b>{fault.get("status")}</b><br>
                    Sensor: {fault.get("sensor")}<br><br>
                    {fault.get("description")}
                    """
                )
                return

    def clear_selected_fault(self):
        selected = self.table.selectedItems()

        if not selected:
            QMessageBox.warning(self, "No Fault Selected", "Select a fault code first.")
            return

        row = selected[0].row()
        code = self.table.item(row, 0).data(Qt.ItemDataRole.UserRole)

        faults = self.app.session.get_faults()

        for fault in faults:
            if str(fault.get("fault_code")).lower() == str(code).lower():
                fault["status"] = "Cleared"

        self.app.session.save_faults(faults)
        self.populate_table()
        self.detail.setText("Selected fault status changed to Cleared.")

    def clear_all_faults(self):
        answer = QMessageBox.question(
            self,
            "Clear All Faults",
            "Do you want to clear all diagnostic trouble codes?",
        )

        if answer != QMessageBox.StandardButton.Yes:
            return

        faults = self.app.session.get_faults()

        for fault in faults:
            fault["status"] = "Cleared"

        self.app.session.save_faults(faults)
        self.populate_table()
        self.detail.setText("All fault codes have been cleared.")

    def refresh(self):
        self.populate_table()


# -------------------------------------------------------------------
# LIVE DATA PAGE
# -------------------------------------------------------------------

class LiveDataPage(BasePage):
    def __init__(self, app):
        super().__init__(
            app,
            "Live Data Monitor",
            "Real-time ECU telemetry simulation using the existing LiveData engine.",
        )

        toolbar = QHBoxLayout()

        self.status = QLabel("MONITOR IDLE")
        self.status.setObjectName("status_bad")

        self.start_button = make_button("START LIVE MONITOR", primary=True)
        self.start_button.clicked.connect(self.start_monitor)

        toolbar.addWidget(self.status)
        toolbar.addStretch()
        toolbar.addWidget(self.start_button)

        self.layout.addLayout(toolbar)

        gauge_grid = QGridLayout()
        gauge_grid.setSpacing(14)

        self.rpm = GaugeWidget("Engine RPM", "RPM", 9500, "#35d9ff")
        self.speed = GaugeWidget("Vehicle Speed", "KM/H", 350, "#5af1ba")
        self.throttle = GaugeWidget("Throttle", "%", 100, "#ffd05d")
        self.boost = GaugeWidget("Boost Pressure", "BAR", 3.5, "#ff8d42")
        self.temp = GaugeWidget("Engine Temp", "°C", 150, "#f05b65")
        self.afr = GaugeWidget("Air Fuel Ratio", "AFR", 20, "#bc80ff")
        self.battery = GaugeWidget("Battery Voltage", "V", 16, "#7dc9ff")
        self.gear = GaugeWidget("Current Gear", "GEAR", 8, "#e8f3ff")

        gauges = [
            self.rpm,
            self.speed,
            self.throttle,
            self.boost,
            self.temp,
            self.afr,
            self.battery,
            self.gear,
        ]

        for index, gauge in enumerate(gauges):
            gauge_grid.addWidget(gauge, index // 4, index % 4)

        self.layout.addLayout(gauge_grid)
        self.layout.addStretch()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh)

    def start_monitor(self):
        live = self.app.session.live_data

        if not live:
            QMessageBox.warning(self, "No ECU", "No LiveData object is available.")
            return

        self.status.setText("● LIVE ECU STREAM ACTIVE")
        self.status.setObjectName("status_good")
        self.status.style().unpolish(self.status)
        self.status.style().polish(self.status)

        self.start_button.setEnabled(False)
        self.timer.start(250)

        self.app.run_worker(
            live.start_live_monitor,
            on_line=lambda _line: None,
            on_complete=self.monitor_finished,
        )

    def monitor_finished(self):
        self.timer.stop()
        self.start_button.setEnabled(True)
        self.status.setText("● LIVE CAPTURE COMPLETE")
        self.status.setObjectName("status_good")
        self.status.style().unpolish(self.status)
        self.status.style().polish(self.status)
        self.refresh()

    def refresh(self):
        live = self.app.session.live_data

        if not live:
            return

        self.rpm.set_value(live.rpm)
        self.speed.set_value(live.speed)
        self.throttle.set_value(live.throttle_position)
        self.boost.set_value(live.boost_pressure)
        self.temp.set_value(live.engine_temperature)
        self.afr.set_value(live.air_fuel_ratio)
        self.battery.set_value(live.battery_voltage)
        self.gear.set_value(live.gear)


# -------------------------------------------------------------------
# REPORT PAGE
# -------------------------------------------------------------------

class ReportsPage(BasePage):
    def __init__(self, app):
        super().__init__(
            app,
            "Professional Performance Report",
            "Printable dyno and performance analysis generated from existing backend calculations.",
        )

        actions = QHBoxLayout()

        generate = make_button("REFRESH REPORT", primary=True)
        generate.clicked.connect(self.refresh)

        print_button = make_button("PRINT REPORT")
        print_button.clicked.connect(self.print_report)

        actions.addWidget(generate)
        actions.addWidget(print_button)
        actions.addStretch()

        self.layout.addLayout(actions)

        self.browser = QTextBrowser()
        self.browser.setOpenExternalLinks(False)
        self.browser.setMinimumHeight(500)

        self.layout.addWidget(self.browser)

    def refresh(self):
        car = self.app.session.car
        ecu = self.app.session.ecu
        dyno = self.app.session.dyno

        if not car or not ecu or not dyno:
            self.browser.setHtml("<h2>No ECU performance data available.</h2>")
            return

        report_output = capture_console_output(
            lambda: dyno.generate_performance_report(car, ecu)
        )

        analysis_output = capture_console_output(
            lambda: dyno.performance_analysis(car, ecu)
        )

        report_output = html.escape(report_output)
        analysis_output = html.escape(analysis_output)

        self.browser.setHtml(
            f"""
            <html>
            <head>
                <style>
                    body {{
                        background: #ffffff;
                        color: #1a2730;
                        font-family: Arial;
                        padding: 30px;
                    }}

                    h1 {{
                        color: #063f5a;
                        border-bottom: 3px solid #00a7d9;
                        padding-bottom: 12px;
                    }}

                    h2 {{
                        color: #045879;
                        margin-top: 28px;
                    }}

                    .brand {{
                        color: #0087b5;
                        font-weight: bold;
                        letter-spacing: 2px;
                    }}

                    .card {{
                        background: #eef7fb;
                        border-left: 5px solid #00a7d9;
                        padding: 14px;
                        margin: 15px 0;
                    }}

                    pre {{
                        background: #f2f5f7;
                        border: 1px solid #d4e0e8;
                        padding: 17px;
                        white-space: pre-wrap;
                        font-family: Consolas;
                        font-size: 12px;
                    }}
                </style>
            </head>

            <body>
                <div class="brand">ECU TUNING SOFTWARE SIMULATOR</div>
                <h1>Professional Performance Report</h1>

                <div class="card">
                    <b>Vehicle:</b> {car.company} {car.model} ({car.year})<br>
                    <b>VIN:</b> {car.vin}<br>
                    <b>ECU:</b> {ecu.ecu_brand} {ecu.ecu_model}<br>
                    <b>Active Tune:</b> {ecu.profile.profile_name}
                </div>

                <h2>Dyno Performance Report</h2>
                <pre>{report_output}</pre>

                <h2>Performance Analysis</h2>
                <pre>{analysis_output}</pre>

                <p style="margin-top: 35px; color: #71808c;">
                    Generated by ECU Tuning Software Simulator • Professional Calibration Environment
                </p>
            </body>
            </html>
            """
        )

    def print_report(self):
        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        dialog = QPrintDialog(printer, self)

        if dialog.exec():
            self.browser.document().print_(printer)


# -------------------------------------------------------------------
# SETTINGS PAGE
# -------------------------------------------------------------------

class SettingsPage(BasePage):
    def __init__(self, app):
        super().__init__(
            app,
            "Application Settings",
            "Session management, database persistence and simulation environment settings.",
        )

        panel = make_panel()
        panel_layout = QVBoxLayout(panel)

        self.storage_info = QLabel()
        self.storage_info.setStyleSheet("line-height: 170%; color: #d5e5ef;")
        self.storage_info.setWordWrap(True)

        self.save_button = make_button("SAVE CURRENT SESSION", primary=True)
        self.save_button.clicked.connect(self.save_session)

        panel_layout.addWidget(self.storage_info)
        panel_layout.addSpacing(15)
        panel_layout.addWidget(self.save_button)
        panel_layout.addStretch()

        self.layout.addWidget(panel)
        self.layout.addStretch()

    def refresh(self):
        car_count = len(self.app.session.car_manager.cars)

        self.storage_info.setText(
            f"""
            <b>UI Framework:</b> PySide6 Desktop Application<br>
            <b>Theme:</b> Dark Professional / Motorsport Engineering<br>
            <b>Vehicles in Session:</b> {car_count}<br>
            <b>Database Path:</b> database/cars.json<br><br>

            The current session uses your existing CarManager, Car, ECU,
            Dyno, Flash, Diagnostic and LiveData backend objects.
            """
        )

    def save_session(self):
        try:
            self.app.session.save_cars()
            QMessageBox.information(
                self,
                "Save Complete",
                "Vehicle and ECU session saved successfully.",
            )
        except Exception as error:
            QMessageBox.warning(
                self,
                "Backend Save Issue",
                f"Current backend serializer returned an error:\n\n{error}\n\n"
                "Apply the ECUFlash.to_dict() fix given below.",
            )


# -------------------------------------------------------------------
# MAIN WINDOW
# -------------------------------------------------------------------

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ECU Tuning Software Simulator")
        self.setMinimumSize(1280, 760)
        self.resize(1580, 920)

        self.session = BackendSession()
        self.workers = []

        root = QWidget()
        self.setCentralWidget(root)

        root_layout = QHBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # ---------------- SIDEBAR ----------------

        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(225)

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(14, 20, 14, 18)
        sidebar_layout.setSpacing(7)

        logo = QLabel("ECU // STUDIO")
        logo.setObjectName("logo")

        version = QLabel("PROFESSIONAL CALIBRATION SYSTEM\nVERSION 1.0")
        version.setStyleSheet(
            "color: #648093; font-size: 9px; font-weight: 700; letter-spacing: 1px;"
        )

        sidebar_layout.addWidget(logo)
        sidebar_layout.addWidget(version)
        sidebar_layout.addSpacing(24)

        self.nav_buttons = {}

        navigation = [
            "Dashboard",
            "Cars",
            "ECU",
            "Fuel Maps",
            "Turbo",
            "Dyno",
            "Flash",
            "Diagnostics",
            "Live Data",
            "Reports",
            "Settings",
        ]

        for page_name in navigation:
            button = QPushButton(page_name)
            button.setObjectName("nav_button")
            button.setCheckable(True)
            button.clicked.connect(
                lambda checked=False, name=page_name: self.navigate(name)
            )

            sidebar_layout.addWidget(button)
            self.nav_buttons[page_name] = button

        sidebar_layout.addStretch()

        footer = QLabel("ENGINEERING MODE\n● SYSTEM ONLINE")
        footer.setStyleSheet(
            "color: #49d7a1; font-size: 10px; font-weight: 800; line-height: 150%;"
        )

        sidebar_layout.addWidget(footer)

        root_layout.addWidget(sidebar)

        # ---------------- CENTER ----------------

        center = QWidget()
        center_layout = QVBoxLayout(center)
        center_layout.setContentsMargins(0, 0, 0, 0)
        center_layout.setSpacing(0)

        topbar = QFrame()
        topbar.setObjectName("topbar")
        topbar.setFixedHeight(72)

        top_layout = QHBoxLayout(topbar)
        top_layout.setContentsMargins(25, 10, 25, 10)

        self.top_vehicle = QLabel()
        self.top_vehicle.setStyleSheet("font-weight: 800; color: #effaff; font-size: 14px;")

        self.top_ecu = QLabel()
        self.top_ecu.setStyleSheet("color: #7e9bad; font-size: 12px;")

        top_left = QVBoxLayout()
        top_left.setSpacing(2)
        top_left.addWidget(self.top_vehicle)
        top_left.addWidget(self.top_ecu)

        self.top_connection = QLabel()
        self.top_connection.setObjectName("status_good")

        top_layout.addLayout(top_left)
        top_layout.addStretch()
        top_layout.addWidget(self.top_connection)

        center_layout.addWidget(topbar)

        self.stack = QStackedWidget()

        self.pages = {
            "Dashboard": DashboardPage(self),
            "Cars": CarsPage(self),
            "ECU": ECUPage(self),
            "Fuel Maps": ObjectEditorPage(
                self,
                "Fuel Map Calibration",
                "Adjust AFR target, injector configuration, fuel pressure and operating mode.",
                lambda: self.session.profile.fuel_map if self.session.profile else None,
                [
                    ("fuel_map_name", "Fuel Map Name"),
                    ("afr", "Target AFR"),
                    ("injector_size", "Injector Size"),
                    ("fuel_pressure", "Fuel Pressure"),
                    ("mode", "Tune Mode"),
                    ("fuel_type", "Fuel Type"),
                ],
            ),
            "Turbo": ObjectEditorPage(
                self,
                "Turbocharger Management",
                "Configure boost pressure, wastegate, spool RPM and turbo hardware parameters.",
                lambda: self.session.profile.turbo if self.session.profile else None,
                [
                    ("turbo_name", "Turbo Name"),
                    ("turbo_brand", "Turbo Brand"),
                    ("turbo_type", "Turbo Type"),
                    ("boost_pressure", "Boost Pressure"),
                    ("wastegate_pressure", "Wastegate Pressure"),
                    ("spool_rpm", "Spool RPM"),
                    ("anti_lag", "Anti-Lag"),
                    ("intercooler_type", "Intercooler Type"),
                    ("horsepower_support", "Horsepower Support"),
                ],
            ),
            "Dyno": DynoPage(self),
            "Flash": FlashPage(self),
            "Diagnostics": DiagnosticPage(self),
            "Live Data": LiveDataPage(self),
            "Reports": ReportsPage(self),
            "Settings": SettingsPage(self),
        }

        self.page_indices = {}

        for index, (name, page) in enumerate(self.pages.items()):
            self.stack.addWidget(page)
            self.page_indices[name] = index

        center_layout.addWidget(self.stack)
        root_layout.addWidget(center, 1)

        # ---------------- RIGHT QUICK STATS ----------------

        right = QFrame()
        right.setObjectName("rightpanel")
        right.setFixedWidth(245)

        right_layout = QVBoxLayout(right)
        right_layout.setContentsMargins(16, 20, 16, 18)
        right_layout.setSpacing(10)

        quick_title = QLabel("VEHICLE QUICK STATS")
        quick_title.setStyleSheet(
            "font-size: 12px; color: #84b6ca; font-weight: 800; letter-spacing: 1px;"
        )

        right_layout.addWidget(quick_title)
        right_layout.addSpacing(8)

        self.quick_hp = MetricCard("Horsepower", "--", "HP")
        self.quick_torque = MetricCard("Torque", "--", "NM")
        self.quick_rpm = MetricCard("RPM", "--", "RPM")
        self.quick_boost = MetricCard("Boost", "--", "BAR")
        self.quick_afr = MetricCard("AFR", "--", "RATIO")
        self.quick_temp = MetricCard("Temperature", "--", "°C")
        self.quick_battery = MetricCard("Battery", "--", "V")

        for card in [
            self.quick_hp,
            self.quick_torque,
            self.quick_rpm,
            self.quick_boost,
            self.quick_afr,
            self.quick_temp,
            self.quick_battery,
        ]:
            right_layout.addWidget(card)

        right_layout.addStretch()
        root_layout.addWidget(right)

        self.navigate("Dashboard")
        self.refresh_everything()

    def navigate(self, page_name):
        if page_name not in self.page_indices:
            return

        self.stack.setCurrentIndex(self.page_indices[page_name])

        for name, button in self.nav_buttons.items():
            button.setChecked(name == page_name)

        page = self.pages.get(page_name)

        if page:
            page.refresh()

    def refresh_topbar(self):
        car = self.session.car
        ecu = self.session.ecu

        if car:
            self.top_vehicle.setText(f"{car.company} {car.model} • VIN {car.vin}")
        else:
            self.top_vehicle.setText("No Vehicle Selected")

        if ecu:
            self.top_ecu.setText(
                f"{ecu.ecu_brand} {ecu.ecu_model} • Tune: {ecu.profile.profile_name}"
            )

            connected = ecu.connection_status.lower().strip() == "connected"

            self.top_connection.setText(
                "● ECU CONNECTED" if connected else "● ECU DISCONNECTED"
            )
            self.top_connection.setObjectName(
                "status_good" if connected else "status_bad"
            )

        else:
            self.top_ecu.setText("No ECU Attached")
            self.top_connection.setText("● ECU OFFLINE")
            self.top_connection.setObjectName("status_bad")

        self.top_connection.style().unpolish(self.top_connection)
        self.top_connection.style().polish(self.top_connection)

    def refresh_quick_stats(self):
        dyno = self.session.dyno
        live = self.session.live_data

        if dyno:
            self.quick_hp.set_data(f"{safe_float(dyno.wheel_horsepower):.0f}", "HP")
            self.quick_torque.set_data(f"{safe_float(dyno.wheel_torque):.0f}", "NM")

        if live:
            self.quick_rpm.set_data(f"{safe_float(live.rpm):.0f}", "RPM")
            self.quick_boost.set_data(f"{safe_float(live.boost_pressure):.2f}", "BAR")
            self.quick_afr.set_data(f"{safe_float(live.air_fuel_ratio):.2f}", "RATIO")
            self.quick_temp.set_data(f"{safe_float(live.engine_temperature):.0f}", "°C")
            self.quick_battery.set_data(f"{safe_float(live.battery_voltage):.2f}", "V")

    def refresh_everything(self):
        self.refresh_topbar()
        self.refresh_quick_stats()

        for page in self.pages.values():
            page.refresh()

    def run_worker(self, operation, on_line=None, on_complete=None):
        worker = BackendWorker(operation)
        self.workers.append(worker)

        if on_line:
            worker.line.connect(on_line)

        def completed():
            if on_complete:
                on_complete()

            if worker in self.workers:
                self.workers.remove(worker)

            worker.deleteLater()

        def failed(error_message):
            QMessageBox.critical(
                self,
                "Backend Operation Error",
                error_message,
            )

            if worker in self.workers:
                self.workers.remove(worker)

            worker.deleteLater()

        worker.completed.connect(completed)
        worker.failed.connect(failed)
        worker.start()

    def show_message(self, text):
        QMessageBox.information(self, "ECU Studio", text)


# -------------------------------------------------------------------
# APPLICATION ENTRY POINT
# -------------------------------------------------------------------

if __name__ == "__main__":
    application = QApplication(sys.argv)
    application.setStyleSheet(APP_STYLE)

    window = MainWindow()
    window.show()

    sys.exit(application.exec())