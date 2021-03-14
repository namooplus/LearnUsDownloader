import sys
import requests
import m3u8
import shutil

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from bs4 import BeautifulSoup

style = """
    QWidget {
        background-color: transparent;
    }
    QWidget#window {
        background-color: #CCffffff;
    }
    QWidget#content {
        background-color: #ffffff;
    }
    QWidget#warning {
        color: red;
    }
    QLineEdit {
        background-color: transparent;
        border-style: none;
        border-bottom: 1px solid gray;
    }
    QLineEdit:focus {
        background-color: transparent;
        border-style: none;
        border-bottom: 1px solid #2dd6c2;
    }
    QLineEdit:disabled {
        background-color: transparent;
        border-style: none;
        border-bottom: 1px solid #dbdbdb;
    }
    QWidget#selector {
        padding: 5px;
        color: black;
        background-color: white;
        border-style: solid;
    }
    QWidget#selector:pressed {
        padding: 5px;
        color: black;
        background-color: #e6e6e6;
        border-style: solid;
    }
    QWidget#selector:disabled {
        padding: 5px;
        color: black;
        background-color: #dbdbdb;
        border-style: solid;
    }
    QWidget#positiveButton {
        color: white;
        background-color: #2dd6c2;
        border-style: solid;
    }
    QWidget#positiveButton:pressed {
        color: white;
        background-color: #1fb8a6;
        border-style: solid;
    }
    QWidget#positiveButton:disabled {
        color: white;
        background-color: #dbdbdb;
        border-style: solid;
    }
    QWidget#negativeButton {
        color: white;
        background-color: #e6605c;
        border-style: solid;
    }
    QWidget#negativeButton:pressed {
        color: white;
        background-color: #d14c47;
        border-style: solid;
    }
"""


class Header(QWidget):
    """헤더"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        # 타이틀
        title = QLabel('LearnUs\nDownloader', self)
        titleFont = title.font()
        titleFont.setPointSize(22)
        titleFont.setBold(True)
        title.setFont(titleFont)

        # 레이아웃
        headerLayout = QVBoxLayout()
        headerLayout.setContentsMargins(30, 30, 30, 30)
        headerLayout.addStretch(1)
        headerLayout.addWidget(title)
        headerLayout.addStretch(1)

        self.setLayout(headerLayout)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.parent.is_moving = True
            self.parent.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.parent.is_moving:
            self.parent.move(event.globalPos() - self.parent.offset)


class Content(QWidget):
    """내용"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.initEffect()
        self.initUI()

    def initEffect(self):
        self.shadowEffect1 = QGraphicsDropShadowEffect()
        self.shadowEffect1.setBlurRadius(20)
        self.shadowEffect1.setOffset(0, 0)

        self.shadowEffect2 = QGraphicsDropShadowEffect()
        self.shadowEffect2.setBlurRadius(20)
        self.shadowEffect2.setOffset(0, 0)

        self.shadowEffect3 = QGraphicsDropShadowEffect()
        self.shadowEffect3.setBlurRadius(20)
        self.shadowEffect3.setOffset(0, 0)

        self.shadowEffect4 = QGraphicsDropShadowEffect()
        self.shadowEffect4.setBlurRadius(20)
        self.shadowEffect4.setOffset(0, 0)

    def initUI(self):
        # 설명
        guide = QLabel('LearnUs Downloader는 LearnUs 내 강의 동영상을 다운로드할 수 있도록 도와줍니다.\n'
                       '하단에 저장할 파일의 이름, 위치 그리고 강의 소스를 입력한 후 다운로드를 클릭합니다.', self)

        # 경고
        warning = QLabel('본 프로그램의 목적은 강의 오프라인 재생 및 수업 복습 용 영상 확인입니다.\n'
                         '강의 영상 공유, 영리 행위를 포함한 모든 불법 행위는 엄격히 금지됩니다.', self)
        warning.setObjectName('warning')
        warning.setContentsMargins(0, 0, 0, 20)

        # 입력
        nameGuide = QLabel('저장 이름 : ', self)
        self.parent.nameState = QLineEdit(self)
        self.parent.nameState.setPlaceholderText('런어스 강의영상 n주차')
        self.parent.nameState.setAttribute(Qt.WA_MacShowFocusRect, False)
        nameLayout = QHBoxLayout()
        nameLayout.addWidget(nameGuide)
        nameLayout.addWidget(self.parent.nameState)

        addressGuide = QLabel('강의 소스 :', self)
        self.parent.addressButton = QPushButton('붙여넣기', self)
        self.parent.addressButton.setObjectName('selector')
        self.parent.addressButton.setGraphicsEffect(self.shadowEffect1)
        self.parent.addressButton.clicked.connect(self.parent.pasteSource)
        self.parent.addressState = QLabel('올바르지 않은 소스입니다.', self)
        self.parent.addressState.setStyleSheet('color: #e6605c')
        addressLayout = QHBoxLayout()
        addressLayout.addWidget(addressGuide)
        addressLayout.addWidget(self.parent.addressButton)
        addressLayout.addWidget(self.parent.addressState)
        addressLayout.addStretch(1)

        locationGuide = QLabel('저장 위치 :', self)
        self.parent.locationButton = QPushButton('지정되지 않음', self)
        self.parent.locationButton.setObjectName('selector')
        self.parent.locationButton.setGraphicsEffect(self.shadowEffect2)
        self.parent.locationButton.clicked.connect(self.parent.selectFolder)
        locationLayout = QHBoxLayout()
        locationLayout.addWidget(locationGuide)
        locationLayout.addWidget(self.parent.locationButton)
        locationLayout.addStretch(1)

        # 상태
        self.parent.state = QLabel('다운로드 대기 중입니다. (v 1.0.1)', self)

        # 버튼
        self.parent.download = QPushButton('다운로드', self)
        self.parent.download.setObjectName('positiveButton')
        self.parent.download.setGraphicsEffect(self.shadowEffect3)
        self.parent.download.setFixedWidth(100)
        self.parent.download.setFixedHeight(40)
        self.parent.download.clicked.connect(self.parent.downloadVideo)
        q = QPushButton('종료', self)
        q.setObjectName('negativeButton')
        q.setGraphicsEffect(self.shadowEffect4)
        q.setFixedWidth(100)
        q.setFixedHeight(40)
        q.clicked.connect(QCoreApplication.instance().quit)

        # 푸터
        footer = QHBoxLayout()
        footer.setContentsMargins(0, 50, 0, 0)
        footer.addWidget(self.parent.state)
        footer.addStretch(1)
        footer.addWidget(self.parent.download)
        footer.addWidget(q)

        # 레이아웃
        childWidget = QWidget()
        childWidget.setObjectName('content')
        child = QVBoxLayout(childWidget)
        child.setContentsMargins(30, 30, 30, 30)
        child.addWidget(guide)
        child.addWidget(warning)
        child.addLayout(nameLayout)
        child.addLayout(addressLayout)
        child.addLayout(locationLayout)
        child.addLayout(footer)

        contentLayout = QVBoxLayout()
        contentLayout.addWidget(childWidget)
        contentLayout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(contentLayout)


