#!python
# -*- mode: python; Encoding: utf-8; coding: utf-8 -*-
# Last updated: <2016/10/28 10:08:12 +0900>

"""
PySide + QGraphicsView上でズーム表示する。
ホイールを回すか、ステータスバー上のボタンを押すとズームが変わる。
マウスカーソル位置にブラシ画像も表示する。
QGraphicsView の scale を変更してズームできるかテスト。

動作確認環境 : Windows10 x64 + Python 2.7.11 + PySide 1.2.4
"""

import sys
from PySide.QtCore import *
from PySide.QtGui import *

brushFile = "brush.png"
bgFile = "bg.jpg"
canvasSize = (640, 480)
padding = 48

# ズーム倍率 (単位は%。floatを使うと誤差がたまるのでint(整数)で管理する)
zoomValue = 100

status = None
zoomDisp = None
gView = None
myApp = None


class DrawAreaScene(QGraphicsScene):
    """ 描画ウインドウ用Scene """

    def __init__(self, *argv, **keywords):
        super(DrawAreaScene, self).__init__(*argv, **keywords)
        self.setBackgroundBrush(QColor(128, 128, 128, 255))  # 背景色を設定

        global brushFile
        global padding
        global bgFile
        global canvasSize

        # 画像読み込み
        self.canvasPixmap = QPixmap(bgFile)
        canvasSize = (self.canvasPixmap.width(), self.canvasPixmap.height())

        # 背景画像(余白込み)を生成
        sw = canvasSize[0] + (padding * 2)
        sh = canvasSize[1] + (padding * 2)
        self.bgPixmap = QPixmap(sw, sh)
        self.bgPixmap.fill(QColor(128, 128, 128, 255))

        # Scene に背景画像(余白込み)を追加
        self.bgItem = QGraphicsPixmapItem(self.bgPixmap)
        self.addItem(self.bgItem)
        self.bgItem.setOffset(0, 0)

        # Scene にキャンバス相当(ここでは画像)を追加
        # オフセットを余白分ずらしている
        self.canvasItem = QGraphicsPixmapItem(self.canvasPixmap)
        self.addItem(self.canvasItem)
        self.canvasItem.setOffset(padding, padding)

        # Scene にブラシ画像を追加
        self.brushPixmap = QPixmap(brushFile)
        self.brushItem = QGraphicsPixmapItem(self.brushPixmap)
        self.addItem(self.brushItem)

    def setVisibleBrush(self, flag):
        """ ブラシ表示の有効無効切り替え """
        self.brushItem.setVisible(flag)

    def changeBrushPos(self, pos):
        """ ブラシの表示位置を変更 """
        # ブラシが非表示だったら表示を有効化
        if not self.brushItem.isVisible():
            self.setVisibleBrush(True)

        pm = self.brushItem.pixmap()
        xd = (pm.width() / 2)
        yd = (pm.height() / 2)
        self.brushItem.setOffset(int(pos.x() - xd), int(pos.y() - yd))


