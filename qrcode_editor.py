import qrcode
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
from qrcode.image.styles.moduledrawers.pil import *
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.colormasks import *
from PIL import ImageColor
import re


def is_valid_hex_color(hexa_color):

    regex = "^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$"
    p = re.compile(regex)
    if hexa_color == "":
        return False
    if re.search(p, hexa_color):
        return True
    else:
        return False


class QrCode(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QrCode Creator")

        self.main_layout = QVBoxLayout()

        # Title
        self.title = QLabel()
        self.title.setText("QrCode Editor")
        self.title.setFont(QFont('Bahnschrift', 18))
        self.title.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.title)

        # Spacer 1
        self.spacer1 = QSpacerItem(20, 50, QSizePolicy.Minimum, QSizePolicy.Maximum)
        self.main_layout.addItem(self.spacer1)

        # Create horizontal layout
        self.h_layout1 = QHBoxLayout()
        self.main_layout.addLayout(self.h_layout1)

        # Creating the two widgets
        self.qrcode_widget = QWidget(self)
        self.h_layout2 = QHBoxLayout()
        self.qrcode_widget.setLayout(self.h_layout2)
        self.h_layout1.addWidget(self.qrcode_widget)

        self.settings_widget = QWidget(self)
        self.form_layout = QFormLayout(self.settings_widget)
        self.settings_widget.setLayout(self.form_layout)
        self.h_layout1.addWidget(self.settings_widget)

        # Populating qrcode_widget
        self.spacer2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.h_layout2.addItem(self.spacer2)
        self.qrcode_img = QLabel()
        self.qrcode_img.setText("")
        self.qrcode_img.setPixmap(QPixmap('YourQrn.png'))
        self.qrcode_img.setAlignment(Qt.AlignCenter)
        self.h_layout2.addWidget(self.qrcode_img)
        self.spacer3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.h_layout2.addItem(self.spacer3)

        # Populating settings_widget
        self.spacer4 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.form_layout.addItem(self.spacer4)

        settings_font = QFont("Bahnschrift", 11)

        self.data_label = QLabel("Data:")
        self.data_label.setFont(settings_font)
        self.data_edit = QLineEdit()
        self.form_layout.addRow(self.data_label, self.data_edit)

        self.error_label = QLabel("Error correction:")
        self.error_label.setFont(settings_font)
        self.error_comboBox = QComboBox(self.settings_widget)
        self.form_layout.addRow(self.error_label, self.error_comboBox)

        self.shape_label = QLabel("Shape:")
        self.shape_label.setFont(settings_font)
        self.shape_comboBox = QComboBox(self.settings_widget)
        self.form_layout.addRow(self.shape_label, self.shape_comboBox)

        self.colormask_label = QLabel("Color mask:")
        self.colormask_label.setFont(settings_font)
        self.colormask_comboBox = QComboBox(self.settings_widget)
        self.form_layout.addRow(self.colormask_label, self.colormask_comboBox)

        self.colormaskimg_label = QLabel("Color mask image:")
        self.colormaskimg_label.setFont(settings_font)
        self.colormaskimg_label.hide()
        self.hlayout3 = QHBoxLayout()
        self.colormaskimg_path_edit = QLineEdit()
        self.colormaskimg_path_edit.setReadOnly(True)
        self.colormaskimg_path_edit.hide()
        self.hlayout3.addWidget(self.colormaskimg_path_edit)
        self.colormaskimg_btn = QPushButton("Select image")
        self.colormaskimg_btn.hide()
        self.hlayout3.addWidget(self.colormaskimg_btn)
        self.form_layout.addRow(self.colormaskimg_label, self.hlayout3)

        self.color_from_label = QLabel("Fill color (HEX):")
        self.color_from_label.setFont(settings_font)
        self.color_from_edit = QLineEdit()
        self.form_layout.addRow(self.color_from_label, self.color_from_edit)

        self.color_to_label = QLabel("Fill color (HEX):")
        self.color_to_label.setFont(settings_font)
        self.color_to_label.hide()
        self.color_to_edit = QLineEdit()
        self.color_to_edit.hide()
        self.form_layout.addRow(self.color_to_label, self.color_to_edit)

        self.background_label = QLabel("Background (HEX):")
        self.background_label.setFont(settings_font)
        self.background_edit = QLineEdit()
        self.form_layout.addRow(self.background_label, self.background_edit)


        self.addimg_label = QLabel("Add image:")
        self.addimg_label.setFont(settings_font)
        self.addimg_checkbox = QCheckBox()
        self.form_layout.addRow(self.addimg_label, self.addimg_checkbox)

        self.openimg_label = QLabel("Image:")
        self.openimg_label.setFont(settings_font)
        self.openimg_label.hide()
        self.hlayout4 = QHBoxLayout()
        self.openimg_path_edit = QLineEdit()
        self.openimg_path_edit.setReadOnly(True)
        self.openimg_path_edit.hide()
        self.hlayout4.addWidget(self.openimg_path_edit)
        self.openimg_btn = QPushButton("Select image")
        self.openimg_btn.hide()
        self.hlayout4.addWidget(self.openimg_btn)
        self.form_layout.addRow(self.openimg_label, self.hlayout4)

        self.spacer6 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Maximum)
        self.form_layout.addItem(self.spacer6)
        self.apply_btn = QPushButton("Apply")
        self.form_layout.addWidget(self.apply_btn)

        self.spacer7 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Maximum)
        self.form_layout.addItem(self.spacer7)
        self.saveimg_btn = QPushButton("Save image")
        self.form_layout.addWidget(self.saveimg_btn)

        self.spacer5 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.form_layout.addItem(self.spacer5)

        # Populating ComboBoxes
        self.error_comboBox.addItems(["Low error correction ~ 7%", "Medium error correction ~ 15%", "Decent error correction ~ 25%", "High error correction ~ 30%"])
        self.shape_comboBox.addItems(["Squares", "Gapped squares", "Circles", "Rounded", "Vertical bars", "Horizonta bars"])
        self.colormask_comboBox.addItems(["Solid fill", "Square gradient", "Radial gradient", "Vertical gradient", "Horizontal gradient", "Image color mask"])

        # Buttons and checkboxes connect
        self.addimg_checkbox.stateChanged.connect(self.addimg_checked)
        self.apply_btn.clicked.connect(self.clicked_apply)
        self.openimg_btn.clicked.connect(self.select_image)
        self.colormask_comboBox.currentIndexChanged.connect(self.selected_imgmask)
        self.colormaskimg_btn.clicked.connect(self.select_imgmask)
        self.saveimg_btn.clicked.connect(self.clicked_save)

        self.setLayout(self.main_layout)

        self.selected_image_path = ""
        self.selected_imgmask_path = ""
        self.canBeSaved = False
        self.qrcode_save_img = None

    # What to show depending on colormask Combo BOX
    def selected_imgmask(self):
        match self.colormask_comboBox.currentIndex():
            case 0:
                self.colormaskimg_label.hide()
                self.colormaskimg_btn.hide()
                self.colormaskimg_path_edit.hide()
                self.color_to_label.hide()
                self.color_to_edit.hide()
                self.color_from_label.show()
                self.color_from_edit.show()
                self.color_from_label.setText("Fill Color (HEX):")

            case 1:
                self.colormaskimg_label.hide()
                self.colormaskimg_btn.hide()
                self.colormaskimg_path_edit.hide()
                self.color_to_label.show()
                self.color_to_edit.show()
                self.color_from_label.show()
                self.color_from_edit.show()
                self.color_from_label.setText("Center color (HEX):")
                self.color_to_label.setText("Edge color (HEX):")

            case 2:
                self.colormaskimg_label.hide()
                self.colormaskimg_btn.hide()
                self.colormaskimg_path_edit.hide()
                self.color_to_label.show()
                self.color_to_edit.show()
                self.color_from_label.show()
                self.color_from_edit.show()
                self.color_from_label.setText("Center color (HEX):")
                self.color_to_label.setText("Edge color (HEX):")

            case 3:
                self.colormaskimg_label.hide()
                self.colormaskimg_btn.hide()
                self.colormaskimg_path_edit.hide()
                self.color_to_label.show()
                self.color_to_edit.show()
                self.color_from_label.show()
                self.color_from_edit.show()
                self.color_from_label.setText("Top color (HEX):")
                self.color_to_label.setText("Bottom color (HEX):")

            case 4:
                self.colormaskimg_label.hide()
                self.colormaskimg_btn.hide()
                self.colormaskimg_path_edit.hide()
                self.color_to_label.show()
                self.color_to_edit.show()
                self.color_from_label.show()
                self.color_from_edit.show()
                self.color_from_label.setText("Left color (HEX):")
                self.color_to_label.setText("Right color (HEX):")

            case 5:
                self.colormaskimg_label.show()
                self.colormaskimg_btn.show()
                self.colormaskimg_path_edit.show()
                self.color_to_label.hide()
                self.color_to_edit.hide()
                self.color_from_label.hide()
                self.color_from_edit.hide()

    # Select color mask image
    def select_imgmask(self):
        self.selected_imgmask_path, _ = QFileDialog.getOpenFileName(self, "Select image", "", "Image files (*.png *.jpg *.jpeg)")
        self.colormaskimg_path_edit.setText(self.selected_imgmask_path)

    # Select Image in the middle
    def select_image(self):
        self.selected_image_path, _ = QFileDialog.getOpenFileName(self, "Open image", "", "Image files (*.png *.jpg *.jpeg)")
        self.openimg_path_edit.setText(self.selected_image_path)

    # Adding an image? or no?
    def addimg_checked(self):
        isChecked = self.addimg_checkbox.isChecked()
        if isChecked:
            self.openimg_label.show()
            self.openimg_btn.show()
            self.openimg_path_edit.show()
            self.error_comboBox.setCurrentIndex(3)
        else:
            self.openimg_label.hide()
            self.openimg_btn.hide()
            self.openimg_path_edit.hide()

    # Clicked apply button
    def clicked_apply(self):

        # Get data from GUI
        data = self.data_edit.text()
        error_correction = self.error_comboBox.currentIndex()
        shape = self.shape_comboBox.currentIndex()
        colormask = self.colormask_comboBox.currentIndex()

        # Initializing parameters
        version_par = 1
        error_cor_par = qrcode.constants.ERROR_CORRECT_L
        shape_par = SquareModuleDrawer()
        colormask_par = SolidFillColorMask()
        img_path_par = None
        rgb_color_from_par = (0, 0, 0)
        rgb_color_to_par = (0, 0, 0)
        rgb_background_par = (255, 255, 255)

        # Getting hex colors.
        hex_color_from = self.color_from_edit.text()
        hex_color_to = self.color_to_edit.text()
        hex_color_background = self.background_edit.text()

        # Cheking if HEX is valid and converting it to RGB
        if is_valid_hex_color(hex_color_from):
            rgb_color_from_par = ImageColor.getcolor(hex_color_from, "RGB")
        if is_valid_hex_color(hex_color_to):
            rgb_color_to_par = ImageColor.getcolor(hex_color_to, "RGB")
        if is_valid_hex_color(hex_color_background):
            rgb_background_par = ImageColor.getcolor(hex_color_background, "RGB")

        # Setting parameters according to informations given by user
        match error_correction:
            case 0:
                error_cor_par = qrcode.constants.ERROR_CORRECT_L
            case 1:
                error_cor_par = qrcode.constants.ERROR_CORRECT_M
            case 2:
                error_cor_par = qrcode.constants.ERROR_CORRECT_Q
            case 3:
                error_cor_par = qrcode.constants.ERROR_CORRECT_H

        match shape:
            case 0:
                shape_par = SquareModuleDrawer()
            case 1:
                shape_par = GappedSquareModuleDrawer()
            case 2:
                shape_par = CircleModuleDrawer()
            case 3:
                shape_par = RoundedModuleDrawer()
            case 4:
                shape_par = VerticalBarsDrawer()
            case 5:
                shape_par = HorizontalBarsDrawer()

        match colormask:
            case 0:
                colormask_par = SolidFillColorMask(back_color=rgb_background_par, front_color=rgb_color_from_par)
            case 1:
                colormask_par = SquareGradiantColorMask(back_color=rgb_background_par, center_color=rgb_color_from_par, edge_color=rgb_color_to_par)
            case 2:
                colormask_par = RadialGradiantColorMask(back_color=rgb_background_par, center_color=rgb_color_from_par, edge_color=rgb_color_to_par)
            case 3:
                colormask_par = VerticalGradiantColorMask(back_color=rgb_background_par, top_color=rgb_color_from_par, bottom_color=rgb_color_to_par)
            case 4:
                colormask_par = HorizontalGradiantColorMask(back_color=rgb_background_par, left_color=rgb_color_from_par, right_color=rgb_color_to_par)
            case 5:
                if self.selected_imgmask_path != "":
                    colormask_par = ImageColorMask(back_color=rgb_background_par, color_mask_path=self.selected_imgmask_path)


        if self.addimg_checkbox.isChecked() and self.selected_image_path != "":
            version_par = 3
            img_path_par = self.selected_image_path
        else:
            version_par = 1
            img_path_par = None

        # Creating QR code
        qr = qrcode.QRCode(version=version_par, error_correction=error_cor_par)
        qr.add_data(data)
        qr.make(fit=True)
        qrcode_image = qr.make_image(image_factory=StyledPilImage, module_drawer=shape_par, color_mask=colormask_par, embeded_image_path=img_path_par)
        self.canBeSaved = True
        qrcode_image.save('pixmappp.png')
        self.qrcode_save_img = qrcode_image
        self.qrcode_img.setPixmap(QPixmap('pixmappp.png'))

    def clicked_save(self):
        if self.canBeSaved:
            saving_path, _ = QFileDialog.getSaveFileName(self, 'Save file', "", "Image file (*.png)")
            self.qrcode_save_img.save(saving_path)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = QrCode()
    win.show()

    sys.exit(app.exec_())