class DownloadThread(QThread):
    """다운로드 쓰레드"""
    signal = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent

    def run(self):
        # 다운로드 준비
        videoSegments = m3u8.load(self.parent.address, verify_ssl=False).segments
        videoUrl = self.parent.address.strip('index.m3u8')
        videoName = self.parent.locationButton.text() + '/' + self.parent.nameState.text() + '.mp4'

        # 다운로드
        with open(videoName, 'wb') as f:
            for i in range(0, len(videoSegments)):
                piece = requests.get(videoUrl + videoSegments[i].uri, stream=True)
                shutil.copyfileobj(piece.raw, f)
                self.signal.emit(int((i + 1) / len(videoSegments) * 100))

        # 다운로드 완료
        self.parent.nameState.setEnabled(True)
        self.parent.addressButton.setEnabled(True)
        self.parent.locationButton.setEnabled(True)
        self.parent.download.setEnabled(True)


class LearnUsDownloader(QWidget):
    """창"""
    def __init__(self):
        super().__init__()
        self.address = ''
        self.initUI()

    def initUI(self):
        # 레이아웃 설정
        header = Header(self)
        content = Content(self)

        parentLayout = QHBoxLayout()
        parentLayout.setContentsMargins(0, 0, 0, 0)
        parentLayout.addWidget(header)
        parentLayout.addWidget(content)

        # 창 설정
        self.setWindowTitle('LearnUs Downloader')
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet(style)
        self.setContentsMargins(0, 0, 0, 0)
        self.setObjectName('window')
        self.setLayout(parentLayout)
        self.setWindowCenter()
        self.show()

    def setWindowCenter(self):
        frame = self.frameGeometry()
        screenCenter = QDesktopWidget().availableGeometry().center()
        frame.moveCenter(screenCenter)
        self.move(frame.topLeft())

    def selectFolder(self):
        folderName = QFileDialog.getExistingDirectory(self, '폴더를 선택하세요')
        if folderName != '':
            self.locationButton.setText(folderName)

    def pasteSource(self):
        source = QApplication.clipboard().text()
        result = BeautifulSoup(source, 'lxml').find('source')
        if result is None:
            self.address = ''
            self.addressState.setText('올바르지 않은 소스입니다.')
            self.addressState.setStyleSheet('color: #e6605c')
            return
        self.address = result.get('src')
        self.addressState.setText('올바른 소스입니다.')
        self.addressState.setStyleSheet('color: #2dd6c2')

    def downloadVideo(self):
        if self.address == '' or self.nameState.text() == '' or self.locationButton.text() == '지정되지 않음':
            self.state.setText('오류 : 폼을 모두 채워주세요!')
            return

        self.nameState.setEnabled(False)
        self.addressButton.setEnabled(False)
        self.locationButton.setEnabled(False)
        self.download.setEnabled(False)

        self.downloadThread = DownloadThread(self)
        self.downloadThread.signal.connect(self.updateStatus)
        self.startDownload()

    @pyqtSlot()
    def startDownload(self):
        self.downloadThread.start()

    @pyqtSlot(int)
    def updateStatus(self, progress):
        if progress == 100:
            self.state.setText('다운로드에 성공하였습니다!')
        else:
            self.state.setText('다운로드 중... (' + str(progress) + '%)')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = LearnUsDownloader()
    app.exec_()