class DrawAreaView(QGraphicsView):
    """ メインになるQGraphicsView """

    def __init__(self, *argv, **keywords):
        super(DrawAreaView, self).__init__(*argv, **keywords)
        self.setBackgroundBrush(QColor(64, 64, 64, 255))  # 背景色を設定
        self.setCacheMode(QGraphicsView.CacheBackground)

        # 描画更新の仕方を選択
        self.setViewportUpdateMode(QGraphicsView.SmartViewportUpdate)
        # self.setViewportUpdateMode(QGraphicsView.MinimalViewportUpdate)
        # self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

        self.oldCurPos = (0, 0)
        self.button = Qt.NoButton
        global zoomValue
        zoomValue = 100

        # Sceneを登録
        scene = DrawAreaScene(self)
        self.setScene(scene)
        self.setSceneNewRect()

        # 子のSceneに対してマウストラッキングを有効にすると
        # マウスカーソル移動時に常時 mouseMoveEvent() が呼ばれるようになる
        vp = self.viewport().setMouseTracking(True)

    def resizeEvent(self, event):
        """ リサイズ時に呼ばれる処理 """
        super(DrawAreaView, self).resizeEvent(event)
        self.setSceneNewRect()

    def setSceneNewRect(self):
        """
        Sceneの矩形を更新。
        キャンバス周辺に余白を設けたサイズを設定
        """
        global canvasSize
        global padding
        global zoomValue

        w, h = canvasSize
        w += padding * 2
        h += padding * 2
        # w *= (zoomValue / 100.0)
        # h *= (zoomValue / 100.0)
        rect = QRectF(0, 0, int(w), int(h))

        # Sceneの矩形を更新。自動でスクロールバーの長さも変わってくれる
        self.scene().setSceneRect(rect)

    def scrollContentsBy(self, dx, dy):
        """ スクロールバー操作時に呼ばれる処理 """
        # スクロール中、Scene内にブラシがあると何故かゴミが残るので、
        # ブラシを非表示にしてからスクロールさせている。
        self.scene().setVisibleBrush(False)
        super(DrawAreaView, self).scrollContentsBy(dx, dy)

    def mousePressEvent(self, event):
        """ マウスボタンを押した時の処理 """
        pos = self.getMousePos(event, "Click")
        self.button = event.button()
        self.oldCurPos = pos

        if event.buttons() & Qt.MidButton:
            # 中ボタンが押されてるならマウスカーソル形状を変更
            qApp.setOverrideCursor(Qt.ClosedHandCursor)

    def mouseReleaseEvent(self, event):
        """ マウスボタンを離した時の処理 """
        pos = self.getMousePos(event, "Release")
        self.button = Qt.NoButton

        # マウスカーソル形状を元に戻す
        qApp.restoreOverrideCursor()

    def mouseMoveEvent(self, event):
        """ マウスを動かしてる時に呼ばれる処理 """
        # マウストラッキングが有効になってるので、ドラッグ時以外も呼ばれる

        if self.button == Qt.NoButton:
            # 何のボタンも押されてない。マウスカーソル移動のみ
            pos = self.getMousePos(event, "Move")
            self.changeBrushPos(pos)
        elif self.button == Qt.LeftButton:
            # 左ドラッグ
            pos = self.getMousePos(event, "Drag")
            self.changeBrushPos(pos)
        elif self.button == Qt.MidButton:
            # 中ボタンドラッグなのでスクロール処理
            pos = self.getMousePos(event, "Drag")

            # 前回の座標位置との差を求める
            mv = self.oldCurPos - pos
            self.oldCurPos = pos

            # スクロールバーの値を変更
            self.addScrollBarValue(mv.x(), mv.y())

    def addScrollBarValue(self, dx, dy):
        """ スクロールバーの現在値を変化させる """
        x = self.horizontalScrollBar().value()
        y = self.verticalScrollBar().value()
        self.horizontalScrollBar().setValue(x + dx)
        self.verticalScrollBar().setValue(y + dy)

    def getMousePos(self, event, msg):
        """ マウス座標を取得 """
        x = event.pos().x()
        y = event.pos().y()

        kind = ""
        if event.buttons() & Qt.LeftButton:
            kind = "Left "
        if event.button() & Qt.MidButton:
            kind += "Mid "
        if event.button() & Qt.RightButton:
            kind += "Right "

        global status
        status.showMessage("(%d , %d) %s %s" % (x, y, kind, msg))
        return event.pos()

    def changeBrushPos(self, pos):
        """ ブラシ表示位置を変更 """
        # mapToScene() を使えば、シーン用の座標に変換してくれる
        scenePos = self.mapToScene(pos)
        self.scene().changeBrushPos(scenePos)

    def wheelEvent(self, event):
        """ マウスホイール回転時の処理。ズーム変更 """
        global status
        status.showMessage("wheel %f" % event.delta())
        
        # ズーム率(単位は%)を取得
        v = self.changeZoomValue(pow(1.2, event.delta() / 240.0)) / 100.0

        # 与えた座標値(QgraphicsView用)をシーン上での座標値に変換
        p0 = self.mapToScene(event.pos())

        # スケール変更
        self.resetMatrix()
        self.scale(v, v)
        # self.setSceneNewRect()

        # 与えた座標値(シーン用)を QGraphicsView用の座標値に変換
        p1 = self.mapFromScene(p0)

        # ズーム変更前後のマウスカーソル座標の差をスクロールバーに反映
        # これをすることで、マウスカーソル位置を基準にズームしてるように見える
        mv = p1 - event.pos()
        self.addScrollBarValue(mv.x(), mv.y())

    def changeZoomRatio(self, d):
        """ 外部から与えられた値でズーム変更 """
        v = self.changeZoomValue(pow(1.2, d)) / 100.0
        self.resetMatrix()
        self.scale(v, v)
        # self.setSceneNewRect()

    def changeZoomValue(self, d):
        """ ズーム率の変数を変更 """
        global zoomValue
        return self.clipZoomValue(zoomValue * d)

    def clipZoomValue(self, zv):
        global zoomDisp
        global zoomValue
        zoomValue = max(10, min(zv, 3200))  # 10 - 3200の範囲にする
        zvi = int(zoomValue)
        zoomDisp.setText("%5d%s" % (zvi, '%'))
        return zvi

    def fitZoom(self):
        """ ウインドウサイズに合わせてズーム変更 """
        cr = self.scene().sceneRect()
        vr = self.viewport().rect()
        ax = float(vr.width()) * 100.0 / float(cr.width())
        ay = float(vr.height()) * 100.0 / float(cr.height())
        if ax <= ay:
            # 横方向で合わせる
            zv = ax
        else:
            # 縦方向で合わせる
            zv = ay

        v = self.clipZoomValue(zv) / 100.0
        self.resetMatrix()
        self.scale(v, v)

    def zoomActualPixels(self):
        """ 等倍表示 """
        v = self.clipZoomValue(100) / 100.0
        self.resetMatrix()
        self.scale(v, v)


