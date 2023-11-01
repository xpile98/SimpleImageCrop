import os
import sys
import time

import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, \
    QFileDialog, QRadioButton, QGroupBox, QLineEdit, QGraphicsView, QGraphicsScene, QMessageBox
from PyQt5.QtGui import QPixmap, QImage, QPainter
from PyQt5.QtCore import QTimer, QCoreApplication
import numpy as np

class CropWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Image Cropper")
        self.setGeometry(100, 100, 600, 600)

        # 폴더 선택
        self.folder_path = None
        self.folder_label = QLabel("폴더를 선택하세요.")
        self.folder_button = QPushButton("폴더 선택")
        self.folder_button.clicked.connect(self.select_folder)

        # CROP ROI 입력
        self.width_label = QLabel("Width:")
        self.width_input = QLineEdit()
        self.width_input.setText("0")
        self.width_input.textChanged.connect(self.update_roi_preview)

        self.height_label = QLabel("Height:")
        self.height_input = QLineEdit()
        self.height_input.setText("0")
        self.height_input.textChanged.connect(self.update_roi_preview)


        # 중심 좌표 지정
        self.center_group = QGroupBox("중심 좌표 지정")

        self.center_radio1 = QRadioButton("이미지 중심")
        self.center_radio1.setChecked(True)
        self.center_radio2 = QRadioButton("이미지 중심 + offset (Width, Height)")
        self.center_radio3 = QRadioButton("절대 좌표 (Width, Height)")

        self.center_layout = QVBoxLayout()
        self.center_layout.addWidget(self.center_radio1)
        self.center_layout.addWidget(self.center_radio2)
        self.center_layout.addWidget(self.center_radio3)
        self.center_group.setLayout(self.center_layout)

        self.x_offset_label = QLabel("X Offset:")
        self.x_offset_input = QLineEdit()
        self.x_offset_label.setEnabled(False)
        self.x_offset_input.setEnabled(False)
        self.x_offset_input.setText("0")
        self.x_offset_input.textChanged.connect(self.update_roi_preview)

        self.y_offset_label = QLabel("Y Offset:")
        self.y_offset_input = QLineEdit()
        self.y_offset_label.setEnabled(False)
        self.y_offset_input.setEnabled(False)
        self.y_offset_input.setText("0")
        self.y_offset_input.textChanged.connect(self.update_roi_preview)

        self.center_radio2.toggled.connect(self.toggle_offset_controls)
        self.center_radio3.toggled.connect(self.toggle_absolute_controls)

        self.center_radio1.toggled.connect(self.update_roi_preview)
        self.center_radio2.toggled.connect(self.update_roi_preview)
        self.center_radio3.toggled.connect(self.update_roi_preview)



        # 크롭 동작 버튼
        self.crop_button = QPushButton("크롭")
        self.crop_button.clicked.connect(self.crop_images)

        # 이미지 뷰어
        self.image_viewer = QGraphicsView()
        self.image_viewer.setFixedHeight(600)  # 이미지 뷰어의 크기를 800x800 픽셀로 설정
        self.image_scene = QGraphicsScene()
        self.image_viewer.setScene(self.image_scene)
        self.image_viewer.setRenderHint(QPainter.Antialiasing)  # 안티앨리어싱 설정

        # ROI 표시를 위한 변수
        self.start_point = None
        self.end_point = None
        self.drawing_roi = False

        # UI 배치
        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.folder_label)
        self.main_layout.addWidget(self.folder_button)
        self.main_layout.addWidget(self.width_label)
        self.main_layout.addWidget(self.width_input)
        self.main_layout.addWidget(self.height_label)
        self.main_layout.addWidget(self.height_input)
        self.main_layout.addWidget(self.center_group)
        self.main_layout.addWidget(self.x_offset_label)
        self.main_layout.addWidget(self.x_offset_input)
        self.main_layout.addWidget(self.y_offset_label)
        self.main_layout.addWidget(self.y_offset_input)
        self.main_layout.addWidget(self.crop_button)
        self.main_layout.addWidget(self.image_viewer)
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)
        # Previous and Next Buttons
        self.prev_button = QPushButton("Previous")
        self.prev_button.clicked.connect(self.load_previous_image)
        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.load_next_image)

        # Add previous and next buttons to the layout
        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.prev_button)
        self.button_layout.addWidget(self.next_button)
        self.main_layout.addLayout(self.button_layout)

        # ...

        self.current_image_index = 0
        self.image_paths = []

    def load_image_paths(self):
        if self.folder_path:
            self.current_image_index = 0
            self.image_paths = []
            for root, _, files in os.walk(self.folder_path):
                for filename in files:
                    if filename.endswith(('.jpg', '.jpeg', '.png', '.bmp')):
                        file_path = os.path.join(root, filename).replace('\\', '/')

                        # encoded_path = np.fromfile(file_path, dtype=np.uint8)
                        self.image_paths.append(file_path)

    def load_previous_image(self):
        if self.current_image_index > 0:
            self.current_image_index -= 1
            self.load_and_display_image(self.image_paths[self.current_image_index])
            self.update_roi_preview()

    def load_next_image(self):
        if self.current_image_index < len(self.image_paths) - 1:
            self.current_image_index += 1
            self.load_and_display_image(self.image_paths[self.current_image_index])
            self.update_roi_preview()

    def select_folder(self):
        self.folder_path = QFileDialog.getExistingDirectory(self, "폴더 선택")
        self.folder_label.setText("선택한 폴더: " + self.folder_path)

        QCoreApplication.processEvents()  # 이벤트 루프를 실행하여 UI 업데이트가 발생하도록 함
        self.adjustSize()

        self.width_input.setText("0")
        self.height_input.setText("0")
        self.x_offset_input.setText("0")
        self.y_offset_input.setText("0")

        # Load image paths
        self.load_image_paths()

        # Display the first image
        if len(self.image_paths) > 0:
            self.load_and_display_image(self.image_paths[self.current_image_index])
        else:
            QMessageBox.critical(self, "오류", "폴더 내에 이미지가 없습니다.")

        """
        # 폴더 선택 후 첫 번째 이미지를 로드하여 뷰어에 표시 
        first_image_path = self.get_first_image_path()
        if first_image_path:
            self.load_and_display_image(first_image_path)
        """

    def get_first_image_path(self):
        if self.folder_path:
            for root, _, files in os.walk(self.folder_path):
                for filename in files:
                    if filename.endswith(('.jpg', '.jpeg', '.png', '.bmp')):
                        return os.path.join(root, filename).replace('\\', '/')
        return None

    def toggle_offset_controls(self, checked):
        self.x_offset_label.setText("X Offset:")
        self.y_offset_label.setText("Y Offset:")
        self.x_offset_label.setEnabled(checked)
        self.x_offset_input.setEnabled(checked)
        self.y_offset_label.setEnabled(checked)
        self.y_offset_input.setEnabled(checked)

    def toggle_absolute_controls(self, checked):
        self.x_offset_label.setText("X Pos:")
        self.y_offset_label.setText("Y Pos:")
        self.x_offset_label.setEnabled(checked)
        self.x_offset_input.setEnabled(checked)
        self.y_offset_label.setEnabled(checked)
        self.y_offset_input.setEnabled(checked)

    def crop_images(self):
        if self.folder_path is None:
            return

        width = int(self.width_input.text())
        height = int(self.height_input.text())

        if self.center_radio1.isChecked():
            center_mode = "center"
            x_offset = 0
            y_offset = 0
        elif self.center_radio2.isChecked():
            center_mode = "center_offset"
            x_offset = int(self.x_offset_input.text())
            y_offset = int(self.y_offset_input.text())
        else:
            center_mode = "absolute"
            x_offset = int(self.x_offset_input.text())
            y_offset = int(self.y_offset_input.text())

        output_root = self.folder_path + "_crop"
        os.makedirs(output_root, exist_ok=True)

        for root, _, files in os.walk(self.folder_path):
            for filename in files:
                if filename.endswith(('.jpg', '.jpeg', '.png', '.bmp')):
                    file_path = os.path.join(root, filename).replace('\\', '/')

                    encoded_path = np.fromfile(file_path, dtype=np.uint8)
                    image = cv2.imdecode(encoded_path, cv2.IMREAD_COLOR)
                    # image = cv2.imread(encoded_path)

                    if image is None:
                        continue

                    image_height, image_width = image.shape[:2]

                    if center_mode == "center":
                        x = image_width // 2 - width // 2
                        y = image_height // 2 - height // 2
                    elif center_mode == "center_offset":
                        x = image_width // 2 - width // 2 + x_offset
                        y = image_height // 2 - height // 2 + y_offset
                    else:
                        x = x_offset
                        y = y_offset

                    if x < 0:
                        x = 0
                    if y < 0:
                        y = 0
                    if x + width > image_width:
                        x = image_width - width
                    if y + height > image_height:
                        y = image_height - height

                    cropped_image = image[y:y+height, x:x+width]

                    relative_output_folder = os.path.relpath(root, self.folder_path)
                    output_folder = os.path.join(output_root, relative_output_folder)
                    os.makedirs(output_folder, exist_ok=True)
                    output_path = os.path.join(output_folder, filename)
                    # cv2.imwrite(output_path, cropped_image)

                    extension = os.path.splitext(filename)[1]  # 이미지 확장자
                    result, encoded_img = cv2.imencode(extension, cropped_image)

                    if result:
                        with open(output_path, mode='w+b') as f:
                            encoded_img.tofile(f)

        QMessageBox.information(self, "Information", "크롭이 완료되었습니다.")
        # self.folder_label.setText("크롭이 완료되었습니다.")
        self.show_image(None)  # 이미지 뷰어 초기화

    def load_and_display_image(self, image_path):
        # image = cv2.imread(image_path)
        encoded_path = np.fromfile(image_path, dtype=np.uint8)
        image = cv2.imdecode(encoded_path, cv2.IMREAD_COLOR)
        if image is not None:
            self.show_image(image)

    def show_image(self, image):
        if image is None:
            self.image_scene.clear()
        else:
            viewer_width = self.image_viewer.width() - 2  # 2 픽셀 여백 제거
            viewer_height = self.image_viewer.height() - 2  # 2 픽셀 여백 제거
            viewer_aspect_ratio = viewer_width / viewer_height
            image_aspect_ratio = image.shape[1] / image.shape[0]

            if viewer_aspect_ratio >= image_aspect_ratio:
                # 이미지가 뷰어보다 너비가 작거나 같을 때
                if image.shape[0] > viewer_height:
                    scaled_height = viewer_height
                    scaled_width = int(viewer_height * image_aspect_ratio)
                else:
                    scaled_height = image.shape[0]
                    scaled_width = image.shape[1]
            else:
                # 이미지가 뷰어보다 높이가 작을 때
                if image.shape[1] > viewer_width:
                    scaled_width = viewer_width
                    scaled_height = int(viewer_width / image_aspect_ratio)
                else:
                    scaled_width = image.shape[1]
                    scaled_height = image.shape[0]

            scaled_image = cv2.resize(image, (scaled_width, scaled_height))
            qimage = QImage(scaled_image.data, scaled_image.shape[1], scaled_image.shape[0], scaled_image.shape[1] * 3,
                            QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qimage)
            self.image_scene.clear()
            self.image_scene.addPixmap(pixmap)
            self.image_scene.setSceneRect(0, 0, pixmap.width(), pixmap.height())  # 스크롤 없이 이미지 전체가 표시되도록 설정

    def update_roi_preview(self):
        if self.folder_path is None:
            return

        width_text = self.width_input.text()
        height_text = self.height_input.text()
        if width_text == '' or height_text == '' or int(width_text) <= 0 or int(height_text) <= 0:
            return

        try:
            width = int(width_text)
            height = int(height_text)
        except ValueError:
            QMessageBox.critical(self, "오류", "정수를 입력해주세요.")
            return

        if self.center_radio1.isChecked():
            center_mode = "center"
            x_offset = 0
            y_offset = 0
        else:
            x_offset_text = self.x_offset_input.text()
            y_offset_text = self.y_offset_input.text()
            if x_offset_text == '' or y_offset_text == '' or x_offset_text == '-' or y_offset_text == '-':
                return

            try:
                x_offset = int(self.x_offset_input.text())
                y_offset = int(self.y_offset_input.text())
            except ValueError:
                QMessageBox.critical(self, "오류", "정수를 입력해주세요.")
                return

            if self.center_radio2.isChecked():
                center_mode = "center_offset"
            else:
                center_mode = "absolute"

        image_path = self.image_paths[self.current_image_index]
        if len(image_path) > 0:
            # encoded_path = np.fromfile(image_path, dtype=np.uint8)
            # image = cv2.imread(encoded_path)
            encoded_path = np.fromfile(image_path, dtype=np.uint8)
            image = cv2.imdecode(encoded_path, cv2.IMREAD_COLOR)
            if image is not None:
                if center_mode == "center":
                    x = image.shape[1] // 2 - width // 2
                    y = image.shape[0] // 2 - height // 2
                elif center_mode == "center_offset":
                    x = image.shape[1] // 2 - width // 2 + x_offset
                    y = image.shape[0] // 2 - height // 2 + y_offset
                else:
                    x = x_offset
                    y = y_offset

                x = max(0, min(x, image.shape[1] - width))
                y = max(0, min(y, image.shape[0] - height))

                cv2.rectangle(image, (x, y), (x + width, y + height), (255, 0, 0), 5)
                self.show_image(image)

                # 전체 이미지를 blur 처리
                blurred_image = cv2.GaussianBlur(image, (71, 71), 0)

                # ROI 영역 내부는 blur 처리하지 않고 ROI 외부만 blur 처리
                mask = np.zeros_like(image)
                mask[y:y + height, x:x + width] = 1
                result_image = np.where(mask == 1, image, blurred_image)

                # blur 처리된 이미지를 표시
                self.show_image(result_image)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CropWindow()
    window.show()
    sys.exit(app.exec_())