class MyMainWindow(QMainWindow):
    """ メインウインドウ """

    def __init__(self, *argv, **keywords):
        super(MyMainWindow, self).__init__(*argv, **keywords)
        self.setWindowTitle("Zoom and Mouse Tracking Test 2")
        self.resize(640, 480)

        self.initMenuBar()  # メニューバー
        self.initStatusBar()  # ステータスバー

        # 中央Widget
        global gView
        gView = DrawAreaView(self)
        self.gView = gView
        self.setCentralWidget(gView)

    def initMenuBar(self):
        """ メニューバー初期化 """
        mb = QMenuBar()
        file_menu = QMenu("&File", self)
        exit_action = file_menu.addAction("&Close")
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(qApp.quit)
        mb.addMenu(file_menu)
        self.setMenuBar(mb)

    def initStatusBar(self):
        """ ステータスバー初期化 """
        global status
        global zoomDisp
        status = QStatusBar(self)
        self.setStatusBar(status)

        # 縮小ボタン
        zoomOutBtn = QPushButton("-", self.statusBar())
        zoomOutBtn.setFixedWidth(24)

        # 拡大ボタン
        zoomInBtn = QPushButton("+", self.statusBar())
        zoomInBtn.setFixedWidth(24)

        # ウインドウに合わせるボタン
        zoomFitBtn = QPushButton("FIT", self.statusBar())
        zoomFitBtn.setFixedWidth(36)

        zoomActualBtn = QPushButton("1:1", self.statusBar())
        zoomActualBtn.setFixedWidth(36)

        # 倍率表示。QLabelだが、等倍表示するボタン相当としても使う
        zoomDisp = QLabel("100%", self.statusBar())
        zoomDisp.setFixedWidth(80)
        zoomDisp.setFrameStyle(QFrame.Box | QFrame.Sunken)
        zoomDisp.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        # ステータスバーに追加
        self.statusBar().addPermanentWidget(zoomOutBtn)
        self.statusBar().addPermanentWidget(zoomDisp)
        self.statusBar().addPermanentWidget(zoomInBtn)
        self.statusBar().addPermanentWidget(zoomFitBtn)
        self.statusBar().addPermanentWidget(zoomActualBtn)

        status.showMessage("Here is the status bar.")

        # ボタンが押されたときの処理を登録
        zoomOutBtn.clicked.connect(self.zoomOut)
        zoomInBtn.clicked.connect(self.zoomIn)
        zoomFitBtn.clicked.connect(self.zoomFit)
        zoomActualBtn.clicked.connect(self.zoomActualPixels)

        # QLabel にマウスクリックイベントを割り当てるなら、こう書く
        zoomDisp.mousePressEvent = self.zoomActualPixelsEvent

    def zoomOut(self):
        """ 縮小ボタンを押した時の処理 """
        self.gView.changeZoomRatio(-2.0)

    def zoomIn(self):
        """ 拡大ボタンを押した時の処理 """
        self.gView.changeZoomRatio(2.0)

    def zoomFit(self):
        """ ウインドウに合わせるボタンを押した時の処理 """
        self.gView.fitZoom()

    def zoomActualPixels(self):
        """ 等倍表示 """
        self.gView.zoomActualPixels()

    def zoomActualPixelsEvent(self, event):
        """ 等倍表示 """
        self.gView.zoomActualPixels()

def main():
    """ メイン処理 """

    # このあたりを指定すると描画が速くなるという話を見かけたが、
    # "native"、"raster"、"opengl" を指定しても結果は変わらなかった…
    QApplication.setGraphicsSystem("raster")

    app = QApplication(sys.argv)
    w = MyMainWindow()
    w.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
